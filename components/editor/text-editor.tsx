"use client";

import { useState, useRef } from "react";
import type { ReportDocument, ReportBlock } from "@/types/report";
import { cn } from "@/lib/utils";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import {
  Edit2,
  Check,
  X,
  Bold,
  Italic,
  Underline,
  List,
  AlignLeft,
  AlignCenter,
  AlignRight,
  Heading1,
  Heading2,
} from "lucide-react";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import type { JSX } from "react/jsx-runtime";

interface TextEditorProps {
  report: ReportDocument;
  selectedBlockId: string | null;
  onBlockSelect: (blockId: string) => void;
  onReportChange: (report: ReportDocument) => void;
  onTextHighlight: (
    blockId: string,
    selectedText: string,
    startIndex: number,
    endIndex: number
  ) => void;
}

export function TextEditor({
  report,
  selectedBlockId,
  onBlockSelect,
  onReportChange,
  onTextHighlight,
}: TextEditorProps) {
  const [editingBlockId, setEditingBlockId] = useState<string | null>(null);
  const [editedContent, setEditedContent] = useState("");
  const [selectedText, setSelectedText] = useState({
    text: "",
    startIndex: 0,
    endIndex: 0,
  });
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  const handleBlockClick = (blockId: string) => {
    if (editingBlockId !== blockId) {
      onBlockSelect(blockId);
    }
  };

  const startEditing = (block: ReportBlock) => {
    setEditingBlockId(block.id);
    setEditedContent(block.content);
  };

  const saveEditing = () => {
    if (!editingBlockId) return;

    const updatedReport = {
      ...report,
      blocks: report.blocks.map((block) =>
        block.id === editingBlockId
          ? { ...block, content: editedContent }
          : block
      ),
      updatedAt: new Date().toISOString(),
    };

    onReportChange(updatedReport);
    setEditingBlockId(null);
  };

  const cancelEditing = () => {
    setEditingBlockId(null);
  };

  const handleTextSelection = (blockId: string) => {
    if (window.getSelection) {
      const selection = window.getSelection();
      if (selection && selection.toString().length > 0) {
        const range = selection.getRangeAt(0);
        const selectedText = selection.toString();

        // Get the parent element of the selection
        const parentElement = range.commonAncestorContainer.parentElement;

        // Make sure we're selecting within the correct block
        if (
          parentElement &&
          parentElement.closest(`[data-block-id="${blockId}"]`)
        ) {
          // Calculate the start and end indices of the selection
          const blockContent =
            report.blocks.find((b) => b.id === blockId)?.content || "";
          const startIndex = blockContent.indexOf(selectedText);
          const endIndex = startIndex + selectedText.length;

          if (startIndex >= 0) {
            setSelectedText({ text: selectedText, startIndex, endIndex });
            onTextHighlight(blockId, selectedText, startIndex, endIndex);
          }
        }
      }
    }
  };

  const applyFormatting = (format: string) => {
    if (!editingBlockId || !textAreaRef.current) return;

    const textarea = textAreaRef.current;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = editedContent.substring(start, end);

    let formattedText = "";
    let newCursorPosition = end;

    switch (format) {
      case "bold":
        formattedText = `**${selectedText}**`;
        newCursorPosition = end + 4;
        break;
      case "italic":
        formattedText = `*${selectedText}*`;
        newCursorPosition = end + 2;
        break;
      case "underline":
        formattedText = `__${selectedText}__`;
        newCursorPosition = end + 4;
        break;
      case "h1":
        formattedText = `# ${selectedText}`;
        newCursorPosition = end + 2;
        break;
      case "h2":
        formattedText = `## ${selectedText}`;
        newCursorPosition = end + 3;
        break;
      case "list":
        formattedText = `- ${selectedText}`;
        newCursorPosition = end + 2;
        break;
      default:
        return;
    }

    const newContent =
      editedContent.substring(0, start) +
      formattedText +
      editedContent.substring(end);
    setEditedContent(newContent);

    // Set cursor position after the formatting
    setTimeout(() => {
      textarea.focus();
      textarea.setSelectionRange(newCursorPosition, newCursorPosition);
    }, 0);
  };

  // Function to render tagged content with highlighting
  const renderTaggedContent = (block: ReportBlock) => {
    if (block.tags.length === 0) {
      return <p className="whitespace-pre-wrap">{block.content}</p>;
    }

    // Sort tags by their position in the text
    const sortedTags = [...block.tags].sort((a, b) => {
      const aPos = a.startIndex || 0;
      const bPos = b.startIndex || 0;
      return aPos - bPos;
    });

    // Create an array of text segments and tagged segments
    const segments: JSX.Element[] = [];
    let lastIndex = 0;

    sortedTags.forEach((tag, index) => {
      const startIndex = tag.startIndex || 0;
      const endIndex = tag.endIndex || block.content.length;

      // Add text before the tag
      if (startIndex > lastIndex) {
        segments.push(
          <span key={`text-${index}`}>
            {block.content.substring(lastIndex, startIndex)}
          </span>
        );
      }

      // Add the tagged text
      segments.push(
        <HoverCard key={`tag-${tag.id}`}>
          <HoverCardTrigger asChild>
            <span
              className="bg-primary/20 px-0.5 rounded cursor-help border-b border-dashed border-primary"
              data-tag-id={tag.id}
            >
              {block.content.substring(startIndex, endIndex)}
            </span>
          </HoverCardTrigger>
          <HoverCardContent className="w-80">
            <div className="space-y-2">
              <h4 className="font-medium">{tag.concept.label}</h4>
              <p className="text-sm text-muted-foreground">
                {tag.concept.definition}
              </p>
              <div className="flex flex-wrap gap-2 pt-1">
                <Badge variant="outline">{tag.concept.type}</Badge>
                <Badge variant="outline">{tag.concept.periodType}</Badge>
              </div>
              <Separator />
              <div className="text-xs">
                <p className="font-medium">Context: {tag.context.label}</p>
                <p className="text-muted-foreground mt-1">
                  Entity: {tag.context.entityName} (
                  {tag.context.entityIdentifier})
                </p>
                <p className="text-muted-foreground">
                  Period:{" "}
                  {tag.context.periodType === "instant"
                    ? `As of ${new Date(
                        tag.context.instantDate || ""
                      ).toLocaleDateString()}`
                    : `${new Date(
                        tag.context.startDate || ""
                      ).toLocaleDateString()} to ${new Date(
                        tag.context.endDate || ""
                      ).toLocaleDateString()}`}
                </p>
              </div>
            </div>
          </HoverCardContent>
        </HoverCard>
      );

      lastIndex = endIndex;
    });

    // Add any remaining text
    if (lastIndex < block.content.length) {
      segments.push(
        <span key="text-last">{block.content.substring(lastIndex)}</span>
      );
    }

    return <div className="whitespace-pre-wrap">{segments}</div>;
  };

  return (
    <div className="space-y-4 max-h-[600px] overflow-y-auto p-2 border ">
      {report.blocks.map((block) => (
        <div
          // key={block.id}
          data-block-id={block.id}
          className={cn(
            "p-3 rounded-md border transition-colors",
            selectedBlockId === block.id && !editingBlockId
              ? "border-primary bg-primary/5"
              : "border-border hover:border-primary/50",
            editingBlockId === block.id ? "border-primary" : ""
          )}
          onClick={() => handleBlockClick(block.id)}
          onMouseUp={() =>
            selectedBlockId === block.id && handleTextSelection(block.id)
          }
        >
          {editingBlockId === block.id ? (
            <div className="space-y-2 ">
              <div className="bg-muted p-1 rounded-md flex flex-wrap gap-1 mb-2">
                <TooltipProvider delayDuration={300}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => applyFormatting("bold")}
                      >
                        <Bold className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Bold</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider delayDuration={300}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => applyFormatting("italic")}
                      >
                        <Italic className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Italic</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider delayDuration={300}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => applyFormatting("underline")}
                      >
                        <Underline className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Underline</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <Separator orientation="vertical" className="h-6 mx-1" />

                <TooltipProvider delayDuration={300}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => applyFormatting("h1")}
                      >
                        <Heading1 className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Heading 1</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider delayDuration={300}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => applyFormatting("h2")}
                      >
                        <Heading2 className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Heading 2</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider delayDuration={300}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => applyFormatting("list")}
                      >
                        <List className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>List</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <Separator orientation="vertical" className="h-6 mx-1" />

                <TooltipProvider delayDuration={300}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button size="icon" variant="ghost">
                        <AlignLeft className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Align Left</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider delayDuration={300}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button size="icon" variant="ghost">
                        <AlignCenter className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Align Center</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider delayDuration={300}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button size="icon" variant="ghost">
                        <AlignRight className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Align Right</TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>

              <div className="h-[40rem]">
                <Textarea
                  ref={textAreaRef}
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                  className="h-full w-full"
                  autoFocus
                />
              </div>
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
              <div className="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity">
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={(e) => {
                    e.stopPropagation();
                    startEditing(block);
                  }}
                >
                  <Edit2 className="h-4 w-4" />
                </Button>
              </div>
              <div className="prose dark:prose-invert max-w-none">
                {renderTaggedContent(block)}
              </div>
              {block.tags.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
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
  );
}
