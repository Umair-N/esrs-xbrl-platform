"use client"

import { useState, useEffect } from "react"
import { Search, Tag, Plus, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import type { ReportDocument, XbrlTag } from "@/types/report"
import { sampleTaxonomyConcepts, sampleContexts } from "@/lib/sample-data"
import { generateUniqueId } from "@/lib/utils"

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

export function TaggingPanel({ report, selectedBlockId, highlightedText, onReportChange }: TaggingPanelProps) {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedConceptId, setSelectedConceptId] = useState<string | null>(null)
  const [selectedContextId, setSelectedContextId] = useState<string | null>(null)

  const selectedBlock = selectedBlockId ? report.blocks.find((block) => block.id === selectedBlockId) : null

  const filteredConcepts = sampleTaxonomyConcepts.filter(
    (concept) =>
      concept.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
      concept.id.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  // Reset selections when block changes
  useEffect(() => {
    setSelectedConceptId(null)
    setSelectedContextId(null)
  }, [selectedBlockId])

  const handleAddTag = () => {
    if (!selectedBlockId || !selectedConceptId || !selectedContextId) return

    const selectedConcept = sampleTaxonomyConcepts.find((c) => c.id === selectedConceptId)
    const selectedContext = sampleContexts.find((c) => c.id === selectedContextId)

    if (!selectedConcept || !selectedContext) return

    const newTag: XbrlTag = {
      id: generateUniqueId(),
      concept: selectedConcept,
      context: selectedContext,
      createdAt: new Date().toISOString(),
      // Add start and end indices for the highlighted text
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

    // Reset selections
    setSelectedConceptId(null)
    setSelectedContextId(null)
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle>Tag Selection</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {!selectedBlock ? (
            <div className="text-center py-6">
              <Tag className="h-10 w-10 text-muted-foreground mx-auto mb-2" />
              <p className="text-sm text-muted-foreground">Select a block of text to tag</p>
            </div>
          ) : (
            <>
              <div className="space-y-2">
                <label className="text-sm font-medium">Selected Text:</label>
                <div className="p-2 border rounded-md bg-muted/50 text-sm">
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
                  <Alert variant="default" className="bg-muted/50 border-primary/30">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Highlight text to tag</AlertTitle>
                    <AlertDescription>
                      Select specific text within this block to create a more precise tag.
                    </AlertDescription>
                  </Alert>
                )}
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">XBRL Concept:</label>
                <div className="flex space-x-2">
                  <div className="relative flex-1">
                    <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search concepts..."
                      className="pl-8"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                  </div>
                </div>

                <div className="max-h-[200px] overflow-y-auto border rounded-md">
                  {filteredConcepts.length === 0 ? (
                    <div className="p-4 text-center text-sm text-muted-foreground">No concepts found</div>
                  ) : (
                    <div className="divide-y">
                      {filteredConcepts.map((concept) => (
                        <div
                          key={concept.id}
                          className={`p-2 cursor-pointer hover:bg-accent ${
                            selectedConceptId === concept.id ? "bg-primary/10" : ""
                          }`}
                          onClick={() => setSelectedConceptId(concept.id)}
                        >
                          <div className="font-medium text-sm">{concept.label}</div>
                          <div className="text-xs text-muted-foreground">{concept.id}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              <div className="space-y-2">
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
            </>
          )}
        </CardContent>
        <CardFooter>
          <Button
            className="w-full"
            disabled={!selectedBlockId || !selectedConceptId || !selectedContextId}
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
