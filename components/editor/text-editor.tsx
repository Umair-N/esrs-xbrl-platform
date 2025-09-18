'use client';

import type { ReportDocument, ReportBlock } from '@/types/report';
import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { Textarea } from '@/components/ui/textarea';
import { Edit2, Check, X, Lightbulb, LucideInfo } from 'lucide-react';
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { Separator } from '@/components/ui/separator';
import type { JSX } from 'react/jsx-runtime';
import { useRecommendations } from '@/features/recommender/api/get-recommendations';
import { usePostFeedback } from '@/features/recommender/api/post-feedback';
import { useTaxonomyStore } from '@/store/taxonomoy-store';
import { useTaggingStore } from '@/store/tagging-store';
import { sampleContexts } from '@/lib/sample-data';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '../ui/tooltip';

/**
 * Tag structure in a ReportBlock:
 * {
 *   id: string;
 *   concept: {
 *     id: string;
 *     label: string;
 *     definition: string;
 *     type: string;
 *     periodType: string;
 *   };
 *   startIndex: number;
 *   endIndex: number;
 *   context?: any; // optional context info if needed
 * }
 */

interface TextEditorProps {
  report: ReportDocument;
  selectedBlockId: string | null;
  onBlockSelect: (blockId: string) => void;
  onReportChange: (report: ReportDocument) => void;
  onTextHighlight: (
    blockId: string,
    selectedText: string,
    startIndex: number,
    endIndex: number
  ) => void;
}

