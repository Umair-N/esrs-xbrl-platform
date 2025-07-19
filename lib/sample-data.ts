import type {
  ReportDocument,
  TaxonomyConcept,
  XbrlContext,
} from "@/types/report";
import { generateUniqueId } from "@/lib/utils";

// Updated ESRS Taxonomy Concepts (2023-12-22 version)
export const sampleTaxonomyConcepts: TaxonomyConcept[] = [
  {
    id: "esrs_e1_ClimateChangeTransitionPlan",
    label: "Climate Change Transition Plan",
    definition:
      "The entity's plan to ensure that its business model and strategy are compatible with the transition to a climate-neutral economy and with limiting global warming to 1.5°C in line with the Paris Agreement.",
    type: "ESRS E1",
    dataType: "string",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Climate Change Transition Plan" },
      {
        role: "documentation",
        value:
          "The entity's plan to ensure that its business model and strategy are compatible with the transition to a climate-neutral economy and with limiting global warming to 1.5°C in line with the Paris Agreement.",
      },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-1",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e1/",
      },
    ],
  },
  {
    id: "esrs_e1_GrossScope1GreenhouseGasEmissions",
    label: "Gross Scope 1 Greenhouse Gas Emissions",
    definition:
      "Direct greenhouse gas emissions from sources that are owned or controlled by the entity, expressed in metric tons of CO2 equivalent.",
    type: "ESRS E1",
    dataType: "decimal",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Gross Scope 1 Greenhouse Gas Emissions" },
      {
        role: "documentation",
        value:
          "Direct greenhouse gas emissions from sources that are owned or controlled by the entity, expressed in metric tons of CO2 equivalent.",
      },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-6",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e1/",
      },
    ],
  },
  {
    id: "esrs_e1_GrossScope2GreenhouseGasEmissions",
    label: "Gross Scope 2 Greenhouse Gas Emissions",
    definition:
      "Indirect greenhouse gas emissions from the generation of purchased electricity, steam, heating and cooling consumed by the entity, expressed in metric tons of CO2 equivalent.",
    type: "ESRS E1",
    dataType: "decimal",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Gross Scope 2 Greenhouse Gas Emissions" },
      {
        role: "documentation",
        value:
          "Indirect greenhouse gas emissions from the generation of purchased electricity, steam, heating and cooling consumed by the entity, expressed in metric tons of CO2 equivalent.",
      },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-6",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e1/",
      },
    ],
  },
  {
    id: "esrs_e1_GrossScope3GreenhouseGasEmissions",
    label: "Gross Scope 3 Greenhouse Gas Emissions",
    definition:
      "Other indirect greenhouse gas emissions that occur in the value chain of the entity, including both upstream and downstream emissions, expressed in metric tons of CO2 equivalent.",
    type: "ESRS E1",
    dataType: "decimal",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Gross Scope 3 Greenhouse Gas Emissions" },
      {
        role: "documentation",
        value:
          "Other indirect greenhouse gas emissions that occur in the value chain of the entity, including both upstream and downstream emissions, expressed in metric tons of CO2 equivalent.",
      },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-6",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e1/",
      },
    ],
  },
  {
    id: "esrs_e1_ScienceBasedTargetsValidatedByInitiative",
    label: "Science-Based Targets Validated by Initiative",
    definition:
      "Whether the entity has science-based targets validated by the Science Based Targets initiative.",
    type: "ESRS E1",
    dataType: "boolean",
    periodType: "duration",
    abstract: false,
    labels: [
      {
        role: "standard",
        value: "Science-Based Targets Validated by Initiative",
      },
      {
        role: "documentation",
        value:
          "Whether the entity has science-based targets validated by the Science Based Targets initiative.",
      },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-3",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e1/",
      },
    ],
  },
  {
    id: "esrs_e1_PercentageOfApproximateGrossScope3GreenhouseGasEmissionsCoveredByInternalCarbonPricingScheme",
    label:
      "Percentage of Scope 3 GHG Emissions Covered by Internal Carbon Pricing",
    definition:
      "The percentage of approximate gross Scope 3 greenhouse gas emissions covered by internal carbon pricing scheme.",
    type: "ESRS E1",
    dataType: "decimal",
    periodType: "duration",
    abstract: false,
    labels: [
      {
        role: "standard",
        value:
          "Percentage of Scope 3 GHG Emissions Covered by Internal Carbon Pricing",
      },
      {
        role: "documentation",
        value:
          "The percentage of approximate gross Scope 3 greenhouse gas emissions covered by internal carbon pricing scheme.",
      },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-7",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e1/",
      },
    ],
  },
  {
    id: "esrs_s1_TotalNumberOfEmployees",
    label: "Total Number of Employees",
    definition:
      "The total number of employees at the end of the reporting period.",
    type: "ESRS S1",
    dataType: "integer",
    periodType: "instant",
    abstract: false,
    labels: [
      { role: "standard", value: "Total Number of Employees" },
      {
        role: "documentation",
        value:
          "The total number of employees at the end of the reporting period.",
      },
    ],
    references: [
      {
        name: "ESRS S1",
        paragraph: "Disclosure Requirement S1-6",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_s1/",
      },
    ],
  },
  {
    id: "esrs_s1_PercentageOfEmployeesCoveredByCollectiveBargainingAgreements",
    label: "Percentage of Employees Covered by Collective Bargaining",
    definition:
      "The percentage of total employees covered by collective bargaining agreements.",
    type: "ESRS S1",
    dataType: "decimal",
    periodType: "instant",
    abstract: false,
    labels: [
      {
        role: "standard",
        value: "Percentage of Employees Covered by Collective Bargaining",
      },
      {
        role: "documentation",
        value:
          "The percentage of total employees covered by collective bargaining agreements.",
      },
    ],
    references: [
      {
        name: "ESRS S1",
        paragraph: "Disclosure Requirement S1-8",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_s1/",
      },
    ],
  },
  {
    id: "esrs_g1_DisclosureOfRoleOfAdministrativeManagementAndSupervisoryBodiesRelatedToBusinessConductExplanatory",
    label: "Role of Administrative Bodies in Business Conduct",
    definition:
      "The role of the administrative, management and supervisory bodies with regard to business conduct matters.",
    type: "ESRS G1",
    dataType: "string",
    periodType: "duration",
    abstract: false,
    labels: [
      {
        role: "standard",
        value: "Role of Administrative Bodies in Business Conduct",
      },
      {
        role: "documentation",
        value:
          "The role of the administrative, management and supervisory bodies with regard to business conduct matters.",
      },
    ],
    references: [
      {
        name: "ESRS G1",
        paragraph: "Disclosure Requirement G1-1",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_g1/",
      },
    ],
  },
  {
    id: "esrs:NetRevenueOtherThanUsedToCalculateGHGIntensity",
    label: "Net Revenue (Other than for GHG Intensity)",
    definition:
      "Net revenue other than the net revenue used to calculate GHG emission intensities.",
    type: "ESRS",
    dataType: "monetary",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Net Revenue (Other than for GHG Intensity)" },
      {
        role: "documentation",
        value:
          "Net revenue other than the net revenue used to calculate GHG emission intensities.",
      },
    ],
    references: [
      {
        name: "ESRS 1",
        paragraph: "Appendix C",
        uri: "https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs/",
      },
    ],
  },
];

