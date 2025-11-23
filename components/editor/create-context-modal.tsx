'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Plus, Loader2 } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useCreateContext } from '@/features/contexts/api/create-context';
import { useToast } from '@/components/ui/use-toast';

const formSchema = z
  .object({
    context_id: z.string().min(1, 'Context ID is required'),
    entity_identifier: z.string().min(1, 'Entity Identifier is required'),
    entity_name: z.string().optional(),
    period_type: z.enum(['instant', 'duration', 'forever']),
    start_date: z.string().optional(),
    end_date: z.string().optional(),
    instant_date: z.string().optional(),
    entity_scheme: z.string().default('http://www.sec.gov/CIK'),
    taxonomy_id: z.string().optional(),
  })
  .refine(
    (data) => {
      if (data.period_type === 'duration') {
        return !!data.start_date && !!data.end_date;
      }
      if (data.period_type === 'instant') {
        return !!data.instant_date;
      }
      return true;
    },
    {
      message: 'Date fields are required based on period type',
      path: ['period_type'], // This might not be perfect placement for the error but works
    }
  );

export function CreateContextModal() {
  const [open, setOpen] = useState(false);
  const { toast } = useToast();
  const createContextMutation = useCreateContext();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      context_id: '',
      entity_identifier: '',
      entity_name: '',
      period_type: 'duration',
      start_date: '',
      end_date: '',
      instant_date: '',
      entity_scheme: 'http://www.sec.gov/CIK',
      taxonomy_id: '',
    },
  });

  const periodType = form.watch('period_type');

  function onSubmit(values: z.infer<typeof formSchema>) {
    createContextMutation.mutate(
      {
        context_id: values.context_id,
        entity_identifier: values.entity_identifier,
        entity_name: values.entity_name,
        period_type: values.period_type,
        start_date:
          values.period_type === 'duration' ? values.start_date : null,
        end_date: values.period_type === 'duration' ? values.end_date : null,
        instant_date:
          values.period_type === 'instant' ? values.instant_date : null,
        entity_scheme: values.entity_scheme,
        taxonomy_id: values.taxonomy_id ? Number(values.taxonomy_id) : null,
        // Default values for other fields
        is_default_context: false,
        status: 'valid',
      },
      {
        onSuccess: () => {
          toast({
            title: 'Context created',
            description: 'The new context has been successfully created.',
          });
          setOpen(false);
          form.reset();
        },
        onError: (error) => {
          toast({
            title: 'Error',
            description: 'Failed to create context. Please try again.',
            variant: 'destructive',
          });
          console.error(error);
        },
      }
    );
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant='outline' size='sm'>
          <Plus className='h-4 w-4' /> Create Context
        </Button>
      </DialogTrigger>
      <DialogContent className='sm:max-w-[500px]'>
        <DialogHeader>
          <DialogTitle>Create New Context</DialogTitle>
          <DialogDescription>
            Add a new reporting context for your XBRL tags.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-4'>
            <FormField
              control={form.control}
              name='context_id'
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Context ID</FormLabel>
                  <FormControl>
                    <Input placeholder='e.g., FY2023' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className='grid grid-cols-2 gap-4'>
              <FormField
                control={form.control}
                name='entity_identifier'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Entity Identifier</FormLabel>
                    <FormControl>
                      <Input placeholder='e.g., 0001234567' {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name='entity_name'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Entity Name</FormLabel>
                    <FormControl>
                      <Input placeholder='Optional' {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <FormField
              control={form.control}
              name='entity_scheme'
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Entity Scheme</FormLabel>
                  <FormControl>
                    <Input placeholder='http://www.sec.gov/CIK' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name='period_type'
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Period Type</FormLabel>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder='Select period type' />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value='duration'>Duration</SelectItem>
                      <SelectItem value='instant'>Instant</SelectItem>
                      <SelectItem value='forever'>Forever</SelectItem>
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            {periodType === 'duration' && (
              <div className='grid grid-cols-2 gap-4'>
                <FormField
                  control={form.control}
                  name='start_date'
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Start Date</FormLabel>
                      <FormControl>
                        <Input type='date' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name='end_date'
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>End Date</FormLabel>
                      <FormControl>
                        <Input type='date' {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            )}

            {periodType === 'instant' && (
              <FormField
                control={form.control}
                name='instant_date'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Instant Date</FormLabel>
                    <FormControl>
                      <Input type='date' {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}

            <FormField
              control={form.control}
              name='taxonomy_id'
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Taxonomy ID (Optional)</FormLabel>
                  <FormControl>
                    <Input type='number' placeholder='e.g., 3' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <DialogFooter>
              <Button type='submit' disabled={createContextMutation.isPending}>
                {createContextMutation.isPending && (
                  <Loader2 className='mr-2 h-4 w-4 animate-spin' />
                )}
                Create Context
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
