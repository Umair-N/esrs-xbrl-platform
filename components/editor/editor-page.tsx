"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import { FileUploader } from "@/components/editor/file-uploader";
import { TextEditor } from "@/components/editor/text-editor";
import { TaggingPanel } from "@/components/editor/tagging-panel";
import { TaggedFactsList } from "@/components/editor/tagged-facts-list";
import { SaveExportPanel } from "@/components/editor/export";
import type { ReportDocument } from "@/types/report";
import { FileText, Tags, Save, Settings, Upload, BookOpen, Sparkles, Activity, GripVertical } from 'lucide-react';

export default function EditorPage() {
  const [report, setReport] = useState<ReportDocument | null>(null);
  const [selectedBlockId, setSelectedBlockId] = useState<string | null>(null);
  const [highlightedText, setHighlightedText] = useState<{
    text: string;
    startIndex: number;
    endIndex: number;
  } | null>(null);

  const handleReportLoaded = (newReport: ReportDocument) => {
    setReport(newReport);
    if (newReport.blocks.length > 0) {
      setSelectedBlockId(newReport.blocks[0].id);
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

  const handleSave = (savedReport: ReportDocument) => {
    console.log("Report saved:", savedReport.title);
  };

  const handleReportChange = (updatedReport: ReportDocument) => {
    setReport(updatedReport);
  };

  // Upload state - no document loaded
  if (!report) {
    return (
     


        <div className="flex-1 flex items-center justify-center  mt-1 mb-1">
          <div className="w-full max-w-4xl">
            <FileUploader onReportLoaded={handleReportLoaded} />
          </div>
        </div>
    );
  }

  const totalTags = report.blocks.reduce((count, block) => count + (block.tags?.length || 0), 0);
  const taggedBlocks = report.blocks.filter(block => block.tags && block.tags.length > 0).length;
  const completionRate = report.blocks.length > 0 ? Math.round((taggedBlocks / report.blocks.length) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 pb-5 py-2">
      {/* Header - Fixed height with better styling */}
      <div className="border-b bg-white/95 dark:bg-slate-800/95 backdrop-blur-md shadow-lg sticky top-0 z-10">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg shadow-md">
                <FileText className="h-5 w-5 text-white" />
              </div>
              <div className="min-w-0">
                <h1 className="text-lg font-bold truncate max-w-md bg-gradient-to-r from-slate-900 to-slate-700 dark:from-white dark:to-slate-300 bg-clip-text text-transparent">
                  {report.title}
                </h1>
                <div className="flex items-center gap-3 mt-1">
                  <Badge variant="secondary" className="text-xs px-2 py-1 bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                    <Activity className="h-3 w-3 mr-1" />
                    {report.blocks.length} blocks
                  </Badge>
                  <Badge variant="outline" className="text-xs px-2 py-1 border-emerald-200 bg-emerald-50 text-emerald-800 dark:bg-emerald-900/20 dark:text-emerald-300">
                    <Tags className="h-3 w-3 mr-1" />
                    {totalTags} tagged
                  </Badge>
                  <Badge variant="outline" className="text-xs px-2 py-1 border-purple-200 bg-purple-50 text-purple-800 dark:bg-purple-900/20 dark:text-purple-300">
                    {completionRate}% complete
                  </Badge>
                </div>
              </div>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setReport(null)}
              className="gap-2 h-9 px-4 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
            >
              <Upload className="h-4 w-4" />
              New Document
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content with Resizable Panels - NO PADDING */}
      <ResizablePanelGroup direction="horizontal" className="min-h-[calc(100vh-140px)] bg-white/50 dark:bg-slate-800/50 backdrop-blur-sm">
        
        {/* Left Panel - Document Editor */}
        <ResizablePanel defaultSize={60} minSize={40}>
          <Card className="h-full shadow-none border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm flex flex-col rounded-none">
            <CardHeader className="pb-4 flex-shrink-0 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20">
              <CardTitle className="flex items-center gap-3 text-lg">
                <div className="p-2 bg-blue-500 rounded-lg">
                  <BookOpen className="h-5 w-5 text-white" />
                </div>
                <div>
                  <span className="bg-gradient-to-r from-blue-700 to-indigo-700 dark:from-blue-300 dark:to-indigo-300 bg-clip-text text-transparent">
                    Document Content
                  </span>
                  <p className="text-sm text-muted-foreground font-normal mt-1">
                    Select text to add ESRS tags
                  </p>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 p-6 min-h-0">
              <div className="h-full bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900/50 dark:to-slate-800/50 rounded-xl border-2 border-dashed border-slate-300 dark:border-slate-600 p-6 overflow-hidden shadow-inner">
                <TextEditor
                  report={report}
                  selectedBlockId={selectedBlockId}
                  onBlockSelect={handleBlockSelect}
                  onReportChange={setReport}
                  onTextHighlight={handleTextHighlight}
                />
              </div>
            </CardContent>
          </Card>
        </ResizablePanel>

        {/* Resizable Handle */}
        <ResizableHandle withHandle className="bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors">
          <div className="flex items-center justify-center h-full">
            <GripVertical className="h-4 w-4 text-slate-500" />
          </div>
        </ResizableHandle>

        {/* Right Panel - Tools and Tagged Facts */}
        <ResizablePanel defaultSize={40} minSize={30}>
          <ResizablePanelGroup direction="vertical">
            
            {/* Top Panel - Tagging Tools */}
            <ResizablePanel defaultSize={45} minSize={30}>
              <Card className="h-full shadow-none border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm flex flex-col rounded-none">
                <CardHeader className="pb-3 flex-shrink-0 bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-950/20 dark:to-green-950/20">
                  <CardTitle className="flex items-center gap-3 text-lg">
                    <div className="p-2 bg-emerald-500 rounded-lg">
                      <Tags className="h-5 w-5 text-white" />
                    </div>
                    <span className="bg-gradient-to-r from-emerald-700 to-green-700 dark:from-emerald-300 dark:to-green-300 bg-clip-text text-transparent">
                      ESRS Tagging Tools
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="flex-1 p-0 min-h-0">
                  <Tabs defaultValue="tagging" className="w-full h-full flex flex-col">
                    <TabsList className="grid w-full grid-cols-3 mx-4 my-4 bg-slate-100 dark:bg-slate-700 flex-shrink-0">
                      <TabsTrigger value="tagging" className="gap-2 text-xs data-[state=active]:bg-emerald-500 data-[state=active]:text-white">
                        <Tags className="h-3 w-3" />
                        Tag
                      </TabsTrigger>
                      <TabsTrigger value="export" className="gap-2 text-xs data-[state=active]:bg-blue-500 data-[state=active]:text-white">
                        <Save className="h-3 w-3" />
                        Export
                      </TabsTrigger>
                      <TabsTrigger value="settings" className="gap-2 text-xs data-[state=active]:bg-purple-500 data-[state=active]:text-white">
                        <Settings className="h-3 w-3" />
                        Settings
                      </TabsTrigger>
                    </TabsList>

                    <TabsContent value="tagging" className="mx-4 mt-0 mb-4 flex-1 min-h-0">
                      <div className="h-full overflow-y-auto">
                        <TaggingPanel
                          report={report}
                          selectedBlockId={selectedBlockId}
                          highlightedText={highlightedText}
                          onReportChange={setReport}
                        />
                      </div>
                    </TabsContent>

                    <TabsContent value="export" className="mx-4 mt-0 mb-4 flex-1 min-h-0">
                      <div className="h-full overflow-y-auto">
                        <SaveExportPanel
                          report={report}
                          onSave={handleSave}
                        />
                      </div>
                    </TabsContent>

                    <TabsContent value="settings" className="mx-4 mt-0 mb-4 flex-1 min-h-0">
                      <div className="h-full flex flex-col justify-center items-center text-center">
                        <div className="p-4 bg-gradient-to-br from-purple-100 to-indigo-100 dark:from-purple-900/20 dark:to-indigo-900/20 rounded-full mb-4 shadow-lg">
                          <Settings className="h-6 w-6 text-purple-600" />
                        </div>
                        <h3 className="font-semibold mb-3 text-base">Configure Context</h3>
                        <p className="text-sm text-muted-foreground mb-4 max-w-sm leading-relaxed">
                          Set up tagging contexts and AI models to improve accuracy.
                        </p>
                        <Button variant="outline" size="sm" asChild className="hover:bg-purple-50 hover:border-purple-300">
                          <a href="/contexts" className="gap-2">
                            <Settings className="h-4 w-4" />
                            Manage Contexts
                          </a>
                        </Button>
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            </ResizablePanel>

            {/* Vertical Resizable Handle */}
            <ResizableHandle withHandle className="bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors">
              <div className="flex items-center justify-center w-full">
                <div className="w-4 h-1 bg-slate-400 rounded-full"></div>
              </div>
            </ResizableHandle>

            {/* Bottom Panel - Tagged Facts */}
            <ResizablePanel defaultSize={55} minSize={30}>
              <Card className="h-full shadow-none border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm flex flex-col rounded-none">
                <CardHeader className="pb-3 flex-shrink-0 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-950/20 dark:to-pink-950/20">
                  <CardTitle className="flex items-center gap-3 text-lg">
                    <div className="p-2 bg-purple-500 rounded-lg">
                      <Sparkles className="h-5 w-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <span className="bg-gradient-to-r from-purple-700 to-pink-700 dark:from-purple-300 dark:to-pink-300 bg-clip-text text-transparent">
                        Tagged Facts
                      </span>
                      {totalTags > 0 && (
                        <Badge variant="secondary" className="ml-3 bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
                          {totalTags} facts
                        </Badge>
                      )}
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent className="flex-1 p-4 min-h-0">
                  <div className="h-full bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/10 dark:to-pink-900/10 rounded-xl border-2 border-dashed border-purple-200 dark:border-purple-800 p-4 overflow-hidden shadow-inner">
                    <div className="h-full overflow-y-auto">
                      <TaggedFactsList
                        report={report}
                        onBlockSelect={(blockId: string) => {
                          setSelectedBlockId(blockId);
                          setHighlightedText(null);
                        }}
                        onReportChange={handleReportChange}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
}
