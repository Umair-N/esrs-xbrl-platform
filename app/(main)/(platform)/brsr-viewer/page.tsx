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

export default function InteractiveViewerPage() {
  // File state
  const [file, setFile] = useState<File | null>(null);
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
  const [isPanelCollapsed, setIsPanelCollapsed] = useState(false);

  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Mutations
  const convertMutation = useConvertInteractive();
  const updateTagsMutation = useUpdateTags();

  // Get tags for selected cell
  const selectedTags = selectedCellId && result?.tag_mapping
    ? result.tag_mapping[selectedCellId] || []
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

  // Auto-process when file is selected
  useEffect(() => {
    if (!file || convertMutation.isPending) return;

    const processFile = async () => {
      try {
        const data = await convertMutation.mutateAsync({ file });
        setResult(data);
        setPendingUpdates([]);
      } catch (error) {
        console.error('Conversion failed:', error);
      }
    };

    processFile();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [file]);

  // Handle cell click from iframe
  const handleCellClick = useCallback((cellId: string, cellText: string) => {
    setSelectedCellId(cellId);
    setSelectedCellText(cellText);
    setEditingTagIndex(null);
    setIsPanelCollapsed(false);
  }, []);

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

      // Add click handlers
      const cells = doc.querySelectorAll('.xml-linked');
      console.log(`[Viewer] Found ${cells.length} tagged cells`);

      cells.forEach((cell) => {
        cell.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();

          const cellId = (cell as HTMLElement).getAttribute('data-id');
          const cellText = (cell as HTMLElement).textContent?.trim() || '';

          // Update selection visuals
          cells.forEach((c) => c.classList.remove('selected'));
          cell.classList.add('selected');

          if (cellId) {
            handleCellClick(cellId, cellText);
          }
        });
      });
    };

    iframe.onload = setupIframe;
    const timer = setTimeout(setupIframe, 100);
    return () => clearTimeout(timer);
  }, [result?.annotated_html, handleCellClick]);

  // Close panel
  const closePanel = useCallback(() => {
    setSelectedCellId(null);
    setEditingTagIndex(null);

    const doc = iframeRef.current?.contentDocument;
    if (doc) {
      doc.querySelectorAll('.xml-linked.selected').forEach((cell) => {
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

  // Save edit
  const saveEdit = useCallback((tag: TagInfo) => {
    if (!selectedCellId) return;

    const hasValueChange = editingField === 'value' && editValue !== tag.v;
    const hasTagChange = editingField === 'tag' && editTagName !== tag.t;

    if (hasValueChange || hasTagChange) {
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

    // Apply pending updates if any
    if (pendingUpdates.length > 0) {
      try {
        const updateResult = await updateTagsMutation.mutateAsync({
          originalXbrl: xbrlContent,
          updates: pendingUpdates,
        });
        xbrlContent = updateResult.updated_xbrl;
      } catch (error) {
        console.error('Failed to apply updates:', error);
      }
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
  }, [result, pendingUpdates, updateTagsMutation, file]);

  // Handle escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (editingTagIndex !== null) {
          cancelEdit();
        } else if (selectedCellId) {
          closePanel();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [closePanel, cancelEdit, editingTagIndex, selectedCellId]);

  // Reset everything
  const handleReset = useCallback(() => {
    setFile(null);
    setResult(null);
    setSelectedCellId(null);
    setPendingUpdates([]);
    convertMutation.reset();
  }, [convertMutation]);

  // If no result, show upload screen
  if (!result) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800">
        {/* Header */}
        <div className="border-b border-slate-200 bg-white/80 backdrop-blur-sm dark:border-slate-700 dark:bg-slate-900/80">
          <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg">
                <Tag className="h-7 w-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900 dark:text-white sm:text-3xl">
                  BRSR Interactive Viewer
                </h1>
                <p className="mt-1 text-slate-600 dark:text-slate-400">
                  Upload your BRSR HTML file to view and edit XBRL tags interactively
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Upload Area */}
        <div className="mx-auto max-w-2xl px-4 py-16">
          <div
            onDrop={handleDrop}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onClick={() => fileInputRef.current?.click()}
            className={cn(
              'relative cursor-pointer rounded-2xl border-2 border-dashed p-16 text-center transition-all',
              isDragging
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-950/30'
                : 'border-slate-300 bg-white hover:border-blue-400 hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:hover:border-blue-500'
            )}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".html,.htm"
              onChange={handleFileSelect}
              className="hidden"
            />

            {convertMutation.isPending ? (
              <div className="flex flex-col items-center">
                <Loader2 className="h-16 w-16 animate-spin text-blue-500" />
                <p className="mt-4 text-lg font-medium text-slate-700 dark:text-slate-300">
                  Processing {file?.name}...
                </p>
                <p className="mt-2 text-sm text-slate-500">
                  Parsing HTML and generating XBRL tags
                </p>
              </div>
            ) : (
              <>
                <Upload className={cn(
                  'mx-auto h-16 w-16 transition-colors',
                  isDragging ? 'text-blue-500' : 'text-slate-400'
                )} />
                <p className="mt-4 text-lg font-medium text-slate-700 dark:text-slate-300">
                  Drop your BRSR HTML file here
                </p>
                <p className="mt-2 text-sm text-slate-500">
                  or click to browse (.html, .htm)
                </p>
              </>
            )}
          </div>

          {convertMutation.isError && (
            <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-950/30">
              <p className="text-sm text-red-700 dark:text-red-300">
                {convertMutation.error?.message || 'Failed to process file'}
              </p>
              <button
                onClick={handleReset}
                className="mt-2 text-sm font-medium text-red-600 hover:text-red-800 dark:text-red-400"
              >
                Try again
              </button>
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
              <span className="font-medium text-green-600">{Number(result.statistics.cells_with_xbrl_tags) || 0}</span>
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

                    {/* Tags */}
                    {selectedTags.length === 0 ? (
                      <div className="flex flex-col items-center justify-center py-8 text-slate-400">
                        <Info className="mb-3 h-10 w-10" />
                        <p className="text-sm font-medium">No XML mapping found</p>
                        <p className="mt-1 text-xs">This cell has no associated XBRL tag</p>
                      </div>
                    ) : (
                      <div className="space-y-3">
                        {selectedTags.map((tag, index) => {
                          // Check if this tag has been updated
                          const pendingUpdate = pendingUpdates.find(
                            (u) => u.cell_id === selectedCellId && u.tag === tag.t
                          );
                          const displayValue = pendingUpdate?.new_value || tag.v;
                          const isModified = !!pendingUpdate;

                          return (
                            <div
                              key={index}
                              className={cn(
                                'overflow-hidden rounded-lg border',
                                isModified
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
                                        onClick={() => saveEdit(tag)}
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
                                  </div>
                                )}
                                <div className="flex items-center gap-1 shrink-0">
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
                                          if (e.key === 'Enter') saveEdit(tag);
                                          if (e.key === 'Escape') cancelEdit();
                                        }}
                                      />
                                      <button
                                        onClick={() => saveEdit(tag)}
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
              {pendingUpdates.length > 0 && (
                <div className="border-t border-slate-200 p-3 dark:border-slate-700">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-500">
                      {pendingUpdates.length} unsaved change{pendingUpdates.length > 1 ? 's' : ''}
                    </span>
                    <button
                      onClick={() => setPendingUpdates([])}
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
