import esrsOutline from "./esrs_outline.json";
// Import calculations if you have them
// import esrsCalculations from './esrs_calculations.json'
import type {
  TaxonomyData,
  TaxonomyNode,
  CalculationArc,
} from "@/types/taxonomy";

/**
 * Merge calculation arcs into taxonomy nodes
 */
function mergeCalculationArcs(
  nodes: TaxonomyNode[],
  calculations: CalculationArc[] = []
) {
  nodes.forEach((node) => {
    // Find all calculation arcs where this node is the parent (from)
    node.calculations = calculations.filter((arc) => arc.from === node.id);

    // Recursively process children
    if (node.children && node.children.length > 0) {
      mergeCalculationArcs(node.children, calculations);
    }
  });
}

export function getTaxonomyData(): TaxonomyData {
  const rawData = esrsOutline as any;

  // Handle different possible structures
  let data: TaxonomyData;
  if (rawData.children) {
    data = rawData;
  } else if (Array.isArray(rawData)) {
    data = { children: rawData, label: "ESRS Taxonomy", id: "root" };
  } else if (rawData.data?.children) {
    data = rawData.data;
  } else {
    // If it's just an object with properties, treat as single root
    data = { children: [rawData], label: "ESRS Taxonomy", id: "root" };
  }

  // Merge calculations if available
  // Uncomment this if you have a calculations file:
  // if (Array.isArray(data.children)) {
  //   mergeCalculationArcs(data.children, esrsCalculations as CalculationArc[])
  // }

  return data;
}

export function searchTaxonomy(
  nodes: TaxonomyNode[],
  query: string
): TaxonomyNode[] {
  if (!nodes || !Array.isArray(nodes)) return [];

  const results: TaxonomyNode[] = [];

  function traverse(node: TaxonomyNode) {
    if (
      node.label?.toLowerCase().includes(query.toLowerCase()) ||
      node.id?.toLowerCase().includes(query.toLowerCase()) ||
      (node.name && node.name.toLowerCase().includes(query.toLowerCase())) ||
      (node.originalLabel &&
        node.originalLabel.toLowerCase().includes(query.toLowerCase()))
    ) {
      results.push(node);
    }

    if (
      node.children &&
      Array.isArray(node.children) &&
      node.children.length > 0
    ) {
      node.children.forEach(traverse);
    }
  }

  nodes.forEach(traverse);
  return results;
}

export function flattenTree(nodes: TaxonomyNode[]): TaxonomyNode[] {
  if (!nodes || !Array.isArray(nodes)) {
    console.warn("flattenTree received invalid nodes:", nodes);
    return [];
  }

  const result: TaxonomyNode[] = [];

  function traverse(node: TaxonomyNode) {
    if (!node) return;

    result.push(node);
    if (
      node.children &&
      Array.isArray(node.children) &&
      node.children.length > 0
    ) {
      node.children.forEach(traverse);
    }
  }

  nodes.forEach(traverse);
  return result;
}

export function findNodeById(
  nodes: TaxonomyNode[],
  id: string
): TaxonomyNode | null {
  if (!nodes || !Array.isArray(nodes)) return null;

  for (const node of nodes) {
    if (node?.id === id) return node;
    if (node?.children && Array.isArray(node.children)) {
      const found = findNodeById(node.children, id);
      if (found) return found;
    }
  }
  return null;
}

export function getNodePath(
  nodes: TaxonomyNode[],
  targetId: string,
  path: string[] = []
): string[] | null {
  if (!nodes || !Array.isArray(nodes)) return null;

  for (const node of nodes) {
    if (!node) continue;

    const currentPath = [...path, node.label || node.id || "Unknown"];
    if (node.id === targetId) {
      return currentPath;
    }
    if (node.children && Array.isArray(node.children)) {
      const found = getNodePath(node.children, targetId, currentPath);
      if (found) return found;
    }
  }
  return null;
}

export function getCalculationChildren(
  node: TaxonomyNode,
  allNodes: TaxonomyNode[]
): TaxonomyNode[] {
  if (!node.calculations || node.calculations.length === 0) return [];

  return node.calculations
    .map((calc) => findNodeById(allNodes, calc.to))
    .filter((child): child is TaxonomyNode => child !== null)
    .sort((a, b) => {
      const aOrder =
        node.calculations?.find((c) => c.to === a.id)?.order || "0";
      const bOrder =
        node.calculations?.find((c) => c.to === b.id)?.order || "0";
      return parseFloat(aOrder) - parseFloat(bOrder);
    });
}
