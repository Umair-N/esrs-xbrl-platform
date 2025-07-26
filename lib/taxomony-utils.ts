// lib/taxonomy-utils.ts
export interface TaxonomyNode {
  id: string
  name?: string
  label: string
  labelType?: string
  originalLabel?: string
  type?: string
  abstract?: string
  order?: string
  children?: TaxonomyNode[]
  [key: string]: any
}

export function processTaxonomyData(rawData: any): TaxonomyNode[] {
  // Process your ESRS-Set1-XBRL-Taxonomy data here
  // Convert the parsed XML/JSON into the standardized format
  return rawData
}

export function searchTaxonomy(nodes: TaxonomyNode[], query: string): TaxonomyNode[] {
  const results: TaxonomyNode[] = []
  
  function traverse(node: TaxonomyNode) {
    if (
      node.label.toLowerCase().includes(query.toLowerCase()) ||
      node.id.toLowerCase().includes(query.toLowerCase())
    ) {
      results.push(node)
    }
    
    if (node.children) {
      node.children.forEach(traverse)
    }
  }
  
  nodes.forEach(traverse)
  return results
}
