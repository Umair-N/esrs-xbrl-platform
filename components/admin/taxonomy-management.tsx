'use client';

import { CardContent } from '@/components/ui/card';
import { CardDescription } from '@/components/ui/card';
import { CardTitle } from '@/components/ui/card';
import { CardHeader } from '@/components/ui/card';
import { Card } from '@/components/ui/card';
import React from 'react';
import { Button } from '@/components/ui/button';
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from '@/components/ui/popover';
import {
  CheckCircle2,
  XCircle,
  MoreHorizontal,
  FileText,
  CalendarDays,
  Loader2,
  Search,
  Filter,
  Grid3X3,
  List,
  Plus,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAllTaxonomies } from '@/features/taxonomy/api/get-all-taxonomy-list';
import { useEnableTaxonomy } from '@/features/taxonomy/api/enable-taxonomy';
import { useDisableTaxonomy } from '@/features/taxonomy/api/disable-taxonomy';
import { toast } from 'sonner';

export type Taxonomy = {
  id: number;
  name: string;
  file_name: string;
  enabled: boolean;
  created_at: string;
};

type TaxonomyCardsProps = {
  items: Taxonomy[];
  className?: string;
  onToggle?(item: Taxonomy): void;
};

function formatISODate(iso: string) {
  try {
    const d = new Date(iso);
    return new Intl.DateTimeFormat(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    }).format(d);
  } catch {
    return iso;
  }
}

function formatRelativeDate(iso: string) {
  try {
    const date = new Date(iso);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
    return `${Math.floor(diffDays / 365)} years ago`;
  } catch {
    return formatISODate(iso);
  }
}

