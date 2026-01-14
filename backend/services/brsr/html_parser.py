"""
BRSR HTML Parser Service

Extracts structured data from BRSR (Business Responsibility & Sustainability Report) HTML files.
Supports SEBI BRSR format for Indian listed entities.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from bs4 import BeautifulSoup, Tag

from schemas.brsr import (
    BRSRReportData,
    CompanyDetails,
    AssuranceData,
    BusinessActivity,
    ProductService,
    Locations,
    LocationData,
    Markets,
    EmployeesWorkersData,
    EmployeeCategory,
    GenderBreakdown,
    WomenRepresentation,
    BoardKMPData,
    TurnoverRates,
    TurnoverCategory,
    TurnoverPeriod,
    Subsidiary,
    CSRData,
    CSRProject,
    Complaint,
    MaterialIssue,
    PrincipleDisclosure,
    StakeholderEngagement,
    ParentalLeaveData,
    ParentalLeaveGender,
    HRTraining,
    HRTrainingCategory,
    SustainabilityData,
    RecycledInput,
    ReclaimedProduct,
    AccountsPayableData,
    WasteData,
    WasteCategory,
    WaterData,
    EnergyData,
    GHGData,
    UnionMembershipData,
    UnionMembershipCategory,
    GrossWages,
    MinimumWagesData,
    MinimumWageCategoryData,
    MinimumWageGenderData,
    RetirementBenefitsData,
    RetirementBenefitItem,
    OtherRetirementBenefitItem,
    BRSRValidationResult,
    SafetySkillTraining,
    SafetySkillTrainingCategory,
    SafetySkillTrainingGender,
    GrievanceMechanismData,
)

logger = logging.getLogger(__name__)


class BRSRHTMLParser:
    """
    Parser for BRSR HTML reports.

    Extracts data from all sections:
    - Section A: General Disclosures (Q1-Q27)
    - Section B: Management and Process Disclosures (P1-P9)
    - Section C: Principle-wise Performance Disclosure
    """

    # Stakeholder mapping for complaints section
    STAKEHOLDER_MAPPING = {
        'communities': 'Communities',
        'investors': 'Investors',
        'shareholders': 'Shareholders',
        'employees': 'EmployeesAndWorkers',
        'workers': 'EmployeesAndWorkers',
        'customers': 'Customers',
        'value chain': 'ValueChainPartners',
        'other': 'Other'
    }

    def __init__(self, html_content: str):
        """
        Initialize parser with HTML content.

        Args:
            html_content: Raw HTML string of BRSR report
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self._tables = self.soup.find_all('table')
        logger.info(f"Initialized BRSR parser with {len(self._tables)} tables")

    # =========================================================================
    # Utility Methods
    # =========================================================================

    @staticmethod
    def clean_text(text: Optional[str]) -> str:
        """Clean and normalize text, escape XML special characters."""
        if text is None:
            return ''
        text = re.sub(r'\s+', ' ', str(text)).strip()
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        text = text.replace('"', '&quot;').replace("'", '&apos;')
        return text

    @staticmethod
    def clean_number(text: Optional[str]) -> float:
        """Extract numeric value from text."""
        if text is None or text == '' or text == '-':
            return 0
        text_upper = str(text).upper()
        if text_upper in ('NA', 'NIL', 'N/A', '-'):
            return 0
        text = re.sub(r'[₹$,\s%]', '', str(text))
        text = text.replace('crores', '').replace('crore', '').strip()
        try:
            return float(text)
        except ValueError:
            return 0

    @staticmethod
    def clean_percentage(text: Optional[str]) -> float:
        """Extract percentage as decimal (0-1 range)."""
        if text is None or text == '' or text == '-':
            return 0
        text_upper = str(text).upper()
        if text_upper in ('NA', 'NIL', 'N/A'):
            return 0
        text = str(text).replace('%', '').strip()
        try:
            value = float(text)
            if value > 1:
                return value / 100
            return value
        except ValueError:
            return 0

    def extract_table_data(self, table: Tag) -> List[List[str]]:
        """Extract table data as list of lists."""
        rows = []
        for tr in table.find_all('tr'):
            row = [self.clean_text(cell.get_text()) for cell in tr.find_all(['td', 'th'])]
            if row:
                rows.append(row)
        return rows

    def find_table_by_header(self, *keywords: str) -> Optional[Tag]:
        """Find table containing all keywords in headers."""
        for table in self._tables:
            headers = ' '.join([th.get_text().lower() for th in table.find_all('th')])
            if all(kw.lower() in headers for kw in keywords):
                return table
        return None

    @staticmethod
    def normalize_stock_exchange(name: str) -> str:
        """Convert stock exchange full names to short forms."""
        name_lower = name.lower()
        if 'national stock exchange' in name_lower or 'nse' in name_lower:
            return 'NSE'
        elif 'bombay stock exchange' in name_lower or 'bse' in name_lower:
            return 'BSE'
        elif 'calcutta' in name_lower or 'cse' in name_lower:
            return 'CSE'
        elif 'metropolitan' in name_lower or 'mse' in name_lower:
            return 'MSE'
        return name

    @staticmethod
    def parse_contact_person(contact_str: str) -> Dict[str, str]:
        """Parse contact person details into separate fields."""
        data = {'name': '', 'phone': '', 'email': ''}
        if not contact_str:
            return data

        name_match = re.search(r'Name[:\s]*([^,\n\-]+)', contact_str, re.I)
        if name_match:
            data['name'] = name_match.group(1).strip()

        phone_match = re.search(r'(?:Contact|Phone|Tel|Telephone)[:\s]*([+\d\s\-\/()]+)', contact_str, re.I)
        if phone_match:
            phone = re.sub(r'[^\d+]', '', phone_match.group(1))
            data['phone'] = phone

        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', contact_str)
        if email_match:
            data['email'] = email_match.group(0)

        return data

    # =========================================================================
    # Section A: General Disclosures Extraction
    # =========================================================================

    def extract_company_details(self) -> CompanyDetails:
        """Extract Q1-Q13, Q16: Company Details."""
        data = CompanyDetails()

        if not self._tables:
            return data

        for row in self.extract_table_data(self._tables[0]):
            if len(row) < 2:
                continue

            q = row[0].lower()
            a = row[1]

            if 'corporate identity' in q or 'cin' in q:
                data.cin = a
            elif 'name of the listed entity' in q:
                data.company_name = a
            elif 'year of incorporation' in q:
                data.incorporation_year = a
            elif 'registered office address' in q:
                data.registered_address = a
            elif 'corporate address' in q:
                data.corporate_address = a
            elif 'name and contact details' in q or 'person who may be contacted' in q:
                contact = self.parse_contact_person(a)
                data.contact_person_name = contact['name']
                data.contact_person_phone = contact['phone']
                data.contact_person_email = contact['email']
            elif 'e-mail' in q and 'contact details' not in q:
                data.email = a
            elif 'telephone' in q and 'contact details' not in q:
                data.telephone = a
            elif 'website' in q:
                data.website = a
            elif 'financial year' in q:
                data.financial_year = a
            elif 'stock exchange' in q:
                exchanges = [e.strip() for e in a.replace(';', '\n').split('\n') if e.strip()]
                data.stock_exchanges = [self.normalize_stock_exchange(ex) for ex in exchanges]
            elif 'paid-up capital' in q:
                data.paid_up_capital = self.clean_number(a)
            elif 'reporting boundary' in q:
                data.reporting_boundary = a

        return data

    def extract_assurance_data(self) -> AssuranceData:
        """Extract Q14-Q15: Assurance provider and assessment details."""
        assurance = AssuranceData()

        for table in self._tables:
            for tr in table.find_all('tr'):
                cells = tr.find_all(['td', 'th'])
                if len(cells) < 2:
                    continue

                q = self.clean_text(cells[0].get_text()).lower()
                a = self.clean_text(cells[1].get_text())

                if 'name of assurance provider' in q:
                    assurance.provider_name = a
                    if a and a.lower() not in ['na', 'nil', '-', 'not applicable', '']:
                        assurance.has_assurance = 'Yes'
                elif 'type of assurance' in q:
                    assurance.assurance_type = a
                    if a:
                        a_lower = a.lower()
                        if 'full' in a_lower:
                            assurance.type_obtained = 'Full'
                        else:
                            assurance.type_obtained = 'Partial'

        # Extract assessor details
        for table in self._tables:
            table_text = table.get_text().lower()
            if ('assessor' in table_text or 'assurer' in table_text) and 'designation' in table_text:
                rows = table.find_all('tr')
                header_found = False

                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    cell_texts = [self.clean_text(c.get_text()) for c in cells]

                    if any('name of' in t.lower() and 'company' in t.lower() for t in cell_texts):
                        header_found = True
                        continue

                    if header_found and len(cells) >= 4:
                        assessor = {
                            'company_name': cell_texts[0] if len(cell_texts) > 0 else '',
                            'company_id': cell_texts[1] if len(cell_texts) > 1 else '',
                            'assessor_name': cell_texts[2] if len(cell_texts) > 2 else '',
                            'designation': cell_texts[3] if len(cell_texts) > 3 else '',
                            'date_of_signing': cell_texts[4] if len(cell_texts) > 4 else ''
                        }
                        if assessor['assessor_name'] and len(assessor['assessor_name']) > 2:
                            assurance.assessors.append(assessor)

        # Extract section-wise assurance
        for table in self._tables:
            for tr in table.find_all('tr'):
                cells = tr.find_all(['td', 'th'])
                if len(cells) >= 2:
                    section = self.clean_text(cells[0].get_text()).lower()
                    value = self.clean_text(cells[1].get_text())

                    if 'section a' in section and 'general' in section:
                        assurance.section_a = value
                    elif 'section b' in section and 'management' in section:
                        assurance.section_b = value
                    elif 'section c' in section and 'principle' in section:
                        assurance.section_c = value

        return assurance

    def extract_business_activities(self) -> List[BusinessActivity]:
        """Extract Q17: Business Activities."""
        activities = []
        table = self.find_table_by_header('description of main activity')

        if table:
            for row in self.extract_table_data(table)[1:]:
                if len(row) >= 4 and row[0].isdigit():
                    activities.append(BusinessActivity(
                        main_activity=row[1],
                        business_activity=row[2],
                        turnover_pct=self.clean_percentage(row[3])
                    ))

        return activities

    def extract_products_services(self) -> List[ProductService]:
        """Extract Q18: Products/Services."""
        products = []

        # Try multiple detection strategies
        table = None

        # Strategy 1: Look for "NIC Code" in headers
        table = self.find_table_by_header('nic code')

        # Strategy 2: Search for table containing product/service + nic + turnover keywords
        if not table:
            for tbl in self._tables:
                all_text = tbl.get_text().lower()
                # Check if table contains relevant keywords
                has_product = 'product' in all_text or 'service' in all_text
                has_nic = 'nic' in all_text
                has_turnover = 'turnover' in all_text or '%' in all_text

                # Look for the specific section marker
                if has_product and has_nic and has_turnover:
                    # Check if it's near "18." or contains "sold by the entity"
                    if '18.' in all_text or 'sold by the entity' in all_text:
                        table = tbl
                        logger.debug("Found products/services table using fallback detection")
                        break

        if table:
            rows = self.extract_table_data(table)
            for row in rows[1:]:  # Skip header row
                if len(row) >= 4:
                    # More flexible detection: check if first column looks like a serial number
                    first_col = row[0].strip()
                    if first_col.isdigit() or re.match(r'^\d+\.?$', first_col):
                        products.append(ProductService(
                            product=row[1],
                            nic_code=row[2],
                            turnover_pct=self.clean_percentage(row[3])
                        ))

        logger.info(f"Extracted {len(products)} products/services")
        return products

    def extract_locations(self) -> Locations:
        """Extract Q19: Location of plants and offices."""
        data = Locations()
        table = self.find_table_by_header('number of plants', 'number of offices')

        if table:
            for row in self.extract_table_data(table):
                if len(row) >= 3:
                    loc = row[0].lower()
                    if 'national' in loc and 'international' not in loc:
                        plants = int(self.clean_number(row[1]))
                        offices = int(self.clean_number(row[2]))
                        total = int(self.clean_number(row[3])) if len(row) > 3 else plants + offices
                        data.national = LocationData(
                            plants=plants,
                            offices=offices,
                            total=total
                        )
                    elif 'international' in loc:
                        plants = int(self.clean_number(row[1]))
                        offices = int(self.clean_number(row[2]))
                        total = int(self.clean_number(row[3])) if len(row) > 3 else plants + offices
                        data.international = LocationData(
                            plants=plants,
                            offices=offices,
                            total=total
                        )

        return data

    def extract_markets(self) -> Markets:
        """Extract Q20: Markets served."""
        data = Markets()

        # Find markets table for states/countries
        # Q20 is about "Markets served" - NOT "Locations" (which is Q19)
        # Q20 mentions "states" and "countries", Q19 mentions "plants" and "offices"
        for table in self._tables:
            rows = self.extract_table_data(table)
            table_text = ' '.join([' '.join(r) for r in rows]).lower()

            # Look for markets table (Q20) - must have "states" AND not have "plants"/"offices"
            # This distinguishes Q20 (markets) from Q19 (locations)
            if ('states' in table_text or 'countries' in table_text) and \
               not ('plants' in table_text or 'offices' in table_text):
                logger.debug(f"Found potential Q20 markets table: {table_text[:100]}")

                for row in rows:
                    if len(row) >= 2:
                        label = row[0].lower()
                        value = row[1]

                        # National: Number of states
                        if 'national' in label and ('states' in label or 'state' in label):
                            data.national_states = self.clean_text(value)
                            # Extract number from text like "28 states and 8 union territories" or just "28"
                            match = re.search(r'(\d+)\s*(?:states|state)?', value.lower())
                            if match:
                                data.national_states_count = int(match.group(1))
                                logger.info(f"Extracted national states count: {data.national_states_count}")

                        # International: Number of countries
                        elif 'international' in label and ('countries' in label or 'country' in label):
                            data.international_countries = self.clean_text(value)
                            # Extract number from text like "58 countries" or just "58"
                            match = re.search(r'(\d+)\s*(?:countries|country)?', value.lower())
                            if match:
                                data.international_countries_count = int(match.group(1))
                                logger.info(f"Extracted international countries count: {data.international_countries_count}")

            # Look for export percentage in tables (Q20 part b)
            # Common patterns: "contribution of exports", "export as percentage", "exports in total turnover"
            if ('export' in table_text and ('turnover' in table_text or 'percentage' in table_text or 'contribution' in table_text)):
                for row in rows:
                    if len(row) >= 2:
                        label = row[0].lower()
                        # Match questions about export contribution/percentage
                        if ('export' in label and ('contribution' in label or 'percentage' in label or 'turnover' in label)) or \
                           ('contribution' in label and 'export' in label):
                            value = row[1].strip()
                            # Try to extract percentage value
                            match = re.search(r'(\d+\.?\d*)\s*%?', value)
                            if match:
                                pct_value = float(match.group(1))
                                # If value > 1, it's already a percentage (e.g., 0.26% or 26%)
                                # If value < 1, it might be a decimal (e.g., 0.0026)
                                if pct_value > 1:
                                    data.export_pct = pct_value / 100
                                else:
                                    # Check if there's a % sign - if so, treat as percentage
                                    if '%' in value:
                                        data.export_pct = pct_value / 100
                                    else:
                                        data.export_pct = pct_value
                                logger.info(f"Extracted export percentage from table: {data.export_pct}")

        # Extract export percentage from paragraph (fallback)
        if data.export_pct == 0:
            for p in self.soup.find_all('p'):
                text = p.get_text()
                text_lower = text.lower()

                # Export percentage
                if 'export' in text_lower and '%' in text:
                    match = re.search(r'(\d+\.?\d*)\s*%', text)
                    if match:
                        data.export_pct = float(match.group(1)) / 100
                        logger.info(f"Extracted export percentage from paragraph: {data.export_pct}")

        # Types of customers (look for paragraph starting with "c." or containing "types of customers")
        for p in self.soup.find_all('p'):
            text = p.get_text()
            text_lower = text.lower()
            if 'types of customers' in text_lower or text_lower.strip().startswith('c.'):
                if 'types of customers' in text_lower:
                    # Extract the content after "types of customers"
                    customer_text = text
                    data.customer_types_brief = self.clean_text(customer_text)

        logger.info(f"Extracted markets data: export_pct={data.export_pct}")
        return data

    def extract_employees_workers(self) -> EmployeesWorkersData:
        """Extract Q21: Comprehensive employee/worker data."""
        data = EmployeesWorkersData()

        for table in self._tables:
            rows = self.extract_table_data(table)
            table_text = ' '.join([' '.join(r) for r in rows]).upper()

            has_emp = 'EMPLOYEES' in table_text
            has_wrk = 'WORKERS' in table_text
            has_male = 'MALE' in table_text

            is_differently_abled = 'DIFFERENTLY ABLED' in table_text

            if has_emp and has_wrk and has_male:
                section = None

                for row in rows:
                    text = ' '.join(row).upper()
                    is_header_row = len(row) <= 2 or (len(row) == 1 and ('EMPLOYEES' in text or 'WORKERS' in text))

                    if is_header_row and 'EMPLOYEES' in text and 'WORKERS' not in text:
                        section = 'differently_abled_employees' if is_differently_abled else 'employees'
                    elif is_header_row and 'WORKERS' in text and 'EMPLOYEES' not in text:
                        section = 'differently_abled_workers' if is_differently_abled else 'workers'
                    elif section and len(row) >= 7:
                        rtype = row[1].lower() if len(row) > 1 else ''
                        if not rtype.strip():
                            rtype = row[0].lower() if len(row) > 0 else ''

                        key = None
                        if 'permanent' in rtype and 'other' not in rtype:
                            key = 'permanent'
                        elif 'other than' in rtype or 'contractual' in rtype or 'temporary' in rtype:
                            key = 'other'
                        elif 'total' in rtype:
                            key = 'total'

                        if key and section:
                            try:
                                data_cells = row[2:] if len(row) > 2 else []
                                nums = [self.clean_number(cell) for cell in data_cells]

                                if len(nums) >= 5 and nums[0] > 0:
                                    breakdown = GenderBreakdown(
                                        total=int(nums[0]),
                                        male=int(nums[1]),
                                        male_pct=nums[2] if nums[2] <= 1 else nums[2] / 100,
                                        female=int(nums[3]),
                                        female_pct=nums[4] if nums[4] <= 1 else nums[4] / 100,
                                        other=int(nums[5]) if len(nums) >= 7 else 0,
                                        other_pct=nums[6] if len(nums) >= 7 and nums[6] <= 1 else (nums[6] / 100 if len(nums) >= 7 else 0)
                                    )

                                    category = getattr(data, section)
                                    setattr(category, key, breakdown)
                            except (IndexError, ValueError):
                                pass

        # Calculate totals if not provided
        for category_name in ['employees', 'workers', 'differently_abled_employees', 'differently_abled_workers']:
            category = getattr(data, category_name)
            if category.total.total == 0:
                category.total.total = category.permanent.total + category.other.total
                category.total.male = category.permanent.male + category.other.male
                category.total.female = category.permanent.female + category.other.female
                category.total.other = category.permanent.other + category.other.other

                total = category.total.total
                if total > 0:
                    category.total.male_pct = round(category.total.male / total, 4)
                    category.total.female_pct = round(category.total.female / total, 4)
                    category.total.other_pct = round(category.total.other / total, 4)

        return data

    def extract_women_representation(self) -> WomenRepresentation:
        """Extract Q22: Participation of women in Board and KMP."""
        data = WomenRepresentation()

        for table in self._tables:
            table_text = table.get_text().lower()

            if 'participation of women' in table_text or ('board' in table_text and 'female' in table_text):
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 3:
                        text = row[0].lower()

                        if 'board of director' in text:
                            nums = [self.clean_number(cell) for cell in row[1:] if self.clean_number(cell) != 0 or cell.strip() in ['0', '-']]
                            if len(nums) >= 2:
                                data.board = BoardKMPData(
                                    total=int(nums[0]),
                                    female=int(nums[1]),
                                    pct=nums[2] if len(nums) >= 3 and nums[2] <= 1 else (nums[2] / 100 if len(nums) >= 3 else (round(nums[1] / nums[0], 4) if nums[0] > 0 else 0))
                                )

                        elif 'key management' in text or 'kmp' in text:
                            nums = [self.clean_number(cell) for cell in row[1:] if self.clean_number(cell) != 0 or cell.strip() in ['0', '-']]
                            if len(nums) >= 2:
                                data.kmp = BoardKMPData(
                                    total=int(nums[0]),
                                    female=int(nums[1]),
                                    pct=nums[2] if len(nums) >= 3 and nums[2] <= 1 else (nums[2] / 100 if len(nums) >= 3 else (round(nums[1] / nums[0], 4) if nums[0] > 0 else 0))
                                )

        return data

    def extract_turnover_rates(self) -> TurnoverRates:
        """Extract Q23: Turnover rates for permanent employees and workers.

        HTML table structure has columns:
        [Category] | Male CY | Female CY | Total CY | Male PY | Female PY | Total PY | Male PPY | Female PPY | Total PPY

        With rows: Permanent Employees, Permanent Workers
        """
        data = TurnoverRates()

        for table in self._tables:
            table_text = table.get_text().lower()

            if 'turnover rate' in table_text:
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) < 4:
                        continue

                    row_type = row[0].lower()

                    # Handle the common HTML format:
                    # Row: [Category, Male CY, Female CY, Total CY, Male PY, Female PY, Total PY, Male PPY, Female PPY, Total PPY]
                    if 'permanent employees' in row_type and 'workers' not in row_type:
                        category = data.employees
                        if len(row) >= 10:
                            # Full 9-column format (Male/Female/Total for CY/PY/PPY)
                            category.cy.male = self.clean_percentage(row[1])
                            category.cy.female = self.clean_percentage(row[2])
                            category.cy.total = self.clean_percentage(row[3])
                            category.py.male = self.clean_percentage(row[4])
                            category.py.female = self.clean_percentage(row[5])
                            category.py.total = self.clean_percentage(row[6])
                            category.ppy.male = self.clean_percentage(row[7])
                            category.ppy.female = self.clean_percentage(row[8])
                            category.ppy.total = self.clean_percentage(row[9])
                        elif len(row) >= 4:
                            # Shorter format - just CY values
                            category.cy.male = self.clean_percentage(row[1])
                            category.cy.female = self.clean_percentage(row[2])
                            category.cy.total = self.clean_percentage(row[3])

                    elif 'permanent workers' in row_type and 'employees' not in row_type:
                        category = data.workers
                        if len(row) >= 10:
                            # Full 9-column format
                            category.cy.male = self.clean_percentage(row[1])
                            category.cy.female = self.clean_percentage(row[2])
                            category.cy.total = self.clean_percentage(row[3])
                            category.py.male = self.clean_percentage(row[4])
                            category.py.female = self.clean_percentage(row[5])
                            category.py.total = self.clean_percentage(row[6])
                            category.ppy.male = self.clean_percentage(row[7])
                            category.ppy.female = self.clean_percentage(row[8])
                            category.ppy.total = self.clean_percentage(row[9])
                        elif len(row) >= 4:
                            # Shorter format - just CY values
                            category.cy.male = self.clean_percentage(row[1])
                            category.cy.female = self.clean_percentage(row[2])
                            category.cy.total = self.clean_percentage(row[3])

        return data

    def extract_subsidiaries(self) -> List[Subsidiary]:
        """Extract Q24: Holding, subsidiary, and associate companies."""
        subs = []
        table = self.find_table_by_header('holding', 'subsidiary')

        if table:
            for row in self.extract_table_data(table)[1:]:
                if len(row) >= 4:
                    subs.append(Subsidiary(
                        name=row[1] if len(row) > 1 else '',
                        category=row[2] if len(row) > 2 else '',
                        shares_pct=self.clean_percentage(row[3]) if len(row) > 3 else 0,
                        participates='Yes' if len(row) > 4 and 'yes' in row[4].lower() else 'No'
                    ))

        return subs

    def extract_csr_data(self) -> CSRData:
        """Extract Q25: CSR applicability and details."""
        data = CSRData()

        for table in self._tables:
            for row in self.extract_table_data(table):
                if len(row) >= 2:
                    q = row[0].lower()
                    if 'csr applicable' in q or 'section 135' in q:
                        data.applicable = 'Yes' if 'yes' in row[1].lower() else 'No'
                    elif 'turnover' in q:
                        data.turnover = self.clean_number(row[1])
                    elif 'net worth' in q:
                        data.net_worth = self.clean_number(row[1])

        # Extract CSR projects in aspirational districts (Leadership Indicator)
        data.aspirational_districts = self.extract_csr_aspirational_districts()

        return data

    def extract_csr_aspirational_districts(self) -> List['CSRProject']:
        """
        Extract CSR projects undertaken in aspirational districts.

        This is a Leadership Indicator under Principle 8.
        Table structure: State | Aspirational District | Amount spent (In INR)
        """
        projects = []

        for table in self._tables:
            rows = self.extract_table_data(table)
            if len(rows) < 2:
                continue

            # Check if this is the aspirational districts table
            # Header should have "State" and "Aspirational District" columns
            table_text = ' '.join([' '.join(r) for r in rows[:2]]).lower()
            if 'aspirational district' in table_text and 'state' in table_text:
                # Found the table, now extract data rows
                # Header row might contain: State, Aspirational District, Amount spent

                # Find the header row index (row containing 'State' and 'Aspirational District')
                header_idx = 0
                for idx, row in enumerate(rows):
                    row_text = ' '.join(row).lower()
                    if 'state' in row_text and 'aspirational' in row_text and 'amount' in row_text:
                        header_idx = idx
                        break

                # Extract data rows (starting after header)
                for row in rows[header_idx + 1:]:
                    if len(row) >= 3:
                        state = row[0].strip()
                        district = row[1].strip()
                        amount_text = row[2].strip()

                        # Skip empty rows or header-like rows
                        if not state or state.lower() in ['state', 's.no', 's. no', 'sr. no', 'total']:
                            continue
                        if not district or district.lower() in ['aspirational district', 'district']:
                            continue

                        # Parse amount
                        amount = self.clean_number(amount_text)

                        # Accept rows even with amount = 0 (might be valid data)
                        if state and district:
                            projects.append(CSRProject(
                                state=state,
                                aspirational_district=district,
                                amount_spent=amount
                            ))

                # Log extraction results
                logger.info(f"Extracted {len(projects)} CSR aspirational district projects")
                break  # Found and processed the table

        if not projects:
            logger.warning("No CSR aspirational districts table found or no data extracted")
        return projects

    def extract_safety_skill_training(self) -> 'SafetySkillTraining':
        """
        Extract Principle 3, Q8: Details of training given to employees and workers.

        Table structure:
        - Category (Employees/Workers with Male, Female, Others, Total)
        - FY Current: Total(A), Health&Safety No.(B), %(B/A), Skill No.(C), %(C/A)
        - FY Previous: Total(D), Health&Safety No.(E), %(E/D), Skill No.(F), %(F/D)
        """
        training = SafetySkillTraining()

        for table in self._tables:
            rows = self.extract_table_data(table)
            if len(rows) < 3:
                continue

            # Check if this is the training table
            table_text = ' '.join([' '.join(r) for r in rows[:3]]).lower()
            if ('training' in table_text and 'health and safety' in table_text and
                'skill upgradation' in table_text):

                # Process rows to find employee and worker data
                current_category = None  # 'employees' or 'workers'

                for row in rows:
                    if len(row) < 8:  # Need at least 8 columns for all data
                        continue

                    first_cell = row[0].lower().strip()

                    # Detect category headers
                    if 'employee' in first_cell:
                        current_category = 'employees'
                        continue
                    elif 'worker' in first_cell:
                        current_category = 'workers'
                        continue

                    # Skip if no category set or if it's a header row
                    if not current_category or 'total' in first_cell and '(' not in first_cell:
                        continue

                    # Determine gender
                    gender_key = None
                    if 'male' in first_cell and 'female' not in first_cell:
                        gender_key = 'male'
                    elif 'female' in first_cell:
                        gender_key = 'female'
                    elif 'other' in first_cell:
                        gender_key = 'others'
                    elif 'total' in first_cell:
                        gender_key = 'total'
                    else:
                        continue  # Skip rows that don't match gender categories

                    # Extract values (indices may vary, but typical structure):
                    # [Category, Total(A), HS No.(B), HS %(B/A), Skill No.(C), Skill %(C/A),
                    #  Total(D), HS No.(E), HS %(E/D), Skill No.(F), Skill %(F/D)]
                    try:
                        gender_data = SafetySkillTrainingGender(
                            total_cy=int(self.clean_number(row[1])) if len(row) > 1 else 0,
                            hs_num_cy=int(self.clean_number(row[2])) if len(row) > 2 else 0,
                            hs_pct_cy=self.clean_number(row[3]) if len(row) > 3 else 0,
                            skill_num_cy=int(self.clean_number(row[4])) if len(row) > 4 else 0,
                            skill_pct_cy=self.clean_number(row[5]) if len(row) > 5 else 0,
                            total_py=int(self.clean_number(row[6])) if len(row) > 6 else 0,
                            hs_num_py=int(self.clean_number(row[7])) if len(row) > 7 else 0,
                            hs_pct_py=self.clean_number(row[8]) if len(row) > 8 else 0,
                            skill_num_py=int(self.clean_number(row[9])) if len(row) > 9 else 0,
                            skill_pct_py=self.clean_number(row[10]) if len(row) > 10 else 0,
                        )

                        # Assign to appropriate category and gender
                        if current_category == 'employees':
                            setattr(training.employees, gender_key, gender_data)
                        elif current_category == 'workers':
                            setattr(training.workers, gender_key, gender_data)
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Error extracting training data for {current_category} {gender_key}: {e}")
                        continue

                logger.info(f"Extracted safety & skill training data")
                break  # Found and processed the table

        return training

    def extract_complaints(self) -> List[Complaint]:
        """Extract Q26: Stakeholder complaints/grievances."""
        complaints = []

        for table in self._tables:
            rows = self.extract_table_data(table)
            if len(rows) < 3:
                continue

            table_text = ' '.join([' '.join(r) for r in rows[:3]]).lower()
            if 'stakeholder' in table_text and 'grievance' in table_text and 'complaint' in table_text:
                for row in rows[2:]:
                    if len(row) >= 8:
                        stakeholder_name = row[0].lower().strip()

                        stakeholder_type = None
                        for key, value in self.STAKEHOLDER_MAPPING.items():
                            if key in stakeholder_name:
                                stakeholder_type = value
                                break

                        if stakeholder_type:
                            grievance_text = row[1].strip()
                            has_mechanism = 'yes' in grievance_text.lower()

                            web_link = ''
                            if 'http' in grievance_text.lower():
                                urls = re.findall(r'https?://[^\s]+', grievance_text)
                                web_link = urls[0] if urls else ''

                            complaints.append(Complaint(
                                stakeholder=stakeholder_type,
                                has_mechanism='Yes' if has_mechanism else 'No',
                                web_link=web_link,
                                filed_cy=int(self.clean_number(row[2])) if len(row) > 2 else 0,
                                pending_cy=int(self.clean_number(row[3])) if len(row) > 3 else 0,
                                remarks_cy=row[4] if len(row) > 4 and row[4].strip() and row[4].upper() != 'NA' else '',
                                filed_py=int(self.clean_number(row[5])) if len(row) > 5 else 0,
                                pending_py=int(self.clean_number(row[6])) if len(row) > 6 else 0,
                                remarks_py=row[7] if len(row) > 7 and row[7].strip() and row[7].upper() != 'NA' else ''
                            ))
                break

        return complaints

    def extract_material_issues(self) -> List[MaterialIssue]:
        """Extract Q27: Material responsible business conduct issues."""
        issues = []
        table = self.find_table_by_header('material issue', 'risk', 'opportunity')

        if table:
            for row in self.extract_table_data(table)[1:]:
                if len(row) >= 5 and row[1].strip():
                    risk_opp_text = row[2].strip() if len(row) > 2 else ''
                    risk_opp_lower = risk_opp_text.lower()
                    # Store the full text to match HTML for interactive viewer tagging
                    if 'risk' in risk_opp_lower:
                        risk_or_opp = 'Risk'
                    elif 'opportunity' in risk_opp_lower:
                        risk_or_opp = 'Opportunity'
                    else:
                        risk_or_opp = risk_opp_text if risk_opp_text else ''

                    fin_impact = row[5] if len(row) > 5 else ''
                    if 'negative' in fin_impact.lower():
                        financial_implication = 'Negative Implications'
                    elif 'positive' in fin_impact.lower():
                        financial_implication = 'Positive Implications'
                    else:
                        financial_implication = fin_impact if fin_impact else ''

                    issues.append(MaterialIssue(
                        issue=row[1] if len(row) > 1 else '',
                        risk_or_opp=risk_or_opp,
                        rationale=row[3] if len(row) > 3 else '',
                        mitigation=row[4] if len(row) > 4 else '',
                        financial_impact=financial_implication
                    ))

        return issues

    # =========================================================================
    # Section B: Management and Process Disclosures
    # =========================================================================

    def extract_governance_data(self) -> Dict[str, str]:
        """Extract Section B: Governance, Leadership and Oversight (Q7-Q9)."""
        data = {
            'director_statement': '',
            'highest_authority': '',
            'has_specific_committee': 'No',
            'specific_committee_details': ''
        }

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for governance, leadership and oversight section
            if 'governance' in table_text and 'leadership' in table_text:
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) < 2:
                        continue

                    question = row[0].lower()
                    # Combine all answer columns
                    answer = ' '.join(row[1:]).strip()

                    # Q7: Director statement
                    if 'statement by director' in question or ('director' in question and 'esg' in question):
                        data['director_statement'] = answer

                    # Q8: Highest authority
                    elif 'highest authority' in question or ('implementation' in question and 'oversight' in question):
                        data['highest_authority'] = answer

                    # Q9: Specific committee
                    elif 'specific committee' in question or ('committee' in question and ('responsible' in question or 'sustainability' in question)):
                        if 'yes' in answer.lower():
                            data['has_specific_committee'] = 'Yes'
                            data['specific_committee_details'] = answer
                        elif 'no' in answer.lower():
                            data['has_specific_committee'] = 'No'
                        else:
                            data['specific_committee_details'] = answer

        return data

    def extract_section_b_principles(self) -> List[PrincipleDisclosure]:
        """Extract Section B: Management and Process Disclosures for P1-P9."""
        principles = [
            PrincipleDisclosure(num=i) for i in range(1, 10)
        ]

        for table in self._tables:
            rows = self.extract_table_data(table)
            if len(rows) < 3:
                continue

            header_row = rows[0] if rows else []
            if len(header_row) >= 10 and 'P1' in header_row and 'P9' in header_row:
                for row in rows[1:]:
                    if len(row) < 10:
                        continue

                    question = row[0].lower()

                    if 'policy' in question and 'cover' in question and 'principle' in question:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].policy_covers = 'Yes' if 'yes' in val.lower() else ('No' if 'no' in val.lower() else val[:50])

                    elif 'approved' in question and 'board' in question:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            if 'yes' in val.lower():
                                principles[i].board_approved = 'Yes'
                            elif 'no' in val.lower():
                                principles[i].board_approved = 'No'

                    elif 'web link' in question or 'weblink' in question:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            urls = re.findall(r'https?://[^\s]+', val)
                            principles[i].web_link = urls[0] if urls else val[:200]

                    elif 'translated' in question and 'procedure' in question:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].translated_to_procedures = 'Yes' if 'yes' in val.lower() else ('No' if 'no' in val.lower() else 'Yes')

                    elif 'value chain' in question and 'partner' in question:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].extends_to_value_chain = 'Yes' if 'yes' in val.lower() else ('No' if 'no' in val.lower() else 'Yes')

                    elif 'code' in question and ('certification' in question or 'standard' in question):
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].codes_certifications = val[:500] if val else ''

                    elif 'commitment' in question and 'goal' in question:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].commitments_goals = val[:500] if val else ''

                    elif 'performance' in question and 'commitment' in question:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].performance = val[:500] if val else ''

                break

        # Extract Q10: Review by and Frequency tables
        for table in self._tables:
            table_text = table.get_text().lower()

            # Q10 Review by table (who reviews)
            if 'indicate whether review' in table_text and 'director' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) < 10:
                        continue
                    row_label = row[0].lower()

                    if 'performance against above policies' in row_label:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].performance_review_by = val[:200] if val else ''

                    elif 'compliance with statutory' in row_label:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].compliance_review_by = val[:200] if val else ''

            # Q10 Frequency table (how often)
            elif 'frequency' in table_text and ('annually' in table_text or 'quarterly' in table_text or 'half yearly' in table_text):
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) < 10:
                        continue
                    row_label = row[0].lower()

                    if 'performance against above policies' in row_label:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].performance_frequency = val[:200] if val else ''

                    elif 'compliance with statutory' in row_label:
                        for i in range(9):
                            val = row[i + 1].strip() if len(row) > i + 1 else ''
                            principles[i].compliance_frequency = val[:200] if val else ''

        return principles

    # =========================================================================
    # Section C: Principle-wise Performance
    # =========================================================================

    def extract_sustainability_data(self) -> SustainabilityData:
        """Extract sustainability-related data including R&D, Capex."""
        data = SustainabilityData()

        for table in self._tables:
            text = table.get_text().lower()
            if 'r&d' in text and 'capex' in text and '%' in text:
                rows = table.find_all('tr')
                for row in rows:
                    cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                    if len(cells) >= 4:
                        label = cells[0].lower()
                        if 'r&d' in label:
                            data.rd_cy = self.clean_percentage(cells[1]) if len(cells) > 1 else 0
                            data.rd_py = self.clean_percentage(cells[2]) if len(cells) > 2 else 0
                            data.rd_improvements = cells[3] if len(cells) > 3 else ''
                        elif 'capex' in label:
                            data.capex_cy = self.clean_percentage(cells[1]) if len(cells) > 1 else 0
                            data.capex_py = self.clean_percentage(cells[2]) if len(cells) > 2 else 0
                            data.capex_improvements = cells[3] if len(cells) > 3 else ''
                break

        # Extract recycled input materials
        for table in self._tables:
            text = table.get_text().lower()
            if 'recycled or reused input material' in text or 'recycled or re-used input' in text:
                rows = table.find_all('tr')
                for row in rows[2:]:
                    cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                    if len(cells) >= 3:
                        material = cells[0]
                        if material and material.lower() not in ['indicate input material', '']:
                            data.recycled_input_cy = RecycledInput(
                                material=material,
                                percentage=self.clean_percentage(cells[1])
                            )
                            data.recycled_input_py = RecycledInput(
                                material=material,
                                percentage=self.clean_percentage(cells[2])
                            )
                            break
                break

        # Extract reclaimed products
        for table in self._tables:
            text = table.get_text()
            if 'Indicate product category' in text and 'Reclaimed products' in text:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                    if len(cells) >= 2:
                        category = cells[0]
                        pct_text = cells[1]
                        pct_val = 0
                        if pct_text and pct_text != '-':
                            match = re.search(r'([\d.]+)%', pct_text)
                            if match:
                                try:
                                    pct_val = round(float(match.group(1)) / 100, 4)
                                except ValueError:
                                    pass
                        if category:
                            data.reclaimed_products.append(ReclaimedProduct(
                                category=category,
                                percentage=pct_val
                            ))
                break

        return data

    def extract_waste_data(self) -> WasteData:
        """Extract waste reclamation data."""
        data = WasteData()

        for table in self._tables:
            text = table.get_text()
            if 'Re-Used' in text and 'Recycled' in text and 'Safely Disposed' in text:
                rows = table.find_all('tr')
                has_plastics = any('plastics' in row.get_text().lower() for row in rows)

                if has_plastics:
                    for row in rows:
                        cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                        if len(cells) >= 7:
                            label = cells[0].lower()

                            if 'plastic' in label:
                                data.plastics_cy = WasteCategory(
                                    reused=self.clean_number(cells[1]),
                                    recycled=self.clean_number(cells[2]),
                                    disposed=self.clean_number(cells[3])
                                )
                                data.plastics_py = WasteCategory(
                                    reused=self.clean_number(cells[4]),
                                    recycled=self.clean_number(cells[5]),
                                    disposed=self.clean_number(cells[6])
                                )
                            elif 'e-waste' in label:
                                data.ewaste_cy = WasteCategory(
                                    reused=self.clean_number(cells[1]),
                                    recycled=self.clean_number(cells[2]),
                                    disposed=self.clean_number(cells[3])
                                )
                                data.ewaste_py = WasteCategory(
                                    reused=self.clean_number(cells[4]),
                                    recycled=self.clean_number(cells[5]),
                                    disposed=self.clean_number(cells[6])
                                )
                            elif 'hazardous' in label:
                                data.hazardous_cy = WasteCategory(
                                    reused=self.clean_number(cells[1]),
                                    recycled=self.clean_number(cells[2]),
                                    disposed=self.clean_number(cells[3])
                                )
                                data.hazardous_py = WasteCategory(
                                    reused=self.clean_number(cells[4]),
                                    recycled=self.clean_number(cells[5]),
                                    disposed=self.clean_number(cells[6])
                                )
                            elif 'other waste' in label:
                                data.other_cy = WasteCategory(
                                    reused=self.clean_number(cells[1]),
                                    recycled=self.clean_number(cells[2]),
                                    disposed=self.clean_number(cells[3])
                                )
                                data.other_py = WasteCategory(
                                    reused=self.clean_number(cells[4]),
                                    recycled=self.clean_number(cells[5]),
                                    disposed=self.clean_number(cells[6])
                                )
                    break

        return data

    def extract_accounts_payable_data(self) -> AccountsPayableData:
        """Extract accounts payable, trading houses, dealers data."""
        data = AccountsPayableData()

        # Days payable
        for table in self._tables:
            text = table.get_text().lower()
            if 'days of accounts payable' in text:
                rows = table.find_all('tr')
                for row in rows:
                    cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                    if len(cells) >= 3:
                        q = cells[0].lower()
                        if 'days of accounts payable' in q:
                            days_cy = int(self.clean_number(cells[1])) if self.clean_number(cells[1]) else 0
                            days_py = int(self.clean_number(cells[2])) if len(cells) > 2 and self.clean_number(cells[2]) else 0
                            data.days_payable_cy = f'P{days_cy}D'
                            data.days_payable_py = f'P{days_py}D'
                break

        # Trading houses
        for table in self._tables:
            text = table.get_text().lower()
            if 'concentration of purchases' in text and 'trading house' in text:
                rows = table.find_all('tr')
                for row in rows:
                    cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                    if len(cells) >= 2:
                        label = cells[0].lower()
                        cy_idx, py_idx = (1, 2) if len(cells) == 3 else (2, 3) if len(cells) == 4 else (1, 2)
                        if len(cells) == 4:
                            label = cells[1].lower()

                        if 'top 10' in label and 'trading' in label:
                            data.top10_trading_pct_cy = self.clean_percentage(cells[cy_idx]) if len(cells) > cy_idx else 0
                            data.top10_trading_pct_py = self.clean_percentage(cells[py_idx]) if len(cells) > py_idx else 0
                        elif 'number of trading houses' in label:
                            data.num_trading_houses_cy = int(self.clean_number(cells[cy_idx])) if len(cells) > cy_idx else 0
                            data.num_trading_houses_py = int(self.clean_number(cells[py_idx])) if len(cells) > py_idx else 0
                        elif ('trading houses as %' in label or 'purchases from trading houses as' in label) and 'top 10' not in label:
                            data.trading_purchases_pct_cy = self.clean_percentage(cells[cy_idx]) if len(cells) > cy_idx else 0
                            data.trading_purchases_pct_py = self.clean_percentage(cells[py_idx]) if len(cells) > py_idx else 0
                break

        # Dealers
        for table in self._tables:
            text = table.get_text().lower()
            if 'concentration of sales' in text and 'dealer' in text:
                rows = table.find_all('tr')
                for row in rows:
                    cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                    if len(cells) >= 2:
                        label = cells[0].lower()
                        cy_idx, py_idx = (1, 2) if len(cells) == 3 else (2, 3) if len(cells) == 4 else (1, 2)
                        if len(cells) == 4:
                            label = cells[1].lower()

                        if 'top 10' in label and ('dealer' in label or 'distributor' in label):
                            data.top10_dealer_pct_cy = self.clean_percentage(cells[cy_idx]) if len(cells) > cy_idx else 0
                            data.top10_dealer_pct_py = self.clean_percentage(cells[py_idx]) if len(cells) > py_idx else 0
                        elif 'number of dealers' in label or 'number of dealer' in label:
                            data.num_dealers_cy = int(self.clean_number(cells[cy_idx])) if len(cells) > cy_idx else 0
                            data.num_dealers_py = int(self.clean_number(cells[py_idx])) if len(cells) > py_idx else 0
                        elif ('dealer' in label or 'distributor' in label) and 'as %' in label and 'total sales' in label and 'top 10' not in label:
                            data.dealer_sales_pct_cy = self.clean_percentage(cells[cy_idx]) if len(cells) > cy_idx else 0
                            data.dealer_sales_pct_py = self.clean_percentage(cells[py_idx]) if len(cells) > py_idx else 0
                break

        return data

    def extract_water_data(self) -> WaterData:
        """Extract water-related data including Zero Liquid Discharge (ZLD)."""
        data = WaterData()

        for table in self._tables:
            rows = self.extract_table_data(table)

            for row in rows:
                if len(row) >= 2:
                    question = row[0].lower()

                    # Zero Liquid Discharge extraction
                    if 'zero liquid discharge' in question:
                        answer = row[1].strip() if len(row) > 1 else ''

                        # Determine if ZLD is implemented (Yes/No)
                        answer_lower = answer.lower()
                        if answer and answer_lower not in ['no', 'na', 'nil', 'not applicable', '-', '']:
                            # If there's substantive content, ZLD is implemented
                            data.has_zld = 'Yes'
                            # Store the full details text
                            data.zld_details = self.clean_text(answer)
                        else:
                            data.has_zld = 'No'
                            data.zld_details = ''

                    # Water withdrawal by source
                    elif 'surface water' in question:
                        data.surface_water_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                        data.surface_water_py = self.clean_number(row[2]) if len(row) > 2 else 0

                    elif 'groundwater' in question and 'seawater' not in question:
                        data.groundwater_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                        data.groundwater_py = self.clean_number(row[2]) if len(row) > 2 else 0

                    elif 'third party water' in question or 'third-party water' in question:
                        data.third_party_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                        data.third_party_py = self.clean_number(row[2]) if len(row) > 2 else 0

                    elif 'seawater' in question or 'sea water' in question:
                        data.seawater_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                        data.seawater_py = self.clean_number(row[2]) if len(row) > 2 else 0

                    elif 'total volume of water withdrawal' in question:
                        data.total_withdrawal_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                        data.total_withdrawal_py = self.clean_number(row[2]) if len(row) > 2 else 0

                    elif 'total volume of water consumption' in question:
                        data.total_consumption_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                        data.total_consumption_py = self.clean_number(row[2]) if len(row) > 2 else 0

                    elif 'water intensity per rupee' in question or 'water intensity in terms of turnover' in question:
                        data.intensity_turnover_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                        data.intensity_turnover_py = self.clean_number(row[2]) if len(row) > 2 else 0

                    elif 'water intensity' in question and 'physical output' in question:
                        data.intensity_physical_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                        data.intensity_physical_py = self.clean_number(row[2]) if len(row) > 2 else 0

                    elif 'total water discharged' in question:
                        data.total_discharge_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                        data.total_discharge_py = self.clean_number(row[2]) if len(row) > 2 else 0

        # Look for water withdrawal external assessment note (appears after water withdrawal table)
        for table in self._tables:
            table_text = table.get_text().lower()
            if ('independent assessment' in table_text or 'external agency' in table_text) and 'water withdrawal' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if ('independent assessment' in question or 'external agency' in question) and data.external_assessment == 'No':
                            answer = row[1].strip()
                            answer_lower = answer.lower()
                            if answer_lower.startswith('yes') or 'reasonable assurance' in answer_lower or 'limited assurance' in answer_lower or 'tuv' in answer_lower or 'assurance' in answer_lower:
                                data.external_assessment = 'Yes'
                                data.external_agency = self.clean_text(answer)

        # Extract water discharge data from discharge table
        current_discharge_dest = None  # Track current discharge destination (surface, groundwater, etc.)

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for water discharge table
            if 'water discharge by destination' in table_text or ('discharge' in table_text and 'treatment' in table_text):
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 1:
                        label = row[0].lower()

                        # Track which discharge destination we're in
                        if 'to surface water' in label or '(i) to surface water' in label:
                            current_discharge_dest = 'surface'
                            if len(row) >= 2:
                                data.discharge_surface_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                data.discharge_surface_py = self.clean_number(row[2]) if len(row) > 2 else 0
                        elif 'to groundwater' in label or '(ii) to groundwater' in label:
                            current_discharge_dest = 'groundwater'
                            if len(row) >= 2:
                                data.discharge_groundwater_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                data.discharge_groundwater_py = self.clean_number(row[2]) if len(row) > 2 else 0
                        elif 'to seawater' in label or '(iii) to seawater' in label:
                            current_discharge_dest = 'seawater'
                            if len(row) >= 2:
                                data.discharge_seawater_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                data.discharge_seawater_py = self.clean_number(row[2]) if len(row) > 2 else 0
                        elif 'third-parties' in label or 'third parties' in label or '(iv) sent to third' in label:
                            current_discharge_dest = 'thirdparty'
                            if len(row) >= 2:
                                data.discharge_thirdparty_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                data.discharge_thirdparty_py = self.clean_number(row[2]) if len(row) > 2 else 0
                        elif '(v) others' in label:
                            current_discharge_dest = 'others'
                            if len(row) >= 2:
                                data.discharge_others_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                data.discharge_others_py = self.clean_number(row[2]) if len(row) > 2 else 0
                        elif 'total water discharged' in label:
                            data.total_discharge_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                            data.total_discharge_py = self.clean_number(row[2]) if len(row) > 2 else 0

                        # Parse treatment details based on current destination
                        elif 'no treatment' in label and current_discharge_dest:
                            cy_val = self.clean_number(row[1]) if len(row) > 1 else 0
                            py_val = self.clean_number(row[2]) if len(row) > 2 else 0
                            if current_discharge_dest == 'surface':
                                data.discharge_surface_no_treatment_cy = cy_val
                                data.discharge_surface_no_treatment_py = py_val
                            elif current_discharge_dest == 'groundwater':
                                data.discharge_groundwater_no_treatment_cy = cy_val
                                data.discharge_groundwater_no_treatment_py = py_val
                            elif current_discharge_dest == 'seawater':
                                data.discharge_seawater_no_treatment_cy = cy_val
                                data.discharge_seawater_no_treatment_py = py_val
                            elif current_discharge_dest == 'thirdparty':
                                data.discharge_thirdparty_no_treatment_cy = cy_val
                                data.discharge_thirdparty_no_treatment_py = py_val
                            elif current_discharge_dest == 'others':
                                data.discharge_others_no_treatment_cy = cy_val
                                data.discharge_others_no_treatment_py = py_val

                        elif 'with treatment' in label and current_discharge_dest:
                            cy_val = self.clean_number(row[1]) if len(row) > 1 else 0
                            py_val = self.clean_number(row[2]) if len(row) > 2 else 0
                            if current_discharge_dest == 'surface':
                                data.discharge_surface_with_treatment_cy = cy_val
                                data.discharge_surface_with_treatment_py = py_val
                            elif current_discharge_dest == 'groundwater':
                                data.discharge_groundwater_with_treatment_cy = cy_val
                                data.discharge_groundwater_with_treatment_py = py_val
                            elif current_discharge_dest == 'seawater':
                                data.discharge_seawater_with_treatment_cy = cy_val
                                data.discharge_seawater_with_treatment_py = py_val
                            elif current_discharge_dest == 'thirdparty':
                                data.discharge_thirdparty_with_treatment_cy = cy_val
                                data.discharge_thirdparty_with_treatment_py = py_val
                            elif current_discharge_dest == 'others':
                                data.discharge_others_with_treatment_cy = cy_val
                                data.discharge_others_with_treatment_py = py_val

            # Look for water discharge external assessment (appears after the discharge table)
            if 'independent assessment' in table_text or 'external agency' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        # Check if this is the discharge assessment (comes after discharge table)
                        if ('independent assessment' in question or 'external agency' in question) and data.discharge_external_assessment == 'No' and data.total_discharge_cy > 0:
                            answer = row[1].strip()
                            answer_lower = answer.lower()
                            if answer_lower.startswith('yes') or 'reasonable assurance' in answer_lower or 'limited assurance' in answer_lower:
                                data.discharge_external_assessment = 'Yes'
                                data.discharge_external_agency = self.clean_text(answer)

        return data

    def extract_energy_data(self) -> EnergyData:
        """Extract energy consumption data from Principle 6."""
        data = EnergyData()
        in_renewable_section = False
        in_nonrenewable_section = False

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for energy consumption table (may have "electricity consumption" or "energy intensity")
            if 'total electricity consumption' in table_text or 'energy intensity' in table_text or 'from renewable sources' in table_text:
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 1:
                        label = row[0].lower()

                        # Track which section we're in (section headers don't have "total" or "energy consumed")
                        if 'from renewable sources' in label and 'total' not in label and 'non' not in label:
                            in_renewable_section = True
                            in_nonrenewable_section = False
                            continue
                        elif ('from non-renewable sources' in label or 'non renewable' in label) and 'total' not in label:
                            in_renewable_section = False
                            in_nonrenewable_section = True
                            continue

                        # Parse values based on current section
                        if len(row) >= 2:
                            cy_val = self.clean_number(row[1]) if len(row) > 1 else 0
                            py_val = self.clean_number(row[2]) if len(row) > 2 else 0

                            # Check subtotals FIRST (before individual rows) to avoid substring matching issues
                            # e.g., "(a)" is substring of "(a+b+c)" so we need to check subtotals first
                            if ('total energy consumed from renewable' in label or '(a+b+c)' in label) and 'non' not in label:
                                data.total_renewable_cy = cy_val
                                data.total_renewable_py = py_val

                            elif 'total energy consumed from non-renewable' in label or '(d+e+f)' in label:
                                data.total_nonrenewable_cy = cy_val
                                data.total_nonrenewable_py = py_val

                            elif ('total energy consumed' in label and 'from' not in label) or '(a+b+c+d+e+f)' in label:
                                data.total_energy_cy = cy_val
                                data.total_energy_py = py_val

                            # Now check individual energy rows
                            elif 'total electricity consumption' in label and ('(a)' in label or '(d)' in label):
                                if in_renewable_section or '(a)' in label:
                                    data.elec_renewable_cy = cy_val
                                    data.elec_renewable_py = py_val
                                elif in_nonrenewable_section or '(d)' in label:
                                    data.elec_nonrenewable_cy = cy_val
                                    data.elec_nonrenewable_py = py_val

                            elif 'total fuel consumption' in label and ('(b)' in label or '(e)' in label):
                                if in_renewable_section or '(b)' in label:
                                    data.fuel_renewable_cy = cy_val
                                    data.fuel_renewable_py = py_val
                                elif in_nonrenewable_section or '(e)' in label:
                                    data.fuel_nonrenewable_cy = cy_val
                                    data.fuel_nonrenewable_py = py_val

                            elif 'energy consumption through other sources' in label and ('(c)' in label or '(f)' in label):
                                # Extract the original row label text for the name parameter
                                original_label = row[0].strip() if row else ""

                                if in_renewable_section or '(c)' in label:
                                    data.other_renewable_cy = cy_val
                                    data.other_renewable_py = py_val
                                    # Capture the name/description of other renewable source
                                    if original_label and not data.other_renewable_name_cy:
                                        data.other_renewable_name_cy = original_label
                                        data.other_renewable_name_py = original_label
                                elif in_nonrenewable_section or '(f)' in label:
                                    data.other_nonrenewable_cy = cy_val
                                    data.other_nonrenewable_py = py_val
                                    # Capture the name/description of other non-renewable source
                                    if original_label and not data.other_nonrenewable_name_cy:
                                        data.other_nonrenewable_name_cy = original_label
                                        data.other_nonrenewable_name_py = original_label

                            elif 'energy intensity per rupee of turnover' in label:
                                if 'ppp' in label or 'purchasing power' in label:
                                    data.intensity_turnover_ppp_cy = cy_val
                                    data.intensity_turnover_ppp_py = py_val
                                else:
                                    data.intensity_turnover_cy = cy_val
                                    data.intensity_turnover_py = py_val

                            elif 'energy intensity in terms of physical output' in label:
                                data.intensity_physical_cy = cy_val
                                data.intensity_physical_py = py_val

                            elif 'energy intensity' in label and ('optional' in label or 'relevant metric may be selected' in label):
                                data.intensity_optional_cy = cy_val
                                data.intensity_optional_py = py_val

            # Look for external assessment note (appears right after energy table)
            if 'independent assessment' in table_text or 'external agency' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        # Check for energy assessment note (usually first one after energy consumption table)
                        if ('independent assessment' in question or 'external agency' in question) and data.external_assessment == 'No':
                            answer = row[1].strip()
                            answer_lower = answer.lower()
                            if answer_lower.startswith('yes') or 'reasonable assurance' in answer_lower or 'assured' in answer_lower:
                                data.external_assessment = 'Yes'
                                # Extract agency name
                                data.external_agency = self.clean_text(answer)

            # Look for PAT scheme / designated consumers
            if 'designated consumer' in table_text or 'pat scheme' in table_text or 'performance, achieve and trade' in table_text.lower():
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'designated consumer' in question or 'pat scheme' in question:
                            answer = row[1].strip()
                            answer_lower = answer.lower()
                            if answer_lower.startswith('yes') or 'designated consumer' in answer_lower:
                                data.pat_applicable = 'Yes'
                                data.pat_details = self.clean_text(answer)
                            elif 'not applicable' in answer_lower or answer_lower.startswith('no'):
                                data.pat_applicable = 'No'
                                data.pat_details = self.clean_text(answer)

            # Look for low/zero carbon sites
            if 'low/zero carbon' in table_text or 'energy efficient' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'low/zero carbon' in question or ('energy efficient' in question and 'external agency' in question):
                            answer = row[1].strip()
                            answer_lower = answer.lower()
                            if answer_lower.startswith('yes'):
                                data.low_carbon_sites = 'Yes'
                                data.low_carbon_details = self.clean_text(answer)
                            else:
                                data.low_carbon_sites = 'No'
                                data.low_carbon_details = self.clean_text(answer)

        return data

    def extract_ghg_data(self) -> GHGData:
        """Extract greenhouse gas emissions data from Principle 6."""
        data = GHGData()

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for GHG emissions table (Scope 1 and Scope 2)
            if 'scope 1' in table_text or 'scope 2' in table_text or 'greenhouse gas' in table_text:
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 2:
                        label = row[0].lower()

                        # Scope 1 emissions
                        if 'total scope 1 emissions' in label or ('scope 1' in label and 'total' in label):
                            data.scope1_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                            data.scope1_py = self.clean_number(row[2]) if len(row) > 2 else 0

                        # Scope 2 emissions
                        elif 'total scope 2 emissions' in label or ('scope 2' in label and 'total' in label):
                            data.scope2_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                            data.scope2_py = self.clean_number(row[2]) if len(row) > 2 else 0

                        # Total Scope 1 + Scope 2 intensity per rupee of turnover
                        elif 'intensity per rupee' in label or ('intensity' in label and 'turnover' in label):
                            if 'ppp' in label or 'purchasing power' in label:
                                data.intensity_turnover_ppp_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                data.intensity_turnover_ppp_py = self.clean_number(row[2]) if len(row) > 2 else 0
                            else:
                                data.intensity_turnover_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                data.intensity_turnover_py = self.clean_number(row[2]) if len(row) > 2 else 0

                        # Intensity in terms of physical output
                        elif 'intensity' in label and 'physical output' in label:
                            data.intensity_physical_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                            data.intensity_physical_py = self.clean_number(row[2]) if len(row) > 2 else 0

                        # Optional intensity metric
                        elif 'intensity' in label and ('optional' in label or 'relevant metric' in label):
                            data.intensity_optional_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                            data.intensity_optional_py = self.clean_number(row[2]) if len(row) > 2 else 0

            # Look for GHG external assessment note
            if ('independent assessment' in table_text or 'external agency' in table_text) and ('greenhouse' in table_text or 'ghg' in table_text or 'scope 1' in table_text):
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if ('independent assessment' in question or 'external agency' in question) and data.external_assessment == 'No':
                            answer = row[1].strip()
                            answer_lower = answer.lower()
                            if answer_lower.startswith('yes') or 'reasonable assurance' in answer_lower or 'limited assurance' in answer_lower or 'tuv' in answer_lower:
                                data.external_assessment = 'Yes'
                                data.external_agency = self.clean_text(answer)

            # Look for GHG reduction projects (Principle 6, Question 8)
            # Multiple pattern variations to catch different HTML formats
            ghg_project_table = (
                'project related to reducing' in table_text or
                'reducing green house gas' in table_text or
                'reducing greenhouse gas' in table_text or
                ('project' in table_text and 'ghg' in table_text) or
                ('project' in table_text and 'emission' in table_text and 'reducing' in table_text) or
                ('green house' in table_text and 'emission' in table_text) or
                ('greenhouse' in table_text and 'emission' in table_text)
            )
            if ghg_project_table:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        # Broader matching for the question about GHG reduction projects
                        is_ghg_project_question = (
                            ('project' in question and ('reducing' in question or 'ghg' in question or 'greenhouse' in question or 'emission' in question)) or
                            ('green house' in question and 'emission' in question) or
                            ('greenhouse gas' in question) or
                            ('ghg emission' in question)
                        )
                        if is_ghg_project_question:
                            answer = row[1].strip()
                            answer_lower = answer.lower()
                            # Check for Not Applicable first (various formats)
                            if 'not applicable' in answer_lower or answer_lower == 'na' or answer_lower == 'n/a' or answer_lower == 'n.a.' or answer_lower == 'n. a.':
                                data.has_reduction_project = 'Not Applicable'
                                data.reduction_project_na_explanation = self.clean_text(answer) if len(answer) > 15 else 'Not Applicable'
                            # Check for Yes with details
                            elif answer_lower.startswith('yes') or (len(answer) > 30 and 'not applicable' not in answer_lower and 'n/a' not in answer_lower):
                                data.has_reduction_project = 'Yes'
                                data.reduction_project_details = self.clean_text(answer)
                            # Check for No
                            elif answer_lower.startswith('no') and len(answer) < 50:
                                data.has_reduction_project = 'No'
                            # Capture any other substantive answer as details
                            elif len(answer) > 10:
                                data.has_reduction_project = 'Yes'
                                data.reduction_project_details = self.clean_text(answer)

        # Calculate totals if not already set
        if data.total_cy == 0 and (data.scope1_cy > 0 or data.scope2_cy > 0):
            data.total_cy = data.scope1_cy + data.scope2_cy
        if data.total_py == 0 and (data.scope1_py > 0 or data.scope2_py > 0):
            data.total_py = data.scope1_py + data.scope2_py

        logger.info(f"Extracted GHG data: has_reduction_project={data.has_reduction_project}, na_explanation={data.reduction_project_na_explanation[:50] if data.reduction_project_na_explanation else 'N/A'}")
        return data

    def extract_union_membership_data(self) -> UnionMembershipData:
        """Extract union/association membership data for employees and workers (Principle 3 Q7)."""
        data = UnionMembershipData()

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for union membership table
            if 'membership' in table_text and ('union' in table_text or 'association' in table_text):
                rows = self.extract_table_data(table)
                current_category = None  # Track if we're in employees or workers section

                for row in rows:
                    if len(row) >= 1:
                        label = row[0].lower()

                        # Detect category
                        if 'permanent employees' in label and 'worker' not in label:
                            current_category = 'permanent_employees'
                        elif 'permanent workers' in label:
                            current_category = 'permanent_workers'

                        # Parse data rows (Total, Male, Female, Other)
                        if current_category and len(row) >= 4:
                            if 'total' in label and 'male' not in label and 'female' not in label:
                                cat = getattr(data, f'{current_category}_total')
                                cat.total_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                cat.members_cy = self.clean_number(row[2]) if len(row) > 2 else 0
                                cat.pct_cy = self.clean_number(row[3]) if len(row) > 3 else 0
                                if len(row) > 6:
                                    cat.total_py = self.clean_number(row[4]) if len(row) > 4 else 0
                                    cat.members_py = self.clean_number(row[5]) if len(row) > 5 else 0
                                    cat.pct_py = self.clean_number(row[6]) if len(row) > 6 else 0
                            elif 'male' in label and 'female' not in label:
                                cat = getattr(data, f'{current_category}_male')
                                cat.total_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                cat.members_cy = self.clean_number(row[2]) if len(row) > 2 else 0
                                cat.pct_cy = self.clean_number(row[3]) if len(row) > 3 else 0
                                if len(row) > 6:
                                    cat.total_py = self.clean_number(row[4]) if len(row) > 4 else 0
                                    cat.members_py = self.clean_number(row[5]) if len(row) > 5 else 0
                                    cat.pct_py = self.clean_number(row[6]) if len(row) > 6 else 0
                            elif 'female' in label:
                                cat = getattr(data, f'{current_category}_female')
                                cat.total_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                cat.members_cy = self.clean_number(row[2]) if len(row) > 2 else 0
                                cat.pct_cy = self.clean_number(row[3]) if len(row) > 3 else 0
                                if len(row) > 6:
                                    cat.total_py = self.clean_number(row[4]) if len(row) > 4 else 0
                                    cat.members_py = self.clean_number(row[5]) if len(row) > 5 else 0
                                    cat.pct_py = self.clean_number(row[6]) if len(row) > 6 else 0
                            elif 'other' in label:
                                cat = getattr(data, f'{current_category}_other')
                                cat.total_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                                cat.members_cy = self.clean_number(row[2]) if len(row) > 2 else 0
                                cat.pct_cy = self.clean_number(row[3]) if len(row) > 3 else 0
                                if len(row) > 6:
                                    cat.total_py = self.clean_number(row[4]) if len(row) > 4 else 0
                                    cat.members_py = self.clean_number(row[5]) if len(row) > 5 else 0
                                    cat.pct_py = self.clean_number(row[6]) if len(row) > 6 else 0

        return data

    def extract_safety_measures(self) -> tuple:
        """
        Extract safety-related text from Principle 3.

        Returns:
            tuple: (safe_workplace_measures, corrective_actions_safety)
        """
        safe_workplace_measures = ""
        corrective_actions_safety = ""

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for Q12: Describe measures for safe and healthy workplace
            if 'describe the measures taken by the entity to ensure a safe and healthy work' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'describe the measures' in question and 'safe and healthy' in question:
                            safe_workplace_measures = self.clean_text(row[1])
                            break

            # Look for Q15: Corrective actions for safety-related incidents
            if 'corrective action taken or underway to address safety-related incidents' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'corrective action' in question and 'safety' in question:
                            corrective_actions_safety = self.clean_text(row[1])
                            break

        logger.info(f"Extracted safety measures: Q12 found={bool(safe_workplace_measures)}, Q15 found={bool(corrective_actions_safety)}")
        return safe_workplace_measures, corrective_actions_safety

    def extract_grievance_mechanism_data(self) -> 'GrievanceMechanismData':
        """
        Extract grievance mechanism data for employees and workers (Principle 3 Q6).

        Returns:
            GrievanceMechanismData: Grievance mechanism information
        """
        data = GrievanceMechanismData()
        has_any_mechanism = False

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for grievance mechanism table (Q6: Is there a mechanism available...)
            if ('mechanism' in table_text and 'grievance' in table_text) or \
               ('receive' in table_text and 'redress' in table_text and 'grievance' in table_text):
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 2:
                        category = row[0].lower().strip()
                        answer = row[1].strip() if len(row) > 1 else ''
                        details = row[2].strip() if len(row) > 2 else answer  # Details may be in column 3

                        # Check if answer indicates "Yes"
                        is_yes = answer.lower().startswith('yes') or 'yes' in answer.lower()

                        # Parse by category
                        if 'permanent employee' in category and 'worker' not in category:
                            data.permanent_employees = 'Yes' if is_yes else 'No'
                            data.permanent_employees_details = self.clean_text(details) if is_yes else ''
                            if is_yes:
                                has_any_mechanism = True
                        elif 'other than permanent employee' in category or ('other' in category and 'employee' in category and 'permanent' in category):
                            data.other_employees = 'Yes' if is_yes else 'No'
                            data.other_employees_details = self.clean_text(details) if is_yes else ''
                            if is_yes:
                                has_any_mechanism = True
                        elif 'permanent worker' in category and 'employee' not in category:
                            data.permanent_workers = 'Yes' if is_yes else 'No'
                            data.permanent_workers_details = self.clean_text(details) if is_yes else ''
                            if is_yes:
                                has_any_mechanism = True
                        elif 'other than permanent worker' in category or ('other' in category and 'worker' in category and 'permanent' in category):
                            data.other_workers = 'Yes' if is_yes else 'No'
                            data.other_workers_details = self.clean_text(details) if is_yes else ''
                            if is_yes:
                                has_any_mechanism = True

        # Set the general mechanism flag based on whether any category has a mechanism
        data.has_mechanism = 'true' if has_any_mechanism else 'false'

        logger.info(f"Extracted grievance mechanism data: has_mechanism={data.has_mechanism}")
        return data

    def extract_revenue_from_operations(self) -> tuple:
        """
        Extract Revenue from Operations for current and previous year.
        This is typically found in Section A or financial data tables.

        Returns:
            tuple: (revenue_from_operations_cy, revenue_from_operations_py)
        """
        revenue_cy = 0
        revenue_py = 0

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for revenue/turnover tables
            if 'revenue from operations' in table_text or 'turnover' in table_text:
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 2:
                        label = row[0].lower()

                        # Match "Revenue from Operations" or similar
                        if 'revenue from operations' in label or ('revenue' in label and 'operations' in label):
                            revenue_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                            revenue_py = self.clean_number(row[2]) if len(row) > 2 else 0
                            break

                        # Alternative: Total Revenue / Turnover
                        elif ('total revenue' in label or 'total turnover' in label) and revenue_cy == 0:
                            revenue_cy = self.clean_number(row[1]) if len(row) > 1 else 0
                            revenue_py = self.clean_number(row[2]) if len(row) > 2 else 0

        logger.info(f"Extracted revenue from operations: CY={revenue_cy}, PY={revenue_py}")
        return revenue_cy, revenue_py

    def extract_p9_corrective_actions(self) -> str:
        """
        Extract Principle 9 Q6: Corrective actions on advertising, cyber security,
        recalls, and regulatory penalties.

        Returns:
            str: Corrective actions text
        """
        corrective_actions = ""

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for P9 Q6 related content
            if ('corrective action' in table_text and
                ('advertising' in table_text or 'cyber' in table_text or
                 'recall' in table_text or 'regulatory' in table_text)):
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()

                        # Match P9 Q6 question pattern
                        if ('corrective action' in question and
                            ('advertising' in question or 'cyber' in question or
                             'recall' in question or 'regulatory' in question or
                             'essential services' in question or 'data privacy' in question)):
                            corrective_actions = self.clean_text(row[1])
                            break

            # Alternative: look for the full question text
            if not corrective_actions and 'provide details of any corrective actions taken' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'provide details of any corrective actions taken' in question:
                            corrective_actions = self.clean_text(row[1])
                            break

        logger.info(f"Extracted P9 Q6 corrective actions: found={bool(corrective_actions)}")
        return corrective_actions

    def extract_principle7_data(self) -> dict:
        """
        Extract Principle 7 (Policy Advocacy) data - Trade and Industry Chamber Affiliations.

        Returns:
            dict: P7 data with number of affiliations and list of chamber details
        """
        p7_data = {
            'num_affiliations': 0,
            'affiliations': []  # List of {name: str, reach: str}
        }

        for table in self._tables:
            table_text = table.get_text().lower()
            rows = self.extract_table_data(table)

            # Look for trade/industry chambers table
            # Common patterns: "trade and industry chambers", "affiliations", "associations"
            if ('trade' in table_text and 'industry' in table_text) or \
               ('chamber' in table_text and 'association' in table_text) or \
               ('affiliation' in table_text and ('national' in table_text or 'state' in table_text)):

                # Check for header row patterns
                header_found = False
                for row in rows:
                    row_text = ' '.join(row).lower()

                    # Check if this is a header row
                    if 'name of' in row_text and ('reach' in row_text or 'national' in row_text or 'state' in row_text):
                        header_found = True
                        continue

                    # Skip header-like rows
                    if 's. no' in row_text or 'sr. no' in row_text or 'sl. no' in row_text:
                        header_found = True
                        continue

                    # If we have a data row after header
                    if header_found and len(row) >= 2:
                        # Try to extract name and reach
                        name = ''
                        reach = ''

                        # Handle different column layouts
                        if len(row) >= 3:
                            # Format: Sr.No | Name | Reach
                            # Check if first column is a number
                            try:
                                int(row[0].strip())
                                name = self.clean_text(row[1])
                                reach = self.clean_text(row[2]) if len(row) > 2 else 'National'
                            except ValueError:
                                # First column is not a number, use first two columns
                                name = self.clean_text(row[0])
                                reach = self.clean_text(row[1])
                        elif len(row) == 2:
                            name = self.clean_text(row[0])
                            reach = self.clean_text(row[1])

                        # Validate and normalize reach
                        if reach.lower() in ['national', 'state', 'international', 'regional', 'local']:
                            reach = reach.capitalize()
                        elif 'national' in reach.lower():
                            reach = 'National'
                        elif 'state' in reach.lower():
                            reach = 'State'
                        elif 'international' in reach.lower():
                            reach = 'International'
                        else:
                            reach = 'National'  # Default

                        # Add valid affiliation
                        if name and len(name) > 3:  # Filter out empty or too short names
                            p7_data['affiliations'].append({
                                'name': name,
                                'reach': reach
                            })

            # Also check for "Number of affiliations" row
            if 'affiliation' in table_text and ('trade' in table_text or 'industry' in table_text or 'chamber' in table_text):
                for row in rows:
                    if len(row) >= 2:
                        label = row[0].lower()
                        if 'number' in label and 'affiliation' in label:
                            try:
                                p7_data['num_affiliations'] = int(self.clean_number(row[1]))
                            except (ValueError, TypeError):
                                pass

        # If num_affiliations wasn't explicitly found, use count of affiliations
        if p7_data['num_affiliations'] == 0 and p7_data['affiliations']:
            p7_data['num_affiliations'] = len(p7_data['affiliations'])

        logger.info(f"Extracted P7 trade/industry affiliations: count={p7_data['num_affiliations']}, affiliations={len(p7_data['affiliations'])}")
        return p7_data

    def extract_principle9_data(self) -> dict:
        """
        Extract all Principle 9 (Consumer Responsibility) data.

        Returns:
            dict: Complete Principle 9 data including complaints, recalls, cyber security, etc.
        """
        # Initialize default structure
        p9_data = {
            'complaint_mechanism': '',  # Q1
            'env_social_pct': 0,  # Q2
            'safe_usage_pct': 0,  # Q2
            'recycling_pct': 0,  # Q2
            'complaints': {
                'data_privacy': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'advertising': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'cyber_security': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'essential_services': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'restrictive_trade': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'unfair_trade': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'other': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
            },
            'voluntary_recalls': 0,  # Q4
            'voluntary_recall_reason': 'NA',
            'forced_recalls': 0,
            'forced_recall_reason': 'NA',
            'cyber_policy': 'No',  # Q5
            'cyber_policy_weblink': '',
            'data_breaches': 0,
            'pii_breach_pct': 0,
            'data_breach_impact': 'NA',
            'corrective_actions_q6': '',  # Q6
            'product_info_link': '',  # Q7
            'consumer_education': '',
            'disruption_mechanism': '',
            'product_info_display': 'No',
            'product_info_display_details': '',
        }

        for table in self._tables:
            table_text = table.get_text().lower()
            rows = self.extract_table_data(table)

            # Q1: Mechanism to receive and respond to consumer complaints
            if 'mechanism' in table_text and 'consumer' in table_text and ('complaint' in table_text or 'feedback' in table_text):
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'mechanism' in question and ('receive' in question or 'respond' in question) and 'consumer' in question:
                            p9_data['complaint_mechanism'] = self.clean_text(row[1])

            # Q2: Turnover percentages for environmental/social parameters
            if ('turnover' in table_text or 'percentage' in table_text) and ('environmental' in table_text or 'social' in table_text or 'recycling' in table_text):
                for row in rows:
                    if len(row) >= 2:
                        label = row[0].lower()
                        value = self.clean_number(row[1]) if len(row) > 1 else 0

                        if 'environmental' in label and 'social' in label:
                            p9_data['env_social_pct'] = value
                        elif 'safe' in label and 'responsible' in label:
                            p9_data['safe_usage_pct'] = value
                        elif 'recycling' in label or 'disposal' in label:
                            p9_data['recycling_pct'] = value

            # Q3: Consumer complaints table
            if 'consumer' in table_text and 'complaint' in table_text and ('received' in table_text or 'pending' in table_text):
                # Detect if this is CY or PY section
                is_py_section = 'previous' in table_text or 'fy' in table_text and ('22' in table_text or '21' in table_text)
                suffix = '_py' if is_py_section else '_cy'

                for row in rows:
                    if len(row) >= 2:
                        category = row[0].lower().strip()

                        # Map category names to keys
                        category_map = {
                            'data privacy': 'data_privacy',
                            'advertising': 'advertising',
                            'cyber-security': 'cyber_security',
                            'cyber security': 'cyber_security',
                            'delivery of essential services': 'essential_services',
                            'essential services': 'essential_services',
                            'restrictive trade practices': 'restrictive_trade',
                            'restrictive trade': 'restrictive_trade',
                            'unfair trade practices': 'unfair_trade',
                            'unfair trade': 'unfair_trade',
                            'other': 'other',
                        }

                        for cat_name, cat_key in category_map.items():
                            if cat_name in category:
                                # Parse columns: typically [category, received, pending, remarks]
                                if len(row) >= 2:
                                    p9_data['complaints'][cat_key][f'received{suffix}'] = self.clean_number(row[1])
                                if len(row) >= 3:
                                    p9_data['complaints'][cat_key][f'pending{suffix}'] = self.clean_number(row[2])
                                if len(row) >= 4:
                                    remark = self.clean_text(row[3])
                                    p9_data['complaints'][cat_key][f'remark{suffix}'] = remark if remark else 'NA'
                                break

            # Q4: Product recalls
            if 'recall' in table_text and ('voluntary' in table_text or 'forced' in table_text):
                for row in rows:
                    if len(row) >= 2:
                        label = row[0].lower()

                        if 'voluntary' in label and 'number' in label:
                            p9_data['voluntary_recalls'] = self.clean_number(row[1])
                        elif 'voluntary' in label and 'reason' in label:
                            p9_data['voluntary_recall_reason'] = self.clean_text(row[1]) or 'NA'
                        elif 'forced' in label and 'number' in label:
                            p9_data['forced_recalls'] = self.clean_number(row[1])
                        elif 'forced' in label and 'reason' in label:
                            p9_data['forced_recall_reason'] = self.clean_text(row[1]) or 'NA'

            # Q5: Cyber security policy
            if 'cyber' in table_text and ('security' in table_text or 'policy' in table_text or 'data privacy' in table_text):
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        answer = row[1].strip()

                        if 'framework' in question or 'policy' in question:
                            if 'cyber' in question and 'data privacy' in question:
                                p9_data['cyber_policy'] = 'Yes' if answer.lower().startswith('yes') else 'No'
                                if not answer.lower().startswith('yes') and not answer.lower().startswith('no'):
                                    # May contain the weblink directly
                                    p9_data['cyber_policy'] = 'Yes'
                                    if 'http' in answer.lower() or 'www' in answer.lower():
                                        p9_data['cyber_policy_weblink'] = self.clean_text(answer)
                        elif 'web' in question or 'link' in question:
                            p9_data['cyber_policy_weblink'] = self.clean_text(answer)
                        elif 'data breach' in question and 'number' in question:
                            p9_data['data_breaches'] = self.clean_number(answer)
                        elif 'personally identifiable' in question or 'pii' in question:
                            p9_data['pii_breach_pct'] = self.clean_number(answer)
                        elif 'impact' in question and 'data breach' in question:
                            p9_data['data_breach_impact'] = self.clean_text(answer) or 'NA'

            # Q6: Corrective actions (already handled by extract_p9_corrective_actions, but include here too)
            if 'corrective action' in table_text and ('advertising' in table_text or 'cyber' in table_text or 'recall' in table_text):
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'corrective action' in question:
                            p9_data['corrective_actions_q6'] = self.clean_text(row[1])

            # Q7: Product information
            if 'product' in table_text and ('information' in table_text or 'consumer' in table_text or 'education' in table_text):
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        answer = row[1].strip()

                        if 'weblink' in question or ('web' in question and 'link' in question) or 'url' in question:
                            p9_data['product_info_link'] = self.clean_text(answer)
                        elif 'steps' in question and ('inform' in question or 'educate' in question) and 'consumer' in question:
                            p9_data['consumer_education'] = self.clean_text(answer)
                        elif 'mechanism' in question and ('disruption' in question or 'discontinuation' in question):
                            p9_data['disruption_mechanism'] = self.clean_text(answer)
                        elif 'display' in question and 'product information' in question:
                            if 'details' in question:
                                p9_data['product_info_display_details'] = self.clean_text(answer)
                            else:
                                p9_data['product_info_display'] = 'Yes' if answer.lower().startswith('yes') else 'No'

        logger.info(f"Extracted Principle 9 data: complaints found, cyber_policy={p9_data['cyber_policy']}")
        return p9_data

    def extract_stakeholder_engagement(self) -> dict:
        """
        Extract Principle 4 Stakeholder Engagement data.

        Returns:
            dict: Contains stakeholder_groups list and related fields
        """
        result = {
            'stakeholder_groups': [],
            'identification_process': '',
            'consultation_process': '',
            'consultation_used': 'Yes',
            'consultation_details': '',
            'vulnerable_marginalized_actions': '',
        }

        # Common stakeholder names to identify
        stakeholder_keywords = [
            'supplier', 'business partner', 'shareholder', 'investor',
            'customer', 'employee', 'community', 'government', 'regulator',
            'ngo', 'media', 'worker', 'distributor', 'dealer', 'vendor'
        ]

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for stakeholder engagement table (has stakeholder group + channels + frequency)
            if ('stakeholder' in table_text and
                ('channel' in table_text or 'frequency' in table_text or 'engagement' in table_text)):
                rows = self.extract_table_data(table)

                # Check if this is the stakeholder groups table
                header_found = False
                for i, row in enumerate(rows):
                    row_text = ' '.join(row).lower()

                    # Skip header rows
                    if 'stakeholder group' in row_text and ('channel' in row_text or 'vulnerable' in row_text):
                        header_found = True
                        continue

                    if header_found and len(row) >= 4:
                        # Check if first cell contains a stakeholder name
                        first_cell = row[0].lower()
                        is_stakeholder = any(kw in first_cell for kw in stakeholder_keywords)

                        if is_stakeholder or (first_cell and len(first_cell) > 2 and first_cell not in ['s.no', 'sr.', 'no.', 'sl.']):
                            stakeholder = StakeholderEngagement()

                            # Parse based on column position
                            stakeholder.name = self.clean_text(row[0]) if len(row) > 0 else ''

                            # Vulnerable/Marginalized (usually Yes/No or true/false)
                            if len(row) > 1:
                                vuln = row[1].lower().strip()
                                if 'yes' in vuln or 'true' in vuln:
                                    stakeholder.vulnerable_marginalized = 'true'
                                else:
                                    stakeholder.vulnerable_marginalized = 'false'

                            # Channels of communication
                            if len(row) > 2:
                                channels = row[2].strip()
                                # Map to standard values
                                if channels:
                                    stakeholder.channels = 'Other'
                                    stakeholder.channels_details = self.clean_text(channels)

                            # Frequency of engagement
                            if len(row) > 3:
                                freq = row[3].strip().lower()
                                if 'annual' in freq:
                                    stakeholder.frequency = 'Annually'
                                elif 'half year' in freq or 'semi' in freq:
                                    stakeholder.frequency = 'Half yearly'
                                elif 'quarter' in freq:
                                    if 'more than' in freq:
                                        stakeholder.frequency = 'More than once a quarter'
                                    else:
                                        stakeholder.frequency = 'Quarterly'
                                else:
                                    stakeholder.frequency = 'Others – please specify'
                                    stakeholder.frequency_details = self.clean_text(row[3])

                            # Purpose and scope (usually last column or combined)
                            if len(row) > 4:
                                stakeholder.purpose_scope = self.clean_text(row[4])
                            elif len(row) > 3 and not stakeholder.purpose_scope:
                                # Sometimes purpose is in the last available column
                                stakeholder.purpose_scope = self.clean_text(row[-1])

                            if stakeholder.name:
                                result['stakeholder_groups'].append(stakeholder)

            # Look for identification process
            if 'process' in table_text and 'identifying' in table_text and 'stakeholder' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'process' in question and 'identifying' in question and 'stakeholder' in question:
                            result['identification_process'] = self.clean_text(row[1])
                            break

            # Look for consultation process
            if 'consultation' in table_text and 'board' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'consultation' in question and 'board' in question:
                            result['consultation_process'] = self.clean_text(row[1])
                            break

            # Look for vulnerable/marginalized actions
            if 'vulnerable' in table_text and 'marginalized' in table_text:
                rows = self.extract_table_data(table)
                for row in rows:
                    if len(row) >= 2:
                        question = row[0].lower()
                        if 'vulnerable' in question and 'marginalized' in question and 'action' in question:
                            result['vulnerable_marginalized_actions'] = self.clean_text(row[1])
                            break

        logger.info(f"Extracted stakeholder engagement: {len(result['stakeholder_groups'])} groups found")
        return result

    def extract_parental_leave_data(self) -> dict:
        """
        Extract parental leave return-to-work and retention rates by gender.

        Returns:
            dict: Parental leave data with male, female, others, and total categories
        """
        result = {
            'male': {'emp_return': 0, 'emp_retention': 0, 'worker_return': 0, 'worker_retention': 0},
            'female': {'emp_return': 0, 'emp_retention': 0, 'worker_return': 0, 'worker_retention': 0},
            'others': {'emp_return': 0, 'emp_retention': 0, 'worker_return': 0, 'worker_retention': 0},
            'total': {'emp_return': 0, 'emp_retention': 0, 'worker_return': 0, 'worker_retention': 0},
        }

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for parental leave table
            if ('parental leave' in table_text or 'maternity' in table_text or 'paternity' in table_text) and \
               ('return to work' in table_text or 'retention' in table_text):
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 3:
                        label = row[0].lower()

                        # Permanent Employees - Return to Work
                        if 'return to work' in label and 'employee' in label:
                            if 'male' in label and 'female' not in label:
                                result['male']['emp_return'] = self.clean_number(row[1])
                            elif 'female' in label:
                                result['female']['emp_return'] = self.clean_number(row[1])
                            elif 'other' in label:
                                result['others']['emp_return'] = self.clean_number(row[1])
                            elif 'total' in label:
                                result['total']['emp_return'] = self.clean_number(row[1])

                        # Permanent Employees - Retention
                        elif 'retention' in label and 'employee' in label:
                            if 'male' in label and 'female' not in label:
                                result['male']['emp_retention'] = self.clean_number(row[1])
                            elif 'female' in label:
                                result['female']['emp_retention'] = self.clean_number(row[1])
                            elif 'other' in label:
                                result['others']['emp_retention'] = self.clean_number(row[1])
                            elif 'total' in label:
                                result['total']['emp_retention'] = self.clean_number(row[1])

                        # Permanent Workers - Return to Work
                        elif 'return to work' in label and 'worker' in label:
                            if 'male' in label and 'female' not in label:
                                result['male']['worker_return'] = self.clean_number(row[1])
                            elif 'female' in label:
                                result['female']['worker_return'] = self.clean_number(row[1])
                            elif 'other' in label:
                                result['others']['worker_return'] = self.clean_number(row[1])
                            elif 'total' in label:
                                result['total']['worker_return'] = self.clean_number(row[1])

                        # Permanent Workers - Retention
                        elif 'retention' in label and 'worker' in label:
                            if 'male' in label and 'female' not in label:
                                result['male']['worker_retention'] = self.clean_number(row[1])
                            elif 'female' in label:
                                result['female']['worker_retention'] = self.clean_number(row[1])
                            elif 'other' in label:
                                result['others']['worker_retention'] = self.clean_number(row[1])
                            elif 'total' in label:
                                result['total']['worker_retention'] = self.clean_number(row[1])

                # Alternative table structure - rows by gender
                for i, row in enumerate(rows):
                    if len(row) >= 5:
                        label = row[0].lower()
                        # Check for header row patterns
                        if 'male' in label and 'female' not in label:
                            result['male']['emp_return'] = self.clean_number(row[1]) if len(row) > 1 else 0
                            result['male']['emp_retention'] = self.clean_number(row[2]) if len(row) > 2 else 0
                            result['male']['worker_return'] = self.clean_number(row[3]) if len(row) > 3 else 0
                            result['male']['worker_retention'] = self.clean_number(row[4]) if len(row) > 4 else 0
                        elif 'female' in label:
                            result['female']['emp_return'] = self.clean_number(row[1]) if len(row) > 1 else 0
                            result['female']['emp_retention'] = self.clean_number(row[2]) if len(row) > 2 else 0
                            result['female']['worker_return'] = self.clean_number(row[3]) if len(row) > 3 else 0
                            result['female']['worker_retention'] = self.clean_number(row[4]) if len(row) > 4 else 0
                        elif 'other' in label:
                            result['others']['emp_return'] = self.clean_number(row[1]) if len(row) > 1 else 0
                            result['others']['emp_retention'] = self.clean_number(row[2]) if len(row) > 2 else 0
                            result['others']['worker_return'] = self.clean_number(row[3]) if len(row) > 3 else 0
                            result['others']['worker_retention'] = self.clean_number(row[4]) if len(row) > 4 else 0
                        elif 'total' in label:
                            result['total']['emp_return'] = self.clean_number(row[1]) if len(row) > 1 else 0
                            result['total']['emp_retention'] = self.clean_number(row[2]) if len(row) > 2 else 0
                            result['total']['worker_return'] = self.clean_number(row[3]) if len(row) > 3 else 0
                            result['total']['worker_retention'] = self.clean_number(row[4]) if len(row) > 4 else 0

        logger.info(f"Extracted parental leave data: male={result['male']}, female={result['female']}")
        return result

    def extract_minimum_wage_data(self) -> dict:
        """
        Extract minimum wage compliance data for employees and workers.

        Returns:
            dict: Minimum wage data with perm_emp, other_emp, perm_workers, other_workers categories
        """
        # Helper function to create gender data structure
        def create_gender_data():
            return {
                'total_cy': 0, 'equal_cy': 0, 'equal_pct_cy': 0.0, 'more_cy': 0, 'more_pct_cy': 0.0,
                'total_py': 0, 'equal_py': 0, 'equal_pct_py': 0.0, 'more_py': 0, 'more_pct_py': 0.0
            }

        def create_category_data():
            return {
                'male': create_gender_data(),
                'female': create_gender_data(),
                'other': create_gender_data(),
                'total': create_gender_data()
            }

        result = {
            'perm_emp': create_category_data(),
            'other_emp': create_category_data(),
            'perm_workers': create_category_data(),
            'other_workers': create_category_data()
        }

        current_category = None
        current_year = 'cy'  # Default to current year

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for minimum wage table
            if 'minimum wage' in table_text:
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 1:
                        label = row[0].lower().strip()

                        # Detect category headers
                        if 'permanent employee' in label and 'other than' not in label:
                            current_category = 'perm_emp'
                        elif 'other than permanent employee' in label:
                            current_category = 'other_emp'
                        elif 'permanent worker' in label and 'other than' not in label:
                            current_category = 'perm_workers'
                        elif 'other than permanent worker' in label:
                            current_category = 'other_workers'

                        # Detect year
                        if 'current' in label or 'fy' in label and ('2024' in label or '2023-24' in label):
                            current_year = 'cy'
                        elif 'previous' in label or 'fy' in label and ('2023' in label or '2022-23' in label):
                            current_year = 'py'

                        # Extract gender data
                        if current_category and len(row) >= 6:
                            gender_key = None
                            if 'male' in label and 'female' not in label:
                                gender_key = 'male'
                            elif 'female' in label:
                                gender_key = 'female'
                            elif 'other' in label:
                                gender_key = 'other'
                            elif 'total' in label:
                                gender_key = 'total'

                            if gender_key:
                                cat_data = result[current_category][gender_key]
                                # Row format: Gender | Total | Equal No | Equal % | More No | More %
                                cat_data[f'total_{current_year}'] = self.clean_number(row[1]) if len(row) > 1 else 0
                                cat_data[f'equal_{current_year}'] = self.clean_number(row[2]) if len(row) > 2 else 0
                                cat_data[f'equal_pct_{current_year}'] = self.clean_number(row[3]) if len(row) > 3 else 0.0
                                cat_data[f'more_{current_year}'] = self.clean_number(row[4]) if len(row) > 4 else 0
                                cat_data[f'more_pct_{current_year}'] = self.clean_number(row[5]) if len(row) > 5 else 0.0

        logger.info(f"Extracted minimum wage data for {len(result)} categories")
        return result

    def extract_retirement_benefits_data(self) -> dict:
        """
        Extract retirement benefits data (PF, Gratuity, ESI, Others).

        Table format:
        Benefits | FY Current (No. of employees %, No. of workers %, Deposited) | FY Previous (No. of employees %, No. of workers %, Deposited)
        PF | 98.28% | 0% | Y | 97.02% | 0% | Y
        Gratuity | 100% | 0% | Y | 100% | 0% | Y
        ESI | 4.31% | 0% | Y | 4.72% | 0% | Y
        Others | N.A | N.A | N.A | N.A | N.A | N.A

        Returns:
            dict: Retirement benefits data for pf, gratuity, esi, others
        """
        result = {
            'pf': {'emp_cy': 0, 'worker_cy': 0, 'deposited_cy': 'N', 'emp_py': 0, 'worker_py': 0, 'deposited_py': 'N'},
            'gratuity': {'emp_cy': 0, 'worker_cy': 0, 'deposited_cy': 'N', 'emp_py': 0, 'worker_py': 0, 'deposited_py': 'N'},
            'esi': {'emp_cy': 0, 'worker_cy': 0, 'deposited_cy': 'N', 'emp_py': 0, 'worker_py': 0, 'deposited_py': 'N'},
            'others': {'name_cy': 'NA', 'emp_cy': 0, 'worker_cy': 0, 'deposited_cy': 'NA', 'name_py': 'NA', 'emp_py': 0, 'worker_py': 0, 'deposited_py': 'NA'},
        }

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for retirement benefits table
            if ('retirement' in table_text or 'pf' in table_text or 'provident fund' in table_text) and \
               ('gratuity' in table_text or 'esi' in table_text):
                rows = self.extract_table_data(table)

                for row in rows:
                    if len(row) >= 4:
                        label = row[0].lower().strip()

                        # Determine benefit type
                        benefit_key = None
                        if 'pf' in label or 'provident fund' in label:
                            benefit_key = 'pf'
                        elif 'gratuity' in label:
                            benefit_key = 'gratuity'
                        elif 'esi' in label or 'employee state insurance' in label:
                            benefit_key = 'esi'
                        elif 'other' in label:
                            benefit_key = 'others'

                        if benefit_key:
                            # Parse based on expected column structure
                            # Columns: [Benefit, Emp% CY, Worker% CY, Deposited CY, Emp% PY, Worker% PY, Deposited PY]
                            if len(row) >= 7:
                                if benefit_key == 'others':
                                    # For Others, extract name if available (row[0] is label, may contain name)
                                    name_val = row[0].strip()
                                    if name_val.lower() not in ['other', 'others', 'other benefits', 'others benefits']:
                                        result[benefit_key]['name_cy'] = name_val
                                        result[benefit_key]['name_py'] = name_val
                                    else:
                                        # Check if values are N.A.
                                        if 'n.a' in row[1].lower() or 'na' in row[1].lower() or row[1].strip() == '-':
                                            result[benefit_key]['name_cy'] = 'NA'
                                            result[benefit_key]['emp_cy'] = 0
                                            result[benefit_key]['worker_cy'] = 0
                                            result[benefit_key]['deposited_cy'] = 'NA'
                                            result[benefit_key]['name_py'] = 'NA'
                                            result[benefit_key]['emp_py'] = 0
                                            result[benefit_key]['worker_py'] = 0
                                            result[benefit_key]['deposited_py'] = 'NA'
                                            continue

                                result[benefit_key]['emp_cy'] = self.clean_number(row[1])
                                result[benefit_key]['worker_cy'] = self.clean_number(row[2])
                                result[benefit_key]['deposited_cy'] = 'Y' if row[3].strip().upper() in ['Y', 'YES', 'TRUE'] else 'N'
                                result[benefit_key]['emp_py'] = self.clean_number(row[4])
                                result[benefit_key]['worker_py'] = self.clean_number(row[5])
                                result[benefit_key]['deposited_py'] = 'Y' if row[6].strip().upper() in ['Y', 'YES', 'TRUE'] else 'N'
                            elif len(row) >= 4:
                                # Simplified structure (just CY data)
                                result[benefit_key]['emp_cy'] = self.clean_number(row[1])
                                result[benefit_key]['worker_cy'] = self.clean_number(row[2])
                                result[benefit_key]['deposited_cy'] = 'Y' if row[3].strip().upper() in ['Y', 'YES', 'TRUE'] else 'N'

        logger.info(f"Extracted retirement benefits data: pf={result['pf']}, gratuity={result['gratuity']}")
        return result

    def extract_employee_wellbeing_data(self) -> dict:
        """
        Extract employee/worker wellbeing measures data (Table 1.a and 1.b).

        Table format for employees:
        Category | Total (A) | Health Insurance (Num, %) | Accident Insurance (Num, %) |
                             Maternity Benefits (Num, %) | Paternity Benefits (Num, %) | Day Care (Num, %)

        Returns:
            dict: Employee and worker wellbeing data by category and gender
        """
        def create_gender_template():
            return {
                'male': {'total': 0, 'health_num': 0, 'health_pct': 0, 'accident_num': 0, 'accident_pct': 0,
                         'maternity_num': 0, 'maternity_pct': 0, 'paternity_num': 0, 'paternity_pct': 0,
                         'daycare_num': 0, 'daycare_pct': 0},
                'female': {'total': 0, 'health_num': 0, 'health_pct': 0, 'accident_num': 0, 'accident_pct': 0,
                           'maternity_num': 0, 'maternity_pct': 0, 'paternity_num': 0, 'paternity_pct': 0,
                           'daycare_num': 0, 'daycare_pct': 0},
                'others': {'total': 0, 'health_num': 0, 'health_pct': 0, 'accident_num': 0, 'accident_pct': 0,
                           'maternity_num': 0, 'maternity_pct': 0, 'paternity_num': 0, 'paternity_pct': 0,
                           'daycare_num': 0, 'daycare_pct': 0},
                'total': {'total': 0, 'health_num': 0, 'health_pct': 0, 'accident_num': 0, 'accident_pct': 0,
                          'maternity_num': 0, 'maternity_pct': 0, 'paternity_num': 0, 'paternity_pct': 0,
                          'daycare_num': 0, 'daycare_pct': 0},
            }

        result = {
            'employees': {
                'permanent': create_gender_template(),
                'other_than_permanent': create_gender_template(),
            },
            'workers': {
                'permanent': create_gender_template(),
                'other_than_permanent': create_gender_template(),
            },
        }

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for employee wellbeing table (1.a - employees)
            if ('health insurance' in table_text and 'accident insurance' in table_text and
                ('maternity' in table_text or 'paternity' in table_text)):

                rows = self.extract_table_data(table)
                current_category = None  # 'permanent' or 'other_than_permanent'
                current_type = 'employees'  # 'employees' or 'workers'

                # Determine if this is employees or workers table
                if 'worker' in table_text and 'employee' not in table_text:
                    current_type = 'workers'
                elif 'employee' in table_text:
                    current_type = 'employees'

                for row in rows:
                    if len(row) < 1:
                        continue

                    row_label = row[0].lower().strip()

                    # Detect category headers (handles both singular and plural forms)
                    # Note: Header rows may have only 1 cell (e.g., "Permanent employees")
                    if ('permanent employee' in row_label or 'permanent employees' in row_label) and 'other' not in row_label:
                        current_category = 'permanent'
                        current_type = 'employees'
                        continue
                    elif 'other than permanent employee' in row_label or 'other than permanent employees' in row_label:
                        current_category = 'other_than_permanent'
                        current_type = 'employees'
                        continue
                    elif ('permanent worker' in row_label or 'permanent workers' in row_label) and 'other' not in row_label:
                        current_category = 'permanent'
                        current_type = 'workers'
                        continue
                    elif 'other than permanent worker' in row_label or 'other than permanent workers' in row_label:
                        current_category = 'other_than_permanent'
                        current_type = 'workers'
                        continue

                    if current_category is None:
                        continue

                    # Determine gender from row label
                    gender_key = None
                    if row_label == 'male':
                        gender_key = 'male'
                    elif row_label == 'female':
                        gender_key = 'female'
                    elif row_label == 'others':
                        gender_key = 'others'
                    elif row_label == 'total':
                        gender_key = 'total'

                    if gender_key and len(row) >= 12:
                        # Column structure:
                        # [0] Category, [1] Total(A),
                        # [2] Health Num, [3] Health %,
                        # [4] Accident Num, [5] Accident %,
                        # [6] Maternity Num, [7] Maternity %,
                        # [8] Paternity Num, [9] Paternity %,
                        # [10] Day Care Num, [11] Day Care %
                        data = result[current_type][current_category][gender_key]
                        data['total'] = self.clean_number(row[1])
                        data['health_num'] = self.clean_number(row[2])
                        data['health_pct'] = self.clean_number(row[3])
                        data['accident_num'] = self.clean_number(row[4])
                        data['accident_pct'] = self.clean_number(row[5])
                        data['maternity_num'] = self.clean_number(row[6])
                        data['maternity_pct'] = self.clean_number(row[7])
                        data['paternity_num'] = self.clean_number(row[8])
                        data['paternity_pct'] = self.clean_number(row[9])
                        data['daycare_num'] = self.clean_number(row[10])
                        data['daycare_pct'] = self.clean_number(row[11])

                        logger.debug(f"Extracted wellbeing for {current_type}/{current_category}/{gender_key}: total={data['total']}")

        logger.info(f"Extracted employee wellbeing data")
        return result

    def extract_performance_career_data(self) -> dict:
        """
        Extract Section 9: Performance and career development reviews data.

        Table format:
        Category | FY Current (Total A, No. B, %B/A) | FY Previous (Total D, No. C, %C/D)
        Employees: Male, Female, Others, Total
        Workers: Male, Female, Others, Total

        Returns:
            dict: Performance and career development data by category and gender
        """
        def create_gender_template():
            return {
                'male': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                'female': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                'others': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                'total': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
            }

        result = {
            'employees': create_gender_template(),
            'workers': create_gender_template(),
        }

        for table in self._tables:
            table_text = table.get_text().lower()
            rows = self.extract_table_data(table)

            # Look for performance and career development table (Section 9)
            # Specific criteria: has headers "Total (A)", "No.(B)", "%(B/A)" and rows for Employees/Workers
            if len(rows) < 2:
                continue

            # Check header row for distinctive pattern: "Total (A)", "No.(B)", "%(B/A)"
            header_text = ' '.join(rows[1]) if len(rows) > 1 else ''
            if not ('total (a)' in header_text.lower() and 'no.(b)' in header_text.lower() and '%(b/a)' in header_text.lower()):
                continue

            # Also verify this table has Employees/Workers rows
            row_labels = [row[0].lower().strip() for row in rows if row]
            if 'employees' not in row_labels or 'workers' not in row_labels:
                continue

            current_type = None  # 'employees' or 'workers'

            for row in rows:
                if len(row) < 1:
                    continue

                row_label = row[0].lower().strip()

                # Detect category headers
                if row_label == 'employees':
                    current_type = 'employees'
                    continue
                elif row_label == 'workers':
                    current_type = 'workers'
                    continue

                if current_type is None:
                    continue

                # Determine gender from row label
                gender_key = None
                if row_label == 'male':
                    gender_key = 'male'
                elif row_label == 'female':
                    gender_key = 'female'
                elif row_label == 'others':
                    gender_key = 'others'
                elif row_label == 'total':
                    gender_key = 'total'

                if gender_key and len(row) >= 7:
                    # Column structure:
                    # [0] Category
                    # [1] Total (A) CY, [2] No.(B) CY, [3] %(B/A) CY
                    # [4] Total (D) PY, [5] No.(C) PY, [6] %(C/D) PY
                    data = result[current_type][gender_key]
                    data['total_cy'] = self.clean_number(row[1])
                    data['reviewed_cy'] = self.clean_number(row[2])
                    # Handle percentage with % sign
                    pct_cy = row[3].replace('%', '').strip() if len(row) > 3 else '0'
                    data['pct_cy'] = self.clean_number(pct_cy)
                    data['total_py'] = self.clean_number(row[4]) if len(row) > 4 else 0
                    data['reviewed_py'] = self.clean_number(row[5]) if len(row) > 5 else 0
                    pct_py = row[6].replace('%', '').strip() if len(row) > 6 else '0'
                    data['pct_py'] = self.clean_number(pct_py)

                    logger.debug(f"Extracted performance for {current_type}/{gender_key}: total_cy={data['total_cy']}")

            # Found and processed the correct table, break
            break

        logger.info(f"Extracted performance and career development data")
        return result

    def extract_safety_incidents_data(self) -> dict:
        """
        Extract Section 11: Safety related incidents data.

        Table format:
        Safety Incident/Number | Category* | FY Current | FY Previous
        LTIFR | Employees/Workers | value | value
        Total recordable injuries | Employees/Workers | value | value
        No. of fatalities | Employees/Workers | value | value
        High consequence injury | Employees/Workers | value | value

        Returns:
            dict: Safety incidents data
        """
        result = {
            'ltifr_emp_cy': 0, 'ltifr_emp_py': 0,
            'ltifr_worker_cy': 0, 'ltifr_worker_py': 0,
            'injuries_emp_cy': 0, 'injuries_emp_py': 0,
            'injuries_worker_cy': 0, 'injuries_worker_py': 0,
            'fatalities_emp_cy': 0, 'fatalities_emp_py': 0,
            'fatalities_worker_cy': 0, 'fatalities_worker_py': 0,
            'high_consequence_emp_cy': 0, 'high_consequence_emp_py': 0,
            'high_consequence_worker_cy': 0, 'high_consequence_worker_py': 0,
        }

        for table in self._tables:
            table_text = table.get_text().lower()

            # Look for safety incidents table (has LTIFR)
            if 'ltifr' in table_text or 'lost time injury frequency rate' in table_text:
                rows = self.extract_table_data(table)
                current_incident = None  # 'ltifr', 'injuries', 'fatalities', 'high_consequence'

                for row in rows:
                    if len(row) < 2:
                        continue

                    row_label = row[0].lower().strip()

                    # Detect incident type from first column
                    if 'ltifr' in row_label or 'lost time injury' in row_label:
                        current_incident = 'ltifr'
                    elif 'total recordable' in row_label:
                        current_incident = 'injuries'
                    elif 'fatalities' in row_label or 'no. of fatalities' in row_label:
                        current_incident = 'fatalities'
                    elif 'high consequence' in row_label:
                        current_incident = 'high_consequence'

                    if not current_incident:
                        continue

                    # Determine category and values based on row structure
                    # Row with 4 cells: [Incident Name, Category, CY, PY] - first row of incident type
                    # Row with 3 cells: [Category, CY, PY] - continuation row
                    if len(row) == 4 and not row_label.startswith('employee') and not row_label.startswith('worker'):
                        # First row of incident type: [Incident, Category, CY, PY]
                        category = row[1].lower().strip()
                        cy_val = row[2]
                        py_val = row[3]
                    elif len(row) >= 3 and (row_label.startswith('employee') or row_label.startswith('worker')):
                        # Continuation row: [Category, CY, PY]
                        category = row_label
                        cy_val = row[1]
                        py_val = row[2]
                    else:
                        continue

                    if 'employee' in category or 'worker' in category:
                        is_employee = 'employee' in category
                        prefix = current_incident
                        suffix = 'emp' if is_employee else 'worker'

                        # Clean values - "-" means 0 or not applicable
                        cy_clean = 0 if cy_val.strip() in ['-', 'na', 'n/a', ''] else self.clean_number(cy_val)
                        py_clean = 0 if py_val.strip() in ['-', 'na', 'n/a', ''] else self.clean_number(py_val)

                        result[f'{prefix}_{suffix}_cy'] = cy_clean
                        result[f'{prefix}_{suffix}_py'] = py_clean

                        logger.debug(f"Extracted safety incident {prefix}_{suffix}: cy={cy_clean}, py={py_clean}")

                # Found the table, break
                break

        logger.info(f"Extracted safety incidents data: ltifr_emp_cy={result['ltifr_emp_cy']}")
        return result

    # =========================================================================
    # Main Extraction Method
    # =========================================================================

    def parse(self) -> BRSRReportData:
        """
        Parse complete BRSR report and return structured data.

        Returns:
            BRSRReportData: Complete extracted report data
        """
        logger.info("Starting BRSR report parsing...")

        data = BRSRReportData(
            # Section A
            company=self.extract_company_details(),
            assurance=self.extract_assurance_data(),
            business_activities=self.extract_business_activities(),
            products_services=self.extract_products_services(),
            locations=self.extract_locations(),
            markets=self.extract_markets(),
            employees_workers=self.extract_employees_workers(),
            women_representation=self.extract_women_representation(),
            turnover_rates=self.extract_turnover_rates(),
            subsidiaries=self.extract_subsidiaries(),
            csr=self.extract_csr_data(),
            complaints=self.extract_complaints(),
            material_issues=self.extract_material_issues(),

            # Section B
            principles=self.extract_section_b_principles(),
            **self.extract_governance_data(),  # Unpack director_statement, highest_authority, etc.

            # Section C
            sustainability=self.extract_sustainability_data(),
            waste=self.extract_waste_data(),
            accounts_payable=self.extract_accounts_payable_data(),
            water=self.extract_water_data(),
            energy=self.extract_energy_data(),
            ghg=self.extract_ghg_data(),
            union_membership=self.extract_union_membership_data(),
            grievance_mechanism=self.extract_grievance_mechanism_data(),
        )

        # Extract Principle 3 safety measures (Q12, Q15)
        safe_workplace, corrective_actions = self.extract_safety_measures()
        data.safe_workplace_measures = safe_workplace
        data.corrective_actions_safety = corrective_actions

        # Extract Revenue from Operations (for intensity calculations)
        revenue_cy, revenue_py = self.extract_revenue_from_operations()
        data.revenue_from_operations_cy = revenue_cy
        data.revenue_from_operations_py = revenue_py

        # Extract Principle 9 Q6: Corrective Actions
        data.corrective_actions_p9_q6 = self.extract_p9_corrective_actions()

        # Extract Complete Principle 9 Data (complaints, cyber security, product info, etc.)
        data.p9_data = self.extract_principle9_data()

        # Extract Principle 7 Data (trade/industry chamber affiliations)
        data.p7_data = self.extract_principle7_data()

        # Extract Principle 4: Stakeholder Engagement
        stakeholder_data = self.extract_stakeholder_engagement()
        data.stakeholder_groups = stakeholder_data['stakeholder_groups']
        data.stakeholder_identification_process = stakeholder_data['identification_process']
        data.stakeholder_consultation_process = stakeholder_data['consultation_process']
        data.stakeholder_consultation_used = stakeholder_data['consultation_used']
        data.stakeholder_consultation_details = stakeholder_data['consultation_details']
        data.vulnerable_marginalized_actions = stakeholder_data['vulnerable_marginalized_actions']

        # Extract Principle 3: Parental Leave Return/Retention Rates
        parental_leave_raw = self.extract_parental_leave_data()
        data.parental_leave = ParentalLeaveData(
            male=ParentalLeaveGender(**parental_leave_raw['male']),
            female=ParentalLeaveGender(**parental_leave_raw['female']),
            others=ParentalLeaveGender(**parental_leave_raw['others']),
            total=ParentalLeaveGender(**parental_leave_raw['total']),
        )

        # Extract Principle 5: Minimum Wages Compliance
        minimum_wage_raw = self.extract_minimum_wage_data()
        data.minimum_wages = MinimumWagesData(
            perm_emp=MinimumWageCategoryData(
                male=MinimumWageGenderData(**minimum_wage_raw['perm_emp']['male']),
                female=MinimumWageGenderData(**minimum_wage_raw['perm_emp']['female']),
                other=MinimumWageGenderData(**minimum_wage_raw['perm_emp']['other']),
                total=MinimumWageGenderData(**minimum_wage_raw['perm_emp']['total']),
            ),
            other_emp=MinimumWageCategoryData(
                male=MinimumWageGenderData(**minimum_wage_raw['other_emp']['male']),
                female=MinimumWageGenderData(**minimum_wage_raw['other_emp']['female']),
                other=MinimumWageGenderData(**minimum_wage_raw['other_emp']['other']),
                total=MinimumWageGenderData(**minimum_wage_raw['other_emp']['total']),
            ),
            perm_workers=MinimumWageCategoryData(
                male=MinimumWageGenderData(**minimum_wage_raw['perm_workers']['male']),
                female=MinimumWageGenderData(**minimum_wage_raw['perm_workers']['female']),
                other=MinimumWageGenderData(**minimum_wage_raw['perm_workers']['other']),
                total=MinimumWageGenderData(**minimum_wage_raw['perm_workers']['total']),
            ),
            other_workers=MinimumWageCategoryData(
                male=MinimumWageGenderData(**minimum_wage_raw['other_workers']['male']),
                female=MinimumWageGenderData(**minimum_wage_raw['other_workers']['female']),
                other=MinimumWageGenderData(**minimum_wage_raw['other_workers']['other']),
                total=MinimumWageGenderData(**minimum_wage_raw['other_workers']['total']),
            ),
        )

        # Extract Principle 3: Retirement Benefits (PF, Gratuity, ESI, Others)
        retirement_raw = self.extract_retirement_benefits_data()
        data.retirement_benefits = RetirementBenefitsData(
            pf=RetirementBenefitItem(**retirement_raw['pf']),
            gratuity=RetirementBenefitItem(**retirement_raw['gratuity']),
            esi=RetirementBenefitItem(**retirement_raw['esi']),
            others=OtherRetirementBenefitItem(**retirement_raw['others']),
        )

        # Extract Principle 3: Employee/Worker Wellbeing Measures (Table 1.a and 1.b)
        data.employee_wellbeing_data = self.extract_employee_wellbeing_data()

        # Extract Principle 3: Performance and Career Development (Section 9)
        data.performance_career_data = self.extract_performance_career_data()

        # Extract Principle 3: Safety Incidents (Section 11)
        data.safety_incidents_data = self.extract_safety_incidents_data()

        # Extract Principle 3 Q8: Training on Health & Safety and Skill Upgradation
        data.safety_skill_training = self.extract_safety_skill_training()

        logger.info(f"Parsing complete. Company: {data.company.company_name}")
        return data

    def validate(self) -> BRSRValidationResult:
        """
        Validate the BRSR HTML structure.

        Returns:
            BRSRValidationResult: Validation results with errors and warnings
        """
        result = BRSRValidationResult(table_count=len(self._tables))

        if len(self._tables) < 5:
            result.warnings.append(f"Only {len(self._tables)} tables found. BRSR reports typically have more.")

        # Check for required sections
        full_text = self.soup.get_text().lower()

        if 'section a' in full_text:
            result.sections_found.append('Section A: General Disclosures')
        else:
            result.errors.append("Section A not found")

        if 'section b' in full_text:
            result.sections_found.append('Section B: Management and Process Disclosures')
        else:
            result.warnings.append("Section B not found")

        if 'section c' in full_text:
            result.sections_found.append('Section C: Principle-wise Performance')
        else:
            result.warnings.append("Section C not found")

        result.is_valid = len(result.errors) == 0

        return result
