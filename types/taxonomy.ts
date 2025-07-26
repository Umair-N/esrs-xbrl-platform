export interface CalculationArc {
  from: string;
  to: string;
  weight: number;
  order?: string;
}

export interface TaxonomyNode {
  id: string;
  name?: string;
  label: string;
  labelType?: string;
  originalLabel?: string;
  type?: string;
  abstract?: string;
  order?: string;
  children?: TaxonomyNode[];
  substitutionGroup?: string;
  nillable?: string;
  periodType?: string;
  calculations?: CalculationArc[];
  [key: string]: any;
}

export interface TaxonomyData {
  id?: string;
  sectionCode?: string;
  labelCode?: string;
  label: string;
  labels?: string[];
  originalLabel?: string;
  roles?: string[];
  sourceFile?: string;
  children: TaxonomyNode[];
  [key: string]: any;
}
