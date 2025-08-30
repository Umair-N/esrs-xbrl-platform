// @ts-nocheck
import type { ReportDocument, XbrlTag } from '@/types/report';

interface XBRLNamespace {
  prefix: string;
  uri: string;
  description?: string;
  entryPoint?: string;
}

interface TaxonomyConfig {
  namespaces: XBRLNamespace[];
  schemaRefs: string[];
  conceptValidation: (conceptId: string) => boolean;
  unitMapping: (conceptId: string, dataType: string) => string | null;
  contextRules: (concept: any) => any;
}

// Enhanced taxonomy configurations
const TAXONOMY_CONFIGS = {
  esrs: {
    namespaces: [
      {
        prefix: 'esrs',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22',
      },
      {
        prefix: 'esrs_e1',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e1',
      },
      {
        prefix: 'esrs_e2',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e2',
      },
      {
        prefix: 'esrs_e3',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e3',
      },
      {
        prefix: 'esrs_e4',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e4',
      },
      {
        prefix: 'esrs_e5',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e5',
      },
      {
        prefix: 'esrs_s1',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_s1',
      },
      {
        prefix: 'esrs_s2',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_s2',
      },
      {
        prefix: 'esrs_s3',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_s3',
      },
      {
        prefix: 'esrs_s4',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_s4',
      },
      {
        prefix: 'esrs_g1',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_g1',
      },
      {
        prefix: 'esrs_g2',
        uri: 'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_g2',
      },
    ],
    schemaRefs: [
      'https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_all.xsd',
    ],
    conceptValidation: (conceptId: string) => {
      return /^esrs(_[esg]\d)?:[A-Za-z][\w]*$/.test(conceptId);
    },
    unitMapping: (conceptId: string, dataType: string) => {
      if (conceptId.includes('GHG') || conceptId.includes('Emission'))
        return 'tCO2e';
      if (conceptId.includes('Energy')) return 'MWh';
      if (conceptId.includes('Water')) return 'm3';
      if (conceptId.includes('Waste')) return 'tonnes';
      if (conceptId.includes('Revenue') || conceptId.includes('Investment'))
        return 'U-EUR';
      if (conceptId.includes('Percentage') || conceptId.includes('Ratio'))
        return 'pure';
      return dataType === 'monetary' ? 'U-EUR' : 'pure';
    },
  },
  gri: {
    namespaces: [
      {
        prefix: 'gri',
        uri: 'https://taxonomy.globalreporting.org/gri-sustainability-taxonomy/gri_srs/core',
      },
      {
        prefix: 'gri_part',
        uri: 'https://taxonomy.globalreporting.org/gri-sustainability-taxonomy/gri_srs/part',
      },
      {
        prefix: 'gri_201',
        uri: 'https://taxonomy.globalreporting.org/gri-sustainability-taxonomy/gri_srs/gri_201',
      },
      {
        prefix: 'gri_301',
        uri: 'https://taxonomy.globalreporting.org/gri-sustainability-taxonomy/gri_srs/gri_301',
      },
      {
        prefix: 'gri_302',
        uri: 'https://taxonomy.globalreporting.org/gri-sustainability-taxonomy/gri_srs/gri_302',
      },
      {
        prefix: 'gri_305',
        uri: 'https://taxonomy.globalreporting.org/gri-sustainability-taxonomy/gri_srs/gri_305',
      },
    ],
    schemaRefs: [
      'https://taxonomy.globalreporting.org/gri-sustainability-taxonomy/gri_srs/gri_srs_entry_point_2023-12-07.xsd',
    ],
    conceptValidation: (conceptId: string) => {
      return /^gri(_\d{3})?:[A-Za-z][\w-]*$/.test(conceptId);
    },
    unitMapping: (conceptId: string, dataType: string) => {
      if (conceptId.includes('305')) return 'tCO2e'; // GHG emissions
      if (conceptId.includes('302')) return 'MWh'; // Energy
      if (conceptId.includes('303')) return 'm3'; // Water
      if (conceptId.includes('201')) return 'U-EUR'; // Economic
      return 'pure';
    },
  },
  sasb: {
    namespaces: [
      {
        prefix: 'sasb',
        uri: 'http://www.sasb.org/xbrl/taxonomy/cor/2024-11-07',
      },
      {
        prefix: 'sasb-dei',
        uri: 'http://www.sasb.org/xbrl/taxonomy/dei/2024-11-07',
      },
      {
        prefix: 'sasb-all',
        uri: 'https://xbrl.ifrs.org/taxonomy/sasb/2024-11-07',
      },
    ],
    schemaRefs: [
      'https://xbrl.ifrs.org/taxonomy/sasb/2024-11-07/sasb-entryPoint-all-2024-11-07.xsd',
    ],
    conceptValidation: (conceptId: string) => {
      return /^sasb(-dei)?:[A-Za-z][\w]*$/.test(conceptId);
    },
    unitMapping: (conceptId: string, dataType: string) => {
      if (conceptId.includes('GHG') || conceptId.includes('CO2'))
        return 'tCO2e';
      if (conceptId.includes('Energy')) return 'MWh';
      if (conceptId.includes('Water')) return 'm3';
      if (conceptId.includes('Revenue') || conceptId.includes('Cost'))
        return 'U-USD';
      return dataType === 'monetary' ? 'U-USD' : 'pure';
    },
  },
};

