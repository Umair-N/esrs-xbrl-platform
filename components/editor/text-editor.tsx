'use client';

import type { ReportDocument, ReportBlock, XbrlTag } from '@/types/report';
import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import {
  X,
  Lightbulb,
  LucideInfo,
  Bot,
  Loader2,
  CheckCircle2,
} from 'lucide-react';
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
import { usePredictEntities, NEREntity } from '@/features/agent';
import { useTaxonomyStore } from '@/store/taxonomoy-store';
import { useTaggingStore } from '@/store/tagging-store';
import { sampleContexts } from '@/lib/sample-data';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '../ui/tooltip';
import { showError, showSuccess } from '../heads-up';

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

  const selectedTaxonomy = useTaxonomyStore((state) => state.selectedTaxonomy);

  // Bring in the tagging store actions. When a recommendation is chosen, we
  // place the corresponding concept into the global store via setPendingConcept.
  // The tagging panel reads this and preselects the concept for context
  // assignment. We also expose the currently selected context ID should we
  // choose to automatically create tags when a context is already selected.
  const {
    setPendingConcept,
    setPendingHighlight,
    selectedContextId,
    agentMode,
    recommenderEnabled,
  } = useTaggingStore();

  // const [recommendations, setRecommendations] = useState<any[]>([]);
  const [showPopover, setShowPopover] = useState(false);
  const [highlightedText, setHighlightedText] = useState('');
  const [popoverTriggerElement, setPopoverTriggerElement] =
    useState<HTMLElement | null>(null);

  // Track the highlighted range (blockId, startIndex, endIndex)
  const [highlightRange, setHighlightRange] = useState<{
    blockId: string;
    startIndex: number;
    endIndex: number;
  } | null>(null);

  const { mutate, data: recommendations } = useRecommendations({
    mutationConfig: {},
  });
  // Hook for submitting feedback to the AI recommender. When a user selects
  // a suggestion, we will use this to notify the service about the choice.
  const { mutate: sendFeedback } = usePostFeedback();

  // NER Agent hook for automatic entity detection
  const { mutate: predictEntities, isPending: isAgentLoading } =
    usePredictEntities({
      mutationConfig: {},
    });

  // State for agent mode - detected entities displayed inline with highlights
  const [agentEntities, setAgentEntities] = useState<NEREntity[]>([]);
  // Track which block the agent entities belong to and their absolute positions
  const [agentHighlightBlock, setAgentHighlightBlock] = useState<{
    blockId: string;
    selectionStart: number; // Start position of the selected text in the block
  } | null>(null);

  // Store entity-to-recommendations mapping for agent mode (lazy loaded on hover)
  // Key: entity key (start-end), Value: array of recommendations or null if failed
  const [entityRecommendations, setEntityRecommendations] = useState<
    Map<
      string,
      | {
          tag: string;
          reference: string;
          datatype: string;
          score: number;
        }[]
      | null
    >
  >(new Map());

  // Track which entities are currently loading recommendations (by key)
  const [loadingEntityKeys, setLoadingEntityKeys] = useState<Set<string>>(
    new Set()
  );

  // Track if we're showing expanded recommendations for an entity (by key)
  const [expandedEntityKey, setExpandedEntityKey] = useState<string | null>(
    null
  );

  // Helper to generate a unique key for an entity
  const getEntityKey = (entity: NEREntity) => `${entity.start}-${entity.end}`;

  /**
   * Clear agent mode highlights and state
   */
  const clearAgentHighlights = () => {
    setAgentEntities([]);
    setAgentHighlightBlock(null);
    setEntityRecommendations(new Map());
    setLoadingEntityKeys(new Set());
    setExpandedEntityKey(null);
  };

  // Clear agent highlights when agent mode is disabled
  useEffect(() => {
    if (!agentMode.enabled) {
      clearAgentHighlights();
    }
  }, [agentMode.enabled]);

  const selectionRef = useRef(false);

  const handleBlockClick = (blockId: string) => {
    if (selectionRef.current) {
      selectionRef.current = false;
      return;
    }
    onBlockSelect(blockId);
  };

  /**
   * Handles highlighting text in a block.  Invokes the recommendations API
   * with the selected text and positions a popover next to the selection.
   * When agent mode is enabled, it uses the NER agent for automatic tagging.
   */
  const handleTextSelection = (blockId: string, e: React.MouseEvent) => {
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
          // Mark that a selection has occurred to prevent handleBlockClick from clearing it
          selectionRef.current = true;

          // Ensure the block is selected
          onBlockSelect(blockId);

          // Calculate start index relative to the block content
          let startIndex = 0;
          const blockElement = e.currentTarget;
          const contentContainer = blockElement.querySelector(
            '.whitespace-pre-wrap'
          );

          if (contentContainer) {
            const preSelectionRange = range.cloneRange();
            preSelectionRange.selectNodeContents(contentContainer);
            preSelectionRange.setEnd(range.startContainer, range.startOffset);
            startIndex = preSelectionRange.toString().length;
          } else {
            // Fallback to indexOf if container not found (shouldn't happen)
            const blockContent =
              report.blocks.find((b) => b.id === blockId)?.content || '';
            startIndex = blockContent.indexOf(selectedText);
          }

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

          // Agent Mode: Use NER for entity detection (recommendations loaded on hover)
          if (agentMode.enabled) {
            if (!selectedTaxonomy?.name) {
              return showError({
                title: 'Please select a taxonomy',
                message: 'A taxonomy is required for AI Agent tagging.',
              });
            }

            // Clear previous agent state
            setAgentEntities([]);
            setEntityRecommendations(new Map());
            setLoadingEntityKeys(new Set());
            setExpandedEntityKey(null);

            // Show loading notification
            showSuccess({
              title: 'Detecting entities...',
              message: 'AI Agent is analyzing the selected text.',
              duration: 2000,
            });

            predictEntities(
              { data: { text: selectedText } },
              {
                onSuccess: async (res) => {
                  const entities = res?.entities ?? [];
                  setAgentEntities(entities);
                  // Store the block and selection start for inline highlighting
                  setAgentHighlightBlock({
                    blockId,
                    selectionStart: startIndex,
                  });

                  if (entities.length === 0) {
                    showError({
                      title: 'No entities detected',
                      message:
                        'AI Agent could not detect any entities in the selected text.',
                    });
                    return;
                  }

                  showSuccess({
                    title: `${entities.length} entit${entities.length > 1 ? 'ies' : 'y'} detected`,
                    message:
                      'Hover over highlighted text to see XBRL tag suggestions.',
                    duration: 3000,
                  });
                },
                onError: () => {
                  setAgentEntities([]);
                  setAgentHighlightBlock(null);
                  showError({
                    title: 'Detection failed',
                    message:
                      'AI Agent failed to detect entities. Please try again.',
                  });
                },
              }
            );
            return;
          }

          // Standard recommendation mode
          if (!selectedTaxonomy?.name) {
            return showError({
              title: 'Please select a taxonomy',
              message: '',
            });
          }

          // Query recommendations only if enabled
          if (recommenderEnabled && selectedTaxonomy?.name) {
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
                  // setRecommendations(res?.results ?? []);
                  setShowPopover(true);
                },
                onError: () => {
                  // setRecommendations([]);
                  setShowPopover(true);
                },
              }
            );
          }
        }
      }
    }
  };

  /**
   * Fetch XBRL tag recommendations for a specific entity (called on hover)
   */
  const fetchEntityRecommendations = (entity: NEREntity) => {
    const entityKey = getEntityKey(entity);

    // Skip if already loaded or loading
    if (
      entityRecommendations.has(entityKey) ||
      loadingEntityKeys.has(entityKey)
    ) {
      return;
    }

    // Mark as loading
    setLoadingEntityKeys((prev) => new Set(prev).add(entityKey));

    mutate(
      {
        data: {
          query: entity.text,
          taxonomy: selectedTaxonomy?.name?.toLocaleLowerCase() || '',
          k: 5, // Get top 5 recommendations
          rerank: true,
        },
      },
      {
        onSuccess: (recRes: any) => {
          const recs = recRes?.results ?? [];
          setEntityRecommendations((prev) => {
            const newMap = new Map(prev);
            newMap.set(entityKey, recs.length > 0 ? recs : null);
            return newMap;
          });
          setLoadingEntityKeys((prev) => {
            const newSet = new Set(prev);
            newSet.delete(entityKey);
            return newSet;
          });
        },
        onError: () => {
          setEntityRecommendations((prev) => {
            const newMap = new Map(prev);
            newMap.set(entityKey, null);
            return newMap;
          });
          setLoadingEntityKeys((prev) => {
            const newSet = new Set(prev);
            newSet.delete(entityKey);
            return newSet;
          });
        },
      }
    );
  };

  /**
   * Select a tag from agent mode recommendations - sets it as pending in the
   * tagging panel rather than directly applying it. The user must click
   * "Add Tag" in the tagging panel to actually apply the tag.
   */
  const selectAgentTag = (
    entity: NEREntity,
    recommendation: { tag: string; reference: string; datatype: string }
  ) => {
    if (!agentHighlightBlock) return;

    const { blockId, selectionStart } = agentHighlightBlock;
    const entityStart = selectionStart + entity.start;
    const entityEnd = selectionStart + entity.end;
    const entityKey = getEntityKey(entity);

    // Set the pending concept in the tagging store - the tagging panel will
    // pick this up and preselect it for context assignment
    setPendingConcept({
      id: recommendation.tag,
      label: recommendation.reference,
      definition: `Detected as ${entity.label}: "${entity.text}"`,
      type: recommendation.datatype,
      periodType: 'duration',
    });

    // Set the pending highlight info so the tagging panel knows where to
    // place the tag and which block to add it to
    setPendingHighlight({
      text: entity.text,
      startIndex: entityStart,
      endIndex: entityEnd,
      blockId: blockId,
    });

    // Remove the entity from agent highlights since it's now selected
    const remainingEntities = agentEntities.filter(
      (e) => getEntityKey(e) !== entityKey
    );
    if (remainingEntities.length === 0) {
      clearAgentHighlights();
    } else {
      setAgentEntities(remainingEntities);
    }

    showSuccess({
      title: 'Tag selected',
      message: `"${entity.text}" ready for tagging. Click "Add Tag" in the panel to apply.`,
      duration: 3000,
    });
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
      dataType: item.datatype,
      periodType: 'duration' as const,
      abstract: false,
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
          createdAt: new Date().toISOString(),
          ...(context ? { context } : {}),
          ...(feedbackId !== undefined ? { feedbackId } : {}),
        };
        const updatedReport: ReportDocument = {
          ...report,
          blocks: report.blocks.map((blk) =>
            blk.id === blockId
              ? { ...blk, tags: [...(blk.tags || []), newTag] }
              : blk
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

  // Label color mapping for different entity types (used in agent highlights)
  const labelColors: Record<string, string> = {
    ENTITY: 'bg-blue-200 dark:bg-blue-800/50 border-blue-400',
    CONCEPT: 'bg-emerald-200 dark:bg-emerald-800/50 border-emerald-400',
    CHANGE: 'bg-amber-200 dark:bg-amber-800/50 border-amber-400',
    METRIC: 'bg-purple-200 dark:bg-purple-800/50 border-purple-400',
    VALUE: 'bg-rose-200 dark:bg-rose-800/50 border-rose-400',
    DATE: 'bg-cyan-200 dark:bg-cyan-800/50 border-cyan-400',
  };

  /**
   * Render a single agent entity with HoverCard for recommendations.
   */
  const renderAgentEntity = (entity: NEREntity, text: string) => {
    const entityKey = getEntityKey(entity);
    const recs = entityRecommendations.get(entityKey);
    const isLoading = loadingEntityKeys.has(entityKey);
    const hasLoaded = entityRecommendations.has(entityKey);
    const colorClass =
      labelColors[entity.label] ||
      'bg-violet-200 dark:bg-violet-800/50 border-violet-400';

    return (
      <HoverCard
        key={`entity-${entityKey}`}
        onOpenChange={(open) => {
          if (open) {
            fetchEntityRecommendations(entity);
          }
        }}
      >
        <HoverCardTrigger asChild>
          <span
            className={cn(
              'px-1 py-0.5 rounded cursor-pointer border-b-2 font-medium transition-all hover:opacity-80',
              colorClass,
              isLoading && 'animate-pulse'
            )}
          >
            {text}
          </span>
        </HoverCardTrigger>
        <HoverCardContent className='w-80 p-0' align='start'>
          <div className='p-3 space-y-3'>
            <div className='flex items-center justify-between gap-2'>
              <span className='font-semibold text-sm'>{entity.text}</span>
              <Badge
                variant='outline'
                className={cn(
                  'text-xs',
                  entity.label === 'ENTITY' && 'bg-blue-100 text-blue-700',
                  entity.label === 'CONCEPT' &&
                    'bg-emerald-100 text-emerald-700',
                  entity.label === 'CHANGE' && 'bg-amber-100 text-amber-700',
                  entity.label === 'METRIC' && 'bg-purple-100 text-purple-700',
                  entity.label === 'VALUE' && 'bg-rose-100 text-rose-700',
                  entity.label === 'DATE' && 'bg-cyan-100 text-cyan-700'
                )}
              >
                {entity.label}
              </Badge>
            </div>

            <Separator />

            <div className='space-y-2'>
              <div className='text-xs font-medium text-muted-foreground'>
                XBRL Tag Suggestions
              </div>

              {!hasLoaded && !isLoading ? (
                <div className='flex items-center gap-1 text-xs text-muted-foreground py-2'>
                  <Loader2 className='w-3 h-3 animate-spin' />
                  <span>Loading suggestions...</span>
                </div>
              ) : isLoading ? (
                <div className='flex items-center gap-1 text-xs text-muted-foreground py-2'>
                  <Loader2 className='w-3 h-3 animate-spin' />
                  <span>Finding XBRL tags...</span>
                </div>
              ) : recs && recs.length > 0 ? (
                <div className='space-y-1 max-h-48 overflow-y-auto'>
                  {(expandedEntityKey === entityKey
                    ? recs
                    : recs.slice(0, 3)
                  ).map((rec) => (
                    <Button
                      key={rec.tag}
                      variant='ghost'
                      size='sm'
                      className='w-full justify-start h-auto p-2 text-left hover:bg-muted/80'
                      onClick={(e) => {
                        e.stopPropagation();
                        selectAgentTag(entity, rec);
                      }}
                    >
                      <div className='flex-1 min-w-0'>
                        <div className='text-xs font-mono truncate text-primary'>
                          {rec.tag}
                        </div>
                        <div className='text-xs text-muted-foreground truncate'>
                          {rec.reference}
                        </div>
                      </div>
                      <CheckCircle2 className='w-4 h-4 ml-2 text-green-500 flex-shrink-0 opacity-0 group-hover:opacity-100' />
                    </Button>
                  ))}
                  {recs.length > 3 && expandedEntityKey !== entityKey && (
                    <Button
                      variant='ghost'
                      size='sm'
                      className='w-full text-xs text-muted-foreground'
                      onClick={(e) => {
                        e.stopPropagation();
                        setExpandedEntityKey(entityKey);
                      }}
                    >
                      Show {recs.length - 3} more suggestions...
                    </Button>
                  )}
                  {expandedEntityKey === entityKey && recs.length > 3 && (
                    <Button
                      variant='ghost'
                      size='sm'
                      className='w-full text-xs text-muted-foreground'
                      onClick={(e) => {
                        e.stopPropagation();
                        setExpandedEntityKey(null);
                      }}
                    >
                      Show less
                    </Button>
                  )}
                </div>
              ) : (
                <div className='flex items-center gap-1 text-xs text-amber-600 py-2'>
                  <X className='w-3 h-3' />
                  <span>No matching XBRL tags found</span>
                </div>
              )}
            </div>

            <Separator />

            <p className='text-xs text-muted-foreground'>
              Click a suggestion to apply it as a tag
            </p>
          </div>
        </HoverCardContent>
      </HoverCard>
    );
  };

  /**
   * Render a single existing XBRL tag with HoverCard showing tag details.
   */
  const renderExistingTag = (tag: XbrlTag, text: string) => {
    return (
      <HoverCard key={`tag-${tag.id}`}>
        <HoverCardTrigger asChild>
          <span className='bg-primary/20 px-1 py-0.5 rounded cursor-help border-b border-dashed border-primary font-medium'>
            {text}
          </span>
        </HoverCardTrigger>
        <HoverCardContent className='w-80'>
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
            {tag?.context && (
              <>
                <Separator />
                <div className='space-y-1 text-xs'>
                  <p className='font-semibold'>
                    Context: {tag?.context?.label}
                  </p>
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
              </>
            )}
          </div>
        </HoverCardContent>
      </HoverCard>
    );
  };

  const renderTaggedContent = (block: ReportBlock) => {
    const content = block.content;
    const tags = block.tags || [];
    const hasAgentHighlights =
      agentHighlightBlock?.blockId === block.id && agentEntities.length > 0;

    // If no tags and no agent highlights, render plain text
    if (tags.length === 0 && !hasAgentHighlights) {
      return (
        <p className='font-medium leading-relaxed whitespace-pre-wrap'>
          {content}
        </p>
      );
    }

    // Build a unified list of highlights (both tags and agent entities)
    // Each highlight has: start, end, type ('tag' | 'entity'), data
    type Highlight =
      | { type: 'tag'; start: number; end: number; data: XbrlTag }
      | { type: 'entity'; start: number; end: number; data: NEREntity };

    const highlights: Highlight[] = [];

    // Add existing tags
    tags.forEach((tag) => {
      highlights.push({
        type: 'tag',
        start: tag.startIndex || 0,
        end: tag.endIndex || content.length,
        data: tag,
      });
    });

    // Add agent entities (with absolute positions)
    if (hasAgentHighlights) {
      const selectionStart = agentHighlightBlock!.selectionStart;
      agentEntities.forEach((entity) => {
        highlights.push({
          type: 'entity',
          start: selectionStart + entity.start,
          end: selectionStart + entity.end,
          data: entity,
        });
      });
    }

    // Sort by start position
    highlights.sort((a, b) => a.start - b.start);

    // Render segments
    const segments: JSX.Element[] = [];
    let lastIndex = 0;

    highlights.forEach((highlight, index) => {
      // Skip if this highlight overlaps with a previous one (tags take priority)
      if (highlight.start < lastIndex) {
        return;
      }

      // Add gap text before this highlight
      if (highlight.start > lastIndex) {
        segments.push(
          <span key={`text-${index}`} className='font-medium leading-relaxed'>
            {content.substring(lastIndex, highlight.start)}
          </span>
        );
      }

      // Render the highlight
      const highlightText = content.substring(highlight.start, highlight.end);
      if (highlight.type === 'tag') {
        segments.push(renderExistingTag(highlight.data, highlightText));
      } else {
        segments.push(renderAgentEntity(highlight.data, highlightText));
      }

      lastIndex = highlight.end;
    });

    // Add remaining text after last highlight
    if (lastIndex < content.length) {
      segments.push(
        <span key='text-last' className='font-medium leading-relaxed'>
          {content.substring(lastIndex)}
        </span>
      );
    }

    return <div className='whitespace-pre-wrap'>{segments}</div>;
  };

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
              'p-4 rounded-lg border transition-colors h-full min-h-fit',
              selectedBlockId === block.id
                ? 'border-primary bg-primary/5'
                : 'border-border hover:border-primary/50'
            )}
            onClick={() => handleBlockClick(block.id)}
            onMouseUp={(e) => handleTextSelection(block.id, e)}
          >
            <div className='relative group max-h-[calc(100dvh-12rem)] overflow-y-auto custom-scrollbar'>
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

            {recommendations && recommendations.results?.length > 0 ? (
              <div className='space-y-1 overflow-y-auto max-h-64 custom-scrollbar'>
                {recommendations?.results?.map((item, index) => (
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
                          <TooltipTrigger
                            asChild
                            className='absolute z-50 invisible p-0 -translate-y-1/2 bg-white rounded-full size-6 hover:bg-muted right-2 group-hover:visible top-1/2'
                          >
                            <div className='absolute z-50 invisible p-0 -translate-y-1/2 bg-white rounded-full size-6 hover:bg-muted right-2 group-hover:visible top-1/2'>
                              <LucideInfo className='text-indigo-500' />
                            </div>
                          </TooltipTrigger>
                          <TooltipContent className='space-y-1 max-w-[100ch]'>
                            <div className='text-sm font-semibold text-foreground'>
                              {item.reference}
                            </div>
                            <div className='font-mono text-xs text-muted-foreground'>
                              {item.tag}
                            </div>
                            <div className='text-xs text-muted-foreground'>
                              {item.datatype}
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

      {/* Agent mode floating info bar - shows when entities are detected */}
      {agentHighlightBlock && agentEntities.length > 0 && (
        <div className='fixed bottom-4 left-1/2 -translate-x-1/2 z-50'>
          <div className='bg-white dark:bg-slate-800 rounded-lg shadow-lg border px-4 py-3 flex items-center gap-4'>
            <div className='flex items-center gap-2'>
              <div className='p-1.5 bg-gradient-to-r from-violet-500 to-purple-500 rounded-md'>
                <Bot className='w-3 h-3 text-white' />
              </div>
              <span className='text-sm font-medium'>
                {agentEntities.length} entit
                {agentEntities.length > 1 ? 'ies' : 'y'} detected
              </span>
              {isAgentLoading && (
                <Loader2 className='w-4 h-4 animate-spin text-violet-500' />
              )}
            </div>
            <Button variant='outline' size='sm' onClick={clearAgentHighlights}>
              <X className='w-4 h-4 mr-1' />
              Clear Labels
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
