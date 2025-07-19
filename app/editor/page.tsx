"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
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

  return (
    <div className="container mx-auto py-6">
      <h1 className="text-3xl font-bold mb-6">Report Editor & Tagging</h1>

      {!report ? (
        <FileUploader onReportLoaded={handleReportLoaded} />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardContent className="p-4">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold">{report.title}</h2>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setReport(null)}
                  >
                    Upload New
                  </Button>
                </div>
                <TextEditor
                  report={report}
                  selectedBlockId={selectedBlockId}
                  onBlockSelect={handleBlockSelect}
                  onReportChange={setReport}
                  onTextHighlight={handleTextHighlight}
                />
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <h2 className="text-xl font-semibold mb-4">Tagged Facts</h2>
                <TaggedFactsList
                  report={report}
                  onBlockSelect={(blockId) => {
                    setSelectedBlockId(blockId);
                    setHighlightedText(null);
                  }}
                />
              </CardContent>
            </Card>
          </div>

          <div>
            <Tabs defaultValue="tagging">
              <TabsList className="grid w-full grid-cols-3">
                {" "}
                {/* Changed to 3 columns */}
                <TabsTrigger value="tagging">Tagging</TabsTrigger>
                <TabsTrigger value="save">Save</TabsTrigger>{" "}
                {/* Add this tab */}
                <TabsTrigger value="context">Context</TabsTrigger>
              </TabsList>
              <TabsContent value="tagging" className="mt-4">
                <TaggingPanel
                  report={report}
                  selectedBlockId={selectedBlockId}
                  highlightedText={highlightedText}
                  onReportChange={setReport}
                />
              </TabsContent>
              <TabsContent value="save" className="mt-4">
                {" "}
                {/* Add this tab content */}
                <SaveExportPanel report={report} onSave={handleSave} />
              </TabsContent>
              <TabsContent value="context" className="mt-4">
                <Card>
                  <CardContent className="p-4">
                    <p className="text-sm text-muted-foreground">
                      Select or create a context to use for tagging.
                    </p>
                    <Button
                      variant="outline"
                      size="sm"
                      className="mt-4"
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
      )}
    </div>
  );
}