const CORE_NAMESPACES: XBRLNamespace[] = [
  { prefix: 'xbrli', uri: 'http://www.xbrl.org/2003/instance' },
  { prefix: 'link', uri: 'http://www.xbrl.org/2003/linkbase' },
  { prefix: 'xlink', uri: 'http://www.w3.org/1999/xlink' },
  { prefix: 'ix', uri: 'http://www.xbrl.org/2013/inlineXBRL' },
  {
    prefix: 'ixt',
    uri: 'http://www.xbrl.org/inlineXBRL/transformation/2020-02-12',
  },
  { prefix: 'iso4217', uri: 'http://www.xbrl.org/2003/iso4217' },
  { prefix: 'xbrldt', uri: 'http://xbrl.org/2005/xbrldt' },
  { prefix: 'xsi', uri: 'http://www.w3.org/2001/XMLSchema-instance' },
];

export function generateiXBRLDocument(
  report: ReportDocument,
  taxonomies: string[] = ['esrs', 'gri', 'sasb']
): string {
  const enabledTaxonomies = taxonomies.filter(
    (t) => TAXONOMY_CONFIGS[t as keyof typeof TAXONOMY_CONFIGS]
  );
  const allNamespaces = getAllNamespaces(enabledTaxonomies);
  const allSchemaRefs = getAllSchemaRefs(enabledTaxonomies);

  const namespaces = allNamespaces
    .map((ns) => `      xmlns:${ns.prefix}="${ns.uri}"`)
    .join('\n');

  const contexts = getUniqueContexts(report);
  const units = getUniqueUnits(report, enabledTaxonomies);

  const ixbrl = `<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"
${namespaces}>
<head>
  <title>${escapeHTML(report.title)}</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <style type="text/css">
    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
    h1, h2, h3 { color: #2c5282; }
    
    /* Enhanced iXBRL element styling */
    ix\\:nonNumeric, ix\\:nonFraction {
      background-color: #e6f3ff;
      padding: 2px 4px;
      border-radius: 3px;
      display: inline;
      border: 1px solid #b3d9ff;
      margin: 0 1px;
      position: relative;
    }
    
    /* Taxonomy-specific styling */
    ix\\:nonFraction[name^="esrs:"], ix\\:nonNumeric[name^="esrs:"] {
      border-left: 3px solid #28a745;
      background-color: #d4edda;
    }
    
    ix\\:nonFraction[name^="gri:"], ix\\:nonNumeric[name^="gri:"] {
      border-left: 3px solid #007bff;
      background-color: #d1ecf1;
    }
    
    ix\\:nonFraction[name^="sasb:"], ix\\:nonNumeric[name^="sasb:"] {
      border-left: 3px solid #ffc107;
      background-color: #fff3cd;
    }
    
    /* Unit-specific styling */
    ix\\:nonFraction[unitRef="U-EUR"], ix\\:nonFraction[unitRef="U-USD"] {
      font-weight: bold;
      color: #2d5016;
    }
    
    ix\\:nonFraction[unitRef="tCO2e"] {
      color: #721c24;
      background-color: #f8d7da;
    }
    
    ix\\:nonFraction[unitRef="pure"] {
      color: #744210;
    }
    
    .section { 
      margin-bottom: 30px; 
      border: 1px solid #e9ecef;
      border-radius: 8px;
      padding: 20px;
    }
    
    .content-block { 
      margin-bottom: 15px; 
      padding: 10px;
      background-color: #f8f9fa;
      border-left: 4px solid #007bff;
      border-radius: 4px;
    }
    
    /* Interactive features */
    ix\\:nonNumeric:hover, ix\\:nonFraction:hover {
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
      transform: translateY(-2px);
      transition: all 0.3s ease;
      cursor: pointer;
      z-index: 10;
    }
    
    /* Tooltip simulation */
    ix\\:nonNumeric::after, ix\\:nonFraction::after {
      content: attr(name);
      position: absolute;
      bottom: 100%;
      left: 50%;
      transform: translateX(-50%);
      background: #333;
      color: white;
      padding: 5px 8px;
      border-radius: 4px;
      font-size: 10px;
      white-space: nowrap;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s;
      z-index: 1000;
    }
    
    ix\\:nonNumeric:hover::after, ix\\:nonFraction:hover::after {
      opacity: 1;
    }
    
    .taxonomy-legend {
      display: flex;
      gap: 20px;
      margin-bottom: 20px;
      padding: 10px;
      background: #f8f9fa;
      border-radius: 8px;
    }
    
    .taxonomy-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
    }
    
    .taxonomy-color {
      width: 20px;
      height: 3px;
      border-radius: 2px;
    }
  </style>
</head>
<body>
  <ix:header>
    <ix:references>
${allSchemaRefs.map((ref) => `      <link:schemaRef xlink:type="simple" xlink:href="${ref}"/>`).join('\n')}
    </ix:references>
    <ix:resources>
${generateContextsXML(contexts)}
${generateUnitsXML(units)}
    </ix:resources>
  </ix:header>

  <h1>Sustainability Disclosures</h1>
  <div class="taxonomy-legend">
    ${enabledTaxonomies.includes('esrs') ? '<div class="taxonomy-item"><div class="taxonomy-color" style="background-color: #28a745;"></div>ESRS</div>' : ''}
    ${enabledTaxonomies.includes('gri') ? '<div class="taxonomy-item"><div class="taxonomy-color" style="background-color: #007bff;"></div>GRI</div>' : ''}
    ${enabledTaxonomies.includes('sasb') ? '<div class="taxonomy-item"><div class="taxonomy-color" style="background-color: #ffc107;"></div>SASB</div>' : ''}
  </div>
  <p><em>Generated on: ${new Date().toLocaleDateString()} | Taxonomies: ${enabledTaxonomies.join(', ').toUpperCase()}</em></p>

${generateReportContent(report, enabledTaxonomies)}

</body>
</html>`;

  return ixbrl;
}