export function TextEditor({
  report,
  selectedBlockId,
  onBlockSelect,
  onReportChange,
  onTextHighlight,
}: TextEditorProps) {
  // Bring in the tagging store actions. When a recommendation is chosen, we
  // place the corresponding concept into the global store via setPendingConcept.
  // The tagging panel reads this and preselects the concept for context
  // assignment. We also expose the currently selected context ID should we
  // choose to automatically create tags when a context is already selected.

  const [editingBlockId, setEditingBlockId] = useState<string | null>(null);
  const [editedContent, setEditedContent] = useState('');
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const selectedTaxonomy = useTaxonomyStore((state) => state.selectedTaxonomy);

  // Bring in the tagging store actions. When a recommendation is chosen, we
  // place the corresponding concept into the global store via setPendingConcept.
  // The tagging panel reads this and preselects the concept for context
  // assignment. We also expose the currently selected context ID should we
  // choose to automatically create tags when a context is already selected.
  const { setPendingConcept, selectedContextId } = useTaggingStore();

  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [showPopover, setShowPopover] = useState(false);
  const [highlightedText, setHighlightedText] = useState('');
  const [popoverTriggerElement, setPopoverTriggerElement] =
    useState<HTMLElement | null>(null);

  const [openInfo, setOpenInfo] = useState(false);
  // Track the highlighted range (blockId, startIndex, endIndex)
  const [highlightRange, setHighlightRange] = useState<{
    blockId: string;
    startIndex: number;
    endIndex: number;
  } | null>(null);

  const { mutate } = useRecommendations();
  // Hook for submitting feedback to the AI recommender. When a user selects
  // a suggestion, we will use this to notify the service about the choice.
  const { mutate: sendFeedback } = usePostFeedback();

  const handleBlockClick = (blockId: string) => {
    if (editingBlockId !== blockId) onBlockSelect(blockId);
  };

  const startEditing = (block: ReportBlock) => {
    setEditingBlockId(block.id);
    setEditedContent(block.content);
  };

  const saveEditing = () => {
    if (!editingBlockId) return;
    const updatedReport: ReportDocument = {
      ...report,
      blocks: report.blocks.map((block) =>
        block.id === editingBlockId
          ? { ...block, content: editedContent }
          : block
      ),
      updatedAt: new Date().toISOString(),
    };

    console.log('Saving edited block:', updatedReport);
    onReportChange(updatedReport);
    setEditingBlockId(null);

    // Persist the updated report to localStorage.
    if (typeof window !== 'undefined') {
      try {
        window.localStorage.setItem(
          'xbrl-editor-session',
          JSON.stringify(updatedReport)
        );
      } catch (err) {
        console.error('Failed to persist updated report:', err);
      }
    }
  };

  const cancelEditing = () => setEditingBlockId(null);

  /**
   * Handles highlighting text in a block.  Invokes the recommendations API
   * with the selected text and positions a popover next to the selection.
   */
  const handleTextSelection = (blockId: string) => {
    if (window.getSelection) {
      const selection = window.getSelection();
      if (selection && selection.toString().length > 0) {
        const range = selection.getRangeAt(0);
        const selectedText = selection.toString();
        const parentElement = range.commonAncestorContainer.parentElement;

        if (
          parentElement &&
          parentElement.closest(`[data-block-id="${blockId}"]`)
        ) {
          const blockContent =
            report.blocks.find((b) => b.id === blockId)?.content || '';
          const startIndex = blockContent.indexOf(selectedText);
          const endIndex = startIndex + selectedText.length;

          if (startIndex >= 0) {
            onTextHighlight(blockId, selectedText, startIndex, endIndex);
            setHighlightRange({ blockId, startIndex, endIndex });
          }

          const rect = range.getBoundingClientRect();
          const virtualElement = document.createElement('div');
          virtualElement.style.position = 'absolute';
          virtualElement.style.top = `${rect.bottom + window.scrollY}px`;
          virtualElement.style.left = `${rect.left + window.scrollX}px`;
          virtualElement.style.width = `${rect.width}px`;
          virtualElement.style.height = '1px';
          virtualElement.style.pointerEvents = 'none';
          document.body.appendChild(virtualElement);

          setPopoverTriggerElement(virtualElement);
          setHighlightedText(selectedText);

          // Query recommendations
          mutate(
            {
              data: {
                query: selectedText,
                taxonomy: selectedTaxonomy?.name?.toLocaleLowerCase() || '',
                k: 5,
                rerank: true,
              },
            },
            {
              onSuccess: (res: any) => {
                setRecommendations(res?.results ?? []);
                setShowPopover(true);
              },
              onError: () => {
                setRecommendations([]);
                setShowPopover(true);
              },
            }
          );
        }
      }
    }
  };

  /**
   * Apply a selected tag from the recommendations to the highlighted text.
   */
  const applyTag = (item: {
    tag: string;
    reference: string;
    datatype: string;
    rank?: number;
  }) => {
    // Guard against applying a tag when no text has been selected
    if (!highlightRange) return;

    // Capture the current highlight range and context ID. We'll need these
    // values later when creating the tag in the onSuccess/onError callbacks.
    const { blockId, startIndex, endIndex } = highlightRange;
    const localContextId = selectedContextId;

    // Construct a minimal concept object from the recommendation. Additional
    // metadata (e.g. definition, period type) may be resolved by the
    // taxonomy lookup within the tagging panel.
    const concept = {
      id: item.tag,
      label: item.reference,
      definition: '',
      type: item.datatype,
      periodType: '',
    };

    /**
     * Helper to finalise tag creation or pending concept storage. This
     * function is called after the feedback API responds. It receives
     * an optional feedback ID and uses captured variables from the
     * applyTag scope to update the report or pending concept. It also
     * hides the suggestion popover and clears the highlight range.
     */
    const finalizeTag = (feedbackId?: number) => {
      if (localContextId) {
        // If a context has been selected, create and attach the tag
        const context = sampleContexts.find((c) => c.id === localContextId);
        const newTag = {
          id: `${Date.now()}`,
          concept,
          startIndex,
          endIndex,
          ...(context ? { context } : {}),
          ...(feedbackId !== undefined ? { feedbackId } : {}),
        };
        const updatedReport: ReportDocument = {
          ...report,
          blocks: report.blocks.map((blk) =>
            blk.id === blockId ? { ...blk, tags: [...blk.tags, newTag] } : blk
          ),
          updatedAt: new Date().toISOString(),
        };
        onReportChange(updatedReport);
      } else {
        // No context selected yet; defer creation by storing the concept
        // along with its feedback ID (if any) in the global tagging store.
        if (feedbackId !== undefined) {
          setPendingConcept({ ...concept, feedbackId });
        } else {
          setPendingConcept(concept);
        }
      }

      // Hide the suggestion popover and clear the highlight range.
      setShowPopover(false);
      setHighlightRange(null);
      if (popoverTriggerElement) {
        document.body.removeChild(popoverTriggerElement);
        setPopoverTriggerElement(null);
      }
    };

    // Prepare the feedback payload. The AI recommender expects these
    // properties to record which suggestion was selected for the query. If
    // the rank is missing, default to 0.
    const feedbackPayload = {
      taxonomy: selectedTaxonomy?.name?.toLocaleLowerCase() || '',
      query: highlightedText,
      reference: item.reference,
      tag: item.tag,
      is_correct: true,
      is_custom: false,
      rank: item.rank ?? 0,
    };

    // Submit feedback and handle the response. We use the mutate function
    // returned from usePostFeedback to perform the API call. On success
    // we extract the returned ID and finalise tag creation. On error we
    // finalise without a feedback ID.
    sendFeedback(
      { data: feedbackPayload },
      {
        onSuccess: (res: any) => {
          // The feedback API returns an object containing an `id` field.
          const fid: number | undefined =
            res && typeof res.id === 'number' ? res.id : undefined;
          finalizeTag(fid);
        },
        onError: () => {
          finalizeTag(undefined);
        },
      }
    );
  };

  const closePopover = () => {
    setShowPopover(false);
    setHighlightRange(null);
    if (popoverTriggerElement) {
      document.body.removeChild(popoverTriggerElement);
      setPopoverTriggerElement(null);
    }
  };

  const renderTaggedContent = (block: ReportBlock) => {
    if (!block.tags || block.tags.length === 0) {
      return (
        <p className='font-medium leading-relaxed whitespace-pre-wrap'>
          {block.content}
        </p>
      );
    }

    const sortedTags = [...block.tags].sort(
      (a, b) => (a.startIndex || 0) - (b.startIndex || 0)
    );
    const segments: JSX.Element[] = [];
    let lastIndex = 0;

    sortedTags.forEach((tag, index) => {
      const startIndex = tag.startIndex || 0;
      const endIndex = tag.endIndex || block.content.length;

      if (startIndex > lastIndex) {
        segments.push(
          <span key={`text-${index}`} className='font-medium leading-relaxed'>
            {block.content.substring(lastIndex, startIndex)}
          </span>
        );
      }

      segments.push(
        <HoverCard key={`tag-${tag.id}`}>
          <HoverCardTrigger asChild>
            <span className='bg-primary/20 px-1 py-0.5 rounded cursor-help border-b border-dashed border-primary font-medium'>
              {block.content.substring(startIndex, endIndex)}
            </span>
          </HoverCardTrigger>
          <HoverCardContent className='w-80 '>
            <div className='space-y-3'>
              <h4 className='text-base font-semibold break-words'>
                {tag.concept.label}
              </h4>
              <p className='text-sm leading-relaxed break-words text-muted-foreground'>
                {tag.concept.definition}
              </p>
              <div className='flex flex-wrap gap-2 pt-1'>
                <Badge variant='outline' className='font-medium'>
                  {tag.concept.type}
                </Badge>
                <Badge variant='outline' className='font-medium'>
                  {tag.concept.periodType}
                </Badge>
              </div>
              <Separator />
              <div className='space-y-1 text-xs'>
                <p className='font-semibold'>Context: {tag?.context?.label}</p>
                <p className='text-muted-foreground'>
                  Entity: {tag?.context?.entityName} (
                  {tag?.context?.entityIdentifier})
                </p>
                <p className='text-muted-foreground'>
                  Period:{' '}
                  {tag?.context?.periodType === 'instant'
                    ? `As of ${new Date(tag.context.instantDate || '').toLocaleDateString()}`
                    : `${new Date(tag?.context?.startDate || '').toLocaleDateString()} to ${new Date(
                        tag?.context?.endDate || ''
                      ).toLocaleDateString()}`}
                </p>
              </div>
            </div>
          </HoverCardContent>
        </HoverCard>
      );

      lastIndex = endIndex;
    });

    if (lastIndex < block.content.length) {
      segments.push(
        <span key='text-last' className='font-medium leading-relaxed'>
          {block.content.substring(lastIndex)}
        </span>
      );
    }

    return <div className='whitespace-pre-wrap'>{segments}</div>;
  };

  /**
   * Persist unsaved edits to localStorage if the editor unmounts.
   */
  const latestEditingBlockId = useRef<string | null>(editingBlockId);
  const latestEditedContent = useRef<string>(editedContent);
  const latestReport = useRef<ReportDocument>(report);

  useEffect(() => {
    latestEditingBlockId.current = editingBlockId;
  }, [editingBlockId]);

  useEffect(() => {
    latestEditedContent.current = editedContent;
  }, [editedContent]);

  useEffect(() => {
    latestReport.current = report;
  }, [report]);

  useEffect(() => {
    return () => {
      const blockId = latestEditingBlockId.current;
      if (blockId) {
        const rep = latestReport.current;
        const updatedReport: ReportDocument = {
          ...rep,
          blocks: rep.blocks.map((block) =>
            block.id === blockId
              ? { ...block, content: latestEditedContent.current }
              : block
          ),
          updatedAt: new Date().toISOString(),
        };
        onReportChange(updatedReport);
        if (typeof window !== 'undefined') {
          try {
            window.localStorage.setItem(
              'xbrl-editor-session',
              JSON.stringify(updatedReport)
            );
          } catch (err) {
            console.error('Failed to persist unsaved edit on unmount:', err);
          }
        }
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className='flex flex-col h-full'>
      <style
        dangerouslySetInnerHTML={{
          __html: `
          .custom-scrollbar {
            scrollbar-width: thin;
            scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
          }
          .custom-scrollbar::-webkit-scrollbar {
            width: 8px;
          }
          .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent;
          }
          .custom-scrollbar::-webkit-scrollbar-thumb {
            background-color: rgba(156, 163, 175, 0.5);
            border-radius: 4px;
            border: 2px solid transparent;
            background-clip: content-box;
          }
          .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background-color: rgba(156, 163, 175, 0.7);
          }
        `,
        }}
      />

      {/* Blocks container */}
      <div className='flex-1 p-1 space-y-4'>
        {report.blocks.map((block) => (
          <div
            key={block.id}
            data-block-id={block.id}
            className={cn(
              'p-4 rounded-lg border transition-colors h-full',
              selectedBlockId === block.id && !editingBlockId
                ? 'border-primary bg-primary/5'
                : 'border-border hover:border-primary/50',
              editingBlockId === block.id ? 'border-primary' : 'min-h-fit'
            )}
            onClick={() => handleBlockClick(block.id)}
            onMouseUp={() =>
              selectedBlockId === block.id && handleTextSelection(block.id)
            }
          >
            {editingBlockId === block.id ? (
              <div className='flex flex-col w-full h-full space-y-3'>
                <Textarea
                  ref={textAreaRef}
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                  className='w-full resize-none text-base font-medium leading-relaxed max-h-[calc(100dvh-9rem)] overflow-y-auto custom-scrollbar h-full'
                  autoFocus
                />
                <div className='flex justify-end space-x-2'>
                  <Button size='sm' variant='outline' onClick={cancelEditing}>
                    <X className='w-4 h-4 mr-1' /> Cancel
                  </Button>
                  <Button size='sm' onClick={saveEditing}>
                    <Check className='w-4 h-4 mr-1' /> Save
                  </Button>
                </div>
              </div>
            ) : (
              <div className='relative group max-h-[calc(100dvh-12rem)] overflow-y-auto custom-scrollbar'>
                <div className='sticky top-0 right-0 z-10 float-right mb-2 ml-2 transition-opacity border rounded-full group-hover:opacity-100'>
                  <Button
                    size='sm'
                    variant='ghost'
                    onClick={(e) => {
                      e.stopPropagation();
                      startEditing(block);
                    }}
                    className='font-medium rounded-full shadow-md'
                  >
                    Edit
                    <Edit2 className='w-4 h-4' />
                  </Button>
                </div>
                <div className='leading-relaxed prose dark:prose-invert max-w-none'>
                  {renderTaggedContent(block)}
                </div>
                {block.tags && block.tags.length > 0 && (
                  <div className='flex flex-wrap clear-both gap-2 mt-3'>
                    {block.tags.map((tag) => (
                      <Badge
                        key={tag.id}
                        variant='outline'
                        className='inline-flex items-center px-3 py-1 text-xs font-semibold rounded-full bg-primary/10 text-primary'
                      >
                        {tag.concept.label}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <Popover open={showPopover} onOpenChange={setShowPopover}>
        <PopoverTrigger asChild>
          <div style={{ display: 'none' }} />
        </PopoverTrigger>
        <PopoverContent
          className='p-0 w-80'
          side='bottom'
          align='start'
          sideOffset={8}
          /*
           * Make the suggestion popover resizable by the user. We preserve
           * positioning when anchored to the highlighted text but always
           * include CSS resize and overflow properties so users can drag
           * the corner to adjust width and height. Without specifying
           * overflow: auto the resize handle would be hidden.
           */
          style={
            popoverTriggerElement
              ? {
                  position: 'fixed',
                  top: popoverTriggerElement.offsetTop,
                  left: popoverTriggerElement.offsetLeft,
                  resize: 'both',
                  overflow: 'auto',
                }
              : {
                  resize: 'both',
                  overflow: 'auto',
                }
          }
        >
          <div className='p-4'>
            <div className='flex items-center justify-between mb-3'>
              <div className='flex items-center gap-2'>
                <Lightbulb className='w-4 h-4 text-primary' />
                <span className='text-sm font-semibold'>
                  Suggestions for "{highlightedText?.slice(0, 50)}"
                </span>
              </div>
              <Button
                variant='ghost'
                size='sm'
                onClick={closePopover}
                className='w-6 h-6 p-0 hover:bg-muted'
              >
                <X className='w-3 h-3' />
              </Button>
            </div>

            {recommendations.length > 0 ? (
              <div className='space-y-1 overflow-y-auto max-h-64 custom-scrollbar'>
                {recommendations.map((item, index) => (
                  <Button
                    key={item.tag}
                    variant='ghost'
                    className='relative justify-start w-full h-auto p-3 py-2 text-left hover:bg-muted/50 group'
                    onClick={() => applyTag(item)}
                  >
                    <div className='space-y-1'>
                      {/* <div className='text-sm font-semibold text-foreground'>
                        {item.reference}
                      </div> */}
                      <div className='font-mono text-xs text-muted-foreground'>
                        {item.tag}
                      </div>
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger className='absolute z-50 invisible p-0 -translate-y-1/2 bg-white rounded-full size-6 hover:bg-muted right-2 group-hover:visible top-1/2'>
                            <LucideInfo className='text-indigo-500' />
                          </TooltipTrigger>
                          <TooltipContent>
                            <div className='space-y-1'>
                              <div className='text-sm font-semibold text-foreground'>
                                {item.reference}
                              </div>
                              <div className='font-mono text-xs text-muted-foreground'>
                                {item.tag}
                              </div>
                              <div className='text-xs text-muted-foreground'>
                                {item.datatype}
                              </div>
                            </div>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    </div>
                  </Button>
                ))}
              </div>
            ) : (
              <div className='py-6 text-center text-muted-foreground'>
                <Lightbulb className='w-8 h-8 mx-auto mb-2 opacity-50' />
                <p className='text-sm font-medium'>No suggestions found</p>
                <p className='text-xs'>Try selecting different text</p>
              </div>
            )}
          </div>
        </PopoverContent>
      </Popover>
    </div>
  );
}
