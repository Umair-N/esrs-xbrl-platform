// Dynamic page for loading and editing a previously saved canvas. The
// ``id`` parameter corresponds to a record in the backend's
// ``canvas_states`` table (mounted under ``/reports/canvas``). When
// visiting ``/reports/[id]`` the canvas is fetched and the editor is
// hydrated without reprocessing the original PDF. Users can continue
// tagging and even save a new copy which will generate its own unique
// identifier.

'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import {
  ResizablePanelGroup,
  ResizablePanel,
  ResizableHandle,
} from '@/components/ui/resizable';
import { TextEditor } from '@/components/editor/text-editor';
import { PdfEditor, type PdfEditorHandle } from '@/components/editor/pdf-editor';
import { TaggingPanel } from '@/components/editor/tagging-panel';
import { TaggedFactsList } from '@/components/editor/tagged-facts-list';
import { SaveExportPanel } from '@/components/editor/export';
import type { ReportDocument } from '@/types/report';
import type { ReportBlock, XbrlTag } from '@/types/report';
import {
  Tags,
  Save,
  Settings,
  Upload,
  BookOpen,
  Sparkles,
  GripVertical,
  MoreHorizontal,
  Loader2,
  FileText,
} from 'lucide-react';
import { axiosInstance } from '@/lib/axios';
import { toast } from 'sonner';

// Reuse the block merging helper for text‑based reports. Saved canvases
// should already be in the correct shape, but if a record was created
// from a non‑PDF source and blocks were not merged prior to saving,
// merging here ensures consistency.
function mergeReportBlocks(report: ReportDocument): ReportDocument {
  if (!report.blocks || report.blocks.length <= 1) {
    return report;
  }
  let combinedContent = '';
  const combinedTags: XbrlTag[] = [];
  let offset = 0;
  report.blocks.forEach((block, idx) => {
    combinedContent += block.content;
    block.tags?.forEach((tag) => {
      const start = tag.startIndex ?? 0;
      const end = tag.endIndex ?? block.content.length;
      combinedTags.push({
        ...tag,
        startIndex: start + offset,
        endIndex: end + offset,
      });
    });
    offset += block.content.length;
    if (idx < report.blocks.length - 1) {
      combinedContent += '\n\n';
      offset += 2;
    }
  });
  const combinedBlock: ReportBlock = {
    id: `combined-block-${report.id}`,
    content: combinedContent,
    type: report.blocks[0].type,
    tags: combinedTags,
  };
  return {
    ...report,
    blocks: [combinedBlock],
  };
}