function getAllNamespaces(enabledTaxonomies: string[]): XBRLNamespace[] {
  const namespaces = [...CORE_NAMESPACES];

  enabledTaxonomies.forEach((taxonomy) => {
    const config = TAXONOMY_CONFIGS[taxonomy as keyof typeof TAXONOMY_CONFIGS];
    if (config) {
      namespaces.push(...config.namespaces);
    }
  });

  return namespaces;
}

function getAllSchemaRefs(enabledTaxonomies: string[]): string[] {
  const schemaRefs: string[] = [];

  enabledTaxonomies.forEach((taxonomy) => {
    const config = TAXONOMY_CONFIGS[taxonomy as keyof typeof TAXONOMY_CONFIGS];
    if (config) {
      schemaRefs.push(...config.schemaRefs);
    }
  });

  return schemaRefs;
}

function getUniqueContexts(report: ReportDocument) {
  const contextMap = new Map<string | undefined, any>();

  // Create default context with proper entity identifier
  if (report.blocks.every((block) => block.tags.every((tag) => !tag.context))) {
    contextMap.set('default', {
      id: 'default',
      entity: '0000000000',
      entityScheme: 'http://www.sec.gov/CIK',
      periodType: 'duration',
      startDate: '2023-01-01',
      endDate: '2023-12-31',
    });
  }

  report.blocks.forEach((block) => {
    block.tags.forEach((tag) => {
      const ctxId = tag?.context?.id || 'default';
      if (!contextMap.has(ctxId)) {
        contextMap.set(
          ctxId,
          tag.context || {
            id: 'default',
            entity: '0000000000',
            entityScheme: 'http://www.sec.gov/CIK',
            periodType: 'duration',
            startDate: '2023-01-01',
            endDate: '2023-12-31',
          }
        );
      }
    });
  });
  return Array.from(contextMap.values());
}

