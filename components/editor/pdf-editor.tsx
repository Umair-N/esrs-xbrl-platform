/*
 * PdfEditor component with caching and improved performance
 *
 * This version of the PdfEditor caches loaded PDF pages in sessionStorage
 * keyed by report ID. When the component mounts, it checks for a cached
 * entry and loads it if available, avoiding repeated network calls when
 * reloading the same session. When pages are fetched from the backend,
 * they are converted to Data URLs and stored in the cache. The component
 * also optimizes tag application by finalising the tag immediately and
 * sending feedback asynchronously, improving responsiveness when the
 * user selects a recommendation. Tagged words are highlighted on the
 * PDF, and drag-selection is supported.
 */

'use client';

import { useEffect, useState, useMemo, useRef, useCallback } from 'react';
import { axiosInstance } from '@/lib/axios';
import type { ReportDocument } from '@/types/report';
import { useRecommendations } from '@/features/recommender/api/get-recommendations';
import { usePostFeedback } from '@/features/recommender/api/post-feedback';
import { useTaggingStore } from '@/store/tagging-store';
import { useTaxonomyStore } from '@/store/taxonomoy-store';
import { sampleContexts } from '@/lib/sample-data';
// We intentionally avoided using the Radix Popover initially for the
// recommendation overlay, but have since integrated the shadcn Popover
// implementation.  For positioning, we compute coordinates and store
// them in `popoverTriggerElement` rather than referencing an actual DOM
// node.  This allows us to emulate an element's `offsetTop` and
// `offsetLeft` in a simple state object.
import { showError } from '@/components/heads-up';
// Import Popover components from shadcn/ui.  We use these for the
// recommendation popover, leveraging Radix's positioning and collision
// detection so the popover appears adjacent to the selected text and flips
// sides when near the viewport edge.
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from '@/components/ui/popover';

// Import UI components and icons for the recommendation popover.  These
// components come from the shadcn/ui library and lucide-react icon set.
import { Button } from '@/components/ui/button';
import {
  TooltipProvider,
  Tooltip,
  TooltipTrigger,
  TooltipContent,
} from '@/components/ui/tooltip';
import { Lightbulb, LucideInfo, X } from 'lucide-react';

interface WordEntry {
  bbox: [number, number, number, number];
  text: string;
  start_index: number;
  end_index: number;
}

interface PageData {
  pageNumber: number;
  width: number;
  height: number;
  imageUrl: string;
  words: WordEntry[];
}

interface PdfEditorProps {
  report: ReportDocument;
  /**
   * Callback invoked when the report object should be updated.  When a tag is
   * applied, the updated report is passed back to the parent so that the
   * state can be persisted.  The parent component then replaces its
   * local report state with the new value.
   */
  onReportChange: (report: ReportDocument) => void;
  /**
   * Callback fired when the user highlights a range of text.  This is used
   * to show the highlight in the tagging panel and to fetch
   * recommendations.  The block ID and character indices identify the
   * highlighted range within the report.
   */
  onTextHighlight: (
    blockId: string,
    selectedText: string,
    startIndex: number,
    endIndex: number
  ) => void;
}

