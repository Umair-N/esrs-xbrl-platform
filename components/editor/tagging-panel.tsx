"use client"

import React, { useState, useEffect, useMemo } from "react"
import { Search, Tag, Plus, AlertCircle, ChevronRight, ChevronDown, Folder, FolderOpen, FileText, Calculator, Sparkles, Target, Info } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import type { ReportDocument, XbrlTag } from "@/types/report"
import { sampleContexts } from "@/lib/sample-data"
import { generateUniqueId } from "@/lib/utils"
import { getTaxonomyData, searchTaxonomy, flattenTree } from "@/lib/taxomony-data"
import type { TaxonomyNode } from "@/types/taxonomy"

interface TaggingPanelProps {
  report: ReportDocument
  selectedBlockId: string | null
  highlightedText: {
    text: string
    startIndex: number
    endIndex: number
  } | null
  onReportChange: (report: ReportDocument) => void
}

// First, you'll need to update your type definition in @/types/report.ts:
// Change: context: XbrlContext
// To: context?: XbrlContext
// This makes context optional in XbrlTag interface

// Tree Node Component for Taxonomy Browser
const TaxonomyTreeNode = ({
  node,
  level = 0,
  onSelect,
  selectedId,
  searchQuery,
}: {
  node: TaxonomyNode
  level?: number
  onSelect: (node: TaxonomyNode) => void
  selectedId?: string
  searchQuery: string
}) => {
  const [isExpanded, setIsExpanded] = useState(false)
  const hasChildren = node.children && node.children.length > 0
  const hasCalculations = node.calculations && node.calculations.length > 0
  const isSelected = selectedId === node.id
  const matchesSearch =
    !searchQuery ||
    node.label?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    node.id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (node.name && node.name.toLowerCase().includes(searchQuery.toLowerCase()))

  const getIcon = () => {
    if (hasChildren) {
      return isExpanded ? <FolderOpen className="h-3 w-3" /> : <Folder className="h-3 w-3" />
    }
    return <FileText className="h-3 w-3" />
  }

  const getBadgeColor = (labelType?: string) => {
    switch (labelType) {
      case "abstract":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
      case "table":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
      case "axis":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300"
      case "member":
        return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300"
      case "text block":
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
    }
  }

  if (!matchesSearch && !hasChildren) return null

  return (
    <div className="select-none">
      <div
        className={`flex items-start py-2 px-2 rounded-sm cursor-pointer hover:bg-muted/50 transition-colors ${
          isSelected ? "bg-primary/10 border-l-2 border-primary" : ""
        }`}
        style={{ paddingLeft: `${level * 12 + 8}px` }}
        onClick={() => onSelect(node)}
      >
        {hasChildren && (
          <Button
            variant="ghost"
            size="sm"
            className="h-4 w-4 p-0 mr-1 hover:bg-muted flex-shrink-0 mt-0.5"
            onClick={(e) => {
              e.stopPropagation()
              setIsExpanded(!isExpanded)
            }}
            aria-label={isExpanded ? "Collapse node" : "Expand node"}
          >
            {isExpanded ? <ChevronDown className="h-2 w-2" /> : <ChevronRight className="h-2 w-2" />}
          </Button>
        )}
        <div className="flex items-start min-w-0 flex-1">
          <span className="mr-1 text-muted-foreground flex-shrink-0 mt-0.5">{getIcon()}</span>
          <div className="min-w-0 flex-1">
            <div className="font-medium text-xs flex items-start gap-1 min-w-0">
              <span className="break-words leading-tight" title={node.label ?? ""}>
                {node.label}
              </span>
              {hasCalculations && <Calculator className="h-2 w-2 text-blue-500 flex-shrink-0 mt-0.5" />}
            </div>
            <div className="flex items-start gap-1 mt-1 min-w-0 flex-wrap">
              <span className="text-xs text-muted-foreground font-mono break-all leading-tight" title={node.id ?? ""}>
                {node.id}
              </span>
              {node.labelType && (
                <Badge variant="outline" className={`text-xs h-4 px-1 flex-shrink-0 ${getBadgeColor(node.labelType)}`}>
                  {node.labelType}
                </Badge>
              )}
            </div>
          </div>
        </div>
      </div>
      {hasChildren && isExpanded && (
        <div>
          {node.children?.map((child, index) => (
            <TaxonomyTreeNode
              key={`${child.id}-${index}`}
              node={child}
              level={level + 1}
              onSelect={onSelect}
              selectedId={selectedId}
              searchQuery={searchQuery}
            />
          ))}
        </div>
      )}
    </div>
  )
}