function getUniqueUnits(report: ReportDocument, enabledTaxonomies: string[]) {
  const unitMap = new Map<string, { id: string; measure: string }>();

  // Standard units
  unitMap.set('U-EUR', { id: 'U-EUR', measure: 'iso4217:EUR' });
  unitMap.set('U-USD', { id: 'U-USD', measure: 'iso4217:USD' });
  unitMap.set('pure', { id: 'pure', measure: 'xbrli:pure' });

  // Sustainability-specific units
  unitMap.set('tCO2e', { id: 'tCO2e', measure: 'xbrli:pure' });
  unitMap.set('MWh', { id: 'MWh', measure: 'xbrli:pure' });
  unitMap.set('m3', { id: 'm3', measure: 'xbrli:pure' });
  unitMap.set('tonnes', { id: 'tonnes', measure: 'xbrli:pure' });
  unitMap.set('GJ', { id: 'GJ', measure: 'xbrli:pure' });
  unitMap.set('kWh', { id: 'kWh', measure: 'xbrli:pure' });
  unitMap.set('liters', { id: 'liters', measure: 'xbrli:pure' });

  return Array.from(unitMap.values());
}

function generateContextsXML(contexts: any[]): string {
  return contexts
    .map((context) => {
      const formatDate = (dateInput: any) => {
        if (!dateInput) return '2023-12-31';
        if (typeof dateInput === 'string') {
          if (/^\d{4}-\d{2}-\d{2}$/.test(dateInput)) {
            return dateInput;
          }
          const date = new Date(dateInput);
          if (!isNaN(date.getTime())) {
            return date.toISOString().split('T')[0];
          }
        } else if (dateInput instanceof Date) {
          return dateInput.toISOString().split('T')[0];
        }
        return '2023-12-31';
      };

      const entityScheme = context?.entityScheme || 'http://www.sec.gov/CIK';
      const entityId = context?.entity || '0000000000';

      return `      <xbrli:context id="${context?.id || 'default'}">
        <xbrli:entity>
          <xbrli:identifier scheme="${entityScheme}">${entityId}</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
          ${
            context?.periodType === 'instant'
              ? `<xbrli:instant>${formatDate(
                  context?.period || context?.instantDate
                )}</xbrli:instant>`
              : `<xbrli:startDate>${formatDate(
                  context?.startDate || '2023-01-01'
                )}</xbrli:startDate>
          <xbrli:endDate>${formatDate(context?.endDate || '2023-12-31')}</xbrli:endDate>`
          }
        </xbrli:period>
      </xbrli:context>`;
    })
    .join('\n');
}

function generateUnitsXML(units: any[]): string {
  return units
    .map(
      (unit) => `      <xbrli:unit id="${unit.id}">
        <xbrli:measure>${unit.measure}</xbrli:measure>
      </xbrli:unit>`
    )
    .join('\n');
}

function generateReportContent(
  report: ReportDocument,
  enabledTaxonomies: string[]
): string {
  const sections = groupBlocksBySection(report.blocks);
  let content = '';
  sections.forEach((section) => {
    content += `  <div class="section">\n`;
    if (section.title) {
      content += `    <h2>${escapeHTML(section.title)}</h2>\n`;
    }
    section.blocks.forEach((block) => {
      content += generateBlockContentWithTaxonomyAwareness(
        block,
        enabledTaxonomies
      );
    });
    content += `  </div>\n\n`;
  });
  return content;
}

function groupBlocksBySection(blocks: any[]) {
  const sections: any[] = [];
  let currentSection = { title: null as string | null, blocks: [] as any[] };
  blocks.forEach((block) => {
    if (block.tags.length > 0) {
      const tagTypes = block.tags.map((tag: XbrlTag) =>
        getTagCategory(tag.concept.id)
      );
      const uniqueTypes = [...new Set(tagTypes)];
      if (uniqueTypes.length > 0 && uniqueTypes[0] !== currentSection.title) {
        if (currentSection.blocks.length > 0) {
          sections.push(currentSection);
        }
        currentSection = {
          title: getSectionTitle(uniqueTypes[0]),
          blocks: [block],
        };
      } else {
        currentSection.blocks.push(block);
      }
    } else {
      currentSection.blocks.push(block);
    }
  });
  if (currentSection.blocks.length > 0) {
    sections.push(currentSection);
  }
  return sections;
}

