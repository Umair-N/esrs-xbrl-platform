"use client"

import type { ReportDocument } from "@/types/report"
import { Button } from "@/components/ui/button"
import { Trash2, Eye, ExternalLink, CheckCircle, Tag, Hash, FileText } from 'lucide-react'
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { toast } from "sonner"
import { useRouter } from "next/navigation"
import { useState } from "react"

interface TaggedFactsListProps {
  report: ReportDocument
  onBlockSelect: (blockId: string) => void
  onReportChange?: (report: ReportDocument) => void
}

export function TaggedFactsList({ report, onBlockSelect, onReportChange }: TaggedFactsListProps) {
  const [deletingTags, setDeletingTags] = useState<Set<string>>(new Set())
  const router = useRouter()

  // Get all tags from all blocks
  const allTags = report.blocks.flatMap(block => 
    block.tags.map(tag => ({
      ...tag,
      blockId: block.id,
      blockContent: block.content,
      taggedText: tag.startIndex !== undefined && tag.endIndex !== undefined 
        ? block.content.substring(tag.startIndex, tag.endIndex)
        : block.content
    }))
  )

  const handleDeleteTag = async (blockId: string, tagId: string) => {
    if (!onReportChange) {
      toast.error("Cannot delete tag", {
        description: "Missing update handler",
      })
      return
    }

    setDeletingTags((prev) => new Set(prev).add(tagId))

    try {
      const block = report.blocks.find((b) => b.id === blockId)
      const tag = block?.tags.find((t) => t.id === tagId)

      if (!block || !tag) {
        toast.error("Cannot delete tag", {
          description: "Tag not found",
        })
        return
      }

      const updatedReport = {
        ...report,
        blocks: report.blocks.map((currentBlock) =>
          currentBlock.id === blockId
            ? {
                ...currentBlock,
                tags: currentBlock.tags.filter((currentTag) => currentTag.id !== tagId),
              }
            : currentBlock,
        ),
        updatedAt: new Date().toISOString(),
      }

      onReportChange(updatedReport)

      toast.success("Tag deleted", {
        description: `Removed "${tag.concept.label}"`,
        icon: <CheckCircle className="h-4 w-4" />,
        duration: 2000,
      })
    } catch (error) {
      console.error("Error deleting tag:", error)
      toast.error("Failed to delete tag")
    } finally {
      setDeletingTags((prev) => {
        const newSet = new Set(prev)
        newSet.delete(tagId)
        return newSet
      })
    }
  }

  const handleViewInTaxonomy = (tag: any) => {
    const queryParams = new URLSearchParams({
      conceptId: tag.concept.id,
      conceptLabel: tag.concept.label || "",
      conceptType: tag.concept.type || "",
      periodType: tag.concept.periodType || "",
    })
    router.push(`/taxonomy?${queryParams.toString()}`)
  }

  const handleViewInDocument = (blockId: string) => {
    onBlockSelect(blockId)
    toast.success("Navigated to document", {
      duration: 1500,
    })
  }

  console.log("TaggedFactsList rendering with", allTags.length, "tags")

  if (allTags.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-8">
        <div className="w-12 h-12 bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900/20 dark:to-pink-900/20 rounded-full flex items-center justify-center mb-4">
          <Tag className="h-6 w-6 text-purple-600" />
        </div>
        <h3 className="text-base font-semibold mb-2">No Tagged Facts Yet</h3>
        <p className="text-sm text-muted-foreground max-w-sm leading-relaxed">
          Start by selecting text in the document and adding ESRS tags.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <div className="text-sm text-muted-foreground mb-3">
        {allTags.length} tagged fact{allTags.length !== 1 ? 's' : ''}
      </div>
      
      {allTags.map((tag, index) => {
        const isDeleting = deletingTags.has(tag.id)
        const isESRS = tag.concept.id.toLowerCase().includes("esrs")
        
        return (
          <Card
            key={tag.id}
            className={`transition-all duration-200 border-l-4 ${
              isESRS 
                ? "border-l-emerald-500 bg-emerald-50/50 dark:bg-emerald-950/10" 
                : "border-l-blue-500 bg-blue-50/50 dark:bg-blue-950/10"
            } ${
              isDeleting ? "opacity-50 scale-95" : "hover:shadow-md"
            }`}
          >
            <CardHeader className="pb-2">
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <CardTitle className="text-sm font-semibold break-words leading-tight">
                    {tag.concept.label}
                  </CardTitle>
                  <div className="flex items-center gap-1 mt-1">
                    <Badge 
                      variant="outline" 
                      className={`text-xs ${
                        isESRS 
                          ? "bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-900/20 dark:text-emerald-300" 
                          : "bg-blue-100 text-blue-800 border-blue-300 dark:bg-blue-900/20 dark:text-blue-300"
                      }`}
                    >
                      {isESRS ? "ESRS" : "XBRL"}
                    </Badge>
                  </div>
                </div>
                <Button
                  size="icon"
                  variant="ghost"
                  className="h-6 w-6 flex-shrink-0 hover:bg-destructive hover:text-destructive-foreground"
                  onClick={() => handleDeleteTag(tag.blockId, tag.id)}
                  disabled={isDeleting}
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
            </CardHeader>

            <CardContent className="space-y-3 pt-0 pb-3">
              {/* Tagged Text - Compact */}
              <div className={`p-2 rounded border text-xs break-words leading-relaxed ${
                isESRS 
                  ? "bg-emerald-50 border-emerald-200 dark:bg-emerald-950/20 dark:border-emerald-800" 
                  : "bg-blue-50 border-blue-200 dark:bg-blue-950/20 dark:border-blue-800"
              }`}>
                {tag.taggedText.length > 100 ? `${tag.taggedText.substring(0, 100)}...` : tag.taggedText}
              </div>

              {/* Action Buttons - Compact */}
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1 text-xs h-7 hover:bg-primary hover:text-primary-foreground"
                  onClick={() => handleViewInDocument(tag.blockId)}
                >
                  <Eye className="h-3 w-3 mr-1" />
                  View
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1 text-xs h-7 hover:bg-secondary hover:text-secondary-foreground"
                  onClick={() => handleViewInTaxonomy(tag)}
                >
                  <ExternalLink className="h-3 w-3 mr-1" />
                  Taxonomy
                </Button>
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
