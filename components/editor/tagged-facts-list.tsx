"use client"

import type { ReportDocument } from "@/types/report"
import { Button } from "@/components/ui/button"
import { Trash2, Eye, ExternalLink } from "lucide-react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

interface TaggedFactsListProps {
  report: ReportDocument
  onBlockSelect: (blockId: string) => void
}

export function TaggedFactsList({ report, onBlockSelect }: TaggedFactsListProps) {
  // Get all tagged blocks
  const taggedBlocks = report.blocks.filter((block) => block.tags.length > 0)

  if (taggedBlocks.length === 0) {
    return (
      <div className="text-center py-6">
        <p className="text-sm text-muted-foreground">
          No tagged facts yet. Select a block of text and add tags using the tagging panel.
        </p>
      </div>
    )
  }

  return (
    <ScrollArea className="h-[300px]">
      <Accordion type="multiple" className="space-y-4">
        {taggedBlocks.map((block) => (
          <AccordionItem key={block.id} value={block.id} className="border rounded-md overflow-hidden">
            <AccordionTrigger className="px-4 py-2 hover:bg-muted/50">
              <div className="flex items-center gap-2 text-left">
                <Badge variant="outline" className="bg-primary/10">
                  {block.tags.length}
                </Badge>
                <span className="font-medium">
                  {block.content.length > 50 ? `${block.content.substring(0, 50)}...` : block.content}
                </span>
              </div>
            </AccordionTrigger>
            <AccordionContent className="px-4 pb-3">
              <div className="space-y-3">
                <div
                  className="p-2 border rounded-md bg-muted/50 text-sm cursor-pointer hover:bg-muted"
                  onClick={() => onBlockSelect(block.id)}
                >
                  {block.content}
                  <div className="flex justify-end mt-2">
                    <Button size="sm" variant="ghost" onClick={() => onBlockSelect(block.id)}>
                      <Eye className="h-3 w-3 mr-1" /> View in Editor
                    </Button>
                  </div>
                </div>

                <div className="space-y-3">
                  {block.tags.map((tag) => (
                    <div key={tag.id} className="border rounded-md p-3">
                      <div className="flex items-center justify-between">
                        <div className="font-medium">{tag.concept.label}</div>
                        <Button size="icon" variant="ghost" className="h-7 w-7">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>

                      <div className="text-xs text-muted-foreground mt-1">{tag.concept.id}</div>

                      {tag.startIndex !== undefined && tag.endIndex !== undefined && (
                        <div className="mt-2 p-1 bg-primary/10 rounded text-sm">
                          {block.content.substring(tag.startIndex, tag.endIndex)}
                        </div>
                      )}

                      <Separator className="my-2" />

                      <div className="flex justify-between items-center">
                        <div className="text-xs">
                          <span className="text-muted-foreground">Context: </span>
                          {tag.context.label}
                        </div>
                        <Button size="sm" variant="ghost" className="h-6 px-2">
                          <ExternalLink className="h-3 w-3 mr-1" /> View in Taxonomy
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </ScrollArea>
  )
}
