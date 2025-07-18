import type { ReportDocument, TaxonomyConcept, XbrlContext } from "@/types/report"
import { generateUniqueId } from "@/lib/utils"

// Sample Taxonomy Concepts
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
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F08%2520Draft%2520ESRS%2520E1.pdf",
      },
    ],
  },
  {
    id: "esrs_e1_GhgEmissionsScope1",
    label: "Greenhouse Gas Emissions Scope 1",
    definition: "Direct greenhouse gas emissions from sources that are owned or controlled by the entity.",
    type: "ESRS E1",
    dataType: "decimal",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Greenhouse Gas Emissions Scope 1" },
      {
        role: "documentation",
        value: "Direct greenhouse gas emissions from sources that are owned or controlled by the entity.",
      },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-6",
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F08%2520Draft%2520ESRS%2520E1.pdf",
      },
    ],
  },
  {
    id: "esrs_e1_GhgEmissionsScope2",
    label: "Greenhouse Gas Emissions Scope 2",
    definition:
      "Indirect greenhouse gas emissions from the generation of purchased electricity, steam, heating and cooling consumed by the entity.",
    type: "ESRS E1",
    dataType: "decimal",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Greenhouse Gas Emissions Scope 2" },
      {
        role: "documentation",
        value:
          "Indirect greenhouse gas emissions from the generation of purchased electricity, steam, heating and cooling consumed by the entity.",
      },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-6",
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F08%2520Draft%2520ESRS%2520E1.pdf",
      },
    ],
  },
  {
    id: "esrs_e1_GhgEmissionsScope3",
    label: "Greenhouse Gas Emissions Scope 3",
    definition:
      "Other indirect greenhouse gas emissions that occur in the value chain of the entity, including both upstream and downstream emissions.",
    type: "ESRS E1",
    dataType: "decimal",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Greenhouse Gas Emissions Scope 3" },
      {
        role: "documentation",
        value:
          "Other indirect greenhouse gas emissions that occur in the value chain of the entity, including both upstream and downstream emissions.",
      },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-6",
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F08%2520Draft%2520ESRS%2520E1.pdf",
      },
    ],
  },
  {
    id: "esrs_e1_ClimateChangeTargets",
    label: "Climate Change Targets",
    definition: "The entity's targets related to climate change mitigation and adaptation.",
    type: "ESRS E1",
    dataType: "string",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Climate Change Targets" },
      { role: "documentation", value: "The entity's targets related to climate change mitigation and adaptation." },
    ],
    references: [
      {
        name: "ESRS E1",
        paragraph: "Disclosure Requirement E1-3",
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F08%2520Draft%2520ESRS%2520E1.pdf",
      },
    ],
  },
  {
    id: "esrs_s1_OwnWorkforceWorkingConditions",
    label: "Own Workforce Working Conditions",
    definition: "Information on the working conditions of the entity's own workforce.",
    type: "ESRS S1",
    dataType: "string",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Own Workforce Working Conditions" },
      { role: "documentation", value: "Information on the working conditions of the entity's own workforce." },
    ],
    references: [
      {
        name: "ESRS S1",
        paragraph: "Disclosure Requirement S1-7",
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F13%2520Draft%2520ESRS%2520S1.pdf",
      },
    ],
  },
  {
    id: "esrs_s1_OwnWorkforceEqualOpportunities",
    label: "Own Workforce Equal Opportunities",
    definition: "Information on equal opportunities for the entity's own workforce.",
    type: "ESRS S1",
    dataType: "string",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Own Workforce Equal Opportunities" },
      { role: "documentation", value: "Information on equal opportunities for the entity's own workforce." },
    ],
    references: [
      {
        name: "ESRS S1",
        paragraph: "Disclosure Requirement S1-8",
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F13%2520Draft%2520ESRS%2520S1.pdf",
      },
    ],
  },
  {
    id: "esrs_g1_BusinessConductCulturePolicies",
    label: "Business Conduct Culture Policies",
    definition: "The entity's policies related to business conduct culture.",
    type: "ESRS G1",
    dataType: "string",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Business Conduct Culture Policies" },
      { role: "documentation", value: "The entity's policies related to business conduct culture." },
    ],
    references: [
      {
        name: "ESRS G1",
        paragraph: "Disclosure Requirement G1-3",
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F19%2520Draft%2520ESRS%2520G1.pdf",
      },
    ],
  },
  {
    id: "esrs_g1_CorporateGovernanceStructure",
    label: "Corporate Governance Structure",
    definition: "The entity's corporate governance structure and composition.",
    type: "ESRS G1",
    dataType: "string",
    periodType: "instant",
    abstract: false,
    labels: [
      { role: "standard", value: "Corporate Governance Structure" },
      { role: "documentation", value: "The entity's corporate governance structure and composition." },
    ],
    references: [
      {
        name: "ESRS G1",
        paragraph: "Disclosure Requirement G1-1",
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F19%2520Draft%2520ESRS%2520G1.pdf",
      },
    ],
  },
  {
    id: "esrs_g1_RemumerationPolicies",
    label: "Remuneration Policies",
    definition: "The entity's remuneration policies for administrative, management and supervisory bodies.",
    type: "ESRS G1",
    dataType: "string",
    periodType: "duration",
    abstract: false,
    labels: [
      { role: "standard", value: "Remuneration Policies" },
      {
        role: "documentation",
        value: "The entity's remuneration policies for administrative, management and supervisory bodies.",
      },
    ],
    references: [
      {
        name: "ESRS G1",
        paragraph: "Disclosure Requirement G1-2",
        uri: "https://www.efrag.org/Assets/Download?assetUrl=%2Fsites%2Fwebpublishing%2FSiteAssets%2F19%2520Draft%2520ESRS%2520G1.pdf",
      },
    ],
  },
]

