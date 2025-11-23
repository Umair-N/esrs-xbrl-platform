'use client';

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import {
  Search,
  Tag,
  Plus,
  AlertCircle,
  ChevronRight,
  ChevronDown,
  Folder,
  FolderOpen,
  FileText,
  Calculator,
  Target,
  Presentation,
  Layers,
  FormInput as Formula,
  BarChart3,
  Info,
  Loader2,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Skeleton } from '@/components/ui/skeleton';

import type { ReportDocument, XbrlContext, XbrlTag } from '@/types/report';
import type { TaxonomyData, TaxonomyNode } from '@/types/taxonomy';

import { sampleContexts } from '@/lib/sample-data';
import { generateUniqueId } from '@/lib/utils';
import { flattenTree } from '@/lib/taxomony-data';
import { useTaxonomyData } from '@/features/tagging/api';
import useDebounceSearch from '@/hooks/use-search';
import { useMyTaxonomies } from '@/features/taxonomy/api/get-user-taxonomies';
import { useSwitchTaxonomy } from '@/features/taxonomy/api/switch-taxonomies';
import { useTaxonomyStore } from '@/store/taxonomoy-store';
import { useTaggingStore } from '@/store/tagging-store';
import { ContextOut, useContexts } from '@/features/contexts/api/list-contexts';
import { CreateContextModal } from './create-context-modal';

/* -------------------------------- Types -------------------------------- */

interface TaggingPanelProps {
  report: ReportDocument;
  selectedBlockId: string | null;
  highlightedText: {
    text: string;
    startIndex: number;
    endIndex: number;
  } | null;
  onReportChange: (report: ReportDocument) => void;
}

type TabKey = 'presentations' | 'dimensions' | 'formulae' | 'calculations';

/* ----------------------------- UI Helpers ------------------------------- */

const LoadingBlock = ({ lines = 3 }: { lines?: number }) => (
  <div className='space-y-2'>
    {Array.from({ length: lines }).map((_, i) => (
      <Skeleton key={i} className='w-full h-4' />
    ))}
  </div>
);

const TreeRowSkeleton = () => (
  <div className='flex items-center gap-2 py-1.5 px-2'>
    <Skeleton className='w-4 h-4 rounded' />
    <Skeleton className='w-4 h-4 rounded' />
    <Skeleton className='h-4 w-28' />
    <Skeleton className='w-40 h-4' />
  </div>
);

const SearchInput = ({
  value,
  onChange,
  placeholder,
  disabled,
}: {
  value: string;
  onChange: (v: string) => void;
  placeholder: string;
  disabled?: boolean;
}) => (
  <div className='relative'>
    <Search className='absolute left-3 top-2.5 h-4 w-4 text-muted-foreground' />
    <Input
      placeholder={placeholder}
      className='pl-10 outline-none h-9'
      value={value}
      onChange={(e) => onChange(e.target.value)}
      disabled={disabled}
    />
  </div>
);

/* ------------------------- Taxonomy Tree (reused) ------------------------ */

