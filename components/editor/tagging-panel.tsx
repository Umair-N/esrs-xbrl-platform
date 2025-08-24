"use client"

import React from "react"

import type { ReactNode } from "react"
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
  Target,
  Info,
  Presentation,
  Layers,
  FormInput as Formula,
  BarChart3,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
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
  selectedId?: string | null
  searchQuery: string
}) => {
  const [isExpanded, setIsExpanded] = useState(false)
  const hasChildren = node.children && node.children.length > 0
  const hasCalculations = node.calculations && node.calculations.length > 0
  const isSelected = Boolean(selectedId && node.id) && selectedId === node.id
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
        className={`group relative flex items-start py-1.5 px-2 rounded-lg cursor-pointer transition-all duration-200 border-2 ${
          isSelected
            ? "bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-950/30 dark:to-green-950/30 border-emerald-300 dark:border-emerald-700 shadow-md ring-2 ring-emerald-200 dark:ring-emerald-800"
            : "border-transparent hover:border-muted-foreground/20 hover:bg-muted/50 hover:shadow-sm bg-transparent"
        }`}
        style={{ paddingLeft: `${level * 12 + 8}px` }}
        onClick={() => onSelect(node)}
      >
        {isSelected && (
          <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-emerald-500 to-green-500 rounded-l-lg" />
        )}

        {hasChildren && (
          <Button
            variant="ghost"
            size="sm"
            className={`h-4 w-4 p-0 mr-2 flex-shrink-0 mt-0.5 transition-colors ${
              isSelected ? "hover:bg-emerald-200 dark:hover:bg-emerald-800" : "hover:bg-muted"
            }`}
            onClick={(e) => {
              e.stopPropagation()
              setIsExpanded(!isExpanded)
            }}
            aria-label={isExpanded ? "Collapse node" : "Expand node"}
          >
            {isExpanded ? <ChevronDown className="h-2 w-2" /> : <ChevronRight className="h-2 w-2" />}
          </Button>
        )}

        <div className="flex items-start min-w-0 flex-1 gap-2">
          <div
            className={`p-1 rounded transition-colors ${
              isSelected ? "bg-emerald-100 dark:bg-emerald-900/50" : "bg-muted/50 group-hover:bg-muted"
            }`}
          >
            <span
              className={`transition-colors ${
                isSelected
                  ? "text-emerald-600 dark:text-emerald-400"
                  : "text-muted-foreground group-hover:text-foreground"
              }`}
            >
              {getIcon()}
            </span>
          </div>

          <div className="min-w-0 flex-1">
            <div className="flex items-start justify-between gap-2 mb-1">
              <span
                className={`font-medium text-xs break-words leading-tight transition-colors ${
                  isSelected ? "text-emerald-900 dark:text-emerald-100" : "text-foreground group-hover:text-foreground"
                }`}
                title={node.label ?? ""}
              >
                {node.label}
              </span>

              <div className="flex items-center gap-1 flex-shrink-0">
                {hasCalculations && (
                  <div
                    className={`p-0.5 rounded transition-colors ${
                      isSelected ? "bg-blue-100 dark:bg-blue-900/50" : "bg-blue-50 dark:bg-blue-950/30"
                    }`}
                  >
                    <Calculator className="h-2 w-2 text-blue-500" />
                  </div>
                )}
                {isSelected && <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />}
              </div>
            </div>

            <div className="flex items-start gap-1 mt-1 min-w-0 flex-wrap">
              <code
                className={`text-xs font-mono px-1.5 py-0.5 rounded transition-colors break-all leading-tight ${
                  isSelected
                    ? "bg-emerald-100 dark:bg-emerald-900/50 text-emerald-800 dark:text-emerald-300"
                    : "bg-muted text-muted-foreground group-hover:bg-muted"
                }`}
                title={node.id ?? ""}
              >
                {node.id}
              </code>

              {node.labelType && (
                <Badge
                  variant={isSelected ? "default" : "outline"}
                  className={`text-xs h-4 px-1 flex-shrink-0 transition-all ${
                    isSelected
                      ? "bg-emerald-600 text-white dark:bg-emerald-500"
                      : `${getBadgeColor(node.labelType)} group-hover:border-muted-foreground/30`
                  }`}
                >
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
              selectedId={selectedId ?? null}
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
  const [activeTab, setActiveTab] = useState("presentations")

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
    const contextToUse = selectedContextId ? sampleContexts.find((c) => c.id === selectedContextId) : undefined

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
      ...(contextToUse && { context: contextToUse }),
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
    setSearchQuery("")
  }

  const demoData = {
    dimensions: [
      {
        id: "esrs:EntityDimension",
        label: "Entity Dimension",
        type: "dimension",
        description: "Represents different entities within the reporting scope",
        labelType: "axis",
        periodType: "duration",
        abstract: "false",
      },
    ],
    formulae: [
      {
        id: "esrs:GHGEmissionsFormula",
        label: "GHG Emissions Calculation",
        type: "formula",
        expression: "Scope1 + Scope2 + Scope3",
        description: "Total greenhouse gas emissions calculation",
        labelType: "formula",
        periodType: "duration",
        abstract: "false",
      },
    ],
    calculations: [
      {
        id: "esrs:TotalEnergyConsumption",
        label: "Total Energy Consumption",
        type: "calculation",
        components: ["RenewableEnergy", "NonRenewableEnergy"],
        description: "Sum of all energy consumption sources",
        labelType: "calculation",
        periodType: "duration",
        abstract: "false",
      },
    ],
  }

  const renderTabContent = (tabName: string, icon: ReactNode, demoItems: any[]) => (
    <div className="space-y-3">
      {/* Search Input (disabled in demo tabs) */}
      <div className="relative">
        <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
        <Input placeholder={`Search ${tabName}...`} className="pl-10 h-9 border-2 focus:border-emerald-500" disabled />
      </div>

      {/* Selected Concept Display for this tab */}
      {selectedConcept && activeTab === tabName && (
        <div className="p-3 bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-950/20 dark:to-green-950/20 rounded-lg border-2 border-emerald-200 dark:border-emerald-800">
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

      {/* Demo Content or Empty State */}
      {demoItems.length > 0 ? (
        <Card className="border-2">
          <CardHeader className="py-2 bg-muted/30">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-medium capitalize">
                {tabName} - {demoItems.length} item{demoItems.length !== 1 ? "s" : ""}
              </h4>
              <Badge variant="secondary" className="text-xs">
                Demo
              </Badge>
            </div>
          </CardHeader>
          <ScrollArea className="h-[250px]">
            <div className="p-2">
              <div className="space-y-1">
                {demoItems.map((item, index) => {
                  const isSelected = Boolean(selectedConcept?.id && item.id) && selectedConcept?.id === item.id
                  return (
                    <div
                      key={`${item.id}-${index}`}
                      className={`group relative p-3 cursor-pointer rounded-lg transition-all duration-200 border-2 ${
                        isSelected
                          ? "bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-950/30 dark:to-green-950/30 border-emerald-300 dark:border-emerald-700 shadow-md ring-2 ring-emerald-200 dark:ring-emerald-800"
                          : "border-transparent hover:border-emerald-200 dark:hover:border-emerald-800 hover:bg-emerald-50/50 dark:hover:bg-emerald-950/10 hover:shadow-sm"
                      }`}
                      onClick={() => setSelectedConcept(item as any)}
                    >
                      {isSelected && (
                        <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-emerald-500 to-green-500 rounded-l-lg" />
                      )}
                      <div className="flex items-start gap-2.5">
                        <div
                          className={`p-1.5 rounded-md ${
                            isSelected
                              ? "bg-emerald-100 dark:bg-emerald-900/50"
                              : "bg-muted/50 group-hover:bg-emerald-100/50 dark:group-hover:bg-emerald-900/30"
                          }`}
                        >
                          {React.cloneElement(icon as React.ReactElement<{ className?: string }>, {
                            className: `h-4 w-4 ${
                              isSelected
                                ? "text-emerald-600 dark:text-emerald-400"
                                : "text-muted-foreground group-hover:text-emerald-600 dark:group-hover:text-emerald-400"
                            }`,
                          })}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-2 mb-1">
                            <h4
                              className={`font-semibold text-sm break-words leading-tight ${
                                isSelected
                                  ? "text-emerald-900 dark:text-emerald-100"
                                  : "text-foreground group-hover:text-emerald-800 dark:group-hover:text-emerald-200"
                              }`}
                            >
                              {item.label}
                            </h4>
                            {item.labelType && (
                              <Badge
                                variant={isSelected ? "default" : "outline"}
                                className={`text-xs h-4 px-1 flex-shrink-0 transition-all ${
                                  isSelected
                                    ? "bg-emerald-600 text-white dark:bg-emerald-500"
                                    : "group-hover:border-muted-foreground/30"
                                }`}
                              >
                                {item.labelType}
                              </Badge>
                            )}
                          </div>
                          <code
                            className={`text-xs font-mono px-1.5 py-0.5 rounded transition-colors break-all leading-tight block mb-2 ${
                              isSelected
                                ? "bg-emerald-100 dark:bg-emerald-900/50 text-emerald-800 dark:text-emerald-300"
                                : "bg-muted text-muted-foreground group-hover:bg-muted"
                            }`}
                          >
                            {item.id}
                          </code>
                          {item.description && (
                            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{item.description}</p>
                          )}
                          {item.expression && (
                            <div className="mt-2 p-2 bg-slate-100 dark:bg-slate-800 rounded text-xs font-mono">
                              <span className="text-muted-foreground">Formula: </span>
                              <span className="text-foreground">{item.expression}</span>
                            </div>
                          )}
                          {item.components && (
                            <div className="mt-2">
                              <span className="text-xs text-muted-foreground">Components: </span>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {item.components.map((component: string, idx: number) => (
                                  <Badge key={idx} variant="outline" className="text-xs">
                                    {component}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </ScrollArea>
        </Card>
      ) : (
        <Card className="border-2 border-dashed border-muted">
          <CardContent className="py-8 text-center">
            <div className="mx-auto w-12 h-12 bg-muted/50 rounded-full flex items-center justify-center mb-3">
              {icon}
            </div>
            <h4 className="text-sm font-medium text-muted-foreground mb-1">No {tabName} Available</h4>
            <p className="text-xs text-muted-foreground">
              {tabName.charAt(0).toUpperCase() + tabName.slice(1)} will appear here when available
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )

  if (!taxonomyData) {
    return (
      <div className="space-y-4">
        <Card className="border-0 shadow-sm">
          <CardContent className="p-6">
            <Alert variant="destructive" className="flex items-center gap-2">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <div>
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>Failed to load taxonomy data. Please check your taxonomy file.</AlertDescription>
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
              Choose a block of text from the document to start adding tags
            </p>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Selected Text Display */}
          <Card className="border-0 shadow-sm mt-0">
            <CardHeader className="pb-1 pt-1">
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
                    <p className="text-sm bg-primary/20 px-2 py-1 rounded break-words">{highlightedText.text}</p>
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
            </CardContent>
          </Card>

          {/* Taxonomy Tabs */}
          <Card className="border-0 shadow-sm mt-1 p-0 ">
            <CardHeader className="p-0">
              <CardTitle className="flex items-center gap-2 text-base p-2">
                <Tag className="h-4 w-4 text-emerald-600" />
                Taxonomy
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 p-0">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="presentations" className="flex items-center gap-1">
                    <Presentation className="h-3 w-3" />
                    <span className="hidden sm:inline">Presentations</span>
                    <span className="sm:hidden">Pres</span>
                  </TabsTrigger>
                  <TabsTrigger value="dimensions" className="flex items-center gap-1">
                    <Layers className="h-3 w-3" />
                    <span className="hidden sm:inline">Dimensions</span>
                    <span className="sm:hidden">Dim</span>
                  </TabsTrigger>
                  <TabsTrigger value="formulae" className="flex items-center gap-1">
                    <Formula className="h-3 w-3" />
                    <span className="hidden sm:inline">Formulae</span>
                    <span className="sm:hidden">Form</span>
                  </TabsTrigger>
                  <TabsTrigger value="calculations" className="flex items-center gap-1">
                    <BarChart3 className="h-3 w-3" />
                    <span className="hidden sm:inline">Calculations</span>
                    <span className="sm:hidden">Calc</span>
                  </TabsTrigger>
                </TabsList>

                {/* Presentations Tab */}
                <TabsContent value="presentations" className="space-y-3 mt-1 p-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search Taxonomy"
                      className="pl-10 h-9   outline-none"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                  </div>

                 

                  <Card className="border-2  ">
                    <CardHeader className="py-2 bg-muted/30">
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
                    <CardContent className="px-0">
                      <ScrollArea className="h-[250px]">
                        <div className="p-2">
                          {viewMode === "search" ? (
                            filteredConcepts.length === 0 ? (
                              <div className="text-center py-6 text-muted-foreground">
                                <Search className="h-8 w-8 mx-auto mb-3 opacity-50" />
                                <p className="text-sm">No results found for "{searchQuery}"</p>
                              </div>
                            ) : (
                              <div className="space-y-1 ">
                                {filteredConcepts.map((concept, index) => {
                                  const isSelected =
                                    Boolean(selectedConcept?.id && concept.id) && selectedConcept?.id === concept.id
                                  return (
                                    <div
                                      key={`${concept.id}-${index}`}
                                      className={`group relative p-2.5 cursor-pointer rounded-lg transition-all duration-200 border-2 ${
                                        isSelected
                                          ? "bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-950/30 dark:to-green-950/30 border-emerald-300 dark:border-emerald-700 shadow-md ring-2 ring-emerald-200 dark:ring-emerald-800"
                                          : "border-transparent hover:border-emerald-200 dark:hover:border-emerald-800 hover:bg-emerald-50/50 dark:hover:bg-emerald-950/10 hover:shadow-sm"
                                      }`}
                                      onClick={() => setSelectedConcept(concept)}
                                    >
                                      {isSelected && (
                                        <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-emerald-500 to-green-500 rounded-l-lg" />
                                      )}
                                      <div className="flex items-start gap-2.5">
                                        <div
                                          className={`p-1.5 rounded-md ${
                                            isSelected
                                              ? "bg-emerald-100 dark:bg-emerald-900/50"
                                              : "bg-muted/50 group-hover:bg-emerald-100/50 dark:group-hover:bg-emerald-900/30"
                                          }`}
                                        >
                                          <FileText
                                            className={`h-4 w-4 ${
                                              isSelected
                                                ? "text-emerald-600 dark:text-emerald-400"
                                                : "text-muted-foreground group-hover:text-emerald-600 dark:group-hover:text-emerald-400"
                                            }`}
                                          />
                                        </div>
                                        <div className="flex-1 min-w-0">
                                          <h4
                                            className={`font-semibold text-sm ${
                                              isSelected
                                                ? "text-emerald-900 dark:text-emerald-100"
                                                : "text-foreground group-hover:text-emerald-800 dark:group-hover:text-emerald-200"
                                            }`}
                                          >
                                            {concept.label}
                                          </h4>
                                          <code className="text-xs font-mono px-2 py-1 rounded block mt-1">
                                            {concept.id}
                                          </code>
                                        </div>
                                      </div>
                                    </div>
                                  )
                                })}
                              </div>
                            )
                          ) : (
                            <div className="space-y-1">
                              {taxonomyData.children.map((child, index) => (
                                <TaxonomyTreeNode
                                  key={`${child.id}-${index}`}
                                  node={child}
                                  onSelect={setSelectedConcept}
                                  selectedId={selectedConcept?.id ?? null}
                                  searchQuery=""
                                />
                              ))}
                            </div>
                          )}
                        </div>
                      </ScrollArea>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="dimensions" className="mt-3">
                  {renderTabContent("dimensions", <Layers className="h-4 w-4" />, demoData.dimensions)}
                </TabsContent>
                <TabsContent value="formulae" className="mt-3">
                  {renderTabContent("formulae", <Formula className="h-4 w-4" />, demoData.formulae)}
                </TabsContent>
                <TabsContent value="calculations" className="mt-3">
                  {renderTabContent("calculations", <BarChart3 className="h-4 w-4" />, demoData.calculations)}
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          {/* Context Selection */}
          <Card className="border-t shadow-sm p-0 mt-0">
            <CardHeader className="">
              <CardTitle className="text-base flex items-center gap-2">
                Context Selection{" "}
                <Badge variant="secondary" className="text-xs">
                  Optional
                </Badge>
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

             
            </CardContent>
          </Card>

          {/* Add Tag Button */}
          <Card className="border-0 shadow-sm bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20">
            <CardContent className="p-4">
              <Button
                className="w-full h-12 text-base font-medium bg-gradient-to-r from-blue-600 to-indigo-600"
                disabled={!selectedBlockId || !selectedConcept}
                onClick={handleAddTag}
                size="lg"
              >
                <Plus className="mr-2 h-5 w-5" />
                Add Tag
              </Button>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  )
}

export { TaggingPanel }
export default TaggingPanel