// Sample Contexts
export const sampleContexts: XbrlContext[] = [
  {
    id: "ctx-2023-12-31",
    label: "Acme Corp - As of 2023-12-31",
    entityName: "Acme Corporation",
    entityScheme: "http://www.sec.gov/CIK",
    entityIdentifier: "0001234567",
    periodType: "instant",
    instantDate: new Date("2023-12-31"),
    createdAt: new Date().toISOString(),
  },
  {
    id: "ctx-2023",
    label: "Acme Corp - FY 2023",
    entityName: "Acme Corporation",
    entityScheme: "http://www.sec.gov/CIK",
    entityIdentifier: "0001234567",
    periodType: "duration",
    startDate: new Date("2023-01-01"),
    endDate: new Date("2023-12-31"),
    createdAt: new Date().toISOString(),
  },
  {
    id: "ctx-2022",
    label: "Acme Corp - FY 2022",
    entityName: "Acme Corporation",
    entityScheme: "http://www.sec.gov/CIK",
    entityIdentifier: "0001234567",
    periodType: "duration",
    startDate: new Date("2022-01-01"),
    endDate: new Date("2022-12-31"),
    createdAt: new Date().toISOString(),
  },
]

// Sample Report
export const sampleReport: ReportDocument = {
  id: generateUniqueId(),
  title: "Acme Corporation Sustainability Report 2023",
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  blocks: [
    {
      id: generateUniqueId(),
      content: "Climate Change Transition Plan",
      type: "heading",
      tags: [],
    },
    {
      id: generateUniqueId(),
      content:
        "Acme Corporation is committed to reducing its greenhouse gas emissions by 50% by 2030 compared to a 2020 baseline, and to achieving net-zero emissions by 2050. The company has developed a comprehensive transition plan that includes investments in renewable energy, energy efficiency improvements, and the electrification of its vehicle fleet.",
      type: "paragraph",
      tags: [
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[0], // Climate Change Transition Plan
          context: sampleContexts[1], // FY 2023
          createdAt: new Date().toISOString(),
        },
      ],
    },
    {
      id: generateUniqueId(),
      content: "Greenhouse Gas Emissions",
      type: "heading",
      tags: [],
    },
    {
      id: generateUniqueId(),
      content:
        "In 2023, Acme Corporation's Scope 1 emissions were 25,000 metric tons of CO2 equivalent, representing a 5% reduction compared to the previous year. The company's Scope 2 emissions were 15,000 metric tons of CO2 equivalent, a 10% reduction from 2022.",
      type: "paragraph",
      tags: [
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[1], // GHG Emissions Scope 1
          context: sampleContexts[1], // FY 2023
          createdAt: new Date().toISOString(),
        },
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[2], // GHG Emissions Scope 2
          context: sampleContexts[1], // FY 2023
          createdAt: new Date().toISOString(),
        },
      ],
    },
    {
      id: generateUniqueId(),
      content:
        "The company's Scope 3 emissions were estimated at 120,000 metric tons of CO2 equivalent, with the majority coming from purchased goods and services, and the use of sold products.",
      type: "paragraph",
      tags: [],
    },
    {
      id: generateUniqueId(),
      content: "Corporate Governance",
      type: "heading",
      tags: [],
    },
    {
      id: generateUniqueId(),
      content:
        "Acme Corporation's Board of Directors consists of 12 members, including 7 independent directors. The Board has established a Sustainability Committee responsible for overseeing the company's environmental, social, and governance (ESG) strategy and performance.",
      type: "paragraph",
      tags: [
        {
          id: generateUniqueId(),
          concept: sampleTaxonomyConcepts[8], // Corporate Governance Structure
          context: sampleContexts[0], // As of 2023-12-31
          createdAt: new Date().toISOString(),
        },
      ],
    },
  ],
}

