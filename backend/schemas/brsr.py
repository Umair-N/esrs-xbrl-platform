"""
BRSR (Business Responsibility & Sustainability Report) Pydantic Schemas

These schemas define the data structures for BRSR report parsing and XBRL generation.
Compliant with SEBI BRSR framework for Indian listed entities.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import date

# SECTION A: General Disclosures

class ContactPerson(BaseModel):
    """Contact person details parsed from BRSR report"""
    name: str = ""
    phone: str = ""
    email: str = ""


class CompanyDetails(BaseModel):
    """Q1-Q13, Q16: Company identification and basic information"""
    cin: str = Field(default="", description="Corporate Identity Number")
    company_name: str = ""
    incorporation_year: str = ""
    registered_address: str = ""
    corporate_address: str = ""
    contact_person_name: str = ""
    contact_person_phone: str = ""
    contact_person_email: str = ""
    email: str = ""
    telephone: str = ""
    website: str = ""
    financial_year: str = ""
    stock_exchanges: List[str] = Field(default_factory=list)
    paid_up_capital: float = 0
    reporting_boundary: str = ""


class AssuranceData(BaseModel):
    """Q14-Q15: Assurance provider and type details"""
    has_assurance: str = "No"
    provider_name: str = ""
    assurance_type: str = ""
    type_obtained: str = ""  # Full/Partial
    assessors: List[Dict[str, str]] = Field(default_factory=list)
    section_a: str = ""
    section_b: str = ""
    section_c: str = ""


class BusinessActivity(BaseModel):
    """Q17: Business activity details"""
    main_activity: str = ""
    business_activity: str = ""
    turnover_pct: float = 0


class ProductService(BaseModel):
    """Q18: Product/Service details"""
    product: str = ""
    nic_code: str = ""
    turnover_pct: float = 0


class LocationData(BaseModel):
    """Q19: Location of plants and offices"""
    plants: int = 0
    offices: int = 0
    total: int = 0


class Locations(BaseModel):
    """National and international locations"""
    national: LocationData = Field(default_factory=LocationData)
    international: LocationData = Field(default_factory=LocationData)


class Markets(BaseModel):
    """Q20: Markets served"""
    national_states: str = ""
    national_states_count: int = 0  # Number of states
    international_countries: str = ""
    international_countries_count: int = 0  # Number of countries
    export_pct: float = 0
    customer_types_brief: str = ""  # Explanatory text about types of customers


# Employee/Worker Data Structures
class GenderBreakdown(BaseModel):
    """Gender-wise breakdown with counts and percentages"""
    total: int = 0
    male: int = 0
    male_pct: float = 0
    female: int = 0
    female_pct: float = 0
    other: int = 0
    other_pct: float = 0


class EmployeeCategory(BaseModel):
    """Employee/Worker category (permanent, other, total)"""
    permanent: GenderBreakdown = Field(default_factory=GenderBreakdown)
    other: GenderBreakdown = Field(default_factory=GenderBreakdown)
    total: GenderBreakdown = Field(default_factory=GenderBreakdown)


class EmployeesWorkersData(BaseModel):
    """Q21: Complete employees and workers data"""
    employees: EmployeeCategory = Field(default_factory=EmployeeCategory)
    workers: EmployeeCategory = Field(default_factory=EmployeeCategory)
    differently_abled_employees: EmployeeCategory = Field(default_factory=EmployeeCategory)
    differently_abled_workers: EmployeeCategory = Field(default_factory=EmployeeCategory)


class BoardKMPData(BaseModel):
    """Board of Directors and KMP gender representation"""
    total: int = 0
    female: int = 0
    pct: float = 0


class WomenRepresentation(BaseModel):
    """Q22: Participation of women"""
    board: BoardKMPData = Field(default_factory=BoardKMPData)
    kmp: BoardKMPData = Field(default_factory=BoardKMPData)


class TurnoverPeriod(BaseModel):
    """Turnover rates for a specific period"""
    male: float = 0
    female: float = 0
    other: float = 0
    total: float = 0


class TurnoverCategory(BaseModel):
    """Turnover rates across fiscal years"""
    cy: TurnoverPeriod = Field(default_factory=TurnoverPeriod)
    py: TurnoverPeriod = Field(default_factory=TurnoverPeriod)
    ppy: TurnoverPeriod = Field(default_factory=TurnoverPeriod)


class TurnoverRates(BaseModel):
    """Q23: Turnover rates for employees and workers"""
    employees: TurnoverCategory = Field(default_factory=TurnoverCategory)
    workers: TurnoverCategory = Field(default_factory=TurnoverCategory)


# Subsidiaries and CSR

class Subsidiary(BaseModel):
    """Q24: Holding, subsidiary, and associate companies"""
    name: str = ""
    category: str = ""
    shares_pct: float = 0
    participates: str = "No"


class CSRProject(BaseModel):
    """CSR project in aspirational district (Principle 8, Leadership Indicator)"""
    state: str = ""
    aspirational_district: str = ""
    amount_spent: float = 0


class CSRData(BaseModel):
    """Q25: CSR applicability"""
    applicable: str = "Yes"
    turnover: float = 0
    net_worth: float = 0
    aspirational_districts: List['CSRProject'] = Field(default_factory=list, description="CSR projects in aspirational districts")


# Complaints and Material Issues

class Complaint(BaseModel):
    """Q26: Stakeholder complaints/grievances"""
    stakeholder: str = ""
    has_mechanism: str = "No"
    web_link: str = ""
    filed_cy: int = 0
    pending_cy: int = 0
    remarks_cy: str = ""
    filed_py: int = 0
    pending_py: int = 0
    remarks_py: str = ""


class MaterialIssue(BaseModel):
    """Q27: Material responsible business conduct issues"""
    issue: str = ""
    risk_or_opp: str = ""  # R or O
    rationale: str = ""
    mitigation: str = ""
    financial_impact: str = ""



# SECTION B: Management and Process Disclosures


class PrincipleDisclosure(BaseModel):
    """Section B: Policy disclosure for each principle P1-P9"""
    num: int = 0
    policy_covers: str = "Yes"
    board_approved: str = "Yes"
    web_link: str = ""
    translated_to_procedures: str = "Yes"
    extends_to_value_chain: str = "Yes"
    codes_certifications: str = ""
    commitments_goals: str = ""
    performance: str = ""
    # Q10: Review details
    performance_review_by: str = ""  # Who reviews performance
    compliance_review_by: str = ""   # Who reviews compliance
    performance_frequency: str = ""  # How often performance is reviewed
    compliance_frequency: str = ""   # How often compliance is reviewed


class StakeholderEngagement(BaseModel):
    """Principle 4: Stakeholder engagement data"""
    name: str = Field(default="", description="Name of stakeholder group (e.g., Suppliers, Employees, Community)")
    vulnerable_marginalized: str = Field(default="false", description="Whether identified as vulnerable/marginalized group (true/false)")
    channels: str = Field(default="Other", description="Channels of communication (Email, SMS, Newspaper, Pamphlets, Advertisement, Community Meetings, etc.)")
    channels_details: str = Field(default="", description="Details of other channels of communication")
    frequency: str = Field(default="Quarterly", description="Frequency of engagement (Annually, Half yearly, Quarterly, More than once a quarter, Others)")
    frequency_details: str = Field(default="", description="Details if frequency is 'Others'")
    purpose_scope: str = Field(default="", description="Purpose and scope of engagement including key topics and concerns")


class ParentalLeaveGender(BaseModel):
    """Parental leave data for a gender category"""
    emp_return: float = Field(default=0, description="Return to work rate for permanent employees")
    emp_retention: float = Field(default=0, description="Retention rate for permanent employees")
    worker_return: float = Field(default=0, description="Return to work rate for permanent workers")
    worker_retention: float = Field(default=0, description="Retention rate for permanent workers")


class ParentalLeaveData(BaseModel):
    """Parental leave return-to-work and retention rates"""
    male: ParentalLeaveGender = Field(default_factory=ParentalLeaveGender)
    female: ParentalLeaveGender = Field(default_factory=ParentalLeaveGender)
    others: ParentalLeaveGender = Field(default_factory=ParentalLeaveGender)
    total: ParentalLeaveGender = Field(default_factory=ParentalLeaveGender)


class RetirementBenefitItem(BaseModel):
    """Retirement benefit data for a single benefit type (PF, Gratuity, ESI)"""
    emp_cy: float = Field(default=0, description="No. of employees covered as % of total employees - Current Year")
    worker_cy: float = Field(default=0, description="No. of workers covered as % of total workers - Current Year")
    deposited_cy: str = Field(default="N", description="Deducted and deposited with authority - Current Year (Y/N)")
    emp_py: float = Field(default=0, description="No. of employees covered as % of total employees - Previous Year")
    worker_py: float = Field(default=0, description="No. of workers covered as % of total workers - Previous Year")
    deposited_py: str = Field(default="N", description="Deducted and deposited with authority - Previous Year (Y/N)")


class OtherRetirementBenefitItem(BaseModel):
    """Retirement benefit data for 'Others' category with name field"""
    name_cy: str = Field(default="NA", description="Name of the other retirement benefit - Current Year")
    emp_cy: float = Field(default=0, description="No. of employees covered as % of total employees - Current Year")
    worker_cy: float = Field(default=0, description="No. of workers covered as % of total workers - Current Year")
    deposited_cy: str = Field(default="NA", description="Deducted and deposited with authority - Current Year")
    name_py: str = Field(default="NA", description="Name of the other retirement benefit - Previous Year")
    emp_py: float = Field(default=0, description="No. of employees covered as % of total employees - Previous Year")
    worker_py: float = Field(default=0, description="No. of workers covered as % of total workers - Previous Year")
    deposited_py: str = Field(default="NA", description="Deducted and deposited with authority - Previous Year")


class RetirementBenefitsData(BaseModel):
    """Principle 3: Retirement benefits coverage (PF, Gratuity, ESI, Others)"""
    pf: RetirementBenefitItem = Field(default_factory=RetirementBenefitItem)
    gratuity: RetirementBenefitItem = Field(default_factory=RetirementBenefitItem)
    esi: RetirementBenefitItem = Field(default_factory=RetirementBenefitItem)
    others: OtherRetirementBenefitItem = Field(default_factory=OtherRetirementBenefitItem)


# SECTION C: Principle-wise Performance

class HRTrainingCategory(BaseModel):
    """Human rights training data for a category"""
    total_cy: int = 0
    covered_cy: int = 0
    pct_cy: float = 0
    total_py: int = 0
    covered_py: int = 0
    pct_py: float = 0


class HRTraining(BaseModel):
    """Principle 5: Human rights training coverage"""
    permanent_employees: HRTrainingCategory = Field(default_factory=HRTrainingCategory)
    other_employees: HRTrainingCategory = Field(default_factory=HRTrainingCategory)
    total_employees: HRTrainingCategory = Field(default_factory=HRTrainingCategory)
    permanent_workers: HRTrainingCategory = Field(default_factory=HRTrainingCategory)
    other_workers: HRTrainingCategory = Field(default_factory=HRTrainingCategory)
    total_workers: HRTrainingCategory = Field(default_factory=HRTrainingCategory)


class MinimumWageGenderData(BaseModel):
    """Minimum wage compliance data for a single gender"""
    total_cy: int = 0
    equal_cy: int = 0
    equal_pct_cy: float = 0
    more_cy: int = 0
    more_pct_cy: float = 0
    total_py: int = 0
    equal_py: int = 0
    equal_pct_py: float = 0
    more_py: int = 0
    more_pct_py: float = 0


class MinimumWageCategoryData(BaseModel):
    """Minimum wage data for a category (Perm Emp/Other Emp/Perm Workers/Other Workers)"""
    male: MinimumWageGenderData = Field(default_factory=MinimumWageGenderData)
    female: MinimumWageGenderData = Field(default_factory=MinimumWageGenderData)
    other: MinimumWageGenderData = Field(default_factory=MinimumWageGenderData)
    total: MinimumWageGenderData = Field(default_factory=MinimumWageGenderData)


class MinimumWagesData(BaseModel):
    """Complete minimum wage compliance data for all categories"""
    perm_emp: MinimumWageCategoryData = Field(default_factory=MinimumWageCategoryData)
    other_emp: MinimumWageCategoryData = Field(default_factory=MinimumWageCategoryData)
    perm_workers: MinimumWageCategoryData = Field(default_factory=MinimumWageCategoryData)
    other_workers: MinimumWageCategoryData = Field(default_factory=MinimumWageCategoryData)


class MedianRemuneration(BaseModel):
    """Median remuneration by gender"""
    male_num: int = 0
    male_median: float = 0
    female_num: int = 0
    female_median: float = 0
    other_num: int = 0
    other_median: float = 0


class GrossWages(BaseModel):
    """Gross wages paid to females"""
    female_cy: float = 0
    female_py: float = 0
    total_cy: float = 0
    total_py: float = 0
    female_pct_cy: float = 0
    female_pct_py: float = 0

    # Average female employee/worker counts (for Principle 5)
    # Average = (Beginning of year + End of year) / 2
    # Beginning of CY = End of PY, so Average CY = (PY_female + CY_female) / 2
    avg_female_emp_workers_cy: float = 0  # Average for current year
    avg_female_emp_workers_py: float = 0  # Average for previous year
    female_emp_workers_cy: int = 0  # Female employees+workers at end of CY
    female_emp_workers_py: int = 0  # Female employees+workers at end of PY


class WasteCategory(BaseModel):
    """Waste management data for a category"""
    reused: float = 0
    recycled: float = 0
    disposed: float = 0


class WasteData(BaseModel):
    """Waste reclamation data"""
    plastics_cy: WasteCategory = Field(default_factory=WasteCategory)
    plastics_py: WasteCategory = Field(default_factory=WasteCategory)
    ewaste_cy: WasteCategory = Field(default_factory=WasteCategory)
    ewaste_py: WasteCategory = Field(default_factory=WasteCategory)
    hazardous_cy: WasteCategory = Field(default_factory=WasteCategory)
    hazardous_py: WasteCategory = Field(default_factory=WasteCategory)
    other_cy: WasteCategory = Field(default_factory=WasteCategory)
    other_py: WasteCategory = Field(default_factory=WasteCategory)


class RecycledInput(BaseModel):
    """Recycled input material data"""
    material: str = ""
    percentage: float = 0


class ReclaimedProduct(BaseModel):
    """Reclaimed products and packaging"""
    category: str = ""
    percentage: float = 0


class EnergyData(BaseModel):
    """Energy consumption data for Principle 6"""
    # Renewable sources (in GJ)
    elec_renewable_cy: float = 0
    elec_renewable_py: float = 0
    fuel_renewable_cy: float = 0
    fuel_renewable_py: float = 0
    other_renewable_cy: float = 0
    other_renewable_py: float = 0
    other_renewable_name_cy: str = ""  # Name/description of other renewable source
    other_renewable_name_py: str = ""  # Name/description of other renewable source PY
    total_renewable_cy: float = 0
    total_renewable_py: float = 0

    # Non-renewable sources (in GJ)
    elec_nonrenewable_cy: float = 0
    elec_nonrenewable_py: float = 0
    fuel_nonrenewable_cy: float = 0
    fuel_nonrenewable_py: float = 0
    other_nonrenewable_cy: float = 0
    other_nonrenewable_py: float = 0
    other_nonrenewable_name_cy: str = ""  # Name/description of other non-renewable source
    other_nonrenewable_name_py: str = ""  # Name/description of other non-renewable source PY
    total_nonrenewable_cy: float = 0
    total_nonrenewable_py: float = 0

    # Totals
    total_energy_cy: float = 0
    total_energy_py: float = 0

    # Intensity
    intensity_turnover_cy: float = 0
    intensity_turnover_py: float = 0
    intensity_turnover_ppp_cy: float = 0  # Purchasing Power Parity adjusted
    intensity_turnover_ppp_py: float = 0
    intensity_physical_cy: float = 0
    intensity_physical_py: float = 0
    intensity_optional_cy: float = 0
    intensity_optional_py: float = 0

    # External assessment
    external_assessment: str = "No"  # Yes/No
    external_agency: str = ""

    # PAT scheme
    pat_applicable: str = "No"  # Yes/No
    pat_details: str = ""

    # Low/zero carbon sites
    low_carbon_sites: str = "No"  # Yes/No
    low_carbon_details: str = ""


class WaterData(BaseModel):
    """Water-related environmental data including ZLD"""
    # Zero Liquid Discharge
    has_zld: str = "No"  # Yes/No
    zld_details: str = ""  # Detailed explanation text

    # Water withdrawal (in kilolitres)
    surface_water_cy: float = 0
    surface_water_py: float = 0
    groundwater_cy: float = 0
    groundwater_py: float = 0
    third_party_cy: float = 0
    third_party_py: float = 0
    seawater_cy: float = 0
    seawater_py: float = 0
    others_cy: float = 0
    others_py: float = 0
    total_withdrawal_cy: float = 0
    total_withdrawal_py: float = 0

    # Water consumption
    total_consumption_cy: float = 0
    total_consumption_py: float = 0

    # Water intensity
    intensity_turnover_cy: float = 0
    intensity_turnover_py: float = 0
    intensity_physical_cy: float = 0
    intensity_physical_py: float = 0

    # Water discharge by destination
    total_discharge_cy: float = 0
    total_discharge_py: float = 0
    # Surface water discharge
    discharge_surface_cy: float = 0
    discharge_surface_py: float = 0
    discharge_surface_no_treatment_cy: float = 0
    discharge_surface_no_treatment_py: float = 0
    discharge_surface_with_treatment_cy: float = 0
    discharge_surface_with_treatment_py: float = 0
    # Groundwater discharge
    discharge_groundwater_cy: float = 0
    discharge_groundwater_py: float = 0
    discharge_groundwater_no_treatment_cy: float = 0
    discharge_groundwater_no_treatment_py: float = 0
    discharge_groundwater_with_treatment_cy: float = 0
    discharge_groundwater_with_treatment_py: float = 0
    # Seawater discharge
    discharge_seawater_cy: float = 0
    discharge_seawater_py: float = 0
    discharge_seawater_no_treatment_cy: float = 0
    discharge_seawater_no_treatment_py: float = 0
    discharge_seawater_with_treatment_cy: float = 0
    discharge_seawater_with_treatment_py: float = 0
    # Third party discharge
    discharge_thirdparty_cy: float = 0
    discharge_thirdparty_py: float = 0
    discharge_thirdparty_no_treatment_cy: float = 0
    discharge_thirdparty_no_treatment_py: float = 0
    discharge_thirdparty_with_treatment_cy: float = 0
    discharge_thirdparty_with_treatment_py: float = 0
    # Others discharge
    discharge_others_cy: float = 0
    discharge_others_py: float = 0
    discharge_others_no_treatment_cy: float = 0
    discharge_others_no_treatment_py: float = 0
    discharge_others_with_treatment_cy: float = 0
    discharge_others_with_treatment_py: float = 0
    # External assessment for water withdrawal
    external_assessment: str = "No"
    external_agency: str = ""
    # External assessment for water discharge
    discharge_external_assessment: str = "No"
    discharge_external_agency: str = ""


class GHGData(BaseModel):
    """Greenhouse Gas emissions data (Scope 1 and Scope 2)"""
    # Scope 1 emissions (tCO2e)
    scope1_cy: float = 0
    scope1_py: float = 0
    # Scope 2 emissions (tCO2e)
    scope2_cy: float = 0
    scope2_py: float = 0
    # Total (Scope 1 + Scope 2)
    total_cy: float = 0
    total_py: float = 0
    # Intensity per rupee of turnover
    intensity_turnover_cy: float = 0
    intensity_turnover_py: float = 0
    # Intensity per rupee of turnover (PPP adjusted)
    intensity_turnover_ppp_cy: float = 0
    intensity_turnover_ppp_py: float = 0
    # Intensity in terms of physical output
    intensity_physical_cy: float = 0
    intensity_physical_py: float = 0
    # Optional intensity metric
    intensity_optional_cy: float = 0
    intensity_optional_py: float = 0
    # External assessment
    external_assessment: str = "No"
    external_agency: str = ""
    # GHG reduction projects
    has_reduction_project: str = "No"
    reduction_project_details: str = ""
    reduction_project_na_explanation: str = ""  # Explanation when not applicable


class UnionMembershipCategory(BaseModel):
    """Union membership data for a category (by gender)"""
    total_cy: int = 0
    total_py: int = 0
    members_cy: int = 0
    members_py: int = 0
    pct_cy: float = 0
    pct_py: float = 0


class UnionMembershipData(BaseModel):
    """Membership of employees and workers in associations/unions"""
    # Permanent Employees
    permanent_employees_total: UnionMembershipCategory = Field(default_factory=UnionMembershipCategory)
    permanent_employees_male: UnionMembershipCategory = Field(default_factory=UnionMembershipCategory)
    permanent_employees_female: UnionMembershipCategory = Field(default_factory=UnionMembershipCategory)
    permanent_employees_other: UnionMembershipCategory = Field(default_factory=UnionMembershipCategory)
    # Permanent Workers
    permanent_workers_total: UnionMembershipCategory = Field(default_factory=UnionMembershipCategory)
    permanent_workers_male: UnionMembershipCategory = Field(default_factory=UnionMembershipCategory)
    permanent_workers_female: UnionMembershipCategory = Field(default_factory=UnionMembershipCategory)
    permanent_workers_other: UnionMembershipCategory = Field(default_factory=UnionMembershipCategory)


class SustainabilityData(BaseModel):
    """Sustainability-related metrics"""
    rd_cy: float = 0
    rd_py: float = 0
    rd_improvements: str = ""
    capex_cy: float = 0
    capex_py: float = 0
    capex_improvements: str = ""
    epr_applicable: str = "No"
    lca_conducted: str = "No"
    lca_product_count: int = 0
    lca_percentage_cy: float = 0
    lca_percentage_py: float = 0
    sustainable_sourcing_pct: float = 0
    recycled_input_cy: RecycledInput = Field(default_factory=RecycledInput)
    recycled_input_py: RecycledInput = Field(default_factory=RecycledInput)
    reclaimed_products: List[ReclaimedProduct] = Field(default_factory=list)


class AccountsPayableData(BaseModel):
    """Accounts payable and trading data"""
    days_payable_cy: str = "P0D"
    days_payable_py: str = "P0D"
    trading_purchases_pct_cy: float = 0
    trading_purchases_pct_py: float = 0
    num_trading_houses_cy: int = 0
    num_trading_houses_py: int = 0
    top10_trading_pct_cy: float = 0
    top10_trading_pct_py: float = 0
    dealer_sales_pct_cy: float = 0
    dealer_sales_pct_py: float = 0
    num_dealers_cy: int = 0
    num_dealers_py: int = 0
    top10_dealer_pct_cy: float = 0
    top10_dealer_pct_py: float = 0


class GrievanceMechanismData(BaseModel):
    """Grievance mechanism data for employees and workers (Principle 3 Q6)"""
    # General mechanism availability
    has_mechanism: str = "true"
    # By category - availability (Yes/No)
    permanent_employees: str = "Yes"
    other_employees: str = "Yes"
    permanent_workers: str = "Yes"
    other_workers: str = "Yes"
    # Details for each category
    permanent_employees_details: str = ""
    other_employees_details: str = ""
    permanent_workers_details: str = ""
    other_workers_details: str = ""

# Complete BRSR Report Data

class BRSRReportData(BaseModel):
    """Complete BRSR report data structure"""
    # Section A: General Disclosures
    company: CompanyDetails = Field(default_factory=CompanyDetails)
    assurance: AssuranceData = Field(default_factory=AssuranceData)
    business_activities: List[BusinessActivity] = Field(default_factory=list)
    products_services: List[ProductService] = Field(default_factory=list)
    locations: Locations = Field(default_factory=Locations)
    markets: Markets = Field(default_factory=Markets)
    employees_workers: EmployeesWorkersData = Field(default_factory=EmployeesWorkersData)
    women_representation: WomenRepresentation = Field(default_factory=WomenRepresentation)
    turnover_rates: TurnoverRates = Field(default_factory=TurnoverRates)
    subsidiaries: List[Subsidiary] = Field(default_factory=list)
    csr: CSRData = Field(default_factory=CSRData)
    complaints: List[Complaint] = Field(default_factory=list)
    material_issues: List[MaterialIssue] = Field(default_factory=list)

    # Section B: Management and Process Disclosures
    principles: List[PrincipleDisclosure] = Field(default_factory=list)

    # Section B: Governance, Leadership and Oversight
    director_statement: str = Field(default="", description="Q7. Statement by director responsible for BR report")
    highest_authority: str = Field(default="", description="Q8. Details of highest authority for BR policy implementation")
    has_specific_committee: str = Field(default="No", description="Q9. Whether specific committee for BR/sustainability issues")
    specific_committee_details: str = Field(default="", description="Q9. Details of BR/sustainability committee")

    # Principle 4: Stakeholder Engagement
    stakeholder_groups: List[StakeholderEngagement] = Field(default_factory=list, description="List of stakeholder engagement data")
    stakeholder_identification_process: str = Field(default="", description="Process for identifying key stakeholder groups")
    stakeholder_consultation_process: str = Field(default="", description="Process for consultation between stakeholders and board")
    stakeholder_consultation_used: str = Field(default="Yes", description="Whether stakeholder consultation is used")
    stakeholder_consultation_details: str = Field(default="", description="Details of how stakeholder inputs were incorporated")
    vulnerable_marginalized_actions: str = Field(default="", description="Actions taken to address concerns of vulnerable/marginalized groups")

    # Section C: Principle-wise Performance
    hr_training: HRTraining = Field(default_factory=HRTraining)
    sustainability: SustainabilityData = Field(default_factory=SustainabilityData)
    accounts_payable: AccountsPayableData = Field(default_factory=AccountsPayableData)
    waste: WasteData = Field(default_factory=WasteData)
    gross_wages: GrossWages = Field(default_factory=GrossWages)
    water: WaterData = Field(default_factory=WaterData)
    energy: EnergyData = Field(default_factory=EnergyData)
    ghg: GHGData = Field(default_factory=GHGData)
    union_membership: UnionMembershipData = Field(default_factory=UnionMembershipData)
    grievance_mechanism: GrievanceMechanismData = Field(default_factory=GrievanceMechanismData, description="Grievance mechanism for employees and workers (P3 Q6)")

    # Principle 3 - Employee Safety (Q12, Q15)
    safe_workplace_measures: str = Field(default="", description="Measures for safe and healthy workplace (P3 Q12)")
    corrective_actions_safety: str = Field(default="", description="Corrective actions for safety-related incidents (P3 Q15)")

    # Principle 6 - Revenue from Operations (for intensity calculations)
    revenue_from_operations_cy: float = Field(default=0, description="Revenue from operations - Current Year (INR)")
    revenue_from_operations_py: float = Field(default=0, description="Revenue from operations - Previous Year (INR)")

    # Principle 9 - Q6: Corrective Actions
    corrective_actions_p9_q6: str = Field(default="", description="Corrective actions on advertising, cyber security, recalls, regulatory penalties (P9 Q6)")

    # Principle 9 - Complete P9 data extraction
    p9_data: dict = Field(default_factory=dict, description="Complete Principle 9 extracted data including complaints, cyber security, product info")

    # Principle 7 - Trade and Industry Chamber Affiliations
    p7_data: dict = Field(default_factory=dict, description="Principle 7 data including trade/industry chamber affiliations")

    # Principle 3 - Parental Leave Return/Retention Rates
    parental_leave: ParentalLeaveData = Field(default_factory=ParentalLeaveData, description="Parental leave return-to-work and retention rates by gender")

    # Principle 3 - Retirement Benefits (PF, Gratuity, ESI, Others)
    retirement_benefits: RetirementBenefitsData = Field(default_factory=RetirementBenefitsData, description="Retirement benefits coverage for employees and workers")

    # Principle 3 - Employee/Worker Wellbeing Measures (Table 1.a and 1.b)
    employee_wellbeing_data: dict = Field(default_factory=dict, description="Employee and worker wellbeing measures (health insurance, accident insurance, maternity/paternity benefits, day care)")

    # Principle 3 - Performance and Career Development (Section 9)
    performance_career_data: dict = Field(default_factory=dict, description="Performance and career development reviews data for employees and workers")

    # Principle 3 - Safety Incidents (Section 11)
    safety_incidents_data: dict = Field(default_factory=dict, description="Safety related incidents data (LTIFR, injuries, fatalities, high consequence)")

    # Principle 5 - Minimum Wages Compliance
    minimum_wages: MinimumWagesData = Field(default_factory=MinimumWagesData, description="Minimum wages compliance data by category and gender")


# API Request/Response Models

class BRSRConversionRequest(BaseModel):
    """Request model for BRSR HTML to XBRL conversion"""
    html_content: Optional[str] = Field(None, description="HTML content as string")
    file_path: Optional[str] = Field(None, description="Path to HTML file")
    output_format: str = Field(default="xml", description="Output format: xml or json")
    include_mapping: bool = Field(default=False, description="Include cell-to-tag mapping data")

    # Reporting period configuration
    reporting_period_start: Optional[date] = None
    reporting_period_end: Optional[date] = None


class BRSRConversionResponse(BaseModel):
    """Response model for BRSR conversion"""
    success: bool = True
    message: str = ""
    xbrl_content: Optional[str] = None
    report_data: Optional[BRSRReportData] = None
    mapping_data: Optional[Dict[str, Any]] = None
    statistics: Dict[str, Any] = Field(default_factory=dict)


class BRSRValidationResult(BaseModel):
    """Validation result for BRSR report"""
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    sections_found: List[str] = Field(default_factory=list)
    table_count: int = 0


# Interactive Viewer Schemas

class TagInfo(BaseModel):
    """Single tag information for a data point"""
    tag: str = Field(..., description="XBRL tag name (e.g., in-capmkt:CorporateIdentityNumber)")
    value: str = Field(..., description="The value in the XML")
    context: str = Field(default="", description="Context ID reference")
    period: Optional[str] = Field(default=None, description="Period description")
    unit: Optional[str] = Field(default=None, description="Unit if numeric")
    dimensions: List[str] = Field(default_factory=list, description="Dimensional members")
    source: Optional[str] = Field(default=None, description="Source section/question")
    editable: bool = Field(default=True, description="Whether this tag can be edited")


class TagMapping(BaseModel):
    """Mapping of cell IDs to their tag information"""
    mapping: Dict[str, List[TagInfo]] = Field(
        default_factory=dict,
        description="Dictionary mapping cell data-id to list of tags"
    )
    total_cells: int = Field(default=0, description="Total number of tagged cells")
    total_tags: int = Field(default=0, description="Total number of tags")


class InteractiveConversionResponse(BaseModel):
    """Response model for interactive BRSR conversion"""
    success: bool = True
    message: str = ""
    annotated_html: str = Field(default="", description="HTML with data-id attributes on tagged cells")
    tag_mapping: Dict[str, List[Dict[str, Any]]] = Field(
        default_factory=dict,
        description="Mapping of cell IDs to tag information"
    )
    xbrl_content: Optional[str] = Field(default=None, description="Generated XBRL XML")
    report_data: Optional[BRSRReportData] = None
    statistics: Dict[str, Any] = Field(default_factory=dict)


class TagUpdateRequest(BaseModel):
    """Request to update tags in the XBRL output"""
    original_xbrl: str = Field(..., description="Original XBRL content")
    updates: List[Dict[str, Any]] = Field(
        ...,
        description="List of updates: [{cell_id, tag, old_value, new_value}]"
    )


class TagUpdateResponse(BaseModel):
    """Response after updating tags"""
    success: bool = True
    message: str = ""
    updated_xbrl: str = Field(default="", description="Updated XBRL content")
    changes_applied: int = Field(default=0, description="Number of changes applied")
