import { useMutation } from '@tanstack/react-query';

// Types
export interface ValidationIssue {
  severity: 'error' | 'warning' | 'info';
  code: string;
  message: string;
  element?: string;
  suggestion?: string;
}

export interface ValidationResult {
  is_valid: boolean;
  error_count: number;
  warning_count: number;
  statistics: {
    context_count?: number;
    unit_count?: number;
    fact_count?: number;
    concepts_used?: string[];
  };
  issues: ValidationIssue[];
  summary: string;
}

export interface ComparisonDifference {
  concept: string;
  context: string;
  type: 'missing' | 'extra' | 'value_mismatch';
  expected_value?: string;
  actual_value?: string;
  message: string;
}

export interface ComparisonResult {
  is_match: boolean;
  match_percentage: number;
  total_facts_expected: number;
  total_facts_actual: number;
  matching_facts: number;
  statistics: {
    expected_concepts?: string[];
    actual_concepts?: string[];
    common_concepts?: string[];
    missing_count?: number;
    extra_count?: number;
    mismatch_count?: number;
    structure_match_percentage?: number;
  };
  differences: ComparisonDifference[];
  total_differences: number;
  // Structure-only comparison fields
  structure_only?: boolean;
  total_concepts_expected?: number;
  total_concepts_actual?: number;
  matching_concepts?: number;
  missing_concepts?: string[];
  extra_concepts?: string[];
  common_concepts?: string[];
}

export interface ConversionResult {
  success: boolean;
  message: string;
  xbrl_content?: string;
  report_data?: {
    company: {
      company_name: string;
      cin: string;
    };
  };
  statistics: Record<string, unknown>;
}

// Interactive Viewer Types
export interface TagInfo {
  t: string; // tag name
  v: string; // value
  c: string; // context
  p?: string; // period
  u?: string; // unit
  d?: string[]; // dimensions
  s?: string; // source
}

export interface InteractiveConversionResult {
  success: boolean;
  message: string;
  annotated_html: string;
  tag_mapping: Record<string, TagInfo[]>;
  xbrl_content?: string;
  statistics: {
    total_cells?: number;
    total_mappings?: number;
    [key: string]: unknown;
  };
}

export interface TagUpdate {
  cell_id: string;
  tag: string;
  old_value: string;
  new_value: string;
  new_tag?: string; // Optional: new tag name if user wants to change the tag
}

export interface TagUpdateResult {
  success: boolean;
  message: string;
  updated_xbrl: string;
  changes_applied: number;
}