// Sample XBRL Output
export const sampleXbrlOutput = `<?xml version="1.0" encoding="UTF-8"?>
<xbrl 
  xmlns="http://www.xbrl.org/2003/instance" 
  xmlns:link="http://www.xbrl.org/2003/linkbase" 
  xmlns:xlink="http://www.w3.org/1999/xlink" 
  xmlns:esrs="http://www.esrs.eu/2023" 
  xmlns:iso4217="http://www.xbrl.org/2003/iso4217">
  
  <!-- Contexts -->
  <context id="ctx-2023-12-31">
    <entity>
      <identifier scheme="http://www.sec.gov/CIK">0001234567</identifier>
    </entity>
    <period>
      <instant>2023-12-31</instant>
    </period>
  </context>
  
  <context id="ctx-2023">
    <entity>
      <identifier scheme="http://www.sec.gov/CIK">0001234567</identifier>
    </entity>
    <period>
      <startDate>2023-01-01</startDate>
      <endDate>2023-12-31</endDate>
    </period>
  </context>
  
  <context id="ctx-2022">
    <entity>
      <identifier scheme="http://www.sec.gov/CIK">0001234567</identifier>
    </entity>
    <period>
      <startDate>2022-01-01</startDate>
      <endDate>2022-12-31</endDate>
    </period>
  </context>
  
  <!-- Units -->
  <unit id="pure">
    <measure>xbrli:pure</measure>
  </unit>
  
  <unit id="metric-tons">
    <measure>esrs:metricTons</measure>
  </unit>
  
  <!-- Facts -->
  <esrs:ClimateChangeTransitionPlan contextRef="ctx-2023">
    Acme Corporation is committed to reducing its greenhouse gas emissions by 50% by 2030 compared to a 2020 baseline, and to achieving net-zero emissions by 2050. The company has developed a comprehensive transition plan that includes investments in renewable energy, energy efficiency improvements, and the electrification of its vehicle fleet.
  </esrs:ClimateChangeTransitionPlan>
  
  <esrs:GhgEmissionsScope1 contextRef="ctx-2023" unitRef="metric-tons" decimals="0">25000</esrs:GhgEmissionsScope1>
  <esrs:GhgEmissionsScope2 contextRef="ctx-2023" unitRef="metric-tons" decimals="0">15000</esrs:GhgEmissionsScope2>
  <esrs:GhgEmissionsScope3 contextRef="ctx-2023" unitRef="metric-tons" decimals="0">120000</esrs:GhgEmissionsScope3>
  
  <esrs:CorporateGovernanceStructure contextRef="ctx-2023-12-31">
    Acme Corporation's Board of Directors consists of 12 members, including 7 independent directors. The Board has established a Sustainability Committee responsible for overseeing the company's environmental, social, and governance (ESG) strategy and performance.
  </esrs:CorporateGovernanceStructure>
</xbrl>`

// Sample JSON Output
export const sampleJsonOutput = `{
  "documentInfo": {
    "documentType": "XBRL-JSON",
    "taxonomy": "ESRS 2023",
    "reportingEntity": "Acme Corporation",
    "reportingPeriod": "2023-01-01 to 2023-12-31"
  },
  "contexts": [
    {
      "id": "ctx-2023-12-31",
      "entity": {
        "identifier": {
          "scheme": "http://www.sec.gov/CIK",
          "value": "0001234567"
        },
        "name": "Acme Corporation"
      },
      "period": {
        "instant": "2023-12-31"
      }
    },
    {
      "id": "ctx-2023",
      "entity": {
        "identifier": {
          "scheme": "http://www.sec.gov/CIK",
          "value": "0001234567"
        },
        "name": "Acme Corporation"
      },
      "period": {
        "startDate": "2023-01-01",
        "endDate": "2023-12-31"
      }
    },
    {
      "id": "ctx-2022",
      "entity": {
        "identifier": {
          "scheme": "http://www.sec.gov/CIK",
          "value": "0001234567"
        },
        "name": "Acme Corporation"
      },
      "period": {
        "startDate": "2022-01-01",
        "endDate": "2022-12-31"
      }
    }
  ],
  "facts": [
    {
      "concept": "esrs:ClimateChangeTransitionPlan",
      "contextRef": "ctx-2023",
      "value": "Acme Corporation is committed to reducing its greenhouse gas emissions by 50% by 2030 compared to a 2020 baseline, and to achieving net-zero emissions by 2050. The company has developed a comprehensive transition plan that includes investments in renewable energy, energy efficiency improvements, and the electrification of its vehicle fleet."
    },
    {
      "concept": "esrs:GhgEmissionsScope1",
      "contextRef": "ctx-2023",
      "value": 25000,
      "unit": "metric-tons",
      "decimals": 0
    },
    {
      "concept": "esrs:GhgEmissionsScope2",
      "contextRef": "ctx-2023",
      "value": 15000,
      "unit": "metric-tons",
      "decimals": 0
    },
    {
      "concept": "esrs:GhgEmissionsScope3",
      "contextRef": "ctx-2023",
      "value": 120000,
      "unit": "metric-tons",
      "decimals": 0
    },
    {
      "concept": "esrs:CorporateGovernanceStructure",
      "contextRef": "ctx-2023-12-31",
      "value": "Acme Corporation's Board of Directors consists of 12 members, including 7 independent directors. The Board has established a Sustainability Committee responsible for overseeing the company's environmental, social, and governance (ESG) strategy and performance."
    }
  ]
}`