function getTagCategory(conceptId: string): string {
  const id = conceptId.toLowerCase();
  if (id.includes('governance') || id.includes('g1') || id.includes('g2'))
    return 'governance';
  if (
    id.includes('ghg') ||
    id.includes('emission') ||
    id.includes('climate') ||
    id.includes('e1')
  )
    return 'climate';
  if (id.includes('pollution') || id.includes('e2')) return 'pollution';
  if (id.includes('water') || id.includes('e3')) return 'water';
  if (id.includes('biodiversity') || id.includes('e4')) return 'biodiversity';
  if (id.includes('circular') || id.includes('e5')) return 'circular';
  if (id.includes('workforce') || id.includes('s1')) return 'social';
  if (id.includes('risk') || id.includes('assessment')) return 'risk';
  if (id.includes('revenue') || id.includes('financial') || id.includes('201'))
    return 'financial';
  return 'general';
}

function getSectionTitle(category: string): string {
  const titles: Record<string, string> = {
    governance: 'Governance and Risk Management',
    climate: 'Climate Change',
    pollution: 'Pollution and Circular Economy',
    water: 'Water and Marine Resources',
    biodiversity: 'Biodiversity and Ecosystems',
    circular: 'Resource Use and Circular Economy',
    social: 'Social and Workforce Disclosures',
    risk: 'Risk Assessment',
    financial: 'Financial Information',
    general: 'General Disclosures',
  };
  return titles[category] || 'Sustainability Disclosures';
}

function generateBlockContentWithTaxonomyAwareness(
  block: any,
  enabledTaxonomies: string[]
): string {
  if (block.tags.length === 0) {
    return `    <div class="content-block">${escapeHTML(
      block.content
    )}</div>\n`;
  }
  const sortedTags = [...block.tags].sort(
    (a, b) => (a.startIndex || 0) - (b.startIndex || 0)
  );
  const content = block.content;
  let processedContent = '';
  let lastIndex = 0;
  sortedTags.forEach((tag: XbrlTag, index: number) => {
    const startIndex = tag.startIndex || 0;
    const endIndex = tag.endIndex || startIndex;
    if (startIndex !== endIndex && startIndex < content.length) {
      processedContent += escapeHTML(content.substring(lastIndex, startIndex));
      const taggedText = content.substring(startIndex, endIndex);
      const ixbrlTag = generateEnhancediXBRLTag(
        tag,
        taggedText,
        enabledTaxonomies
      );
      processedContent += ixbrlTag;
      lastIndex = endIndex;
    }
  });
  processedContent += escapeHTML(content.substring(lastIndex));
  processedContent = processedContent.replace(/\n/g, '<br/>');
  return `    <div class="content-block">${processedContent}</div>\n\n`;
}

function generateEnhancediXBRLTag(
  tag: any,
  value: string,
  enabledTaxonomies: string[]
): string {
  const concept = tag.concept;
  const isNumeric = isNumericConcept(concept);
  const conceptName = parseConceptNameWithTaxonomy(
    concept.id,
    enabledTaxonomies
  );
  const contextRef = tag.context?.id || 'default';

  // Enhanced validation with taxonomy-specific rules
  if (!isValidConceptForTaxonomies(conceptName, enabledTaxonomies)) {
    console.warn(`Invalid concept: ${conceptName}, using fallback`);
    return escapeHTML(value);
  }

  if (isNumeric) {
    const cleanValue = cleanFactValue(value, concept.dataType);
    const unitRef = determineUnitRefWithTaxonomy(
      conceptName,
      concept.dataType,
      enabledTaxonomies
    );
    const attributes = [
      `name="${conceptName}"`,
      `contextRef="${contextRef}"`,
      unitRef ? `unitRef="${unitRef}"` : null,
      `decimals="${getDecimals(concept)}"`,
      `format="ixt:fixed-zero"`,
    ]
      .filter(Boolean)
      .join(' ');
    return `<ix:nonFraction ${attributes}>${cleanValue}</ix:nonFraction>`;
  } else {
    const attributes = [`name="${conceptName}"`, `contextRef="${contextRef}"`]
      .filter(Boolean)
      .join(' ');
    return `<ix:nonNumeric ${attributes}>${escapeHTML(value)}</ix:nonNumeric>`;
  }
}