// Updated XBRL Contexts with LEI scheme
export const sampleContexts: XbrlContext[] = [
  {
    id: "current",
    label: "Current Period - 2024",
    entityName: "Acme Corporation",
    entityScheme: "http://www.moorpro.com",
    entityIdentifier: "12345654321",
    periodType: "duration",
    startDate: new Date("2024-01-01"),
    endDate: new Date("2024-12-31"),
    createdAt: new Date().toISOString(),
  },
  {
    id: "instant-current",
    label: "As of December 31, 2024",
    entityName: "Acme Corporation",
    entityScheme: "http://www.moorpro.com",
    entityIdentifier: "12345654321",
    periodType: "instant",
    instantDate: new Date("2024-12-31"),
    createdAt: new Date().toISOString(),
  },
  {
    id: "previous",
    label: "Previous Period - 2023",
    entityName: "Acme Corporation",
    entityScheme: "http://www.moorpro.com",
    entityIdentifier: "12345654321",
    periodType: "duration",
    startDate: new Date("2023-01-01"),
    endDate: new Date("2023-12-31"),
    createdAt: new Date().toISOString(),
  },
];

// Updated Sample Report with proper ESRS structure
export const sampleReport: ReportDocument = {
  id: generateUniqueId(),
  title: "Acme Corporation Sustainability Report 2024",
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  blocks: [
    {
      id: generateUniqueId(),
      content: "Governance and Risk Management",
      type: "heading",
      tags: [],
    },
    {
      id: generateUniqueId(),
      content:
        "The administrative and supervisory bodies ensure ESG integration into core governance. Risk assessment results and controls are embedded in strategic and operational decision-making.",
      type: "paragraph",
      tags: [
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[8], // Role of Administrative Bodies
          context: sampleContexts[0], // Current period
          createdAt: new Date().toISOString(),
          startIndex: 0,
          endIndex: 89,
        },
      ],
    },
    {
      id: generateUniqueId(),
      content: "Climate Change and Emissions",
      type: "heading",
      tags: [],
    },
    {
      id: generateUniqueId(),
      content:
        "In 2024, our Scope 1 emissions totaled 25,400 metric tons CO2e, Scope 2 emissions were 18,200 metric tons CO2e, and Scope 3 emissions reached 145,800 metric tons CO2e. We have validated science-based targets and cover 65.25% of our Scope 3 emissions with internal carbon pricing.",
      type: "paragraph",
      tags: [
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[1], // Scope 1 Emissions
          context: sampleContexts[0],
          createdAt: new Date().toISOString(),
          startIndex: 34,
          endIndex: 56, // "25,400 metric tons CO2e"
        },
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[2], // Scope 2 Emissions
          context: sampleContexts[0],
          createdAt: new Date().toISOString(),
          startIndex: 79,
          endIndex: 101, // "18,200 metric tons CO2e"
        },
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[3], // Scope 3 Emissions
          context: sampleContexts[0],
          createdAt: new Date().toISOString(),
          startIndex: 131,
          endIndex: 154, // "145,800 metric tons CO2e"
        },
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[5], // Percentage covered by carbon pricing
          context: sampleContexts[0],
          createdAt: new Date().toISOString(),
          startIndex: 230,
          endIndex: 236, // "65.25%"
        },
      ],
    },
    {
      id: generateUniqueId(),
      content: "Workforce Information",
      type: "heading",
      tags: [],
    },
    {
      id: generateUniqueId(),
      content:
        "As of December 31, 2024, we employed 8,450 people. Approximately 72.3% of our workforce is covered by collective bargaining agreements.",
      type: "paragraph",
      tags: [
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[6], // Total Number of Employees
          context: sampleContexts[1], // Instant context
          createdAt: new Date().toISOString(),
          startIndex: 41,
          endIndex: 46, // "8,450"
        },
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[7], // Collective bargaining percentage
          context: sampleContexts[1],
          createdAt: new Date().toISOString(),
          startIndex: 70,
          endIndex: 75, // "72.3%"
        },
      ],
    },
    {
      id: generateUniqueId(),
      content: "Financial Performance",
      type: "heading",
      tags: [],
    },
    {
      id: generateUniqueId(),
      content:
        "Our net revenue for 2024, excluding amounts used for GHG intensity calculations, was €248,000,000.",
      type: "paragraph",
      tags: [
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[9], // Net Revenue
          context: sampleContexts[0],
          createdAt: new Date().toISOString(),
          startIndex: 82,
          endIndex: 96, // "€248,000,000"
        },
      ],
    },
  ],
};