export default function TaxonomyManagement() {
  const [searchTerm, setSearchTerm] = React.useState('');
  const [filterStatus, setFilterStatus] = React.useState<
    'all' | 'enabled' | 'disabled'
  >('all');
  const [viewMode, setViewMode] = React.useState<'grid' | 'list'>('grid');

  const { data: taxonomiesList, isLoading } = useAllTaxonomies();

  const { mutate: enableTaxonomy, isPending: isEnabling } = useEnableTaxonomy({
    mutationConfig: {
      onSuccess: (data, variables) => {
        toast.success(
          `Taxonomy "${taxonomiesList?.find((t) => t.id === variables.taxonomyId)?.name}" has been enabled successfully.`
        );
      },
      onError: (error, variables) => {
        toast.error(`Failed to enable taxonomy. Please try again.`);
        console.error('Enable taxonomy error:', error);
      },
    },
  });

  const { mutate: disableTaxonomy, isPending: isDisabling } =
    useDisableTaxonomy({
      mutationConfig: {
        onSuccess: (data, variables) => {
          toast.success(
            `Taxonomy "${taxonomiesList?.find((t) => t.id === variables.taxonomyId)?.name}" has been disabled successfully.`
          );
        },
        onError: (error, variables) => {
          toast.error(`Failed to disable taxonomy. Please try again.`);
          console.error('Disable taxonomy error:', error);
        },
      },
    });

  const handleEnableTaxonomy = React.useCallback(
    (taxonomyId: number) => {
      enableTaxonomy({ taxonomyId });
    },
    [enableTaxonomy]
  );

  const handleDisableTaxonomy = React.useCallback(
    (taxonomyId: number) => {
      disableTaxonomy({ taxonomyId });
    },
    [disableTaxonomy]
  );

  // Filter and search logic
  const filteredTaxonomies = React.useMemo(() => {
    if (!taxonomiesList) return [];

    return taxonomiesList.filter((taxonomy) => {
      const matchesSearch =
        taxonomy.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        taxonomy.file_name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesFilter =
        filterStatus === 'all' ||
        (filterStatus === 'enabled' && taxonomy.enabled) ||
        (filterStatus === 'disabled' && !taxonomy.enabled);
      return matchesSearch && matchesFilter;
    });
  }, [taxonomiesList, searchTerm, filterStatus]);

  const stats = React.useMemo(() => {
    if (!taxonomiesList) return { total: 0, enabled: 0, disabled: 0 };

    return {
      total: taxonomiesList.length,
      enabled: taxonomiesList.filter((t) => t.enabled).length,
      disabled: taxonomiesList.filter((t) => !t.enabled).length,
    };
  }, [taxonomiesList]);

  if (isLoading) {
    return (
      <div className='w-full min-h-[400px] flex items-center justify-center'>
        <div className='text-center space-y-4'>
          <Loader2 className='size-8 animate-spin mx-auto text-primary' />
          <div className='space-y-1'>
            <div className='text-sm font-medium'>Loading taxonomies...</div>
            <div className='text-xs text-muted-foreground'>
              This may take a moment
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!taxonomiesList?.length) {
    return (
      <div className='w-full min-h-[400px] flex items-center justify-center'>
        <div className='text-center space-y-6 max-w-md'>
          <div className='mx-auto w-24 h-24 bg-muted rounded-full flex items-center justify-center'>
            <FileText className='w-8 h-8 text-muted-foreground' />
          </div>
          <div className='space-y-2'>
            <h3 className='text-lg font-semibold'>No taxonomies found</h3>
            <p className='text-sm text-muted-foreground'>
              Get started by uploading your first taxonomy file to begin
              organizing your content.
            </p>
          </div>
          <Button className='gap-2'>
            <Plus className='w-4 h-4' />
            Upload Taxonomy
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className='w-full space-y-6 p-6'>
      {/* Header */}
      <div className='flex flex-col gap-4'>
        <div className='flex items-center justify-between'>
          <div>
            <h1 className='text-2xl font-bold tracking-tight'>
              Taxonomy Management
            </h1>
            <p className='text-muted-foreground'>
              Manage and organize your content taxonomies
            </p>
          </div>
          <Button className='gap-2'>
            <Plus className='w-4 h-4' />
            Add Taxonomy
          </Button>
        </div>

        {/* Stats Cards */}
        <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
          <Card className='relative overflow-hidden bg-gradient-to-br from-slate-50 to-blue-50 border border-slate-200 hover:shadow-md transition-all duration-300 hover:-translate-y-0.5'>
            <div className='absolute top-0 right-0 w-16 h-16 bg-blue-100/50 rounded-bl-full' />
            <CardContent className='p-5 relative z-10'>
              <div className='flex items-center justify-between'>
                <div>
                  <p className='text-slate-600 text-sm font-medium mb-1'>
                    Total Taxonomies
                  </p>
                  <p className='text-2xl font-bold text-slate-900'>
                    {stats.total}
                  </p>
                  <p className='text-slate-500 text-xs mt-1'>
                    All taxonomies in system
                  </p>
                </div>
                <div className='w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center'>
                  <FileText className='w-5 h-5 text-blue-600' />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className='relative overflow-hidden bg-gradient-to-br from-slate-50 to-emerald-50 border border-slate-200 hover:shadow-md transition-all duration-300 hover:-translate-y-0.5'>
            <div className='absolute top-0 right-0 w-16 h-16 bg-emerald-100/50 rounded-bl-full' />
            <CardContent className='p-5 relative z-10'>
              <div className='flex items-center justify-between'>
                <div>
                  <p className='text-slate-600 text-sm font-medium mb-1'>
                    Active
                  </p>
                  <p className='text-2xl font-bold text-emerald-700'>
                    {stats.enabled}
                  </p>
                  <p className='text-slate-500 text-xs mt-1'>
                    Currently enabled
                  </p>
                </div>
                <div className='w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center'>
                  <CheckCircle2 className='w-5 h-5 text-emerald-600' />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className='relative overflow-hidden bg-gradient-to-br from-slate-50 to-rose-50 border border-slate-200 hover:shadow-md transition-all duration-300 hover:-translate-y-0.5'>
            <div className='absolute top-0 right-0 w-16 h-16 bg-rose-100/50 rounded-bl-full' />
            <CardContent className='p-5 relative z-10'>
              <div className='flex items-center justify-between'>
                <div>
                  <p className='text-slate-600 text-sm font-medium mb-1'>
                    Inactive
                  </p>
                  <p className='text-2xl font-bold text-rose-700'>
                    {stats.disabled}
                  </p>
                  <p className='text-slate-500 text-xs mt-1'>
                    Currently disabled
                  </p>
                </div>
                <div className='w-10 h-10 bg-rose-100 rounded-lg flex items-center justify-center'>
                  <XCircle className='w-5 h-5 text-rose-600' />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Search and Filters */}
        <div className='flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between'>
          <div className='flex flex-col sm:flex-row gap-3 w-full sm:w-auto'>
            <div className='relative'>
              <Search className='absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground' />
              <input
                type='text'
                placeholder='Search taxonomies...'
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className='pl-9 pr-4 py-2 border border-input bg-background rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent min-w-[250px]'
              />
            </div>

            <Popover>
              <PopoverTrigger asChild>
                <Button variant='outline' className='gap-2'>
                  <Filter className='w-4 h-4' />
                  Filter
                  {filterStatus !== 'all' && (
                    <span className='ml-1 bg-primary text-primary-foreground px-1.5 py-0.5 rounded-full text-xs'>
                      {filterStatus === 'enabled' ? 'On' : 'Off'}
                    </span>
                  )}
                </Button>
              </PopoverTrigger>
              <PopoverContent align='start' className='w-48 p-2'>
                <div className='space-y-1'>
                  <div className='px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase tracking-wide'>
                    Status
                  </div>
                  {[
                    { value: 'all', label: 'All Taxonomies' },
                    { value: 'enabled', label: 'Enabled Only' },
                    { value: 'disabled', label: 'Disabled Only' },
                  ].map((option) => (
                    <Button
                      key={option.value}
                      variant={
                        filterStatus === option.value ? 'secondary' : 'ghost'
                      }
                      size='sm'
                      className='w-full justify-start'
                      onClick={() =>
                        setFilterStatus(option.value as typeof filterStatus)
                      }
                    >
                      {option.label}
                    </Button>
                  ))}
                </div>
              </PopoverContent>
            </Popover>
          </div>

          <div className='flex items-center gap-2'>
            <div className='flex border rounded-md'>
              <Button
                variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
                size='sm'
                onClick={() => setViewMode('grid')}
                className='rounded-r-none border-r'
              >
                <Grid3X3 className='w-4 h-4' />
              </Button>
              <Button
                variant={viewMode === 'list' ? 'secondary' : 'ghost'}
                size='sm'
                onClick={() => setViewMode('list')}
                className='rounded-l-none'
              >
                <List className='w-4 h-4' />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Results count */}
      <div className='text-sm text-muted-foreground'>
        Showing {filteredTaxonomies.length} of {stats.total} taxonomies
      </div>

      {/* Taxonomy Grid/List */}
      <div
        className={cn(
          viewMode === 'grid'
            ? 'grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3'
            : 'space-y-4'
        )}
      >
        {filteredTaxonomies.map((t) => {
          const isEnabled = t.enabled;
          const createdLabel = formatRelativeDate(t.created_at);
          const exactDate = formatISODate(t.created_at);
          const isActionPending = isEnabling || isDisabling;

          if (viewMode === 'list') {
            return (
              <Card
                key={t.id}
                className={cn(
                  'transition-all duration-200 hover:shadow-md border-l-4 relative overflow-hidden',
                  isEnabled
                    ? 'border-l-emerald-500 bg-gradient-to-r from-emerald-50/50 to-white hover:from-emerald-50'
                    : 'border-l-rose-500 bg-gradient-to-r from-rose-50/50 to-white hover:from-rose-50'
                )}
              >
                <div
                  className={cn(
                    'absolute inset-0 opacity-5',
                    isEnabled
                      ? 'bg-gradient-to-r from-emerald-200 to-transparent'
                      : 'bg-gradient-to-r from-rose-200 to-transparent'
                  )}
                />
                <CardContent className='p-4 relative z-10'>
                  <div className='flex items-center justify-between gap-4'>
                    <div className='flex items-center gap-3 flex-1 min-w-0'>
                      <div
                        className={cn(
                          'w-10 h-10 rounded-lg flex items-center justify-center',
                          isEnabled
                            ? 'bg-emerald-100 text-emerald-600'
                            : 'bg-rose-100 text-rose-600'
                        )}
                      >
                        <FileText className='w-5 h-5' />
                      </div>
                      <div className='flex-1 min-w-0'>
                        <div className='flex items-center gap-2'>
                          <h3
                            className={cn(
                              'font-semibold truncate',
                              isEnabled ? 'text-slate-900' : 'text-slate-900'
                            )}
                          >
                            {t.name}
                          </h3>
                          <div
                            className={cn(
                              'inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium whitespace-nowrap',
                              isEnabled
                                ? 'border-emerald-200 bg-emerald-100 text-emerald-700'
                                : 'border-rose-200 bg-rose-100 text-rose-700'
                            )}
                          >
                            {isEnabled ? (
                              <>
                                <CheckCircle2 className='size-3' />
                                Active
                              </>
                            ) : (
                              <>
                                <XCircle className='size-3' />
                                Inactive
                              </>
                            )}
                          </div>
                        </div>
                        <div className='flex items-center gap-4 mt-1 text-sm text-slate-600'>
                          <div className='flex items-center gap-1'>
                            <FileText className='w-3 h-3 text-slate-400' />
                            <code
                              className={cn(
                                'text-xs px-1.5 py-0.5 rounded font-mono',
                                isEnabled
                                  ? 'bg-emerald-50 text-emerald-700'
                                  : 'bg-rose-50 text-rose-700'
                              )}
                            >
                              {t.file_name}
                            </code>
                          </div>
                          <div
                            className='flex items-center gap-1 text-slate-500'
                            title={exactDate}
                          >
                            <CalendarDays className='w-3 h-3' />
                            <span className='text-xs'>{createdLabel}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className='flex items-center gap-2'>
                      <Popover>
                        <PopoverTrigger asChild>
                          <Button
                            variant='ghost'
                            size='sm'
                            disabled={isActionPending}
                            className='hover:bg-slate-100'
                          >
                            {isActionPending ? (
                              <Loader2 className='size-4 animate-spin' />
                            ) : (
                              <MoreHorizontal className='size-4' />
                            )}
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent align='end' className='w-48 p-1'>
                          <div className='space-y-1'>
                            {!isEnabled ? (
                              <Button
                                variant='ghost'
                                size='sm'
                                className='w-full justify-start gap-2 text-emerald-600 hover:text-emerald-700'
                                onClick={() => handleEnableTaxonomy(t.id)}
                                disabled={isActionPending}
                              >
                                <CheckCircle2 className='size-4' />
                                Enable
                              </Button>
                            ) : (
                              <Button
                                variant='ghost'
                                size='sm'
                                className='w-full justify-start gap-2 text-rose-600 hover:text-rose-700'
                                onClick={() => handleDisableTaxonomy(t.id)}
                                disabled={isActionPending}
                              >
                                <XCircle className='size-4' />
                                Disable
                              </Button>
                            )}
                          </div>
                        </PopoverContent>
                      </Popover>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          }

          return (
            <Card
              key={t.id}
              className={cn(
                'group flex flex-col transition-all duration-200 hover:shadow-lg hover:-translate-y-1 border relative overflow-hidden',
                isEnabled
                  ? 'bg-gradient-to-br from-white to-emerald-50/30 border-emerald-200 hover:border-emerald-300'
                  : 'bg-gradient-to-br from-white to-rose-50/30 border-rose-200 hover:border-rose-300'
              )}
            >
              {/* Subtle decorative element */}
              <div
                className={cn(
                  'absolute top-0 right-0 w-20 h-20 rounded-bl-full opacity-20',
                  isEnabled ? 'bg-emerald-200' : 'bg-rose-200'
                )}
              />
              <CardHeader className='p-4 pb-2 relative z-10'>
                <div className='flex items-start justify-between gap-2'>
                  <div className='flex-1 min-w-0'>
                    <CardTitle
                      className={cn(
                        'text-base leading-tight truncate transition-colors font-semibold',
                        isEnabled
                          ? 'text-slate-900 group-hover:text-emerald-700'
                          : 'text-slate-900 group-hover:text-rose-700'
                      )}
                    >
                      {t.name}
                    </CardTitle>
                    <CardDescription className='text-xs mt-1 truncate text-slate-500'>
                      {t.file_name}
                    </CardDescription>
                  </div>

                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant='ghost'
                        size='icon'
                        className='h-8 w-8 text-slate-400 hover:text-slate-600 hover:bg-slate-100 opacity-0 group-hover:opacity-100 transition-all'
                        disabled={isActionPending}
                      >
                        {isActionPending ? (
                          <Loader2 className='size-4 animate-spin' />
                        ) : (
                          <MoreHorizontal className='size-4' />
                        )}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent align='end' className='w-48 p-1'>
                      <div className='space-y-1'>
                        {!isEnabled ? (
                          <Button
                            variant='ghost'
                            size='sm'
                            className='w-full justify-start gap-2 text-emerald-600 hover:text-emerald-700'
                            onClick={() => handleEnableTaxonomy(t.id)}
                            disabled={isActionPending}
                          >
                            <CheckCircle2 className='size-4' />
                            Enable
                          </Button>
                        ) : (
                          <Button
                            variant='ghost'
                            size='sm'
                            className='w-full justify-start gap-2 text-rose-600 hover:text-rose-700'
                            onClick={() => handleDisableTaxonomy(t.id)}
                            disabled={isActionPending}
                          >
                            <XCircle className='size-4' />
                            Disable
                          </Button>
                        )}
                      </div>
                    </PopoverContent>
                  </Popover>
                </div>
              </CardHeader>

              <CardContent className='flex-1 p-4 pt-2'>
                <div className='space-y-4'>
                  <div className='flex justify-between items-center'>
                    <div
                      className={cn(
                        'inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium',
                        isEnabled
                          ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
                          : 'border-rose-200 bg-rose-50 text-rose-700'
                      )}
                    >
                      {isEnabled ? (
                        <>
                          <CheckCircle2 className='size-3' />
                          Active
                        </>
                      ) : (
                        <>
                          <XCircle className='size-3' />
                          Inactive
                        </>
                      )}
                    </div>
                  </div>

                  <div className='space-y-2 text-xs text-muted-foreground'>
                    <div
                      className='flex items-center gap-2'
                      title={t.file_name}
                    >
                      <FileText className='size-3 flex-shrink-0' />
                      <code className='rounded bg-muted px-2 py-1 text-[10px] font-mono truncate flex-1'>
                        {t.file_name}
                      </code>
                    </div>
                    <div className='flex items-center gap-2' title={exactDate}>
                      <CalendarDays className='size-3 flex-shrink-0' />
                      <span>{createdLabel}</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {filteredTaxonomies.length === 0 && searchTerm && (
        <div className='text-center py-12'>
          <div className='mx-auto w-20 h-20 bg-muted rounded-full flex items-center justify-center mb-4'>
            <Search className='w-6 h-6 text-muted-foreground' />
          </div>
          <h3 className='text-lg font-semibold mb-2'>No results found</h3>
          <p className='text-sm text-muted-foreground mb-4'>
            No taxonomies match your search for "{searchTerm}". Try adjusting
            your search terms or filters.
          </p>
          <Button
            variant='outline'
            onClick={() => {
              setSearchTerm('');
              setFilterStatus('all');
            }}
          >
            Clear search
          </Button>
        </div>
      )}
    </div>
  );
}