function parseConceptNameWithTaxonomy(
  conceptId: string,
  enabledTaxonomies: string[]
): string {
  if (conceptId.includes(':')) {
    return conceptId;
  }

  // Enhanced parsing with taxonomy-specific logic
  for (const taxonomy of enabledTaxonomies) {
    const config = TAXONOMY_CONFIGS[taxonomy as keyof typeof TAXONOMY_CONFIGS];
    if (config) {
      const namespaces = config.namespaces.map((ns) => ns.prefix);

      for (const prefix of namespaces) {
        const prefixUnderscore = `${prefix}_`;
        if (conceptId.startsWith(prefixUnderscore)) {
          const local = conceptId
            .substring(prefixUnderscore.length)
            .replace(/_([a-z])/g, (match, letter) => letter.toUpperCase());
          return `${prefix.replace(/_/g, '-')}:${local}`;
        }
      }
    }
  }

  // Fallback logic
  const underscoreIndex = conceptId.indexOf('_');
  if (underscoreIndex > 0) {
    const ns = conceptId.substring(0, underscoreIndex).replace(/_/g, '-');
    const local = conceptId
      .substring(underscoreIndex + 1)
      .replace(/_([a-z])/g, (match, letter) => letter.toUpperCase());
    return `${ns}:${local}`;
  }

  // Default to first enabled taxonomy
  const defaultTaxonomy = enabledTaxonomies[0] || 'esrs';
  return `${defaultTaxonomy}:${conceptId.replace(/_([a-z])/g, (match, letter) => letter.toUpperCase())}`;
}

function isValidConceptForTaxonomies(
  conceptName: string,
  enabledTaxonomies: string[]
): boolean {
  for (const taxonomy of enabledTaxonomies) {
    const config = TAXONOMY_CONFIGS[taxonomy as keyof typeof TAXONOMY_CONFIGS];
    if (config && config.conceptValidation(conceptName)) {
      return true;
    }
  }
  return conceptName.includes(':');
}

function determineUnitRefWithTaxonomy(
  conceptName: string,
  dataType: string,
  enabledTaxonomies: string[]
): string | null {
  for (const taxonomy of enabledTaxonomies) {
    const config = TAXONOMY_CONFIGS[taxonomy as keyof typeof TAXONOMY_CONFIGS];
    if (config) {
      const unit = config.unitMapping(conceptName, dataType);
      if (unit) return unit;
    }
  }

  // Fallback unit determination
  if (dataType?.toLowerCase() === 'monetary') {
    return 'U-EUR';
  }
  if (conceptName.includes('Percentage') || conceptName.includes('Ratio')) {
    return 'pure';
  }
  return 'pure';
}

function isNumericConcept(concept: any): boolean {
  const numericTypes = [
    'monetary',
    'decimal',
    'integer',
    'shares',
    'percentage',
    'nonNegativeInteger',
    'positiveInteger',
    'float',
    'double',
  ];
  return numericTypes.includes(concept?.dataType?.toLowerCase());
}

function getDecimals(concept: any): string {
  const dataType = concept?.dataType?.toLowerCase();
  switch (dataType) {
    case 'monetary':
      return '0';
    case 'percentage':
      return '2';
    case 'decimal':
    case 'float':
    case 'double':
      return '2';
    case 'integer':
    case 'nonNegativeInteger':
    case 'positiveInteger':
      return '0';
    default:
      return '2';
  }
}

