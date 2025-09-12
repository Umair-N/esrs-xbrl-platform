'use client';

import { useState } from 'react';
import {
  Download,
  Save,
  FileText,
  AlertCircle,
  Eye,
  CheckCircle,
  XCircle,
  Shield,
  Zap,
  BarChart3,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import type { ReportDocument } from '@/types/report';
import { downloadXBRLFile, previewXBRLContent } from '@/lib/xbrl';

interface SaveExportPanelProps {
  report: ReportDocument;
  onSave?: (report: ReportDocument) => void;
}

export function SaveExportPanel({ report, onSave }: SaveExportPanelProps) {
  const [isSaving, setIsSaving] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [previewContent, setPreviewContent] = useState<string>('');
  const [validationResult, setValidationResult] = useState<{
    isValid: boolean;
    errors: string[];
    warnings: string[];
  } | null>(null);

  const totalTags = report.blocks.reduce(
    (sum, block) => sum + block.tags.length,
    0
  );

  const taggedBlocks = report.blocks.filter(
    (block) => block.tags.length > 0
  ).length;

  const esrsTags = report.blocks.reduce(
    (sum, block) =>
      sum +
      block.tags.filter((tag) => tag.concept.id.toLowerCase().includes('esrs'))
        .length,
    0
  );

  const completionPercentage = Math.round(
    (taggedBlocks / report.blocks.length) * 100
  );

  const handleSaveProject = async () => {
    setIsSaving(true);
    try {
      const updatedReport = {
        ...report,
        updatedAt: new Date().toISOString(),
      };
      localStorage.setItem(
        `report_${report.id}`,
        JSON.stringify(updatedReport)
      );
      if (onSave) {
        onSave(updatedReport);
      }
      console.log('ESRS Report saved successfully');
    } catch (error) {
      console.error('Error saving report:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleExportXBRL = async () => {
    setIsExporting(true);
    try {
      downloadXBRLFile(report);
    } catch (error) {
      console.error('Error exporting iXBRL:', error);
      alert(
        'Error exporting iXBRL file. Please check the console for details.'
      );
    } finally {
      setIsExporting(false);
    }
  };

  const handlePreviewXBRL = () => {
    try {
      const content = previewXBRLContent(report);
      setPreviewContent(content);
      setShowPreview(true);
    } catch (error) {
      console.error('Error generating preview:', error);
      alert('Error generating preview. Please check the console for details.');
    }
  };

  const validateReport = (): {
    isValid: boolean;
    errors: string[];
    warnings: string[];
  } => {
    const errors: string[] = [];
    const warnings: string[] = [];

    if (totalTags === 0) {
      errors.push('No XBRL tags found in the report');
    }

    const contexts = new Set();
    report.blocks.forEach((block) => {
      block.tags.forEach((tag) => {
        // Fix: Check if tag.context exists before accessing its id
        if (tag.context?.id) {
          contexts.add(tag.context.id);
        }
      });
    });

    if (contexts.size === 0) {
      errors.push('No contexts found for XBRL tags');
    }

    const hasClimateDisclosure = report.blocks.some((block) =>
      block.tags.some(
        (tag) =>
          tag.concept.id.toLowerCase().includes('climate') ||
          tag.concept.id.toLowerCase().includes('ghg')
      )
    );

    if (!hasClimateDisclosure) {
      warnings.push(
        'No climate-related disclosures found. Consider adding ESRS E1 elements.'
      );
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    };
  };

  const handleValidate = async () => {
    setIsValidating(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const result = validateReport();
      setValidationResult(result);
    } catch (error) {
      console.error('Error validating report:', error);
      setValidationResult({
        isValid: false,
        errors: ['Validation failed due to an error'],
        warnings: [],
      });
    } finally {
      setIsValidating(false);
    }
  };

  return (
    <div className='space-y-4'>
      {/* Progress Overview */}
      <Card className='border-0 shadow-sm bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20'>
        <CardHeader className='pb-2'>
          <CardTitle className='flex items-center gap-2 text-sm'>
            <BarChart3 className='w-4 h-4 text-blue-600' />
            Progress
          </CardTitle>
        </CardHeader>
        <CardContent className='space-y-3'>
          <div className='space-y-1'>
            <div className='flex justify-between text-xs'>
              <span>Completion</span>
              <span className='font-medium'>{completionPercentage}%</span>
            </div>
            <Progress value={completionPercentage} className='h-1.5' />
          </div>

          <div className='grid grid-cols-1 gap-2'>
            <div className='p-2 text-center border rounded bg-white/60 dark:bg-slate-800/60'>
              <div className='text-lg font-bold text-blue-600'>{totalTags}</div>
              <div className='text-xs text-muted-foreground'>Total Tags</div>
            </div>
            <div className='p-2 text-center border rounded bg-white/60 dark:bg-slate-800/60'>
              <div className='text-lg font-bold text-emerald-600'>
                {esrsTags}
              </div>
              <div className='text-xs text-muted-foreground'>Tags</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Status Alert */}
      <Card className='border-0 shadow-sm'>
        <CardContent className='p-3'>
          {totalTags === 0 ? (
            <Alert variant='destructive' className='border-0'>
              <AlertCircle className='w-3 h-3' />
              <AlertDescription className='text-xs'>
                No tags added yet. Add some tags before exporting.
              </AlertDescription>
            </Alert>
          ) : (
            <Alert className='border-0 bg-blue-50 dark:bg-blue-950/20'>
              <FileText className='w-3 h-3 text-blue-600' />
              <AlertDescription className='text-xs'>
                <span className='font-medium'>Ready!</span> {totalTags} tags (
                {esrsTags} ) ready for export.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Export & Session Controls */}
      <div className='space-y-2'>
        {/* Save Session Button */}
        <Button
          onClick={handleSaveProject}
          disabled={isSaving}
          className='w-full text-sm bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800'
          size='sm'
        >
          {isSaving ? (
            <>
              <div className='w-3 h-3 mr-2 border-2 border-white rounded-full animate-spin border-t-transparent' />
              Saving...
            </>
          ) : (
            <>
              <Save className='w-3 h-3 mr-2' />
              Save Session
            </>
          )}
        </Button>

        {/* Export XBRL Button */}
        <Button
          onClick={handleExportXBRL}
          disabled={isExporting || totalTags === 0}
          className='w-full text-sm bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
          size='sm'
        >
          {isExporting ? (
            <>
              <div className='w-3 h-3 mr-2 border-2 border-white rounded-full animate-spin border-t-transparent' />
              Exporting...
            </>
          ) : (
            <>
              <Download className='w-3 h-3 mr-2' />
              Export iXBRL
            </>
          )}
        </Button>

        <div className='grid grid-cols-2 gap-2'>
          {/* Preview Button */}
          <Dialog open={showPreview} onOpenChange={setShowPreview}>
            <DialogTrigger asChild>
              <Button
                variant='outline'
                size='sm'
                onClick={handlePreviewXBRL}
                disabled={totalTags === 0}
                className='text-xs'
              >
                <Eye className='w-3 h-3 mr-1' />
                Preview
              </Button>
            </DialogTrigger>
            <DialogContent className='max-w-4xl max-h-[80vh]'>
              <DialogHeader>
                <DialogTitle className='flex items-center gap-2'>
                  <FileText className='w-5 h-5' />
                  iXBRL Preview
                </DialogTitle>
                <DialogDescription>
                  Preview of the generated iXBRL file
                </DialogDescription>
              </DialogHeader>
              <ScrollArea className='h-[500px] w-full rounded border'>
                <pre className='p-4 font-mono text-xs whitespace-pre-wrap'>
                  {previewContent}
                </pre>
              </ScrollArea>
            </DialogContent>
          </Dialog>

          {/* Validate Button */}
          <Button
            variant='outline'
            size='sm'
            onClick={handleValidate}
            disabled={isValidating || totalTags === 0}
            className='text-xs'
          >
            {isValidating ? (
              <>
                <div className='w-2 h-2 mr-1 border-2 border-current rounded-full animate-spin border-t-transparent' />
                Validating...
              </>
            ) : validationResult?.isValid ? (
              <>
                <CheckCircle className='w-3 h-3 mr-1 text-emerald-600' />
                Valid
              </>
            ) : validationResult?.isValid === false ? (
              <>
                <XCircle className='w-3 h-3 mr-1 text-red-600' />
                Invalid
              </>
            ) : (
              <>
                <Shield className='w-3 h-3 mr-1' />
                Validate
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Validation Results */}
      {validationResult && (
        <Card className='border-0 shadow-sm'>
          <CardContent className='p-3'>
            <div className='space-y-2'>
              {validationResult.errors.length > 0 && (
                <div className='space-y-1'>
                  <h4 className='flex items-center gap-1 text-xs font-medium text-red-600'>
                    <XCircle className='w-3 h-3' />
                    Errors ({validationResult.errors.length})
                  </h4>
                  <div className='space-y-1'>
                    {validationResult.errors.map((error, index) => (
                      <div
                        key={index}
                        className='p-2 text-xs text-red-600 rounded bg-red-50 dark:bg-red-950/20'
                      >
                        • {error}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {validationResult.warnings.length > 0 && (
                <div className='space-y-1'>
                  <h4 className='flex items-center gap-1 text-xs font-medium text-amber-600'>
                    <AlertCircle className='w-3 h-3' />
                    Warnings ({validationResult.warnings.length})
                  </h4>
                  <div className='space-y-1'>
                    {validationResult.warnings.map((warning, index) => (
                      <div
                        key={index}
                        className='p-2 text-xs rounded text-amber-600 bg-amber-50 dark:bg-amber-950/20'
                      >
                        • {warning}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
