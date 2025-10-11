'use client';

import type { ReportDocument } from '@/types/report';
import { Button } from '@/components/ui/button';
import { Trash2, Eye, ExternalLink, CheckCircle, Tag } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { useDeleteFeedback } from '@/features/recommender/api/delete-feedback';

interface TaggedFactsListProps {
  report: ReportDocument;
  onBlockSelect: (blockId: string) => void;
  onReportChange?: (report: ReportDocument) => void;
}

export function TaggedFactsList({
  report,
  onBlockSelect,
  onReportChange,
}: TaggedFactsListProps) {
  const [deletingTags, setDeletingTags] = useState<Set<string>>(new Set());
  const router = useRouter();

  // Hook for deleting feedback associated with a tag. When a tag that
  // originated from a recommendation is removed, this will remove the
  // corresponding feedback entry in the AI recommender. Use the mutate
  // function to trigger the API call.
  const { mutate: deleteFeedback } = useDeleteFeedback();

  // Collect all tags.  For tags originating from PDF pages, the report
  // block may not contain any text (content is empty).  In those cases,
  // the tag will carry a `selectedText` property (set when the tag
  // was created) containing the selected text.  Use this property
  // whenever available; otherwise, fall back to computing the substring
  // from the block's content using start and end indices.
  const allTags = report.blocks.flatMap((block) =>
    block.tags.map((tag) => {
      const taggedText = (tag as any)?.selectedText
        ? (tag as any).selectedText
        : tag.startIndex !== undefined && tag.endIndex !== undefined
          ? block.content.substring(tag.startIndex, tag.endIndex)
          : block.content;
      return {
        ...tag,
        blockId: block.id,
        blockContent: block.content,
        taggedText,
      };
    })
  );

  const handleDeleteTag = async (blockId: string, tagId: string) => {
    if (!onReportChange) {
      toast.error('Cannot delete tag', {
        description: 'Missing update handler',
      });
      return;
    }

    setDeletingTags((prev) => new Set(prev).add(tagId));

    try {
      const block = report.blocks.find((b) => b.id === blockId);
      const tag = block?.tags.find((t) => t.id === tagId);

      if (!block || !tag) {
        toast.error('Cannot delete tag', { description: 'Tag not found' });
        return;
      }

      const updatedReport = {
        ...report,
        blocks: report.blocks.map((currentBlock) =>
          currentBlock.id === blockId
            ? {
                ...currentBlock,
                tags: currentBlock.tags.filter(
                  (currentTag) => currentTag.id !== tagId
                ),
              }
            : currentBlock
        ),
        updatedAt: new Date().toISOString(),
      };

      onReportChange(updatedReport);

      // If the tag has an associated feedback ID, delete the feedback
      // entry from the AI recommender. We call the mutation without
      // blocking the UI; the deletion happens in the background. Any
      // errors will be handled internally by the hook.
      if ((tag as any)?.feedbackId !== undefined) {
        deleteFeedback({ id: (tag as any).feedbackId });
      }

      toast.success('Tag deleted', {
        description: `Removed "${tag.concept.label}"`,
        icon: <CheckCircle className='w-4 h-4' />,
        duration: 2000,
      });
    } catch (error) {
      console.error('Error deleting tag:', error);
      toast.error('Failed to delete tag');
    } finally {
      setDeletingTags((prev) => {
        const newSet = new Set(prev);
        newSet.delete(tagId);
        return newSet;
      });
    }
  };

  const handleViewInTaxonomy = (tag: any) => {
    const queryParams = new URLSearchParams({
      conceptId: tag.concept.id,
      conceptLabel: tag.concept.label || '',
      conceptType: tag.concept.type || '',
      periodType: tag.concept.periodType || '',
    });
    router.push(`/taxonomy?${queryParams.toString()}`);
  };

  const handleViewInDocument = (blockId: string) => {
    onBlockSelect(blockId);
    toast.success('Navigated to document', { duration: 1500 });
  };

  // Empty state
  if (allTags.length === 0) {
    return (
      <div className='flex flex-col items-center justify-center h-full py-8 text-center'>
        <div className='flex items-center justify-center w-12 h-12 mb-4 rounded-full bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900/20 dark:to-pink-900/20'>
          <Tag className='w-6 h-6 text-purple-600' />
        </div>
        <h3 className='mb-2 text-base font-semibold'>No Tagged Facts Yet</h3>
        <p className='max-w-sm text-sm leading-relaxed text-muted-foreground'>
          Start by selecting text in the document and adding tags.
        </p>
      </div>
    );
  }

  return (
    <div className='flex flex-col h-full min-h-0'>
      {/* Header */}
      <div className='flex-shrink-0 mb-3 text-sm text-muted-foreground'>
        {allTags.length} tagged fact{allTags.length !== 1 ? 's' : ''}
      </div>

      {/* Scrollable List */}
      <div className='flex-1 pr-1 space-y-3 overflow-y-auto'>
        {allTags.map((tag) => {
          const isDeleting = deletingTags.has(tag.id);
          const isESRS = tag.concept.id.toLowerCase().includes('esrs');

          return (
            <Card
              key={tag.id}
              className={`transition-all duration-200 border-l-4 ${
                isESRS
                  ? 'border-l-emerald-500 bg-emerald-50/50 dark:bg-emerald-950/10'
                  : 'border-l-blue-500 bg-blue-50/50 dark:bg-blue-950/10'
              } ${isDeleting ? 'opacity-50 scale-95' : 'hover:shadow-md'}`}
            >
              <CardHeader className='pb-2'>
                <div className='flex items-start justify-between gap-2'>
                  <div className='flex-1 min-w-0'>
                    <CardTitle className='text-sm font-semibold leading-tight break-words'>
                      {tag.concept.label}
                    </CardTitle>
                    <div className='flex items-center gap-1 mt-1'>
                      <Badge
                        variant='outline'
                        className={`text-xs ${
                          isESRS
                            ? 'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-900/20 dark:text-emerald-300'
                            : 'bg-blue-100 text-blue-800 border-blue-300 dark:bg-blue-900/20 dark:text-blue-300'
                        }`}
                      >
                        {tag?.concept?.id}
                      </Badge>
                    </div>
                  </div>
                  <Button
                    size='icon'
                    variant='ghost'
                    className='flex-shrink-0 w-6 h-6 hover:bg-destructive hover:text-destructive-foreground'
                    onClick={() => handleDeleteTag(tag.blockId, tag.id)}
                    disabled={isDeleting}
                  >
                    <Trash2 className='w-3 h-3' />
                  </Button>
                </div>
              </CardHeader>

              <CardContent className='pt-0'>
                {/* Tagged Text */}
                <span className='text-xs'>Tagged text:</span>
                <div
                  className={`p-2 rounded border text-xs break-words leading-relaxed max-h-24 overflow-hidden text-ellipsis bg-emerald-50 border-emerald-200 dark:bg-emerald-950/20 dark:border-emerald-800'`}
                >
                  {tag.taggedText}
                </div>
                {/* Actions */}
                {/* <div className='flex gap-2'>
                  <Button
                    variant='outline'
                    size='sm'
                    className='flex-1 text-xs h-7 hover:bg-primary hover:text-primary-foreground'
                    onClick={() => handleViewInDocument(tag.blockId)}
                  >
                    <Eye className='w-3 h-3 mr-1' />
                    View
                  </Button>
                  <Button
                    variant='outline'
                    size='sm'
                    className='flex-1 text-xs h-7 hover:bg-secondary hover:text-secondary-foreground'
                    onClick={() => handleViewInTaxonomy(tag)}
                  >
                    <ExternalLink className='w-3 h-3 mr-1' />
                    Taxonomy
                  </Button>
                </div> */}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