function cleanFactValue(text: string, dataType: string): string {
  if (!text) return '';

  switch (dataType?.toLowerCase()) {
    case 'monetary': {
      // Enhanced monetary value extraction
      const match = text.match(/-?[\d,]+\.?\d*/);
      return match ? match[0].replace(/,/g, '') : '0';
    }
    case 'integer':
    case 'nonNegativeInteger':
    case 'positiveInteger': {
      const match = text.match(/-?\d+/);
      return match ? match[0] : '0';
    }
    case 'decimal':
    case 'percentage':
    case 'float':
    case 'double': {
      const match = text.match(/-?\d+\.?\d*/);
      return match ? match[0] : '0';
    }
    case 'boolean': {
      const lower = text.toLowerCase().trim();
      if (
        lower.includes('true') ||
        lower.includes('yes') ||
        lower.includes('1')
      )
        return 'true';
      if (
        lower.includes('false') ||
        lower.includes('no') ||
        lower.includes('0')
      )
        return 'false';
      return 'true';
    }
    case 'date': {
      // Enhanced date handling
      const dateMatch = text.match(/\d{4}-\d{2}-\d{2}/);
      if (dateMatch) return dateMatch[0];
      try {
        const date = new Date(text);
        if (!isNaN(date.getTime())) {
          return date.toISOString().split('T')[0];
        }
      } catch (e) {
        // Ignore parsing errors
      }
      return '2023-12-31';
    }
    default: {
      return text.replace(/\s+/g, ' ').trim().substring(0, 500);
    }
  }
}

