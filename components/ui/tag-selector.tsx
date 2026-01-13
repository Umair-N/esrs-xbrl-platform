'use client';

import * as React from 'react';
import { Check, ChevronsUpDown, Info } from 'lucide-react';
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
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import brsrTaxonomyWithReferences from '@/lib/brsr-taxonomy-with-references.json';

interface TagSelectorProps {
  value: string;
  onValueChange: (value: string) => void;
  placeholder?: string;
  className?: string;
}

type TagData = {
  tag: string;
  reference: string;
  type: string;
  shortName: string;
  searchText: string;
};

export function TagSelector({
  value,
  onValueChange,
  placeholder = 'Search BRSR tags...',
  className,
}: TagSelectorProps) {
  const [open, setOpen] = React.useState(false);
  const [search, setSearch] = React.useState('');

  // Convert the taxonomy object to array of tag data
  const allTags = React.useMemo(() => {
    const taxonomy = brsrTaxonomyWithReferences as Record<string, TagData>;
    return Object.values(taxonomy);
  }, []);

  const filteredTags = React.useMemo(() => {
    if (!search) return allTags.slice(0, 100);

    const searchLower = search.toLowerCase();
    return allTags
      .filter((tagData) => tagData.searchText.includes(searchLower))
      .slice(0, 100);
  }, [search, allTags]);

  const handleSelect = (currentValue: string) => {
    onValueChange(currentValue === value ? '' : currentValue);
    setOpen(false);
    setSearch('');
  };

  // Find current tag reference
  const currentTagData = allTags.find((t) => t.tag === value);

  return (
    <TooltipProvider>
      <div className="space-y-1">
        {value && (
          <div className="px-2 py-1 text-xs text-muted-foreground bg-muted/50 rounded border">
            <div className="flex items-center justify-between gap-2">
              <div className="flex-1 min-w-0">
                <span className="font-semibold">Current: </span>
                <span className="font-mono break-all">{value}</span>
              </div>
              {currentTagData?.reference && (
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Info className="h-4 w-4 text-blue-500 shrink-0 cursor-help" />
                  </TooltipTrigger>
                  <TooltipContent side="top" className="max-w-md">
                    <p className="text-sm">{currentTagData.reference}</p>
                  </TooltipContent>
                </Tooltip>
              )}
            </div>
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
          <PopoverContent className="w-[600px] p-0" align="start">
            <Command shouldFilter={false}>
              <CommandInput
                placeholder="Search all 2,646 BRSR tags..."
                value={search}
                onValueChange={setSearch}
              />
              <CommandList>
                <CommandEmpty>No tags found.</CommandEmpty>
                <CommandGroup>
                  {filteredTags.map((tagData) => (
                    <CommandItem
                      key={tagData.tag}
                      value={tagData.tag}
                      onSelect={handleSelect}
                      className="font-mono text-xs py-2"
                    >
                      <Check
                        className={cn(
                          'mr-2 h-4 w-4 shrink-0',
                          value === tagData.tag ? 'opacity-100' : 'opacity-0'
                        )}
                      />
                      <div className="flex-1 min-w-0 flex items-center gap-2">
                        <span className="break-all flex-1">{tagData.tag}</span>
                        {tagData.reference && (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Info className="h-3.5 w-3.5 text-blue-500 shrink-0 cursor-help" />
                            </TooltipTrigger>
                            <TooltipContent side="right" className="max-w-md">
                              <div className="space-y-1">
                                <p className="text-sm font-medium">{tagData.reference}</p>
                                {tagData.type && (
                                  <p className="text-xs text-muted-foreground">Type: {tagData.type}</p>
                                )}
                              </div>
                            </TooltipContent>
                          </Tooltip>
                        )}
                      </div>
                    </CommandItem>
                  ))}
                </CommandGroup>
                {!search && filteredTags.length > 0 && (
                  <div className="border-t px-2 py-1.5 text-xs text-muted-foreground bg-muted/30">
                    Showing first 100 of 2,646 tags. Type to search all.
                  </div>
                )}
                {search && filteredTags.length > 0 && (
                  <div className="border-t px-2 py-1.5 text-xs text-muted-foreground bg-muted/30">
                    Showing {filteredTags.length} of{' '}
                    {allTags.filter((t) => t.searchText.includes(search.toLowerCase())).length}{' '}
                    results
                  </div>
                )}
              </CommandList>
            </Command>
          </PopoverContent>
        </Popover>
      </div>
    </TooltipProvider>
  );
}