// API URL helper
function getApiUrl(): string {
  const isLocal =
    typeof window !== 'undefined' &&
    (window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1');
  return isLocal
    ? 'http://localhost:8000/api/v1'
    : `${process.env.NEXT_PUBLIC_API_URL}`;
}

// API Functions
export async function validateXbrl(file: File): Promise<ValidationResult> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${getApiUrl()}/brsr/validate-xbrl`, {
    method: 'POST',
    body: formData,
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Validation failed');
  }

  return response.json();
}

export async function compareXbrl(
  expectedFile: File,
  actualFile: File,
  options?: { ignoreWhitespace?: boolean; ignoreDecimals?: boolean; structureOnly?: boolean }
): Promise<ComparisonResult> {
  const formData = new FormData();
  formData.append('expected_file', expectedFile);
  formData.append('actual_file', actualFile);
  formData.append('ignore_whitespace', String(options?.ignoreWhitespace ?? true));
  formData.append('ignore_decimals', String(options?.ignoreDecimals ?? false));
  formData.append('structure_only', String(options?.structureOnly ?? false));

  const response = await fetch(`${getApiUrl()}/brsr/compare`, {
    method: 'POST',
    body: formData,
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Comparison failed');
  }

  return response.json();
}

export async function convertHtmlToXbrl(
  file: File,
  options?: { startDate?: string; endDate?: string }
): Promise<ConversionResult> {
  const formData = new FormData();
  formData.append('file', file);
  if (options?.startDate) formData.append('start_date', options.startDate);
  if (options?.endDate) formData.append('end_date', options.endDate);
  formData.append('include_mapping', 'false');

  const response = await fetch(`${getApiUrl()}/brsr/convert/file`, {
    method: 'POST',
    body: formData,
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Conversion failed');
  }

  return response.json();
}

export async function downloadXbrl(
  file: File,
  options?: { startDate?: string; endDate?: string }
): Promise<Blob> {
  const formData = new FormData();
  formData.append('file', file);
  if (options?.startDate) formData.append('start_date', options.startDate);
  if (options?.endDate) formData.append('end_date', options.endDate);

  const response = await fetch(`${getApiUrl()}/brsr/convert/file/xml`, {
    method: 'POST',
    body: formData,
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Download failed');
  }

  return response.blob();
}

// React Query Hooks
export function useValidateXbrl() {
  return useMutation({
    mutationFn: validateXbrl,
  });
}

export function useCompareXbrl() {
  return useMutation({
    mutationFn: ({
      expectedFile,
      actualFile,
      options,
    }: {
      expectedFile: File;
      actualFile: File;
      options?: { ignoreWhitespace?: boolean; ignoreDecimals?: boolean; structureOnly?: boolean };
    }) => compareXbrl(expectedFile, actualFile, options),
  });
}

export function useConvertHtml() {
  return useMutation({
    mutationFn: ({
      file,
      options,
    }: {
      file: File;
      options?: { startDate?: string; endDate?: string };
    }) => convertHtmlToXbrl(file, options),
  });
}

export function useDownloadXbrl() {
  return useMutation({
    mutationFn: ({
      file,
      options,
    }: {
      file: File;
      options?: { startDate?: string; endDate?: string };
    }) => downloadXbrl(file, options),
  });
}

// Interactive Viewer API Functions
export async function convertHtmlInteractive(
  file: File,
  options?: { startDate?: string; endDate?: string }
): Promise<InteractiveConversionResult> {
  const formData = new FormData();
  formData.append('file', file);
  if (options?.startDate) formData.append('start_date', options.startDate);
  if (options?.endDate) formData.append('end_date', options.endDate);

  const response = await fetch(`${getApiUrl()}/brsr/convert/interactive`, {
    method: 'POST',
    body: formData,
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Interactive conversion failed');
  }

  return response.json();
}

export async function updateXbrlTags(
  originalXbrl: string,
  updates: TagUpdate[]
): Promise<TagUpdateResult> {
  const formData = new FormData();
  formData.append('original_xbrl', originalXbrl);
  formData.append('updates', JSON.stringify(updates));

  const response = await fetch(`${getApiUrl()}/brsr/update-tags`, {
    method: 'POST',
    body: formData,
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Tag update failed');
  }

  return response.json();
}

export async function downloadUpdatedXbrl(
  originalXbrl: string,
  updates: TagUpdate[],
  filename?: string
): Promise<Blob> {
  const formData = new FormData();
  formData.append('original_xbrl', originalXbrl);
  formData.append('updates', JSON.stringify(updates));
  if (filename) formData.append('filename', filename);

  const response = await fetch(`${getApiUrl()}/brsr/update-tags/download`, {
    method: 'POST',
    body: formData,
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Download failed');
  }

  return response.blob();
}

// Interactive Viewer Hooks
export function useConvertInteractive() {
  return useMutation({
    mutationFn: ({
      file,
      options,
    }: {
      file: File;
      options?: { startDate?: string; endDate?: string };
    }) => convertHtmlInteractive(file, options),
  });
}

export function useUpdateTags() {
  return useMutation({
    mutationFn: ({
      originalXbrl,
      updates,
    }: {
      originalXbrl: string;
      updates: TagUpdate[];
    }) => updateXbrlTags(originalXbrl, updates),
  });
}

export function useDownloadUpdatedXbrl() {
  return useMutation({
    mutationFn: ({
      originalXbrl,
      updates,
      filename,
    }: {
      originalXbrl: string;
      updates: TagUpdate[];
      filename?: string;
    }) => downloadUpdatedXbrl(originalXbrl, updates, filename),
  });
}