const TaxonomyTreeNode = ({
  node,
  level = 0,
  onSelect,
  selectedId,
  searchQuery,
}: {
  node: TaxonomyNode;
  level?: number;
  onSelect: (node: TaxonomyNode) => void;
  selectedId?: string | null;
  searchQuery: string;
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const hasChildren = !!node.children?.length;
  const hasCalculations = !!node.calculations?.length;
  const isSelected = Boolean(selectedId && node.id) && selectedId === node.id;

  const matchesSearch =
    !searchQuery ||
    node.label?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    node.id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (node.name && node.name.toLowerCase().includes(searchQuery.toLowerCase()));

  const getIcon = () =>
    hasChildren ? (
      isExpanded ? (
        <FolderOpen className='w-3 h-3' />
      ) : (
        <Folder className='w-3 h-3' />
      )
    ) : (
      <FileText className='w-3 h-3' />
    );

  const getBadgeColor = (labelType?: string) => {
    switch (labelType) {
      case 'abstract':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      case 'table':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'axis':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300';
      case 'member':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300';
      case 'text block':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  if (!matchesSearch && !hasChildren) return null;

  return (
    <div className='select-none'>
      <div
        className={`group relative flex items-start py-1.5 px-2 rounded-lg cursor-pointer transition-all duration-200 border-2 ${
          isSelected
            ? 'bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-950/30 dark:to-green-950/30 border-emerald-300 dark:border-emerald-700 shadow-md ring-2 ring-emerald-200 dark:ring-emerald-800'
            : 'border-transparent hover:border-muted-foreground/20 hover:bg-muted/50 hover:shadow-sm bg-transparent'
        }`}
        style={{ paddingLeft: `${level * 12 + 8}px` }}
        onClick={() => onSelect(node)}
      >
        {isSelected && (
          <div className='absolute top-0 bottom-0 left-0 w-1 rounded-l-lg bg-gradient-to-b from-emerald-500 to-green-500' />
        )}

        {hasChildren ? (
          <Button
            variant='ghost'
            size='sm'
            className={`h-4 w-4 p-0 mr-2 flex-shrink-0 mt-0.5 transition-colors ${isSelected ? 'hover:bg-emerald-200 dark:hover:bg-emerald-800' : 'hover:bg-muted'}`}
            onClick={(e) => {
              e.stopPropagation();
              setIsExpanded((s) => !s);
            }}
            aria-label={isExpanded ? 'Collapse node' : 'Expand node'}
          >
            {isExpanded ? (
              <ChevronDown className='w-2 h-2' />
            ) : (
              <ChevronRight className='w-2 h-2' />
            )}
          </Button>
        ) : (
          <div className='w-4 h-4 mr-2' />
        )}

        <div className='flex items-start flex-1 min-w-0 gap-2'>
          <div
            className={`p-1 rounded ${isSelected ? 'bg-emerald-100 dark:bg-emerald-900/50' : 'bg-muted/50 group-hover:bg-muted'}`}
          >
            <span
              className={`${isSelected ? 'text-emerald-600 dark:text-emerald-400' : 'text-muted-foreground group-hover:text-foreground'}`}
            >
              {getIcon()}
            </span>
          </div>

          <div className='flex-1 min-w-0'>
            <div className='flex items-start justify-between gap-2 mb-1'>
              <span
                className={`font-medium text-xs break-words leading-tight ${isSelected ? 'text-emerald-900 dark:text-emerald-100' : 'text-foreground'}`}
                title={node.label ?? ''}
              >
                {node.label}
              </span>

              <div className='flex items-center flex-shrink-0 gap-1'>
                {hasCalculations && (
                  <div
                    className={`p-0.5 rounded ${isSelected ? 'bg-blue-100 dark:bg-blue-900/50' : 'bg-blue-50 dark:bg-blue-950/30'}`}
                  >
                    <Calculator className='w-2 h-2 text-blue-500' />
                  </div>
                )}
                {isSelected && (
                  <div className='w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse' />
                )}
              </div>
            </div>

            <div className='flex flex-wrap items-start min-w-0 gap-1 mt-1'>
              <code
                className={`text-xs font-mono px-1.5 py-0.5 rounded break-all leading-tight ${
                  isSelected
                    ? 'bg-emerald-100 dark:bg-emerald-900/50 text-emerald-800 dark:text-emerald-300'
                    : 'bg-muted text-muted-foreground'
                }`}
                title={node.id ?? ''}
              >
                {node.id}
              </code>

              {node.labelType && (
                <Badge
                  variant={isSelected ? 'default' : 'outline'}
                  className={`text-xs h-4 px-1 flex-shrink-0 ${isSelected ? 'bg-emerald-600 text-white dark:bg-emerald-500' : `${getBadgeColor(node.labelType)}`}`}
                >
                  {node.labelType}
                </Badge>
              )}
            </div>
          </div>
        </div>
      </div>

      {hasChildren && isExpanded && (
        <div>
          {node.children!.map((child, i) => (
            <TaxonomyTreeNode
              key={`${child.id}-${i}`}
              node={child}
              level={level + 1}
              onSelect={onSelect}
              selectedId={selectedId ?? null}
              searchQuery={searchQuery}
            />
          ))}
        </div>
      )}
    </div>
  );
};

/* --------------------------- Browser (reusable) --------------------------- */

const TaxonomyBrowser = ({
  activeTab,
  taxonomyData,
  isInitialLoading,
  isUpdating,
  searchQuery,
  setSearchQuery,
  selectedConcept,
  setSelectedConcept,
}: {
  activeTab: TabKey;
  taxonomyData: TaxonomyData | null;
  isInitialLoading: boolean;
  isUpdating: boolean;
  searchQuery: string;
  setSearchQuery: (v: string) => void;
  selectedConcept: TaxonomyNode | null;
  setSelectedConcept: (n: TaxonomyNode) => void;
}) => {
  const allNodes = useMemo(
    () => (taxonomyData?.children ? flattenTree(taxonomyData.children) : []),
    [taxonomyData]
  );

  const isSearching = searchQuery.trim().length > 0;

  const label = useMemo(() => {
    switch (activeTab) {
      case 'presentations':
        return 'Presentations';
      case 'dimensions':
        return 'Dimensions';
      case 'formulae':
        return 'Formulae';
      case 'calculations':
        return 'Calculations';
      default:
        return 'Taxonomy';
    }
  }, [activeTab]);

  const showSkeleton = isInitialLoading;
  const showUpdatingChip = isUpdating;

  return (
    <Card
      className='p-0 mt-1 border-0 shadow-sm'
      aria-busy={showSkeleton || showUpdatingChip}
    >
      <CardHeader className='p-0'>
        <CardTitle className='flex items-center gap-2 p-2 text-base'>
          <Tag className='w-4 h-4 text-emerald-600' />
          {label}
          {showUpdatingChip && (
            <span className='inline-flex items-center gap-1 ml-2 text-xs text-muted-foreground'>
              <Loader2 className='w-3 h-3 animate-spin' /> updating…
            </span>
          )}
        </CardTitle>
      </CardHeader>

      <CardContent className='p-0 space-y-4'>
        <div className='p-2 mt-1 space-y-3'>
          {/* Search */}
          {/* {showSkeleton ? (
            <Skeleton className='w-full h-9' />
          ) : (
            <SearchInput
              value={searchQuery}
              onChange={setSearchQuery}
              placeholder={`Search ${label}`}
              disabled={showSkeleton}
            />
          )} */}

          <Card className='border-2'>
            <CardHeader className='py-2 bg-muted/30'>
              <div className='flex items-center justify-between'>
                <h4 className='text-sm font-medium'>
                  {showSkeleton
                    ? `Loading ${label.toLowerCase()}…`
                    : isSearching
                      ? `${allNodes.length} search results`
                      : `${taxonomyData?.label || 'ESRS Taxonomy'}${allNodes.length ? ` - ${allNodes.length} concepts` : ''}`}
                </h4>
                <Badge variant='secondary' className='text-xs'>
                  {showSkeleton ? 'Loading' : isSearching ? 'Search' : 'Browse'}
                </Badge>
              </div>
            </CardHeader>

            <CardContent className='px-0'>
              <ScrollArea className='h-[250px]'>
                <div className='p-2'>
                  {showSkeleton ? (
                    <div className='space-y-1'>
                      {Array.from({ length: 10 }).map((_, i) => (
                        <TreeRowSkeleton key={i} />
                      ))}
                    </div>
                  ) : isSearching ? (
                    allNodes.length === 0 ? (
                      <div className='py-6 text-center text-muted-foreground'>
                        <Search className='w-8 h-8 mx-auto mb-3 opacity-50' />
                        <p className='text-sm'>
                          No results found for “{searchQuery}”.
                        </p>
                      </div>
                    ) : (
                      <div className='space-y-1'>
                        {allNodes.map((concept, index) => {
                          const isSelected =
                            Boolean(selectedConcept?.id && concept.id) &&
                            selectedConcept?.id === concept.id;
                          return (
                            <div
                              key={`${concept.id}-${index}`}
                              className={`group relative p-2.5 cursor-pointer rounded-lg transition-all duration-200 border-2 ${
                                isSelected
                                  ? 'bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-950/30 dark:to-green-950/30 border-emerald-300 dark:border-emerald-700 shadow-md ring-2 ring-emerald-200 dark:ring-emerald-800'
                                  : 'border-transparent hover:border-emerald-200 dark:hover:border-emerald-800 hover:bg-emerald-50/50 dark:hover:bg-emerald-950/10 hover:shadow-sm'
                              }`}
                              onClick={() => setSelectedConcept(concept)}
                            >
                              {isSelected && (
                                <div className='absolute top-0 bottom-0 left-0 w-1 rounded-l-lg bg-gradient-to-b from-emerald-500 to-green-500' />
                              )}
                              <div className='flex items-start gap-2.5'>
                                <div
                                  className={`p-1.5 rounded-md ${isSelected ? 'bg-emerald-100 dark:bg-emerald-900/50' : 'bg-muted/50 group-hover:bg-emerald-100/50 dark:group-hover:bg-emerald-900/30'}`}
                                >
                                  <FileText
                                    className={`h-4 w-4 ${isSelected ? 'text-emerald-600 dark:text-emerald-400' : 'text-muted-foreground group-hover:text-emerald-600 dark:group-hover:text-emerald-400'}`}
                                  />
                                </div>
                                <div className='flex-1 min-w-0'>
                                  <h4
                                    className={`font-semibold text-sm ${isSelected ? 'text-emerald-900 dark:text-emerald-100' : 'text-foreground group-hover:text-emerald-800 dark:group-hover:text-emerald-200'}`}
                                  >
                                    {concept.label}
                                  </h4>
                                  <code className='block px-2 py-1 mt-1 font-mono text-xs rounded'>
                                    {concept.id}
                                  </code>
                                </div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )
                  ) : (
                    <div className='space-y-1'>
                      {/* Browse mode: show tree when hierarchical; otherwise list all nodes top-level */}
                      {taxonomyData?.children?.length ? (
                        taxonomyData.children.map((child, index) => (
                          <TaxonomyTreeNode
                            key={`${child.id}-${index}`}
                            node={child}
                            onSelect={setSelectedConcept}
                            selectedId={selectedConcept?.id ?? null}
                            searchQuery=''
                          />
                        ))
                      ) : (
                        <div className='py-6 text-center text-muted-foreground'>
                          <Info className='w-8 h-8 mx-auto mb-3 opacity-50' />
                          <p className='text-sm'>No items available.</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>
      </CardContent>
    </Card>
  );
};

/* -------------------------------- Component -------------------------------- */

const TAB_META: Record<
  TabKey,
  { label: string; icon: React.ComponentType<{ className?: string }> }
> = {
  presentations: { label: 'Presentations', icon: Presentation },
  dimensions: { label: 'Dimensions', icon: Layers },
  formulae: { label: 'Formulae', icon: Formula },
  calculations: { label: 'Calculations', icon: BarChart3 },
};

const TaggingPanel: React.FC<TaggingPanelProps> = ({
  report,
  selectedBlockId,
  highlightedText,
  onReportChange,
}) => {
  const [activeTab, setActiveTab] = useState<TabKey>('presentations');
  const [searchQuery, setSearchQuery] = useState('');
  const debouncedSearchQuery = useDebounceSearch(searchQuery, 500);
  const [selectedConcept, setSelectedConcept] = useState<TaxonomyNode | null>(
    null
  );
  // Pull state and actions from the global tagging store. The store keeps
  // track of a pending concept (selected via the recommendation popover) and
  // the globally selected context ID. When the tagging panel is mounted or
  // the store values change, we synchronise our local state with the store.
  const {
    pendingConcept,
    setPendingConcept,
    selectedContextId: globalContextId,
    setSelectedContextId: setGlobalContextId,
  } = useTaggingStore();
  const { data: contexts } = useContexts({});

  // Local context selection. Initialise with the global context if one has
  // been chosen previously. This value will be mirrored back to the
  // tagging store whenever it changes.
  const [selectedContextId, setSelectedContextId] = useState<string | null>(
    globalContextId
  );
  const [value, setValue] = useState<string>('');

  // Load taxonomy for current tab
  // const { data, isLoading, isFetching, isError, error } = useQuery({
  //   queryKey: ['taxonomy', activeTab],
  //   queryFn: async () => api.get(`/taxonomy/${activeTab}`),
  //   staleTime: 60_000,
  //   refetchOnWindowFocus: false,
  // });

  const { data, isLoading, isFetching, isError, error } = useTaxonomyData({
    entity: activeTab,
    search_query: debouncedSearchQuery,
  });

  // Normalize incoming taxonomy structure
  const taxonomyData: TaxonomyData | null = useMemo(() => {
    const rawData = data;
    if (!rawData) return null;
    if (rawData?.children) return rawData as TaxonomyData;
    if (Array.isArray(rawData))
      return { children: rawData, label: 'Taxonomy', id: 'root' };
    if (rawData?.data?.children) return rawData?.data as TaxonomyData;
    return { children: [rawData], label: 'Taxonomy', id: 'root' };
  }, [data]);

  // Reset concept selection and search query when switching block or tab. Do
  // not reset the context globally; instead initialise the local context with
  // the current global context so the user's last selected context remains
  // available for subsequent tags created via recommendations. This effect
  // should not run when only the context changes, otherwise it clears the
  // selected concept and disables the Add Tag button.
  useEffect(() => {
    setSelectedConcept(null);
    // Restore the local context from the global store (if any)
    setSelectedContextId(globalContextId ?? null);
    setSearchQuery('');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedBlockId, activeTab]);

  // When a concept is selected from the recommendation popover, it is stored
  // in the global tagging store as a pending concept. Detect this change and
  // preselect the concept in the tagging panel, then clear the pending
  // concept so it is not reused. The minimal fields required by the
  // taxonomy browser are mapped from the recommendation object.
  useEffect(() => {
    if (pendingConcept) {
      setSelectedConcept({
        id: pendingConcept.id,
        label: pendingConcept.label,
        type: pendingConcept.type,
        periodType: pendingConcept.periodType as any,
        // Use definition as the original label/definition. This ensures the
        // definition appears in the hover card.
        originalLabel: pendingConcept.definition,
        // Propagate the feedback ID from the pending concept so it can be
        // attached to the tag when created. If no feedback ID is present,
        // this field will be undefined.
        ...(pendingConcept.feedbackId !== undefined
          ? { feedbackId: pendingConcept.feedbackId }
          : {}),
      } as any);
      // Clear the pending concept so it is only applied once
      setPendingConcept(null);
    }
    // Only run this effect when the pending concept changes
  }, [pendingConcept, setPendingConcept]);

  // Keep the global context ID in sync with the local state. Whenever the
  // selected context changes in the tagging panel, update the global store.
  useEffect(() => {
    const normalisedLocal = selectedContextId ?? null;
    const normalisedGlobal = globalContextId ?? null;
    if (normalisedLocal !== normalisedGlobal) {
      setGlobalContextId(normalisedLocal);
    }
  }, [selectedContextId, globalContextId, setGlobalContextId]);

  // Mirror updates from the global context back to the local state. This is
  // required when a context is selected outside of the tagging panel and
  // ensures the UI reflects the current selection.
  useEffect(() => {
    const normalisedLocal = selectedContextId ?? null;
    const normalisedGlobal = globalContextId ?? null;
    if (normalisedLocal !== normalisedGlobal) {
      setSelectedContextId(normalisedGlobal);
    }
  }, [globalContextId]);

  const selectedBlock = useMemo(
    () =>
      selectedBlockId
        ? (report.blocks.find((b) => b.id === selectedBlockId) ?? null)
        : null,
    [report.blocks, selectedBlockId]
  );

  const isInitialLoading = isLoading || (!data && isFetching);
  const isUpdating = !!data && isFetching;

  function convertContextOutToXbrlContext(contextOut: ContextOut): XbrlContext {
    return {
      id: contextOut.context_id, // Use context_id as the ID
      label:
        contextOut.entity_name ||
        contextOut.entity_identifier ||
        'Unnamed Context', // Fallback label
      entityName: contextOut.entity_name || 'Unknown Entity', // Default name
      entityIdentifier: contextOut.entity_identifier, // `entity_identifier` is crucial for unique identification
      periodType: contextOut.period_type, // `period_type` is directly available
      // Convert string dates to Date objects if not already Date objects
      startDate: contextOut.start_date
        ? new Date(contextOut.start_date)
        : new Date('2023-01-01'),
      endDate: contextOut.end_date
        ? new Date(contextOut.end_date)
        : new Date('2023-12-31'),
      instantDate: contextOut.instant_date
        ? new Date(contextOut.instant_date)
        : new Date('2023-12-31'),
      entityScheme: contextOut.entity_scheme || 'http://www.sec.gov/CIK', // Fallback to default entity scheme
      createdAt: contextOut.created_at, // Use created_at from the API data
      updatedAt: contextOut.updated_at, // Optional updated_at field
    };
  }
  const handleAddTag = useCallback(() => {
    // Ensure both selectedBlockId and selectedConcept are set before proceeding
    if (!selectedBlockId || !selectedConcept) return;

    // Get the selected context by contextId, or undefined if no context is selected
    const contextToUse = selectedContextId
      ? contexts?.find((c) => c.context_id === selectedContextId)
      : undefined;

    // Convert the context (if available) from ContextOut to XbrlContext
    const convertedContext = contextToUse
      ? convertContextOutToXbrlContext(contextToUse) // Convert ContextOut to XbrlContext
      : undefined;

    // Creating the new tag object. If the selected concept originated from a
    // recommendation, it may carry a feedbackId property that should be
    // attached to the tag. We use a computed spread to include this
    // property only when defined.
    const newTag: XbrlTag = {
      id: generateUniqueId(), // Generate a unique ID for the tag
      concept: {
        id: selectedConcept.id,
        label: selectedConcept.label,
        type: selectedConcept.type || 'string', // Default to 'string' if no type is set
        definition: selectedConcept.originalLabel || selectedConcept.label, // Use the original label as the definition if available
        periodType:
          (selectedConcept.periodType as 'instant' | 'duration') || 'duration', // Default to 'duration' if no periodType is specified
        dataType: selectedConcept.type || 'xbrli:stringItemType', // Default to 'xbrli:stringItemType'
        balance: undefined,
        abstract: (selectedConcept as any).abstract === 'true', // Ensure abstract is correctly handled
        labels: selectedConcept.originalLabel
          ? [{ value: selectedConcept.originalLabel, role: 'label' }] // Assign the original label to the concept
          : undefined,
        references: undefined, // Handle references if needed
      },
      ...(convertedContext && { context: convertedContext }), // Attach converted context if it's available
      // Include the feedback ID if the selected concept originated from a recommendation
      ...((selectedConcept as any).feedbackId !== undefined
        ? { feedbackId: (selectedConcept as any).feedbackId }
        : {}),
      createdAt: new Date().toISOString(), // Record creation timestamp
      startIndex: highlightedText?.startIndex || 0, // Use the start index from the highlighted text
      endIndex: highlightedText?.endIndex || 0, // Use the end index from the highlighted text
    };

    // Update the report with the new tag added to the correct block
    const updatedReport: ReportDocument = {
      ...report,
      blocks: report.blocks.map((block) =>
        block.id === selectedBlockId
          ? { ...block, tags: [...block.tags, newTag] } // Add the new tag to the block's tags
          : block
      ),
      updatedAt: new Date().toISOString(), // Update the report's last modified timestamp
    };

    // Apply the updated report to the global state (or parent component)
    onReportChange(updatedReport);

    // Reset the selected concept and search query after applying the tag
    setSelectedConcept(null);
    setSearchQuery('');
  }, [
    selectedBlockId,
    selectedConcept,
    selectedContextId,
    highlightedText?.startIndex,
    highlightedText?.endIndex,
    onReportChange,
    report,
    contexts, // Make sure to include contexts here for conversion
  ]);

  /* ------------------------------- Error UI ------------------------------- */

  // if (isError) {
  //   return (
  //     <div className='space-y-4'>
  //       <Card className='border-0 shadow-sm'>
  //         <CardContent className='p-6'>
  //           <Alert variant='destructive' className='flex items-start gap-2'>
  //             <AlertCircle className='h-4 w-4 shrink-0 mt-0.5' />
  //             <div>
  //               <AlertTitle>Failed to load taxonomy</AlertTitle>
  //               <AlertDescription className='space-y-2'>
  //                 <p>
  //                   There was a problem fetching{' '}
  //                   <code className='font-mono text-xs'>
  //                     /taxonomy/{activeTab}
  //                   </code>
  //                   .
  //                 </p>
  //                 <p className='text-xs text-muted-foreground'>
  //                   {(error as any)?.message ?? 'Unknown error'}
  //                 </p>
  //               </AlertDescription>
  //             </div>
  //           </Alert>
  //         </CardContent>
  //       </Card>
  //     </div>
  //   );
  // }

  /* --------------------------------- UI ---------------------------------- */

  const ActiveIcon = TAB_META[activeTab].icon;
  const { data: myTaxonomies, isSuccess } = useMyTaxonomies();
  const { mutate: switchTaxonomy } = useSwitchTaxonomy({});

  const handleSwitchTaxonomy = () => {
    if (!value) return;

    // Call the mutate function with the taxonomyId
    switchTaxonomy(
      { taxonomyId: Number(value) },
      {
        onSuccess: () => {
          console.log('Taxonomy switched successfully');
        },
        onError: (error) => {
          console.error('Error switching taxonomy:', error);
        },
      }
    );
  };

  // Handle value change and automatically switch taxonomy

  const handleValueChange = (newValue: string) => {
    setValue(newValue);

    const selected = myTaxonomies?.find(
      (item) => item.id.toString() === newValue
    );
    if (selected) {
      switchTaxonomy({ taxonomyId: selected.id });
      setSelectedTaxonomy(selected);
    }
  };

  const { setSelectedTaxonomy } = useTaxonomyStore();

  useEffect(() => {
    // console.log(isSuccess, 'success');
    if (isSuccess) {
      setValue(myTaxonomies[0]?.id.toString());
      console.log(isSuccess, 'success');
      setSelectedTaxonomy(myTaxonomies[0]);
    }
  }, [isSuccess]);

  return (
    <div className='w-full space-y-6'>
      {!selectedBlock ? (
        <Card className='border-0 shadow-sm bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900'>
          <CardContent className='p-8 text-center'>
            <div className='flex items-center justify-center w-16 h-16 mx-auto mb-4 rounded-full bg-primary/10'>
              <Target className='w-8 h-8 text-primary' />
            </div>
            <h3 className='mb-2 text-lg font-semibold'>Select Text to Tag</h3>
            <p className='text-sm text-muted-foreground'>
              Choose a block of text from the document to start adding tags
            </p>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Selected Text */}
          <Card className='mt-0 border-0 shadow-sm'>
            <CardHeader className='pt-1 pb-1'>
              <CardTitle className='flex items-center gap-2 text-base'>
                <FileText className='w-4 h-4 text-blue-600' />
                Selected Text
              </CardTitle>
            </CardHeader>
            <CardContent className='space-y-3'>
              {isInitialLoading ? (
                <div className='p-3 border-2 border-blue-200 border-dashed rounded-lg dark:border-blue-800'>
                  <Skeleton className='h-5 mb-2 w-28' />
                  <LoadingBlock lines={2} />
                </div>
              ) : (
                <div className='p-3 border-2 border-blue-200 border-dashed rounded-lg dark:border-blue-800 bg-blue-50/50 dark:bg-blue-950/20'>
                  {highlightedText?.text ? (
                    <div className='space-y-2'>
                      <Badge variant='secondary' className='text-xs'>
                        Highlighted Selection
                      </Badge>
                      <p className='px-2 py-1 text-sm break-words rounded bg-primary/20'>
                        {highlightedText.text}
                      </p>
                    </div>
                  ) : (
                    <div className='space-y-2'>
                      <Badge variant='outline' className='text-xs'>
                        Full Block
                      </Badge>
                      <p className='text-sm break-words'>
                        {selectedBlock.content.length > 150
                          ? `${selectedBlock.content.substring(0, 150)}...`
                          : selectedBlock.content}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Tabs */}
          <Card className='border-0 shadow-sm'>
            <CardHeader className='flex flex-row items-center justify-between pb-2'>
              <div className='flex items-center gap-2'>
                <ActiveIcon className='w-4 h-4 text-muted-foreground' />
                <CardTitle className='text-base'>Taxonomy</CardTitle>
                {isUpdating && (
                  <span className='inline-flex items-center gap-1 ml-1 text-xs text-muted-foreground'>
                    <Loader2 className='w-3 h-3 animate-spin' /> updating…
                  </span>
                )}
              </div>
              {myTaxonomies && myTaxonomies.length > 0 && (
                <Select value={value} onValueChange={handleValueChange}>
                  <SelectTrigger className='w-[180px]'>
                    <SelectValue placeholder='Taxonomy' />
                  </SelectTrigger>
                  <SelectContent>
                    {myTaxonomies.map((item) => (
                      <SelectItem value={item.id.toString()} key={item.id}>
                        {item.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            </CardHeader>
            <CardContent className='p-0'>
              <Tabs
                value={activeTab}
                onValueChange={(v) => setActiveTab(v as TabKey)}
                className='w-full'
              >
                <TabsList className='grid w-full grid-cols-4'>
                  {(Object.keys(TAB_META) as TabKey[]).map((tab) => {
                    const Icon = TAB_META[tab].icon;
                    return (
                      <TabsTrigger
                        key={tab}
                        value={tab}
                        className='flex items-center gap-1'
                      >
                        <Icon className='w-3 h-3' />
                        <span className='hidden sm:inline'>
                          {TAB_META[tab].label}
                        </span>
                        <span className='sm:hidden'>
                          {TAB_META[tab].label.slice(0, 4)}
                        </span>
                      </TabsTrigger>
                    );
                  })}
                </TabsList>

                {(Object.keys(TAB_META) as TabKey[]).map((tab) => (
                  <TabsContent key={tab} value={tab}>
                    <TaxonomyBrowser
                      activeTab={tab}
                      taxonomyData={activeTab === tab ? taxonomyData : null}
                      isInitialLoading={
                        activeTab === tab ? isInitialLoading : false
                      }
                      isUpdating={activeTab === tab ? isUpdating : false}
                      searchQuery={activeTab === tab ? searchQuery : ''}
                      setSearchQuery={setSearchQuery}
                      selectedConcept={selectedConcept}
                      setSelectedConcept={setSelectedConcept}
                    />
                  </TabsContent>
                ))}
              </Tabs>
            </CardContent>
          </Card>

          {/* Context Selection */}
          <Card className='p-0 mt-0 border-t shadow-sm'>
            <CardHeader>
              <CardTitle className='flex items-center justify-between gap-2 text-base'>
                <div>
                  Context Selection{' '}
                  <Badge variant='secondary' className='text-xs ml-2'>
                    Optional
                  </Badge>
                </div>
                <CreateContextModal />
              </CardTitle>
            </CardHeader>
            <CardContent className='space-y-3'>
              {isInitialLoading ? (
                <Skeleton className='w-full h-10' />
              ) : (
                <div className='flex gap-2'>
                  <Select
                    value={selectedContextId || ''}
                    onValueChange={setSelectedContextId}
                  >
                    <SelectTrigger className='h-10 flex-1'>
                      <SelectValue placeholder='Select a reporting context (optional)' />
                    </SelectTrigger>
                    <SelectContent>
                      {contexts?.map((context) => (
                        <SelectItem key={context.id} value={context.context_id}>
                          <div className='flex items-end '>
                            <div className='flex flex-col items-start'>
                              <span className='font-medium'>
                                {context.entity_name || 'Unnamed Entity'}
                              </span>
                              <span className='text-xs text-muted-foreground'>
                                {context.entity_identifier} •{' '}
                                {context.period_type}
                              </span>
                            </div>
                            <span className='text-[10px] text-muted-foreground'>
                              Context ID: {context.context_id}
                            </span>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Selected Concept */}
          <Card className='p-0 mt-0 border-t shadow-sm'>
            <CardHeader>
              <CardTitle className='flex items-center gap-2 text-base'>
                Selected Tag
              </CardTitle>
            </CardHeader>
            <CardContent className='space-y-2'>
              {selectedConcept ? (
                <div className='space-y-1'>
                  <Badge variant='secondary' className='text-xs'>
                    {selectedConcept.label}
                  </Badge>
                  {selectedConcept.originalLabel && (
                    <p className='text-xs text-muted-foreground'>
                      {selectedConcept.originalLabel}
                    </p>
                  )}
                </div>
              ) : (
                <p className='text-sm text-muted-foreground'>
                  No tag selected yet
                </p>
              )}
            </CardContent>
          </Card>

          {/* Add Tag */}
          <Card className='border-0 shadow-sm bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20'>
            <CardContent className='p-4'>
              <Button
                className='w-full h-12 text-base font-medium bg-gradient-to-r from-blue-600 to-indigo-600'
                disabled={
                  isInitialLoading || !selectedBlockId || !selectedConcept
                }
                onClick={handleAddTag}
                size='lg'
              >
                <Plus className='w-5 h-5 mr-2' />
                Add Tag
              </Button>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
};

export { TaggingPanel };
export default TaggingPanel;
