// components/editor/save-export-panel.tsx
"use client";

import { useState } from "react";
import {
  Download,
  Save,
  FileText,
  AlertCircle,
  Eye,
  CheckCircle,
  XCircle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
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

    // Basic validation checks
    if (totalTags === 0) {
      errors.push("No XBRL tags found in the report");
    }

    // Check for contexts
    const contexts = new Set();
    report.blocks.forEach((block) => {
      block.tags.forEach((tag) => {
        contexts.add(tag.context.id);
      });
    });

    if (contexts.size === 0) {
      errors.push("No contexts found for XBRL tags");
    }

    // Check for required ESRS elements
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

    // Check for proper concept naming
    const invalidConcepts = [];
    report.blocks.forEach((block) => {
      block.tags.forEach((tag) => {
        if (!tag.concept.id.includes(":") && !tag.concept.id.includes("_")) {
          invalidConcepts.push(tag.concept.id);
        }
      });
    });

    if (invalidConcepts.length > 0) {
      warnings.push(
        `Concepts may need proper namespace prefixes: ${invalidConcepts
          .slice(0, 3)
          .join(", ")}${invalidConcepts.length > 3 ? "..." : ""}`
      );
    }

    // Check for missing numeric values
    const missingNumericValues = [];
    report.blocks.forEach((block) => {
      block.tags.forEach((tag) => {
        if (
          ["monetary", "decimal", "integer", "percentage"].includes(
            tag.concept.dataType?.toLowerCase()
          )
        ) {
          const content =
            tag.startIndex !== undefined && tag.endIndex !== undefined
              ? block.content.substring(tag.startIndex, tag.endIndex)
              : block.content;

          const hasNumber = /[\d,]+\.?\d*/.test(content);
          if (!hasNumber) {
            missingNumericValues.push(tag.concept.label || tag.concept.id);
          }
        }
      });
    });

    if (missingNumericValues.length > 0) {
      warnings.push(
        `Numeric concepts may be missing values: ${missingNumericValues
          .slice(0, 2)
          .join(", ")}${missingNumericValues.length > 2 ? "..." : ""}`
      );
    }

    // Check for duplicate contexts with same period
    const contextPeriods = new Map();
    report.blocks.forEach((block) => {
      block.tags.forEach((tag) => {
        const key = `${tag.context.periodType}-${tag.context.startDate}-${tag.context.endDate}`;
        if (
          contextPeriods.has(key) &&
          contextPeriods.get(key) !== tag.context.id
        ) {
          warnings.push(
            `Multiple contexts found for same period: ${tag.context.id}`
          );
        }
        contextPeriods.set(key, tag.context.id);
      });
    });

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    };
  };

  const handleValidate = async () => {
    setIsValidating(true);
    try {
      // Simulate validation delay
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
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Save className="h-5 w-5" />
          ESRS Export
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Report Statistics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-3 bg-muted/50 rounded-lg">
            <div className="text-2xl font-bold text-primary">{totalTags}</div>
            <div className="text-sm text-muted-foreground">Total Tags</div>
          </div>
          <div className="text-center p-3 bg-muted/50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{esrsTags}</div>
            <div className="text-sm text-muted-foreground">ESRS Tags</div>
          </div>
        </div>

        {/* Validation Status */}
        {validationResult && (
          <Alert variant={validationResult.isValid ? "default" : "destructive"}>
            {validationResult.isValid ? (
              <CheckCircle className="h-4 w-4" />
            ) : (
              <XCircle className="h-4 w-4" />
            )}
            <AlertDescription>
              {validationResult.isValid
                ? `Validation passed${
                    validationResult.warnings.length > 0
                      ? ` with ${validationResult.warnings.length} warning(s)`
                      : ""
                  }`
                : `Validation failed: ${validationResult.errors.join(", ")}`}
            </AlertDescription>
          </Alert>
        )}

        {/* Status Alert */}
        {totalTags === 0 ? (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              No tags added yet. Add some ESRS tags before exporting.
            </AlertDescription>
          </Alert>
        ) : (
          <Alert>
            <FileText className="h-4 w-4" />
            <AlertDescription>
              Report ready for ESRS iXBRL export with {totalTags} tags (
              {esrsTags} ESRS-specific).
            </AlertDescription>
          </Alert>
        )}

        {/* Export Information */}
        <div className="space-y-2">
          <h4 className="font-medium text-sm">Export Details:</h4>
          <div className="space-y-1 text-xs text-muted-foreground">
            <div className="flex justify-between">
              <span>Format:</span>
              <Badge variant="outline">iXBRL (XHTML)</Badge>
            </div>
            <div className="flex justify-between">
              <span>Schema:</span>
              <Badge variant="outline">ESRS 2023-12-22</Badge>
            </div>
            <div className="flex justify-between">
              <span>Compatible with:</span>
              <Badge variant="outline">Arelle</Badge>
            </div>
            <div className="flex justify-between">
              <span>Last Modified:</span>
              <span>{new Date(report.updatedAt).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-2">
          <Button
            onClick={handleSaveProject}
            disabled={isSaving}
            className="w-full"
            variant="outline"
          >
            <Save className="mr-2 h-4 w-4" />
            {isSaving ? "Saving..." : "Save Project"}
          </Button>

          <Button
            onClick={handleExportXBRL}
            disabled={isExporting || totalTags === 0}
            className="w-full"
          >
            <Download className="mr-2 h-4 w-4" />
            {isExporting ? "Exporting..." : "Export ESRS iXBRL"}
          </Button>
        </div>

        {/* Additional Options */}
        <div className="pt-2 border-t">
          <p className="text-xs text-muted-foreground mb-2">
            Quality Assurance:
          </p>
          <div className="space-y-1">
            {/* Preview Dialog */}
            <Dialog open={showPreview} onOpenChange={setShowPreview}>
              <DialogTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-start h-auto p-2"
                  onClick={handlePreviewXBRL}
                  disabled={totalTags === 0}
                >
                  <Eye className="mr-2 h-3 w-3" />
                  <span className="text-xs">Preview iXBRL Output</span>
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-4xl max-h-[80vh]">
                <DialogHeader>
                  <DialogTitle>ESRS iXBRL Preview</DialogTitle>
                  <DialogDescription>
                    Preview of the generated ESRS iXBRL file (Arelle-compatible)
                  </DialogDescription>
                </DialogHeader>
                <ScrollArea className="h-[500px] w-full rounded border">
                  <pre className="text-xs p-4 whitespace-pre-wrap font-mono">
                    {previewContent}
                  </pre>
                </ScrollArea>
              </DialogContent>
            </Dialog>

            {/* Validate Button */}
            <Button
              variant="ghost"
              size="sm"
              className="w-full justify-start h-auto p-2"
              onClick={handleValidate}
              disabled={isValidating || totalTags === 0}
            >
              {validationResult?.isValid ? (
                <CheckCircle className="mr-2 h-3 w-3 text-green-600" />
              ) : validationResult?.isValid === false ? (
                <XCircle className="mr-2 h-3 w-3 text-red-600" />
              ) : (
                <AlertCircle className="mr-2 h-3 w-3" />
              )}
              <span className="text-xs">
                {isValidating ? "Validating..." : "Validate Report"}
              </span>
            </Button>
          </div>
        </div>

        {/* Validation Details */}
        {validationResult &&
          (validationResult.errors.length > 0 ||
            validationResult.warnings.length > 0) && (
            <div className="pt-2 border-t">
              <div className="space-y-2">
                {validationResult.errors.length > 0 && (
                  <div>
                    <p className="text-xs font-medium text-red-600 mb-1">
                      Errors:
                    </p>
                    <ul className="text-xs text-red-600 space-y-1">
                      {validationResult.errors.map((error, index) => (
                        <li key={index}>• {error}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {validationResult.warnings.length > 0 && (
                  <div>
                    <p className="text-xs font-medium text-yellow-600 mb-1">
                      Warnings:
                    </p>
                    <ul className="text-xs text-yellow-600 space-y-1">
                      {validationResult.warnings.map((warning, index) => (
                        <li key={index}>• {warning}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

        {/* Arelle Instructions */}
        <div className="pt-2 border-t">
          <p className="text-xs text-muted-foreground mb-1">Open in Arelle:</p>
          <div className="text-xs text-muted-foreground space-y-1">
            <p>1. Download and open the generated XHTML file</p>
            <p>2. In Arelle: File → Open → Select the XHTML file</p>
            <p>3. Use Tools → Validate to check ESRS compliance</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