// Updated XBRL Output Sample
export const sampleXbrlOutput = `<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:xbrli="http://www.xbrl.org/2003/instance"
      xmlns:link="http://www.xbrl.org/2003/linkbase"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"
      xmlns:esrs="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22"
      xmlns:esrs_e1="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_e1"
      xmlns:esrs_s1="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_s1"
      xmlns:esrs_g1="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_g1"
      xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<head>
  <title>Acme Corporation Sustainability Report 2024</title>
</head>
<body>
  <ix:header>
    <ix:references>
      <link:schemaRef xlink:type="simple"
        xlink:href="https://xbrl.efrag.org/taxonomy/esrs/2023-12-22/esrs_all.xsd"/>
    </ix:references>
    <ix:resources>
      <xbrli:context id="current">
        <xbrli:entity>
          <xbrli:identifier scheme="http://www.moorpro.com">12345654321</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
          <xbrli:startDate>2024-01-01</xbrli:startDate>
          <xbrli:endDate>2024-12-31</xbrli:endDate>
        </xbrli:period>
      </xbrli:context>
      <xbrli:unit id="U-EUR">
        <xbrli:measure>iso4217:EUR</xbrli:measure>
      </xbrli:unit>
      <xbrli:unit id="pure">
        <xbrli:measure>xbrli:pure</xbrli:measure>
      </xbrli:unit>
      <xbrli:unit id="tCO2e">
        <xbrli:measure>xbrli:pure</xbrli:measure>
      </xbrli:unit>
    </ix:resources>
  </ix:header>

  <h1>Sustainability Disclosures</h1>

  <p>
    <ix:nonFraction name="esrs_e1:GrossScope1GreenhouseGasEmissions"
                    contextRef="current"
                    unitRef="tCO2e"
                    decimals="0">25400</ix:nonFraction> metric tons CO2e Scope 1 emissions
  </p>

  <p>
    <ix:nonFraction name="esrs:NetRevenueOtherThanUsedToCalculateGHGIntensity"
                    contextRef="current"
                    unitRef="U-EUR"
                    decimals="0">248000000</ix:nonFraction>
  </p>

</body>
</html>`;

// Updated JSON Output Sample
export const sampleJsonOutput = `{
  "documentInfo": {
    "documentType": "ESRS-XBRL",
    "taxonomy": "ESRS 2023-12-22",
    "reportingEntity": "Acme Corporation",
    "reportingPeriod": "2024-01-01 to 2024-12-31"
  },
  "contexts": [
    {
      
      "id": "current", 
      "entity": {
        "identifier": {
          "scheme": "http://www.moorpro.com",
          "value": "12345654321"
        }
      },
      "period": {
        "startDate": "2024-01-01",
        "endDate": "2024-12-31"
      }
    }
  ],
  "facts": [
    {
      "concept": "esrs_e1:GrossScope1GreenhouseGasEmissions",
      "contextRef": "current",
      "value": 25400,
      "unit": "tCO2e",
      "decimals": 0
    },
    {
      "concept": "esrs:NetRevenueOtherThanUsedToCalculateGHGIntensity", 
      "contextRef": "current",
      "value": 248000000,
      "unit": "EUR",
      "decimals": 0
    }
  ]
}`;
