// Report Document Types
export interface ReportDocument {
  id: string
  title: string
  createdAt: string
  updatedAt: string
  blocks: ReportBlock[]
}

export interface ReportBlock {
  id: string
  content: string
  type: "paragraph" | "heading" | "table" | "list"
  tags: XbrlTag[]
}

// XBRL Types
export interface XbrlTag {
  id: string
  concept: TaxonomyConcept
  context: XbrlContext
  createdAt: string
  // Add start and end indices for highlighting
  startIndex?: number
  endIndex?: number
}

export interface TaxonomyConcept {
  id: string
  label: string
  definition: string
  type: string
  dataType: string
  periodType: "instant" | "duration"
  balance?: "debit" | "credit"
  abstract: boolean
  labels?: {
    role: string
    value: string
  }[]
  references?: {
    name: string
    paragraph: string
    uri?: string
  }[]
}

export interface XbrlContext {
  id: string
  label: string
  entityName: string
  entityScheme: string
  entityIdentifier: string
  periodType: "instant" | "duration"
  instantDate?: Date
  startDate?: Date
  endDate?: Date
  createdAt: string
}
