"use client"

import type { ReportDocument, ReportBlock } from "@/types/report"
import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { Textarea } from "@/components/ui/textarea"
import { Edit2, Check, X } from "lucide-react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Separator } from "@/components/ui/separator"
import type { JSX } from "react/jsx-runtime"

interface TextEditorProps {
  report: ReportDocument
  selectedBlockId: string | null
  onBlockSelect: (blockId: string) => void
  onReportChange: (report: ReportDocument) => void
  onTextHighlight: (
    blockId: string,
    selectedText: string,
    startIndex: number,
    endIndex: number
  ) => void
}

export function TextEditor({
  report,
  selectedBlockId,
  onBlockSelect,
  onReportChange,
  onTextHighlight,
}: TextEditorProps) {
  const [editingBlockId, setEditingBlockId] = useState<string | null>(null)
  const [editedContent, setEditedContent] = useState("")
  const textAreaRef = useRef<HTMLTextAreaElement>(null)

  const handleBlockClick = (blockId: string) => {
    if (editingBlockId !== blockId) onBlockSelect(blockId)
  }

  const startEditing = (block: ReportBlock) => {
    setEditingBlockId(block.id)
    setEditedContent(block.content)
  }

  const saveEditing = () => {
    if (!editingBlockId) return
    const updatedReport = {
      ...report,
      blocks: report.blocks.map((block) =>
        block.id === editingBlockId ? { ...block, content: editedContent } : block
      ),
      updatedAt: new Date().toISOString(),
    }
    onReportChange(updatedReport)
    setEditingBlockId(null)
  }

  const cancelEditing = () => setEditingBlockId(null)

  const handleTextSelection = (blockId: string) => {
    if (window.getSelection) {
      const selection = window.getSelection()
      if (selection && selection.toString().length > 0) {
        const range = selection.getRangeAt(0)
        const selectedText = selection.toString()
        const parentElement = range.commonAncestorContainer.parentElement

        if (parentElement && parentElement.closest(`[data-block-id="${blockId}"]`)) {
          const blockContent = report.blocks.find((b) => b.id === blockId)?.content || ""
          const startIndex = blockContent.indexOf(selectedText)
          const endIndex = startIndex + selectedText.length

          if (startIndex >= 0) {
            onTextHighlight(blockId, selectedText, startIndex, endIndex)
          }
        }
      }
    }
  }

  const renderTaggedContent = (block: ReportBlock) => {
    if (block.tags.length === 0) {
      return <p className="whitespace-pre-wrap">{block.content}</p>
    }

    const sortedTags = [...block.tags].sort((a, b) => (a.startIndex || 0) - (b.startIndex || 0))
    const segments: JSX.Element[] = []
    let lastIndex = 0

    sortedTags.forEach((tag, index) => {
      const startIndex = tag.startIndex || 0
      const endIndex = tag.endIndex || block.content.length

      if (startIndex > lastIndex) {
        segments.push(<span key={`text-${index}`}>{block.content.substring(lastIndex, startIndex)}</span>)
      }

      segments.push(
        <HoverCard key={`tag-${tag.id}`}>
          <HoverCardTrigger asChild>
            <span className="bg-primary/20 px-0.5 rounded cursor-help border-b border-dashed border-primary">
              {block.content.substring(startIndex, endIndex)}
            </span>
          </HoverCardTrigger>
          <HoverCardContent className="w-80">
            <div className="space-y-2">
              <h4 className="font-medium">{tag.concept.label}</h4>
              <p className="text-sm text-muted-foreground">{tag.concept.definition}</p>
              <div className="flex flex-wrap gap-2 pt-1">
                <Badge variant="outline">{tag.concept.type}</Badge>
                <Badge variant="outline">{tag.concept.periodType}</Badge>
              </div>
              <Separator />
              <div className="text-xs">
                <p className="font-medium">Context: {tag?.context?.label}</p>
                <p className="text-muted-foreground mt-1">
                  Entity: {tag?.context?.entityName} ({tag?.context?.entityIdentifier})
                </p>
                <p className="text-muted-foreground">
                  Period:{" "}
                  {tag?.context?.periodType === "instant"
                    ? `As of ${new Date(tag.context.instantDate || "").toLocaleDateString()}`
                    : `${new Date(tag?.context?.startDate || "").toLocaleDateString()} to ${new Date(
                        tag?.context?.endDate || ""
                      ).toLocaleDateString()}`}
                </p>
              </div>
            </div>
          </HoverCardContent>
        </HoverCard>
      )

      lastIndex = endIndex
    })

    if (lastIndex < block.content.length) {
      segments.push(<span key="text-last">{block.content.substring(lastIndex)}</span>)
    }

    return <div className="whitespace-pre-wrap">{segments}</div>
  }

  return (
    <div className="flex flex-col h-full">
      <style
        dangerouslySetInnerHTML={{
          __html: `
          .custom-scrollbar {
            scrollbar-width: thin;
            scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
          }
          .custom-scrollbar::-webkit-scrollbar {
            width: 8px;
          }
          .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent;
          }
          .custom-scrollbar::-webkit-scrollbar-thumb {
            background-color: rgba(156, 163, 175, 0.5);
            border-radius: 4px;
            border: 2px solid transparent;
            background-clip: content-box;
          }
          .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background-color: rgba(156, 163, 175, 0.7);
          }
        `,
        }}
      />
      {/* Scrollable blocks */}
      <div className="flex-1 overflow-y-auto space-y-4 custom-scrollbar p-1">
        {report.blocks.map((block) => (
          <div
            key={block.id}
            data-block-id={block.id}
            className={cn(
              "p-3 rounded-md border transition-colors",
              selectedBlockId === block.id && !editingBlockId
                ? "border-primary bg-primary/5"
                : "border-border hover:border-primary/50",
              editingBlockId === block.id ? "border-primary h-full" : "min-h-fit"
            )}
            onClick={() => handleBlockClick(block.id)}
            onMouseUp={() => selectedBlockId === block.id && handleTextSelection(block.id)}
          >
            {editingBlockId === block.id ? (
              <div className="flex flex-col space-y-2 h-full w-full">
                <Textarea
                  ref={textAreaRef}
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                  className="w-full resize-none h-full pr-0 text"
                  autoFocus
                />
                <div className="flex justify-end space-x-2">
                  <Button size="sm" variant="outline" onClick={cancelEditing}>
                    <X className="h-4 w-4 mr-1" /> Cancel
                  </Button>
                  <Button size="sm" onClick={saveEditing}>
                    <Check className="h-4 w-4 mr-1" /> Save
                  </Button>
                </div>
              </div>
            ) : (
              <div className="relative group">
                <div className="sticky top-0 right-0 float-right opacity-0 group-hover:opacity-100 transition-opacity z-10 ml-2 mb-2">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={(e) => {
                      e.stopPropagation()
                      startEditing(block)
                    }}
                  >
                    <Edit2 className="h-4 w-4" />
                  </Button>
                </div>
                <div className="prose dark:prose-invert max-w-none leading-relaxed">
                  {renderTaggedContent(block)}
                </div>
                {block.tags.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-2 clear-both">
                    {block.tags.map((tag) => (
                      <Badge
                        key={tag.id}
                        variant="outline"
                        className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary"
                      >
                        {tag.concept.label}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}