"use client";

import type React from "react";
import { useState } from "react";
import { Upload, FileText, Clipboard, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import type { ReportDocument } from "@/types/report";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL!;

interface FileUploaderProps {
  onReportLoaded: (report: ReportDocument) => void;
}

export function FileUploader({ onReportLoaded }: FileUploaderProps) {
  const [rawText, setRawText] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null);

  // Get auth token from localStorage or your auth context
  const getAuthToken = () => {
    return localStorage.getItem("access_token") || "";
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/msword",
    ];
    if (!allowedTypes.includes(file.type)) {
      setUploadError("Please upload a PDF or DOCX file");
      return;
    }

    // Validate file size (10MB limit)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setUploadError("File size must be less than 10MB");
      return;
    }

    setIsUploading(true);
    setUploadError(null);
    setUploadSuccess(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/api/files/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${getAuthToken()}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Upload failed");
      }

      const reportData: ReportDocument = await response.json();
      setUploadSuccess(`Successfully processed "${file.name}"`);
      onReportLoaded(reportData);

      // Reset file input
      event.target.value = "";
    } catch (error) {
      console.error("Upload error:", error);
      setUploadError(error instanceof Error ? error.message : "Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  const handleTextSubmit = async () => {
    if (!rawText.trim()) {
      setUploadError("Please enter some text");
      return;
    }

    setIsUploading(true);
    setUploadError(null);
    setUploadSuccess(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/reports/text`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getAuthToken()}`,
        },
        body: JSON.stringify({
          text: rawText,
          title: "Pasted Report",
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Processing failed");
      }

      const reportData: ReportDocument = await response.json();
      setUploadSuccess("Successfully processed pasted text");
      onReportLoaded(reportData);

      // Clear textarea
      setRawText("");
    } catch (error) {
      console.error("Text processing error:", error);
      setUploadError(
        error instanceof Error ? error.message : "Processing failed"
      );
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      {uploadError && (
        <Alert className="mb-4 border-red-200 bg-red-50">
          <AlertDescription className="text-red-700">
            {uploadError}
          </AlertDescription>
        </Alert>
      )}

      {uploadSuccess && (
        <Alert className="mb-4 border-green-200 bg-green-50">
          <AlertDescription className="text-green-700">
            {uploadSuccess}
          </AlertDescription>
        </Alert>
      )}

      <Tabs defaultValue="upload" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="upload">Upload File</TabsTrigger>
          <TabsTrigger value="paste">Paste Text</TabsTrigger>
        </TabsList>

        <TabsContent value="upload">
          <Card>
            <CardHeader>
              <CardTitle>Upload Report</CardTitle>
              <CardDescription>
                Upload a PDF or DOCX file to extract the report content for
                tagging.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-12 text-center">
                {isUploading ? (
                  <Loader2 className="h-10 w-10 text-blue-500 animate-spin mb-4" />
                ) : (
                  <Upload className="h-10 w-10 text-muted-foreground mb-4" />
                )}
                <p className="mb-2 text-sm text-muted-foreground">
                  {isUploading
                    ? "Processing your file..."
                    : "Drag and drop your file here, or click to browse"}
                </p>
                <input
                  type="file"
                  id="file-upload"
                  className="hidden"
                  accept=".pdf,.docx,.doc"
                  onChange={handleFileUpload}
                  disabled={isUploading}
                />
                <Button
                  variant="outline"
                  onClick={() =>
                    document.getElementById("file-upload")?.click()
                  }
                  disabled={isUploading}
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <FileText className="mr-2 h-4 w-4" />
                      Select File
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <p className="text-xs text-muted-foreground">
                Supported formats: PDF, DOCX • Max size: 10MB
              </p>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="paste">
          <Card>
            <CardHeader>
              <CardTitle>Paste Report Text</CardTitle>
              <CardDescription>
                Paste the raw text of your report for tagging.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Paste your report text here..."
                className="min-h-[300px]"
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                disabled={isUploading}
              />
            </CardContent>
            <CardFooter>
              <Button
                onClick={handleTextSubmit}
                className="w-full"
                disabled={isUploading || !rawText.trim()}
              >
                {isUploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Clipboard className="mr-2 h-4 w-4" />
                    Process Text
                  </>
                )}
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
