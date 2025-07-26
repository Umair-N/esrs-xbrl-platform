// @ts-nocheck

import type { ReportDocument, XbrlTag } from "@/types/report";

interface XBRLNamespace {
  prefix: string;
  uri: string;
}

const IXBRL_NAMESPACES: XBRLNamespace[] = [
  { prefix: "xbrli", uri: "http://www.xbrl.org/2003/instance" },
  { prefix: "link", uri: "http://www.xbrl.org/2003/linkbase" },
  { prefix: "xlink", uri: "http://www.w3.org/1999/xlink" },
  { prefix: "ix", uri: "http://www.xbrl.org/2013/inlineXBRL" },
  { prefix: "esrs", uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22" },
  {
    prefix: "esrs_e1",
    uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e1",
  },
  {
    prefix: "esrs_g1",
    uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_g1",
  },
  {
    prefix: "esrs_s1",
    uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_s1",
  },
  { prefix: "iso4217", uri: "http://www.xbrl.org/2003/iso4217" },
  { prefix: "xbrldt", uri: "http://xbrl.org/2005/xbrldt" },
  { prefix: "xsi", uri: "http://www.w3.org/2001/XMLSchema-instance" },
];

export function generateiXBRLDocument(report: ReportDocument): string {
  const namespaces = IXBRL_NAMESPACES.map(
    (ns) => `      xmlns:${ns.prefix}="${ns.uri}"`
  ).join("\n");

  // Get all unique contexts and units from the report
  const contexts = getUniqueContexts(report);
  const units = getUniqueUnits(report);

  // Generate iXBRL document
  const ixbrl = `<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"
${namespaces}>
<head>
  <title>${escapeHTML(report.title)}</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <style type="text/css">
    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
    h1, h2, h3 { color: #2c5282; }
    
    /* Style iXBRL elements directly without class attributes */
    ix\\:nonNumeric, ix\\:nonFraction {
      background-color: #e6f3ff;
      padding: 2px 4px;
      border-radius: 3px;
      display: inline;
      border: 1px solid #b3d9ff;
      margin: 0 1px;
    }
    
    /* Style monetary values */
    ix\\:nonFraction[unitRef="U-EUR"], ix\\:nonFraction[unitRef="U-USD"] {
      font-weight: bold;
      color: #2d5016;
      background-color: #e8f5e8;
      border-color: #c3e6c3;
    }
    
    /* Style percentage values */
    ix\\:nonFraction[unitRef="pure"] {
      color: #744210;
      background-color: #fff3cd;
      border-color: #ffeaa7;
    }
    
    .section { margin-bottom: 30px; }
    .content-block { 
      margin-bottom: 15px; 
      padding: 10px;
      background-color: #f8f9fa;
      border-left: 4px solid #007bff;
    }
    
    /* Hover effects for tagged elements */
    ix\\:nonNumeric:hover, ix\\:nonFraction:hover {
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      transform: translateY(-1px);
      transition: all 0.2s ease;
      cursor: pointer;
    }
    
    /* Additional styling for better readability */
    ix\\:nonNumeric::before, ix\\:nonFraction::before {
      content: "📊";
      font-size: 10px;
      margin-right: 2px;
      opacity: 0.7;
    }
  </style>
</head>
<body>
  <ix:header>
    <ix:references>
      <link:schemaRef xlink:type="simple"
        xlink:href="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_all.xsd"/>
    </ix:references>
    <ix:resources>
${generateContextsXML(contexts)}
${generateUnitsXML(units)}
    </ix:resources>
  </ix:header>

  <h1>Sustainability Disclosures</h1>
  <p><em>Generated on: ${new Date().toLocaleDateString()}</em></p>

${generateReportContent(report)}

</body>
</html>`;

  return ixbrl;
}

function getUniqueContexts(report: ReportDocument) {
  const contextMap = new Map();

  report.blocks.forEach((block) => {
    block.tags.forEach((tag) => {
      if (!contextMap.has(tag.context.id)) {
        contextMap.set(tag.context.id, tag.context);
      }
    });
  });

  return Array.from(contextMap.values());
}

function getUniqueUnits(report: ReportDocument) {
  const unitMap = new Map();

  // Add standard units
  unitMap.set("U-EUR", { id: "U-EUR", measure: "iso4217:EUR" });
  unitMap.set("U-USD", { id: "U-USD", measure: "iso4217:USD" });
  unitMap.set("pure", { id: "pure", measure: "xbrli:pure" });
  unitMap.set("tCO2e", { id: "tCO2e", measure: "xbrli:pure" });
  unitMap.set("MWh", { id: "MWh", measure: "xbrli:pure" });
  unitMap.set("m3", { id: "m3", measure: "xbrli:pure" });
  unitMap.set("tonnes", { id: "tonnes", measure: "xbrli:pure" });

  return Array.from(unitMap.values());
}

function generateContextsXML(contexts: any[]): string {
  return contexts
    .map((context) => {
      const formatDate = (dateInput: any) => {
        if (!dateInput) return "2024-12-31";

        if (typeof dateInput === "string") {
          if (/^\d{4}-\d{2}-\d{2}$/.test(dateInput)) {
            return dateInput;
          }
          const date = new Date(dateInput);
          if (!isNaN(date.getTime())) {
            return date.toISOString().split("T")[0];
          }
        } else if (dateInput instanceof Date) {
          return dateInput.toISOString().split("T")[0];
        }

        return "2024-12-31";
      };

      const entityScheme = context.entityScheme || "http://www.sec.gov/CIK";
      const entityId = context.entity || "12345654321";

      return `      <xbrli:context id="${context.id}">
        <xbrli:entity>
          <xbrli:identifier scheme="${entityScheme}">${entityId}</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
          ${
            context.periodType === "instant"
              ? `<xbrli:instant>${formatDate(
                  context.period || context.instantDate
                )}</xbrli:instant>`
              : `<xbrli:startDate>${formatDate(
                  context.startDate
                )}</xbrli:startDate>
          <xbrli:endDate>${formatDate(context.endDate)}</xbrli:endDate>`
          }
        </xbrli:period>
      </xbrli:context>`;
    })
    .join("\n");
}

function generateUnitsXML(units: any[]): string {
  return units
    .map(
      (unit) => `      <xbrli:unit id="${unit.id}">
        <xbrli:measure>${unit.measure}</xbrli:measure>
      </xbrli:unit>`
    )
    .join("\n");
}

function generateReportContent(report: ReportDocument): string {
  const sections = groupBlocksBySection(report.blocks);
  let content = "";

  sections.forEach((section) => {
    content += `  <div class="section">\n`;

    if (section.title) {
      content += `    <h2>${escapeHTML(section.title)}</h2>\n`;
    }

    section.blocks.forEach((block) => {
      content += generateBlockContentWithTagsDetailed(block);
    });

    content += `  </div>\n\n`;
  });

  return content;
}

function groupBlocksBySection(blocks: any[]) {
  const sections = [];
  let currentSection = { title: null, blocks: [] };

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
  if (id.includes("governance") || id.includes("administrative"))
    return "governance";
  if (id.includes("ghg") || id.includes("emission") || id.includes("climate"))
    return "climate";
  if (id.includes("risk") || id.includes("assessment")) return "risk";
  if (id.includes("revenue") || id.includes("financial")) return "financial";
  return "general";
}

function getSectionTitle(category: string): string {
  const titles = {
    governance: "Governance and Risk Management",
    climate: "Climate-related Risks and Opportunities",
    risk: "Risk Assessment",
    financial: "Financial Information",
    general: "General Disclosures",
  };
  return titles[category] || "Sustainability Disclosures";
}

function generateBlockContentWithTagsDetailed(block: any): string {
  if (block.tags.length === 0) {
    return `    <div class="content-block">${escapeHTML(
      block.content
    )}</div>\n`;
  }

  const sortedTags = [...block.tags].sort(
    (a, b) => (a.startIndex || 0) - (b.startIndex || 0)
  );

  let content = block.content;
  let processedContent = "";
  let lastIndex = 0;

  sortedTags.forEach((tag: XbrlTag, index: number) => {
    const startIndex = tag.startIndex || 0;
    const endIndex = tag.endIndex || startIndex;

    if (startIndex !== endIndex && startIndex < block.content.length) {
      // Add content before the tag (escaped)
      processedContent += escapeHTML(content.substring(lastIndex, startIndex));

      // Add the tagged content with tooltip
      const taggedText = content.substring(startIndex, endIndex);
      const ixbrlTag = generateiXBRLTagWithTooltip(tag, taggedText, index + 1);
      processedContent += ixbrlTag;

      lastIndex = endIndex;
    }
  });

  // Add remaining content after the last tag (escaped)
  processedContent += escapeHTML(content.substring(lastIndex));

  // Preserve line breaks
  processedContent = processedContent.replace(/\n/g, "<br/>");

  return `    <div class="content-block">${processedContent}</div>\n\n`;
}

function generateiXBRLTagWithTooltip(
  tag: any,
  value: string,
  tagNumber: number
): string {
  const concept = tag.concept;
  const isNumeric = isNumericConcept(concept);
  const unitRef = determineUnitRef(concept);
  const conceptName = parseConceptName(concept.id);
  const label = generateLabelFromConcept(concept.id);

  const tooltipInfo = `Tag ${tagNumber}: ${label} (${conceptName})${
    unitRef ? ` - Unit: ${unitRef}` : ""
  }`;

  if (isNumeric) {
    const attributes = [
      `name="${conceptName}"`,
      `contextRef="${tag.context.id}"`,
      unitRef ? `unitRef="${unitRef}"` : null,
      `decimals="${getDecimals(concept)}"`,
      `title="${escapeHTML(tooltipInfo)}"`,
    ]
      .filter(Boolean)
      .join(" ");

    return `<ix:nonFraction ${attributes}>${escapeHTML(
      value
    )}</ix:nonFraction>`;
  } else {
    const attributes = [
      `name="${conceptName}"`,
      `contextRef="${tag.context.id}"`,
      `title="${escapeHTML(tooltipInfo)}"`,
    ]
      .filter(Boolean)
      .join(" ");

    return `<ix:nonNumeric ${attributes}>${escapeHTML(value)}</ix:nonNumeric>`;
  }
}

function generateiXBRLTag(tag: any, value: string): string {
  const concept = tag.concept;
  const isNumeric = isNumericConcept(concept);
  const unitRef = determineUnitRef(concept);

  // Convert concept ID to proper namespace:element format
  const conceptName = parseConceptName(concept.id);

  if (isNumeric) {
    const attributes = [
      `name="${conceptName}"`,
      `contextRef="${tag.context.id}"`,
      unitRef ? `unitRef="${unitRef}"` : null,
      `decimals="${getDecimals(concept)}"`,
    ]
      .filter(Boolean)
      .join(" ");

    return `<ix:nonFraction ${attributes}>${escapeHTML(
      value
    )}</ix:nonFraction>`;
  } else {
    const attributes = [
      `name="${conceptName}"`,
      `contextRef="${tag.context.id}"`,
    ]
      .filter(Boolean)
      .join(" ");

    return `<ix:nonNumeric ${attributes}>${escapeHTML(value)}</ix:nonNumeric>`;
  }
}

function parseConceptName(conceptId: string): string {
  // Handle different concept ID formats and convert to proper namespace:element format
  if (conceptId.includes(":")) {
    return conceptId; // Already in correct format
  }

  // Handle ESRS taxonomy concepts properly
  if (conceptId.startsWith("esrs_")) {
    // Extract the proper namespace and local name
    const withoutPrefix = conceptId.substring(5); // Remove "esrs_"

    // Check if it has a subnamespace like e1, g1, s1
    const parts = withoutPrefix.split("_");
    if (parts.length >= 1 && ["e1", "g1", "s1"].includes(parts[0])) {
      const namespace = `esrs_${parts[0]}`;
      const localName = parts.slice(1).join("");
      return `${namespace}:${localName}`;
    } else {
      // General ESRS concept
      return `esrs:${withoutPrefix}`;
    }
  }

  // Convert underscore format to colon format for other cases
  if (conceptId.includes("_")) {
    const parts = conceptId.split("_");
    if (parts.length >= 2) {
      return `${parts[0]}:${parts.slice(1).join("")}`;
    }
  }

  // Default to esrs namespace if no clear namespace found
  return `esrs:${conceptId}`;
}

function extractTaggedText(content: string, tag: any): string {
  if (
    tag.startIndex !== undefined &&
    tag.endIndex !== undefined &&
    tag.startIndex !== tag.endIndex
  ) {
    return content.substring(tag.startIndex, tag.endIndex).trim();
  }

  return cleanFactValue(content, tag.concept.dataType);
}

function generateLabelFromConcept(conceptId: string): string {
  const parts = conceptId.split(":");
  const name = parts[parts.length - 1];

  return name
    .replace(/([A-Z])/g, " $1")
    .replace(/^./, (str) => str.toUpperCase())
    .trim();
}

function isNumericConcept(concept: any): boolean {
  const numericTypes = [
    "monetary",
    "decimal",
    "integer",
    "shares",
    "percentage",
  ];
  return numericTypes.includes(concept.dataType?.toLowerCase());
}

function determineUnitRef(concept: any): string | null {
  const conceptId = concept.id.toLowerCase();
  const dataType = concept.dataType?.toLowerCase();

  if (dataType === "monetary") {
    return "U-EUR";
  }

  if (conceptId.includes("percentage") || conceptId.includes("ratio")) {
    return "pure";
  }

  if (
    conceptId.includes("ghg") ||
    conceptId.includes("emission") ||
    conceptId.includes("carbon")
  ) {
    return "tCO2e";
  }

  if (conceptId.includes("energy")) {
    return "MWh";
  }

  if (conceptId.includes("water")) {
    return "m3";
  }

  if (conceptId.includes("waste")) {
    return "tonnes";
  }

  if (dataType === "decimal" || dataType === "integer") {
    return "pure";
  }

  return null;
}

function getDecimals(concept: any): string {
  const dataType = concept.dataType?.toLowerCase();

  if (dataType === "monetary") {
    return "0";
  } else if (dataType === "percentage") {
    return "2";
  } else if (dataType === "decimal") {
    return "2";
  } else if (dataType === "integer") {
    return "0";
  }

  return "2";
}

function cleanFactValue(text: string, dataType: string): string {
  if (!text) return "";

  switch (dataType?.toLowerCase()) {
    case "monetary":
      const monetaryMatch = text.match(/-?[\d,]+\.?\d*/g);
      if (monetaryMatch) {
        return monetaryMatch[0].replace(/,/g, "");
      }
      return "0";

    case "integer":
      const intMatch = text.match(/-?\d+/g);
      return intMatch ? intMatch[0] : "0";

    case "decimal":
    case "percentage":
      const decimalMatch = text.match(/-?\d+\.?\d*/g);
      return decimalMatch ? decimalMatch[0] : "0";

    case "boolean":
      const lowerText = text.toLowerCase().trim();
      if (lowerText.includes("true") || lowerText.includes("yes"))
        return "true";
      if (lowerText.includes("false") || lowerText.includes("no"))
        return "false";
      return "true";

    default:
      return text.replace(/\s+/g, " ").trim().substring(0, 500);
  }
}

function escapeHTML(text: string): string {
  if (!text) return "";
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

export function downloadiXBRLFile(report: ReportDocument) {
  try {
    const ixbrlContent = generateiXBRLDocument(report);

    if (
      !ixbrlContent.includes('<html xmlns="http://www.w3.org/1999/xhtml"') ||
      !ixbrlContent.includes("</html>")
    ) {
      throw new Error("Invalid iXBRL structure generated");
    }

    const blob = new Blob([ixbrlContent], {
      type: "application/xhtml+xml;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    const fileName = `${report.title
      .replace(/[^a-z0-9]/gi, "_")
      .toLowerCase()}_esrs.ixbrl`;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);

    console.log("ESRS iXBRL file downloaded successfully:", fileName);
  } catch (error) {
    console.error("Error generating iXBRL file:", error);
    throw new Error(
      `Failed to generate iXBRL file: ${
        error instanceof Error ? error.message : "Unknown error"
      }`
    );
  }
}

export function previewiXBRLContent(report: ReportDocument): string {
  return generateiXBRLDocument(report);
}

export const downloadXBRLFile = downloadiXBRLFile;
export const previewXBRLContent = previewiXBRLContent;
