'use client';

import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
} from 'lucide-react';
import { cn } from '@/lib/utils';

export interface PaginationProps {
  currentPage: number | undefined;
  totalPages: number | undefined;
  totalItems: number | undefined;
  itemsPerPage: number | undefined;
  onPageChange: (page: number) => void;
  onItemsPerPageChange?: (itemsPerPage: number) => void;
  showItemsPerPage?: boolean;
  showInfo?: boolean;
  maxVisiblePages?: number;
  className?: string;
}

export function Pagination({
  currentPage,
  totalPages,
  totalItems,
  itemsPerPage,
  onPageChange,
  onItemsPerPageChange,
  showItemsPerPage = true,
  showInfo = true,
  maxVisiblePages = 5,
  className,
}: PaginationProps) {
  if (!currentPage || !totalPages || !totalItems || !itemsPerPage) return null;

  const canGoPrevious = currentPage > 1;
  const canGoNext = currentPage < totalPages;

  const getPageNumbers = (): (number | '...')[] => {
    if (totalPages <= maxVisiblePages) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    const pages: (number | '...')[] = [];
    const halfVisible = Math.floor(maxVisiblePages / 2);

    if (currentPage <= halfVisible + 1) {
      for (let i = 1; i <= maxVisiblePages - 1; i++) {
        pages.push(i);
      }
      pages.push('...');
      pages.push(totalPages);
    } else if (currentPage >= totalPages - halfVisible) {
      pages.push(1);
      pages.push('...');
      for (let i = totalPages - maxVisiblePages + 2; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      pages.push(1);
      pages.push('...');
      for (
        let i = currentPage - halfVisible + 1;
        i <= currentPage + halfVisible - 1;
        i++
      ) {
        pages.push(i);
      }
      pages.push('...');
      pages.push(totalPages);
    }

    return pages;
  };

  const startItem = (currentPage - 1) * itemsPerPage + 1;
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  return (
    <div
      className={cn(
        'flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between',
        className
      )}
    >
      {showInfo && (
        <div className="text-sm text-muted-foreground">
          Showing {startItem} to {endItem} of {totalItems} results
        </div>
      )}

      <div className="flex items-center gap-2">
        {showItemsPerPage && onItemsPerPageChange && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">Show</span>
            <Select
              value={itemsPerPage.toString()}
              onValueChange={(value) =>
                onItemsPerPageChange(Number.parseInt(value))
              }
            >
              <SelectTrigger className="w-16">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="5">5</SelectItem>
                <SelectItem value="10">10</SelectItem>
                <SelectItem value="20">20</SelectItem>
                <SelectItem value="50">50</SelectItem>
                <SelectItem value="100">100</SelectItem>
              </SelectContent>
            </Select>
          </div>
        )}

        <div className="flex items-center gap-1">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onPageChange(1)}
            disabled={!canGoPrevious}
            className="h-8 w-8 p-0"
          >
            <ChevronsLeft className="h-4 w-4" />
            <span className="sr-only">Go to first page</span>
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={() => onPageChange(currentPage - 1)}
            disabled={!canGoPrevious}
            className="h-8 w-8 p-0"
          >
            <ChevronLeft className="h-4 w-4" />
            <span className="sr-only">Go to previous page</span>
          </Button>

          {getPageNumbers().map((page, index) => (
            <Button
              key={index}
              variant={page === currentPage ? 'default' : 'outline'}
              size="sm"
              onClick={() => typeof page === 'number' && onPageChange(page)}
              disabled={page === '...'}
              className={cn(
                'h-8 w-8 p-0',
                page === '...' && 'cursor-default hover:bg-transparent'
              )}
            >
              {page}
              {typeof page === 'number' && (
                <span className="sr-only">Go to page {page}</span>
              )}
            </Button>
          ))}

          <Button
            variant="outline"
            size="sm"
            onClick={() => onPageChange(currentPage + 1)}
            disabled={!canGoNext}
            className="h-8 w-8 p-0"
          >
            <ChevronRight className="h-4 w-4" />
            <span className="sr-only">Go to next page</span>
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={() => onPageChange(totalPages)}
            disabled={!canGoNext}
            className="h-8 w-8 p-0"
          >
            <ChevronsRight className="h-4 w-4" />
            <span className="sr-only">Go to last page</span>
          </Button>
        </div>
      </div>
    </div>
  );
}
