"use client";

import type React from "react";
import { useState } from "react";
import axios from "axios";
import { toast } from "sonner";
import { Upload, FileText, Clipboard, Loader2, CloudUpload, File, CheckCircle } from 'lucide-react';
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
import { Progress } from "@/components/ui/progress";
import type { ReportDocument } from "@/types/report";
import {axiosInstance} from "@/lib/axios";

interface FileUploaderProps {
  onReportLoaded: (report: ReportDocument) => void;
}

export function FileUploader({ onReportLoaded }: FileUploaderProps) {
  const [rawText, setRawText] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [dragActive, setDragActive] = useState(false);

  const getAuthToken = () => {
    return localStorage.getItem("access_token") || "";
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileProcess(e.dataTransfer.files[0]);
    }
  };

// Ensure you import the fetchApi correctly

const handleFileProcess = async (file: File) => {
  const allowedTypes = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
  ];

  if (!allowedTypes.includes(file.type)) {
    toast.error("Invalid file type", {
      description: "Please upload a PDF or DOCX file"
    });
    return;
  }

  const maxSize = 10 * 1024 * 1024;
  if (file.size > maxSize) {
    toast.error("File too large", {
      description: "File size must be less than 10MB"
    });
    return;
  }

  setIsUploading(true);
  setUploadProgress(0);

  // Create a new FormData object and append the file
  const formData = new FormData();
  formData.append("file", file);

  // Simulating progress for the file upload
  const progressInterval = setInterval(() => {
    setUploadProgress(prev => {
      if (prev < 30) return prev + 5;
      if (prev < 70) return prev + 2;
      if (prev < 90) return prev + 1;
      return prev;
    });
  }, 500);

  // Show processing message after 5 seconds
  const messageTimeout = setTimeout(() => {
    toast.info("Still processing...", {
      description: "Large documents may take up to 2 minutes to process",
      duration: 5000
    });
  }, 5000);

  try {
    // Make the request using fetchApi
    const response = await axiosInstance.post('/reports/upload', formData, {
      headers: {
        "Content-Type": "multipart/form-data", 
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(Math.min(percentCompleted, 95));  // Update progress bar
        }
      }
    });

    clearInterval(progressInterval);
    clearTimeout(messageTimeout);
    setUploadProgress(100);

    // Assuming the response data is the report object
    const reportData = response.data;

    toast.success("Upload successful!", {
      description: `Successfully processed "${file.name}"`,
      icon: <CheckCircle className="h-4 w-4" />
    });

    onReportLoaded(reportData);
  } catch (error: any) {
    console.error("Upload error:", error);

    let message = "Upload failed";
    let description = "Please try again";

    if (error.name === 'AbortError') {
      message = "Upload cancelled";
      description = "The upload was cancelled";
    } else if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      message = "Upload timeout";
      description = "The upload took too long. Try with a smaller file or check your connection";
    } else if (error.response?.status === 413) {
      message = "File too large";
      description = "The file exceeds the server's size limit";
    } else if (error.response?.status >= 500) {
      message = "Server error";
      description = "There was a problem processing your file on the server";
    } else {
      const serverMessage = error.response?.data?.detail || error.response?.data?.message;
      if (serverMessage) {
        description = serverMessage;
      }
    }

    toast.error(message, { description });
  } finally {
    setIsUploading(false);
    setUploadProgress(0);
  }
};


  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    await handleFileProcess(file);
    event.target.value = "";
  };

  const handleTextSubmit = async () => {
    if (!rawText.trim()) {
      toast.error("Empty text", {
        description: "Please enter some text"
      });
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);

    // Create AbortController for request cancellation
    const controller = new AbortController();

    try {
      // Progress simulation for text processing
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev < 50) return prev + 8;
          if (prev < 85) return prev + 3;
          return prev;
        });
      }, 300);

      // Show processing message for long operations
      const messageTimeout = setTimeout(() => {
        toast.info("Processing text...", {
          description: "Analyzing content for ESRS compliance",
          duration: 3000
        });
      }, 3000);

      const response = await axiosInstance.post(
        "/reports/text",
        {
          text: rawText,
          title: "Pasted Report",
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAuthToken()}`,
          },
          timeout: 60000, // 1 minute timeout for text processing
          signal: controller.signal,
        }
      );

      clearInterval(progressInterval);
      clearTimeout(messageTimeout);
      setUploadProgress(100);

      const reportData: ReportDocument = response.data;
      
      toast.success("Processing complete!", {
        description: "Successfully processed pasted text",
        icon: <CheckCircle className="h-4 w-4" />
      });
      
      onReportLoaded(reportData);
      setRawText("");
    } catch (error: any) {
      console.error("Text processing error:", error);
      
      let message = "Processing failed";
      let description = "Please try again";

      if (error.name === 'AbortError') {
        message = "Processing cancelled";
        description = "The processing was cancelled";
      } else if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        message = "Processing timeout";
        description = "The text processing took too long. Try with shorter text";
      } else {
        const serverMessage = error.response?.data?.detail || error.response?.data?.message;
        if (serverMessage) {
          description = serverMessage;
        }
      }

      toast.error(message, { description });
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="h-full">
      <Tabs defaultValue="upload" className="h-full flex flex-col">
        <TabsList className="grid w-full grid-cols-2 mb-6 flex-shrink-0">
          <TabsTrigger value="upload" className="gap-2">
            <Upload className="h-4 w-4" />
            Upload File
          </TabsTrigger>
          <TabsTrigger value="paste" className="gap-2">
            <Clipboard className="h-4 w-4" />
            Paste Text
          </TabsTrigger>
        </TabsList>

        <TabsContent value="upload" className="flex-1 mt-0">
          <Card className="border-0 shadow-lg h-full">
            <CardHeader className="text-center pb-6">
              <div className="mx-auto w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mb-4">
                <CloudUpload className="h-8 w-8 text-white" />
              </div>
              <CardTitle className="text-2xl">Upload Your Report</CardTitle>
              <CardDescription className="text-base">
                Upload a PDF or DOCX file to extract content for ESRS tagging
              </CardDescription>
            </CardHeader>
            
            <CardContent className="flex-1">
              <div
                className={`relative flex flex-col items-center justify-center border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 h-64 ${
                  dragActive
                    ? "border-blue-500 bg-blue-50 dark:bg-blue-950/20"
                    : isUploading
                    ? "border-green-500 bg-green-50 dark:bg-green-950/20"
                    : "border-slate-300 dark:border-slate-600 hover:border-blue-400 hover:bg-slate-50 dark:hover:bg-slate-800"
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                {isUploading ? (
                  <div className="space-y-4 w-full max-w-xs">
                    <div className="animate-spin rounded-full h-12 w-12 border-4 border-green-500 border-t-transparent mx-auto" />
                    <div className="space-y-2">
                      <p className="text-sm font-medium text-green-700 dark:text-green-400">
                        Processing your document...
                      </p>
                      <Progress value={uploadProgress} className="h-2" />
                      <p className="text-xs text-muted-foreground">
                        {uploadProgress}% complete
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Large files may take up to 2 minutes
                      </p>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className={`p-4 rounded-full mb-4 transition-colors ${
                      dragActive 
                        ? "bg-blue-100 dark:bg-blue-900" 
                        : "bg-slate-100 dark:bg-slate-800"
                    }`}>
                      <File className={`h-8 w-8 ${
                        dragActive 
                          ? "text-blue-600" 
                          : "text-slate-500"
                      }`} />
                    </div>
                    <h3 className="text-lg font-semibold mb-2">
                      {dragActive ? "Drop your file here" : "Choose a file or drag it here"}
                    </h3>
                    <p className="text-muted-foreground mb-6 max-w-sm">
                      Supports PDF and DOCX files up to 10MB. Processing may take 1-2 minutes for large documents.
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
                      size="lg"
                      onClick={() =>
                        document.getElementById("file-upload")?.click()
                      }
                      disabled={isUploading}
                      className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 py-2"
                    >
                      <FileText className="mr-2 h-5 w-5" />
                      Select File
                    </Button>
                  </>
                )}
              </div>
            </CardContent>
            
            <CardFooter className="justify-center">
              <div className="flex items-center gap-4 text-xs text-muted-foreground">
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>PDF, DOCX supported</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span>Max 10MB</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span>Secure processing</span>
                </div>
              </div>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="paste" className="flex-1 mt-0">
          <Card className="border-0 shadow-lg h-full">
            <CardHeader className="text-center pb-6">
              <div className="mx-auto w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-full flex items-center justify-center mb-4">
                <Clipboard className="h-8 w-8 text-white" />
              </div>
              <CardTitle className="text-2xl">Paste Report Text</CardTitle>
              <CardDescription className="text-base">
                Paste the raw text of your report for immediate processing
              </CardDescription>
            </CardHeader>
            
            <CardContent className="space-y-4 flex-1">
              {isUploading && (
                <div className="space-y-3 p-4 bg-emerald-50 dark:bg-emerald-950/20 rounded-lg border border-emerald-200 dark:border-emerald-800">
                  <div className="flex items-center gap-3">
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-emerald-500 border-t-transparent" />
                    <span className="text-sm font-medium text-emerald-700 dark:text-emerald-400">
                      Processing your text...
                    </span>
                  </div>
                  <Progress value={uploadProgress} className="h-2" />
                  <p className="text-xs text-emerald-600 dark:text-emerald-400">
                    {uploadProgress}% complete
                  </p>
                </div>
              )}
              
              <Textarea
                placeholder="Paste your report text here... 

Example: Our company's greenhouse gas emissions for 2023 totaled 1,250 tonnes CO2 equivalent, representing a 15% reduction from the previous year..."
                className="min-h-[200px] text-sm leading-relaxed resize-none border-2 focus:border-emerald-500"
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                disabled={isUploading}
              />
              
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>{rawText.length} characters</span>
                <span>Minimum 50 characters recommended</span>
              </div>
            </CardContent>
            
            <CardFooter>
              <Button
                onClick={handleTextSubmit}
                className="w-full h-12 text-base bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700"
                disabled={isUploading || !rawText.trim() || rawText.length < 10}
                size="lg"
              >
                {isUploading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2" />
                    Processing Text...
                  </>
                ) : (
                  <>
                    <Clipboard className="mr-2 h-5 w-5" />
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