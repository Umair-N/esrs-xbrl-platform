"use client"
import type { ReportDocument } from "@/types/report"
import { Button } from "@/components/ui/button"
import { Trash2, Eye, ExternalLink, CheckCircle } from "lucide-react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
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

  // Get all tagged blocks
  const taggedBlocks = report.blocks.filter((block) => block.tags.length > 0)
  const router = useRouter()

  const handleDeleteTag = async (blockId: string, tagId: string) => {
    console.log("Delete tag called:", { blockId, tagId })
    console.log("onReportChange available:", !!onReportChange)

    if (!onReportChange) {
      console.error("onReportChange prop is missing!")
      toast.error("Cannot delete tag", {
        description: "Missing update handler",
      })
      return
    }

    // Add to deleting set for visual feedback
    setDeletingTags((prev) => new Set(prev).add(tagId))

    try {
      // Find the tag being deleted for the toast message
      const block = report.blocks.find((b) => b.id === blockId)
      const tag = block?.tags.find((t) => t.id === tagId)

      console.log("Block found:", !!block)
      console.log("Tag found:", !!tag)
      console.log("Current tags count:", block?.tags.length)

      if (!block || !tag) {
        console.error("Block or tag not found!")
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

      console.log("Updated report created, calling onReportChange...")
      console.log("New tags count for block:", updatedReport.blocks.find((b) => b.id === blockId)?.tags.length)

      // Call the update function
      onReportChange(updatedReport)

      // Show success toast with custom styling
      toast.success("Tag deleted successfully", {
        description: tag.concept.label ? `Removed "${tag.concept.label}" tag` : "Tag has been removed",
        icon: <CheckCircle className="h-4 w-4" />,
        duration: 3000,
      })
    } catch (error) {
      console.error("Error deleting tag:", error)
      toast.error("Failed to delete tag", {
        description: "An unexpected error occurred",
      })
    } finally {
      // Remove from deleting set
      setDeletingTags((prev) => {
        const newSet = new Set(prev)
        newSet.delete(tagId)
        return newSet
      })
    }
  }

  const handleViewInTaxonomy = (tag: any) => {
    // Show loading toast
    toast.loading("Opening taxonomy...", {
      duration: 1000,
    })

    // Navigate to taxonomy page with concept data
    const queryParams = new URLSearchParams({
      conceptId: tag.concept.id,
      conceptLabel: tag.concept.label || "",
      conceptType: tag.concept.type || "",
      periodType: tag.concept.periodType || "",
    })
    router.push(`/taxonomy?${queryParams.toString()}`)
  }

  if (taggedBlocks.length === 0) {
    return (
      <div className="text-center py-8 animate-in fade-in-0 duration-500">
        <div className="mx-auto w-16 h-16 bg-muted rounded-full flex items-center justify-center mb-4">
          <Eye className="h-8 w-8 text-muted-foreground" />
        </div>
        <p className="text-sm text-muted-foreground">
          No tagged facts yet. Select a block of text and add tags using the tagging panel.
        </p>
      </div>
    )
  }

  return (
    <ScrollArea className="h-[300px]">
      <Accordion type="multiple" className="space-y-4">
        {taggedBlocks.map((block, index) => (
          <AccordionItem
            key={block.id}
            value={block.id}
            className="border rounded-md overflow-hidden hover:shadow-md transition-all duration-200 animate-in fade-in-0 duration-500"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <AccordionTrigger className="px-4 py-2 hover:bg-muted/50 transition-colors duration-200 group">
              <div className="flex items-center gap-2 text-left">
                <Badge
                  variant="outline"
                  className="bg-primary/10 group-hover:bg-primary/20 transition-colors duration-200"
                >
                  {block.tags.length}
                </Badge>
                <span className="font-medium group-hover:text-primary transition-colors duration-200">
                  {block.content.length > 50 ? `${block.content.substring(0, 50)}...` : block.content}
                </span>
              </div>
            </AccordionTrigger>
            <AccordionContent className="px-4 pb-3">
              <div className="space-y-3">
                <div
                  className="p-3 border rounded-md bg-muted/50 text-sm cursor-pointer hover:bg-muted hover:shadow-sm transition-all duration-200 group"
                  onClick={() => onBlockSelect(block.id)}
                >
                  <div className="group-hover:text-foreground transition-colors duration-200">{block.content}</div>
                  <div className="flex justify-end mt-2">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={(e) => {
                        e.stopPropagation()
                        onBlockSelect(block.id)
                      }}
                      className="hover:bg-primary hover:text-primary-foreground transition-all duration-200"
                    >
                      <Eye className="h-3 w-3 mr-1" /> View in Editor
                    </Button>
                  </div>
                </div>
                <div className="space-y-3">
                  {block.tags.map((tag, tagIndex) => {
                    const isDeleting = deletingTags.has(tag.id)
                    return (
                      <div
                        key={tag.id}
                        className={`border rounded-md p-3 transition-all duration-300 hover:shadow-sm hover:border-primary/30 animate-in fade-in-0 duration-300 ${
                          isDeleting ? "opacity-50 scale-95" : "hover:scale-[1.02]"
                        }`}
                        style={{ animationDelay: `${tagIndex * 50}ms` }}
                      >
                        <div className="flex items-center justify-between">
                          <div className="font-medium break-words flex-1 mr-2 hover:text-primary transition-colors duration-200">
                            {tag.concept.label}
                          </div>
                          <Button
                            size="icon"
                            variant="ghost"
                            className={`h-7 w-7 flex-shrink-0 hover:bg-destructive hover:text-destructive-foreground transition-all duration-200 ${
                              isDeleting ? "animate-pulse" : "hover:scale-110"
                            }`}
                            onClick={(e) => {
                              e.preventDefault()
                              e.stopPropagation()
                              console.log("Delete button clicked for tag:", tag.id, "in block:", block.id)
                              handleDeleteTag(block.id, tag.id)
                            }}
                            title="Delete tag"
                            disabled={isDeleting}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                        <div className="text-xs text-muted-foreground mt-1 break-all font-mono">{tag.concept.id}</div>
                        {tag.startIndex !== undefined && tag.endIndex !== undefined && (
                          <div className="mt-2 p-2 bg-primary/10 rounded text-sm break-words border-l-2 border-primary/30 hover:bg-primary/15 transition-colors duration-200">
                            {block.content.substring(tag.startIndex, tag.endIndex)}
                          </div>
                        )}
                        <Separator className="my-2" />
                        <div className="flex justify-between items-center">
                          <div className="text-xs">
                            <span className="text-muted-foreground">Context: </span>
                            <span className="font-medium">{tag.context.label}</span>
                          </div>
                          <Button
                            size="sm"
                            variant="ghost"
                            className="h-6 px-2 hover:bg-primary hover:text-primary-foreground transition-all duration-200 hover:scale-105"
                            onClick={() => handleViewInTaxonomy(tag)}
                          >
                            <ExternalLink className="h-3 w-3 mr-1" /> View in Taxonomy
                          </Button>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </ScrollArea>
  )
}
