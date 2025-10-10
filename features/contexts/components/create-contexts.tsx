import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
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
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { cn, generateUniqueId } from '@/lib/utils';
import { CalendarIcon, Loader2, Plus, Building2 } from 'lucide-react';
import React from 'react';
import { useCreateContext } from '../api/create-context';
import { toast } from '@/components/ui/use-toast';
import { useForm } from 'react-hook-form';
import { format } from 'date-fns';
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from '@/components/ui/form';

// Import Zod and zodResolver
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

// Define the Zod schema with proper date validation
const schema = z
  .object({
    entityName: z.string().min(1, { message: 'Entity name is required' }),
    entityScheme: z.string().min(1, { message: 'Entity scheme is required' }),
    entityIdentifier: z
      .string()
      .min(1, { message: 'Entity identifier is required' }),
    periodType: z.enum(['instant', 'duration'], {
      message: 'Period type is required',
    }),
    instantDate: z.date().nullable(),
    startDate: z.date().nullable(),
    endDate: z.date().nullable(),
    taxonomyId: z.string().optional(),
  })
  .refine(
    (data) => {
      if (data.periodType === 'instant') {
        return data.instantDate !== null;
      }
      return true;
    },
    {
      message: 'Instant date is required for instant period type',
      path: ['instantDate'],
    }
  )
  .refine(
    (data) => {
      if (data.periodType === 'duration') {
        return data.startDate !== null && data.endDate !== null;
      }
      return true;
    },
    {
      message: 'Start and end dates are required for duration period type',
      path: ['startDate'],
    }
  );

type FormValues = z.infer<typeof schema>;

