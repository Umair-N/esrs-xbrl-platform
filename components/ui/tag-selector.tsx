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
    <TooltipProvider delayDuration={300}>
      <div className="space-y-2">
        {value && (
          <div className="px-3 py-2.5 rounded-lg border-2 border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950 dark:border-blue-800">
            <div className="flex items-center justify-between gap-3">
              <div className="flex-1 min-w-0">
                <div className="text-[10px] font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400 mb-1">
                  Selected Tag
                </div>
                <code className="text-sm font-bold text-slate-800 dark:text-slate-100 break-all block leading-relaxed">
                  {value}
                </code>
              </div>
              {currentTagData?.reference && (
                <Tooltip>
                  <TooltipTrigger asChild>
                    <button
                      type="button"
                      className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900 hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <Info className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                    </button>
                  </TooltipTrigger>
                  <TooltipContent side="top" className="max-w-md p-3 bg-white dark:bg-slate-800 shadow-lg">
                    <p className="text-sm font-medium leading-relaxed text-slate-700 dark:text-slate-200">
                      {currentTagData.reference}
                    </p>
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
                'w-full justify-between h-11 px-4 font-semibold text-sm border-2 hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-950 transition-all',
                !value && 'text-muted-foreground font-normal',
                value && 'font-mono text-slate-700 dark:text-slate-200',
                className
              )}
            >
              <span className="truncate">
                {value || placeholder}
              </span>
              <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-60" />
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-[650px] p-0 shadow-xl" align="start">
            <Command shouldFilter={false}>
              <div className="border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-3 py-2">
                <div className="text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-2">
                  Search BRSR Tags
                </div>
                <CommandInput
                  placeholder="Type to search all 2,646 tags..."
                  value={search}
                  onValueChange={setSearch}
                  className="font-medium"
                />
              </div>
              <CommandList>
                <CommandEmpty className="py-8 text-center">
                  <div className="flex flex-col items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
                      <span className="text-2xl">🔍</span>
                    </div>
                    <div>
                      <p className="font-semibold text-slate-700 dark:text-slate-300">No tags found</p>
                      <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Try a different search term</p>
                    </div>
                  </div>
                </CommandEmpty>
                <CommandGroup className="p-2">
                  {filteredTags.map((tagData) => (
                    <CommandItem
                      key={tagData.tag}
                      value={tagData.tag}
                      onSelect={handleSelect}
                      className={cn(
                        "px-3 py-3 rounded-md mb-1 cursor-pointer transition-all",
                        "hover:bg-blue-50 dark:hover:bg-blue-950",
                        value === tagData.tag && "bg-blue-100 dark:bg-blue-900 border border-blue-300 dark:border-blue-700"
                      )}
                    >
                      <Check
                        className={cn(
                          'mr-3 h-4 w-4 shrink-0 text-blue-600 dark:text-blue-400',
                          value === tagData.tag ? 'opacity-100' : 'opacity-0'
                        )}
                      />
                      <div className="flex-1 min-w-0 flex items-center gap-3">
                        <code className="break-all flex-1 text-sm font-semibold text-slate-700 dark:text-slate-200 leading-relaxed">
                          {tagData.tag}
                        </code>
                        {tagData.reference && (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <button
                                type="button"
                                className="flex items-center justify-center w-7 h-7 rounded-full bg-blue-100 dark:bg-blue-900 hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
                                onClick={(e) => e.stopPropagation()}
                              >
                                <Info className="h-3.5 w-3.5 text-blue-600 dark:text-blue-400" />
                              </button>
                            </TooltipTrigger>
                            <TooltipContent side="right" className="max-w-md p-4 bg-white dark:bg-slate-800 shadow-xl border-2 border-blue-200 dark:border-blue-700">
                              <div className="space-y-2">
                                <div className="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                                  Reference
                                </div>
                                <p className="text-sm font-medium leading-relaxed text-slate-700 dark:text-slate-200">
                                  {tagData.reference}
                                </p>
                                {tagData.type && (
                                  <div className="pt-2 border-t border-slate-200 dark:border-slate-700">
                                    <p className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                                      Type: <span className="font-mono text-slate-600 dark:text-slate-300">{tagData.type}</span>
                                    </p>
                                  </div>
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
                  <div className="border-t-2 border-slate-200 dark:border-slate-700 px-4 py-2.5 bg-gradient-to-r from-slate-50 to-blue-50 dark:from-slate-900 dark:to-blue-950">
                    <p className="text-xs font-semibold text-slate-600 dark:text-slate-400">
                      📋 Showing first <span className="text-blue-600 dark:text-blue-400">100</span> of{' '}
                      <span className="text-blue-600 dark:text-blue-400">2,646</span> tags. Type to search all.
                    </p>
                  </div>
                )}
                {search && filteredTags.length > 0 && (
                  <div className="border-t-2 border-slate-200 dark:border-slate-700 px-4 py-2.5 bg-gradient-to-r from-slate-50 to-green-50 dark:from-slate-900 dark:to-green-950">
                    <p className="text-xs font-semibold text-slate-600 dark:text-slate-400">
                      🔍 Found <span className="text-green-600 dark:text-green-400">{filteredTags.length}</span> of{' '}
                      <span className="text-green-600 dark:text-green-400">
                        {allTags.filter((t) => t.searchText.includes(search.toLowerCase())).length}
                      </span>{' '}
                      matching tags
                    </p>
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