function escapeHTML(text: string): string {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Enhanced validation functions
function validateiXBRLDocument(ixbrlContent: string): {
  isValid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  // Basic structure validation
  if (!ixbrlContent.includes('<html xmlns="http://www.w3.org/1999/xhtml"')) {
    errors.push('Missing HTML namespace declaration');
  }

  if (
    !ixbrlContent.includes('<ix:header>') ||
    !ixbrlContent.includes('</ix:header>')
  ) {
    errors.push('Missing or malformed ix:header');
  }

  if (
    !ixbrlContent.includes('<ix:resources>') ||
    !ixbrlContent.includes('</ix:resources>')
  ) {
    errors.push('Missing or malformed ix:resources');
  }

  if (
    !ixbrlContent.includes('<ix:references>') ||
    !ixbrlContent.includes('</ix:references>')
  ) {
    errors.push('Missing or malformed ix:references');
  }

  // Check for at least one context
  if (!ixbrlContent.includes('<xbrli:context')) {
    errors.push('No contexts defined');
  }

  // Check for at least one unit
  if (!ixbrlContent.includes('<xbrli:unit')) {
    errors.push('No units defined');
  }

  // Validate XML structure
  try {
    // Basic XML validation (check for balanced tags)
    const openTags = (ixbrlContent.match(/<[^\/][^>]*>/g) || []).length;
    const closeTags = (ixbrlContent.match(/<\/[^>]*>/g) || []).length;
    const selfClosingTags = (ixbrlContent.match(/<[^>]*\/>/g) || []).length;

    if (openTags !== closeTags + selfClosingTags) {
      errors.push('Unbalanced XML tags detected');
    }
  } catch (e) {
    errors.push('XML structure validation failed');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

// Taxonomy-specific optimization functions
function optimizeForESRS(report: ReportDocument): ReportDocument {
  // Add ESRS-specific optimizations
  const optimizedBlocks = report.blocks.map((block) => ({
    ...block,
    tags: block.tags.map((tag) => ({
      ...tag,
      concept: {
        ...tag.concept,
        // Ensure ESRS concepts follow proper naming conventions
        id: tag.concept.id.replace(/([A-Z])/g, (match, letter, index) =>
          index === 0 ? letter : letter.toLowerCase()
        ),
      },
    })),
  }));

  return {
    ...report,
    blocks: optimizedBlocks,
  };
}

function optimizeForGRI(report: ReportDocument): ReportDocument {
  // Add GRI-specific optimizations
  const optimizedBlocks = report.blocks.map((block) => ({
    ...block,
    tags: block.tags.map((tag) => {
      // Map GRI disclosure numbers to proper concept names
      let conceptId = tag.concept.id;
      if (conceptId.match(/^\d{3}-\d+/)) {
        const parts = conceptId.split('-');
        conceptId = `gri_${parts[0]}:Disclosure${parts[0]}${parts[1]}`;
      }

      return {
        ...tag,
        concept: {
          ...tag.concept,
          id: conceptId,
        },
      };
    }),
  }));

  return {
    ...report,
    blocks: optimizedBlocks,
  };
}

function optimizeForSASB(report: ReportDocument): ReportDocument {
  // Add SASB-specific optimizations
  const optimizedBlocks = report.blocks.map((block) => ({
    ...block,
    tags: block.tags.map((tag) => ({
      ...tag,
      concept: {
        ...tag.concept,
        // Ensure SASB concepts include proper industry codes
        id: tag.concept.id.includes('sasb:')
          ? tag.concept.id
          : `sasb:${tag.concept.id}`,
      },
    })),
  }));

  return {
    ...report,
    blocks: optimizedBlocks,
  };
}

export function generateOptimizediXBRLDocument(
  report: ReportDocument,
  taxonomies: string[] = ['esrs', 'gri', 'sasb'],
  options: {
    validate?: boolean;
    optimize?: boolean;
    includeMetadata?: boolean;
  } = {}
): {
  content: string;
  validation?: { isValid: boolean; errors: string[] };
  metadata?: any;
} {
  let optimizedReport = report;

  // Apply taxonomy-specific optimizations
  if (options.optimize) {
    if (taxonomies.includes('esrs')) {
      optimizedReport = optimizeForESRS(optimizedReport);
    }
    if (taxonomies.includes('gri')) {
      optimizedReport = optimizeForGRI(optimizedReport);
    }
    if (taxonomies.includes('sasb')) {
      optimizedReport = optimizeForSASB(optimizedReport);
    }
  }

  const ixbrlContent = generateiXBRLDocument(optimizedReport, taxonomies);

  const result: any = { content: ixbrlContent };

  // Add validation if requested
  if (options.validate) {
    result.validation = validateiXBRLDocument(ixbrlContent);
  }

  // Add metadata if requested
  if (options.includeMetadata) {
    result.metadata = {
      generatedAt: new Date().toISOString(),
      taxonomies: taxonomies,
      totalBlocks: report.blocks.length,
      totalTags: report.blocks.reduce(
        (sum, block) => sum + block.tags.length,
        0
      ),
      documentSize: ixbrlContent.length,
      validationStatus: options.validate
        ? result.validation?.isValid
        : 'not_validated',
    };
  }

  return result;
}

export function downloadiXBRLFile(
  report: ReportDocument,
  taxonomies: string[] = ['esrs', 'gri', 'sasb'],
  options: {
    validate?: boolean;
    optimize?: boolean;
    includeMetadata?: boolean;
  } = { validate: true, optimize: true, includeMetadata: false }
) {
  try {
    const result = generateOptimizediXBRLDocument(report, taxonomies, options);

    // Check validation results if validation was performed
    if (options.validate && result.validation && !result.validation.isValid) {
      console.warn('iXBRL validation warnings:', result.validation.errors);
      // Continue with download but log warnings
    }

    const blob = new Blob([result.content], {
      type: 'application/xhtml+xml;charset=utf-8',
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;

    const taxonomyString = taxonomies.join('_');
    const fileName = `${report.title
      .replace(/[^a-z0-9]/gi, '_')
      .toLowerCase()}_${taxonomyString}_sustainability.ixbrl`;

    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    console.log('Enhanced iXBRL file downloaded successfully:', fileName);
    if (result.metadata) {
      console.log('Document metadata:', result.metadata);
    }
  } catch (error) {
    console.error('Error generating enhanced iXBRL file:', error);
    throw new Error(
      `Failed to generate iXBRL file: ${
        error instanceof Error ? error.message : 'Unknown error'
      }`
    );
  }
}

export function previewiXBRLContent(
  report: ReportDocument,
  taxonomies: string[] = ['esrs', 'gri', 'sasb']
): string {
  return generateiXBRLDocument(report, taxonomies);
}

// Utility functions for taxonomy-specific features
export function getSupportedTaxonomies(): string[] {
  return Object.keys(TAXONOMY_CONFIGS);
}

export function getTaxonomyInfo(taxonomy: string) {
  return TAXONOMY_CONFIGS[taxonomy as keyof typeof TAXONOMY_CONFIGS];
}

export function validateConceptForTaxonomy(
  conceptId: string,
  taxonomy: string
): boolean {
  const config = TAXONOMY_CONFIGS[taxonomy as keyof typeof TAXONOMY_CONFIGS];
  if (!config) return false;

  const conceptName = parseConceptNameWithTaxonomy(conceptId, [taxonomy]);
  return config.conceptValidation(conceptName);
}

// Legacy exports for backward compatibility
export const downloadXBRLFile = downloadiXBRLFile;
export const previewXBRLContent = previewiXBRLContent;
