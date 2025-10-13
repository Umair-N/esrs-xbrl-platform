// Report Document Types
export interface ReportDocument {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  /**
   * Optional file metadata. When a report is uploaded from a PDF or DOCX
   * file, the backend includes these fields so the frontend can
   * determine the file type and fetch page-level data. These are
   * undefined when a report is created from pasted text.
   */
  file_path?: string;
  file_size?: number;
  file_type?: string;
  blocks: ReportBlock[];

  /**
   * Optional array of saved page images and associated word data. When a
   * report is saved via the canvas API, the frontend serializes each
   * rendered PDF page into a data URL along with the word metadata.
   * Including this in the report allows the editor to rehydrate the
   * canvas instantly without re-fetching or re-rendering the original
   * PDF. This property is undefined for reports that have not been
   * persisted with a canvas snapshot.
   */
  pages?: SavedPage[];
}

/**
 * Represents a saved PDF page with its rendered image and word metadata.
 * The image property contains a data URL (e.g. data:image/png;base64,...)
 * which can be used directly in an <img> or canvas element.
 */
export interface SavedPage {
  pageNumber: number;
  width: number;
  height: number;
  image: string;
  imageUrl?: string;
  words: any[];
}

export interface ReportBlock {
  id: string;
  content: string;
  type: 'paragraph' | 'heading' | 'table' | 'list';
  tags: XbrlTag[];
}

export interface XbrlTag {
  id: string; // Unique ID for the tag (e.g., generated from `generateUniqueId`)
  concept: TaxonomyConcept; // The concept associated with this tag, containing details like `label`, `definition`, `type`
  context?: XbrlContext; // Optional: the context associated with this tag (e.g., period, entity)
  createdAt: string; // Date when the tag was created (ISO string)

  // Optional: indices of the highlighted text in the content
  startIndex?: number; // Start index of the highlighted text
  endIndex?: number; // End index of the highlighted text
  /**
   * Optional text that was explicitly selected by the user when creating
   * the tag. This is particularly important for PDF-derived blocks where
   * the underlying block content may be empty.
   */
  selectedText?: string;
  /**
   * Optional list of word indices captured when tagging PDF content. These
   * indices reference the word positions within the associated PDF page
   * (see ``ReportDocument.pages``) and allow consumers to rebuild the
   * tagged phrase even when character offsets are unavailable.
   */
  wordIndices?: number[];

  /**
   * Optional feedback ID returned from the AI recommender when a user
   * selects a recommended tag. Storing this ID allows the application
   * to delete the associated feedback when the tag is removed. Tags
   * created manually without using the recommendation service will have
   * this property undefined.
   */
  feedbackId?: number;
}

export interface TaxonomyConcept {
  id: string;
  label: string;
  definition: string;
  type: string;
  dataType: string;
  periodType: 'instant' | 'duration';
  balance?: 'debit' | 'credit';
  abstract: boolean;
  labels?: {
    role: string;
    value: string;
  }[];
  references?: {
    name: string;
    paragraph: string;
    uri?: string;
  }[];
}

export interface XbrlContext {
  id: string; // Unique identifier for the context
  label: string; // Display label for the context (e.g., "Acme Corp - 2025 Q1")
  entityName: string; // The name of the entity (e.g., "Acme Corporation")
  entityScheme: string; // The scheme for the entity identifier (e.g., "http://www.sec.gov/CIK")
  entityIdentifier: string; // The identifier for the entity (e.g., CIK or LEI)
  periodType: 'instant' | 'duration' | 'forever'; // Type of period ("instant" or "duration")

  // Optional fields based on the period type
  instantDate?: Date; // Relevant only if periodType is "instant"
  startDate?: Date; // Relevant only if periodType is "duration"
  endDate?: Date; // Relevant only if periodType is "duration"

  createdAt: string; // Timestamp of when the context was created (e.g., ISO format)
  updatedAt?: string; // Timestamp of when the context was last updated (optional)
}
