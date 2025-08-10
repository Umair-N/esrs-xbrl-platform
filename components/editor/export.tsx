"use client";

import { useState } from "react";
import { Download, Save, FileText, AlertCircle, Eye, CheckCircle, XCircle, Shield, Zap, BarChart3 } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { ReportDocument } from "@/types/report";
import { downloadXBRLFile, previewXBRLContent } from "@/lib/xbrl";

interface SaveExportPanelProps {
  report: ReportDocument;
  onSave?: (report: ReportDocument) => void;
}

export function SaveExportPanel({ report, onSave }: SaveExportPanelProps) {
  const [isSaving, setIsSaving] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [previewContent, setPreviewContent] = useState<string>("");
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
      block.tags.filter((tag) => tag.concept.id.toLowerCase().includes("esrs"))
        .length,
    0
  );

  const completionPercentage = Math.round((taggedBlocks / report.blocks.length) * 100);

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
      console.log("ESRS Report saved successfully");
    } catch (error) {
      console.error("Error saving report:", error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleExportXBRL = async () => {
    setIsExporting(true);
    try {
      downloadXBRLFile(report);
    } catch (error) {
      console.error("Error exporting iXBRL:", error);
      alert(
        "Error exporting iXBRL file. Please check the console for details."
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
      console.error("Error generating preview:", error);
      alert("Error generating preview. Please check the console for details.");
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
      errors.push("No XBRL tags found in the report");
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
      errors.push("No contexts found for XBRL tags");
    }

    const hasClimateDisclosure = report.blocks.some((block) =>
      block.tags.some(
        (tag) =>
          tag.concept.id.toLowerCase().includes("climate") ||
          tag.concept.id.toLowerCase().includes("ghg")
      )
    );

    if (!hasClimateDisclosure) {
      warnings.push(
        "No climate-related disclosures found. Consider adding ESRS E1 elements."
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
      console.error("Error validating report:", error);
      setValidationResult({
        isValid: false,
        errors: ["Validation failed due to an error"],
        warnings: [],
      });
    } finally {
      setIsValidating(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Progress Overview */}
      <Card className="border-0 shadow-sm bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20">
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center gap-2 text-sm">
            <BarChart3 className="h-4 w-4 text-blue-600" />
            Progress
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="space-y-1">
            <div className="flex justify-between text-xs">
              <span>Completion</span>
              <span className="font-medium">{completionPercentage}%</span>
            </div>
            <Progress value={completionPercentage} className="h-1.5" />
          </div>
          
          <div className="grid grid-cols-1 gap-2">
            <div className="text-center p-2 bg-white/60 dark:bg-slate-800/60 rounded border">
              <div className="text-lg font-bold text-blue-600">{totalTags}</div>
              <div className="text-xs text-muted-foreground">Total Tags</div>
            </div>
            <div className="text-center p-2 bg-white/60 dark:bg-slate-800/60 rounded border">
              <div className="text-lg font-bold text-emerald-600">{esrsTags}</div>
              <div className="text-xs text-muted-foreground">ESRS Tags</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Status Alert */}
      <Card className="border-0 shadow-sm">
        <CardContent className="p-3">
          {totalTags === 0 ? (
            <Alert variant="destructive" className="border-0">
              <AlertCircle className="h-3 w-3" />
              <AlertDescription className="text-xs">
                No tags added yet. Add some ESRS tags before exporting.
              </AlertDescription>
            </Alert>
          ) : (
            <Alert className="border-0 bg-blue-50 dark:bg-blue-950/20">
              <FileText className="h-3 w-3 text-blue-600" />
              <AlertDescription className="text-xs">
                <span className="font-medium">Ready!</span> {totalTags} tags ({esrsTags} ESRS) ready for export.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Export Buttons */}
      <div className="space-y-2">
        <Button
          onClick={handleExportXBRL}
          disabled={isExporting || totalTags === 0}
          className="w-full text-sm bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
          size="sm"
        >
          {isExporting ? (
            <>
              <div className="animate-spin rounded-full h-3 w-3 border-2 border-white border-t-transparent mr-2" />
              Exporting...
            </>
          ) : (
            <>
              <Download className="mr-2 h-3 w-3" />
              Export iXBRL
            </>
          )}
        </Button>

        <div className="grid grid-cols-2 gap-2">
          <Dialog open={showPreview} onOpenChange={setShowPreview}>
            <DialogTrigger asChild>
              <Button
                variant="outline"
                size="sm"
                onClick={handlePreviewXBRL}
                disabled={totalTags === 0}
                className="text-xs"
              >
                <Eye className="mr-1 h-3 w-3" />
                Preview
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-4xl max-h-[80vh]">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  ESRS iXBRL Preview
                </DialogTitle>
                <DialogDescription>
                  Preview of the generated ESRS iXBRL file
                </DialogDescription>
              </DialogHeader>
              <ScrollArea className="h-[500px] w-full rounded border">
                <pre className="text-xs p-4 whitespace-pre-wrap font-mono">
                  {previewContent}
                </pre>
              </ScrollArea>
            </DialogContent>
          </Dialog>

          <Button
            variant="outline"
            size="sm"
            onClick={handleValidate}
            disabled={isValidating || totalTags === 0}
            className="text-xs"
          >
            {isValidating ? (
              <>
                <div className="animate-spin rounded-full h-2 w-2 border-2 border-current border-t-transparent mr-1" />
                Validating...
              </>
            ) : validationResult?.isValid ? (
              <>
                <CheckCircle className="mr-1 h-3 w-3 text-emerald-600" />
                Valid
              </>
            ) : validationResult?.isValid === false ? (
              <>
                <XCircle className="mr-1 h-3 w-3 text-red-600" />
                Invalid
              </>
            ) : (
              <>
                <Shield className="mr-1 h-3 w-3" />
                Validate
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Validation Results */}
      {validationResult && (
        <Card className="border-0 shadow-sm">
          <CardContent className="p-3">
            <div className="space-y-2">
              {validationResult.errors.length > 0 && (
                <div className="space-y-1">
                  <h4 className="text-xs font-medium text-red-600 flex items-center gap-1">
                    <XCircle className="h-3 w-3" />
                    Errors ({validationResult.errors.length})
                  </h4>
                  <div className="space-y-1">
                    {validationResult.errors.map((error, index) => (
                      <div key={index} className="text-xs text-red-600 bg-red-50 dark:bg-red-950/20 p-2 rounded">
                        • {error}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {validationResult.warnings.length > 0 && (
                <div className="space-y-1">
                  <h4 className="text-xs font-medium text-amber-600 flex items-center gap-1">
                    <AlertCircle className="h-3 w-3" />
                    Warnings ({validationResult.warnings.length})
                  </h4>
                  <div className="space-y-1">
                    {validationResult.warnings.map((warning, index) => (
                      <div key={index} className="text-xs text-amber-600 bg-amber-50 dark:bg-amber-950/20 p-2 rounded">
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