export function PdfEditor({
  report,
  onReportChange,
  onTextHighlight,
}: PdfEditorProps) {
  /**
   * pagesInfo holds basic information for each page such as width and height.
   * These entries come from the `/pages_info` endpoint and allow us to
   * preallocate page containers without loading the heavy image and word data.
   */
  /**
   * pagesInfo holds lightweight metadata for each page in the PDF such as
   * dimensions.  We retrieve this once from the `/pages_info` endpoint and
   * use it to preallocate the page containers before any heavy data is
   * loaded.  This allows virtualization of pages and reduces initial load
   * time, since images and words are fetched only when the user scrolls
   * near a page.
   */
  const [pagesInfo, setPagesInfo] = useState<any[]>([]);
  /**
   * loadedPages stores the fully loaded page data (image and words) keyed by
   * their page index.  Only pages that the user has viewed or scrolled
   * near are fetched and stored here.  This lazy loading strategy
   * drastically reduces the initial import time for large PDFs by loading
   * only what is necessary.
   */
  const [loadedPages, setLoadedPages] = useState<Record<number, PageData>>({});
  /**
   * loadingPages tracks which page indices are currently being fetched.
   * This prevents duplicate network requests when multiple events try to
   * trigger loading of the same page concurrently.
   */
  const [loadingPages, setLoadingPages] = useState<Record<number, boolean>>({});
  const [selectedWords, setSelectedWords] = useState<{
    pageIndex: number;
    indices: number[];
  } | null>(null);
  const [selectionAnchor, setSelectionAnchor] = useState<{
    pageIndex: number;
    wordIndex: number;
  } | null>(null);
  const [showPopover, setShowPopover] = useState(false);
  /**
   * Coordinates for the recommendation overlay. When the user highlights a phrase
   * on the PDF we compute the bounding box of the selected words and store
   * these coordinates here. The overlay uses `position: fixed` to appear at
   * this location relative to the viewport. See `handleMouseUp` for details.
   */
  // Coordinates for the recommendation popover.  Instead of storing a DOM
  // element reference we store an object with `offsetTop` and `offsetLeft`
  // properties to mimic an element's position.  This mirrors the API
  // expected in the user-provided snippet (see PopoverContent style).  When
  // the user highlights text on a PDF page we compute the bounding box of the
  // selected words and store the resulting coordinates here.  The popover
  // reads these values to position itself relative to the viewport via
  // `position: fixed`.
  const [popoverTriggerElement, setPopoverTriggerElement] = useState<{
    offsetTop: number;
    offsetLeft: number;
  } | null>(null);

  // Note: we no longer track popover alignment via state.  The popover's
  // absolute position is computed directly in handleMouseUp() below.  See
  // `handleMouseUp` for details on how `popoverTriggerElement` is calculated.
  const [highlightRange, setHighlightRange] = useState<{
    blockId: string;
    startIndex: number;
    endIndex: number;
  } | null>(null);
  const [highlightedText, setHighlightedText] = useState('');

  // In-place editing of PDF content is not supported in this version. The PDF
  // editor focuses on tagging and highlighting functionality. If in-place
  // editing becomes feasible in the future, it should be implemented here.

  /**
   * Track progress of PDF page loading. A value between 0 and 1 indicates the
   * proportion of pages that have been fetched and processed. This allows
   * displaying a progress indicator to the user. When pages are loaded from
   * cache the progress is set to 1 immediately.
   */
  /**
   * Track progress of PDF page loading as a fraction of pages loaded.  When
   * using lazy loading, this indicates the fraction of pages that have
   * completed loading relative to the total number of pages.  A value of 1
   * means all pages have been loaded.
   */
  const [progress, setProgress] = useState(0);

  /**
   * containerRef refers to the scrollable element that contains all PDF
   * pages.  It is used as the root for the IntersectionObserver so that
   * pages can be loaded when they become visible within the scroll area.
   */
  const containerRef = useRef<HTMLDivElement | null>(null);
  /**
   * pageRefs holds references to each page's container div.  These refs
   * are populated during render and are observed by the IntersectionObserver.
   */
  const pageRefs = useRef<(HTMLDivElement | null)[]>([]);

  /**
   * Load a single page's image and words from the backend.  If the page is
   * already loaded or currently being loaded, this function returns early.
   * On success the loadedPages state is updated with the new page data.
   * Pages are keyed by their index (0-based).  Use this function to
   * lazily fetch pages as they come into view.
   */
  const loadPage = useCallback(
    async (index: number) => {
      // Guard: ensure we have metadata and a valid index
      if (!pagesInfo || index < 0 || index >= pagesInfo.length) return;
      if (!report || !report.id) return;
      // If page is already loaded or in the process of loading, skip
      if (loadedPages[index] || loadingPages[index]) return;
      // Mark as loading
      setLoadingPages((prev) => ({ ...prev, [index]: true }));
      try {
        const pInfo = pagesInfo[index];
        const pageNumber = pInfo.page_number;
        // Fetch image as a Blob.  To minimise parsing overhead for large
        // images, immediately create an object URL for display.  Later we
        // asynchronously convert the blob to a Data URL for caching.  Using
        // URL.createObjectURL makes page rendering snappier because it
        // avoids the heavy base64 conversion up front.
        const imgRes = await axiosInstance.get(
          `/reports/${report.id}/pages/${pageNumber}/image`,
          { responseType: 'blob' }
        );
        const blob: Blob = imgRes.data;
        // Create a temporary object URL for immediate display
        const objectUrl = URL.createObjectURL(blob);
        // Define a function to convert to Data URL asynchronously for cache
        const convertToDataUrl = async (b: Blob) => {
          return new Promise<string>((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result as string);
            reader.onerror = reject;
            reader.readAsDataURL(b);
          });
        };
        // Fetch words
        const wordsRes = await axiosInstance.get(
          `/reports/${report.id}/pages/${pageNumber}/words`
        );
        const wordData: WordEntry[] = wordsRes.data?.words || [];
        const pageWidth = wordsRes.data?.page_width || pInfo.width;
        const pageHeight = wordsRes.data?.page_height || pInfo.height;
        // Save page data with object URL for fast display
        setLoadedPages((prev) => ({
          ...prev,
          [index]: {
            pageNumber: pageNumber,
            width: pageWidth,
            height: pageHeight,
            imageUrl: objectUrl,
            words: wordData,
          },
        }));
        // Asynchronously convert the blob to a Data URL and update
        // sessionStorage.  We do not await this conversion to avoid blocking
        // the main thread.  When complete, the Data URL is stored in the
        // cache for subsequent sessions.  Note: we do not update the
        // loadedPages entry with the Data URL because the object URL is
        // sufficient for display and avoids unnecessary re-renders.
        if (typeof window !== 'undefined') {
          const cacheKey = `pdf-pages-partial-${report.id}`;
          convertToDataUrl(blob)
            .then((dataUrl) => {
              try {
                const existing = window.sessionStorage.getItem(cacheKey);
                const parsed = existing ? JSON.parse(existing) : {};
                parsed[index] = {
                  pageNumber: pageNumber,
                  width: pageWidth,
                  height: pageHeight,
                  imageUrl: dataUrl,
                  words: wordData,
                };
                window.sessionStorage.setItem(cacheKey, JSON.stringify(parsed));
              } catch (err) {
                // Ignore cache errors
              }
            })
            .catch(() => {
              /* ignore conversion errors */
            });
        }
      } catch (err) {
        console.error(`Failed to load page ${index}`, err);
      } finally {
        // Remove loading flag
        setLoadingPages((prev) => {
          const copy = { ...prev };
          delete copy[index];
          return copy;
        });
      }
    },
    [pagesInfo, loadedPages, loadingPages, report]
  );

  /**
   * Recompute the overall progress whenever either the page metadata or the
   * loaded pages change.  Progress is defined as the fraction of pages
   * currently loaded relative to the total number of pages.  When no
   * metadata has been loaded yet, the progress is set to 1 to avoid
   * showing a spinner indefinitely.
   */
  useEffect(() => {
    if (!pagesInfo || pagesInfo.length === 0) {
      setProgress(1);
      return;
    }
    const loadedCount = Object.keys(loadedPages).length;
    const fraction = loadedCount / pagesInfo.length;
    setProgress(fraction);
  }, [loadedPages, pagesInfo]);

  /**
   * Setup an IntersectionObserver to lazily load pages as they come into
   * view.  The observer is attached to each page's container and triggers
   * loadPage when the page intersects the viewport (within a root margin).
   * We also prefetch the next page when a page becomes visible to smooth
   * user scrolling.  The observer is cleaned up when the component or
   * pagesInfo changes.
   */
  useEffect(() => {
    if (!containerRef.current || !pagesInfo || pagesInfo.length === 0) return;
    const rootEl = containerRef.current;
    // IntersectionObserver callback
    const handleIntersect: IntersectionObserverCallback = (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const idxAttr = (entry.target as HTMLElement).getAttribute(
            'data-index'
          );
          const idx = idxAttr ? parseInt(idxAttr, 10) : NaN;
          if (!isNaN(idx)) {
            loadPage(idx);
            // Prefetch the next page if available
            if (idx + 1 < pagesInfo.length) loadPage(idx + 1);
          }
        }
      });
    };
    const observer = new IntersectionObserver(handleIntersect, {
      root: rootEl,
      rootMargin: '200px',
      threshold: 0.1,
    });
    // Observe each page container
    pageRefs.current.forEach((el) => {
      if (el) observer.observe(el);
    });
    return () => {
      observer.disconnect();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pagesInfo, loadPage]);

  const { mutate: fetchRecommendations, data: recommendations } =
    useRecommendations({
      mutationConfig: {},
    });
  const { mutate: sendFeedback } = usePostFeedback();
  const selectedTaxonomy = useTaxonomyStore((state) => state.selectedTaxonomy);
  const { setPendingConcept, selectedContextId } = useTaggingStore();

  /**
   * Load pages either from the cache or via network. Cached pages are stored
   * in sessionStorage using the report ID as the key. When fetching from
   * the network, convert blobs to Data URLs so they can be serialised.
   */
  useEffect(() => {
    // If there is no report or the file is not a PDF, reset state.  We do
    // not attempt to load page information in that case.
    if (
      !report ||
      !report.id ||
      !report.file_type?.toLowerCase().includes('pdf')
    ) {
      setPagesInfo([]);
      setLoadedPages({});
      setLoadingPages({});
      setProgress(1);
      return;
    }
    // Fetch lightweight page metadata.  These entries contain the width,
    // height and page_number for each page.  We load the actual page
    // contents lazily as the user scrolls.
    const fetchPagesInfo = async () => {
      try {
        const infoRes = await axiosInstance.get(
          `/reports/${report.id}/pages_info`
        );
        const info: any[] = infoRes.data?.pages || [];
        setPagesInfo(info);
        // Preload the first page and, if available, the second page so that
        // the user sees content immediately.  Additional pages will be
        // loaded on demand via the IntersectionObserver.
        if (info.length > 0) {
          loadPage(0);
          if (info.length > 1) loadPage(1);
        }
      } catch (err) {
        console.error('Failed to fetch PDF page info', err);
        setPagesInfo([]);
      }
    };
    fetchPagesInfo();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [report?.id, report?.file_type]);

  /**
   * Compute which words belong to tags for each page. Results are cached via
   * useMemo so they recompute only when pages or report change.
   */
  const taggedWordIndicesByPage = useMemo(() => {
    const result: Record<number, Set<number>> = {};
    if (!report?.blocks) return result;
    // Only compute for pages that have been loaded.  Each key in
    // loadedPages corresponds to a page index.  We parse the key to get
    // the numeric index and look up the corresponding block.  If the
    // block contains tags, we map each tag to the set of words on that
    // page whose bounding boxes overlap the tag's character range.
    Object.entries(loadedPages).forEach(([key, page]) => {
      const pIdx = parseInt(key, 10);
      if (isNaN(pIdx)) return;
      const block = report.blocks?.[pIdx];
      if (!block || !block.tags || block.tags.length === 0) return;
      const set = new Set<number>();
      block.tags.forEach((tag) => {
        const tagStart = tag.startIndex ?? 0;
        const tagEnd = tag.endIndex ?? block.content?.length ?? 0;
        page.words.forEach((word, wIdx) => {
          if (word.start_index < tagEnd && word.end_index > tagStart) {
            set.add(wIdx);
          }
        });
      });
      result[pIdx] = set;
    });
    return result;
  }, [loadedPages, report]);

  // Function to close the popover and clear selection
  function closePopover() {
    setShowPopover(false);
    setHighlightRange(null);
    // Clear the popover trigger coordinates
    setPopoverTriggerElement(null);
    setSelectedWords(null);
  }

  /**
   * Begin a drag selection when the user presses on a word overlay.  We use
   * event delegation: the overlay container listens for mouse down and
   * determines which word index was clicked based on a data attribute.  This
   * eliminates the need to attach separate handlers to each word, improving
   * performance on pages with thousands of words.
   */
  const handleOverlayMouseDown = (
    pageIndex: number,
    event: React.MouseEvent<HTMLDivElement>
  ) => {
    const target = event.target as HTMLElement;
    const idxStr = target.getAttribute('data-index');
    if (idxStr === null) return;
    const wordIndex = parseInt(idxStr, 10);
    if (isNaN(wordIndex)) return;
    event.preventDefault();
    closePopover();
    // Ensure the page is loaded before starting a selection.  If not, do
    // nothing.  This prevents highlighting from being attempted on
    // unloaded pages (which would have no word data).
    if (!loadedPages[pageIndex]) return;
    setSelectionAnchor({ pageIndex, wordIndex });
    setSelectedWords({ pageIndex, indices: [wordIndex] });
  };

  /**
   * Update selection range as the cursor moves over word overlays.  This
   * function is attached to the overlay container rather than individual
   * word divs.  It computes the current word index based on the data
   * attribute and updates the selected range accordingly.
   */
  const handleOverlayMouseMove = (
    pageIndex: number,
    event: React.MouseEvent<HTMLDivElement>
  ) => {
    if (!selectionAnchor || pageIndex !== selectionAnchor.pageIndex) return;
    // Only update selection on pages that are loaded
    if (!loadedPages[pageIndex]) return;
    const target = event.target as HTMLElement;
    const idxStr = target.getAttribute('data-index');
    if (idxStr === null) return;
    const wordIndex = parseInt(idxStr, 10);
    if (isNaN(wordIndex)) return;
    const start = selectionAnchor.wordIndex;
    const end = wordIndex;
    const indices: number[] = [];
    if (start <= end) {
      for (let i = start; i <= end; i++) indices.push(i);
    } else {
      for (let i = start; i >= end; i--) indices.push(i);
    }
    setSelectedWords({ pageIndex, indices });
  };

  /**
   * Finalise drag selection. Compute selected text and character indices and
   * invoke the parent callback. Then fetch recommendations and show popover.
   */
  const handleMouseUp = () => {
    // No edit mode check: in-place editing is not supported
    if (!selectionAnchor || !selectedWords) {
      setSelectionAnchor(null);
      return;
    }
    const { pageIndex } = selectionAnchor;
    const page = loadedPages[pageIndex];
    if (!page) {
      setSelectionAnchor(null);
      return;
    }
    const indices = selectedWords.indices;
    if (!indices || indices.length === 0) {
      setSelectionAnchor(null);
      return;
    }
    const sorted = [...indices].sort((a, b) => a - b);
    const startWord = page.words[sorted[0]];
    const endWord = page.words[sorted[sorted.length - 1]];
    if (!startWord || !endWord) {
      setSelectionAnchor(null);
      return;
    }
    const startIndex = startWord.start_index;
    const endIndex = endWord.end_index;
    const block = report.blocks?.[pageIndex];
    const blockId = block?.id || '';
    // Unused: blockContent remains available in case of future improvements.
    // Build the selected text by concatenating the actual word texts.  Joining
    // based on page.words ensures that we capture exactly the words the user
    // selected rather than slicing the raw block content (which can result in
    // truncated or garbled substrings if the underlying word boundaries and
    // block content do not align perfectly).  This approach also avoids
    // including characters outside of the selected words when indices are
    // mis‑aligned.
    const selectedText = sorted
      .map((i) => {
        const w = page.words[i];
        return w?.text || '';
      })
      .join(' ');
    onTextHighlight(blockId, selectedText, startIndex, endIndex);
    setHighlightRange({ blockId, startIndex, endIndex });
    setHighlightedText(selectedText);
    // Compute bounding box union for popover
    let x0 = Infinity,
      y0 = Infinity,
      x1 = -Infinity,
      y1 = -Infinity;
    sorted.forEach((i) => {
      const [bx0, by0, bx1, by1] = page.words[i].bbox;
      if (bx0 < x0) x0 = bx0;
      if (by0 < y0) y0 = by0;
      if (bx1 > x1) x1 = bx1;
      if (by1 > y1) y1 = by1;
    });
    // Compute absolute position for the recommendation popover.  We calculate the
    // top and left coordinates in viewport space, taking into account the
    // container's position.  If the popover would overflow the viewport on
    // the right side, we shift it to the left side of the selection.  A
    // constant overlay width of 320px (≈ 20rem) is assumed for collision
    // detection.
    const container = document.getElementById(`pdf-page-${pageIndex}`);
    if (container) {
      const containerRect = container.getBoundingClientRect();
      const overlayWidth = 320; // width of the popover content in pixels
      // Compute candidate absolute coordinates relative to the viewport
      const candidateTop = containerRect.top + y1 + 4;
      let candidateLeft = containerRect.left + x0;
      // If the overlay would overflow the right edge of the viewport, anchor
      // to the right edge of the selection instead and shift left by its width
      if (candidateLeft + overlayWidth > window.innerWidth - 16) {
        candidateLeft = containerRect.left + x1 - overlayWidth;
        if (candidateLeft < 0) candidateLeft = 0;
      }
      setPopoverTriggerElement({
        offsetTop: candidateTop,
        offsetLeft: candidateLeft,
      });
    } else {
      // Fallback: set popover position relative to word bounding box only
      setPopoverTriggerElement({ offsetTop: y1 + 4, offsetLeft: x0 });
    }
    // Fetch recommendations if taxonomy is selected
    if (!selectedTaxonomy?.name) {
      showError({ title: 'Please select a taxonomy', message: '' });
    } else if (selectedText && selectedText.trim().length > 0) {
      fetchRecommendations(
        {
          data: {
            query: selectedText,
            taxonomy: selectedTaxonomy.name?.toLocaleLowerCase() || '',
            k: 5,
            rerank: true,
          },
        },
        {
          onSuccess: () => setShowPopover(true),
          onError: () => setShowPopover(true),
        }
      );
    }
    setSelectionAnchor(null);
  };

  /**
   * Apply a selected recommendation. Finalise the tag immediately to improve
   * responsiveness, then send feedback asynchronously without awaiting
   * completion. We do not update the tag with the feedback ID to avoid
   * re-rendering; feedback is purely informational for the recommender.
   */
  const applyTag = (item: {
    tag: string;
    reference: string;
    datatype: string;
    rank?: number;
  }) => {
    if (!highlightRange) return;
    const { blockId, startIndex, endIndex } = highlightRange;
    const localContextId = selectedContextId;
    const concept = {
      id: item.tag,
      label: item.reference,
      definition: '',
      type: item.datatype,
      periodType: '',
    };
    const finalizeTag = () => {
      if (localContextId) {
        const context = sampleContexts.find((c) => c.id === localContextId);
        const newTag = {
          id: `${Date.now()}`,
          concept,
          startIndex,
          endIndex,
          ...(context ? { context } : {}),
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
        // No context selected; store concept for tagging panel
        setPendingConcept(concept);
      }
      closePopover();
    };
    // Finalise tag immediately
    finalizeTag();
    // Send feedback asynchronously but do not wait for result
    const feedbackPayload = {
      taxonomy: selectedTaxonomy?.name?.toLocaleLowerCase() || '',
      query: highlightedText,
      reference: item.reference,
      tag: item.tag,
      is_correct: true,
      is_custom: false,
      rank: item.rank ?? 0,
    };
    sendFeedback({ data: feedbackPayload });
  };

  // We no longer gate rendering on progress.  Instead, render the pages as soon
  // as metadata is available and show a progress bar at the top indicating
  // how many pages have been loaded relative to the total.  As the user
  // scrolls through the document, more pages will load and the progress bar
  // will update accordingly.  When all pages are loaded (which occurs only
  // after they have all been viewed), the bar reaches 100%.
  const percent = Math.round(progress * 100);

  /**
   * Build a unified list of pages by combining lightweight page metadata
   * (pagesInfo) with any loaded page data (loadedPages).  When a page
   * has not been loaded yet its imageUrl will be an empty string and
   * words will be an empty array.  This allows us to reuse the existing
   * rendering logic with minimal changes.  The list is memoised to
   * avoid unnecessary recalculations on each render.
   */
  const pages = useMemo(() => {
    return pagesInfo.map((info: any, idx: number) => {
      const loaded = loadedPages[idx];
      if (loaded) return loaded;
      return {
        pageNumber: info.page_number ?? idx,
        width: info.width,
        height: info.height,
        imageUrl: '',
        words: [] as WordEntry[],
      } as PageData;
    });
  }, [pagesInfo, loadedPages]);

  return (
    <div
      ref={containerRef}
      className='overflow-y-auto max-h-[80vh] px-4 py-2 space-y-8'
    >
      {/* Progress bar indicating how many pages have been loaded.  This bar
          will gradually fill as the user scrolls and additional pages
          load.  When all pages have been loaded the bar reaches 100%. */}
      {pagesInfo.length > 0 && (
        <div className='flex flex-col items-center justify-center mb-4'>
          <p className='text-sm text-muted-foreground'>
            Loading PDF… {percent}%
          </p>
          <div className='w-64 bg-muted/20 rounded-full h-2 overflow-hidden'>
            <div
              className='bg-primary h-2 rounded-full'
              style={{ width: `${percent}%` }}
            />
          </div>
        </div>
      )}
      {pages.map((page, pIdx) => (
        <div
          key={pIdx}
          id={`pdf-page-${pIdx}`}
          data-index={pIdx}
          ref={(el) => {
            pageRefs.current[pIdx] = el;
          }}
          className='relative mx-auto shadow-sm'
          style={{ width: `${page.width}px`, height: `${page.height}px` }}
          onMouseUp={handleMouseUp}
        >
          {/* Page image or placeholder */}
          {page.imageUrl ? (
            <img
              src={page.imageUrl}
              alt={`Page ${page.pageNumber}`}
              style={{
                width: `${page.width}px`,
                height: `${page.height}px`,
                display: 'block',
              }}
            />
          ) : (
            <div
              style={{
                width: `${page.width}px`,
                height: `${page.height}px`,
                backgroundColor: 'rgba(200, 200, 200, 0.2)',
              }}
            />
          )}
          {/* Word overlays are rendered inside a single container with delegated
              event handlers.  Each word div carries a data-index attribute
              identifying its position in the words array.  This approach
              eliminates the need to attach per-word event listeners, greatly
              improving performance for pages with many words. */}
          {page.imageUrl && page.words.length > 0 && (
            <div
              className='word-overlay-container'
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: `${page.width}px`,
                height: `${page.height}px`,
              }}
              onMouseDown={(e) => handleOverlayMouseDown(pIdx, e)}
              onMouseMove={(e) => handleOverlayMouseMove(pIdx, e)}
            >
              {page.words.map((word, wIdx) => {
                const [x0, y0, x1, y1] = word.bbox;
                const isInSelection =
                  selectedWords !== null &&
                  selectedWords.pageIndex === pIdx &&
                  selectedWords.indices.includes(wIdx);
                const taggedSet = taggedWordIndicesByPage[pIdx];
                const isTagged = taggedSet ? taggedSet.has(wIdx) : false;
                return (
                  <div
                    key={wIdx}
                    data-index={wIdx}
                    style={{
                      position: 'absolute',
                      left: `${x0}px`,
                      top: `${y0}px`,
                      width: `${x1 - x0}px`,
                      height: `${y1 - y0}px`,
                      backgroundColor: isInSelection
                        ? 'rgba(255, 255, 0, 0.4)'
                        : isTagged
                          ? 'rgba(0, 128, 255, 0.2)'
                          : 'transparent',
                      cursor: 'text',
                    }}
                  />
                );
              })}
            </div>
          )}

          {/* Recommendation popover using shadcn/ui Popover.  When a selection is
          highlighted on the current page, we show a popover anchored to a
          hidden trigger.  The popover's position is explicitly set via the
          `style` prop on the PopoverContent using the coordinates computed in
          `handleMouseUp`.  This avoids randomness and allows flipping to the
          left when the popover would overflow the viewport.  The popover
          remains resizable via the `resize` CSS property. */}
          {page.imageUrl &&
            showPopover &&
            selectedWords?.pageIndex === pIdx &&
            popoverTriggerElement && (
              <Popover
                open={showPopover && selectedWords?.pageIndex === pIdx}
                onOpenChange={(open) => {
                  // Mirror the open state to show/hide the popover.  When the
                  // popover closes (e.g., when clicking outside), call closePopover
                  // to reset selection and internal state.
                  setShowPopover(open);
                  if (!open) {
                    closePopover();
                  }
                }}
              >
                <PopoverTrigger asChild>
                  {/* The trigger element is hidden.  We position the popover via the
                inline `style` on PopoverContent rather than relying on
                the trigger's position. */}
                  <div style={{ display: 'none' }} />
                </PopoverTrigger>
                <PopoverContent
                  side='bottom'
                  align='start'
                  sideOffset={8}
                  className='p-0 w-80'
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
                        {recommendations?.results?.map(
                          (item: any, index: number) => (
                            <Button
                              key={item.tag}
                              variant='ghost'
                              className='relative justify-start w-full h-auto p-3 py-2 text-left hover:bg-muted/50 group'
                              onClick={() => applyTag(item)}
                            >
                              <div className='space-y-1'>
                                {/*
                          We intentionally omit the item.reference from the main line to
                          keep the suggestion list compact.  Hover over the info icon
                          to see the full concept details in the tooltip below.
                        */}
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
                          )
                        )}
                      </div>
                    ) : (
                      <div className='py-6 text-center text-muted-foreground'>
                        <Lightbulb className='w-8 h-8 mx-auto mb-2 opacity-50' />
                        <p className='text-sm font-medium'>
                          No suggestions found
                        </p>
                        <p className='text-xs'>Try selecting different text</p>
                      </div>
                    )}
                  </div>
                </PopoverContent>
              </Popover>
            )}
        </div>
      ))}
      {/* In-place editing overlay is disabled. If future support for
          editing PDF text becomes available, it can be implemented here. */}
    </div>
  );
}
