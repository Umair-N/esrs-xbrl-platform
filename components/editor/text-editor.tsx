'use client';

import type { ReportDocument, ReportBlock } from '@/types/report';
import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { Textarea } from '@/components/ui/textarea';
import { Edit2, Check, X } from 'lucide-react';
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card';
import { Separator } from '@/components/ui/separator';
import type { JSX } from 'react/jsx-runtime';
import { UseRecommendations } from '@/features/recommender/api/get-recommendations';

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
  const [editingBlockId, setEditingBlockId] = useState<string | null>(null);
  const [editedContent, setEditedContent] = useState('');
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  // State for recommendations popover
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [popoverPos, setPopoverPos] = useState<{
    top: number;
    left: number;
  } | null>(null);
  const [showPopover, setShowPopover] = useState(false);
  const [highlightedText, setHighlightedText] = useState('');

  // Track the highlighted range (blockId, startIndex, endIndex)
  const [highlightRange, setHighlightRange] = useState<{
    blockId: string;
    startIndex: number;
    endIndex: number;
  } | null>(null);

  const { mutate } = UseRecommendations();

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

          // Position the popover
          const rect = range.getBoundingClientRect();
          setPopoverPos({
            top: rect.bottom + window.scrollY,
            left: rect.left + window.scrollX,
          });
          setHighlightedText(selectedText);

          // Query recommendations
          mutate(
            {
              data: {
                query: selectedText,
                taxonomy: 'brsr',
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
  }) => {
    if (!highlightRange) return;
    const { blockId, startIndex, endIndex } = highlightRange;

    // Create a minimal concept from the recommendation.  If you have a taxonomy
    // lookup available, enrich this object accordingly.
    const concept = {
      id: item.tag,
      label: item.reference,
      definition: '', // fill with taxonomy definition if available
      type: item.datatype,
      periodType: '', // fill if known
    };

    const newTag = {
      id: `${Date.now()}`, // simple unique id; replace with uuid if you have one
      concept,
      startIndex,
      endIndex,
      context: {}, // add context if needed; can reuse context from another tag/block
    };

    // Update the report’s blocks with the new tag
    const updatedReport: ReportDocument = {
      ...report,
      blocks: report.blocks.map((blk) =>
        blk.id === blockId ? { ...blk, tags: [...blk.tags, newTag] } : blk
      ),
      updatedAt: new Date().toISOString(),
    };

    onReportChange(updatedReport);
    setShowPopover(false);
    setHighlightRange(null);
  };

  const renderTaggedContent = (block: ReportBlock) => {
    if (!block.tags || block.tags.length === 0) {
      return <p className='whitespace-pre-wrap'>{block.content}</p>;
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
          <span key={`text-${index}`}>
            {block.content.substring(lastIndex, startIndex)}
          </span>
        );
      }

      segments.push(
        <HoverCard key={`tag-${tag.id}`}>
          <HoverCardTrigger asChild>
            <span className='bg-primary/20 px-0.5 rounded cursor-help border-b border-dashed border-primary'>
              {block.content.substring(startIndex, endIndex)}
            </span>
          </HoverCardTrigger>
          <HoverCardContent className='w-80'>
            <div className='space-y-2'>
              <h4 className='font-medium'>{tag.concept.label}</h4>
              <p className='text-sm text-muted-foreground'>
                {tag.concept.definition}
              </p>
              <div className='flex flex-wrap gap-2 pt-1'>
                <Badge variant='outline'>{tag.concept.type}</Badge>
                <Badge variant='outline'>{tag.concept.periodType}</Badge>
              </div>
              <Separator />
              <div className='text-xs'>
                <p className='font-medium'>Context: {tag?.context?.label}</p>
                <p className='text-muted-foreground mt-1'>
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
        <span key='text-last'>{block.content.substring(lastIndex)}</span>
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
      <div className='flex-1 space-y-4 p-1'>
        {report.blocks.map((block) => (
          <div
            key={block.id}
            data-block-id={block.id}
            className={cn(
              'p-3 rounded-md border transition-colors h-full',
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
              <div className='flex flex-col space-y-2 w-full h-full'>
                <Textarea
                  ref={textAreaRef}
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                  className='w-full resize-none pr-0 text max-h-[calc(100dvh-9rem)] overflow-y-auto custom-scrollbar h-full'
                  autoFocus
                />
                <div className='flex justify-end space-x-2'>
                  <Button size='sm' variant='outline' onClick={cancelEditing}>
                    <X className='h-4 w-4 mr-1' /> Cancel
                  </Button>
                  <Button size='sm' onClick={saveEditing}>
                    <Check className='h-4 w-4 mr-1' /> Save
                  </Button>
                </div>
              </div>
            ) : (
              <div className='relative group max-h-[calc(100dvh-12rem)] overflow-y-auto custom-scrollbar'>
                <div className='sticky border rounded-full top-0 right-0 float-right group-hover:opacity-100 transition-opacity z-10 ml-2 mb-2'>
                  <Button
                    size='sm'
                    variant='ghost'
                    onClick={(e) => {
                      e.stopPropagation();
                      startEditing(block);
                    }}
                    className='rounded-full shadow-md'
                  >
                    Edit
                    <Edit2 className='h-4 w-4' />
                  </Button>
                </div>
                <div className='prose dark:prose-invert max-w-none leading-relaxed'>
                  {renderTaggedContent(block)}
                </div>
                {block.tags && block.tags.length > 0 && (
                  <div className='mt-2 flex flex-wrap gap-2 clear-both'>
                    {block.tags.map((tag) => (
                      <Badge
                        key={tag.id}
                        variant='outline'
                        className='inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary'
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

      {/* Popover with recommendations and apply buttons */}
      {showPopover && popoverPos && (
        <div
          style={{
            position: 'absolute',
            top: popoverPos.top,
            left: popoverPos.left,
            zIndex: 50,
            maxWidth: '20rem',
            backgroundColor: '#fff',
            border: '1px solid #ccc',
            borderRadius: '4px',
            padding: '0.75rem',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
          }}
        >
          <div className='flex justify-between items-center mb-2'>
            <span className='font-medium'>
              Suggestions for “{highlightedText}”
            </span>
            <button
              onClick={() => setShowPopover(false)}
              className='ml-2 text-sm'
            >
              ×
            </button>
          </div>
          <ul className='space-y-1'>
            {recommendations.map((item) => (
              <li key={item.tag}>
                <button
                  className='w-full text-left hover:bg-gray-100 rounded p-1'
                  onClick={() => applyTag(item)}
                >
                  <strong>{item.reference}</strong>
                  <div className='text-xs text-muted-foreground'>
                    {item.tag}
                  </div>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