function CreateContexts() {
  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      entityName: '',
      entityScheme: 'http://www.sec.gov/CIK',
      entityIdentifier: '',
      periodType: 'instant',
      instantDate: new Date(),
      startDate: null,
      endDate: null,
      taxonomyId: '',
    },
  });

  const createContext = useCreateContext({
    mutationConfig: {
      onSuccess: () => {
        toast({
          title: 'Context created',
          description: 'Your context is now available for tagging.',
        });
        form.reset({
          entityName: '',
          entityScheme: 'http://www.sec.gov/CIK',
          entityIdentifier: '',
          periodType: 'instant',
          instantDate: new Date(),
          startDate: null,
          endDate: null,
          taxonomyId: '',
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

  function yyyyMmDd(d?: Date | null) {
    return d ? format(d, 'yyyy-MM-dd') : null;
  }

  const onSubmit = async (data: FormValues) => {
    // Generate a unique context ID
    const contextId = `ctx-${generateUniqueId().slice(0, 8)}`;
    const payload = {
      context_id: contextId,
      entity_scheme: data.entityScheme,
      entity_identifier: data.entityIdentifier,
      entity_name: data.entityName || undefined,
      lei: undefined,
      period_type: data.periodType,
      start_date:
        data.periodType === 'duration' ? yyyyMmDd(data.startDate) : null,
      end_date: data.periodType === 'duration' ? yyyyMmDd(data.endDate) : null,
      instant_date:
        data.periodType === 'instant' ? yyyyMmDd(data.instantDate) : null,
      dimensions_json: null,
      taxonomy_id: data.taxonomyId ? Number(data.taxonomyId) : null,
      is_default_context: false,
      status: 'valid' as const,
      validation_messages: [],
    };

    createContext.mutate(payload);
  };

  return (
    <div>
      <Card className='sticky top-6 backdrop-blur supports-[backdrop-filter]:bg-white/70'>
        <CardHeader>
          <CardTitle>Create Context</CardTitle>
          <CardDescription>
            Define a new XBRL context to use for tagging.
          </CardDescription>
        </CardHeader>
        <CardContent className='space-y-4'>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-4'>
              {/* Entity Name */}
              <FormField
                control={form.control}
                name='entityName'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Entity Name</FormLabel>
                    <FormControl>
                      <div className='relative'>
                        <Input
                          type='text'
                          placeholder='e.g., Acme Corporation'
                          {...field}
                          className=' text-black placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12'
                        />
                      </div>
                    </FormControl>
                    <FormDescription>
                      Enter the name of the entity.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Entity Scheme */}
              <FormField
                control={form.control}
                name='entityScheme'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Entity Scheme</FormLabel>
                    <FormControl>
                      <Input
                        type='text'
                        placeholder='e.g., http://www.sec.gov/CIK'
                        {...field}
                        className=' text-black placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12'
                      />
                    </FormControl>
                    <FormDescription>
                      Enter the entity's scheme (e.g., CIK, LEI).
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Entity Identifier */}
              <FormField
                control={form.control}
                name='entityIdentifier'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Entity Identifier</FormLabel>
                    <FormControl>
                      <Input
                        type='text'
                        placeholder='e.g., 0001234567'
                        {...field}
                        className=' text-black placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12'
                      />
                    </FormControl>
                    <FormDescription>
                      Enter the unique identifier for the entity.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Period Type */}
              <FormField
                control={form.control}
                name='periodType'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Period Type</FormLabel>
                    <FormControl>
                      <Select
                        value={field.value}
                        onValueChange={(value) => {
                          field.onChange(value);
                          if (value === 'instant') {
                            form.setValue('instantDate', new Date());
                            form.setValue('startDate', null);
                            form.setValue('endDate', null);
                          } else {
                            form.setValue('instantDate', null);
                            form.setValue('startDate', new Date());
                            form.setValue('endDate', new Date());
                          }
                        }}
                      >
                        <SelectTrigger className=' text-black placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12'>
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
                    </FormControl>
                    <FormDescription>
                      Select whether the period is "instant" or "duration".
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Instant Date */}
              {form.watch('periodType') === 'instant' && (
                <FormField
                  control={form.control}
                  name='instantDate'
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Instant Date</FormLabel>
                      <FormControl>
                        <Popover>
                          <PopoverTrigger asChild>
                            <Button
                              variant='outline'
                              className={cn(
                                'w-full justify-start text-left font-normal text-black h-12 rounded-xl hover:bg-gray-800/70',
                                !field.value && 'text-muted-foreground'
                              )}
                            >
                              <CalendarIcon className='mr-2 h-4 w-4' />
                              {field.value
                                ? format(field.value, 'PPP')
                                : 'Select date'}
                            </Button>
                          </PopoverTrigger>
                          <PopoverContent className='w-auto p-0'>
                            <Calendar
                              mode='single'
                              selected={field.value || undefined}
                              onSelect={(date) => field.onChange(date || null)}
                              initialFocus
                            />
                          </PopoverContent>
                        </Popover>
                      </FormControl>
                      <FormDescription>
                        Select the date for the instant period.
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )}

              {/* Duration Dates */}
              {form.watch('periodType') === 'duration' && (
                <div className='space-y-4'>
                  {/* Start Date */}
                  <FormField
                    control={form.control}
                    name='startDate'
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Start Date</FormLabel>
                        <FormControl>
                          <Popover>
                            <PopoverTrigger asChild>
                              <Button
                                variant='outline'
                                className={cn(
                                  'w-full justify-start text-left font-normal text-black h-12 rounded-xl hover:bg-gray-800/70',
                                  !field.value && 'text-muted-foreground'
                                )}
                              >
                                <CalendarIcon className='mr-2 h-4 w-4' />
                                {field.value
                                  ? format(field.value, 'PPP')
                                  : 'Select start date'}
                              </Button>
                            </PopoverTrigger>
                            <PopoverContent className='w-auto p-0'>
                              <Calendar
                                mode='single'
                                selected={field.value || undefined}
                                onSelect={(date) =>
                                  field.onChange(date || null)
                                }
                                initialFocus
                              />
                            </PopoverContent>
                          </Popover>
                        </FormControl>
                        <FormDescription>
                          Select the start date for the duration.
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  {/* End Date */}
                  <FormField
                    control={form.control}
                    name='endDate'
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>End Date</FormLabel>
                        <FormControl>
                          <Popover>
                            <PopoverTrigger asChild>
                              <Button
                                variant='outline'
                                className={cn(
                                  'w-full justify-start text-left font-normal  text-black h-12 rounded-xl hover:bg-gray-800/70',
                                  !field.value && 'text-muted-foreground'
                                )}
                              >
                                <CalendarIcon className='mr-2 h-4 w-4' />
                                {field.value
                                  ? format(field.value, 'PPP')
                                  : 'Select end date'}
                              </Button>
                            </PopoverTrigger>
                            <PopoverContent className='w-auto p-0'>
                              <Calendar
                                mode='single'
                                selected={field.value || undefined}
                                onSelect={(date) =>
                                  field.onChange(date || null)
                                }
                                initialFocus
                              />
                            </PopoverContent>
                          </Popover>
                        </FormControl>
                        <FormDescription>
                          Select the end date for the duration.
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
              )}

              {/* Taxonomy ID */}
              <FormField
                control={form.control}
                name='taxonomyId'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Taxonomy ID (optional)</FormLabel>
                    <FormControl>
                      <Input
                        type='number'
                        placeholder='e.g., 3'
                        {...field}
                        className=' text-black placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12'
                      />
                    </FormControl>
                    <FormDescription>Optional taxonomy ID.</FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Submit Button */}
              <div className='pt-4'>
                <Button
                  className='w-full'
                  type='submit'
                  disabled={createContext.isPending}
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
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}

export default CreateContexts;