const TaggingPanel: React.FC<TaggingPanelProps> = ({ report, selectedBlockId, highlightedText, onReportChange }) => {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedConcept, setSelectedConcept] = useState<TaxonomyNode | null>(null)
  const [selectedContextId, setSelectedContextId] = useState<string | null>(null)
  const [viewMode, setViewMode] = useState<"tree" | "search">("tree")

  const taxonomyData = useMemo(() => {
    try {
      return getTaxonomyData()
    } catch (error) {
      console.error("Error loading taxonomy data:", error)
      return null
    }
  }, [])

  const allNodes = useMemo(() => {
    if (!taxonomyData || !taxonomyData.children) return []
    return flattenTree(taxonomyData.children)
  }, [taxonomyData])

  const filteredConcepts = useMemo(() => {
    if (!searchQuery) return []
    return searchTaxonomy(allNodes, searchQuery)
  }, [searchQuery, allNodes])

  const selectedBlock = selectedBlockId ? report.blocks.find((block) => block.id === selectedBlockId) : null

  useEffect(() => {
    setSelectedConcept(null)
    setSelectedContextId(null)
    setSearchQuery("")
  }, [selectedBlockId])

  useEffect(() => {
    setViewMode(searchQuery ? "search" : "tree")
  }, [searchQuery])

  const handleAddTag = () => {
    if (!selectedBlockId || !selectedConcept) return

    // Only use context if one is explicitly selected
    const contextToUse = selectedContextId 
      ? sampleContexts.find((c) => c.id === selectedContextId) 
      : undefined

    const newTag: XbrlTag = {
      id: generateUniqueId(),
      concept: {
        id: selectedConcept.id,
        label: selectedConcept.label,
        type: selectedConcept.type || "string",
        definition: selectedConcept.originalLabel || selectedConcept.label,
        periodType: (selectedConcept.periodType as "instant" | "duration") || "duration",
        dataType: selectedConcept.type || "xbrli:stringItemType",
        balance: undefined,
        abstract: selectedConcept.abstract === "true",
        labels: selectedConcept.originalLabel ? [{ value: selectedConcept.originalLabel, role: "label" }] : undefined,
        references: undefined,
      },
      ...(contextToUse && { context: contextToUse }), // Only add context if it exists
      createdAt: new Date().toISOString(),
      startIndex: highlightedText?.startIndex || 0,
      endIndex: highlightedText?.endIndex || 0,
    }

    const updatedReport = {
      ...report,
      blocks: report.blocks.map((block) =>
        block.id === selectedBlockId ? { ...block, tags: [...block.tags, newTag] } : block,
      ),
      updatedAt: new Date().toISOString(),
    }

    onReportChange(updatedReport)
    setSelectedConcept(null)
    // Don't reset context selection to allow reuse
    setSearchQuery("")
  }

  if (!taxonomyData) {
    return (
      <div className="space-y-4">
        <Card className="border-0 shadow-sm">
          <CardContent className="p-6">
            <Alert variant="destructive" className="flex items-center gap-2">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <div>
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>Failed to load ESRS taxonomy data. Please check your taxonomy file.</AlertDescription>
              </div>
            </Alert>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6 w-full">
      {!selectedBlock ? (
        <Card className="border-0 shadow-sm bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900">
          <CardContent className="p-8 text-center">
            <div className="mx-auto w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
              <Target className="h-8 w-8 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Select Text to Tag</h3>
            <p className="text-sm text-muted-foreground">
              Choose a block of text from the document to start adding ESRS tags
            </p>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Selected Text Display */}
          <Card className="border-0 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-base">
                <FileText className="h-4 w-4 text-blue-600" />
                Selected Text
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="p-3 border-2 border-dashed border-blue-200 dark:border-blue-800 rounded-lg bg-blue-50/50 dark:bg-blue-950/20">
                {highlightedText && highlightedText.text ? (
                  <div className="space-y-2">
                    <Badge variant="secondary" className="text-xs">
                      Highlighted Selection
                    </Badge>
                    <p className="text-sm bg-primary/20 px-2 py-1 rounded break-words">
                      {highlightedText.text}
                    </p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Badge variant="outline" className="text-xs">
                      Full Block
                    </Badge>
                    <p className="text-sm break-words">
                      {selectedBlock.content.length > 150
                        ? `${selectedBlock.content.substring(0, 150)}...`
                        : selectedBlock.content}
                    </p>
                  </div>
                )}
              </div>
              
              {!highlightedText?.text && (
                <Alert className="border-amber-200 bg-amber-50 dark:bg-amber-950/20">
                  <Sparkles className="h-4 w-4 text-amber-600" />
                  <AlertDescription className="text-amber-800 dark:text-amber-200">
                    <strong>Tip:</strong> Highlight specific text within this block for more precise tagging
                  </AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* ESRS Taxonomy Concept Section */}
          <Card className="border-0 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-base">
                <Tag className="h-4 w-4 text-emerald-600" />
                ESRS Taxonomy
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Search Input */}
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search ESRS concepts..."
                  className="pl-10 h-10 border-2 focus:border-emerald-500"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>

              {/* Selected Concept Display */}
              {selectedConcept && (
                <div className="p-4 bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-950/20 dark:to-green-950/20 rounded-lg border-2 border-emerald-200 dark:border-emerald-800">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <h4 className="font-semibold text-sm text-emerald-900 dark:text-emerald-100 break-words">
                        {selectedConcept.label}
                      </h4>
                      <p className="text-xs text-emerald-700 dark:text-emerald-300 font-mono break-all mt-1">
                        {selectedConcept.id}
                      </p>
                    </div>
                    {selectedConcept.labelType && (
                      <Badge variant="outline" className="text-xs bg-white dark:bg-slate-800 flex-shrink-0">
                        {selectedConcept.labelType}
                      </Badge>
                    )}
                  </div>
                </div>
              )}

              {/* Taxonomy Browser Container */}
              <Card className="border-2">
                <CardHeader className="py-3 bg-muted/30">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-medium">
                      {viewMode === "search"
                        ? `${filteredConcepts.length} search results`
                        : `${taxonomyData.label || "ESRS Taxonomy"} - ${allNodes.length} concepts`}
                    </h4>
                    <Badge variant="secondary" className="text-xs">
                      {viewMode === "search" ? "Search" : "Browse"}
                    </Badge>
                  </div>
                </CardHeader>
                <ScrollArea className="h-[300px]">
                  <div className="p-3">
                    {viewMode === "search" ? (
                      filteredConcepts.length === 0 ? (
                        <div className="text-center py-8 text-muted-foreground">
                          <Search className="h-8 w-8 mx-auto mb-3 opacity-50" />
                          <p className="text-sm">No results found for "{searchQuery}"</p>
                          <p className="text-xs mt-1">Try different keywords or browse the taxonomy</p>
                        </div>
                      ) : (
                        <div className="space-y-1">
                          {filteredConcepts.map((concept, index) => (
                            <div
                              key={`${concept.id}-${index}`}
                              className={`p-3 cursor-pointer hover:bg-muted rounded-md transition-colors border ${
                                selectedConcept?.id === concept.id 
                                  ? "bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800" 
                                  : "border-transparent hover:border-muted-foreground/20"
                              }`}
                              onClick={() => setSelectedConcept(concept)}
                            >
                              <div className="flex items-start gap-2">
                                <FileText className="h-4 w-4 text-muted-foreground flex-shrink-0 mt-0.5" />
                                <div className="flex-1 min-w-0">
                                  <div className="font-medium text-sm flex items-start gap-2">
                                    <span className="break-words leading-tight" title={concept.label ?? ""}>
                                      {concept.label}
                                    </span>
                                    {concept.calculations && concept.calculations.length > 0 && (
                                      <Calculator className="h-3 w-3 text-blue-500 flex-shrink-0 mt-0.5" />
                                    )}
                                  </div>
                                  <div className="flex items-center gap-2 mt-1">
                                    <span className="text-xs text-muted-foreground font-mono break-all" title={concept.id ?? ""}>
                                      {concept.id}
                                    </span>
                                    {concept.labelType && (
                                      <Badge variant="outline" className="text-xs h-4 px-1">
                                        {concept.labelType}
                                      </Badge>
                                    )}
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )
                    ) : (
                      <div>
                        {taxonomyData.children.map((child, index) => (
                          <TaxonomyTreeNode
                            key={`${child.id}-${index}`}
                            node={child}
                            onSelect={setSelectedConcept}
                            selectedId={selectedConcept?.id}
                            searchQuery=""
                          />
                        ))}
                      </div>
                    )}
                  </div>
                </ScrollArea>
              </Card>
            </CardContent>
          </Card>

          {/* Context Selection - Now Optional */}
          <Card className="border-0 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                Context Selection
                <Badge variant="secondary" className="text-xs">Optional</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Select value={selectedContextId || ""} onValueChange={setSelectedContextId}>
                <SelectTrigger className="h-10">
                  <SelectValue placeholder="Select a reporting context (optional)" />
                </SelectTrigger>
                <SelectContent>
                  {sampleContexts.map((context) => (
                    <SelectItem key={context.id} value={context.id}>
                      <div className="flex flex-col items-start">
                        <span className="font-medium">{context.label}</span>
                        <span className="text-xs text-muted-foreground">
                          {context.entityName} • {context.periodType}
                        </span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              {!selectedContextId && (
                <Alert className="border-blue-200 bg-blue-50 dark:bg-blue-950/20">
                  <Info className="h-4 w-4 text-blue-600" />
                  <AlertDescription className="text-blue-800 dark:text-blue-200">
                    No context selected. Tag will be created without context information.
                  </AlertDescription>
                </Alert>
              )}
              
              {selectedContextId && (
                <div className="p-3 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 rounded-lg border border-blue-200 dark:border-blue-800">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-sm text-blue-900 dark:text-blue-100">
                        {sampleContexts.find(c => c.id === selectedContextId)?.label}
                      </h4>
                      <p className="text-xs text-blue-700 dark:text-blue-300 mt-1">
                        {sampleContexts.find(c => c.id === selectedContextId)?.entityName} • 
                        {sampleContexts.find(c => c.id === selectedContextId)?.periodType}
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-6 w-6 p-0 text-blue-600"
                      onClick={() => setSelectedContextId(null)}
                    >
                      ×
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Selected Concept Details */}
          {selectedConcept && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Concept Details</CardTitle>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="basic" className="w-full">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="basic">Basic Info</TabsTrigger>
                    <TabsTrigger value="properties">Properties</TabsTrigger>
                  </TabsList>
                  <TabsContent value="basic" className="space-y-3 mt-4">
                    <div className="grid grid-cols-2 gap-3">
                      <div className="space-y-1">
                        <label className="text-xs font-medium text-muted-foreground">Type</label>
                        <div className="text-sm p-2 bg-muted/50 rounded">
                          {selectedConcept.type || "N/A"}
                        </div>
                      </div>
                      <div className="space-y-1">
                        <label className="text-xs font-medium text-muted-foreground">Period</label>
                        <div className="text-sm p-2 bg-muted/50 rounded">
                          {selectedConcept.periodType || "N/A"}
                        </div>
                      </div>
                      <div className="space-y-1">
                        <label className="text-xs font-medium text-muted-foreground">Abstract</label>
                        <div className="text-sm p-2 bg-muted/50 rounded">
                          {selectedConcept.abstract === "true" ? "Yes" : "No"}
                        </div>
                      </div>
                      <div className="space-y-1">
                        <label className="text-xs font-medium text-muted-foreground">Order</label>
                        <div className="text-sm p-2 bg-muted/50 rounded">
                          {selectedConcept.order || "N/A"}
                        </div>
                      </div>
                    </div>
                    {selectedConcept.originalLabel && (
                      <div className="space-y-1">
                        <label className="text-xs font-medium text-muted-foreground">Original Label</label>
                        <div className="text-sm p-3 bg-muted/50 rounded break-words">
                          {selectedConcept.originalLabel}
                        </div>
                      </div>
                    )}
                  </TabsContent>
                  <TabsContent value="properties" className="mt-4">
                    <ScrollArea className="h-32">
                      <div className="space-y-2">
                        {Object.entries(selectedConcept).map(([key, value]) => {
                          if (key === "children" || !value) return null
                          return (
                            <div key={key} className="flex justify-between items-start gap-2 p-2 bg-muted/30 rounded text-xs">
                              <span className="font-medium font-mono text-left shrink-0">{key}:</span>
                              <span className="text-muted-foreground break-words text-right">
                                {Array.isArray(value) ? value.join(", ") : String(value)}
                              </span>
                            </div>
                          )
                        })}
                      </div>
                    </ScrollArea>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          )}

          {/* Add Tag Button - Now only requires concept */}
          <Card className="border-0 shadow-sm bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20">
            <CardContent className="p-4">
              <Button
                className="w-full h-12 text-base font-medium bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                disabled={!selectedBlockId || !selectedConcept}
                onClick={handleAddTag}
                size="lg"
              >
                <Plus className="mr-2 h-5 w-5" />
                Add ESRS Tag
              </Button>
              {!selectedConcept && (
                <p className="text-xs text-muted-foreground text-center mt-2">
                  Select a concept to add a tag
                </p>
              )}
              {selectedConcept && !selectedContextId && (
                <p className="text-xs text-blue-600 dark:text-blue-400 text-center mt-2">
                  Ready to tag without context
                </p>
              )}
              {selectedConcept && selectedContextId && (
                <p className="text-xs text-green-600 dark:text-green-400 text-center mt-2">
                  Ready to tag with selected context
                </p>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  )
}

// Export both named and default exports for flexibility
export { TaggingPanel };
export default TaggingPanel;