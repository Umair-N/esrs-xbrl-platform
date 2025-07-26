"use client"

import { useState, useEffect, useMemo } from "react"
import {
  Search,
  Tag,
  Plus,
  AlertCircle,
  ChevronRight,
  ChevronDown,
  Folder,
  FolderOpen,
  FileText,
  Calculator,
} from "lucide-react"
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
  // Keep all nodes initially collapsed
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

export function TaggingPanel({ report, selectedBlockId, highlightedText, onReportChange }: TaggingPanelProps) {
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
    if (!selectedBlockId || !selectedConcept || !selectedContextId) return

    const selectedContext = sampleContexts.find((c) => c.id === selectedContextId)
    if (!selectedContext) return

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
      context: selectedContext,
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
    setSelectedContextId(null)
    setSearchQuery("")
  }

  if (!taxonomyData) {
    return (
      <div className="space-y-4">
        <Card>
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
    <div className="space-y-4 w-full">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2">
            <Tag className="h-4 w-4 flex-shrink-0" />
            Taxonomy
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 w-full">
          {!selectedBlock ? (
            <div className="text-center py-6">
              <Tag className="h-10 w-10 text-muted-foreground mx-auto mb-2" />
              <p className="text-sm text-muted-foreground">Select a block of text to tag</p>
            </div>
          ) : (
            <>
              {/* Selected Text Display */}
              <div className="space-y-2 w-full">
                <label className="text-sm font-medium">Selected Text:</label>
                <div className="p-2 border rounded-md bg-muted/50 text-sm break-words w-full">
                  {highlightedText && highlightedText.text ? (
                    <span className="bg-primary/20 px-1 rounded">{highlightedText.text}</span>
                  ) : (
                    <span>
                      {selectedBlock.content.length > 100
                        ? `${selectedBlock.content.substring(0, 100)}...`
                        : selectedBlock.content}
                    </span>
                  )}
                </div>
                {!highlightedText?.text && (
                  <Alert variant="default" className="bg-muted/50 border-primary/30 flex items-center gap-2">
                    <AlertCircle className="h-4 w-4 shrink-0" />
                    <div>
                      <AlertTitle>Highlight text to tag</AlertTitle>
                      <AlertDescription>
                        Select specific text within this block to create a more precise tag.
                      </AlertDescription>
                    </div>
                  </Alert>
                )}
              </div>

              <Separator />

              {/* ESRS Taxonomy Concept Section */}
              <div className="space-y-2 w-full">
                <label className="text-sm font-medium">ESRS Taxonomy Concept:</label>

                {/* Search Input */}
                <div className="relative w-full">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <Input
                    placeholder="Search ESRS concepts..."
                    className="pl-8 w-full"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>

                {/* Selected Concept Display */}
                {selectedConcept && (
                  <div className="p-2 bg-primary/10 rounded-md border border-primary/30 w-full">
                    <div className="font-medium text-sm break-words w-full" title={selectedConcept.label ?? ""}>
                      {selectedConcept.label}
                    </div>
                    <div
                      className="text-xs text-muted-foreground font-mono break-all w-full mt-1"
                      title={selectedConcept.id ?? ""}
                    >
                      {selectedConcept.id}
                    </div>
                    {selectedConcept.labelType && (
                      <Badge variant="outline" className="text-xs mt-1 flex-shrink-0">
                        {selectedConcept.labelType}
                      </Badge>
                    )}
                  </div>
                )}

                {/* Taxonomy Browser & Search Results Container */}
                <div className="border rounded-md w-full">
                  <div className="p-2 bg-muted/50 border-b">
                    <div
                      className="text-xs font-medium break-words w-full"
                      title={
                        viewMode === "search"
                          ? `${filteredConcepts.length} search results`
                          : `${taxonomyData.label || "ESRS Taxonomy"} - ${allNodes.length} concepts`
                      }
                    >
                      {viewMode === "search"
                        ? `${filteredConcepts.length} search results`
                        : `${taxonomyData.label || "ESRS Taxonomy"} - ${allNodes.length} concepts`}
                    </div>
                  </div>
                  <ScrollArea className="h-[300px] w-full">
                    <div className="p-2 w-full">
                      {viewMode === "search" ? (
                        filteredConcepts.length === 0 ? (
                          <div className="text-center py-4 text-muted-foreground text-sm">
                            <Search className="h-6 w-6 mx-auto mb-2" />
                            <p>No results found for "{searchQuery}"</p>
                          </div>
                        ) : (
                          filteredConcepts.map((concept, index) => (
                            <div
                              key={`${concept.id}-${index}`}
                              className={`p-2 cursor-pointer hover:bg-muted rounded-sm transition-colors ${
                                selectedConcept?.id === concept.id ? "bg-primary/10 border-l-2 border-primary" : ""
                              }`}
                              onClick={() => setSelectedConcept(concept)}
                            >
                              <div className="font-medium text-sm flex items-start gap-1 min-w-0">
                                <span className="break-words leading-tight" title={concept.label ?? ""}>
                                  {concept.label}
                                </span>
                                {concept.calculations && concept.calculations.length > 0 && (
                                  <Calculator className="h-3 w-3 text-blue-500 flex-shrink-0 mt-0.5" />
                                )}
                              </div>
                              <div className="text-xs text-muted-foreground mt-1 flex items-start gap-2 min-w-0 flex-wrap">
                                <span className="font-mono break-all leading-tight" title={concept.id ?? ""}>
                                  {concept.id}
                                </span>
                                {concept.labelType && (
                                  <Badge variant="outline" className="text-xs h-4 px-1 flex-shrink-0">
                                    {concept.labelType}
                                  </Badge>
                                )}
                              </div>
                            </div>
                          ))
                        )
                      ) : (
                        <div className="w-full">
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
                </div>
              </div>

              <Separator />

              {/* Context Selection */}
              <div className="space-y-2 w-full">
                <label className="text-sm font-medium">Context:</label>
                <Select value={selectedContextId || ""} onValueChange={setSelectedContextId}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a context" />
                  </SelectTrigger>
                  <SelectContent>
                    {sampleContexts.map((context) => (
                      <SelectItem key={context.id} value={context.id}>
                        {context.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Selected Concept Details */}
              {selectedConcept && (
                <div className="space-y-2 w-full">
                  <label className="text-sm font-medium">Concept Details:</label>
                  <Tabs defaultValue="basic" className="w-full">
                    <TabsList className="grid w-full grid-cols-2">
                      <TabsTrigger value="basic">Basic Info</TabsTrigger>
                      <TabsTrigger value="properties">Properties</TabsTrigger>
                    </TabsList>
                    <TabsContent value="basic" className="space-y-2 mt-3">
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="font-medium">Type:</span>
                          <div
                            className="text-muted-foreground break-words w-full"
                            title={selectedConcept.type || "N/A"}
                          >
                            {selectedConcept.type || "N/A"}
                          </div>
                        </div>
                        <div>
                          <span className="font-medium">Period:</span>
                          <div
                            className="text-muted-foreground break-words w-full"
                            title={selectedConcept.periodType || "N/A"}
                          >
                            {selectedConcept.periodType || "N/A"}
                          </div>
                        </div>
                        <div>
                          <span className="font-medium">Abstract:</span>
                          <div className="text-muted-foreground">
                            {selectedConcept.abstract === "true" ? "Yes" : "No"}
                          </div>
                        </div>
                        <div>
                          <span className="font-medium">Order:</span>
                          <div
                            className="text-muted-foreground break-words w-full"
                            title={selectedConcept.order || "N/A"}
                          >
                            {selectedConcept.order || "N/A"}
                          </div>
                        </div>
                      </div>
                      {selectedConcept.originalLabel && (
                        <div className="mt-2 w-full">
                          <span className="font-medium text-xs">Original Label:</span>
                          <div
                            className="text-xs text-muted-foreground bg-muted p-2 rounded mt-1 break-words w-full"
                            title={selectedConcept.originalLabel}
                          >
                            {selectedConcept.originalLabel}
                          </div>
                        </div>
                      )}
                    </TabsContent>
                    <TabsContent value="properties" className="mt-3">
                      <ScrollArea className="h-32 w-full">
                        <div className="space-y-1 text-xs w-full">
                          {Object.entries(selectedConcept).map(([key, value]) => {
                            if (key === "children" || !value) return null
                            return (
                              <div
                                key={key}
                                className="flex flex-col sm:flex-row sm:justify-between p-1 bg-muted rounded w-full gap-1"
                              >
                                <span className="font-medium font-mono break-words" title={key}>
                                  {key}:
                                </span>
                                <span
                                  className="text-muted-foreground break-words"
                                  title={Array.isArray(value) ? value.join(", ") : String(value)}
                                >
                                  {Array.isArray(value) ? value.join(", ") : String(value)}
                                </span>
                              </div>
                            )
                          })}
                        </div>
                      </ScrollArea>
                    </TabsContent>
                  </Tabs>
                </div>
              )}
            </>
          )}
        </CardContent>
        <CardFooter>
          <Button
            className="w-full"
            disabled={!selectedBlockId || !selectedConcept || !selectedContextId}
            onClick={handleAddTag}
          >
            <Plus className="mr-2 h-4 w-4" />
            Add Tag 
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
