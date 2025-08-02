"use client";

import type React from "react";
import { useState } from "react";
import axios from "axios";
import { toast } from "sonner";
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
import type { ReportDocument } from "@/types/report";
import axiosInstance from "@/lib/axios";

interface FileUploaderProps {
  onReportLoaded: (report: ReportDocument) => void;
}

export function FileUploader({ onReportLoaded }: FileUploaderProps) {
  const [rawText, setRawText] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const getAuthToken = () => {
    return localStorage.getItem("access_token") || "";
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/msword",
    ];

    if (!allowedTypes.includes(file.type)) {
      toast.error("Please upload a PDF or DOCX file");
      return;
    }

    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      toast.error("File size must be less than 10MB");
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axiosInstance.post(
        "/api/v1/reports/upload",
        formData,
        {
          headers: {
            Authorization: `Bearer ${getAuthToken()}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const reportData: ReportDocument = response.data;
      toast.success(`Successfully processed "${file.name}"`);
      onReportLoaded(reportData);
      event.target.value = ""; // Clear the input after upload
    } catch (error: any) {
      console.error("Upload error:", error);
      const message =
        error.response?.data?.detail || error.message || "Upload failed";
      toast.error(message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleTextSubmit = async () => {
    if (!rawText.trim()) {
      toast.error("Please enter some text");
      return;
    }

    setIsUploading(true);

    try {
      const response = await axiosInstance.post(
        "/api/v1/reports/text",
        {
          text: rawText,
          title: "Pasted Report",
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAuthToken()}`,
          },
        }
      );

      const reportData: ReportDocument = response.data;
      toast.success("Successfully processed pasted text");
      onReportLoaded(reportData);
      setRawText("");
    } catch (error: any) {
      console.error("Text processing error:", error);
      const message =
        error.response?.data?.detail || error.message || "Processing failed";
      toast.error(message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
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