export default function CanvasPage() {
  const params = useParams();
  const router = useRouter();
  const [report, setReport] = useState<ReportDocument | null>(null);
  const [selectedBlockId, setSelectedBlockId] = useState<string | null>(null);
  const [highlightedText, setHighlightedText] = useState<{
    text: string;
    startIndex: number;
    endIndex: number;
  } | null>(null);
  const [isTaggedFactsOpen, setIsTaggedFactsOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  // Ref to interact with the PdfEditor component. Enables loading all pages
  // and extracting page images for persistence.
  const pdfEditorRef = useRef<PdfEditorHandle | null>(null);

  // Track the ID of the current canvas for updates. This ref is set
  // once the page parameter is available and persists across renders. If
  // null, auto‑saves will create a new canvas record on the backend.
  const canvasIdRef = useRef<string | null>(null);
  // Hold the extracted pages so that auto‑saves can reuse the same
  // images instead of re-extracting them on every change. When the
  // user manually saves (handles Save Report), this ref is updated.
  const pagesRef = useRef<any[] | undefined>(undefined);
  // Skip auto‑saving on the first render to avoid saving before the
  // report has been loaded from the backend. This ref flips after
  // initial mount.
  const skipInitialAutoSave = useRef(true);
  // Store timeout ID for debouncing auto saves.
  const autoSaveTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Fetch the saved canvas based on the dynamic route parameter. The
  // backend returns an object with an ``id`` and the serialized
  // report under ``data``. The data is deserialized for the editor.
  useEffect(() => {
    const { id } = params as { id?: string };
    // Capture the canvas ID into a ref for auto‑save updates
    if (id) {
      canvasIdRef.current = id;
    }
    if (!id) return;
    (async () => {
      try {
        const res = await axiosInstance.get(`/reports/canvas/${id}`);
        const resp = res.data;
        const doc: ReportDocument = resp.data;
        // If the report isn't a PDF, merge its blocks for consistency
        const isPdf = doc.file_type?.toLowerCase().includes('pdf');
        const restored = isPdf ? doc : mergeReportBlocks(doc);
        if (Array.isArray((doc as any)?.pages)) {
          pagesRef.current = (doc as any).pages;
        } else {
          pagesRef.current = undefined;
        }
        setReport(restored);
        if (restored.blocks && restored.blocks.length > 0) {
          setSelectedBlockId(restored.blocks[0].id);
        }
      } catch (err) {
        console.error('Failed to fetch canvas', err);
        toast.error('Failed to load saved report');
        router.replace('/upload');
      }
    })();
  }, [params, router]);

  const handleBlockSelect = (blockId: string) => {
    setSelectedBlockId(blockId);
    setHighlightedText(null);
  };

  const handleTextHighlight = (
    blockId: string,
    selectedText: string,
    startIndex: number,
    endIndex: number
  ) => {
    setHighlightedText({ text: selectedText, startIndex, endIndex });
  };

  /**
   * Save the current report. When editing an existing canvas the record
   * is updated in place; otherwise a brand new canvas is created and the
   * user is redirected to that ID.
   */
  const handleSaveSession = async () => {
    if (!report) return;
    setIsSaving(true);
    try {
      // Ensure all pages are loaded and extract their images. The PdfEditor
      // component exposes imperative methods via its ref.
      const editor = pdfEditorRef.current;
      let pages: any[] | undefined = pagesRef.current;
      if (editor) {
        editor.loadAllPages();
        while (editor.getProgress() < 1) {
          // eslint-disable-next-line no-await-in-loop
          await new Promise((resolve) => setTimeout(resolve, 200));
        }
        pages = await editor.extractPages();
      }
      const payload = {
        name: report.title ?? 'Untitled report',
        data: {
          ...report,
          ...(pages ? { pages } : {}),
        },
        report_id: report.id,
      };
      const existingCanvasId = canvasIdRef.current;
      if (existingCanvasId) {
        await axiosInstance.put(`/reports/canvas/${existingCanvasId}`, payload);
        pagesRef.current = pages ?? pagesRef.current;
        toast.success('Report saved successfully');
      } else {
        const res = await axiosInstance.post('/reports/canvas', payload);
        const newId = res.data?.id;
        if (newId) {
          canvasIdRef.current = newId;
          pagesRef.current = pages;
          toast.success('Report saved successfully');
          router.push(`/reports/${newId}`);
        } else {
          toast.error('Failed to save report');
        }
      }
    } catch (err) {
      console.error('Error saving report:', err);
      toast.error('Failed to save report');
    } finally {
      setIsSaving(false);
    }
  };

  const handleReportChange = (updatedReport: ReportDocument) => {
    setReport(updatedReport);
  };

  // Debounced auto‑save. Whenever the report state changes after the
  // initial load, schedule a save to the backend. If a canvas ID is
  // already known (i.e. the user is editing an existing saved report),
  // the update endpoint is called. Otherwise a new canvas is created.
  useEffect(() => {
    if (!report) return;
    // Skip the initial effect run after mount
    if (skipInitialAutoSave.current) {
      skipInitialAutoSave.current = false;
      return;
    }
    // Clear any pending auto save
    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
    }
    autoSaveTimeoutRef.current = setTimeout(async () => {
      try {
        const editor = pdfEditorRef.current;
        // Use previously extracted pages if available; otherwise
        // extract pages if all pages are loaded. This avoids
        // repeatedly converting images to data URLs. If pages are
        // partially loaded the report will still be saved without the
        // pages field. Users can manually save to capture all pages.
        let pages: any[] | undefined = pagesRef.current;
        if (!pages && editor && editor.getProgress() >= 1) {
          pages = await editor.extractPages();
          pagesRef.current = pages;
        }
        const payload = {
          name: report.title ?? 'Untitled report',
          data: {
            ...report,
            ...(pages ? { pages } : {}),
          },
          report_id: report.id,
        };
        if (canvasIdRef.current) {
          // Update existing canvas
          await axiosInstance.put(`/reports/canvas/${canvasIdRef.current}`, payload);
          if (pages) {
            pagesRef.current = pages;
          }
        } else {
          // Create a new canvas record (will not redirect)
          const res = await axiosInstance.post('/reports/canvas', payload);
          const newId = res.data?.id;
          if (newId) {
            canvasIdRef.current = newId;
            if (pages) {
              pagesRef.current = pages;
            }
          }
        }
        toast.success('Report auto‑saved');
      } catch (err) {
        console.error('Auto save failed:', err);
        toast.error('Failed to auto‑save');
      }
    }, 2000);
    // Cleanup function clears timeout on unmount or when report changes
    return () => {
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
      }
    };
  }, [report]);

  const handleNewDocument = () => {
    router.push('/upload');
    setIsMenuOpen(false);
  };

  // Navigate to the reports listing page and close the popover menu. Allows
  // users to view all of their saved reports from within an open report.
  const handleViewReports = () => {
    router.push('/reports');
    setIsMenuOpen(false);
  };

  if (!report) {
    // While report is loading or being redirected, return null to avoid flash
    return null;
  }

  const totalTags = report.blocks.reduce(
    (count, block) => count + (block.tags?.length || 0),
    0
  );

  return (
    <div
      className='bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex flex-col'
      style={{ height: 'calc(100vh - 80px)' }}
    >
      <ResizablePanelGroup
        direction='horizontal'
        className='flex-1 bg-white/50 dark:bg-slate-800/50 backdrop-blur-sm'
      >
        <ResizablePanel defaultSize={50} minSize={40}>
          <Card className='h-full shadow-none border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm flex flex-col rounded-none overflow-hidden'>
            <CardHeader className='flex-shrink-0 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 pb-2 pt-2 pl-3'>
              <CardTitle className='flex items-center gap-3 text-lg'>
                <div className='p-2 bg-blue-500 rounded-lg'>
                  <BookOpen className='h-5 w-5 text-white' />
                </div>
                <div>
                  <span className='bg-gradient-to-r from-blue-700 to-indigo-700 dark:from-blue-300 dark:to-indigo-300 bg-clip-text text-transparent p-0'>
                    Document Content
                  </span>
                  <p className='text-sm text-muted-foreground font-normal mt-1'>
                    Select text to add tags
                  </p>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent className='flex-1 p-0 mt-2 overflow-hidden'>
              {report.file_type?.toLowerCase().includes('pdf') ? (
                <PdfEditor
                  ref={pdfEditorRef}
                  report={report}
                  onReportChange={setReport}
                  // When selecting a word in a PDF, update the selected block
                  // and the highlighted text. The block ID corresponds to the
                  // page index, preserving correct tag alignment.
                  onTextHighlight={(blockId, text, start, end) => {
                    setSelectedBlockId(blockId);
                    setHighlightedText({
                      text,
                      startIndex: start,
                      endIndex: end,
                    });
                  }}
                />
              ) : (
                <TextEditor
                  report={report}
                  selectedBlockId={selectedBlockId}
                  onBlockSelect={handleBlockSelect}
                  onReportChange={setReport}
                  onTextHighlight={handleTextHighlight}
                />
              )}
            </CardContent>
          </Card>
        </ResizablePanel>

        <ResizableHandle
          withHandle
          className='bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors'
        >
          <div className='flex items-center justify-center h-full'>
            <GripVertical className='h-4 w-4 text-slate-500' />
          </div>
        </ResizableHandle>

        <ResizablePanel defaultSize={50} minSize={30}>
          <Card className='h-full shadow-none border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm flex flex-col rounded-none overflow-hidden'>
            <CardHeader className='flex-shrink-0 bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-950/20 dark:to-green-950/20 pb-1 pt-1 pl-3'>
              <CardTitle className='flex items-center justify-between gap-3 text-lg'>
                <div className='flex items-center gap-3'>
                  <div className='p-2 bg-emerald-500 rounded-lg'>
                    <Tags className='h-5 w-5 text-white' />
                  </div>
                  <div>
                    <span className='bg-gradient-to-r from-emerald-700 to-green-700 dark:from-emerald-300 dark:to-green-300 bg-clip-text text-transparent p-0'>
                      XBRL Tagging Tools
                    </span>
                    <p className='text-sm text-muted-foreground font-normal mt-1'>
                      Tag selected text with XBRL elements
                    </p>
                  </div>
                </div>
                <div className='flex items-center gap-2'>
                  {/* Save Report Button */}
                  <Button
                    variant='outline'
                    size='sm'
                    onClick={handleSaveSession}
                    disabled={isSaving}
                    className='gap-2 h-9 px-3 hover:bg-green-50 hover:border-green-300 dark:hover:bg-green-900/20 transition-colors flex-shrink-0'
                  >
                    {isSaving ? (
                      <Loader2 className='h-4 w-4 animate-spin' />
                    ) : (
                      <Save className='h-4 w-4' />
                    )}
                    {isSaving ? 'Saving...' : 'Save Report'}
                  </Button>

                  {/* View Tagged Facts Dialog */}
                  <Dialog
                    open={isTaggedFactsOpen}
                    onOpenChange={setIsTaggedFactsOpen}
                  >
                    <DialogTrigger asChild>
                      <Button
                        variant='outline'
                        size='sm'
                        className='gap-2 h-9 px-4 hover:bg-purple-50 hover:border-purple-300 dark:hover:bg-purple-900/20 transition-colors flex-shrink-0'
                      >
                        <Sparkles className='h-4 w-4' />
                        View Tagged Facts
                        {totalTags > 0 && (
                          <Badge
                            variant='secondary'
                            className='ml-1 bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
                          >
                            {totalTags}
                          </Badge>
                        )}
                      </Button>
                    </DialogTrigger>
                    <DialogContent className='max-w-4xl max-h-[80vh] overflow-hidden'>
                      <DialogHeader>
                        <DialogTitle className='flex items-center gap-3'>
                          <div className='p-2 bg-purple-500 rounded-lg'>
                            <Sparkles className='h-5 w-5 text-white' />
                          </div>
                          <div>
                            <span className='bg-gradient-to-r from-purple-700 to-pink-700 dark:from-purple-300 dark:to-pink-300 bg-clip-text text-transparent'>
                              Tagged Facts
                            </span>
                            {totalTags > 0 && (
                              <Badge
                                variant='secondary'
                                className='ml-2 bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
                              >
                                {totalTags} facts
                              </Badge>
                            )}
                          </div>
                        </DialogTitle>
                      </DialogHeader>
                      <div className='mt-4 h-[60vh] overflow-y-auto'>
                        <TaggedFactsList
                          report={report}
                          onBlockSelect={(blockId: string) => {
                            setSelectedBlockId(blockId);
                            setHighlightedText(null);
                            setIsTaggedFactsOpen(false);
                          }}
                          onReportChange={handleReportChange}
                        />
                      </div>
                    </DialogContent>
                  </Dialog>

                  {/* Menu Popover: only show New Document; saved sessions are
                      accessed via their URLs so there is no listing
                      available */}
                  <Popover open={isMenuOpen} onOpenChange={setIsMenuOpen}>
                    <PopoverTrigger asChild>
                      <Button
                        variant='outline'
                        size='sm'
                        className='gap-2 h-9 px-3 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors flex-shrink-0'
                      >
                        <MoreHorizontal className='h-4 w-4' />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className='w-56 p-0' align='end'>
                      <div className='p-1'>
                        <Button
                          variant='ghost'
                          size='sm'
                          onClick={handleNewDocument}
                          className='w-full justify-start gap-2 h-9'
                        >
                          <Upload className='h-4 w-4' />
                          New Document
                        </Button>
                        <Button
                          variant='ghost'
                          size='sm'
                          onClick={handleViewReports}
                          className='w-full justify-start gap-2 h-9'
                        >
                          <FileText className='h-4 w-4' />
                          View Reports
                        </Button>
                      </div>
                    </PopoverContent>
                  </Popover>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent className='flex-1 p-0 min-h-0 mt-1'>
              <Tabs
                defaultValue='tagging'
                className='w-full h-full flex flex-col'
              >
                <TabsList className='grid w-full grid-cols-2 mx-4 my-2  bg-slate-100 dark:bg-slate-700 flex-shrink-0'>
                  <TabsTrigger
                    value='tagging'
                    className='gap-2 text-xs data-[state=active]:bg-emerald-500 data-[state=active]:text-white'
                  >
                    <Tags className='h-3 w-3' />
                    Tag
                  </TabsTrigger>
                  <TabsTrigger
                    value='export'
                    className='gap-2 text-xs data-[state=active]:bg-blue-500 data-[state=active]:text-white'
                  >
                    <Save className='h-3 w-3' />
                    Export
                  </TabsTrigger>
                </TabsList>
                <TabsContent
                  value='tagging'
                  className='mx-2 mt-0 mb-0 flex-1 min-h-0'
                >
                  <div className='h-full overflow-y-auto'>
                    <TaggingPanel
                      report={report}
                      selectedBlockId={selectedBlockId}
                      highlightedText={highlightedText}
                      onReportChange={setReport}
                    />
                  </div>
                </TabsContent>
                <TabsContent
                  value='export'
                  className='mx-4 mt-0 mb-4 flex-1 min-h-0'
                >
                  <div className='h-full overflow-y-auto'>
                    {/* SaveExportPanel still supports exporting XBRL. The onSave handler is a no‑op
                        because saving sessions is handled via handleSaveSession above. */}
                    <SaveExportPanel report={report} onSave={() => {}} />
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
}
