'use client';

import * as React from 'react';
import { Check, ChevronsUpDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import brsrTaxonomy from '@/lib/brsr-taxonomy.json';

interface TagSelectorProps {
  value: string;
  onValueChange: (value: string) => void;
  placeholder?: string;
  className?: string;
}

export function TagSelector({
  value,
  onValueChange,
  placeholder = 'Search BRSR tags...',
  className,
}: TagSelectorProps) {
  const [open, setOpen] = React.useState(false);
  const [search, setSearch] = React.useState('');

  const allTags = React.useMemo(() => brsrTaxonomy.tags || [], []);

  const filteredTags = React.useMemo(() => {
    if (!search) return allTags.slice(0, 100);

    const searchLower = search.toLowerCase();
    return allTags
      .filter((tag) => tag.toLowerCase().includes(searchLower))
      .slice(0, 100);
  }, [search, allTags]);

  const handleSelect = (currentValue: string) => {
    onValueChange(currentValue === value ? '' : currentValue);
    setOpen(false);
    setSearch('');
  };

  return (
    <div className="space-y-1">
      {value && (
        <div className="px-2 py-1 text-xs text-muted-foreground bg-muted/50 rounded border">
          <span className="font-semibold">Current: </span>
          <span className="font-mono break-all">{value}</span>
        </div>
      )}
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            title={value || placeholder}
            className={cn(
              'w-full justify-between font-mono text-sm',
              !value && 'text-muted-foreground',
              className
            )}
          >
            <span className="truncate">
              {value || placeholder}
            </span>
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[500px] p-0" align="start">
          <Command shouldFilter={false}>
            <CommandInput
              placeholder="Search all 2,543 BRSR tags..."
              value={search}
              onValueChange={setSearch}
            />
            <CommandList>
              <CommandEmpty>No tags found.</CommandEmpty>
              <CommandGroup>
                {filteredTags.map((tag) => (
                  <CommandItem
                    key={tag}
                    value={tag}
                    onSelect={handleSelect}
                    title={tag}
                    className="font-mono text-xs"
                  >
                    <Check
                      className={cn(
                        'mr-2 h-4 w-4 shrink-0',
                        value === tag ? 'opacity-100' : 'opacity-0'
                      )}
                    />
                    <span className="break-all">{tag}</span>
                  </CommandItem>
                ))}
              </CommandGroup>
              {!search && filteredTags.length > 0 && (
                <div className="border-t px-2 py-1.5 text-xs text-muted-foreground bg-muted/30">
                  Showing first 100 of 2,543 tags. Type to search all.
                </div>
              )}
              {search && filteredTags.length > 0 && (
                <div className="border-t px-2 py-1.5 text-xs text-muted-foreground bg-muted/30">
                  Showing {filteredTags.length} of{' '}
                  {allTags.filter((tag) => tag.toLowerCase().includes(search.toLowerCase())).length}{' '}
                  results
                </div>
              )}
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}
