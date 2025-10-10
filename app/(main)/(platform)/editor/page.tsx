// 'EditorPage' is dedicated to editing and tagging the loaded report. It
// expects the report to already be present in localStorage under
// 'xbrl-editor-session'. If no report exists, it redirects the user to the
// upload page. Users can navigate back to the sessions list or start a new
// document via buttons in the header.

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
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
import { PdfEditor } from '@/components/editor/pdf-editor';
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
} from 'lucide-react';
import { axiosInstance } from '@/lib/axios';
import { toast } from 'sonner';

/**
 * Merge multiple blocks of a report into a single block. This combines the
 * content of all blocks with double newline separators and adjusts the start
 * and end indices of each tag to account for the offset in the merged content.
 */
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

export default function EditorPage() {
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

  // Load the report from localStorage on mount. If none exists, redirect.
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const saved = localStorage.getItem('xbrl-editor-session');
    if (saved) {
      try {
        const parsed: ReportDocument = JSON.parse(saved);
        // Determine if the report was created from a PDF. If so,
        // avoid merging blocks so that each page remains a separate
        // block and character indices stay aligned. Otherwise merge
        // blocks by default.
        const isPdf = parsed.file_type?.toLowerCase().includes('pdf');
        const restored = isPdf ? parsed : mergeReportBlocks(parsed);
        setReport(restored);
        if (restored.blocks && restored.blocks.length > 0) {
          setSelectedBlockId(restored.blocks[0].id);
        }
      } catch (err) {
        console.error('Failed to parse saved report', err);
        localStorage.removeItem('xbrl-editor-session');
        router.replace('/upload');
      }
    } else {
      // no report saved; redirect to upload
      router.replace('/upload');
    }
  }, [router]);

  // Persist changes to the report
  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (report) {
      try {
        localStorage.setItem('xbrl-editor-session', JSON.stringify(report));
      } catch (err) {
        console.error('Failed to save report', err);
      }
    }
  }, [report]);

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

  const handleSave = async (savedReport: ReportDocument) => {
    try {
      let sessionName =
        prompt(
          'Enter a name for this session',
          savedReport.title ?? 'Untitled session'
        ) ||
        savedReport.title ||
        'Untitled session';
      if (!sessionName) {
        sessionName = savedReport.title || 'Untitled session';
      }
      const sessionId = localStorage.getItem('xbrl-session-id');
      if (sessionId) {
        await axiosInstance.put(`/sessions/${sessionId}`, {
          name: sessionName,
          data: savedReport,
        });
        toast.success('Session updated successfully');
      } else {
        const res = await axiosInstance.post('/sessions', {
          name: sessionName,
          data: savedReport,
        });
        const newId = res.data?.id;
        if (newId) {
          localStorage.setItem('xbrl-session-id', newId);
        }
        toast.success('Session saved successfully');
      }
    } catch (err) {
      console.error('Failed to save session', err);
      toast.error('Failed to save session');
    }
  };

  const handleSaveSession = async () => {
    if (!report) return;

    setIsSaving(true);
    try {
      const updatedReport = {
        ...report,
        updatedAt: new Date().toISOString(),
      };

      // Save to localStorage with report ID
      localStorage.setItem(
        `report_${report.id}`,
        JSON.stringify(updatedReport)
      );

      // Update the current session
      setReport(updatedReport);

      // Also call the existing handleSave function for API persistence
      await handleSave(updatedReport);

      console.log('ESRS Report saved successfully');
    } catch (error) {
      console.error('Error saving report:', error);
      toast.error('Failed to save session');
    } finally {
      setIsSaving(false);
    }
  };

  const handleReportChange = (updatedReport: ReportDocument) => {
    setReport(updatedReport);
  };

  const handleNewDocument = () => {
    router.push('/upload');
    setIsMenuOpen(false);
  };

  const handleViewSessions = () => {
    router.push('/sessions');
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
                  {/* Save Session Button */}
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
                    {isSaving ? 'Saving...' : 'Save Session'}
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

                  {/* Menu Popover */}
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
                          onClick={handleViewSessions}
                          className='w-full justify-start gap-2 h-9'
                        >
                          <BookOpen className='h-4 w-4' />
                          Sessions
                        </Button>
                        <Button
                          variant='ghost'
                          size='sm'
                          onClick={handleNewDocument}
                          className='w-full justify-start gap-2 h-9'
                        >
                          <Upload className='h-4 w-4' />
                          New Document
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
                    <SaveExportPanel report={report} onSave={handleSave} />
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
