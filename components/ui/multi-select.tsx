import { useState } from 'react';
import * as z from 'zod';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from '@/components/ui/command';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Check, ChevronsUpDown, X } from 'lucide-react';
import { cn } from '@/lib/utils';

// Type definitions
interface User {
  id: string;
  name: string;
  email: string;
  status: 'active' | 'inactive';
  platform_access?: boolean;
}

interface TaxonomyOption {
  value: string;
  label: string;
}

interface MultiSelectProps {
  value: string[];
  onValueChange: (value: string[]) => void;
  options: TaxonomyOption[];
  placeholder: string;
}

interface SetTaxonomyModalProps {
  user: User | null;
  open: boolean;
  setOpen: (open: boolean) => void;
}

interface UserActionsDropdownProps {
  user: User;
  setActionUser: (user: User) => void;
  setActionType: (type: 'enable' | 'disable' | 'grant' | 'revoke') => void;
  setSelectedUser: (user: User) => void;
}

// Zod schema for form validation
const taxonomyFormSchema = z.object({
  taxonomies: z.array(z.string()).min(1, {
    message: 'Please select at least one taxonomy.',
  }),
});

type TaxonomyFormValues = z.infer<typeof taxonomyFormSchema>;

// Mock taxonomy options - replace with your actual taxonomies
const taxonomyOptions: TaxonomyOption[] = [
  { value: 'admin', label: 'Administrator' },
  { value: 'editor', label: 'Editor' },
  { value: 'viewer', label: 'Viewer' },
  { value: 'moderator', label: 'Moderator' },
  { value: 'analyst', label: 'Analyst' },
  { value: 'content_creator', label: 'Content Creator' },
  { value: 'reviewer', label: 'Reviewer' },
];

// Multi-select component using shadcn/ui
export const MultiSelect: React.FC<MultiSelectProps> = ({
  value,
  onValueChange,
  options,
  placeholder,
}) => {
  const [open, setOpen] = useState<boolean>(false);

  const handleSelect = (selectedValue: string): void => {
    const newValue = value.includes(selectedValue)
      ? value.filter((v) => v !== selectedValue)
      : [...value, selectedValue];
    onValueChange(newValue);
  };

  const handleRemove = (valueToRemove: string): void => {
    onValueChange(value.filter((v) => v !== valueToRemove));
  };

  return (
    <div className='space-y-2 w-full '>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant='outline'
            role='combobox'
            aria-expanded={open}
            className='w-full justify-between'
          >
            {value.length === 0 ? placeholder : `${value.length} selected`}
            <ChevronsUpDown className='ml-2 h-4 w-4 shrink-0 opacity-50' />
          </Button>
        </PopoverTrigger>
        <PopoverContent className='w-[27rem] p-0 '>
          <Command>
            <CommandInput placeholder='Search taxonomies...' />
            <CommandEmpty>No taxonomy found.</CommandEmpty>
            <CommandGroup>
              {options.map((option) => (
                <CommandItem
                  key={option.value}
                  value={option.value}
                  onSelect={() => handleSelect(option.value)}
                >
                  <Check
                    className={cn(
                      'mr-2 h-4 w-4',
                      value.includes(option.value) ? 'opacity-100' : 'opacity-0'
                    )}
                  />
                  {option.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </Command>
        </PopoverContent>
      </Popover>

      {value.length > 0 && (
        <div className='flex flex-wrap gap-2'>
          {value.map((selectedValue) => {
            const option = options.find((opt) => opt.value === selectedValue);
            return (
              <Badge key={selectedValue} variant='secondary' className='pr-1'>
                {option?.label}
                <Button
                  variant='ghost'
                  size='sm'
                  className='ml-1 h-auto p-0 text-muted-foreground hover:text-foreground'
                  onClick={() => handleRemove(selectedValue)}
                >
                  <X className='h-3 w-3' />
                </Button>
              </Badge>
            );
          })}
        </div>
      )}
    </div>
  );
};
