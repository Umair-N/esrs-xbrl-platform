'use client';

import { useEffect, useMemo, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import {
  CalendarIcon,
  Edit,
  Loader2,
  Plus,
  RefreshCw,
  Trash2,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Calendar } from '@/components/ui/calendar';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { Switch } from '@/components/ui/switch';
import { useToast } from '@/components/ui/use-toast';

import { cn, generateUniqueId } from '@/lib/utils';

// hooks
import { useContexts } from '@/features/contexts/api/list-contexts';
import { useCreateContext } from '@/features/contexts/api/create-context';
import { useDeleteContext } from '@/features/contexts/api/delete-taxonomy';

// --- Types aligned with backend ---
type PeriodType = 'instant' | 'duration' | 'forever';
type ContextStatus = 'valid' | 'warning' | 'error';

type XBRLContextOut = {
  id: number;
  user_id: number;
  context_id: string;
  entity_scheme: string;
  entity_identifier: string;
  entity_name?: string | null;
  lei?: string | null;
  period_type: PeriodType;
  start_date?: string | null;
  end_date?: string | null;
  instant_date?: string | null;
  dimensions_json?: Record<string, any> | null;
  taxonomy_id?: number | null;
  content_hash: string;
  is_default_context: boolean;
  status: ContextStatus;
  validation_messages?: Array<Record<string, any>> | null;
  created_at: string;
  updated_at: string;
};

// --- New-context form state ---
type NewContextForm = {
  entityName: string;
  entityScheme: string;
  entityIdentifier: string;
  periodType: Exclude<PeriodType, 'forever'>; // UI supports instant or duration for now
  instantDate?: Date;
  startDate?: Date;
  endDate?: Date;
  taxonomyId?: string;
};

export default function ContextsPage() {
  const { toast } = useToast();
  const queryClient = useQueryClient();

  // ---------- Filters (server + client) ----------
  const [entityIdFilter, setEntityIdFilter] = useState('');
  const [periodFilter, setPeriodFilter] = useState<
    'all' | 'instant' | 'duration'
  >('all');
  const [taxonomyFilter, setTaxonomyFilter] = useState<string>('');
  const [onlyDefault, setOnlyDefault] = useState(false);

  // debounce entity_identifier a bit for nicer UX
  const [debouncedEntityId, setDebouncedEntityId] = useState('');
  useEffect(() => {
    const t = setTimeout(
      () => setDebouncedEntityId(entityIdFilter.trim()),
      300
    );
    return () => clearTimeout(t);
  }, [entityIdFilter]);

  const { data, isLoading, isError, error } = useContexts({
    entity_identifier: debouncedEntityId || undefined,
    period_type: periodFilter === 'all' ? undefined : periodFilter,
    taxonomy_id: taxonomyFilter ? Number(taxonomyFilter) : undefined,
    is_default_context: onlyDefault ? true : undefined,
    limit: 200,
  });

  // ---------- Create ----------
  const [form, setForm] = useState<NewContextForm>({
    entityName: '',
    entityScheme: 'http://www.sec.gov/CIK',
    entityIdentifier: '',
    periodType: 'instant',
    instantDate: new Date(),
    startDate: new Date(),
    endDate: new Date(),
    taxonomyId: '',
  });

  const canCreate = useMemo(() => {
    const hasCore =
      !!form.entityName && !!form.entityIdentifier && !!form.entityScheme;
    if (!hasCore) return false;
    if (form.periodType === 'instant') return !!form.instantDate;
    return !!form.startDate && !!form.endDate && form.startDate <= form.endDate;
  }, [form]);

  const createContext = useCreateContext({
    mutationConfig: {
      onSuccess: () => {
        toast({
          title: 'Context created',
          description: 'Your context is now available for tagging.',
        });
      },
      onError: (err: any) => {
        toast({
          title: 'Create failed',
          description:
            err?.response?.data?.detail || err?.message || 'Unknown error',
          variant: 'destructive',
        });
      },
    },
  });

  function yyyyMmDd(d?: Date) {
    return d ? format(d, 'yyyy-MM-dd') : null;
  }

  async function handleCreateContext() {
    if (!canCreate) {
      toast({
        title: 'Missing fields',
        description: 'Fill Entity Name, Identifier, and the period date(s).',
        variant: 'destructive',
      });
      return;
    }
    const contextId = `ctx-${generateUniqueId().slice(0, 8)}`;

    const payload = {
      context_id: contextId,
      entity_scheme: form.entityScheme,
      entity_identifier: form.entityIdentifier,
      entity_name: form.entityName || undefined,
      lei: undefined,
      period_type: form.periodType,
      start_date:
        form.periodType === 'duration' ? yyyyMmDd(form.startDate) : null,
      end_date: form.periodType === 'duration' ? yyyyMmDd(form.endDate) : null,
      instant_date:
        form.periodType === 'instant' ? yyyyMmDd(form.instantDate) : null,
      dimensions_json: null, // optional for now
      taxonomy_id: form.taxonomyId ? Number(form.taxonomyId) : null,
      is_default_context: false,
      status: 'valid' as const,
      validation_messages: [],
    };

    await createContext.mutateAsync(payload);

    setForm({
      entityName: '',
      entityScheme: 'http://www.sec.gov/CIK',
      entityIdentifier: '',
      periodType: 'instant',
      instantDate: new Date(),
      startDate: new Date(),
      endDate: new Date(),
      taxonomyId: '',
    });
  }

  // ---------- Delete ----------
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [toDeleteId, setToDeleteId] = useState<number | null>(null);

  const deleteContext = useDeleteContext({
    mutationConfig: {
      onSuccess: () => {
        toast({ title: 'Context deleted' });
      },
      onError: (err: any) => {
        toast({
          title: 'Delete failed',
          description:
            err?.response?.data?.detail || err?.message || 'Unknown error',
          variant: 'destructive',
        });
      },
    },
  });

  function askDelete(id: number) {
    setToDeleteId(id);
    setDeleteOpen(true);
  }
  function confirmDelete() {
    if (toDeleteId == null) return;
    deleteContext.mutate({ id: toDeleteId });
    setDeleteOpen(false);
    setToDeleteId(null);
  }

  // ---------- Helpers ----------
  function refresh() {
    queryClient.invalidateQueries({ queryKey: ['contexts'] });
    toast({ title: 'Refreshed' });
  }

  return (
    <TooltipProvider>
      <div className='min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900'>
        <div className='container mx-auto py-8'>
          {/* Header */}
          <div className='mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between'>
            <div>
              <h1 className='text-3xl font-bold tracking-tight'>
                Context Management
              </h1>
              <p className='text-muted-foreground'>
                Define and manage XBRL contexts (entity + period) used for
                tagging.
              </p>
            </div>
            <div className='flex gap-2'>
              <Button variant='outline' onClick={refresh}>
                <RefreshCw className='mr-2 h-4 w-4' />
                Refresh
              </Button>
            </div>
          </div>

          <div className='grid grid-cols-1 xl:grid-cols-3 gap-6'>
            {/* Left: List & Filters */}
            <div className='xl:col-span-2 space-y-4'>
              {/* Filters */}
              <Card className='backdrop-blur supports-[backdrop-filter]:bg-white/60'>
                <CardHeader className='pb-3'>
                  <CardTitle className='text-lg'>Filters</CardTitle>
                  <CardDescription>
                    Narrow down the contexts list.
                  </CardDescription>
                </CardHeader>
                <CardContent className='grid grid-cols-1 md:grid-cols-5 gap-3'>
                  <div className='md:col-span-2'>
                    <Label htmlFor='entityIdFilter'>Entity Identifier</Label>
                    <Input
                      id='entityIdFilter'
                      placeholder='e.g., 0001234567'
                      value={entityIdFilter}
                      onChange={(e) => setEntityIdFilter(e.target.value)}
                    />
                  </div>
                  <div>
                    <Label htmlFor='periodFilter'>Period</Label>
                    <Select
                      value={periodFilter}
                      onValueChange={(v) => setPeriodFilter(v as any)}
                    >
                      <SelectTrigger id='periodFilter'>
                        <SelectValue placeholder='All' />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value='all'>All</SelectItem>
                        <SelectItem value='instant'>Instant</SelectItem>
                        <SelectItem value='duration'>Duration</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor='taxonomyFilter'>Taxonomy ID</Label>
                    <Input
                      id='taxonomyFilter'
                      type='number'
                      placeholder='e.g., 3'
                      value={taxonomyFilter}
                      onChange={(e) => setTaxonomyFilter(e.target.value)}
                    />
                  </div>
                  <div className='flex items-end justify-between gap-2'>
                    <div className='flex items-center gap-2'>
                      <Switch
                        id='onlyDefault'
                        checked={onlyDefault}
                        onCheckedChange={setOnlyDefault}
                      />
                      <Label htmlFor='onlyDefault' className='cursor-pointer'>
                        Only default
                      </Label>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* List */}
              <Card className='border-0 shadow-none'>
                <CardHeader className='pb-2'>
                  <div className='flex items-center justify-between'>
                    <div>
                      <CardTitle>Contexts</CardTitle>
                      <CardDescription>
                        {isLoading
                          ? 'Loading…'
                          : `${data?.length || 0} context(s)`}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {isLoading ? (
                    <div className='space-y-3'>
                      {[...Array(4)].map((_, i) => (
                        <div
                          key={i}
                          className='rounded-xl border bg-white/60 dark:bg-slate-900/60 p-4'
                        >
                          <Skeleton className='h-5 w-1/3 mb-2' />
                          <Skeleton className='h-4 w-1/4 mb-1' />
                          <Skeleton className='h-4 w-1/2' />
                        </div>
                      ))}
                    </div>
                  ) : isError ? (
                    <div className='text-sm text-red-600 py-6'>
                      {(error as Error)?.message || 'Failed to load contexts'}
                    </div>
                  ) : !data?.length ? (
                    <div className='rounded-xl border-dashed border p-8 text-center'>
                      <div className='mx-auto mb-2 inline-flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800'>
                        <Plus className='h-5 w-5 text-slate-600' />
                      </div>
                      <div className='font-medium'>No contexts yet</div>
                      <p className='text-sm text-muted-foreground'>
                        Use the form on the right to create your first context.
                      </p>
                    </div>
                  ) : (
                    <ScrollArea className='h-[560px] pr-2'>
                      <div className='grid gap-4'>
                        {data.map((ctx: XBRLContextOut) => {
                          const period =
                            ctx.period_type === 'instant'
                              ? `Instant: ${ctx.instant_date ?? '—'}`
                              : `Duration: ${ctx.start_date ?? '—'} → ${ctx.end_date ?? '—'}`;
                          const label = `${ctx.entity_name || ctx.entity_identifier} — ${period}`;

                          return (
                            <div
                              key={ctx.id}
                              className={cn(
                                'group relative overflow-hidden rounded-2xl border p-4 transition-colors',
                                'bg-gradient-to-br from-white to-slate-50 dark:from-slate-900 dark:to-slate-950',
                                'hover:border-slate-300 dark:hover:border-slate-700'
                              )}
                            >
                              {/* subtle gradient stripe */}
                              <div className='pointer-events-none absolute inset-x-0 -top-1 h-1 bg-gradient-to-r from-indigo-500 via-sky-500 to-emerald-500 opacity-60' />

                              <div className='flex items-start justify-between gap-4'>
                                <div className='min-w-0'>
                                  <div className='flex items-center gap-2 flex-wrap'>
                                    <div className='truncate font-medium'>
                                      {label}
                                    </div>
                                    {ctx.is_default_context && (
                                      <Badge>default</Badge>
                                    )}
                                    {ctx.status !== 'valid' && (
                                      <Badge
                                        variant='secondary'
                                        className='capitalize'
                                      >
                                        {ctx.status}
                                      </Badge>
                                    )}
                                  </div>
                                  <div className='text-xs text-muted-foreground mt-1'>
                                    Context ID:{' '}
                                    <span className='font-mono'>
                                      {ctx.context_id}
                                    </span>
                                  </div>

                                  <Separator className='my-3' />

                                  <div className='grid grid-cols-1 sm:grid-cols-3 gap-2 text-sm'>
                                    <div>
                                      <div className='text-muted-foreground'>
                                        Entity
                                      </div>
                                      <div className='truncate'>
                                        {ctx.entity_name || '—'} (
                                        {ctx.entity_identifier})
                                      </div>
                                    </div>
                                    <div>
                                      <div className='text-muted-foreground'>
                                        Period
                                      </div>
                                      <div>{period}</div>
                                    </div>
                                    <div>
                                      <div className='text-muted-foreground'>
                                        Updated
                                      </div>
                                      <div>
                                        {new Date(
                                          ctx.updated_at
                                        ).toLocaleString()}
                                      </div>
                                    </div>
                                  </div>
                                </div>

                                <div className='flex shrink-0 items-center gap-2'>
                                  <Tooltip>
                                    <TooltipTrigger asChild>
                                      <Button
                                        size='icon'
                                        variant='ghost'
                                        disabled
                                        title='Edit not implemented yet'
                                      >
                                        <Edit className='h-4 w-4' />
                                      </Button>
                                    </TooltipTrigger>
                                    <TooltipContent>
                                      Edit (coming soon)
                                    </TooltipContent>
                                  </Tooltip>

                                  <Tooltip>
                                    <TooltipTrigger asChild>
                                      <Button
                                        size='icon'
                                        variant='ghost'
                                        onClick={() => askDelete(ctx.id)}
                                        disabled={
                                          deleteContext.isPending &&
                                          ctx.id === toDeleteId
                                        }
                                      >
                                        {deleteContext.isPending &&
                                        ctx.id === toDeleteId ? (
                                          <Loader2 className='h-4 w-4 animate-spin' />
                                        ) : (
                                          <Trash2 className='h-4 w-4' />
                                        )}
                                      </Button>
                                    </TooltipTrigger>
                                    <TooltipContent>Delete</TooltipContent>
                                  </Tooltip>
                                </div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </ScrollArea>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Right: Create form */}
            <div>
              <Card className='sticky top-6 backdrop-blur supports-[backdrop-filter]:bg-white/70'>
                <CardHeader>
                  <CardTitle>Create Context</CardTitle>
                  <CardDescription>
                    Define a new XBRL context to use for tagging.
                  </CardDescription>
                </CardHeader>
                <CardContent className='space-y-4'>
                  <div className='space-y-2'>
                    <Label htmlFor='entityName'>Entity Name</Label>
                    <Input
                      id='entityName'
                      placeholder='e.g., Acme Corporation'
                      value={form.entityName}
                      onChange={(e) =>
                        setForm({ ...form, entityName: e.target.value })
                      }
                    />
                  </div>

                  <div className='space-y-2'>
                    <Label htmlFor='entityScheme'>Entity Scheme</Label>
                    <Input
                      id='entityScheme'
                      value={form.entityScheme}
                      onChange={(e) =>
                        setForm({ ...form, entityScheme: e.target.value })
                      }
                    />
                  </div>

                  <div className='space-y-2'>
                    <Label htmlFor='entityIdentifier'>Entity Identifier</Label>
                    <Input
                      id='entityIdentifier'
                      placeholder='e.g., 0001234567'
                      value={form.entityIdentifier}
                      onChange={(e) =>
                        setForm({ ...form, entityIdentifier: e.target.value })
                      }
                    />
                  </div>

                  <div className='space-y-2'>
                    <Label>Period Type</Label>
                    <Select
                      value={form.periodType}
                      onValueChange={(value) =>
                        setForm({
                          ...form,
                          periodType: value as 'instant' | 'duration',
                          instantDate:
                            value === 'instant'
                              ? (form.instantDate ?? new Date())
                              : undefined,
                          startDate:
                            value === 'duration'
                              ? (form.startDate ?? new Date())
                              : undefined,
                          endDate:
                            value === 'duration'
                              ? (form.endDate ?? new Date())
                              : undefined,
                        })
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder='Select period type' />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value='instant'>
                          Instant (As of Date)
                        </SelectItem>
                        <SelectItem value='duration'>
                          Duration (Date Range)
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {form.periodType === 'instant' ? (
                    <div className='space-y-2'>
                      <Label>Instant Date</Label>
                      <Popover>
                        <PopoverTrigger asChild>
                          <Button
                            variant='outline'
                            className={cn(
                              'w-full justify-start text-left font-normal',
                              !form.instantDate && 'text-muted-foreground'
                            )}
                          >
                            <CalendarIcon className='mr-2 h-4 w-4' />
                            {form.instantDate
                              ? format(form.instantDate, 'PPP')
                              : 'Select date'}
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent className='w-auto p-0'>
                          <Calendar
                            mode='single'
                            selected={form.instantDate}
                            onSelect={(date) =>
                              setForm({
                                ...form,
                                instantDate: date ?? undefined,
                              })
                            }
                            initialFocus
                          />
                        </PopoverContent>
                      </Popover>
                    </div>
                  ) : (
                    <div className='space-y-4'>
                      <div className='space-y-2'>
                        <Label>Start Date</Label>
                        <Popover>
                          <PopoverTrigger asChild>
                            <Button
                              variant='outline'
                              className={cn(
                                'w-full justify-start text-left font-normal',
                                !form.startDate && 'text-muted-foreground'
                              )}
                            >
                              <CalendarIcon className='mr-2 h-4 w-4' />
                              {form.startDate
                                ? format(form.startDate, 'PPP')
                                : 'Select start date'}
                            </Button>
                          </PopoverTrigger>
                          <PopoverContent className='w-auto p-0'>
                            <Calendar
                              mode='single'
                              selected={form.startDate}
                              onSelect={(date) =>
                                setForm({
                                  ...form,
                                  startDate: date ?? undefined,
                                })
                              }
                              initialFocus
                            />
                          </PopoverContent>
                        </Popover>
                      </div>

                      <div className='space-y-2'>
                        <Label>End Date</Label>
                        <Popover>
                          <PopoverTrigger asChild>
                            <Button
                              variant='outline'
                              className={cn(
                                'w-full justify-start text-left font-normal',
                                !form.endDate && 'text-muted-foreground'
                              )}
                            >
                              <CalendarIcon className='mr-2 h-4 w-4' />
                              {form.endDate
                                ? format(form.endDate, 'PPP')
                                : 'Select end date'}
                            </Button>
                          </PopoverTrigger>
                          <PopoverContent className='w-auto p-0'>
                            <Calendar
                              mode='single'
                              selected={form.endDate}
                              onSelect={(date) =>
                                setForm({ ...form, endDate: date ?? undefined })
                              }
                              initialFocus
                            />
                          </PopoverContent>
                        </Popover>
                      </div>
                    </div>
                  )}

                  <div className='space-y-2'>
                    <Label htmlFor='taxonomyId'>Taxonomy ID (optional)</Label>
                    <Input
                      id='taxonomyId'
                      type='number'
                      placeholder='e.g., 3'
                      value={form.taxonomyId ?? ''}
                      onChange={(e) =>
                        setForm({ ...form, taxonomyId: e.target.value })
                      }
                    />
                  </div>
                </CardContent>
                <CardFooter className='gap-2'>
                  <Button
                    className='w-full'
                    onClick={handleCreateContext}
                    disabled={!canCreate || createContext.isPending}
                  >
                    {createContext.isPending ? (
                      <>
                        <Loader2 className='mr-2 h-4 w-4 animate-spin' />
                        Creating…
                      </>
                    ) : (
                      <>
                        <Plus className='mr-2 h-4 w-4' />
                        Create Context
                      </>
                    )}
                  </Button>
                </CardFooter>
              </Card>
            </div>
          </div>
        </div>

        {/* Delete dialog */}
        <AlertDialog open={deleteOpen} onOpenChange={setDeleteOpen}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Delete context?</AlertDialogTitle>
              <AlertDialogDescription>
                This will permanently remove the selected context. This action
                cannot be undone.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel disabled={deleteContext.isPending}>
                Cancel
              </AlertDialogCancel>
              <AlertDialogAction
                onClick={confirmDelete}
                disabled={deleteContext.isPending}
                className='bg-red-600 hover:bg-red-700'
              >
                {deleteContext.isPending ? (
                  <Loader2 className='mr-2 h-4 w-4 animate-spin' />
                ) : (
                  <Trash2 className='mr-2 h-4 w-4' />
                )}
                Delete
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </TooltipProvider>
  );
}
