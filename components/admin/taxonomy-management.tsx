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
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAllTaxonomies } from '@/features/taxonomy/api/get-all-taxonomy-list';
import { useEnableTaxonomy } from '@/features/taxonomy/api/enable-taxonomy';
import { useDisableTaxonomy } from '@/features/taxonomy/api/disable-taxonomy';
import { toast } from 'sonner'; // or your preferred toast library

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
      month: 'long',
      day: 'numeric',
    }).format(d);
  } catch {
    return iso;
  }
}

export default function TaxonomyManagement() {
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

  if (isLoading) {
    return (
      <div className='w-full text-center py-10'>
        <Loader2 className='size-6 animate-spin mx-auto mb-2' />
        <div className='text-sm text-muted-foreground'>
          Loading taxonomies...
        </div>
      </div>
    );
  }

  if (!taxonomiesList?.length) {
    return (
      <div className='w-full text-center text-sm text-muted-foreground py-10'>
        No taxonomies found.
      </div>
    );
  }

  return (
    <div className='w-full p-4'>
      {/* Responsive grid: 1 on mobile, 2 on small, 3 on large, 4 on xl */}
      <div className='grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3'>
        {taxonomiesList.map((t) => {
          const isEnabled = t.enabled;
          const createdLabel = `Created on ${formatISODate(t.created_at)}`;
          const isActionPending = isEnabling || isDisabling;

          return (
            <Card
              key={t.id}
              className='flex flex-col transition-shadow hover:shadow-md '
            >
              <CardHeader className='p-4'>
                <div className='flex items-start justify-between gap-2'>
                  <div>
                    <CardTitle className='text-pretty'>{t.name}</CardTitle>
                    <CardDescription className='truncate'>
                      {t.file_name}
                    </CardDescription>
                  </div>

                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant='ghost'
                        size='icon'
                        aria-label={`More options for ${t.name}`}
                        title='More'
                        className='text-muted-foreground hover:text-foreground'
                        disabled={isActionPending}
                      >
                        {isActionPending ? (
                          <Loader2
                            className='size-4 animate-spin'
                            aria-hidden='true'
                          />
                        ) : (
                          <MoreHorizontal
                            className='size-4'
                            aria-hidden='true'
                          />
                        )}
                        <span className='sr-only'>More</span>
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent align='end' className='w-56 p-2'>
                      <div
                        role='menu'
                        aria-label={`More options for ${t.name}`}
                        className='flex flex-col gap-1'
                      >
                        {!isEnabled ? (
                          <Button
                            variant='ghost'
                            className='justify-start gap-2 text-emerald-600 hover:text-emerald-700'
                            onClick={() => handleEnableTaxonomy(t.id)}
                            role='menuitem'
                            disabled={isActionPending}
                          >
                            {isEnabling ? (
                              <Loader2
                                className='size-4 animate-spin'
                                aria-hidden='true'
                              />
                            ) : (
                              <CheckCircle2
                                className='size-4'
                                aria-hidden='true'
                              />
                            )}
                            Enable
                          </Button>
                        ) : (
                          <Button
                            variant='ghost'
                            className='justify-start gap-2 text-rose-600 hover:text-rose-700'
                            onClick={() => handleDisableTaxonomy(t.id)}
                            role='menuitem'
                            disabled={isActionPending}
                          >
                            {isDisabling ? (
                              <Loader2
                                className='size-4 animate-spin'
                                aria-hidden='true'
                              />
                            ) : (
                              <XCircle className='size-4' aria-hidden='true' />
                            )}
                            Disable
                          </Button>
                        )}
                      </div>
                    </PopoverContent>
                  </Popover>
                </div>
              </CardHeader>

              <CardContent className='flex-1 p-4 pt'>
                <div className='flex items-center justify-between'>
                  <div
                    role='status'
                    aria-live='polite'
                    aria-atomic='true'
                    className={cn(
                      'inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium',
                      isEnabled
                        ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
                        : 'border-rose-200 bg-rose-50 text-rose-700'
                    )}
                  >
                    {isEnabled ? (
                      <>
                        <CheckCircle2 className='size-3.5' aria-hidden='true' />
                        Enabled
                      </>
                    ) : (
                      <>
                        <XCircle className='size-3.5' aria-hidden='true' />
                        Disabled
                      </>
                    )}
                  </div>
                </div>

                <div className='mt-3 space-y-2 text-sm'>
                  <div className='flex items-center gap-2 text-muted-foreground'>
                    <FileText className='size-4' aria-hidden='true' />
                    <code className='rounded bg-muted px-1.5 py-0.5 text-foreground/90'>
                      {t.file_name}
                    </code>
                  </div>
                  <div className='flex items-center gap-2 text-muted-foreground'>
                    <CalendarDays className='size-4' aria-hidden='true' />
                    <span>{createdLabel}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
