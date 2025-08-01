"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  ResizablePanelGroup,
  ResizablePanel,
  ResizableHandle,
} from "@/components/ui/resizable";
import { FileUploader } from "@/components/editor/file-uploader";
import { TextEditor } from "@/components/editor/text-editor";
import { TaggingPanel } from "@/components/editor/tagging-panel";
import { TaggedFactsList } from "@/components/editor/tagged-facts-list";
import type { ReportDocument } from "@/types/report";
import { sampleReport } from "@/lib/sample-data";
import { SaveExportPanel } from "@/components/editor/export";

export default function EditorPage() {
  const [report, setReport] = useState<ReportDocument | null>(sampleReport);
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
    // Handle successful save (e.g., show notification)
    console.log("Report saved:", savedReport.title);
  };

  // Handler for when TaggedFactsList updates the report (e.g., deleting tags)
  const handleReportChange = (updatedReport: ReportDocument) => {
    console.log("Report updated from TaggedFactsList");
    setReport(updatedReport);
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      {/* Header - Fixed height */}

      {/* Main Content - Takes remaining height */}
      <div className="flex-1 min-h-0">
        {!report ? (
          <div className="h-full flex items-center justify-center p-6">
            <FileUploader onReportLoaded={handleReportLoaded} />
          </div>
        ) : (
          <ResizablePanelGroup
            direction="horizontal"
            className="h-full border-2 border-primary/30"
          >
            {/* Left Panel - Main Content */}
            <ResizablePanel defaultSize={70} minSize={50}>
              <ResizablePanelGroup direction="vertical" className="h-full">
                {/* Text Editor Section */}
                <ResizablePanel defaultSize={60} minSize={30}>
                  <div className="h-full p-3 border-r border-border">
                    <Card className="h-full border-2 border-primary/20">
                      <CardContent className="p-3 h-full flex flex-col">
                        <div className="flex justify-between items-center mb-2 flex-shrink-0">
                          <h2 className="text-lg font-semibold">
                            {report.title}
                          </h2>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setReport(null)}
                          >
                            Upload New
                          </Button>
                        </div>
                        <div className="flex-1 min-h-0 border border-dashed border-blue-300 rounded p-2 overflow-hidden">
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
                  </div>
                </ResizablePanel>

                <ResizableHandle withHandle />

                {/* Tagged Facts Section */}
                <ResizablePanel defaultSize={40} minSize={20}>
                  <div className="h-full p-3 border-r border-border">
                    <Card className="h-full border-2 border-primary/20">
                      <CardContent className="p-3 h-full flex flex-col">
                        <h2 className="text-lg font-semibold mb-2 flex-shrink-0">
                          Tagged Facts
                        </h2>
                        <div className="flex-1 min-h-0 border border-dashed border-green-300 rounded p-2 overflow-auto">
                          <TaggedFactsList
                            report={report}
                            onBlockSelect={(blockId) => {
                              setSelectedBlockId(blockId);
                              setHighlightedText(null);
                            }}
                            onReportChange={handleReportChange}
                          />
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </ResizablePanel>
              </ResizablePanelGroup>
            </ResizablePanel>

            <ResizableHandle withHandle />

            {/* Right Panel - Sidebar */}
            <ResizablePanel defaultSize={30} minSize={25} maxSize={50}>
              <div className="h-full border-l border-border bg-muted/5 flex flex-col">
                <div className="p-3 flex-1 min-h-0">
                  <Tabs defaultValue="tagging" className="h-full flex flex-col">
                    <TabsList className="grid w-full grid-cols-3 flex-shrink-0">
                      <TabsTrigger value="tagging">Tagging</TabsTrigger>
                      <TabsTrigger value="save">Save</TabsTrigger>
                      <TabsTrigger value="context">Context</TabsTrigger>
                    </TabsList>

                    <TabsContent
                      value="tagging"
                      className="flex-1 min-h-0 mt-3"
                    >
                      <div className="h-full border border-border rounded-md p-2">
                        <div className="h-full border border-dashed border-muted-foreground/30 rounded p-2 overflow-auto">
                          <TaggingPanel
                            report={report}
                            selectedBlockId={selectedBlockId}
                            highlightedText={highlightedText}
                            onReportChange={setReport}
                          />
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="save" className="flex-1 min-h-0 mt-3">
                      <div className="h-full border border-border rounded-md p-2">
                        <div className="h-full border border-dashed border-muted-foreground/30 rounded p-2 overflow-auto">
                          <SaveExportPanel
                            report={report}
                            onSave={handleSave}
                          />
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent
                      value="context"
                      className="flex-1 min-h-0 mt-3"
                    >
                      <Card className="h-full border-2 border-secondary">
                        <CardContent className="p-3 h-full flex flex-col justify-center">
                          <p className="text-sm text-muted-foreground mb-4">
                            Select or create a context to use for tagging.
                          </p>
                          <Button
                            variant="outline"
                            size="sm"
                            className="bg-transparent"
                            asChild
                          >
                            <a href="/contexts">Manage Contexts</a>
                          </Button>
                        </CardContent>
                      </Card>
                    </TabsContent>
                  </Tabs>
                </div>
              </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        )}
      </div>
    </div>
  );
}
