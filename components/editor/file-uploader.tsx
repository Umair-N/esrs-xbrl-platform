'use client';

import type React from 'react';
import { useState } from 'react';
import { toast } from 'sonner';
import { FileText, CloudUpload, File, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import type { ReportDocument } from '@/types/report';
import { axiosInstance } from '@/lib/axios';

interface FileUploaderProps {
  onReportLoaded: (report: ReportDocument) => void;
}

export function FileUploader({ onReportLoaded }: FileUploaderProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [dragActive, setDragActive] = useState(false);
  const [processingStage, setProcessingStage] = useState<
    'uploading' | 'processing' | 'complete'
  >('uploading');

  const getAuthToken = () => {
    return localStorage.getItem('access_token') || '';
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
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

  const handleFileProcess = async (file: File) => {
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/msword',
    ];

    if (!allowedTypes.includes(file.type)) {
      toast.error('Invalid file type', {
        description: 'Please upload a PDF or DOCX file',
      });
      return;
    }

    const maxSize = 60 * 1024 * 1024;
    if (file.size > maxSize) {
      toast.error('File too large', {
        description: 'File size must be less than 60MB',
      });
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);
    setProcessingStage('uploading');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axiosInstance.post('/reports/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percentCompleted);

            if (percentCompleted === 100) {
              setProcessingStage('processing');
            }
          }
        },
      });

      setProcessingStage('complete');
      setUploadProgress(100);

      const reportData = response.data;

      toast.success('Upload successful!', {
        description: `Successfully processed "${file.name}"`,
        icon: <CheckCircle className='h-4 w-4' />,
      });

      onReportLoaded(reportData);
    } catch (error: any) {
      console.error('Upload error:', error);

      let message = 'Upload failed';
      let description = 'Please try again';

      if (error.name === 'AbortError') {
        message = 'Upload cancelled';
        description = 'The upload was cancelled';
      } else if (
        error.code === 'ECONNABORTED' ||
        error.message.includes('timeout')
      ) {
        message = 'Upload timeout';
        description =
          'The upload took too long. Try with a smaller file or check your connection';
      } else if (error.response?.status === 413) {
        message = 'File too large';
        description = "The file exceeds the server's size limit";
      } else if (error.response?.status >= 500) {
        message = 'Server error';
        description = 'There was a problem processing your file on the server';
      } else {
        const serverMessage =
          error.response?.data?.detail || error.response?.data?.message;
        if (serverMessage) {
          description = serverMessage;
        }
      }

      toast.error(message, { description });
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
      setProcessingStage('uploading');
    }
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    await handleFileProcess(file);
    event.target.value = '';
  };

  const getProgressMessage = () => {
    switch (processingStage) {
      case 'uploading':
        return 'Uploading your document...';
      case 'processing':
        return 'Processing and analyzing content...';
      case 'complete':
        return 'Processing complete!';
      default:
        return 'Processing your document...';
    }
  };

  return (
    <div className='h-full'>
      <Card className='border-0 shadow-lg h-full'>
        <CardHeader className='text-center pb-6'>
          <div className='mx-auto w-16 h-16 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-full flex items-center justify-center mb-4 shadow-lg'>
            <CloudUpload className='h-8 w-8 text-white' />
          </div>
          <CardTitle className='text-2xl font-bold text-slate-900 dark:text-slate-100'>
            Upload Your Report
          </CardTitle>
          <CardDescription className='text-base text-slate-600 dark:text-slate-400'>
            Upload a PDF or DOCX file for analysis
          </CardDescription>
        </CardHeader>

        <CardContent className='flex-1'>
          <div
            className={`relative flex flex-col items-center justify-center border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 h-64 cursor-pointer ${
              dragActive
                ? 'border-blue-600 bg-blue-100 dark:bg-blue-900/50'
                : isUploading
                  ? 'border-emerald-600 bg-emerald-100 dark:bg-emerald-900/50'
                  : 'border-slate-400 dark:border-slate-500 hover:border-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() =>
              !isUploading && document.getElementById('file-upload')?.click()
            }
          >
            {isUploading ? (
              <div className='space-y-4 w-full max-w-xs'>
                <div className='animate-spin rounded-full h-12 w-12 border-4 border-green-600 border-t-transparent mx-auto' />
                <div className='space-y-2'>
                  <p className='text-sm font-semibold text-green-700 dark:text-green-300'>
                    {getProgressMessage()}
                  </p>
                  <Progress value={uploadProgress} className='h-2' />
                  <p className='text-xs text-slate-600 dark:text-slate-400'>
                    {processingStage === 'uploading'
                      ? `${uploadProgress}% uploaded`
                      : 'Processing...'}
                  </p>
                </div>
              </div>
            ) : (
              <>
                <div
                  className={`p-4 rounded-full mb-4 transition-colors ${
                    dragActive
                      ? 'bg-blue-200 dark:bg-blue-800'
                      : 'bg-slate-200 dark:bg-slate-700'
                  }`}
                >
                  <File
                    className={`h-8 w-8 ${dragActive ? 'text-blue-700 dark:text-blue-300' : 'text-slate-700 dark:text-slate-300'}`}
                  />
                </div>
                <h3 className='text-lg font-semibold mb-2 text-slate-800 dark:text-slate-200'>
                  {dragActive
                    ? 'Drop your file here'
                    : 'Choose a file or drag it here'}
                </h3>
                <p className='text-slate-600 dark:text-slate-400 mb-6 max-w-sm'>
                  Supports PDF and DOCX files up to 60MB. Processing typically
                  takes 30-60 seconds.
                </p>
                <input
                  type='file'
                  id='file-upload'
                  className='hidden'
                  accept='.pdf,.docx,.doc'
                  onChange={handleFileUpload}
                  disabled={isUploading}
                />
                <Button
                  size='lg'
                  disabled={isUploading}
                  className='bg-gradient-to-r from-blue-700 to-indigo-800 hover:from-blue-800 hover:to-indigo-900 py-2 shadow-xl font-bold text-white border-0'
                >
                  <FileText className='mr-2 h-5 w-5' />
                  Select File
                </Button>
              </>
            )}
          </div>
        </CardContent>

        <CardFooter className='justify-center'>
          <div className='flex items-center gap-4 text-xs text-slate-600 dark:text-slate-400'>
            <div className='flex items-center gap-1'>
              <div className='w-2 h-2 bg-green-500 rounded-full'></div>
              <span>PDF, DOCX supported</span>
            </div>
            <div className='flex items-center gap-1'>
              <div className='w-2 h-2 bg-blue-500 rounded-full'></div>
              <span>Max 60MB</span>
            </div>
            <div className='flex items-center gap-1'>
              <div className='w-2 h-2 bg-purple-500 rounded-full'></div>
              <span>Secure processing</span>
            </div>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
