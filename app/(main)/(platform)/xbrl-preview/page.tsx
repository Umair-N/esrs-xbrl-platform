'use client';
import type React from 'react';
import { useState, useRef } from 'react';
import { Upload, FileText, Download, X, ZoomIn, ZoomOut } from 'lucide-react';

interface XBRLFact {
  id: number;
  elementId: string;
  name: string;
  value: string;
  contextRef: string;
  unitRef: string;
  decimals: string;
  precision: string;
  scale: string;
  format: string;
  element: string;
  className: string;
  attributes: Record<string, string>;
  xpath: string;
  position: {
    text: string;
    parent: string;
  };
}

interface XBRLContext {
  id: string;
  entity: string;
  period: {
    instant: string;
    startDate: string;
    endDate: string;
  };
}

interface ParsedData {
  facts: XBRLFact[];
  contexts: XBRLContext[];
  units: any[];
  namespaces: Record<string, string>;
  schemaRefs: any[];
  rawContent: string;
  processedHTML: string;
  documentElement: string;
  totalElements: number;
  taggedElements: Map<string, XBRLFact>;
}

type ViewMode = 'upload' | 'document' | 'table';

const IXBRLViewer: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [parsedData, setParsedData] = useState<ParsedData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [showMetadata, setShowMetadata] = useState<boolean>(false);
  const [selectedTag, setSelectedTag] = useState<XBRLFact | null>(null);
  const [hoveredTag, setHoveredTag] = useState<XBRLFact | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('upload');
  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const parseIXBRL = (content: string): ParsedData => {
    try {
      // Try parsing as HTML first
      let doc: Document;
      try {
        doc = new DOMParser().parseFromString(content, 'text/html');
        if (!doc.body || doc.body.innerHTML === '') {
          doc = new DOMParser().parseFromString(content, 'application/xml');
        }
      } catch {
        doc = new DOMParser().parseFromString(content, 'application/xml');
      }

      const facts: XBRLFact[] = [];
      const taggedElements = new Map<string, XBRLFact>();

      // Look for ix: prefixed elements
      const ixElements = doc.querySelectorAll(
        '*[class*="ix"], ix\\:nonFraction, ix\\:nonNumeric, ix\\:fraction'
      );

      // Look for elements with XBRL attributes
      const xbrlAttrElements = doc.querySelectorAll(
        '[name*=":"], [contextRef], [unitRef], [decimals]'
      );

      // Look for namespaced elements
      const namespacedElements = doc.querySelectorAll(
        '[name^="us-gaap:"], [name^="dei:"], [name^="ifrs:"]'
      );

      // Combine all potential XBRL elements
      const allPotentialElements = new Set([
        ...Array.from(ixElements),
        ...Array.from(xbrlAttrElements),
        ...Array.from(namespacedElements),
      ]);

      // If no elements found, check all elements for XBRL indicators
      if (allPotentialElements.size === 0) {
        const allElements = doc.querySelectorAll('*');
        Array.from(allElements).forEach((element) => {
          const hasXbrlIndicators =
            element.getAttribute('name') ||
            element.getAttribute('contextRef') ||
            element.getAttribute('unitRef') ||
            element.tagName.includes(':') ||
            element.className?.includes('ix');

          if (hasXbrlIndicators) {
            allPotentialElements.add(element);
          }
        });
      }

      Array.from(allPotentialElements).forEach((element, index) => {
        // Add unique identifier to element for highlighting
        element.setAttribute('data-xbrl-id', `xbrl-${index}`);

        const fact: XBRLFact = {
          id: index,
          elementId: `xbrl-${index}`,
          name: element.getAttribute('name') || element.tagName,
          value: element.textContent?.trim() || '',
          contextRef: element.getAttribute('contextRef') || '',
          unitRef: element.getAttribute('unitRef') || '',
          decimals: element.getAttribute('decimals') || '',
          precision: element.getAttribute('precision') || '',
          scale: element.getAttribute('scale') || '',
          format: element.getAttribute('format') || '',
          element: element.tagName,
          className: element.className || '',
          attributes: Array.from(element.attributes).reduce(
            (acc, attr) => {
              acc[attr.name] = attr.value;
              return acc;
            },
            {} as Record<string, string>
          ),
          xpath: getElementXPath(element),
          position: {
            text: element.textContent?.substring(0, 100) + '...',
            parent: element.parentElement?.tagName || 'unknown',
          },
        };

        if (fact.name && (fact.value || fact.contextRef || fact.unitRef)) {
          facts.push(fact);
          taggedElements.set(`xbrl-${index}`, fact);
        }
      });

      // Extract contexts
      const contexts: XBRLContext[] = [];
      const contextElements = doc.querySelectorAll(
        'xbrli\\:context, context, [id*="context"]'
      );
      contextElements.forEach((context) => {
        const contextData: XBRLContext = {
          id: context.getAttribute('id') || '',
          entity: context.querySelector('identifier')?.textContent || '',
          period: {
            instant: context.querySelector('instant')?.textContent || '',
            startDate: context.querySelector('startDate')?.textContent || '',
            endDate: context.querySelector('endDate')?.textContent || '',
          },
        };
        contexts.push(contextData);
      });

      // Extract namespaces
      const namespaces: Record<string, string> = {};
      if (doc.documentElement) {
        Array.from(doc.documentElement.attributes).forEach((attr) => {
          if (attr.name.startsWith('xmlns:') || attr.name === 'xmlns') {
            const prefix =
              attr.name === 'xmlns' ? 'default' : attr.name.substring(6);
            namespaces[prefix] = attr.value;
          }
        });
      }

      // Add highlighting styles to the document
      const style = doc.createElement('style');
      style.textContent = `
        [data-xbrl-id] {
          background-color: rgba(59, 130, 246, 0.1) !important;
          border: 1px solid rgba(59, 130, 246, 0.3) !important;
          cursor: pointer !important;
          transition: all 0.2s ease !important;
          position: relative !important;
        }
        [data-xbrl-id]:hover {
          background-color: rgba(59, 130, 246, 0.2) !important;
          border: 2px solid rgba(59, 130, 246, 0.6) !important;
          box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
        }
        [data-xbrl-id].selected {
          background-color: rgba(16, 185, 129, 0.2) !important;
          border: 2px solid rgba(16, 185, 129, 0.8) !important;
        }
      `;
      doc.head?.appendChild(style);

      console.log('Parsing results:', {
        factsFound: facts.length,
        contextsFound: contexts.length,
        documentType: doc.documentElement?.tagName,
        totalElements: doc.getElementsByTagName('*').length,
      });

      return {
        facts,
        contexts,
        units: [],
        namespaces,
        schemaRefs: [],
        rawContent: content,
        processedHTML: doc.documentElement.outerHTML,
        documentElement: doc.documentElement?.tagName || 'unknown',
        totalElements: doc.getElementsByTagName('*').length,
        taggedElements,
      };
    } catch (err) {
      console.error('Parse error:', err);
      throw new Error(`Failed to parse file: ${(err as Error).message}`);
    }
  };

  // Helper function to get XPath
  const getElementXPath = (element: Element): string => {
    if (element.id) return `//*[@id="${element.id}"]`;

    const parts: string[] = [];
    let currentElement: Element | null = element;
    while (currentElement && currentElement.nodeType === 1) {
      const tagName = currentElement.tagName.toLowerCase();
      let index = 1;

      const siblings = currentElement.parentNode?.children;
      if (siblings) {
        for (let i = 0; i < siblings.length; i++) {
          if (siblings[i] === currentElement) break;
          if (siblings[i].tagName.toLowerCase() === tagName) index++;
        }
      }

      parts.unshift(`${tagName}[${index}]`);
      currentElement = currentElement.parentNode as Element;
    }
    return '/' + parts.join('/');
  };

  const handleFileSelect = async (selectedFile: File): Promise<void> => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setParsedData(null);

    try {
      const content = await selectedFile.text();

      if (!content.trim()) {
        throw new Error('File is empty');
      }

      const parsed = parseIXBRL(content);
      setParsedData(parsed);
      setFile(selectedFile);
      setViewMode('document');
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleTagClick = (tagId: string): void => {
    const fact =
      parsedData?.taggedElements?.get(tagId) ||
      parsedData?.facts.find((f) => f.elementId === tagId);
    setSelectedTag(fact || null);

    // Highlight selected element
    const iframe = document.querySelector(
      '#document-viewer'
    ) as HTMLIFrameElement;
    if (iframe?.contentDocument) {
      // Remove previous selection
      iframe.contentDocument
        .querySelectorAll('[data-xbrl-id].selected')
        .forEach((el) => {
          el.classList.remove('selected');
        });

      // Add selection to current element
      const element = iframe.contentDocument.querySelector(
        `[data-xbrl-id="${tagId}"]`
      );
      if (element) {
        element.classList.add('selected');
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  };

  const allFacts = parsedData?.facts || [];

  const downloadJSON = (): void => {
    if (!parsedData) return;

    const dataStr = JSON.stringify(parsedData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${file?.name || 'ixbrl'}_parsed.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className='min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100'>
      <div className='container mx-auto px-2 py-4 max-w-full'>
        {/* Header - Reduced header size and spacing */}
        <div className='text-center mb-4'>
          <h1 className='text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2'>
            iXBRL Document Viewer
          </h1>
          <p className='text-lg text-gray-600'>
            Interactive iXBRL file analyzer with tag highlighting and metadata
            extraction
          </p>
        </div>

        {/* Navigation - Reduced padding and made more compact */}
        {parsedData && (
          <div className='bg-white rounded-lg shadow-lg p-3 mb-4'>
            <div className='flex flex-wrap gap-2 items-center justify-between'>
              <div className='flex gap-2'>
                <button
                  onClick={() => setViewMode('document')}
                  className={`px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
                    viewMode === 'document'
                      ? 'bg-blue-600 text-white shadow-md'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  📄 Document View
                </button>
                <button
                  onClick={() => setViewMode('table')}
                  className={`px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
                    viewMode === 'table'
                      ? 'bg-blue-600 text-white shadow-md'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  📊 Table View
                </button>
                <button
                  onClick={() => setViewMode('upload')}
                  className={`px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
                    viewMode === 'upload'
                      ? 'bg-blue-600 text-white shadow-md'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  📁 Upload New
                </button>
              </div>

              {viewMode === 'document' && (
                <div className='flex gap-1 items-center'>
                  <button
                    onClick={() => setZoomLevel(Math.max(50, zoomLevel - 25))}
                    className='p-1.5 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors'
                  >
                    <ZoomOut className='h-4 w-4' />
                  </button>
                  <span className='text-sm font-medium text-gray-600 min-w-[50px] text-center'>
                    {zoomLevel}%
                  </span>
                  <button
                    onClick={() => setZoomLevel(Math.min(200, zoomLevel + 25))}
                    className='p-1.5 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors'
                  >
                    <ZoomIn className='h-4 w-4' />
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Upload Section - Improved UI design */}
        {viewMode === 'upload' && (
          <div className='bg-white rounded-xl shadow-xl overflow-hidden max-w-4xl mx-auto'>
            <div className='bg-gradient-to-r from-blue-600 to-indigo-700 p-8'>
              <div className='text-center mb-6'>
                <Upload className='mx-auto h-12 w-12 text-white/90 mb-3' />
                <h3 className='text-2xl font-bold text-white mb-2'>
                  Upload iXBRL Document
                </h3>
                <p className='text-blue-100'>
                  Drag and drop your file or click to browse
                </p>
              </div>

              <div
                className='border-2 border-dashed border-white/40 rounded-xl p-8 cursor-pointer hover:border-white/70 hover:bg-white/5 transition-all duration-300 text-center'
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => {
                  e.preventDefault();
                  e.currentTarget.classList.add(
                    'border-white/70',
                    'bg-white/5'
                  );
                }}
                onDragLeave={(e) => {
                  e.preventDefault();
                  e.currentTarget.classList.remove(
                    'border-white/70',
                    'bg-white/5'
                  );
                }}
                onDrop={(e) => {
                  e.preventDefault();
                  e.currentTarget.classList.remove(
                    'border-white/70',
                    'bg-white/5'
                  );
                  const droppedFile = e.dataTransfer.files?.[0];
                  if (droppedFile) {
                    handleFileSelect(droppedFile);
                  }
                }}
              >
                <div className='space-y-3'>
                  <div className='text-white/80 text-lg font-medium'>
                    Choose your iXBRL file
                  </div>
                  <div className='text-white/60 text-sm'>
                    Supports .ixbrl, .xhtml, .html, .xml and other text formats
                  </div>
                  <div className='inline-flex items-center px-4 py-2 bg-white/20 backdrop-blur-sm rounded-lg text-white font-medium text-sm hover:bg-white/30 transition-colors'>
                    <FileText className='h-4 w-4 mr-2' />
                    Browse Files
                  </div>
                </div>

                <input
                  ref={fileInputRef}
                  type='file'
                  onChange={(e) => {
                    const selectedFile = e.target.files?.[0];
                    if (selectedFile) {
                      handleFileSelect(selectedFile);
                    }
                  }}
                  className='hidden'
                  accept='.ixbrl,.xhtml,.html,.xml,.txt'
                />
              </div>

              {file && (
                <div className='mt-6 p-4 bg-white/10 backdrop-blur-sm rounded-lg'>
                  <div className='flex items-center justify-between'>
                    <div className='flex items-center'>
                      <FileText className='h-5 w-5 text-white mr-3' />
                      <div>
                        <div className='text-white font-medium'>
                          {file.name}
                        </div>
                        <div className='text-white/70 text-sm'>
                          {(file.size / 1024).toFixed(1)} KB
                        </div>
                      </div>
                    </div>
                    <div className='text-white/80 text-sm'>
                      Ready to process
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Loading - Reduced spacing */}
        {loading && (
          <div className='text-center py-8'>
            <div className='inline-block animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600'></div>
            <p className='mt-3 text-gray-600'>
              Processing your iXBRL document...
            </p>
          </div>
        )}

        {/* Error - Reduced padding */}
        {error && (
          <div className='bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4'>
            <p className='font-semibold'>Error:</p>
            <p>{error}</p>
          </div>
        )}

        {/* Document View - Reduced gaps and made layout more compact */}
        {parsedData && viewMode === 'document' && (
          <div className='grid grid-cols-1 lg:grid-cols-4 gap-4'>
            {/* Main Document */}
            <div className='lg:col-span-3'>
              <div className='bg-white rounded-lg shadow-lg overflow-hidden'>
                <div className='p-3 border-b bg-gray-50 flex items-center justify-between'>
                  <h3 className='font-bold text-gray-800 text-sm'>
                    📄 {file?.name}
                  </h3>
                  <div className='flex gap-3 text-xs text-gray-600'>
                    <span>🏷️ {parsedData.facts.length} Tags</span>
                    <span>📊 {parsedData.totalElements} Elements</span>
                  </div>
                </div>
                <div
                  className='p-2 overflow-auto bg-white'
                  style={{ height: '85vh', fontSize: `${zoomLevel}%` }}
                >
                  <iframe
                    id='document-viewer'
                    srcDoc={parsedData.processedHTML}
                    className='w-full h-full border-0'
                    onLoad={(e) => {
                      const iframe = e.target as HTMLIFrameElement;
                      const doc = iframe.contentDocument;

                      // Add event listeners for tagged elements
                      doc
                        ?.querySelectorAll('[data-xbrl-id]')
                        .forEach((element) => {
                          element.addEventListener('mouseenter', () => {
                            const tagId = element.getAttribute('data-xbrl-id');
                            const fact = parsedData.facts.find(
                              (f) => f.elementId === tagId
                            );
                            setHoveredTag(fact || null);
                          });

                          element.addEventListener('mouseleave', () => {
                            setHoveredTag(null);
                          });

                          element.addEventListener('click', (e) => {
                            e.preventDefault();
                            const tagId = element.getAttribute('data-xbrl-id');
                            if (tagId) handleTagClick(tagId);
                          });
                        });
                    }}
                  />
                </div>
              </div>
            </div>

            {/* Sidebar - Fixed overflow issues */}
            <div className='space-y-4'>
              {/* Hovered Tag Info - Fixed overflow and text wrapping */}
              {hoveredTag && (
                <div className='bg-blue-50 border border-blue-200 rounded-lg p-3 overflow-hidden'>
                  <h4 className='font-bold text-blue-800 mb-2 text-sm'>
                    🏷️ Hovered Tag
                  </h4>
                  <div className='space-y-2 text-xs'>
                    <div className='break-words'>
                      <strong className='text-blue-700'>Name:</strong>
                      <div className='mt-1 p-2 bg-white rounded border font-mono text-xs break-all'>
                        {hoveredTag.name}
                      </div>
                    </div>
                    <div className='break-words'>
                      <strong className='text-blue-700'>Value:</strong>
                      <div className='mt-1 p-1 bg-white rounded border max-h-20 overflow-y-auto'>
                        {hoveredTag.value || (
                          <span className='text-gray-400 italic'>Empty</span>
                        )}
                      </div>
                    </div>
                    {hoveredTag.contextRef && (
                      <div className='break-words'>
                        <strong className='text-blue-700'>Context:</strong>
                        <div className='mt-1 p-1 bg-white rounded border font-mono text-xs break-all'>
                          {hoveredTag.contextRef}
                        </div>
                      </div>
                    )}
                    {hoveredTag.unitRef && (
                      <div className='break-words'>
                        <strong className='text-blue-700'>Unit:</strong>
                        <div className='mt-1 p-1 bg-white rounded border font-mono text-xs break-all'>
                          {hoveredTag.unitRef}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Quick Stats - Made more compact */}
              <div className='bg-white rounded-lg shadow-lg p-3'>
                <h4 className='font-bold text-gray-800 mb-2 text-sm'>
                  📊 Quick Stats
                </h4>
                <div className='space-y-1 text-xs'>
                  <div className='flex justify-between'>
                    <span>XBRL Facts:</span>
                    <span className='font-semibold text-blue-600'>
                      {parsedData.facts.length}
                    </span>
                  </div>
                  <div className='flex justify-between'>
                    <span>Contexts:</span>
                    <span className='font-semibold text-green-600'>
                      {parsedData.contexts.length}
                    </span>
                  </div>
                  <div className='flex justify-between'>
                    <span>Namespaces:</span>
                    <span className='font-semibold text-purple-600'>
                      {Object.keys(parsedData.namespaces).length}
                    </span>
                  </div>
                  <div className='flex justify-between'>
                    <span>Total Elements:</span>
                    <span className='font-semibold text-orange-600'>
                      {parsedData.totalElements}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Table View - Removed search functionality */}
        {parsedData && viewMode === 'table' && (
          <div className='space-y-4'>
            {/* Controls - Removed search input */}
            <div className='bg-white rounded-lg p-4 shadow-lg'>
              <div className='flex flex-wrap gap-3 items-center justify-between'>
                <div className='flex gap-3 items-center'>
                  <button
                    onClick={() => setShowMetadata(!showMetadata)}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      showMetadata
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {showMetadata ? 'Hide' : 'Show'} Metadata
                  </button>
                </div>
                <button
                  onClick={downloadJSON}
                  className='bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2 transition-colors'
                >
                  <Download className='h-4 w-4' />
                  Export JSON
                </button>
              </div>
            </div>

            {/* Metadata Panel - Reduced padding */}
            {showMetadata && (
              <div className='bg-white rounded-lg p-4 shadow-lg'>
                <h3 className='text-lg font-bold text-gray-800 mb-3'>
                  📋 File Metadata
                </h3>
                <div className='grid grid-cols-1 lg:grid-cols-2 gap-4'>
                  <div>
                    <h4 className='font-semibold text-gray-700 mb-2 text-sm'>
                      Namespaces ({Object.keys(parsedData.namespaces).length})
                    </h4>
                    <div className='bg-gray-50 rounded-md p-3 max-h-32 overflow-y-auto'>
                      {Object.entries(parsedData.namespaces).map(
                        ([prefix, uri]) => (
                          <div key={prefix} className='mb-1'>
                            <span className='font-mono text-xs bg-blue-100 px-1.5 py-0.5 rounded mr-2'>
                              {prefix}
                            </span>
                            <span className='text-xs text-gray-600 break-all'>
                              {uri}
                            </span>
                          </div>
                        )
                      )}
                      {Object.keys(parsedData.namespaces).length === 0 && (
                        <p className='text-gray-500 text-xs'>
                          No namespaces found
                        </p>
                      )}
                    </div>
                  </div>
                  <div>
                    <h4 className='font-semibold text-gray-700 mb-2 text-sm'>
                      Document Info
                    </h4>
                    <div className='bg-gray-50 rounded-md p-3 text-sm'>
                      <p>
                        <strong>Document Type:</strong>{' '}
                        {parsedData.documentElement}
                      </p>
                      <p>
                        <strong>Total Elements:</strong>{' '}
                        {parsedData.totalElements}
                      </p>
                      <p>
                        <strong>XBRL Facts:</strong> {parsedData.facts.length}
                      </p>
                      <p>
                        <strong>File Size:</strong>{' '}
                        {file
                          ? (file.size / 1024).toFixed(1) + ' KB'
                          : 'Unknown'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Facts Table - Updated to use allFacts instead of filteredFacts */}
            <div className='bg-white rounded-lg shadow-lg overflow-hidden'>
              <div className='p-4 border-b border-gray-200'>
                <h3 className='text-lg font-bold text-gray-800'>
                  🏷️ XBRL Facts ({allFacts.length})
                </h3>
              </div>
              <div className='overflow-x-auto'>
                <table className='min-w-full divide-y divide-gray-200'>
                  <thead className='bg-gray-50'>
                    <tr>
                      <th className='px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                        Name
                      </th>
                      <th className='px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                        Value
                      </th>
                      <th className='px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                        Context
                      </th>
                      <th className='px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                        Unit
                      </th>
                      <th className='px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className='bg-white divide-y divide-gray-200'>
                    {allFacts.slice(0, 50).map((fact) => (
                      <tr key={fact.id} className='hover:bg-gray-50'>
                        <td className='px-4 py-2 whitespace-nowrap'>
                          <span className='font-mono text-xs bg-blue-100 px-2 py-1 rounded break-all'>
                            {fact.name}
                          </span>
                        </td>
                        <td className='px-4 py-2'>
                          <div
                            className='text-xs text-gray-900 max-w-xs break-words'
                            title={fact.value}
                          >
                            {fact.value || (
                              <span className='text-gray-400'>Empty</span>
                            )}
                          </div>
                        </td>
                        <td className='px-4 py-2 whitespace-nowrap text-xs text-gray-500 break-all'>
                          {fact.contextRef || '-'}
                        </td>
                        <td className='px-4 py-2 whitespace-nowrap text-xs text-gray-500 break-all'>
                          {fact.unitRef || '-'}
                        </td>
                        <td className='px-4 py-2 whitespace-nowrap'>
                          <button
                            onClick={() => setSelectedTag(fact)}
                            className='text-blue-600 hover:text-blue-800 text-xs font-medium'
                          >
                            View Details
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {allFacts.length > 50 && (
                  <div className='px-4 py-3 bg-gray-50 text-center text-sm text-gray-600'>
                    Showing first 50 of {allFacts.length} facts
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Tag Details Modal - Reduced padding and made more compact */}
        {selectedTag && (
          <div className='fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50'>
            <div className='bg-white rounded-lg shadow-2xl max-w-2xl w-full max-h-[85vh] overflow-auto'>
              <div className='p-4 border-b bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-t-lg'>
                <div className='flex items-center justify-between'>
                  <h3 className='text-lg font-bold'>🏷️ Tag Details</h3>
                  <button
                    onClick={() => setSelectedTag(null)}
                    className='p-1.5 hover:bg-white/20 rounded-md transition-colors'
                  >
                    <X className='h-4 w-4' />
                  </button>
                </div>
              </div>
              <div className='p-4 space-y-3'>
                <div className='grid grid-cols-1 md:grid-cols-2 gap-3'>
                  <div>
                    <h4 className='font-semibold text-gray-700 mb-2 text-sm'>
                      Basic Information
                    </h4>
                    <div className='space-y-1 text-xs'>
                      <div>
                        <strong>Name:</strong>{' '}
                        <code className='bg-gray-100 px-1.5 py-0.5 rounded text-xs'>
                          {selectedTag.name}
                        </code>
                      </div>
                      <div>
                        <strong>Element:</strong> {selectedTag.element}
                      </div>
                      <div>
                        <strong>Value:</strong>{' '}
                        {selectedTag.value || (
                          <span className='text-gray-400'>Empty</span>
                        )}
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className='font-semibold text-gray-700 mb-2 text-sm'>
                      XBRL Attributes
                    </h4>
                    <div className='space-y-1 text-xs'>
                      {selectedTag.contextRef && (
                        <div>
                          <strong>Context:</strong> {selectedTag.contextRef}
                        </div>
                      )}
                      {selectedTag.unitRef && (
                        <div>
                          <strong>Unit:</strong> {selectedTag.unitRef}
                        </div>
                      )}
                      {selectedTag.decimals && (
                        <div>
                          <strong>Decimals:</strong> {selectedTag.decimals}
                        </div>
                      )}
                      {selectedTag.precision && (
                        <div>
                          <strong>Precision:</strong> {selectedTag.precision}
                        </div>
                      )}
                      {selectedTag.scale && (
                        <div>
                          <strong>Scale:</strong> {selectedTag.scale}
                        </div>
                      )}
                      {selectedTag.format && (
                        <div>
                          <strong>Format:</strong> {selectedTag.format}
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {selectedTag.position && (
                  <div>
                    <h4 className='font-semibold text-gray-700 mb-2 text-sm'>
                      Position Information
                    </h4>
                    <div className='bg-gray-50 rounded-md p-2 text-xs'>
                      <div>
                        <strong>Parent Element:</strong>{' '}
                        {selectedTag.position.parent}
                      </div>
                      <div>
                        <strong>Text Preview:</strong>{' '}
                        {selectedTag.position.text}
                      </div>
                      {selectedTag.xpath && (
                        <div>
                          <strong>XPath:</strong>{' '}
                          <code className='text-xs break-all'>
                            {selectedTag.xpath}
                          </code>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                <div>
                  <h4 className='font-semibold text-gray-700 mb-2 text-sm'>
                    All Attributes
                  </h4>
                  <div className='bg-gray-50 rounded-md p-2 max-h-32 overflow-y-auto'>
                    <div className='grid grid-cols-1 gap-1 text-xs'>
                      {Object.entries(selectedTag.attributes).map(
                        ([key, value]) => (
                          <div
                            key={key}
                            className='flex justify-between py-0.5 border-b border-gray-200 last:border-b-0'
                          >
                            <span className='font-medium text-gray-600'>
                              {key}:
                            </span>
                            <span className='text-gray-800 break-all ml-2'>
                              {value}
                            </span>
                          </div>
                        )
                      )}
                      {Object.keys(selectedTag.attributes).length === 0 && (
                        <p className='text-gray-500 italic'>
                          No additional attributes
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                <div className='flex gap-2 pt-3'>
                  <button
                    onClick={() => {
                      setViewMode('document');
                      handleTagClick(selectedTag.elementId);
                      setSelectedTag(null);
                    }}
                    className='flex-1 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-md text-sm font-medium transition-colors'
                  >
                    📄 View in Document
                  </button>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(
                        JSON.stringify(selectedTag, null, 2)
                      );
                    }}
                    className='px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md text-sm font-medium transition-colors'
                  >
                    📋 Copy JSON
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Debug Info - Reduced padding */}
        {parsedData && parsedData.facts.length === 0 && (
          <div className='bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg mb-4'>
            <p className='font-semibold'>⚠️ Debug Information:</p>
            <p>Document type: {parsedData.documentElement}</p>
            <p>Total elements: {parsedData.totalElements}</p>
            <p>
              Raw content preview: {parsedData.rawContent.substring(0, 200)}...
            </p>
            <p className='mt-2 text-sm'>
              No XBRL facts found. The file might not contain iXBRL data or use
              a different structure.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default IXBRLViewer;
