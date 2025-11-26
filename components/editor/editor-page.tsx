'use client';

import { useState, useEffect } from 'react';
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
  ResizablePanelGroup,
  ResizablePanel,
  ResizableHandle,
} from '@/components/ui/resizable';
import { FileUploader } from '@/components/editor/file-uploader';
import { TextEditor } from '@/components/editor/text-editor';
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
  Bot,
  Zap,
} from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { useTaggingStore } from '@/store/tagging-store';
import { axiosInstance } from '@/lib/axios';
import { toast } from 'sonner';

// Lightweight definition of a saved session summary returned from the backend.
interface SessionSummary {
  id: string;
  name: string;
  created_at?: string;
  updated_at?: string;
}

/**
 * Merge multiple blocks of a report into a single block. This combines the
 * content of all blocks with double newline separators and adjusts the start
 * and end indices of each tag to account for the offset in the merged content.
 * If the report already contains a single block, it is returned unchanged.
 *
 * @param report The original report document
 * @returns A new report document with a single merged block
 */
function mergeReportBlocks(report: ReportDocument): ReportDocument {
  // If there is only one block, return as is
  if (!report.blocks || report.blocks.length <= 1) {
    return report;
  }
  let combinedContent = '';
  const combinedTags: XbrlTag[] = [];
  let offset = 0;
  report.blocks.forEach((block, idx) => {
    combinedContent += block.content;
    // Adjust tags for this block
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
    // Add two newlines between blocks except after the last block
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
  const [report, setReport] = useState<ReportDocument | null>(null);
  const [selectedBlockId, setSelectedBlockId] = useState<string | null>(null);
  const [highlightedText, setHighlightedText] = useState<{
    text: string;
    startIndex: number;
    endIndex: number;
  } | null>(null);
  const [isTaggedFactsOpen, setIsTaggedFactsOpen] = useState(false);

  // List of saved sessions for the current user. `null` means they haven't been loaded yet.
  const [sessions, setSessions] = useState<SessionSummary[] | null>(null);
  const [loadingSessions, setLoadingSessions] = useState(false);

  // Agent mode state from global store
  const agentMode = useTaggingStore((state) => state.agentMode);
  const setAgentModeEnabled = useTaggingStore(
    (state) => state.setAgentModeEnabled
  );
  const setAgentModeAutoApply = useTaggingStore(
    (state) => state.setAgentModeAutoApply
  );

  /**
   * When the editor first mounts, attempt to restore any previously saved
   * session from localStorage. If a saved report exists and there is no
   * report currently loaded, update the editor state with the saved
   * document and select its first block (if available).
   */
  useEffect(() => {
    // Only execute on client side
    if (typeof window === 'undefined') return;
    // Do not overwrite a report that has already been loaded via the file uploader
    if (report) return;
    try {
      const saved = localStorage.getItem('xbrl-editor-session');
      if (saved) {
        const parsed: ReportDocument = JSON.parse(saved);
        // Always merge the report blocks on load so the editor
        // consistently displays a single combined block. This also
        // updates tag indices when the original report contained
        // multiple blocks.
        const merged = mergeReportBlocks(parsed);
        setReport(merged);
        if (merged.blocks && merged.blocks.length > 0) {
          setSelectedBlockId(merged.blocks[0].id);
        }
      }
    } catch (err) {
      console.error('Failed to load saved editor session:', err);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /**
   * Persist the current report to localStorage whenever it changes. This
   * ensures that navigating away from the editor does not cause the
   * in-memory editing session to be lost. Only run on the client when a
   * report is present.
   */
  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (report) {
      try {
        localStorage.setItem('xbrl-editor-session', JSON.stringify(report));
      } catch (err) {
        console.error('Failed to save editor session:', err);
      }
    }
  }, [report]);

  // Fetch saved sessions when no report is loaded. This effect runs once on mount
  // and whenever the report changes to null. Errors are surfaced via toast.
  useEffect(() => {
    const fetchSessions = async () => {
      if (sessions !== null || report) return;
      setLoadingSessions(true);
      try {
        const res = await axiosInstance.get<SessionSummary[]>('/sessions');
        setSessions(res.data);
      } catch (err: any) {
        console.error('Failed to fetch sessions', err);
        toast.error('Failed to load saved sessions');
        setSessions([]);
      } finally {
        setLoadingSessions(false);
      }
    };
    if (!report) {
      fetchSessions();
    }
    // We deliberately leave `sessions` and `report` out of the dependency array to avoid
    // unnecessary re-fetching. eslint-disable-next-line is used to silence warnings.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [report]);

  const handleReportLoaded = (newReport: ReportDocument) => {
    // Merge multiple blocks into a single block to avoid rendering
    // separate scrollable sections for each block. This preserves the
    // original tag positions by adjusting their indices and combines
    // content with double newlines. If the report already has a
    // single block, mergeReportBlocks returns it unchanged.
    const mergedReport = mergeReportBlocks(newReport);
    setReport(mergedReport);
    if (mergedReport.blocks.length > 0) {
      setSelectedBlockId(mergedReport.blocks[0].id);
    }
  };

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
      // Prompt the user for a name. Use the report title as a sensible default.
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

  const handleReportChange = (updatedReport: ReportDocument) => {
    setReport(updatedReport);
  };

  // Load an existing session by its ID. The report state and localStorage are updated.
  const handleSessionSelect = async (sessionId: string) => {
    try {
      const res = await axiosInstance.get(`/sessions/${sessionId}`);
      const session = res.data;
      const reportData = session?.data as ReportDocument;
      // Persist sessionId so future saves update instead of creating new
      localStorage.setItem('xbrl-session-id', sessionId);
      // Merge blocks to maintain consistency
      const merged = mergeReportBlocks(reportData);
      setReport(merged);
      if (merged.blocks && merged.blocks.length > 0) {
        setSelectedBlockId(merged.blocks[0].id);
      }
      // Persist to local storage as well
      localStorage.setItem('xbrl-editor-session', JSON.stringify(merged));
    } catch (err) {
      console.error('Failed to load session', err);
      toast.error('Failed to load session');
    }
  };

  // Upload state - no document loaded
  if (!report) {
    // If sessions are still loading, display a loading indicator
    if (sessions === null || loadingSessions) {
      return (
        <div
          className='flex-1 flex items-center justify-center mt-1 mb-1'
          style={{ height: 'calc(100vh - 80px)' }}
        >
          <p className='text-sm text-muted-foreground'>
            Loading your sessions…
          </p>
        </div>
      );
    }
    // Present a list of saved sessions, if any exist
    if (sessions.length > 0) {
      return (
        <div
          className='flex-1 flex items-center justify-center mt-1 mb-1'
          style={{ height: 'calc(100vh - 80px)' }}
        >
          <div className='w-full max-w-4xl space-y-4'>
            <Card className='border shadow-none bg-white/80 dark:bg-slate-800/80'>
              <CardHeader>
                <CardTitle className='flex items-center justify-between text-lg'>
                  <span>Your Sessions</span>
                  <Button
                    variant='outline'
                    size='sm'
                    onClick={() => {
                      // Clear any persisted session state and show file uploader
                      localStorage.removeItem('xbrl-editor-session');
                      localStorage.removeItem('xbrl-session-id');
                      setReport(null);
                      setSelectedBlockId(null);
                      // Set sessions to an empty array rather than null to avoid
                      // triggering the "Loading your sessions…" state. When
                      // sessions is null the effect hook skips fetching due to a
                      // stale closure and the UI shows loading indefinitely. Use
                      // an empty list to indicate no saved sessions and fall back
                      // to the file uploader.
                      setSessions([]);
                    }}
                  >
                    New Document
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className='space-y-2'>
                {sessions.map((s) => (
                  <div
                    key={s.id}
                    className='flex items-center justify-between p-2 border rounded cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-700'
                    onClick={() => handleSessionSelect(s.id)}
                  >
                    <div>
                      <p className='font-medium'>{s.name}</p>
                      <p className='text-xs text-muted-foreground'>
                        Last updated&nbsp;
                        {s.updated_at
                          ? new Date(s.updated_at).toLocaleString()
                          : 'n/a'}
                      </p>
                    </div>
                    <Button
                      variant='outline'
                      size='sm'
                      onClick={(e) => {
                        e.stopPropagation();
                        handleSessionSelect(s.id);
                      }}
                    >
                      Open
                    </Button>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      );
    }
    // Otherwise, there are no sessions. Show the file uploader.
    return (
      <div
        className='flex-1 flex items-center justify-center mt-1 mb-1'
        style={{ height: 'calc(100vh - 80px)' }}
      >
        <div className='w-full max-w-4xl'>
          <FileUploader onReportLoaded={handleReportLoaded} />
        </div>
      </div>
    );
  }

  const totalTags = report.blocks.reduce(
    (count, block) => count + (block.tags?.length || 0),
    0
  );
  const taggedBlocks = report.blocks.filter(
    (block) => block.tags && block.tags.length > 0
  ).length;
  const completionRate =
    report.blocks.length > 0
      ? Math.round((taggedBlocks / report.blocks.length) * 100)
      : 0;

  return (
    <div
      className='bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex flex-col'
      style={{ height: 'calc(100vh - 80px)' }}
    >
      {/* Main Content with Resizable Panels - NO PADDING */}
      <ResizablePanelGroup
        direction='horizontal'
        className='flex-1 bg-white/50 dark:bg-slate-800/50 backdrop-blur-sm'
      >
        {/* Left Panel - Document Editor */}
        <ResizablePanel defaultSize={50} minSize={40}>
          <Card className='h-full shadow-none border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm flex flex-col rounded-none'>
            <CardHeader className='flex-shrink-0 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 pb-1 pt-1 pl-3'>
              <CardTitle className='flex items-center justify-between gap-3 text-lg'>
                <div className='flex items-center gap-3'>
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
                </div>
                {/* Agent Mode Toggle */}
                <div className='flex items-center gap-2'>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant={agentMode.enabled ? 'default' : 'outline'}
                        size='sm'
                        className={`gap-2 h-9 px-4 transition-colors flex-shrink-0 ${
                          agentMode.enabled
                            ? 'bg-gradient-to-r from-violet-500 to-purple-500 hover:from-violet-600 hover:to-purple-600 text-white border-0'
                            : 'hover:bg-violet-50 hover:border-violet-300 dark:hover:bg-violet-900/20'
                        }`}
                      >
                        <Bot className='h-4 w-4' />
                        AI Agent
                        {agentMode.enabled && (
                          <Badge
                            variant='secondary'
                            className='ml-1 bg-white/20 text-white text-xs'
                          >
                            ON
                          </Badge>
                        )}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className='w-72' align='end'>
                      <div className='space-y-4'>
                        <div className='flex items-center gap-2'>
                          <div className='p-2 bg-gradient-to-r from-violet-500 to-purple-500 rounded-lg'>
                            <Bot className='h-4 w-4 text-white' />
                          </div>
                          <div>
                            <h4 className='font-medium text-sm'>
                              AI Agent Mode
                            </h4>
                            <p className='text-xs text-muted-foreground'>
                              Automatic XBRL tagging with NER
                            </p>
                          </div>
                        </div>
                        <div className='space-y-3'>
                          <div className='flex items-center justify-between'>
                            <Label htmlFor='agent-enabled' className='text-sm'>
                              Enable Agent Mode
                            </Label>
                            <Switch
                              id='agent-enabled'
                              checked={agentMode.enabled}
                              onCheckedChange={setAgentModeEnabled}
                            />
                          </div>
                          <div className='flex items-center justify-between'>
                            <div className='space-y-0.5'>
                              <Label htmlFor='auto-apply' className='text-sm'>
                                Auto-apply tags
                              </Label>
                              <p className='text-xs text-muted-foreground'>
                                Apply detected tags without confirmation
                              </p>
                            </div>
                            <Switch
                              id='auto-apply'
                              checked={agentMode.autoApply}
                              onCheckedChange={setAgentModeAutoApply}
                              disabled={!agentMode.enabled}
                            />
                          </div>
                        </div>
                        {agentMode.enabled && (
                          <div className='pt-2 border-t'>
                            <div className='flex items-center gap-2 text-xs text-violet-600 dark:text-violet-400'>
                              <Zap className='h-3 w-3' />
                              <span>Agent will auto-tag selected text</span>
                            </div>
                          </div>
                        )}
                      </div>
                    </PopoverContent>
                  </Popover>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent className='flex-1 p-0 mt-2 h-screen'>
              <TextEditor
                report={report}
                selectedBlockId={selectedBlockId}
                onBlockSelect={handleBlockSelect}
                onReportChange={setReport}
                onTextHighlight={handleTextHighlight}
              />
            </CardContent>
          </Card>
        </ResizablePanel>

        {/* Resizable Handle */}
        <ResizableHandle
          withHandle
          className='bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors'
        >
          <div className='flex items-center justify-center h-full'>
            <GripVertical className='h-4 w-4 text-slate-500' />
          </div>
        </ResizableHandle>

        {/* Right Panel - Tools Only (no more vertical split) */}
        <ResizablePanel defaultSize={50} minSize={30}>
          <Card className='h-full shadow-none border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm flex flex-col rounded-none'>
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
                            setIsTaggedFactsOpen(false); // Close modal when selecting a block
                          }}
                          onReportChange={handleReportChange}
                        />
                      </div>
                    </DialogContent>
                  </Dialog>

                  <Button
                    variant='outline'
                    size='sm'
                    onClick={() => {
                      // Clear any persisted editor state before starting a new document
                      if (typeof window !== 'undefined') {
                        localStorage.removeItem('xbrl-editor-session');
                        localStorage.removeItem('xbrl-session-id');
                      }
                      setReport(null);
                      setSelectedBlockId(null);
                      // Reset sessions to an empty array rather than null. When
                      // sessions is null the effect hook skips fetching due to a stale closure
                      // and the UI shows "Loading your sessions…" indefinitely. Use an
                      // empty list to indicate no saved sessions.
                      setSessions([]);
                    }}
                    className='gap-2 h-9 px-4 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors flex-shrink-0'
                  >
                    <Upload className='h-4 w-4' />
                    New Document
                  </Button>
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
                  {/* <TabsTrigger
                    value='settings'
                    className='gap-2 text-xs data-[state=active]:bg-purple-500 data-[state=active]:text-white'
                  >
                    <Settings className='h-3 w-3' />
                    Settings
                  </TabsTrigger> */}
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

                <TabsContent
                  value='settings'
                  className='mx-4 mt-0 mb-4 flex-1 min-h-0'
                >
                  <div className='h-full flex flex-col justify-center items-center text-center'>
                    <div className='p-4 bg-gradient-to-br from-purple-100 to-indigo-100 dark:from-purple-900/20 dark:to-indigo-900/20 rounded-full mb-4 shadow-lg'>
                      <Settings className='h-6 w-6 text-purple-600' />
                    </div>
                    <h3 className='font-semibold mb-3 text-base'>
                      Configure Context
                    </h3>
                    <p className='text-sm text-muted-foreground mb-4 max-w-sm leading-relaxed'>
                      Set up tagging contexts and AI models to improve accuracy.
                    </p>
                    <Button
                      variant='outline'
                      size='sm'
                      asChild
                      className='hover:bg-purple-50 hover:border-purple-300 bg-transparent'
                    >
                      <a href='/contexts' className='gap-2'>
                        <Settings className='h-4 w-4' />
                        Manage Contexts
                      </a>
                    </Button>
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
