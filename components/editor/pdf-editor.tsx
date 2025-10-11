/*
 * PdfEditor component with virtualization and canvas-based overlays
 *
 * This version of the PdfEditor addresses performance issues when loading
 * large PDFs by lazily loading pages on demand and drawing tag and
 * selection highlights onto a single canvas per page.  The number of
 * DOM nodes is dramatically reduced compared to using individual divs
 * for each word, preventing browser lag and improving interactivity.
 */

'use client';

import React, {
  useEffect,
  useState,
  useMemo,
  useRef,
  useCallback,
} from 'react';
import { axiosInstance } from '@/lib/axios';
import type { ReportDocument } from '@/types/report';
import { useRecommendations } from '@/features/recommender/api/get-recommendations';
import { usePostFeedback } from '@/features/recommender/api/post-feedback';
import { useTaggingStore } from '@/store/tagging-store';
import { useTaxonomyStore } from '@/store/taxonomoy-store';
import { sampleContexts } from '@/lib/sample-data';
import { showError } from '@/components/heads-up';
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from '@/components/ui/popover';
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
  onReportChange: (report: ReportDocument) => void;
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
  // Metadata for each page (width, height, page_number)
  const [pagesInfo, setPagesInfo] = useState<any[]>([]);
  // Loaded page data keyed by index
  const [loadedPages, setLoadedPages] = useState<Record<number, PageData>>({});
  // Tracks which pages are currently being fetched to avoid duplicate requests
  const [loadingPages, setLoadingPages] = useState<Record<number, boolean>>({});
  // Selection state: selected word indices and anchor for drag selection
  const [selectedWords, setSelectedWords] = useState<{
    pageIndex: number;
    indices: number[];
  } | null>(null);
  const [selectionAnchor, setSelectionAnchor] = useState<{
    pageIndex: number;
    wordIndex: number;
  } | null>(null);
  // Popover visibility state
  const [showPopover, setShowPopover] = useState(false);
  // Coordinates for positioning the recommendation popover
  const [popoverTriggerElement, setPopoverTriggerElement] = useState<{
    offsetTop: number;
    offsetLeft: number;
  } | null>(null);
  // Range of highlighted text and the text itself
  const [highlightRange, setHighlightRange] = useState<{
    blockId: string;
    startIndex: number;
    endIndex: number;
  } | null>(null);
  const [highlightedText, setHighlightedText] = useState('');
  // Page load progress (0..1)
  const [progress, setProgress] = useState(0);
  // Allow user to trigger loading all pages at once
  const [loadAllPages, setLoadAllPages] = useState(false);

  // Refs
  const containerRef = useRef<HTMLDivElement | null>(null);
  const pageRefs = useRef<(HTMLDivElement | null)[]>([]);
  const canvasRefs = useRef<(HTMLCanvasElement | null)[]>([]);

  /**
   * Load a page's image and words.  Skip if the page is already loaded or being
   * loaded.  Images are fetched as blobs and displayed immediately using
   * object URLs; conversion to data URLs happens asynchronously for caching.
   */
  const loadPage = useCallback(
    async (index: number) => {
      if (!pagesInfo || index < 0 || index >= pagesInfo.length) return;
      if (!report || !report.id) return;
      if (loadedPages[index] || loadingPages[index]) return;
      // Mark as loading
      setLoadingPages((prev) => ({ ...prev, [index]: true }));
      try {
        const pInfo = pagesInfo[index];
        const pageNumber = pInfo.page_number;
        // Fetch image as blob
        const imgRes = await axiosInstance.get(
          `/reports/${report.id}/pages/${pageNumber}/image`,
          {
            // Use a scale query to control resolution and reduce
            // payload size.  A scale of 1.0 corresponds to ~72 dpi.
            params: { scale: 1.0 },
            responseType: 'blob',
          }
        );
        const blob: Blob = imgRes.data;
        const objectUrl = URL.createObjectURL(blob);
        // Fetch words
        const wordsRes = await axiosInstance.get(
          `/reports/${report.id}/pages/${pageNumber}/words`
        );
        const wordData: WordEntry[] = wordsRes.data?.words || [];
        const pageWidth = wordsRes.data?.page_width || pInfo.width;
        const pageHeight = wordsRes.data?.page_height || pInfo.height;
        // Update state with loaded page
        setLoadedPages((prev) => ({
          ...prev,
          [index]: {
            pageNumber,
            width: pageWidth,
            height: pageHeight,
            imageUrl: objectUrl,
            words: wordData,
          },
        }));
        // Asynchronously convert to data URL and cache in sessionStorage
        if (typeof window !== 'undefined') {
          const cacheKey = `pdf-pages-partial-${report.id}`;
          const convertToDataUrl = async (b: Blob) => {
            return new Promise<string>((resolve, reject) => {
              const reader = new FileReader();
              reader.onloadend = () => resolve(reader.result as string);
              reader.onerror = reject;
              reader.readAsDataURL(b);
            });
          };
          convertToDataUrl(blob)
            .then((dataUrl) => {
              try {
                const existing = window.sessionStorage.getItem(cacheKey);
                const parsed = existing ? JSON.parse(existing) : {};
                parsed[index] = {
                  pageNumber,
                  width: pageWidth,
                  height: pageHeight,
                  imageUrl: dataUrl,
                  words: wordData,
                };
                window.sessionStorage.setItem(cacheKey, JSON.stringify(parsed));
              } catch {
                // ignore
              }
            })
            .catch(() => {});
        }
      } catch (err) {
        console.error(`Failed to load page ${index}`, err);
      } finally {
        setLoadingPages((prev) => {
          const copy = { ...prev };
          delete copy[index];
          return copy;
        });
      }
    },
    [pagesInfo, loadedPages, loadingPages, report]
  );
  // Ref to hold latest loadPage function to avoid stale closure in effects
  const loadPageRef = useRef(loadPage);
  useEffect(() => {
    loadPageRef.current = loadPage;
  }, [loadPage]);

  // Recommendation and feedback hooks
  const { mutate: fetchRecommendations, data: recommendations } =
    useRecommendations({
      mutationConfig: {},
    });
  const { mutate: sendFeedback } = usePostFeedback();
  const selectedTaxonomy = useTaxonomyStore((state) => state.selectedTaxonomy);
  const { setPendingConcept, selectedContextId, setSelection } =
    useTaggingStore();

  // Update progress whenever loaded pages or metadata changes
  useEffect(() => {
    if (!pagesInfo || pagesInfo.length === 0) {
      setProgress(1);
      return;
    }
    const loadedCount = Object.keys(loadedPages).length;
    const fraction = loadedCount / pagesInfo.length;
    setProgress(fraction);
  }, [loadedPages, pagesInfo]);

  // Remove loadAllPages effect. Loading all pages will be triggered directly

  // IntersectionObserver: lazy load pages as they enter the viewport
  useEffect(() => {
    if (!pagesInfo || pagesInfo.length === 0) return;
    const handleIntersect: IntersectionObserverCallback = (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const idxAttr = (entry.target as HTMLElement).getAttribute(
            'data-index'
          );
          const idx = idxAttr ? parseInt(idxAttr, 10) : NaN;
          if (!isNaN(idx)) {
            loadPageRef.current(idx);
            if (idx + 1 < pagesInfo.length) loadPageRef.current(idx + 1);
          }
        }
      });
    };
    const observer = new IntersectionObserver(handleIntersect, {
      root: null,
      rootMargin: '200px',
      threshold: 0.1,
    });
    pageRefs.current.forEach((el) => {
      if (el) observer.observe(el);
    });
    return () => {
      observer.disconnect();
    };
  }, [pagesInfo]);

  // Fetch pages metadata and preload first pages on report change
  useEffect(() => {
    // Reset state if report is not a PDF
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
    const fetchPagesInfo = async () => {
      try {
        // Try to read metadata from sessionStorage first
        let cachedInfo: any[] | null = null;
        if (typeof window !== 'undefined') {
          const key = `pdf-pages-info-${report.id}`;
          const cached = window.sessionStorage.getItem(key);
          if (cached) {
            try {
              cachedInfo = JSON.parse(cached);
            } catch {
              cachedInfo = null;
            }
          }
        }
        let info: any[];
        if (cachedInfo && cachedInfo.length > 0) {
          info = cachedInfo;
        } else {
          const infoRes = await axiosInstance.get(
            `/reports/${report.id}/pages_info`
          );
          info = infoRes.data?.pages || [];
          // Save to sessionStorage
          if (typeof window !== 'undefined') {
            try {
              window.sessionStorage.setItem(
                `pdf-pages-info-${report.id}`,
                JSON.stringify(info)
              );
            } catch {
              // ignore
            }
          }
        }
        setPagesInfo(info);
        // Attempt to restore loaded pages from sessionStorage
        if (typeof window !== 'undefined') {
          const cacheKey = `pdf-pages-partial-${report.id}`;
          const cached = window.sessionStorage.getItem(cacheKey);
          if (cached) {
            try {
              const parsed = JSON.parse(cached);
              const initialLoaded: Record<number, PageData> = {};
              Object.keys(parsed).forEach((idxStr) => {
                const idx = parseInt(idxStr, 10);
                const data = parsed[idxStr];
                if (data && data.imageUrl && data.words) {
                  initialLoaded[idx] = {
                    pageNumber: data.pageNumber,
                    width: data.width,
                    height: data.height,
                    imageUrl: data.imageUrl,
                    words: data.words,
                  };
                }
              });
              if (Object.keys(initialLoaded).length > 0) {
                setLoadedPages(initialLoaded);
              }
            } catch {
              // ignore
            }
          }
        }
        // Preload the first few pages unless loadAllPages is set
        if (info.length > 0) {
          const preloadCount = Math.min(
            loadAllPages ? info.length : 3,
            info.length
          );
          for (let i = 0; i < preloadCount; i++) {
            // Use ref to avoid re-creating effect dependency
            loadPageRef.current(i);
          }
        }
      } catch (err) {
        console.error('Failed to fetch PDF page info', err);
        setPagesInfo([]);
      }
    };
    fetchPagesInfo();
  }, [report?.id, report?.file_type, loadAllPages]);

  // Compute mapping of word indices to tags for each loaded page
  const taggedWordIndicesByPage = useMemo(() => {
    const result: Record<number, Set<number>> = {};
    if (!report?.blocks) return result;
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

  // Close popover and clear selection
  function closePopover() {
    setShowPopover(false);
    setHighlightRange(null);
    setPopoverTriggerElement(null);
    setSelectedWords(null);
    // Clear selection in global tagging store if available
    try {
      if (setSelection) {
        setSelection(null as any);
      }
    } catch {
      // ignore
    }
  }

  // Hit-test words at a given point on a canvas
  const getWordIndexAtPoint = useCallback(
    (pageIndex: number, x: number, y: number): number | null => {
      const page = loadedPages[pageIndex];
      if (!page) return null;
      for (let i = 0; i < page.words.length; i++) {
        const [bx0, by0, bx1, by1] = page.words[i].bbox;
        if (x >= bx0 && x <= bx1 && y >= by0 && y <= by1) {
          return i;
        }
      }
      return null;
    },
    [loadedPages]
  );

  // Begin a drag selection on canvas
  const handleCanvasMouseDown = (
    pageIndex: number,
    event: React.MouseEvent<HTMLCanvasElement>
  ) => {
    const canvas = canvasRefs.current[pageIndex];
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const wordIndex = getWordIndexAtPoint(pageIndex, x, y);
    if (wordIndex === null || isNaN(wordIndex)) return;
    event.preventDefault();
    closePopover();
    if (!loadedPages[pageIndex]) return;
    setSelectionAnchor({ pageIndex, wordIndex });
    setSelectedWords({ pageIndex, indices: [wordIndex] });
  };

  // Update selection during drag
  const handleCanvasMouseMove = (
    pageIndex: number,
    event: React.MouseEvent<HTMLCanvasElement>
  ) => {
    if (!selectionAnchor || selectionAnchor.pageIndex !== pageIndex) return;
    if (!loadedPages[pageIndex]) return;
    const canvas = canvasRefs.current[pageIndex];
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const wordIndex = getWordIndexAtPoint(pageIndex, x, y);
    if (wordIndex === null || isNaN(wordIndex)) return;
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

  // Finalise selection on mouse up
  const handleMouseUp = () => {
    if (!selectionAnchor || !selectedWords) {
      setSelectionAnchor(null);
      return;
    }
    const pageIndex = selectionAnchor.pageIndex;
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
    // Determine the block ID for this page.  In some cases (e.g. when
    // placeholder blocks have not been persisted), the block may be
    // undefined.  Avoid using an empty string as the block ID because
    // downstream components treat a falsy ID as "no block selected".  When
    // no block exists for a page, fall back to a synthetic ID based on
    // the page index (e.g. "page-0").  This ensures the tagging panel
    // receives a non-empty block identifier and the Add Tag button can
    // become enabled.
    const block = report.blocks?.[pageIndex];
    let blockId: string;
    if (block && block.id) {
      blockId = block.id;
    } else if (report.blocks && report.blocks[pageIndex]) {
      // If a block exists but has no ID (unlikely), use its index
      blockId = String(pageIndex);
    } else {
      // Fallback synthetic ID
      blockId = `page-${pageIndex}`;
    }
    const selectedText = sorted
      .map((i) => {
        const w = page.words[i];
        return w?.text || '';
      })
      .join(' ');
    onTextHighlight(blockId, selectedText, startIndex, endIndex);
    // Update global tagging store with current selection if available
    try {
      if (setSelection) {
        setSelection({
          blockId,
          startIndex,
          endIndex,
          selectedText,
        });
      }
    } catch (e) {
      // ignore if setSelection not available
    }
    setHighlightRange({ blockId, startIndex, endIndex });
    setHighlightedText(selectedText);
    // Compute popover position
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
    const container = document.getElementById(`pdf-page-${pageIndex}`);
    if (container) {
      const containerRect = container.getBoundingClientRect();
      const overlayWidth = 320;
      let candidateTop = containerRect.top + y1 + 4;
      let candidateLeft = containerRect.left + x0;
      if (candidateLeft + overlayWidth > window.innerWidth - 16) {
        candidateLeft = containerRect.left + x1 - overlayWidth;
        if (candidateLeft < 0) candidateLeft = 0;
      }
      setPopoverTriggerElement({
        offsetTop: candidateTop,
        offsetLeft: candidateLeft,
      });
    } else {
      setPopoverTriggerElement({ offsetTop: y1 + 4, offsetLeft: x0 });
    }
    // Fetch recommendations
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

  // Apply a tag from recommendation
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
        setPendingConcept(concept);
      }
      closePopover();
    };
    finalizeTag();
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

  // Build unified list of pages combining metadata and loaded content
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

  // Draw highlights onto canvases whenever loaded pages, selections or tags change
  useEffect(() => {
    const drawHighlights = (pageIndex: number) => {
      const canvas = canvasRefs.current[pageIndex];
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      const page = loadedPages[pageIndex];
      if (!page) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        return;
      }
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // Draw tagged words
      const tagSet = taggedWordIndicesByPage[pageIndex];
      if (tagSet) {
        ctx.fillStyle = 'rgba(0, 128, 255, 0.2)';
        page.words.forEach((word, idx) => {
          if (tagSet.has(idx)) {
            const [x0, y0, x1, y1] = word.bbox;
            ctx.fillRect(x0, y0, x1 - x0, y1 - y0);
          }
        });
      }
      // Draw selection on top
      if (selectedWords && selectedWords.pageIndex === pageIndex) {
        ctx.fillStyle = 'rgba(255, 255, 0, 0.4)';
        selectedWords.indices.forEach((idx) => {
          const word = page.words[idx];
          if (!word) return;
          const [x0, y0, x1, y1] = word.bbox;
          ctx.fillRect(x0, y0, x1 - x0, y1 - y0);
        });
      }
    };
    Object.keys(loadedPages).forEach((key) => {
      const idx = parseInt(key, 10);
      if (!isNaN(idx)) drawHighlights(idx);
    });
  }, [loadedPages, selectedWords, taggedWordIndicesByPage]);

  // Fallback: ensure at least the first page is loaded if progress is non-zero
  useEffect(() => {
    if (!pagesInfo || pagesInfo.length === 0) return;
    // If progress indicates some pages processed but no loaded page exists yet, load the first page(s).
    if (Object.keys(loadedPages).length === 0 && progress > 0) {
      const preloadCount = Math.min(3, pagesInfo.length);
      for (let i = 0; i < preloadCount; i++) {
        loadPageRef.current(i);
      }
    }
  }, [pagesInfo, loadedPages, progress]);

  const percent = Math.round(progress * 100);

  return (
    <div
      ref={containerRef}
      className='overflow-y-auto max-h-[80vh] px-4 py-2 space-y-8'
    >
      {/* Top progress bar (optional). Remove if using bottom-right indicator only */}
      {pagesInfo.length > 0 && progress < 1 && (
        <div className='flex flex-col items-center justify-center mb-4'>
          <p className='text-sm text-muted-foreground'>
            Loading PDF… {percent}%
          </p>
          <div className='w-64 bg-muted/20 rounded-full h-2 overflow-hidden'>
            <div
              className='bg-primary h-2 rounded-full transition-all'
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
          {/* Canvas overlay for highlighting and selection */}
          {page.imageUrl && page.words.length > 0 && (
            <canvas
              ref={(el) => {
                canvasRefs.current[pIdx] = el;
              }}
              width={page.width}
              height={page.height}
              style={{ position: 'absolute', top: 0, left: 0, cursor: 'text' }}
              onMouseDown={(e) => handleCanvasMouseDown(pIdx, e)}
              onMouseMove={(e) => handleCanvasMouseMove(pIdx, e)}
            />
          )}
          {/* Recommendation popover */}
          {page.imageUrl &&
            showPopover &&
            selectedWords?.pageIndex === pIdx &&
            popoverTriggerElement && (
              <Popover
                open={showPopover && selectedWords?.pageIndex === pIdx}
                onOpenChange={(open) => {
                  setShowPopover(open);
                  if (!open) closePopover();
                }}
              >
                <PopoverTrigger asChild>
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
                      : { resize: 'both', overflow: 'auto' }
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
                        {recommendations?.results?.map((item: any) => (
                          <Button
                            key={item.tag}
                            variant='ghost'
                            className='relative justify-start w-full h-auto p-3 py-2 text-left hover:bg-muted/50 group'
                            onClick={() => applyTag(item)}
                          >
                            <div className='space-y-1'>
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
      {/* Bottom-right circular progress indicator */}
      {pagesInfo.length > 0 && progress < 1 && (
        <div className='fixed bottom-4 right-4 z-50 pointer-events-none'>
          <div className='relative w-12 h-12'>
            <div
              className='absolute inset-0 rounded-full border-2 border-gray-300'
              style={{
                background: `conic-gradient(rgb(99,102,241) 0deg ${percent * 3.6}deg, rgba(229,231,235,0.5) ${percent * 3.6}deg 360deg)`,
              }}
            />
            <div className='absolute inset-0 flex items-center justify-center text-xs font-semibold text-gray-700'>
              {percent}%
            </div>
          </div>
        </div>
      )}
      {/* Load all pages button */}
      {pagesInfo.length > 0 && progress < 1 && !loadAllPages && (
        <div className='fixed bottom-4 left-4 z-50'>
          <button
            onClick={() => {
              setLoadAllPages(true);
              // Trigger load for all remaining pages immediately
              if (pagesInfo && pagesInfo.length > 0) {
                for (let i = 0; i < pagesInfo.length; i++) {
                  loadPageRef.current(i);
                }
              }
            }}
            className='px-3 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md shadow-md hover:bg-indigo-700'
          >
            Load all pages
          </button>
        </div>
      )}
    </div>
  );
}
