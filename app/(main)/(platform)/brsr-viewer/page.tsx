'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import {
  X,
  Copy,
  Check,
  Edit3,
  Save,
  Download,
  Tag,
  FileCode,
  Info,
  Loader2,
  Upload,
  ChevronLeft,
  ChevronRight,
  RefreshCw,
  Trash2,
  Plus,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { TagSelector } from '@/components/ui/tag-selector';
import {
  useConvertInteractive,
  useUpdateTags,
  type InteractiveConversionResult,
  type TagUpdate,
  type TagInfo,
} from '@/features/brsr-validator/api';

// Available taxonomies
const TAXONOMIES = [
  { value: 'brsr', label: 'BRSR (Business Responsibility & Sustainability Reporting)', description: 'Indian sustainability reporting standard' },
  // Future taxonomies can be added here
  // { value: 'gri', label: 'GRI (Global Reporting Initiative)', description: 'International sustainability standard' },
  // { value: 'sasb', label: 'SASB (Sustainability Accounting Standards Board)', description: 'Industry-specific sustainability standards' },
] as const;

export default function InteractiveViewerPage() {
  // File state
  const [file, setFile] = useState<File | null>(null);
  const [selectedTaxonomy, setSelectedTaxonomy] = useState<string>('');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Viewer state
  const [result, setResult] = useState<InteractiveConversionResult | null>(null);
  const [selectedCellId, setSelectedCellId] = useState<string | null>(null);
  const [selectedCellText, setSelectedCellText] = useState<string>('');
  const [editingTagIndex, setEditingTagIndex] = useState<number | null>(null);
  const [editingField, setEditingField] = useState<'value' | 'tag'>('value');
  const [editValue, setEditValue] = useState<string>('');
  const [editTagName, setEditTagName] = useState<string>('');
  const [copiedTag, setCopiedTag] = useState<string | null>(null);
  const [pendingUpdates, setPendingUpdates] = useState<TagUpdate[]>([]);
  const [removedTags, setRemovedTags] = useState<Set<string>>(new Set());
  const [isPanelCollapsed, setIsPanelCollapsed] = useState(false);
  const [isAddingNewTag, setIsAddingNewTag] = useState(false);
  const [newTagName, setNewTagName] = useState<string>('');
  const [newTags, setNewTags] = useState<Map<string, TagInfo[]>>(new Map());

  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Mutations
  const convertMutation = useConvertInteractive();
  const updateTagsMutation = useUpdateTags();

  // Get tags for selected cell
  const selectedTags = selectedCellId && result?.tag_mapping
    ? [
        ...(result.tag_mapping[selectedCellId] || []).filter((tag) => {
          const tagKey = `${selectedCellId}:${tag.t}`;
          return !removedTags.has(tagKey);
        }),
        ...(newTags.get(selectedCellId) || [])
      ]
    : [];

  // Max file size (10MB)
  const MAX_FILE_SIZE = 10 * 1024 * 1024;

  // Handle file drop
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile?.name.match(/\.(html|htm)$/i)) {
      if (droppedFile.size > MAX_FILE_SIZE) {
        alert(`File too large. Maximum size is 10MB. Your file is ${(droppedFile.size / 1024 / 1024).toFixed(1)}MB`);
        return;
      }
      setFile(droppedFile);
    }
  }, []);

  // Handle file select
  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.size > MAX_FILE_SIZE) {
        alert(`File too large. Maximum size is 10MB. Your file is ${(selectedFile.size / 1024 / 1024).toFixed(1)}MB`);
        return;
      }
      setFile(selectedFile);
    }
  }, []);

  // Auto-process when both file and taxonomy are selected
  useEffect(() => {
    if (!file || !selectedTaxonomy || convertMutation.isPending) return;

    const processFile = async () => {
      try {
        const data = await convertMutation.mutateAsync({ file });
        setResult(data);
        setPendingUpdates([]);
        setRemovedTags(new Set());
      } catch (error) {
        console.error('Conversion failed:', error);
      }
    };

    processFile();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [file, selectedTaxonomy]);

  // Handle cell click from iframe
  const handleCellClick = useCallback((cellId: string, cellText: string) => {
    // Check if cell has any tags (original or newly added)
    const hasOriginalTags = result?.tag_mapping[cellId]?.some((tag) => {
      const tagKey = `${cellId}:${tag.t}`;
      return !removedTags.has(tagKey);
    });
    
    const hasNewTags = newTags.has(cellId) && (newTags.get(cellId)?.length || 0) > 0;
    
    const hasTags = hasOriginalTags || hasNewTags;

    setSelectedCellId(cellId);
    setSelectedCellText(cellText);
    setEditingTagIndex(null);
    setIsPanelCollapsed(false);
    setIsAddingNewTag(false);
    setNewTagName('');
  }, [result, removedTags, newTags]);

  // Update cell styling based on removed tags
  const updateCellStyling = useCallback(() => {
    const doc = iframeRef.current?.contentDocument;
    if (!doc || !result) return;

    const cells = doc.querySelectorAll('.xml-linked');
    cells.forEach((cell) => {
      const cellId = (cell as HTMLElement).getAttribute('data-id');
      if (!cellId) return;

      // Check if cell has any remaining tags (original or new)
      const cellTags = result.tag_mapping[cellId] || [];
      const hasRemainingOriginalTags = cellTags.some((tag) => {
        const tagKey = `${cellId}:${tag.t}`;
        return !removedTags.has(tagKey);
      });

      const hasNewTagsForCell = newTags.has(cellId) && (newTags.get(cellId)?.length || 0) > 0;
      const hasRemainingTags = hasRemainingOriginalTags || hasNewTagsForCell;

      // Update styling - remove ALL styling if no tags remain
      if (hasRemainingTags) {
        cell.classList.add('has-tag');
        cell.classList.add('xml-linked');
        (cell as HTMLElement).style.cursor = 'pointer';
      } else {
        cell.classList.remove('has-tag');
        cell.classList.remove('xml-linked');
        cell.classList.remove('selected');
        // Remove all custom styling
        (cell as HTMLElement).style.borderLeft = '';
        (cell as HTMLElement).style.backgroundColor = '';
        (cell as HTMLElement).style.cursor = 'text';
        (cell as HTMLElement).style.outline = '';
        (cell as HTMLElement).style.outlineOffset = '';
      }
    });
  }, [result, removedTags, newTags]);

  // Update cell styling when removed tags change
  useEffect(() => {
    updateCellStyling();
  }, [updateCellStyling]);

  // Setup iframe content and click handlers
  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe || !result?.annotated_html) return;

    const setupIframe = () => {
      const doc = iframe.contentDocument;
      if (!doc) return;

      // Enhanced styles
      const enhancedStyles = `
        <style>
          * { box-sizing: border-box; }
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 24px;
            background: #ffffff;
            line-height: 1.6;
            color: #1f2937;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 13px;
            background: white;
          }
          th, td {
            border: 1px solid #e5e7eb;
            padding: 10px 12px;
            text-align: left;
            vertical-align: top;
            cursor: pointer;
            user-select: text;
          }
          th {
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
            position: sticky;
            top: 0;
          }
          tr:hover td {
            background: #f9fafb;
          }

          /* Tagged cells - subtle border indicators */
          .xml-linked {
            cursor: pointer;
            transition: all 0.15s ease;
            position: relative;
            border-left: 3px solid transparent !important;
          }
          .xml-linked:not(.has-tag) {
            border-left-color: #f59e0b !important;
            background-color: rgba(254, 243, 199, 0.3) !important;
          }
          .xml-linked.has-tag {
            border-left-color: #10b981 !important;
            background-color: rgba(209, 250, 229, 0.2) !important;
          }
          .xml-linked:hover {
            outline: 2px solid #3b82f6;
            outline-offset: -1px;
            z-index: 1;
            background-color: rgba(191, 219, 254, 0.4) !important;
          }
          .xml-linked.selected {
            outline: 3px solid #1d4ed8 !important;
            outline-offset: -1px;
            background-color: #bfdbfe !important;
            z-index: 2;
          }

          /* Tag indicator badge */
          .xml-linked.has-tag::after {
            content: '';
            position: absolute;
            top: 2px;
            right: 2px;
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            border: 1px solid white;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
          }

          /* Selectable cells (any td) */
          td.cell-selectable {
            cursor: text;
            transition: background-color 0.15s ease;
          }
          td.cell-selectable:hover {
            background-color: rgba(191, 219, 254, 0.2) !important;
          }
          td.cell-selectable.selected {
            outline: 2px solid #3b82f6;
            outline-offset: -1px;
            background-color: rgba(191, 219, 254, 0.3) !important;
          }

          h1, h2, h3, h4, h5, h6 {
            color: #111827;
            margin-top: 24px;
            margin-bottom: 12px;
            font-weight: 600;
          }
          h1 { font-size: 24px; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; }
          h2 { font-size: 20px; }
          h3 { font-size: 18px; }
          h4 { font-size: 16px; }
          p {
            margin: 12px 0;
            color: #4b5563;
          }

          /* Section headers */
          .section-header {
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            color: white;
            padding: 16px;
            margin: 24px 0 16px;
            border-radius: 8px;
            font-weight: 600;
          }
        </style>
      `;

      // Build HTML content
      const hasHtmlTag = result.annotated_html.toLowerCase().includes('<html');
      let htmlContent: string;

      if (hasHtmlTag) {
        if (result.annotated_html.toLowerCase().includes('<head>')) {
          htmlContent = result.annotated_html.replace(/<head>/i, `<head>${enhancedStyles}`);
        } else if (result.annotated_html.toLowerCase().includes('<body')) {
          htmlContent = result.annotated_html.replace(/<body/i, `<head>${enhancedStyles}</head><body`);
        } else {
          htmlContent = result.annotated_html;
        }
      } else {
        htmlContent = `<!DOCTYPE html><html><head>${enhancedStyles}</head><body>${result.annotated_html}</body></html>`;
      }

      doc.open();
      doc.write(htmlContent);
      doc.close();

      // Add click handlers to all table cells
      const allCells = doc.querySelectorAll('td');
      console.log(`[Viewer] Found ${allCells.length} total cells`);

      allCells.forEach((cell, cellIndex) => {
        // Add selectable class to all cells
        cell.classList.add('cell-selectable');
        
        // Generate a cell ID if it doesn't have one
        let cellId = (cell as HTMLElement).getAttribute('data-id');
        if (!cellId) {
          cellId = `cell-${cellIndex}`;
          (cell as HTMLElement).setAttribute('data-id', cellId);
        }

        // Check if this cell has new tags and should be highlighted
        if (newTags.has(cellId) && (newTags.get(cellId)?.length || 0) > 0) {
          cell.classList.add('xml-linked', 'has-tag');
          (cell as HTMLElement).style.cursor = 'pointer';
        }

        cell.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();

          const cellText = (cell as HTMLElement).textContent?.trim() || '';

          // Update selection visuals
          allCells.forEach((c) => c.classList.remove('selected'));
          cell.classList.add('selected');

          if (cellId) {
            handleCellClick(cellId, cellText);
          }
        });
      });

      // Apply initial styling for xml-linked cells
      updateCellStyling();
    };

    iframe.onload = setupIframe;
    const timer = setTimeout(setupIframe, 100);
    return () => clearTimeout(timer);
  }, [result?.annotated_html, handleCellClick, updateCellStyling, newTags]);

  // Close panel
  const closePanel = useCallback(() => {
    setSelectedCellId(null);
    setEditingTagIndex(null);

    const doc = iframeRef.current?.contentDocument;
    if (doc) {
      doc.querySelectorAll('.selected').forEach((cell) => {
        cell.classList.remove('selected');
      });
    }
  }, []);

  // Copy tag name
  const copyTag = useCallback((tagName: string) => {
    navigator.clipboard.writeText(tagName);
    setCopiedTag(tagName);
    setTimeout(() => setCopiedTag(null), 2000);
  }, []);

  // Start editing value
  const startEditValue = useCallback((index: number, currentValue: string) => {
    setEditingTagIndex(index);
    setEditingField('value');
    setEditValue(currentValue);
  }, []);

  // Start editing tag name
  const startEditTag = useCallback((index: number, currentTag: string) => {
    setEditingTagIndex(index);
    setEditingField('tag');
    setEditTagName(currentTag);
  }, []);

  // Add new tag
  const addNewTag = useCallback(() => {
    if (!selectedCellId || !newTagName || !selectedCellText) return;

    const newTag = {
      t: newTagName,
      v: selectedCellText,
      c: 'instant',
      p: undefined,
      u: undefined,
      d: [],
      s: 'User Added',
      orig_v: selectedCellText,
    } as TagInfo & { orig_v?: string };

    setNewTags((prev) => {
      const updated = new Map(prev);
      const existing = updated.get(selectedCellId) || [];
      updated.set(selectedCellId, [...existing, newTag]);
      return updated;
    });

    // Update cell styling in iframe to show it's now tagged
    const doc = iframeRef.current?.contentDocument;
    if (doc) {
      const cell = doc.querySelector(`[data-id="${selectedCellId}"]`);
      if (cell) {
        cell.classList.add('xml-linked', 'has-tag');
        (cell as HTMLElement).style.cursor = 'pointer';
      }
    }

    setIsAddingNewTag(false);
    setNewTagName('');
  }, [selectedCellId, newTagName, selectedCellText]);

  // Undo a value change (for original tags remove pending update; for new tags restore original value)
  const undoValue = useCallback((tag: TagInfo, isNewTag: boolean = false) => {
    if (!selectedCellId) return;

    if (isNewTag) {
      setNewTags((prev) => {
        const updated = new Map(prev);
        const existing = updated.get(selectedCellId) || [];
        const restored = existing.map((t) => {
          if (t.t === tag.t) {
            const orig = (t as any).orig_v ?? tag.v ?? '';
            return { ...t, v: orig } as TagInfo;
          }
          return t;
        });
        updated.set(selectedCellId, restored);
        return updated;
      });

      try {
        const doc = iframeRef.current?.contentDocument;
        const cell = doc?.querySelector(`[data-id="${selectedCellId}"]`);
        if (cell) {
          const orig = (tag as any).orig_v ?? tag.v ?? '';
          (cell as HTMLElement).textContent = orig;
        }
      } catch (e) {
        // ignore
      }
    } else {
      setPendingUpdates((prev) => prev.filter((u) => !(u.cell_id === selectedCellId && u.tag === tag.t)));

      try {
        const doc = iframeRef.current?.contentDocument;
        const cell = doc?.querySelector(`[data-id="${selectedCellId}"]`);
        if (cell) {
          (cell as HTMLElement).textContent = tag.v || '';
        }
      } catch (e) {
        // ignore
      }
    }
  }, [selectedCellId]);

  // Remove tag
  const removeTag = useCallback((tag: TagInfo, isNewTag: boolean = false) => {
    if (!selectedCellId) return;

    // Show confirmation dialog
    const confirmed = window.confirm(
      `Are you sure you want to remove this tag?\n\nTag: ${tag.t}\nValue: ${tag.v}\n\nThis action will remove the tag from the XML output.`
    );

    if (!confirmed) return;

    if (isNewTag) {
      // Remove from new tags
      setNewTags((prev) => {
        const updated = new Map(prev);
        const existing = updated.get(selectedCellId) || [];
        const filtered = existing.filter(t => t.t !== tag.t || t.v !== tag.v);
        if (filtered.length === 0) {
          updated.delete(selectedCellId);
        } else {
          updated.set(selectedCellId, filtered);
        }
        return updated;
      });
    } else {
      // Remove from original tags
      const tagKey = `${selectedCellId}:${tag.t}`;
      setRemovedTags((prev) => new Set(prev).add(tagKey));

      // Also remove any pending updates for this tag
      setPendingUpdates((prev) =>
        prev.filter((u) => !(u.cell_id === selectedCellId && u.tag === tag.t))
      );
    }

    // Check if this was the last tag for the selected cell
    const originalTags = result?.tag_mapping[selectedCellId] || [];
    const remainingOriginalTags = originalTags.filter((t) => {
      const tKey = `${selectedCellId}:${t.t}`;
      return !removedTags.has(tKey) && !(t.t === tag.t && !isNewTag);
    });
    
    const remainingNewTags = isNewTag 
      ? (newTags.get(selectedCellId) || []).filter(t => t.t !== tag.t || t.v !== tag.v)
      : (newTags.get(selectedCellId) || []);

    // If no tags remain, remove highlighting and close the panel
    if (remainingOriginalTags.length === 0 && remainingNewTags.length === 0) {
      // Remove cell highlighting
      const doc = iframeRef.current?.contentDocument;
      if (doc) {
        const cell = doc.querySelector(`[data-id="${selectedCellId}"]`);
        if (cell) {
          cell.classList.remove('xml-linked', 'has-tag', 'selected');
          (cell as HTMLElement).style.borderLeft = '';
          (cell as HTMLElement).style.backgroundColor = '';
          (cell as HTMLElement).style.cursor = 'text';
          (cell as HTMLElement).style.outline = '';
          (cell as HTMLElement).style.outlineOffset = '';
        }
      }
      closePanel();
    }
  }, [selectedCellId, result, removedTags, newTags, closePanel]);

  // Save edit
  const saveEdit = useCallback((tag: TagInfo, isNewTag: boolean = false) => {
    if (!selectedCellId) return;

    const hasValueChange = editingField === 'value' && editValue !== tag.v;
    const hasTagChange = editingField === 'tag' && editTagName !== tag.t;

    if (hasValueChange || hasTagChange) {
      if (isNewTag) {
        // Update new tag directly
        setNewTags((prev) => {
          const updated = new Map(prev);
          const existing = updated.get(selectedCellId) || [];
          const updatedTags = existing.map(t => {
            if (t.t === tag.t && t.v === tag.v) {
              return {
                ...t,
                t: editingField === 'tag' ? editTagName : t.t,
                v: editingField === 'value' ? editValue : t.v,
              };
            }
            return t;
          });
          updated.set(selectedCellId, updatedTags);
          return updated;
        });

          // Reflect value change in iframe immediately (keep everything else unchanged)
          if (editingField === 'value') {
            try {
              const doc = iframeRef.current?.contentDocument;
              const cell = doc?.querySelector(`[data-id="${selectedCellId}"]`);
              if (cell) {
                (cell as HTMLElement).textContent = editValue;
                cell.classList.add('xml-linked', 'has-tag');
                (cell as HTMLElement).style.cursor = 'pointer';
              }
            } catch (e) {
              // ignore DOM update errors
            }
          }
      } else {
        // Add to pending updates for original tags
        const update: TagUpdate = {
          cell_id: selectedCellId,
          tag: tag.t,
          old_value: tag.v,
          new_value: editingField === 'value' ? editValue : tag.v,
          new_tag: editingField === 'tag' ? editTagName : undefined,
        };

        setPendingUpdates((prev) => {
          const existingIndex = prev.findIndex(
            (u) => u.cell_id === selectedCellId && u.tag === tag.t
          );
          if (existingIndex >= 0) {
            const newUpdates = [...prev];
            newUpdates[existingIndex] = { ...newUpdates[existingIndex], ...update };
            return newUpdates;
          }
          return [...prev, update];
        });

        // Reflect pending value change in iframe immediately (keep everything else unchanged)
        if (editingField === 'value') {
          try {
            const doc = iframeRef.current?.contentDocument;
            const cell = doc?.querySelector(`[data-id="${selectedCellId}"]`);
            if (cell) {
              (cell as HTMLElement).textContent = editValue;
              cell.classList.add('xml-linked', 'has-tag');
              (cell as HTMLElement).style.cursor = 'pointer';
            }
          } catch (e) {
            // ignore DOM update errors
          }
        }
      }
    }
    setEditingTagIndex(null);
    setEditingField('value');
  }, [selectedCellId, editValue, editTagName, editingField]);

  // Cancel edit
  const cancelEdit = useCallback(() => {
    setEditingTagIndex(null);
    setEditingField('value');
    setEditValue('');
    setEditTagName('');
  }, []);

  // Download XML with updates
  const handleDownload = useCallback(async () => {
    if (!result?.xbrl_content) return;

    let xbrlContent = result.xbrl_content;

    try {
      // Parse XML
      const parser = new DOMParser();
      let xmlDoc = parser.parseFromString(xbrlContent, 'text/xml');

      // Check for parse errors
      const parseError = xmlDoc.querySelector('parsererror');
      if (parseError) {
        throw new Error('Failed to parse XML');
      }

      // Step 1: Apply value updates manually
      if (pendingUpdates.length > 0) {
        pendingUpdates.forEach((update) => {
          // Find elements with matching tag name
          const elements = xmlDoc.getElementsByTagName(update.tag);
          
          for (let i = 0; i < elements.length; i++) {
            const element = elements[i];
            const currentValue = element.textContent?.trim();
            
            // Match by old value to ensure we're updating the right element
            if (currentValue === update.old_value) {
              element.textContent = update.new_value;
              console.log(`Updated ${update.tag}: "${update.old_value}" → "${update.new_value}"`);
            }
          }

          // If tag name changed, rename the element
          if (update.new_tag && update.new_tag !== update.tag) {
            const elements = xmlDoc.getElementsByTagName(update.tag);
            for (let i = elements.length - 1; i >= 0; i--) {
              const element = elements[i];
              const currentValue = element.textContent?.trim();
              
              if (currentValue === update.new_value || currentValue === update.old_value) {
                // Create new element with new tag name
                const newElement = xmlDoc.createElement(update.new_tag);
                newElement.textContent = update.new_value;
                
                // Copy attributes
                for (let j = 0; j < element.attributes.length; j++) {
                  const attr = element.attributes[j];
                  newElement.setAttribute(attr.name, attr.value);
                }
                
                // Replace old element
                element.parentNode?.replaceChild(newElement, element);
                console.log(`Renamed tag: ${update.tag} → ${update.new_tag}`);
              }
            }
          }
        });
      }

      // Step 2: Add new tags to XML
      if (newTags.size > 0) {
        const rootElement = xmlDoc.documentElement;
        
        newTags.forEach((tags, cellId) => {
          tags.forEach((tag) => {
            const newElement = xmlDoc.createElement(tag.t);
            newElement.textContent = tag.v;
            
            // Add contextRef attribute if available
            if (tag.c) {
              newElement.setAttribute('contextRef', tag.c);
            }
            
            // Add unitRef if available
            if (tag.u) {
              newElement.setAttribute('unitRef', tag.u);
            }
            
            // Add decimals attribute for numeric values
            if (!isNaN(parseFloat(tag.v))) {
              newElement.setAttribute('decimals', '0');
            }
            
            rootElement.appendChild(newElement);
            console.log(`Added new tag: ${tag.t} = ${tag.v}`);
          });
        });
      }

      // Step 3: Remove tags from XML
      if (removedTags.size > 0) {
        let removalCount = 0;

        removedTags.forEach((tagKey) => {
          // Extract tag name from key (format: "cellId:tagName")
          const tagName = tagKey.split(':').slice(1).join(':');
          
          // Find and remove all elements with this tag name
          const elements = xmlDoc.getElementsByTagName(tagName);
          
          // Convert to array and remove (iterate backwards to avoid index issues)
          const elementsArray = Array.from(elements);
          elementsArray.forEach((element) => {
            element.parentNode?.removeChild(element);
            removalCount++;
          });
        });

        console.log(`Removed ${removalCount} tag elements from XML`);
      }

      // Serialize back to string
      const serializer = new XMLSerializer();
      xbrlContent = serializer.serializeToString(xmlDoc);

      console.log(`Applied ${pendingUpdates.length} updates, added ${newTags.size} new tag groups, removed ${removedTags.size} tags`);
    } catch (error) {
      console.error('Failed to apply updates:', error);
      alert(`Failed to apply updates to XML: ${error instanceof Error ? error.message : 'Unknown error'}`);
      return;
    }

    // Download
    const blob = new Blob([xbrlContent], { type: 'application/xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file?.name.replace(/\.(html|htm)$/i, '.xml') || 'brsr_output.xml';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [result, pendingUpdates, removedTags, newTags, file]);

  // Handle escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (isAddingNewTag) {
          setIsAddingNewTag(false);
          setNewTagName('');
        } else if (editingTagIndex !== null) {
          cancelEdit();
        } else if (selectedCellId) {
          closePanel();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [closePanel, cancelEdit, editingTagIndex, selectedCellId, isAddingNewTag]);

  // Reset everything
  const handleReset = useCallback(() => {
    setFile(null);
    setSelectedTaxonomy('');
    setResult(null);
    setSelectedCellId(null);
    setPendingUpdates([]);
    setRemovedTags(new Set());
    setNewTags(new Map());
    setIsAddingNewTag(false);
    setNewTagName('');
    convertMutation.reset();
  }, [convertMutation]);

  // If no result, show upload screen
  if (!result) {
    const canProcess = file && selectedTaxonomy;

    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800">
        {/* Header */}
        <div className="border-b border-slate-200 bg-white/80 backdrop-blur-sm dark:border-slate-700 dark:bg-slate-900/80">
          <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
            <div className="flex items-center gap-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg">
                <Tag className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
                  Interactive XBRL Viewer
                </h1>
                <p className="mt-1 text-slate-600 dark:text-slate-400">
                  Select taxonomy and upload your file to view and edit XBRL tags
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Upload Area */}
        <div className="mx-auto max-w-4xl px-4 py-12">
          {/* Step Indicator */}
          <div className="mb-8 flex items-center justify-center gap-4">
            <div className="flex items-center gap-2">
              <div className={cn(
                "flex h-8 w-8 items-center justify-center rounded-full font-semibold text-sm transition-all",
                selectedTaxonomy
                  ? "bg-green-500 text-white"
                  : "bg-blue-500 text-white"
              )}>
                1
              </div>
              <span className={cn(
                "font-medium text-sm",
                selectedTaxonomy ? "text-green-600 dark:text-green-400" : "text-blue-600 dark:text-blue-400"
              )}>
                Select Taxonomy
              </span>
            </div>
            <div className="h-0.5 w-12 bg-slate-300 dark:bg-slate-600" />
            <div className="flex items-center gap-2">
              <div className={cn(
                "flex h-8 w-8 items-center justify-center rounded-full font-semibold text-sm transition-all",
                file
                  ? "bg-green-500 text-white"
                  : selectedTaxonomy
                  ? "bg-blue-500 text-white"
                  : "bg-slate-300 dark:bg-slate-600 text-slate-600 dark:text-slate-400"
              )}>
                2
              </div>
              <span className={cn(
                "font-medium text-sm",
                file
                  ? "text-green-600 dark:text-green-400"
                  : selectedTaxonomy
                  ? "text-blue-600 dark:text-blue-400"
                  : "text-slate-500 dark:text-slate-400"
              )}>
                Upload File
              </span>
            </div>
          </div>

          {/* Taxonomy Selector Card */}
          <div className="mb-6 rounded-2xl border-2 border-slate-200 bg-white p-6 shadow-lg dark:border-slate-700 dark:bg-slate-800">
            <div className="mb-4 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 text-white">
                <FileCode className="h-5 w-5" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-white">
                  Step 1: Select Taxonomy
                </h2>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Choose the reporting standard for your document
                </p>
              </div>
            </div>

            <div className="grid gap-3">
              {TAXONOMIES.map((taxonomy) => (
                <button
                  key={taxonomy.value}
                  onClick={() => setSelectedTaxonomy(taxonomy.value)}
                  className={cn(
                    "group relative flex items-start gap-4 rounded-xl border-2 p-4 text-left transition-all",
                    selectedTaxonomy === taxonomy.value
                      ? "border-blue-500 bg-blue-50 dark:border-blue-600 dark:bg-blue-950/30"
                      : "border-slate-200 bg-white hover:border-blue-300 hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:hover:border-blue-600"
                  )}
                >
                  <div className={cn(
                    "mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition-all",
                    selectedTaxonomy === taxonomy.value
                      ? "border-blue-500 bg-blue-500"
                      : "border-slate-300 bg-white dark:border-slate-600 dark:bg-slate-700"
                  )}>
                    {selectedTaxonomy === taxonomy.value && (
                      <Check className="h-4 w-4 text-white" />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-slate-900 dark:text-white">
                      {taxonomy.label}
                    </div>
                    <div className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                      {taxonomy.description}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* File Upload Card */}
          <div className={cn(
            "rounded-2xl border-2 transition-all",
            selectedTaxonomy
              ? "border-slate-200 bg-white shadow-lg dark:border-slate-700 dark:bg-slate-800"
              : "border-slate-200 bg-slate-100 opacity-60 dark:border-slate-700 dark:bg-slate-900"
          )}>
            <div className="p-6">
              <div className="mb-4 flex items-center gap-3">
                <div className={cn(
                  "flex h-10 w-10 items-center justify-center rounded-lg text-white transition-all",
                  selectedTaxonomy
                    ? "bg-gradient-to-br from-blue-500 to-indigo-600"
                    : "bg-slate-400"
                )}>
                  <Upload className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-slate-900 dark:text-white">
                    Step 2: Upload HTML File
                  </h2>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    {selectedTaxonomy ? "Drag and drop or click to browse" : "Select a taxonomy first"}
                  </p>
                </div>
              </div>

              <div
                onDrop={selectedTaxonomy ? handleDrop : undefined}
                onDragOver={selectedTaxonomy ? (e) => { e.preventDefault(); setIsDragging(true); } : undefined}
                onDragLeave={selectedTaxonomy ? () => setIsDragging(false) : undefined}
                onClick={selectedTaxonomy ? () => fileInputRef.current?.click() : undefined}
                className={cn(
                  'relative rounded-xl border-2 border-dashed p-12 text-center transition-all',
                  !selectedTaxonomy && 'cursor-not-allowed opacity-50',
                  selectedTaxonomy && (
                    isDragging
                      ? 'border-blue-500 bg-blue-50 cursor-pointer dark:bg-blue-950/30'
                      : 'border-slate-300 bg-slate-50 hover:border-blue-400 hover:bg-blue-50/50 cursor-pointer dark:border-slate-600 dark:bg-slate-700/50 dark:hover:border-blue-500'
                  )
                )}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".html,.htm"
                  onChange={handleFileSelect}
                  className="hidden"
                  disabled={!selectedTaxonomy}
                />

                {convertMutation.isPending ? (
                  <div className="flex flex-col items-center">
                    <Loader2 className="h-14 w-14 animate-spin text-blue-500" />
                    <p className="mt-4 text-lg font-semibold text-slate-700 dark:text-slate-300">
                      Processing {file?.name}...
                    </p>
                    <p className="mt-2 text-sm text-slate-500">
                      Parsing HTML and generating XBRL tags for {TAXONOMIES.find(t => t.value === selectedTaxonomy)?.label}
                    </p>
                  </div>
                ) : file ? (
                  <div className="flex flex-col items-center">
                    <div className="flex h-14 w-14 items-center justify-center rounded-full bg-green-100 dark:bg-green-900">
                      <Check className="h-7 w-7 text-green-600 dark:text-green-400" />
                    </div>
                    <p className="mt-4 text-lg font-semibold text-slate-700 dark:text-slate-300">
                      {file.name}
                    </p>
                    <p className="mt-1 text-sm text-slate-500">
                      {(file.size / 1024).toFixed(1)} KB • Ready to process
                    </p>
                  </div>
                ) : (
                  <>
                    <Upload className={cn(
                      'mx-auto h-14 w-14 transition-colors',
                      isDragging ? 'text-blue-500' : 'text-slate-400'
                    )} />
                    <p className="mt-4 text-lg font-semibold text-slate-700 dark:text-slate-300">
                      {selectedTaxonomy ? 'Drop your HTML file here' : 'Select taxonomy first'}
                    </p>
                    <p className="mt-2 text-sm text-slate-500">
                      {selectedTaxonomy ? 'or click to browse • .html, .htm files up to 10MB' : 'Taxonomy selection is required'}
                    </p>
                  </>
                )}
              </div>

              {file && selectedTaxonomy && !convertMutation.isPending && (
                <div className="mt-4 flex items-center justify-between gap-4 rounded-lg border border-green-200 bg-green-50 px-4 py-3 dark:border-green-800 dark:bg-green-950/30">
                  <div className="flex items-center gap-3">
                    <Check className="h-5 w-5 text-green-600 dark:text-green-400" />
                    <p className="text-sm font-medium text-green-700 dark:text-green-300">
                      Ready to process with {TAXONOMIES.find(t => t.value === selectedTaxonomy)?.label.split('(')[0].trim()}
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setFile(null);
                      setSelectedTaxonomy('');
                    }}
                    className="text-sm font-medium text-green-600 hover:text-green-800 dark:text-green-400"
                  >
                    Reset
                  </button>
                </div>
              )}
            </div>
          </div>

          {convertMutation.isError && (
            <div className="mt-6 rounded-xl border-2 border-red-200 bg-red-50 p-5 dark:border-red-800 dark:bg-red-950/30">
              <div className="flex items-start gap-3">
                <Info className="h-5 w-5 text-red-600 dark:text-red-400 mt-0.5" />
                <div className="flex-1">
                  <p className="font-semibold text-red-700 dark:text-red-300">
                    Processing Failed
                  </p>
                  <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                    {convertMutation.error?.message || 'An error occurred while processing your file'}
                  </p>
                  <button
                    onClick={handleReset}
                    className="mt-3 font-medium text-sm text-red-600 hover:text-red-800 dark:text-red-400 underline"
                  >
                    Try again
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Main viewer interface
  return (
    <div className="flex h-screen flex-col bg-slate-100 dark:bg-slate-900">
      {/* Top Bar */}
      <div className="flex items-center justify-between border-b border-slate-200 bg-white px-4 py-2 dark:border-slate-700 dark:bg-slate-800">
        <div className="flex items-center gap-4">
          <button
            onClick={handleReset}
            className="flex items-center gap-2 rounded-lg px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-700"
          >
            <RefreshCw className="h-4 w-4" />
            New File
          </button>
          <div className="h-6 w-px bg-slate-200 dark:bg-slate-700" />
          <div className="flex items-center gap-2">
            <Tag className="h-4 w-4 text-blue-600" />
            <span className="font-medium text-slate-900 dark:text-white">
              {file?.name}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Stats */}
          <div className="flex items-center gap-4 text-sm text-slate-600 dark:text-slate-400">
            <span>
              <span className="font-medium text-green-600">
                {Number(result.statistics.cells_with_xbrl_tags) - removedTags.size + Array.from(newTags.values()).reduce((sum, tags) => sum + tags.length, 0) || 0}
              </span>
              {' '}matched tags
            </span>
            <span>
              <span className="font-medium">{Number(result.statistics.total_cells) || 0}</span>
              {' '}total cells
            </span>
          </div>

          {/* Pending updates badge */}
          {pendingUpdates.length > 0 && (
            <div className="flex items-center gap-2 rounded-full bg-amber-100 px-3 py-1 text-xs font-medium text-amber-700 dark:bg-amber-900/30 dark:text-amber-300">
              {pendingUpdates.length} pending change{pendingUpdates.length > 1 ? 's' : ''}
            </div>
          )}

          {/* Removed tags badge */}
          {removedTags.size > 0 && (
            <div className="flex items-center gap-2 rounded-full bg-red-100 px-3 py-1 text-xs font-medium text-red-700 dark:bg-red-900/30 dark:text-red-300">
              {removedTags.size} removed
            </div>
          )}

          {/* Download button */}
          <button
            onClick={handleDownload}
            disabled={updateTagsMutation.isPending}
            className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {updateTagsMutation.isPending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Download className="h-4 w-4" />
            )}
            Download XML
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* HTML Viewer */}
        <div className="flex-1 overflow-hidden">
          <iframe
            ref={iframeRef}
            className="h-full w-full border-none bg-white"
            title="BRSR Report"
          />
        </div>

        {/* Tag Panel */}
        <div
          className={cn(
            'flex flex-col border-l border-slate-200 bg-white transition-all duration-300 dark:border-slate-700 dark:bg-slate-800',
            isPanelCollapsed ? 'w-12' : 'w-[400px]'
          )}
        >
          {/* Panel Toggle */}
          <button
            onClick={() => setIsPanelCollapsed(!isPanelCollapsed)}
            className="flex items-center justify-center border-b border-slate-200 p-2 hover:bg-slate-50 dark:border-slate-700 dark:hover:bg-slate-700"
          >
            {isPanelCollapsed ? (
              <ChevronLeft className="h-5 w-5 text-slate-500" />
            ) : (
              <ChevronRight className="h-5 w-5 text-slate-500" />
            )}
          </button>

          {!isPanelCollapsed && (
            <>
              {/* Panel Header */}
              <div className="border-b border-slate-200 p-4 dark:border-slate-700">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <FileCode className="h-5 w-5 text-blue-600" />
                    <span className="font-semibold text-slate-900 dark:text-white">
                      Tag Details
                    </span>
                  </div>
                  {selectedCellId && (
                    <button
                      onClick={closePanel}
                      className="rounded p-1 hover:bg-slate-100 dark:hover:bg-slate-700"
                    >
                      <X className="h-4 w-4 text-slate-500" />
                    </button>
                  )}
                </div>

                {selectedCellId && (
                  <p className="mt-1 text-xs text-slate-500">
                    Cell ID: {selectedCellId}
                  </p>
                )}
              </div>

              {/* Panel Content */}
              <div className="flex-1 overflow-y-auto p-4">
                {!selectedCellId ? (
                  <div className="flex flex-col items-center justify-center py-16 text-slate-400">
                    <Tag className="mb-4 h-12 w-12" />
                    <p className="text-center font-medium">
                      Click on any highlighted cell
                    </p>
                    <p className="mt-1 text-center text-sm">
                      to view its XBRL tag information
                    </p>
                    <div className="mt-6 space-y-2 text-xs">
                      <div className="flex items-center gap-2">
                        <div className="h-4 w-4 rounded bg-green-200" />
                        <span>Matched XBRL tag</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="h-4 w-4 rounded bg-amber-200" />
                        <span>Unmatched (placeholder)</span>
                      </div>
                    </div>
                  </div>
                ) : (
                  <>
                    {/* Selected Value */}
                    <div className="mb-4 rounded-lg border border-blue-200 bg-blue-50 p-3 dark:border-blue-800 dark:bg-blue-950/30">
                      <p className="text-xs font-medium text-blue-600 dark:text-blue-400">
                        Selected Value
                      </p>
                      <p className="mt-1 break-words text-sm text-blue-900 dark:text-blue-100">
                        {selectedCellText || '-'}
                      </p>
                    </div>

                    {/* Add Tag Button - Only show if cell has no tags */}
                    {selectedTags.length === 0 && !isAddingNewTag && (
                      <button
                        onClick={() => setIsAddingNewTag(true)}
                        className="mb-4 flex w-full items-center justify-center gap-2 rounded-lg border-2 border-dashed border-blue-300 bg-blue-50 px-4 py-3 text-sm font-medium text-blue-600 transition-colors hover:border-blue-400 hover:bg-blue-100 dark:border-blue-700 dark:bg-blue-950/30 dark:text-blue-400"
                      >
                        <Plus className="h-4 w-4" />
                        Add New Tag
                      </button>
                    )}

                    {/* Add Tag Interface - Only show if cell has no tags */}
                    {selectedTags.length === 0 && isAddingNewTag && (
                      <div className="mb-4 rounded-lg border border-blue-300 bg-blue-50 p-3 dark:border-blue-700 dark:bg-blue-950/30">
                        <p className="mb-2 text-xs font-medium text-blue-600 dark:text-blue-400">
                          Add New Tag
                        </p>
                        <TagSelector
                          value={newTagName}
                          onValueChange={setNewTagName}
                          placeholder="Search BRSR tags..."
                          className="mb-2"
                        />
                        <div className="flex gap-2">
                          <button
                            onClick={addNewTag}
                            disabled={!newTagName}
                            className="flex-1 rounded bg-green-500 px-3 py-2 text-xs font-medium text-white hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <Save className="h-3 w-3 inline mr-1" />
                            Add Tag
                          </button>
                          <button
                            onClick={() => {
                              setIsAddingNewTag(false);
                              setNewTagName('');
                            }}
                            className="flex-1 rounded bg-slate-300 px-3 py-2 text-xs font-medium text-slate-600 hover:bg-slate-400"
                          >
                            <X className="h-3 w-3 inline mr-1" />
                            Cancel
                          </button>
                        </div>
                      </div>
                    )}

                    {/* Tags */}
                    {selectedTags.length === 0 ? (
                      <div className="flex flex-col items-center justify-center py-8 text-slate-400">
                        <Info className="mb-3 h-10 w-10" />
                        <p className="text-sm font-medium">No XML mapping found</p>
                        <p className="mt-1 text-xs">Click "Add New Tag" to create one</p>
                      </div>
                    ) : (
                      <div className="space-y-3">
                        {selectedTags.map((tag, index) => {
                          // Determine if this is a new tag
                          const isNewTag = tag.s === 'User Added';
                          
                          // Check if this tag has been updated
                          const pendingUpdate = !isNewTag ? pendingUpdates.find(
                            (u) => u.cell_id === selectedCellId && u.tag === tag.t
                          ) : undefined;
                          const displayValue = pendingUpdate?.new_value || tag.v;
                          const isModified = !!pendingUpdate;

                          return (
                            <div
                              key={`${index}-${tag.t}-${tag.v}`}
                              className={cn(
                                'overflow-hidden rounded-lg border',
                                isNewTag
                                  ? 'border-green-300 bg-green-50 dark:border-green-700 dark:bg-green-950/30'
                                  : isModified
                                  ? 'border-amber-300 bg-amber-50 dark:border-amber-700 dark:bg-amber-950/30'
                                  : 'border-slate-200 bg-white dark:border-slate-600 dark:bg-slate-700'
                              )}
                            >
                              {/* Tag Header */}
                              <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-3 py-2 dark:border-slate-600 dark:bg-slate-600">
                                {editingTagIndex === index && editingField === 'tag' ? (
                                  <div className="flex flex-1 flex-col gap-2 mr-2">
                                    <TagSelector
                                      value={editTagName}
                                      onValueChange={setEditTagName}
                                      placeholder="Search BRSR tags..."
                                      className="flex-1"
                                    />
                                    <div className="flex gap-1">
                                      <button
                                        onClick={() => saveEdit(tag, isNewTag)}
                                        className="flex-1 rounded bg-green-500 px-2 py-1 text-xs text-white hover:bg-green-600"
                                      >
                                        <Save className="h-3 w-3 inline mr-1" />
                                        Save
                                      </button>
                                      <button
                                        onClick={cancelEdit}
                                        className="flex-1 rounded bg-slate-300 px-2 py-1 text-xs text-slate-600 hover:bg-slate-400"
                                      >
                                        <X className="h-3 w-3 inline mr-1" />
                                        Cancel
                                      </button>
                                    </div>
                                  </div>
                                ) : (
                                  <div className="flex items-center gap-1 min-w-0 flex-1 mr-2">
                                    <code
                                      className="truncate text-xs font-semibold text-blue-600 dark:text-blue-400 cursor-pointer hover:underline"
                                      onClick={() => startEditTag(index, pendingUpdate?.new_tag || tag.t)}
                                      title="Click to edit tag name"
                                    >
                                      {pendingUpdate?.new_tag || tag.t}
                                    </code>
                                    <button
                                      onClick={() => startEditTag(index, pendingUpdate?.new_tag || tag.t)}
                                      className="shrink-0 p-0.5 text-slate-400 hover:text-blue-600"
                                      title="Edit tag name"
                                    >
                                      <Edit3 className="h-3 w-3" />
                                    </button>
                                    <button
                                      onClick={() => removeTag(tag, isNewTag)}
                                      className="shrink-0 p-0.5 text-slate-400 hover:text-red-600"
                                      title="Remove tag"
                                    >
                                      <Trash2 className="h-3 w-3" />
                                    </button>
                                  </div>
                                )}
                                <div className="flex items-center gap-1 shrink-0">
                                  {isNewTag && (
                                    <span className="rounded bg-green-200 px-1.5 py-0.5 text-[10px] font-medium text-green-700 dark:bg-green-800 dark:text-green-200">
                                      New
                                    </span>
                                  )}
                                  {isModified && (
                                    <span className="rounded bg-amber-200 px-1.5 py-0.5 text-[10px] font-medium text-amber-700 dark:bg-amber-800 dark:text-amber-200">
                                      Modified
                                    </span>
                                  )}
                                  <button
                                    onClick={() => copyTag(pendingUpdate?.new_tag || tag.t)}
                                    className={cn(
                                      'flex items-center gap-1 rounded px-2 py-0.5 text-xs transition-colors',
                                      copiedTag === (pendingUpdate?.new_tag || tag.t)
                                        ? 'bg-green-100 text-green-700'
                                        : 'bg-slate-200 text-slate-600 hover:bg-slate-300'
                                    )}
                                  >
                                    {copiedTag === (pendingUpdate?.new_tag || tag.t) ? (
                                      <>
                                        <Check className="h-3 w-3" />
                                        Copied
                                      </>
                                    ) : (
                                      <>
                                        <Copy className="h-3 w-3" />
                                        Copy
                                      </>
                                    )}
                                  </button>
                                </div>
                              </div>

                              {/* Tag Body */}
                              <div className="space-y-2 p-3 text-xs">
                                {/* Value */}
                                <div className="flex items-start gap-2">
                                  <span className="w-16 shrink-0 font-medium text-slate-500">
                                    Value:
                                  </span>
                                  {editingTagIndex === index && editingField === 'value' ? (
                                    <div className="flex flex-1 items-center gap-1">
                                      <input
                                        type="text"
                                        value={editValue}
                                        onChange={(e) => setEditValue(e.target.value)}
                                        className="flex-1 rounded border border-slate-300 px-2 py-1 text-xs focus:border-blue-500 focus:outline-none dark:border-slate-500 dark:bg-slate-600"
                                        autoFocus
                                        onKeyDown={(e) => {
                                          if (e.key === 'Enter') saveEdit(tag, isNewTag);
                                          if (e.key === 'Escape') cancelEdit();
                                        }}
                                      />
                                      <button
                                        onClick={() => saveEdit(tag, isNewTag)}
                                        className="rounded bg-green-500 p-1 text-white hover:bg-green-600"
                                      >
                                        <Save className="h-3 w-3" />
                                      </button>
                                      <button
                                        onClick={cancelEdit}
                                        className="rounded bg-slate-300 p-1 text-slate-600 hover:bg-slate-400"
                                      >
                                        <X className="h-3 w-3" />
                                      </button>
                                    </div>
                                  ) : (
                                    <div className="flex flex-1 items-start justify-between gap-1">
                                      <code className="break-all rounded bg-slate-100 px-1.5 py-0.5 text-slate-700 dark:bg-slate-600 dark:text-slate-300">
                                        {displayValue}
                                      </code>
                                      {/* Undo button (reset to original) */}
                                      {(
                                        (!isNewTag && isModified) ||
                                        (isNewTag && ((tag as any).orig_v && (tag as any).orig_v !== tag.v))
                                      ) && (
                                        <button
                                          onClick={() => undoValue(tag, isNewTag)}
                                          className="shrink-0 mr-2 flex items-center gap-1 rounded border border-slate-200 px-2 py-1 text-xs text-slate-600 hover:bg-slate-100"
                                          title="Undo value change"
                                        >
                                          Undo
                                        </button>
                                      )}

                                      <button
                                        onClick={() => startEditValue(index, displayValue)}
                                        className="shrink-0 flex items-center gap-1 rounded border border-blue-200 px-2 py-1 text-xs text-blue-600 hover:bg-blue-50 dark:border-blue-700 dark:text-blue-400"
                                      >
                                        <Edit3 className="h-3 w-3" />
                                        Edit
                                      </button>
                                    </div>
                                  )}
                                </div>

                                {/* Context */}
                                <div className="flex items-start gap-2">
                                  <span className="w-16 shrink-0 font-medium text-slate-500">
                                    Context:
                                  </span>
                                  <span className="text-slate-700 dark:text-slate-300">
                                    {tag.c}
                                  </span>
                                </div>

                                {/* Period */}
                                {tag.p && (
                                  <div className="flex items-start gap-2">
                                    <span className="w-16 shrink-0 font-medium text-slate-500">
                                      Period:
                                    </span>
                                    <span className="text-slate-700 dark:text-slate-300">
                                      {tag.p}
                                    </span>
                                  </div>
                                )}

                                {/* Unit */}
                                {tag.u && (
                                  <div className="flex items-start gap-2">
                                    <span className="w-16 shrink-0 font-medium text-slate-500">
                                      Unit:
                                    </span>
                                    <span className="text-slate-700 dark:text-slate-300">
                                      {tag.u}
                                    </span>
                                  </div>
                                )}

                                {/* Dimensions */}
                                {tag.d && tag.d.length > 0 && (
                                  <div className="flex items-start gap-2">
                                    <span className="w-16 shrink-0 font-medium text-slate-500">
                                      Dims:
                                    </span>
                                    <div className="flex flex-1 flex-wrap gap-1">
                                      {tag.d.map((dim, i) => (
                                        <span
                                          key={i}
                                          className="rounded bg-indigo-100 px-1.5 py-0.5 text-[10px] text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300"
                                        >
                                          {dim}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                )}

                                {/* Source */}
                                {tag.s && (
                                  <div className="flex items-start gap-2">
                                    <span className="w-16 shrink-0 font-medium text-slate-500">
                                      Source:
                                    </span>
                                    <span className="italic text-slate-500">
                                      {tag.s}
                                    </span>
                                  </div>
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </>
                )}
              </div>

              {/* Pending Updates Footer */}
              {(pendingUpdates.length > 0 || removedTags.size > 0) && (
                <div className="border-t border-slate-200 p-3 dark:border-slate-700">
                  <div className="flex items-center justify-between">
                    <div className="text-xs text-slate-500">
                      {pendingUpdates.length > 0 && (
                        <span>{pendingUpdates.length} unsaved change{pendingUpdates.length > 1 ? 's' : ''}</span>
                      )}
                      {pendingUpdates.length > 0 && removedTags.size > 0 && <span> • </span>}
                      {removedTags.size > 0 && (
                        <span>{removedTags.size} removed</span>
                      )}
                    </div>
                    <button
                      onClick={() => {
                        setPendingUpdates([]);
                        setRemovedTags(new Set());
                      }}
                      className="text-xs text-red-600 hover:text-red-800"
                    >
                      Discard all
                    </button>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}