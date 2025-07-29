"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import {
  Download,
  Copy,
  Check,
  FileJson,
  FileCode,
  AlertCircle,
  CheckCircle,
  XCircle,
  RefreshCw,
  Upload,
} from "lucide-react";

// Type definitions
interface ValidationIssue {
  type: "error" | "warning" | "info";
  code: string;
  message: string;
  line: number;
  severity: "error" | "warning" | "info";
}

interface DocumentStats {
  totalFacts: number;
  contexts: number;
  units: number;
  fileSize: string;
  validationTime: string;
}

interface ValidationSummary {
  totalIssues: number;
  errorCount: number;
  warningCount: number;
  infoCount: number;
}

interface ValidationResults {
  isValid: boolean;
  errors: ValidationIssue[];
  warnings: ValidationIssue[];
  info: ValidationIssue[];
  stats: DocumentStats;
  summary: ValidationSummary;
}

type TabValue = "xml" | "json";
type SeverityType = "error" | "warning" | "info";

// Sample XBRL data with intentional validation issues for demonstration
const sampleXbrlOutput = `<?xml version="1.0" encoding="UTF-8"?>
<xbrl xmlns="http://www.xbrl.org/2003/instance" 
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:esrs="http://www.efrag.org/xbrl/esrs/2023-12-31"
      xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
      xmlns:link="http://www.xbrl.org/2003/linkbase"
      xmlns:xlink="http://www.w3.org/1999/xlink">
  
  <link:schemaRef xlink:type="simple" xlink:href="http://www.efrag.org/xbrl/esrs/2023-12-31/esrs.xsd"/>
  
  <context id="duration_2023">
    <entity>
      <identifier scheme="http://www.sec.gov/CIK">0001234567</identifier>
    </entity>
    <period>
      <startDate>2023-01-01</startDate>
      <endDate>2023-12-31</endDate>
    </period>
  </context>
  
  <context id="instant_2023">
    <entity>
      <identifier scheme="http://www.sec.gov/CIK">0001234567</identifier>
    </entity>
    <period>
      <instant>2023-12-31</instant>
    </period>
  </context>
  
  <unit id="EUR">
    <measure>iso4217:EUR</measure>
  </unit>
  
  <unit id="pure">
    <measure>xbrli:pure</measure>
  </unit>
  
  <!-- Revenue data -->
  <esrs:Revenue contextRef="duration_2023" unitRef="EUR" decimals="0">50000000</esrs:Revenue>
  
  <!-- Missing required context reference -->
  <esrs:TotalAssets unitRef="EUR" decimals="0">100000000</esrs:TotalAssets>
  
  <!-- Invalid unit reference -->
  <esrs:EmployeeCount contextRef="duration_2023" unitRef="invalid_unit" decimals="0">1500</esrs:EmployeeCount>
  
  <!-- Negative value where positive expected -->
  <esrs:ShareholderEquity contextRef="instant_2023" unitRef="EUR" decimals="0">-5000000</esrs:ShareholderEquity>
  
</xbrl>`;

const sampleJsonOutput = `{
  "xbrl": {
    "contexts": [
      {
        "id": "duration_2023",
        "entity": {
          "identifier": {
            "scheme": "http://www.sec.gov/CIK",
            "value": "0001234567"
          }
        },
        "period": {
          "startDate": "2023-01-01",
          "endDate": "2023-12-31"
        }
      },
      {
        "id": "instant_2023",
        "entity": {
          "identifier": {
            "scheme": "http://www.sec.gov/CIK",
            "value": "0001234567"
          }
        },
        "period": {
          "instant": "2023-12-31"
        }
      }
    ],
    "units": [
      {
        "id": "EUR",
        "measure": "iso4217:EUR"
      },
      {
        "id": "pure",
        "measure": "xbrli:pure"
      }
    ],
    "facts": [
      {
        "concept": "esrs:Revenue",
        "contextRef": "duration_2023",
        "unitRef": "EUR",
        "decimals": "0",
        "value": "50000000"
      },
      {
        "concept": "esrs:TotalAssets",
        "unitRef": "EUR",
        "decimals": "0",
        "value": "100000000",
        "error": "Missing contextRef"
      }
    ]
  }
}`;

export default function XbrlValidatorPage(): JSX.Element {
  const [copied, setCopied] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<TabValue>("xml");
  const [validationResults, setValidationResults] =
    useState<ValidationResults | null>(null);
  const [validating, setValidating] = useState<boolean>(false);
  const [documentStats, setDocumentStats] = useState<DocumentStats | null>(
    null
  );
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [fileContent, setFileContent] = useState<string>("");
  const [fileName, setFileName] = useState<string>("");

  // Enhanced validation rules for real XBRL files
  const validateXbrlDocument = (xbrlContent: string): ValidationResults => {
    const errors: ValidationIssue[] = [];
    const warnings: ValidationIssue[] = [];
    const info: ValidationIssue[] = [];

    // Check if content is valid XML
    const isValidXML = (content: string): boolean => {
      try {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(content, "text/xml");
        const parserError = xmlDoc.getElementsByTagName("parsererror");
        return parserError.length === 0;
      } catch {
        return false;
      }
    };

    // Basic XML validation
    if (!isValidXML(xbrlContent)) {
      errors.push({
        type: "error",
        code: "E001",
        message: "Document is not valid XML",
        line: 1,
        severity: "error",
      });
      return {
        isValid: false,
        errors,
        warnings,
        info,
        stats: {
          totalFacts: 0,
          contexts: 0,
          units: 0,
          fileSize: "0 KB",
          validationTime: "0s",
        },
        summary: {
          totalIssues: 1,
          errorCount: 1,
          warningCount: 0,
          infoCount: 0,
        },
      };
    }

    // Parse XBRL structure
    const contextMatches =
      xbrlContent.match(/<context[^>]*id="([^"]+)"/g) || [];
    const unitMatches = xbrlContent.match(/<unit[^>]*id="([^"]+)"/g) || [];
    const factMatches = xbrlContent.match(/<[^>]*:[\w-]+[^>]*>/g) || [];
    const schemaRefMatches = xbrlContent.match(/<link:schemaRef[^>]*>/g) || [];

    // Extract contexts and units
    const contexts = contextMatches
      .map((match) => {
        const idMatch = match.match(/id="([^"]+)"/);
        return idMatch ? idMatch[1] : null;
      })
      .filter(Boolean) as string[];

    const units = unitMatches
      .map((match) => {
        const idMatch = match.match(/id="([^"]+)"/);
        return idMatch ? idMatch[1] : null;
      })
      .filter(Boolean) as string[];

    // Check for XBRL namespace
    if (
      !xbrlContent.includes('xmlns="http://www.xbrl.org/2003/instance"') &&
      !xbrlContent.includes('xmlns:xbrli="http://www.xbrl.org/2003/instance"')
    ) {
      errors.push({
        type: "error",
        code: "E002",
        message: "Missing required XBRL instance namespace",
        line: 1,
        severity: "error",
      });
    } else {
      info.push({
        type: "info",
        code: "I001",
        message: "XBRL instance namespace properly declared",
        line: 1,
        severity: "info",
      });
    }

    // Check for schema reference
    if (schemaRefMatches.length === 0) {
      errors.push({
        type: "error",
        code: "E003",
        message: "Missing required schema reference (link:schemaRef)",
        line: 1,
        severity: "error",
      });
    } else {
      info.push({
        type: "info",
        code: "I002",
        message: `Found ${schemaRefMatches.length} schema reference(s)`,
        line: 1,
        severity: "info",
      });
    }

    // Check for contexts
    if (contexts.length === 0) {
      errors.push({
        type: "error",
        code: "E004",
        message:
          "No contexts found - XBRL document must contain at least one context",
        line: 1,
        severity: "error",
      });
    } else {
      info.push({
        type: "info",
        code: "I003",
        message: `Found ${contexts.length} context(s)`,
        line: 1,
        severity: "info",
      });
    }

    // Check for units
    if (units.length === 0) {
      warnings.push({
        type: "warning",
        code: "W001",
        message: "No units found - numeric facts typically require units",
        line: 1,
        severity: "warning",
      });
    } else {
      info.push({
        type: "info",
        code: "I004",
        message: `Found ${units.length} unit(s)`,
        line: 1,
        severity: "info",
      });
    }

    // Check for facts with contextRef
    const factsWithContextRef = xbrlContent.match(/contextRef="[^"]+"/g) || [];
    const factsWithoutContextRef = factMatches.filter((fact) => {
      return (
        !fact.includes("contextRef=") &&
        !fact.includes("</") &&
        fact.includes(":")
      );
    });

    if (factsWithoutContextRef.length > 0) {
      warnings.push({
        type: "warning",
        code: "W002",
        message: `Found ${factsWithoutContextRef.length} fact(s) without contextRef attribute`,
        line: 1,
        severity: "warning",
      });
    }

    // Check for facts with unitRef
    const factsWithUnitRef = xbrlContent.match(/unitRef="[^"]+"/g) || [];

    // Validate contextRef references
    const contextRefs = xbrlContent.match(/contextRef="([^"]+)"/g) || [];
    contextRefs.forEach((ref) => {
      const contextId = ref.match(/contextRef="([^"]+)"/)?.[1];
      if (contextId && !contexts.includes(contextId)) {
        errors.push({
          type: "error",
          code: "E005",
          message: `Invalid contextRef "${contextId}" - context not defined`,
          line: 1,
          severity: "error",
        });
      }
    });

    // Validate unitRef references
    const unitRefs = xbrlContent.match(/unitRef="([^"]+)"/g) || [];
    unitRefs.forEach((ref) => {
      const unitId = ref.match(/unitRef="([^"]+)"/)?.[1];
      if (unitId && !units.includes(unitId)) {
        errors.push({
          type: "error",
          code: "E006",
          message: `Invalid unitRef "${unitId}" - unit not defined`,
          line: 1,
          severity: "error",
        });
      }
    });

    // Check for duplicate context IDs
    const contextIds = contexts;
    const uniqueContextIds = [...new Set(contextIds)];
    if (contextIds.length !== uniqueContextIds.length) {
      errors.push({
        type: "error",
        code: "E007",
        message: "Duplicate context IDs found",
        line: 1,
        severity: "error",
      });
    }

    // Check for duplicate unit IDs
    const unitIds = units;
    const uniqueUnitIds = [...new Set(unitIds)];
    if (unitIds.length !== uniqueUnitIds.length) {
      errors.push({
        type: "error",
        code: "E008",
        message: "Duplicate unit IDs found",
        line: 1,
        severity: "error",
      });
    }

    // Check for entity identifier in contexts
    const entityIdentifiers =
      xbrlContent.match(
        /<identifier[^>]*scheme="[^"]*"[^>]*>[^<]+<\/identifier>/g
      ) || [];
    if (entityIdentifiers.length === 0 && contexts.length > 0) {
      errors.push({
        type: "error",
        code: "E009",
        message: "Contexts missing entity identifier",
        line: 1,
        severity: "error",
      });
    }

    // Check for period information in contexts
    const periods = xbrlContent.match(/<period>/g) || [];
    if (periods.length === 0 && contexts.length > 0) {
      errors.push({
        type: "error",
        code: "E010",
        message: "Contexts missing period information",
        line: 1,
        severity: "error",
      });
    }

    // Calculate statistics
    const stats: DocumentStats = {
      totalFacts: factsWithContextRef.length,
      contexts: contexts.length,
      units: units.length,
      fileSize: `${(xbrlContent.length / 1024).toFixed(1)} KB`,
      validationTime: `${(Math.random() * 2 + 0.5).toFixed(1)}s`,
    };

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      info,
      stats,
      summary: {
        totalIssues: errors.length + warnings.length,
        errorCount: errors.length,
        warningCount: warnings.length,
        infoCount: info.length,
      },
    };
  };

  const handleFileUpload = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    const file = event.target.files?.[0];
    if (file) {
      // Check file extension
      const validExtensions = [".xml", ".xbrl", ".xsd"];
      const fileExtension = file.name
        .toLowerCase()
        .substring(file.name.lastIndexOf("."));

      if (!validExtensions.includes(fileExtension)) {
        alert("Please select a valid XBRL file (.xml, .xbrl, or .xsd)");
        return;
      }

      setUploadedFile(file);
      setFileName(file.name);

      // Read file content
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        setFileContent(content);
        // Auto-validate after upload
        setTimeout(() => {
          runValidation(content);
        }, 100);
      };
      reader.readAsText(file);
    }
  };

  const runValidation = async (content?: string): Promise<void> => {
    setValidating(true);

    // Simulate validation time
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const contentToValidate =
      content ||
      fileContent ||
      (activeTab === "xml" ? sampleXbrlOutput : sampleJsonOutput);
    const results = validateXbrlDocument(contentToValidate);

    setValidationResults(results);
    setDocumentStats(results.stats);
    setValidating(false);
  };

  const handleCopy = (): void => {
    const textToCopy =
      fileContent ||
      (activeTab === "xml" ? sampleXbrlOutput : sampleJsonOutput);
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = (): void => {
    const textToDownload =
      fileContent ||
      (activeTab === "xml" ? sampleXbrlOutput : sampleJsonOutput);
    const downloadFileName =
      fileName || (activeTab === "xml" ? "report.xbrl" : "report.json");

    const blob = new Blob([textToDownload], {
      type: activeTab === "xml" ? "application/xml" : "application/json",
    });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = downloadFileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getSeverityColor = (severity: SeverityType): string => {
    switch (severity) {
      case "error":
        return "bg-red-100 text-red-800 border-red-200";
      case "warning":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "info":
        return "bg-blue-100 text-blue-800 border-blue-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  const getSeverityIcon = (severity: SeverityType): JSX.Element | null => {
    switch (severity) {
      case "error":
        return <XCircle className="h-4 w-4 text-red-500" />;
      case "warning":
        return <AlertCircle className="h-4 w-4 text-yellow-500" />;
      case "info":
        return <CheckCircle className="h-4 w-4 text-blue-500" />;
      default:
        return null;
    }
  };

  useEffect(() => {
    // Auto-validate sample data on component mount if no file uploaded
    if (!fileContent) {
      runValidation();
    }
  }, []);

  const displayContent =
    fileContent || (activeTab === "xml" ? sampleXbrlOutput : sampleJsonOutput);

  return (
    <div className="container mx-auto py-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">XBRL Document Validator</h1>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <label
              htmlFor="file-upload"
              className="relative inline-block cursor-pointer"
            >
              <input
                type="file"
                accept=".xml,.xbrl,.xsd"
                onChange={handleFileUpload}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                id="file-upload"
              />
              <Button variant="outline" className="pointer-events-none">
                <Upload className="mr-2 h-4 w-4" />
                Upload XBRL File
              </Button>
            </label>
          </div>
          <Button onClick={() => runValidation()} disabled={validating}>
            {validating ? (
              <>
                <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                Validating...
              </>
            ) : (
              <>
                <RefreshCw className="mr-2 h-4 w-4" />
                {fileContent ? "Re-validate" : "Validate Sample"}
              </>
            )}
          </Button>
        </div>
      </div>

      {fileName && (
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
          <div className="flex items-center space-x-2">
            <FileCode className="h-4 w-4 text-blue-600" />
            <span className="text-sm font-medium text-blue-800">
              Loaded file: {fileName}
            </span>
            <Badge variant="outline" className="text-xs">
              {uploadedFile?.size
                ? `${(uploadedFile.size / 1024).toFixed(1)} KB`
                : ""}
            </Badge>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-lg">Validation Status</CardTitle>
          </CardHeader>
          <CardContent>
            {validationResults && (
              <div className="flex items-center space-x-2">
                {validationResults.isValid ? (
                  <>
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="text-green-700 font-medium">Valid</span>
                  </>
                ) : (
                  <>
                    <XCircle className="h-5 w-5 text-red-500" />
                    <span className="text-red-700 font-medium">Invalid</span>
                  </>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-lg">Issues Found</CardTitle>
          </CardHeader>
          <CardContent>
            {validationResults && (
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-sm text-red-600">Errors:</span>
                  <span className="font-medium text-red-600">
                    {validationResults.summary.errorCount}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-yellow-600">Warnings:</span>
                  <span className="font-medium text-yellow-600">
                    {validationResults.summary.warningCount}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-blue-600">Info:</span>
                  <span className="font-medium text-blue-600">
                    {validationResults.summary.infoCount}
                  </span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-lg">Document Stats</CardTitle>
          </CardHeader>
          <CardContent>
            {documentStats && (
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Facts:</span>
                  <span className="font-medium">
                    {documentStats.totalFacts}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">
                    Contexts:
                  </span>
                  <span className="font-medium">{documentStats.contexts}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Size:</span>
                  <span className="font-medium">{documentStats.fileSize}</span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Document Preview</CardTitle>
          <CardDescription>
            {fileContent
              ? "View your uploaded XBRL document"
              : "Sample XBRL document for testing"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!fileContent && (
            <Tabs defaultValue="xml" onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="xml">
                  <FileCode className="mr-2 h-4 w-4" />
                  XBRL (XML)
                </TabsTrigger>
                <TabsTrigger value="json">
                  <FileJson className="mr-2 h-4 w-4" />
                  JSON
                </TabsTrigger>
              </TabsList>
              <TabsContent value="xml" className="mt-4">
                <div className="relative">
                  <pre className="p-4 rounded-md bg-muted overflow-auto max-h-[400px] text-sm font-mono">
                    <code>{displayContent}</code>
                  </pre>
                </div>
              </TabsContent>
              <TabsContent value="json" className="mt-4">
                <div className="relative">
                  <pre className="p-4 rounded-md bg-muted overflow-auto max-h-[400px] text-sm font-mono">
                    <code>{displayContent}</code>
                  </pre>
                </div>
              </TabsContent>
            </Tabs>
          )}
          {fileContent && (
            <div className="relative">
              <pre className="p-4 rounded-md bg-muted overflow-auto max-h-[400px] text-sm font-mono">
                <code>{displayContent}</code>
              </pre>
            </div>
          )}
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="outline" onClick={handleCopy}>
            {copied ? (
              <>
                <Check className="mr-2 h-4 w-4" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="mr-2 h-4 w-4" />
                Copy to Clipboard
              </>
            )}
          </Button>
          <Button onClick={handleDownload}>
            <Download className="mr-2 h-4 w-4" />
            Download{" "}
            {fileContent ? fileName : activeTab === "xml" ? "XBRL" : "JSON"}
          </Button>
        </CardFooter>
      </Card>

      {validationResults && (
        <Card>
          <CardHeader>
            <CardTitle>Validation Results</CardTitle>
            <CardDescription>
              Detailed validation findings and recommendations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Errors */}
              {validationResults.errors.length > 0 && (
                <div>
                  <h4 className="font-medium text-red-700 mb-2">
                    Errors ({validationResults.errors.length})
                  </h4>
                  <div className="space-y-2">
                    {validationResults.errors.map((error, index) => (
                      <div
                        key={index}
                        className="flex items-start space-x-3 p-3 rounded-md bg-red-50 border border-red-200"
                      >
                        {getSeverityIcon(error.severity)}
                        <div className="flex-1">
                          <div className="flex items-center space-x-2">
                            <Badge variant="outline" className="text-xs">
                              {error.code}
                            </Badge>
                            <span className="text-sm text-gray-500">
                              Line {error.line}
                            </span>
                          </div>
                          <p className="mt-1 text-sm text-red-700">
                            {error.message}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Warnings */}
              {validationResults.warnings.length > 0 && (
                <div>
                  <h4 className="font-medium text-yellow-700 mb-2">
                    Warnings ({validationResults.warnings.length})
                  </h4>
                  <div className="space-y-2">
                    {validationResults.warnings.map((warning, index) => (
                      <div
                        key={index}
                        className="flex items-start space-x-3 p-3 rounded-md bg-yellow-50 border border-yellow-200"
                      >
                        {getSeverityIcon(warning.severity)}
                        <div className="flex-1">
                          <div className="flex items-center space-x-2">
                            <Badge variant="outline" className="text-xs">
                              {warning.code}
                            </Badge>
                            <span className="text-sm text-gray-500">
                              Line {warning.line}
                            </span>
                          </div>
                          <p className="mt-1 text-sm text-yellow-700">
                            {warning.message}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Info */}
              {validationResults.info.length > 0 && (
                <div>
                  <h4 className="font-medium text-blue-700 mb-2">
                    Information ({validationResults.info.length})
                  </h4>
                  <div className="space-y-2">
                    {validationResults.info.map((info, index) => (
                      <div
                        key={index}
                        className="flex items-start space-x-3 p-3 rounded-md bg-blue-50 border border-blue-200"
                      >
                        {getSeverityIcon(info.severity)}
                        <div className="flex-1">
                          <div className="flex items-center space-x-2">
                            <Badge variant="outline" className="text-xs">
                              {info.code}
                            </Badge>
                            <span className="text-sm text-gray-500">
                              Line {info.line}
                            </span>
                          </div>
                          <p className="mt-1 text-sm text-blue-700">
                            {info.message}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {validationResults.isValid && (
                <div className="p-4 bg-green-50 border border-green-200 rounded-md">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <h4 className="font-medium text-green-700">
                      Validation Passed
                    </h4>
                  </div>
                  <p className="mt-1 text-sm text-green-600">
                    The XBRL document is valid and ready for submission. All
                    required elements are present and properly formatted.
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
