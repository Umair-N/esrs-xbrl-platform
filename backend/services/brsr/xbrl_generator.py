"""
BRSR XBRL Generator Service

Generates SEBI-compliant XBRL XML from parsed BRSR data.
Uses the complete Jinja2 template ported from the Jupyter notebook.
"""

import logging
import re
from typing import Dict, Any, Optional, List, Tuple
from datetime import date, datetime
from jinja2 import Template, Environment, BaseLoader, Undefined

from schemas.brsr import BRSRReportData
from .brsr_template import XBRL_TEMPLATE

logger = logging.getLogger(__name__)


class SilentUndefined(Undefined):
    """
    Custom Undefined class that returns sensible defaults instead of raising errors.
    Used to handle missing template variables gracefully.
    """
    def _fail_with_undefined_error(self, *args, **kwargs):
        """Override to return default instead of raising."""
        return ''

    def __str__(self):
        return ''

    def __int__(self):
        return 0

    def __float__(self):
        return 0.0

    def __bool__(self):
        return False

    def __iter__(self):
        return iter([])

    def __getattr__(self, name):
        return SilentUndefined()

    def __getitem__(self, key):
        return SilentUndefined()

    def __call__(self, *args, **kwargs):
        return SilentUndefined()


class BRSRXBRLGenerator:
    """
    Generates XBRL XML documents from BRSR report data.

    Uses the complete SEBI in-capmkt taxonomy for Indian listed entities.
    Supports multi-period reporting (CY, PY, PPY).
    """

    # Month name to number mapping
    MONTH_MAP = {
        'january': 1, 'jan': 1,
        'february': 2, 'feb': 2,
        'march': 3, 'mar': 3,
        'april': 4, 'apr': 4,
        'may': 5,
        'june': 6, 'jun': 6,
        'july': 7, 'jul': 7,
        'august': 8, 'aug': 8,
        'september': 9, 'sep': 9, 'sept': 9,
        'october': 10, 'oct': 10,
        'november': 11, 'nov': 11,
        'december': 12, 'dec': 12,
    }

    @classmethod
    def _parse_financial_year_text(cls, text: str) -> Tuple[Optional[date], Optional[date]]:
        """
        Parse financial year text to extract start and end dates.

        Handles various formats:
        - "1st April, 2023 to 31st March, 2024"
        - "April 1, 2023 to March 31, 2024"
        - "01-04-2023 to 31-03-2024"
        - "01/04/2023 to 31/03/2024"
        - "2023-04-01 to 2024-03-31"
        - "FY 2023-24"
        - "FY2023-24"

        Args:
            text: Financial year text from the report

        Returns:
            Tuple of (start_date, end_date), or (None, None) if parsing fails
        """
        if not text:
            return None, None

        text = text.strip().lower()

        # Pattern 1: "FY 2023-24" or "FY2023-24" or "F.Y. 2023-24"
        fy_pattern = r'f\.?y\.?\s*(\d{4})[-–](\d{2,4})'
        match = re.search(fy_pattern, text)
        if match:
            start_year = int(match.group(1))
            end_year_str = match.group(2)
            if len(end_year_str) == 2:
                # Convert 24 to 2024, handling century boundary
                end_year = int(f"{str(start_year)[:2]}{end_year_str}")
                if end_year < start_year:
                    end_year += 100  # Handle cases like 2099-00
            else:
                end_year = int(end_year_str)
            # Indian financial year: April 1 to March 31
            return date(start_year, 4, 1), date(end_year, 3, 31)

        # Pattern 2: Date with month name "1st April, 2023" or "April 1, 2023"
        # Split by "to" or "-" for range
        parts = re.split(r'\s+to\s+|–|-(?=\s*\d{1,2}(?:st|nd|rd|th)?\s+[a-z]|\s*[a-z]+\s+\d)', text, maxsplit=1)

        if len(parts) == 2:
            start_date = cls._parse_single_date(parts[0].strip())
            end_date = cls._parse_single_date(parts[1].strip())
            if start_date and end_date:
                return start_date, end_date

        # Pattern 3: Try to extract just year information for FY assumption
        year_pattern = r'(\d{4})\s*[-–]\s*(\d{2,4})'
        match = re.search(year_pattern, text)
        if match:
            start_year = int(match.group(1))
            end_year_str = match.group(2)
            if len(end_year_str) == 2:
                end_year = int(f"{str(start_year)[:2]}{end_year_str}")
                if end_year < start_year:
                    end_year += 100
            else:
                end_year = int(end_year_str)
            return date(start_year, 4, 1), date(end_year, 3, 31)

        return None, None

    @classmethod
    def _parse_single_date(cls, text: str) -> Optional[date]:
        """
        Parse a single date from text.

        Handles:
        - "1st April, 2023" or "1st April 2023"
        - "April 1, 2023" or "April 1 2023"
        - "01-04-2023" or "01/04/2023"
        - "2023-04-01"

        Args:
            text: Single date text

        Returns:
            date object or None if parsing fails
        """
        text = text.strip().lower()

        # Remove ordinal suffixes
        text = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', text)

        # Pattern 1: ISO format "2023-04-01"
        iso_match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', text)
        if iso_match:
            year, month, day = int(iso_match.group(1)), int(iso_match.group(2)), int(iso_match.group(3))
            try:
                return date(year, month, day)
            except ValueError:
                pass

        # Pattern 2: DD-MM-YYYY or DD/MM/YYYY
        dmy_match = re.search(r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})', text)
        if dmy_match:
            day, month, year = int(dmy_match.group(1)), int(dmy_match.group(2)), int(dmy_match.group(3))
            try:
                return date(year, month, day)
            except ValueError:
                pass

        # Pattern 3: "1 April, 2023" or "1 April 2023"
        day_month_year_match = re.search(r'(\d{1,2})\s*,?\s*([a-z]+)\s*,?\s*(\d{4})', text)
        if day_month_year_match:
            day = int(day_month_year_match.group(1))
            month_name = day_month_year_match.group(2).strip()
            year = int(day_month_year_match.group(3))
            month = cls.MONTH_MAP.get(month_name)
            if month:
                try:
                    return date(year, month, day)
                except ValueError:
                    pass

        # Pattern 4: "April 1, 2023" or "April 1 2023"
        month_day_year_match = re.search(r'([a-z]+)\s*(\d{1,2})\s*,?\s*(\d{4})', text)
        if month_day_year_match:
            month_name = month_day_year_match.group(1).strip()
            day = int(month_day_year_match.group(2))
            year = int(month_day_year_match.group(3))
            month = cls.MONTH_MAP.get(month_name)
            if month:
                try:
                    return date(year, month, day)
                except ValueError:
                    pass

        return None

    def __init__(
        self,
        report_data: BRSRReportData,
        start_date_cy: Optional[date] = None,
        end_date_cy: Optional[date] = None,
    ):
        """
        Initialize generator with report data and reporting period.

        Args:
            report_data: Parsed BRSR report data
            start_date_cy: Start date of current year reporting period
            end_date_cy: End date of current year reporting period
        """
        self.data = report_data

        # Try to extract dates from the financial_year field in report data
        parsed_start, parsed_end = None, None
        if hasattr(report_data, 'company') and hasattr(report_data.company, 'financial_year'):
            financial_year_text = report_data.company.financial_year
            if financial_year_text:
                parsed_start, parsed_end = self._parse_financial_year_text(financial_year_text)
                if parsed_start and parsed_end:
                    logger.info(f"Parsed financial year from report: {parsed_start} to {parsed_end}")

        # Use parsed dates if available, otherwise use provided parameters
        if parsed_start and start_date_cy is None:
            start_date_cy = parsed_start
        if parsed_end and end_date_cy is None:
            end_date_cy = parsed_end

        # Fall back to current fiscal year if still not specified
        today = date.today()
        if end_date_cy is None:
            # Default to March 31 of current year
            if today.month > 3:
                end_date_cy = date(today.year, 3, 31)
            else:
                end_date_cy = date(today.year - 1, 3, 31)
            logger.warning(f"Could not parse financial year from report, defaulting to: ending {end_date_cy}")

        if start_date_cy is None:
            start_date_cy = date(end_date_cy.year - 1, 4, 1)

        self.start_date_cy = start_date_cy
        self.end_date_cy = end_date_cy

        # Calculate previous years
        self.start_date_py = date(start_date_cy.year - 1, start_date_cy.month, start_date_cy.day)
        self.end_date_py = date(end_date_cy.year - 1, end_date_cy.month, end_date_cy.day)

        self.start_date_ppy = date(start_date_cy.year - 2, start_date_cy.month, start_date_cy.day)
        self.end_date_ppy = date(end_date_cy.year - 2, end_date_cy.month, end_date_cy.day)

        logger.info(f"XBRL Generator initialized for period {start_date_cy} to {end_date_cy}")

    def _format_date(self, d: date) -> str:
        """Format date as YYYY-MM-DD."""
        return d.strftime('%Y-%m-%d')

    def _get_cin(self) -> str:
        """Get CIN from report data or return placeholder."""
        return self.data.company.cin or 'L00000XX0000XXX000000'

    def _build_template_context(self) -> Dict[str, Any]:
        """Build complete Jinja2 template context from report data."""
        d = self.data

        # Build employee/worker data structure matching template expectations
        emp_workers = {
            'employees': {
                'permanent': {
                    'total': d.employees_workers.employees.permanent.total,
                    'male': d.employees_workers.employees.permanent.male,
                    'male_pct': d.employees_workers.employees.permanent.male_pct,
                    'female': d.employees_workers.employees.permanent.female,
                    'female_pct': d.employees_workers.employees.permanent.female_pct,
                    'other': d.employees_workers.employees.permanent.other,
                    'other_pct': d.employees_workers.employees.permanent.other_pct,
                },
                'other': {
                    'total': d.employees_workers.employees.other.total,
                    'male': d.employees_workers.employees.other.male,
                    'male_pct': d.employees_workers.employees.other.male_pct,
                    'female': d.employees_workers.employees.other.female,
                    'female_pct': d.employees_workers.employees.other.female_pct,
                    'other': d.employees_workers.employees.other.other,
                    'other_pct': d.employees_workers.employees.other.other_pct,
                },
                'total': {
                    'total': d.employees_workers.employees.total.total,
                    'male': d.employees_workers.employees.total.male,
                    'male_pct': d.employees_workers.employees.total.male_pct,
                    'female': d.employees_workers.employees.total.female,
                    'female_pct': d.employees_workers.employees.total.female_pct,
                    'other': d.employees_workers.employees.total.other,
                    'other_pct': d.employees_workers.employees.total.other_pct,
                },
            },
            'workers': {
                'permanent': {
                    'total': d.employees_workers.workers.permanent.total,
                    'male': d.employees_workers.workers.permanent.male,
                    'male_pct': d.employees_workers.workers.permanent.male_pct,
                    'female': d.employees_workers.workers.permanent.female,
                    'female_pct': d.employees_workers.workers.permanent.female_pct,
                    'other': d.employees_workers.workers.permanent.other,
                    'other_pct': d.employees_workers.workers.permanent.other_pct,
                },
                'other': {
                    'total': d.employees_workers.workers.other.total,
                    'male': d.employees_workers.workers.other.male,
                    'male_pct': d.employees_workers.workers.other.male_pct,
                    'female': d.employees_workers.workers.other.female,
                    'female_pct': d.employees_workers.workers.other.female_pct,
                    'other': d.employees_workers.workers.other.other,
                    'other_pct': d.employees_workers.workers.other.other_pct,
                },
                'total': {
                    'total': d.employees_workers.workers.total.total,
                    'male': d.employees_workers.workers.total.male,
                    'male_pct': d.employees_workers.workers.total.male_pct,
                    'female': d.employees_workers.workers.total.female,
                    'female_pct': d.employees_workers.workers.total.female_pct,
                    'other': d.employees_workers.workers.total.other,
                    'other_pct': d.employees_workers.workers.total.other_pct,
                },
            },
            'differently_abled_employees': {
                'permanent': {
                    'total': d.employees_workers.differently_abled_employees.permanent.total,
                    'male': d.employees_workers.differently_abled_employees.permanent.male,
                    'male_pct': d.employees_workers.differently_abled_employees.permanent.male_pct,
                    'female': d.employees_workers.differently_abled_employees.permanent.female,
                    'female_pct': d.employees_workers.differently_abled_employees.permanent.female_pct,
                    'other': d.employees_workers.differently_abled_employees.permanent.other,
                    'other_pct': d.employees_workers.differently_abled_employees.permanent.other_pct,
                },
                'other': {
                    'total': d.employees_workers.differently_abled_employees.other.total,
                    'male': d.employees_workers.differently_abled_employees.other.male,
                    'male_pct': d.employees_workers.differently_abled_employees.other.male_pct,
                    'female': d.employees_workers.differently_abled_employees.other.female,
                    'female_pct': d.employees_workers.differently_abled_employees.other.female_pct,
                    'other': d.employees_workers.differently_abled_employees.other.other,
                    'other_pct': d.employees_workers.differently_abled_employees.other.other_pct,
                },
                'total': {
                    'total': d.employees_workers.differently_abled_employees.total.total,
                    'male': d.employees_workers.differently_abled_employees.total.male,
                    'male_pct': d.employees_workers.differently_abled_employees.total.male_pct,
                    'female': d.employees_workers.differently_abled_employees.total.female,
                    'female_pct': d.employees_workers.differently_abled_employees.total.female_pct,
                    'other': d.employees_workers.differently_abled_employees.total.other,
                    'other_pct': d.employees_workers.differently_abled_employees.total.other_pct,
                },
            },
            'differently_abled_workers': {
                'permanent': {
                    'total': d.employees_workers.differently_abled_workers.permanent.total,
                    'male': d.employees_workers.differently_abled_workers.permanent.male,
                    'male_pct': d.employees_workers.differently_abled_workers.permanent.male_pct,
                    'female': d.employees_workers.differently_abled_workers.permanent.female,
                    'female_pct': d.employees_workers.differently_abled_workers.permanent.female_pct,
                    'other': d.employees_workers.differently_abled_workers.permanent.other,
                    'other_pct': d.employees_workers.differently_abled_workers.permanent.other_pct,
                },
                'other': {
                    'total': d.employees_workers.differently_abled_workers.other.total,
                    'male': d.employees_workers.differently_abled_workers.other.male,
                    'male_pct': d.employees_workers.differently_abled_workers.other.male_pct,
                    'female': d.employees_workers.differently_abled_workers.other.female,
                    'female_pct': d.employees_workers.differently_abled_workers.other.female_pct,
                    'other': d.employees_workers.differently_abled_workers.other.other,
                    'other_pct': d.employees_workers.differently_abled_workers.other.other_pct,
                },
                'total': {
                    'total': d.employees_workers.differently_abled_workers.total.total,
                    'male': d.employees_workers.differently_abled_workers.total.male,
                    'male_pct': d.employees_workers.differently_abled_workers.total.male_pct,
                    'female': d.employees_workers.differently_abled_workers.total.female,
                    'female_pct': d.employees_workers.differently_abled_workers.total.female_pct,
                    'other': d.employees_workers.differently_abled_workers.total.other,
                    'other_pct': d.employees_workers.differently_abled_workers.total.other_pct,
                },
            },
        }

        # Build turnover rates structure - matching template expected format
        turnover_rates = {
            'employees': {
                'cy': {
                    'male': d.turnover_rates.employees.cy.male,
                    'female': d.turnover_rates.employees.cy.female,
                    'other': d.turnover_rates.employees.cy.other,
                    'total': d.turnover_rates.employees.cy.total,
                },
                'py': {
                    'male': d.turnover_rates.employees.py.male,
                    'female': d.turnover_rates.employees.py.female,
                    'other': d.turnover_rates.employees.py.other,
                    'total': d.turnover_rates.employees.py.total,
                },
                'ppy': {
                    'male': d.turnover_rates.employees.ppy.male,
                    'female': d.turnover_rates.employees.ppy.female,
                    'other': d.turnover_rates.employees.ppy.other,
                    'total': d.turnover_rates.employees.ppy.total,
                },
            },
            'workers': {
                'cy': {
                    'male': d.turnover_rates.workers.cy.male,
                    'female': d.turnover_rates.workers.cy.female,
                    'other': d.turnover_rates.workers.cy.other,
                    'total': d.turnover_rates.workers.cy.total,
                },
                'py': {
                    'male': d.turnover_rates.workers.py.male,
                    'female': d.turnover_rates.workers.py.female,
                    'other': d.turnover_rates.workers.py.other,
                    'total': d.turnover_rates.workers.py.total,
                },
                'ppy': {
                    'male': d.turnover_rates.workers.ppy.male,
                    'female': d.turnover_rates.workers.ppy.female,
                    'other': d.turnover_rates.workers.ppy.other,
                    'total': d.turnover_rates.workers.ppy.total,
                },
            },
        }

        # Build women representation structure
        women_representation = {
            'board': {
                'total': d.women_representation.board.total,
                'female': d.women_representation.board.female,
                'pct': d.women_representation.board.pct,
            },
            'kmp': {
                'total': d.women_representation.kmp.total,
                'female': d.women_representation.kmp.female,
                'pct': d.women_representation.kmp.pct,
            },
        }

        # Build locations structure
        locations = {
            'national': {
                'plants': d.locations.national.plants,
                'offices': d.locations.national.offices,
                'total': d.locations.national.total,
            },
            'international': {
                'plants': d.locations.international.plants,
                'offices': d.locations.international.offices,
                'total': d.locations.international.total,
            },
        }

        # Build markets structure
        markets = {
            'national_states': d.markets.national_states,
            'national_states_count': d.markets.national_states_count,
            'international_countries': d.markets.international_countries,
            'international_countries_count': d.markets.international_countries_count,
            'export_pct': d.markets.export_pct,
            'customer_types_brief': d.markets.customer_types_brief,
        }

        # Build assurance structure
        assurance = {
            'has_assurance': d.assurance.has_assurance,
            'provider_name': d.assurance.provider_name or '',
            'assurance_type': d.assurance.assurance_type or '',
            'type_obtained': d.assurance.assurance_type or '',
            'section_a': 'Yes' if d.assurance.has_assurance == 'Yes' else 'No',
            'section_b': 'Yes' if d.assurance.has_assurance == 'Yes' else 'No',
            'section_c': 'Yes' if d.assurance.has_assurance == 'Yes' else 'No',
        }

        # Build CSR structure
        # Build CSR aspirational districts list
        csr_aspirational_districts = []
        if hasattr(d.csr, 'aspirational_districts'):
            for idx, project in enumerate(d.csr.aspirational_districts, start=1):
                csr_aspirational_districts.append({
                    'axis_id': f'CSRProjectsUndertakenAxis{idx}',
                    'state': project.state,
                    'aspirational_district': project.aspirational_district,
                    'amount_spent': int(project.amount_spent),  # Convert to int for XBRL
                })

        csr = {
            'applicable': d.csr.applicable if hasattr(d.csr, 'applicable') else 'Yes',
            'turnover': d.csr.turnover if hasattr(d.csr, 'turnover') else 0,
            'net_worth': d.csr.net_worth if hasattr(d.csr, 'net_worth') else 0,
            'aspirational_districts': csr_aspirational_districts,
        }

        # Build complaints list
        complaints = []
        for c in d.complaints:
            complaints.append({
                'stakeholder': c.stakeholder,
                'filed_cy': c.filed_cy,
                'filed_py': c.filed_py,
                'pending_cy': c.pending_cy,
                'pending_py': c.pending_py,
                'remarks_cy': c.remarks_cy if hasattr(c, 'remarks_cy') else '',
                'remarks_py': c.remarks_py if hasattr(c, 'remarks_py') else '',
                'has_mechanism': 'Yes',
                'web_link': '',
            })

        # Build business activities list
        business_activities = []
        for act in d.business_activities:
            business_activities.append({
                'main_activity': act.main_activity,
                'business_activity': act.business_activity,
                'nic_code': '',  # BusinessActivity doesn't have nic_code
                'turnover_pct': act.turnover_pct,
            })

        # Build products/services list
        products_services = []
        for ps in d.products_services:
            products_services.append({
                'product': ps.product,  # Template uses {{ prod.product }}
                'nic_code': ps.nic_code,
                'turnover_pct': ps.turnover_pct,
            })

        # Build subsidiaries list
        subsidiaries = []
        for sub in d.subsidiaries:
            subsidiaries.append({
                'name': sub.name,
                'category': sub.category,  # Template uses {{ sub.category }}
                'shares_pct': sub.shares_pct,
                'participates': sub.participates,
            })

        # Build accounts payable data
        accounts_data = {
            'accounts_payable_cy': d.accounts_payable.accounts_payable_cy if hasattr(d.accounts_payable, 'accounts_payable_cy') else 0,
            'accounts_payable_py': d.accounts_payable.accounts_payable_py if hasattr(d.accounts_payable, 'accounts_payable_py') else 0,
            'cost_of_goods_cy': d.accounts_payable.cost_of_goods_cy if hasattr(d.accounts_payable, 'cost_of_goods_cy') else 0,
            'cost_of_goods_py': d.accounts_payable.cost_of_goods_py if hasattr(d.accounts_payable, 'cost_of_goods_py') else 0,
            'days_payable_cy': d.accounts_payable.days_payable_cy if hasattr(d.accounts_payable, 'days_payable_cy') else 'P0D',
            'days_payable_py': d.accounts_payable.days_payable_py if hasattr(d.accounts_payable, 'days_payable_py') else 'P0D',
            'num_trading_houses_cy': d.accounts_payable.num_trading_houses_cy,
            'num_trading_houses_py': d.accounts_payable.num_trading_houses_py if hasattr(d.accounts_payable, 'num_trading_houses_py') else 0,
            'num_dealers_cy': d.accounts_payable.num_dealers_cy,
            'num_dealers_py': d.accounts_payable.num_dealers_py if hasattr(d.accounts_payable, 'num_dealers_py') else 0,
            'trading_purchases_cy': 0,
            'trading_purchases_py': 0,
            'trading_purchases_pct_cy': d.accounts_payable.trading_purchases_pct_cy if hasattr(d.accounts_payable, 'trading_purchases_pct_cy') else 0,
            'trading_purchases_pct_py': d.accounts_payable.trading_purchases_pct_py if hasattr(d.accounts_payable, 'trading_purchases_pct_py') else 0,
            'total_purchases_cy': 0,
            'total_purchases_py': 0,
            'top10_trading_purchases_cy': 0,
            'top10_trading_purchases_py': 0,
            'total_trading_purchases_cy': 0,
            'total_trading_purchases_py': 0,
            'top10_trading_pct_cy': d.accounts_payable.top10_trading_pct_cy if hasattr(d.accounts_payable, 'top10_trading_pct_cy') else 0,
            'top10_trading_pct_py': d.accounts_payable.top10_trading_pct_py if hasattr(d.accounts_payable, 'top10_trading_pct_py') else 0,
            'dealer_sales_cy': 0,
            'dealer_sales_py': 0,
            'dealer_sales_pct_cy': d.accounts_payable.dealer_sales_pct_cy if hasattr(d.accounts_payable, 'dealer_sales_pct_cy') else 0,
            'dealer_sales_pct_py': d.accounts_payable.dealer_sales_pct_py if hasattr(d.accounts_payable, 'dealer_sales_pct_py') else 0,
            'total_sales_cy': 0,
            'total_sales_py': 0,
            'top10_dealer_sales_cy': 0,
            'top10_dealer_sales_py': 0,
            'total_dealer_sales_cy': 0,
            'total_dealer_sales_py': 0,
            'top10_dealer_pct_cy': d.accounts_payable.top10_dealer_pct_cy if hasattr(d.accounts_payable, 'top10_dealer_pct_cy') else 0,
            'top10_dealer_pct_py': d.accounts_payable.top10_dealer_pct_py if hasattr(d.accounts_payable, 'top10_dealer_pct_py') else 0,
            'rpt_purchases_cy': 0,
            'rpt_purchases_py': 0,
            'rpt_total_purchases_cy': 0,
            'rpt_total_purchases_py': 0,
            'rpt_sales_cy': 0,
            'rpt_sales_py': 0,
            'rpt_total_sales_cy': 0,
            'rpt_total_sales_py': 0,
            'rpt_loans_cy': 0,
            'rpt_loans_py': 0,
            'rpt_total_loans_cy': 0,
            'rpt_total_loans_py': 0,
            'rpt_investments_cy': 0,
            'rpt_investments_py': 0,
            'rpt_total_investments_cy': 0,
            'rpt_total_investments_py': 0,
        }

        # Build environment data (water, energy, emissions, waste)
        # Field names must match template expectations exactly
        environment_data = {
            'energy': {
                # Renewable energy sources
                'elec_renewable_cy': d.energy.elec_renewable_cy,
                'elec_renewable_py': d.energy.elec_renewable_py,
                'fuel_renewable_cy': d.energy.fuel_renewable_cy,
                'fuel_renewable_py': d.energy.fuel_renewable_py,
                'other_renewable_cy': d.energy.other_renewable_cy,
                'other_renewable_py': d.energy.other_renewable_py,
                'total_renewable_cy': d.energy.total_renewable_cy,
                'total_renewable_py': d.energy.total_renewable_py,
                # Non-renewable energy sources
                'elec_nonrenewable_cy': d.energy.elec_nonrenewable_cy,
                'elec_nonrenewable_py': d.energy.elec_nonrenewable_py,
                'fuel_nonrenewable_cy': d.energy.fuel_nonrenewable_cy,
                'fuel_nonrenewable_py': d.energy.fuel_nonrenewable_py,
                'other_nonrenewable_cy': d.energy.other_nonrenewable_cy,
                'other_nonrenewable_py': d.energy.other_nonrenewable_py,
                'total_nonrenewable_cy': d.energy.total_nonrenewable_cy,
                'total_nonrenewable_py': d.energy.total_nonrenewable_py,
                # Totals and intensity
                'total_energy_cy': d.energy.total_energy_cy,
                'total_energy_py': d.energy.total_energy_py,
                'intensity_turnover_cy': d.energy.intensity_turnover_cy,
                'intensity_turnover_py': d.energy.intensity_turnover_py,
                'intensity_turnover_ppp_cy': d.energy.intensity_turnover_ppp_cy,  # Purchasing Power Parity adjusted
                'intensity_turnover_ppp_py': d.energy.intensity_turnover_ppp_py,
                'intensity_physical_cy': d.energy.intensity_physical_cy,
                'intensity_physical_py': d.energy.intensity_physical_py,
                'intensity_optional_cy': d.energy.intensity_optional_cy,
                'intensity_optional_py': d.energy.intensity_optional_py,
                'external_assessment': d.energy.external_assessment,
                'external_agency': d.energy.external_agency,
                # PAT scheme
                'pat_applicable': d.energy.pat_applicable,
                'pat_details': d.energy.pat_details,
                # Low/zero carbon sites
                'low_carbon_sites': d.energy.low_carbon_sites,
                'low_carbon_details': d.energy.low_carbon_details,
            },
            'water': {
                # Flat structure as expected by template
                'surface_cy': d.water.surface_water_cy,
                'surface_py': d.water.surface_water_py,
                'groundwater_cy': d.water.groundwater_cy,
                'groundwater_py': d.water.groundwater_py,
                'thirdparty_cy': d.water.third_party_cy,  # Template expects 'thirdparty' not 'third_party'
                'thirdparty_py': d.water.third_party_py,
                'seawater_cy': d.water.seawater_cy,
                'seawater_py': d.water.seawater_py,
                'others_cy': d.water.others_cy,
                'others_py': d.water.others_py,
                'total_withdrawal_cy': d.water.total_withdrawal_cy,
                'total_withdrawal_py': d.water.total_withdrawal_py,
                'total_consumption_cy': d.water.total_consumption_cy,
                'total_consumption_py': d.water.total_consumption_py,
                'intensity_turnover_cy': d.water.intensity_turnover_cy,
                'intensity_turnover_py': d.water.intensity_turnover_py,
                'intensity_turnover_ppp_cy': 0,
                'intensity_turnover_ppp_py': 0,
                'intensity_physical_cy': d.water.intensity_physical_cy,
                'intensity_physical_py': d.water.intensity_physical_py,
                'intensity_optional_cy': 0,
                'intensity_optional_py': 0,
                'zld': d.water.has_zld,  # Direct value: "Yes" or "No"
                'zld_details': d.water.zld_details,
                # Water discharge by destination
                'discharge_surface_cy': d.water.discharge_surface_cy,
                'discharge_surface_py': d.water.discharge_surface_py,
                'discharge_surface_no_treatment_cy': d.water.discharge_surface_no_treatment_cy,
                'discharge_surface_no_treatment_py': d.water.discharge_surface_no_treatment_py,
                'discharge_surface_with_treatment_cy': d.water.discharge_surface_with_treatment_cy,
                'discharge_surface_with_treatment_py': d.water.discharge_surface_with_treatment_py,
                'discharge_groundwater_cy': d.water.discharge_groundwater_cy,
                'discharge_groundwater_py': d.water.discharge_groundwater_py,
                'discharge_groundwater_no_treatment_cy': d.water.discharge_groundwater_no_treatment_cy,
                'discharge_groundwater_no_treatment_py': d.water.discharge_groundwater_no_treatment_py,
                'discharge_groundwater_with_treatment_cy': d.water.discharge_groundwater_with_treatment_cy,
                'discharge_groundwater_with_treatment_py': d.water.discharge_groundwater_with_treatment_py,
                'discharge_seawater_cy': d.water.discharge_seawater_cy,
                'discharge_seawater_py': d.water.discharge_seawater_py,
                'discharge_seawater_no_treatment_cy': d.water.discharge_seawater_no_treatment_cy,
                'discharge_seawater_no_treatment_py': d.water.discharge_seawater_no_treatment_py,
                'discharge_seawater_with_treatment_cy': d.water.discharge_seawater_with_treatment_cy,
                'discharge_seawater_with_treatment_py': d.water.discharge_seawater_with_treatment_py,
                'discharge_thirdparty_cy': d.water.discharge_thirdparty_cy,
                'discharge_thirdparty_py': d.water.discharge_thirdparty_py,
                'discharge_thirdparty_no_treatment_cy': d.water.discharge_thirdparty_no_treatment_cy,
                'discharge_thirdparty_no_treatment_py': d.water.discharge_thirdparty_no_treatment_py,
                'discharge_thirdparty_with_treatment_cy': d.water.discharge_thirdparty_with_treatment_cy,
                'discharge_thirdparty_with_treatment_py': d.water.discharge_thirdparty_with_treatment_py,
                'discharge_others_cy': d.water.discharge_others_cy,
                'discharge_others_py': d.water.discharge_others_py,
                'discharge_others_no_treatment_cy': d.water.discharge_others_no_treatment_cy,
                'discharge_others_no_treatment_py': d.water.discharge_others_no_treatment_py,
                'discharge_others_with_treatment_cy': d.water.discharge_others_with_treatment_cy,
                'discharge_others_with_treatment_py': d.water.discharge_others_with_treatment_py,
                'total_discharge_cy': d.water.total_discharge_cy,
                'total_discharge_py': d.water.total_discharge_py,
                'discharge_external_assessment': d.water.discharge_external_assessment,
                'discharge_external_agency': d.water.discharge_external_agency,
                'external_assessment': d.water.external_assessment,
                'external_agency': d.water.external_agency,
            },
            # GHG emissions - template uses 'ghg' not 'emissions'
            'ghg': {
                'scope1_cy': d.ghg.scope1_cy,
                'scope1_py': d.ghg.scope1_py,
                'scope2_cy': d.ghg.scope2_cy,
                'scope2_py': d.ghg.scope2_py,
                'total_cy': d.ghg.total_cy,
                'total_py': d.ghg.total_py,
                'intensity_turnover_cy': d.ghg.intensity_turnover_cy,
                'intensity_turnover_py': d.ghg.intensity_turnover_py,
                'intensity_turnover_ppp_cy': d.ghg.intensity_turnover_ppp_cy,
                'intensity_turnover_ppp_py': d.ghg.intensity_turnover_ppp_py,
                'intensity_physical_cy': d.ghg.intensity_physical_cy,
                'intensity_physical_py': d.ghg.intensity_physical_py,
                'intensity_optional_cy': d.ghg.intensity_optional_cy,
                'intensity_optional_py': d.ghg.intensity_optional_py,
                'external_assessment': d.ghg.external_assessment,
                'external_agency': d.ghg.external_agency,
                'has_reduction_project': d.ghg.has_reduction_project,
                'reduction_project_details': d.ghg.reduction_project_details,
                'reduction_project_na_explanation': d.ghg.reduction_project_na_explanation,
            },
            'air': {
                'nox_cy': 0,
                'nox_py': 0,
                'sox_cy': 0,
                'sox_py': 0,
                'pm_cy': 0,
                'pm_py': 0,
                'pop_cy': 0,
                'pop_py': 0,
                'voc_cy': 0,
                'voc_py': 0,
                'hap_cy': 0,
                'hap_py': 0,
                'external_assessment': 'No',
                'external_agency': '',
            },
            'waste': {
                # Waste by category (template expects flat names)
                'plastic_cy': d.waste.plastics_cy.reused + d.waste.plastics_cy.recycled + d.waste.plastics_cy.disposed,
                'plastic_py': d.waste.plastics_py.reused + d.waste.plastics_py.recycled + d.waste.plastics_py.disposed,
                'ewaste_cy': d.waste.ewaste_cy.reused + d.waste.ewaste_cy.recycled + d.waste.ewaste_cy.disposed,
                'ewaste_py': d.waste.ewaste_py.reused + d.waste.ewaste_py.recycled + d.waste.ewaste_py.disposed,
                'biomedical_cy': 0,
                'biomedical_py': 0,
                'construction_cy': 0,
                'construction_py': 0,
                'battery_cy': 0,
                'battery_py': 0,
                'radioactive_cy': 0,
                'radioactive_py': 0,
                'other_hazardous_cy': d.waste.hazardous_cy.reused + d.waste.hazardous_cy.recycled + d.waste.hazardous_cy.disposed,
                'other_hazardous_py': d.waste.hazardous_py.reused + d.waste.hazardous_py.recycled + d.waste.hazardous_py.disposed,
                'other_nonhazardous_cy': d.waste.other_cy.reused + d.waste.other_cy.recycled + d.waste.other_cy.disposed,
                'other_nonhazardous_py': d.waste.other_py.reused + d.waste.other_py.recycled + d.waste.other_py.disposed,
                # Totals
                'total_cy': (d.waste.plastics_cy.reused + d.waste.plastics_cy.recycled + d.waste.plastics_cy.disposed +
                            d.waste.ewaste_cy.reused + d.waste.ewaste_cy.recycled + d.waste.ewaste_cy.disposed +
                            d.waste.hazardous_cy.reused + d.waste.hazardous_cy.recycled + d.waste.hazardous_cy.disposed +
                            d.waste.other_cy.reused + d.waste.other_cy.recycled + d.waste.other_cy.disposed),
                'total_py': (d.waste.plastics_py.reused + d.waste.plastics_py.recycled + d.waste.plastics_py.disposed +
                            d.waste.ewaste_py.reused + d.waste.ewaste_py.recycled + d.waste.ewaste_py.disposed +
                            d.waste.hazardous_py.reused + d.waste.hazardous_py.recycled + d.waste.hazardous_py.disposed +
                            d.waste.other_py.reused + d.waste.other_py.recycled + d.waste.other_py.disposed),
                'intensity_turnover_cy': 0,
                'intensity_turnover_py': 0,
                'intensity_turnover_ppp_cy': 0,
                'intensity_turnover_ppp_py': 0,
                'intensity_physical_cy': 0,
                'intensity_physical_py': 0,
                'intensity_optional_cy': 0,
                'intensity_optional_py': 0,
                # Recovery and disposal
                'recycled_cy': d.waste.plastics_cy.recycled + d.waste.ewaste_cy.recycled + d.waste.hazardous_cy.recycled + d.waste.other_cy.recycled,
                'recycled_py': d.waste.plastics_py.recycled + d.waste.ewaste_py.recycled + d.waste.hazardous_py.recycled + d.waste.other_py.recycled,
                'reused_cy': d.waste.plastics_cy.reused + d.waste.ewaste_cy.reused + d.waste.hazardous_cy.reused + d.waste.other_cy.reused,
                'reused_py': d.waste.plastics_py.reused + d.waste.ewaste_py.reused + d.waste.hazardous_py.reused + d.waste.other_py.reused,
                'total_recovered_cy': (d.waste.plastics_cy.recycled + d.waste.ewaste_cy.recycled + d.waste.hazardous_cy.recycled + d.waste.other_cy.recycled +
                                       d.waste.plastics_cy.reused + d.waste.ewaste_cy.reused + d.waste.hazardous_cy.reused + d.waste.other_cy.reused),
                'total_recovered_py': (d.waste.plastics_py.recycled + d.waste.ewaste_py.recycled + d.waste.hazardous_py.recycled + d.waste.other_py.recycled +
                                       d.waste.plastics_py.reused + d.waste.ewaste_py.reused + d.waste.hazardous_py.reused + d.waste.other_py.reused),
                'other_recovery_cy': 0,
                'other_recovery_py': 0,
                'incineration_cy': 0,
                'incineration_py': 0,
                'landfill_cy': 0,
                'landfill_py': 0,
                'other_disposal_cy': 0,
                'other_disposal_py': 0,
                'total_disposed_cy': d.waste.plastics_cy.disposed + d.waste.ewaste_cy.disposed + d.waste.hazardous_cy.disposed + d.waste.other_cy.disposed,
                'total_disposed_py': d.waste.plastics_py.disposed + d.waste.ewaste_py.disposed + d.waste.hazardous_py.disposed + d.waste.other_py.disposed,
                'external_assessment': 'No',
                'external_agency': '',
                'waste_management_practices': '',
            },
            # Environmental compliance fields
            'environmental_compliance': 'Yes',
            'disaster_plan': 'Yes',
            'disaster_plan_weblink': '',
            'water_stress_external_assessment': 'No',
            'scope3_applicable': 'No',
            'biodiversity_impact': '',
            'value_chain_env_impact': '',
            'value_chain_env_assessment_pct': 0,
            'green_credits_entity': 0,
            'green_credits_value_chain': 0,
            # Revenue from Operations (for intensity calculations)
            'revenue_from_operations_cy': d.revenue_from_operations_cy,
            'revenue_from_operations_py': d.revenue_from_operations_py,
        }

        # Build sustainability data
        sustainability = {
            'rd_cy': d.sustainability.rd_cy,
            'rd_py': d.sustainability.rd_py,
            'rd_improvements': d.sustainability.rd_improvements,
            'capex_cy': d.sustainability.capex_cy,
            'capex_py': d.sustainability.capex_py,
            'capex_improvements': d.sustainability.capex_improvements,
            'epr_applicable': d.sustainability.epr_applicable,
            'lca_conducted': d.sustainability.lca_conducted,
            'lca_product_count': d.sustainability.lca_product_count,
            'lca_percentage_cy': d.sustainability.lca_percentage_cy,
            'lca_percentage_py': d.sustainability.lca_percentage_py,
            'sustainable_sourcing_pct': d.sustainability.sustainable_sourcing_pct,
        }

        # Build principles disclosure list
        principles = []
        for p in d.principles:
            principles.append({
                'num': p.num,
                'policy_covers': p.policy_covers,
                'board_approved': p.board_approved,
                'web_link': p.web_link,
                'translated_to_procedures': p.translated_to_procedures,
                'extends_to_value_chain': p.extends_to_value_chain,
                'codes_certifications': p.codes_certifications,
                'commitments_goals': p.commitments_goals,
                'performance': p.performance,
            })

        # Build gross wages structure
        # Calculate female employee+worker counts for average calculation
        female_emp_cy = d.employees_workers.employees.total.female
        female_workers_cy = d.employees_workers.workers.total.female
        female_emp_workers_cy = female_emp_cy + female_workers_cy

        # For PY, use the stored value if available, otherwise estimate from current
        female_emp_workers_py = d.gross_wages.female_emp_workers_py if d.gross_wages.female_emp_workers_py > 0 else female_emp_workers_cy

        # Calculate average: (Beginning of year + End of year) / 2
        # Beginning of CY = End of PY
        avg_female_emp_workers_cy = (female_emp_workers_py + female_emp_workers_cy) / 2 if female_emp_workers_py > 0 else female_emp_workers_cy
        avg_female_emp_workers_py = female_emp_workers_py  # For PY, we only have year-end data

        gross_wages = {
            'female_cy': d.gross_wages.female_cy,
            'female_py': d.gross_wages.female_py,
            'total_cy': d.gross_wages.total_cy,
            'total_py': d.gross_wages.total_py,
            'female_pct_cy': d.gross_wages.female_pct_cy,
            'female_pct_py': d.gross_wages.female_pct_py,
            'avg_female_emp_workers_cy': avg_female_emp_workers_cy,
            'avg_female_emp_workers_py': avg_female_emp_workers_py,
        }

        # Build union membership data structure
        union_membership = {
            'permanent_employees': {
                'total': {
                    'total_cy': d.union_membership.permanent_employees_total.total_cy,
                    'total_py': d.union_membership.permanent_employees_total.total_py,
                    'members_cy': d.union_membership.permanent_employees_total.members_cy,
                    'members_py': d.union_membership.permanent_employees_total.members_py,
                    'pct_cy': d.union_membership.permanent_employees_total.pct_cy,
                    'pct_py': d.union_membership.permanent_employees_total.pct_py,
                },
                'male': {
                    'total_cy': d.union_membership.permanent_employees_male.total_cy,
                    'total_py': d.union_membership.permanent_employees_male.total_py,
                    'members_cy': d.union_membership.permanent_employees_male.members_cy,
                    'members_py': d.union_membership.permanent_employees_male.members_py,
                    'pct_cy': d.union_membership.permanent_employees_male.pct_cy,
                    'pct_py': d.union_membership.permanent_employees_male.pct_py,
                },
                'female': {
                    'total_cy': d.union_membership.permanent_employees_female.total_cy,
                    'total_py': d.union_membership.permanent_employees_female.total_py,
                    'members_cy': d.union_membership.permanent_employees_female.members_cy,
                    'members_py': d.union_membership.permanent_employees_female.members_py,
                    'pct_cy': d.union_membership.permanent_employees_female.pct_cy,
                    'pct_py': d.union_membership.permanent_employees_female.pct_py,
                },
                'other': {
                    'total_cy': d.union_membership.permanent_employees_other.total_cy,
                    'total_py': d.union_membership.permanent_employees_other.total_py,
                    'members_cy': d.union_membership.permanent_employees_other.members_cy,
                    'members_py': d.union_membership.permanent_employees_other.members_py,
                    'pct_cy': d.union_membership.permanent_employees_other.pct_cy,
                    'pct_py': d.union_membership.permanent_employees_other.pct_py,
                },
            },
            'permanent_workers': {
                'total': {
                    'total_cy': d.union_membership.permanent_workers_total.total_cy,
                    'total_py': d.union_membership.permanent_workers_total.total_py,
                    'members_cy': d.union_membership.permanent_workers_total.members_cy,
                    'members_py': d.union_membership.permanent_workers_total.members_py,
                    'pct_cy': d.union_membership.permanent_workers_total.pct_cy,
                    'pct_py': d.union_membership.permanent_workers_total.pct_py,
                },
                'male': {
                    'total_cy': d.union_membership.permanent_workers_male.total_cy,
                    'total_py': d.union_membership.permanent_workers_male.total_py,
                    'members_cy': d.union_membership.permanent_workers_male.members_cy,
                    'members_py': d.union_membership.permanent_workers_male.members_py,
                    'pct_cy': d.union_membership.permanent_workers_male.pct_cy,
                    'pct_py': d.union_membership.permanent_workers_male.pct_py,
                },
                'female': {
                    'total_cy': d.union_membership.permanent_workers_female.total_cy,
                    'total_py': d.union_membership.permanent_workers_female.total_py,
                    'members_cy': d.union_membership.permanent_workers_female.members_cy,
                    'members_py': d.union_membership.permanent_workers_female.members_py,
                    'pct_cy': d.union_membership.permanent_workers_female.pct_cy,
                    'pct_py': d.union_membership.permanent_workers_female.pct_py,
                },
                'other': {
                    'total_cy': d.union_membership.permanent_workers_other.total_cy,
                    'total_py': d.union_membership.permanent_workers_other.total_py,
                    'members_cy': d.union_membership.permanent_workers_other.members_cy,
                    'members_py': d.union_membership.permanent_workers_other.members_py,
                    'pct_cy': d.union_membership.permanent_workers_other.pct_cy,
                    'pct_py': d.union_membership.permanent_workers_other.pct_py,
                },
            },
        }

        # Build employee wellbeing structure (matching template expectations)
        # Template uses: permanent/other_than_permanent and male/female/others/total
        # Keys expected by template: benefit_key + '_num' and benefit_key + '_pct'
        def create_default_gender_template():
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

        # Use extracted employee wellbeing data if available, otherwise use defaults
        extracted_wellbeing = d.employee_wellbeing_data if hasattr(d, 'employee_wellbeing_data') and d.employee_wellbeing_data else {}
        employee_wellbeing = {
            'accessibility': '',
            'affected_employees_cy': 0,
            'affected_employees_py': 0,
            'affected_workers_cy': 0,
            'affected_workers_py': 0,
            'assessments': {
                'health_safety_pct': 0,
                'working_conditions_pct': 0,
            },
            'safe_workplace_measures': d.safe_workplace_measures,
            'corrective_actions_safety': d.corrective_actions_safety,
            'complaints': {
                'health_safety': {'filed_cy': 0, 'filed_py': 0, 'pending_cy': 0, 'pending_py': 0},
                'working_conditions': {'filed_cy': 0, 'filed_py': 0, 'pending_cy': 0, 'pending_py': 0},
            },
            'employees': extracted_wellbeing.get('employees', {
                'permanent': create_default_gender_template(),
                'other_than_permanent': create_default_gender_template(),
            }),
            'workers': extracted_wellbeing.get('workers', {
                'permanent': create_default_gender_template(),
                'other_than_permanent': create_default_gender_template(),
            }),
            'grievance': {
                'has_mechanism': d.grievance_mechanism.has_mechanism if hasattr(d, 'grievance_mechanism') else 'true',
                'permanent_employees': {'available': d.grievance_mechanism.permanent_employees if hasattr(d, 'grievance_mechanism') else 'Yes', 'details': d.grievance_mechanism.permanent_employees_details if hasattr(d, 'grievance_mechanism') else ''},
                'other_employees': {'available': d.grievance_mechanism.other_employees if hasattr(d, 'grievance_mechanism') else 'Yes', 'details': d.grievance_mechanism.other_employees_details if hasattr(d, 'grievance_mechanism') else ''},
                'permanent_workers': {'available': d.grievance_mechanism.permanent_workers if hasattr(d, 'grievance_mechanism') else 'Yes', 'details': d.grievance_mechanism.permanent_workers_details if hasattr(d, 'grievance_mechanism') else ''},
                'other_workers': {'available': d.grievance_mechanism.other_workers if hasattr(d, 'grievance_mechanism') else 'Yes', 'details': d.grievance_mechanism.other_workers_details if hasattr(d, 'grievance_mechanism') else ''},
            },
            'equal_opportunity': {
                'has_policy': 'Yes',
                'web_link': '',
            },
            'parental_leave': {
                'male': {
                    'emp_return': d.parental_leave.male.emp_return,
                    'emp_retention': d.parental_leave.male.emp_retention,
                    'worker_return': d.parental_leave.male.worker_return,
                    'worker_retention': d.parental_leave.male.worker_retention,
                },
                'female': {
                    'emp_return': d.parental_leave.female.emp_return,
                    'emp_retention': d.parental_leave.female.emp_retention,
                    'worker_return': d.parental_leave.female.worker_return,
                    'worker_retention': d.parental_leave.female.worker_retention,
                },
                'others': {
                    'emp_return': d.parental_leave.others.emp_return,
                    'emp_retention': d.parental_leave.others.emp_retention,
                    'worker_return': d.parental_leave.others.worker_return,
                    'worker_retention': d.parental_leave.others.worker_retention,
                },
                'total': {
                    'emp_return': d.parental_leave.total.emp_return,
                    'emp_retention': d.parental_leave.total.emp_retention,
                    'worker_return': d.parental_leave.total.worker_return,
                    'worker_retention': d.parental_leave.total.worker_retention,
                },
            },
            'retirement_benefits': {
                'pf': {
                    'emp_cy': d.retirement_benefits.pf.emp_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'pf') else 0,
                    'worker_cy': d.retirement_benefits.pf.worker_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'pf') else 0,
                    'deposited_cy': d.retirement_benefits.pf.deposited_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'pf') else 'N',
                    'emp_py': d.retirement_benefits.pf.emp_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'pf') else 0,
                    'worker_py': d.retirement_benefits.pf.worker_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'pf') else 0,
                    'deposited_py': d.retirement_benefits.pf.deposited_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'pf') else 'N',
                },
                'gratuity': {
                    'emp_cy': d.retirement_benefits.gratuity.emp_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'gratuity') else 0,
                    'worker_cy': d.retirement_benefits.gratuity.worker_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'gratuity') else 0,
                    'deposited_cy': d.retirement_benefits.gratuity.deposited_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'gratuity') else 'N',
                    'emp_py': d.retirement_benefits.gratuity.emp_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'gratuity') else 0,
                    'worker_py': d.retirement_benefits.gratuity.worker_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'gratuity') else 0,
                    'deposited_py': d.retirement_benefits.gratuity.deposited_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'gratuity') else 'N',
                },
                'esi': {
                    'emp_cy': d.retirement_benefits.esi.emp_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'esi') else 0,
                    'worker_cy': d.retirement_benefits.esi.worker_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'esi') else 0,
                    'deposited_cy': d.retirement_benefits.esi.deposited_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'esi') else 'N',
                    'emp_py': d.retirement_benefits.esi.emp_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'esi') else 0,
                    'worker_py': d.retirement_benefits.esi.worker_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'esi') else 0,
                    'deposited_py': d.retirement_benefits.esi.deposited_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'esi') else 'N',
                },
                'others': {
                    'name_cy': d.retirement_benefits.others.name_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'others') else 'NA',
                    'emp_cy': d.retirement_benefits.others.emp_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'others') else 0,
                    'worker_cy': d.retirement_benefits.others.worker_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'others') else 0,
                    'deposited_cy': d.retirement_benefits.others.deposited_cy if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'others') else 'NA',
                    'name_py': d.retirement_benefits.others.name_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'others') else 'NA',
                    'emp_py': d.retirement_benefits.others.emp_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'others') else 0,
                    'worker_py': d.retirement_benefits.others.worker_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'others') else 0,
                    'deposited_py': d.retirement_benefits.others.deposited_py if hasattr(d, 'retirement_benefits') and hasattr(d.retirement_benefits, 'others') else 'NA',
                },
            },
            'wellbeing_spending': {'cy': 0, 'py': 0},
            'ohs': {
                'implemented': 'Yes',
                'coverage': '',
                'hazard_process': '',
                'worker_report_process': 'Yes',
                'non_occupational_access': 'Yes',
            },
            # Section 11: Safety Incidents - use extracted data if available
            'safety_incidents': d.safety_incidents_data if hasattr(d, 'safety_incidents_data') and d.safety_incidents_data else {
                'ltifr_emp_cy': 0, 'ltifr_emp_py': 0,
                'ltifr_worker_cy': 0, 'ltifr_worker_py': 0,
                'injuries_emp_cy': 0, 'injuries_emp_py': 0,
                'injuries_worker_cy': 0, 'injuries_worker_py': 0,
                'fatalities_emp_cy': 0, 'fatalities_emp_py': 0,
                'fatalities_worker_cy': 0, 'fatalities_worker_py': 0,
                'high_consequence_emp_cy': 0, 'high_consequence_emp_py': 0,
                'high_consequence_worker_cy': 0, 'high_consequence_worker_py': 0,
            },
            # Section 9: Performance and Career Development
            'performance': d.performance_career_data if hasattr(d, 'performance_career_data') and d.performance_career_data else {
                'employees': {
                    'male': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                    'female': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                    'others': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                    'total': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                },
                'workers': {
                    'male': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                    'female': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                    'others': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                    'total': {'total_cy': 0, 'reviewed_cy': 0, 'pct_cy': 0, 'total_py': 0, 'reviewed_py': 0, 'pct_py': 0},
                },
            },
            # Section 8: Training on Health & Safety and Skill Upgradation (P3 Q8)
            'training': {
                'employees': {
                    'male': {
                        'total_cy': d.safety_skill_training.employees.male.total_cy,
                        'hs_num_cy': d.safety_skill_training.employees.male.hs_num_cy,
                        'hs_pct_cy': d.safety_skill_training.employees.male.hs_pct_cy,
                        'skill_num_cy': d.safety_skill_training.employees.male.skill_num_cy,
                        'skill_pct_cy': d.safety_skill_training.employees.male.skill_pct_cy,
                        'total_py': d.safety_skill_training.employees.male.total_py,
                        'hs_num_py': d.safety_skill_training.employees.male.hs_num_py,
                        'hs_pct_py': d.safety_skill_training.employees.male.hs_pct_py,
                        'skill_num_py': d.safety_skill_training.employees.male.skill_num_py,
                        'skill_pct_py': d.safety_skill_training.employees.male.skill_pct_py,
                    },
                    'female': {
                        'total_cy': d.safety_skill_training.employees.female.total_cy,
                        'hs_num_cy': d.safety_skill_training.employees.female.hs_num_cy,
                        'hs_pct_cy': d.safety_skill_training.employees.female.hs_pct_cy,
                        'skill_num_cy': d.safety_skill_training.employees.female.skill_num_cy,
                        'skill_pct_cy': d.safety_skill_training.employees.female.skill_pct_cy,
                        'total_py': d.safety_skill_training.employees.female.total_py,
                        'hs_num_py': d.safety_skill_training.employees.female.hs_num_py,
                        'hs_pct_py': d.safety_skill_training.employees.female.hs_pct_py,
                        'skill_num_py': d.safety_skill_training.employees.female.skill_num_py,
                        'skill_pct_py': d.safety_skill_training.employees.female.skill_pct_py,
                    },
                    'others': {
                        'total_cy': d.safety_skill_training.employees.others.total_cy,
                        'hs_num_cy': d.safety_skill_training.employees.others.hs_num_cy,
                        'hs_pct_cy': d.safety_skill_training.employees.others.hs_pct_cy,
                        'skill_num_cy': d.safety_skill_training.employees.others.skill_num_cy,
                        'skill_pct_cy': d.safety_skill_training.employees.others.skill_pct_cy,
                        'total_py': d.safety_skill_training.employees.others.total_py,
                        'hs_num_py': d.safety_skill_training.employees.others.hs_num_py,
                        'hs_pct_py': d.safety_skill_training.employees.others.hs_pct_py,
                        'skill_num_py': d.safety_skill_training.employees.others.skill_num_py,
                        'skill_pct_py': d.safety_skill_training.employees.others.skill_pct_py,
                    },
                    'total': {
                        'total_cy': d.safety_skill_training.employees.total.total_cy,
                        'hs_num_cy': d.safety_skill_training.employees.total.hs_num_cy,
                        'hs_pct_cy': d.safety_skill_training.employees.total.hs_pct_cy,
                        'skill_num_cy': d.safety_skill_training.employees.total.skill_num_cy,
                        'skill_pct_cy': d.safety_skill_training.employees.total.skill_pct_cy,
                        'total_py': d.safety_skill_training.employees.total.total_py,
                        'hs_num_py': d.safety_skill_training.employees.total.hs_num_py,
                        'hs_pct_py': d.safety_skill_training.employees.total.hs_pct_py,
                        'skill_num_py': d.safety_skill_training.employees.total.skill_num_py,
                        'skill_pct_py': d.safety_skill_training.employees.total.skill_pct_py,
                    },
                },
                'workers': {
                    'male': {
                        'total_cy': d.safety_skill_training.workers.male.total_cy,
                        'hs_num_cy': d.safety_skill_training.workers.male.hs_num_cy,
                        'hs_pct_cy': d.safety_skill_training.workers.male.hs_pct_cy,
                        'skill_num_cy': d.safety_skill_training.workers.male.skill_num_cy,
                        'skill_pct_cy': d.safety_skill_training.workers.male.skill_pct_cy,
                        'total_py': d.safety_skill_training.workers.male.total_py,
                        'hs_num_py': d.safety_skill_training.workers.male.hs_num_py,
                        'hs_pct_py': d.safety_skill_training.workers.male.hs_pct_py,
                        'skill_num_py': d.safety_skill_training.workers.male.skill_num_py,
                        'skill_pct_py': d.safety_skill_training.workers.male.skill_pct_py,
                    },
                    'female': {
                        'total_cy': d.safety_skill_training.workers.female.total_cy,
                        'hs_num_cy': d.safety_skill_training.workers.female.hs_num_cy,
                        'hs_pct_cy': d.safety_skill_training.workers.female.hs_pct_cy,
                        'skill_num_cy': d.safety_skill_training.workers.female.skill_num_cy,
                        'skill_pct_cy': d.safety_skill_training.workers.female.skill_pct_cy,
                        'total_py': d.safety_skill_training.workers.female.total_py,
                        'hs_num_py': d.safety_skill_training.workers.female.hs_num_py,
                        'hs_pct_py': d.safety_skill_training.workers.female.hs_pct_py,
                        'skill_num_py': d.safety_skill_training.workers.female.skill_num_py,
                        'skill_pct_py': d.safety_skill_training.workers.female.skill_pct_py,
                    },
                    'others': {
                        'total_cy': d.safety_skill_training.workers.others.total_cy,
                        'hs_num_cy': d.safety_skill_training.workers.others.hs_num_cy,
                        'hs_pct_cy': d.safety_skill_training.workers.others.hs_pct_cy,
                        'skill_num_cy': d.safety_skill_training.workers.others.skill_num_cy,
                        'skill_pct_cy': d.safety_skill_training.workers.others.skill_pct_cy,
                        'total_py': d.safety_skill_training.workers.others.total_py,
                        'hs_num_py': d.safety_skill_training.workers.others.hs_num_py,
                        'hs_pct_py': d.safety_skill_training.workers.others.hs_pct_py,
                        'skill_num_py': d.safety_skill_training.workers.others.skill_num_py,
                        'skill_pct_py': d.safety_skill_training.workers.others.skill_pct_py,
                    },
                    'total': {
                        'total_cy': d.safety_skill_training.workers.total.total_cy,
                        'hs_num_cy': d.safety_skill_training.workers.total.hs_num_cy,
                        'hs_pct_cy': d.safety_skill_training.workers.total.hs_pct_cy,
                        'skill_num_cy': d.safety_skill_training.workers.total.skill_num_cy,
                        'skill_pct_cy': d.safety_skill_training.workers.total.skill_pct_cy,
                        'total_py': d.safety_skill_training.workers.total.total_py,
                        'hs_num_py': d.safety_skill_training.workers.total.hs_num_py,
                        'hs_pct_py': d.safety_skill_training.workers.total.hs_pct_py,
                        'skill_num_py': d.safety_skill_training.workers.total.skill_num_py,
                        'skill_pct_py': d.safety_skill_training.workers.total.skill_pct_py,
                    },
                },
            },
        }

        # Build material issues list
        material_issues = []
        for m in d.material_issues:
            material_issues.append({
                'issue': m.issue,
                'risk_or_opp': m.risk_or_opp,
                'rationale': m.rationale,
                'mitigation': m.mitigation,
                'financial_impact': m.financial_impact,
            })

        # Build assessor info (placeholder)
        assessor = {
            'company_id': self._get_cin(),
            'company_name': d.company.company_name,
            'assessor_name': '',
            'designation': '',
            'date_of_signing': self._format_date(self.end_date_cy),
        }

        # Empty lists/structures for sections not yet implemented
        affiliations = []
        human_rights_training = {'employees': [], 'workers': []}
        value_chain_partners = []
        responsible_business = {}
        stakeholder_engagement = []
        innovations = []

        # Build stakeholder groups from parsed data
        stakeholder_groups_list = []
        for sg in d.stakeholder_groups:
            stakeholder_groups_list.append({
                'name': sg.name,
                'vulnerable_marginalized': sg.vulnerable_marginalized,
                'channels': sg.channels,
                'channels_details': sg.channels_details,
                'frequency': sg.frequency,
                'frequency_details': sg.frequency_details,
                'purpose_scope': sg.purpose_scope,
            })

        # Stakeholder data structure
        stakeholder_data = {
            'identification_process': d.stakeholder_identification_process,
            'stakeholder_groups': stakeholder_groups_list,
            'consultation_process': d.stakeholder_consultation_process,
            'stakeholder_consultation_used': d.stakeholder_consultation_used or 'Yes',
            'stakeholder_consultation_details': d.stakeholder_consultation_details,
            'vulnerable_marginalized_actions': d.vulnerable_marginalized_actions or 'NA',
        }

        # Human rights data structure
        human_rights_data = {
            'complaints': {
                'sexual_harassment': {'filed_cy': 0, 'pending_cy': 0, 'remarks_cy': 'NA', 'filed_py': 0, 'pending_py': 0, 'remarks_py': 'NA'},
                'child_labour': {'filed_cy': 0, 'pending_cy': 0, 'remarks_cy': 'NA', 'filed_py': 0, 'pending_py': 0, 'remarks_py': 'NA'},
                'forced_labour': {'filed_cy': 0, 'pending_cy': 0, 'remarks_cy': 'NA', 'filed_py': 0, 'pending_py': 0, 'remarks_py': 'NA'},
                'discrimination': {'filed_cy': 0, 'pending_cy': 0, 'remarks_cy': 'NA', 'filed_py': 0, 'pending_py': 0, 'remarks_py': 'NA'},
                'wages': {'filed_cy': 0, 'pending_cy': 0, 'remarks_cy': 'NA', 'filed_py': 0, 'pending_py': 0, 'remarks_py': 'NA'},
                'other': {'filed_cy': 0, 'pending_cy': 0, 'remarks_cy': 'NA', 'filed_py': 0, 'pending_py': 0, 'remarks_py': 'NA'},
            },
            'posh': {
                'total_complaints_cy': 0, 'total_complaints_py': 0,
                'pct_complaints_cy': 0, 'pct_complaints_py': 0,
                'upheld_cy': 0, 'upheld_py': 0,
            },
            'mechanisms_prevent_adverse': '',
            'plant_assessments': {
                'child_labour': 0, 'forced_labour': 0, 'sexual_harassment': 0, 'discrimination': 0, 'wages': 0,
            },
            'value_chain_assessments': {
                'child_labour': 0, 'forced_labour': 0, 'sexual_harassment': 0, 'discrimination': 0, 'wages': 0,
            },
            'corrective_actions_plants': '',
            'corrective_actions_value_chain': '',
            'other_assessments_plants': {
                'name': 'NA',
                'percentage': 0,
            },
            'other_assessments_value_chain': {
                'name': 'NA',
                'percentage': 0,
            },
            'business_process_modified': '',
            'hr_due_diligence': '',
            'differently_abled_accessible': 'No',
            # Include gross_wages for template access via human_rights_data.gross_wages
            'gross_wages': gross_wages,
            # Include median_remuneration for template access
            'median_remuneration': {
                'bod': {
                    'male_num': d.median_remuneration.bod.male_num if hasattr(d, 'median_remuneration') else 0,
                    'male_median': d.median_remuneration.bod.male_median if hasattr(d, 'median_remuneration') else 0,
                    'female_num': d.median_remuneration.bod.female_num if hasattr(d, 'median_remuneration') else 0,
                    'female_median': d.median_remuneration.bod.female_median if hasattr(d, 'median_remuneration') else 0,
                    'other_num': d.median_remuneration.bod.other_num if hasattr(d, 'median_remuneration') else 0,
                    'other_median': d.median_remuneration.bod.other_median if hasattr(d, 'median_remuneration') else 0,
                },
                'kmp': {
                    'male_num': d.median_remuneration.kmp.male_num if hasattr(d, 'median_remuneration') else 0,
                    'male_median': d.median_remuneration.kmp.male_median if hasattr(d, 'median_remuneration') else 0,
                    'female_num': d.median_remuneration.kmp.female_num if hasattr(d, 'median_remuneration') else 0,
                    'female_median': d.median_remuneration.kmp.female_median if hasattr(d, 'median_remuneration') else 0,
                    'other_num': d.median_remuneration.kmp.other_num if hasattr(d, 'median_remuneration') else 0,
                    'other_median': d.median_remuneration.kmp.other_median if hasattr(d, 'median_remuneration') else 0,
                },
                'employees': {
                    'male_num': d.median_remuneration.employees.male_num if hasattr(d, 'median_remuneration') else 0,
                    'male_median': d.median_remuneration.employees.male_median if hasattr(d, 'median_remuneration') else 0,
                    'female_num': d.median_remuneration.employees.female_num if hasattr(d, 'median_remuneration') else 0,
                    'female_median': d.median_remuneration.employees.female_median if hasattr(d, 'median_remuneration') else 0,
                    'other_num': d.median_remuneration.employees.other_num if hasattr(d, 'median_remuneration') else 0,
                    'other_median': d.median_remuneration.employees.other_median if hasattr(d, 'median_remuneration') else 0,
                },
                'workers': {
                    'male_num': d.median_remuneration.workers.male_num if hasattr(d, 'median_remuneration') else 0,
                    'male_median': d.median_remuneration.workers.male_median if hasattr(d, 'median_remuneration') else 0,
                    'female_num': d.median_remuneration.workers.female_num if hasattr(d, 'median_remuneration') else 0,
                    'female_median': d.median_remuneration.workers.female_median if hasattr(d, 'median_remuneration') else 0,
                    'other_num': d.median_remuneration.workers.other_num if hasattr(d, 'median_remuneration') else 0,
                    'other_median': d.median_remuneration.workers.other_median if hasattr(d, 'median_remuneration') else 0,
                },
            },
        }

        # Return complete context
        return {
            # Entity identification
            'cin': self._get_cin(),
            'company_name': d.company.company_name,
            'incorporation_year': d.company.incorporation_year,
            'registered_address': d.company.registered_address,
            'corporate_address': d.company.corporate_address,
            'email': d.company.email,
            'telephone': d.company.telephone,
            'website': d.company.website,
            'paid_up_capital': d.company.paid_up_capital / 10000000 if d.company.paid_up_capital > 1000000 else d.company.paid_up_capital,
            'reporting_boundary': d.company.reporting_boundary,
            'contact_person_name': d.company.contact_person_name if hasattr(d.company, 'contact_person_name') else '',
            'contact_person_email': d.company.contact_person_email if hasattr(d.company, 'contact_person_email') else '',
            'contact_person_phone': d.company.contact_person_phone if hasattr(d.company, 'contact_person_phone') else '',

            # Reporting periods
            'start_date_cy': self._format_date(self.start_date_cy),
            'end_date_cy': self._format_date(self.end_date_cy),
            'start_date_py': self._format_date(self.start_date_py),
            'end_date_py': self._format_date(self.end_date_py),
            'start_date_ppy': self._format_date(self.start_date_ppy),
            'end_date_ppy': self._format_date(self.end_date_ppy),

            # Company and assurance
            'assurance': assurance,
            'csr': csr,

            # Locations and markets
            'locations': locations,
            'markets': markets,

            # Employee data
            'emp_workers': emp_workers,
            'turnover_rates': turnover_rates,
            'women_representation': women_representation,
            'women_rep': women_representation,  # Alias for template compatibility
            'employee_wellbeing': employee_wellbeing,
            'gross_wages': gross_wages,
            'union_membership': union_membership,

            # Business info
            'business_activities': business_activities,
            'products_services': products_services,
            'subsidiaries': subsidiaries,

            # Stakeholder data
            'complaints': complaints,
            'material_issues': material_issues,

            # Section B - Principles (section_b is used in template loops)
            'principles': principles,
            'section_b': principles,  # Alias for template loops

            # Section C - Environment
            'environment_data': environment_data,
            'sustainability': sustainability,
            'accounts_data': accounts_data,

            # Additional structures
            'assessor': assessor,
            'affiliations': affiliations,
            'human_rights_training': human_rights_training,
            'human_rights_data': human_rights_data,

            # Principle 5 - Minimum Wages Compliance
            'minimum_wages': {
                'perm_emp': {
                    'male': self.data.minimum_wages.perm_emp.male.model_dump(),
                    'female': self.data.minimum_wages.perm_emp.female.model_dump(),
                    'other': self.data.minimum_wages.perm_emp.other.model_dump(),
                    'total': self.data.minimum_wages.perm_emp.total.model_dump(),
                },
                'other_emp': {
                    'male': self.data.minimum_wages.other_emp.male.model_dump(),
                    'female': self.data.minimum_wages.other_emp.female.model_dump(),
                    'other': self.data.minimum_wages.other_emp.other.model_dump(),
                    'total': self.data.minimum_wages.other_emp.total.model_dump(),
                },
                'perm_workers': {
                    'male': self.data.minimum_wages.perm_workers.male.model_dump(),
                    'female': self.data.minimum_wages.perm_workers.female.model_dump(),
                    'other': self.data.minimum_wages.perm_workers.other.model_dump(),
                    'total': self.data.minimum_wages.perm_workers.total.model_dump(),
                },
                'other_workers': {
                    'male': self.data.minimum_wages.other_workers.male.model_dump(),
                    'female': self.data.minimum_wages.other_workers.female.model_dump(),
                    'other': self.data.minimum_wages.other_workers.other.model_dump(),
                    'total': self.data.minimum_wages.other_workers.total.model_dump(),
                },
            },

            'value_chain_partners': value_chain_partners,
            'responsible_business': responsible_business,
            'stakeholder_engagement': stakeholder_engagement,
            'innovations': innovations,
            'stakeholder_data': stakeholder_data,

            # Fines, Penalties and Anti-Corruption (Principle 1)
            'fines_penalties': {
                'penalty_fine': {'ngrbc': '', 'name': '', 'amount': 0, 'brief': '', 'appeal': ''},
                'settlement': {'ngrbc': '', 'name': '', 'amount': 0, 'brief': '', 'appeal': ''},
                'compounding': {'ngrbc': '', 'name': '', 'amount': 0, 'brief': '', 'appeal': ''},
                'imprisonment': {'ngrbc': '', 'name': '', 'period': '', 'brief': '', 'appeal': ''},
                'punishment': {'ngrbc': '', 'name': '', 'details': '', 'brief': '', 'appeal': ''},
                'appeal_revision': {'details': '', 'agency': ''},
                'anti_corruption': {
                    'has_policy': 'Yes',
                    'policy_details': '',
                    'web_link': '',
                },
                'disciplinary_cy': {'directors': 0, 'kmps': 0, 'employees': 0, 'workers': 0},
                'disciplinary_py': {'directors': 0, 'kmps': 0, 'employees': 0, 'workers': 0},
                'conflict_directors_cy': {'number': 0, 'remarks': ''},
                'conflict_directors_py': {'number': 0, 'remarks': ''},
                'conflict_kmps_cy': {'number': 0, 'remarks': ''},
                'conflict_kmps_py': {'number': 0, 'remarks': ''},
            },

            # Principles 7, 8, 9 data
            'p789_data': {
                'p7': self._build_p7_data(d),
                'p8': {
                    # Placeholder for Principle 8 data
                },
                'p9': self._build_p9_data(d),
            },

            # Section B: Management and Process Disclosures - Governance
            'governance': {
                'director_statement': d.director_statement if hasattr(d, 'director_statement') else '',
                'highest_authority': d.highest_authority if hasattr(d, 'highest_authority') else '',
                'has_esg_committee': d.has_specific_committee if hasattr(d, 'has_specific_committee') else 'Yes',
                'esg_committee': d.specific_committee_details if hasattr(d, 'specific_committee_details') else '',
                # Principles 1-9 governance data (Q10 review details)
                'principles': [
                    {
                        'performance_review_by': d.principles[i].performance_review_by if i < len(d.principles) and d.principles[i].performance_review_by else 'Director',
                        'compliance_review_by': d.principles[i].compliance_review_by if i < len(d.principles) and d.principles[i].compliance_review_by else 'Director',
                        'performance_frequency': d.principles[i].performance_frequency if i < len(d.principles) and d.principles[i].performance_frequency else 'Annually',
                        'performance_frequency_other': '',
                        'compliance_frequency': d.principles[i].compliance_frequency if i < len(d.principles) and d.principles[i].compliance_frequency else 'Annually',
                        'independent_assessment': 'false',
                    }
                    for i in range(9)  # Generate for all 9 principles
                ],
            },

            # Section B: Training and awareness programs
            'training': {
                'board_of_directors': {'count': 0, 'topics': '', 'coverage': 0},
                'kmp': {'count': 0, 'topics': '', 'coverage': 0},
                'employees': {'count': 0, 'topics': '', 'coverage': 0},
                'workers': {'count': 0, 'topics': '', 'coverage': 0},
            },
        }

    def _build_p7_data(self, d) -> Dict[str, Any]:
        """
        Build Principle 7 (Policy Advocacy) data structure.
        Uses extracted p7_data if available, otherwise falls back to defaults.

        Args:
            d: BRSRReportData instance

        Returns:
            Dict with P7 data for template rendering
        """
        # Default structure
        defaults = {
            'num_affiliations': 0,
            'affiliations': []
        }

        # If p7_data was extracted from HTML, use those values
        if d.p7_data:
            extracted = d.p7_data
            if extracted.get('num_affiliations'):
                defaults['num_affiliations'] = extracted['num_affiliations']
            if extracted.get('affiliations'):
                defaults['affiliations'] = extracted['affiliations']

        return defaults

    def _build_p9_data(self, d) -> Dict[str, Any]:
        """
        Build Principle 9 (Consumer Responsibility) data structure.
        Uses extracted p9_data if available, otherwise falls back to defaults.

        Args:
            d: BRSRReportData instance

        Returns:
            Dict with P9 data for template rendering
        """
        # Default structure
        defaults = {
            'complaint_mechanism': '',
            'env_social_pct': 0,
            'safe_usage_pct': 0,
            'recycling_pct': 0,
            'complaints': {
                'data_privacy': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'advertising': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'cyber_security': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'essential_services': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'restrictive_trade': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'unfair_trade': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
                'other': {'received_cy': 0, 'pending_cy': 0, 'remark_cy': 'NA', 'received_py': 0, 'pending_py': 0, 'remark_py': 'NA'},
            },
            'turnover_pct_noncompliant': 0,
            'corrective_action_noncompliant': '',
            'voluntary_recalls': 0,
            'voluntary_recall_reason': 'NA',
            'forced_recalls': 0,
            'forced_recall_reason': 'NA',
            'cyber_policy': 'Yes',
            'cyber_policy_weblink': '',
            'data_breaches': 0,
            'pii_breach_pct': 0,
            'data_breach_impact': 'NA',
            'corrective_actions_q6': d.corrective_actions_p9_q6,
            'product_info_link': '',
            'consumer_education': '',
            'disruption_mechanism': '',
            'product_info_display': 'Yes',
            'product_info_display_details': '',
        }

        # If p9_data was extracted from HTML, use those values
        if d.p9_data:
            extracted = d.p9_data

            # Update top-level fields
            for key in ['complaint_mechanism', 'env_social_pct', 'safe_usage_pct', 'recycling_pct',
                        'voluntary_recalls', 'voluntary_recall_reason', 'forced_recalls', 'forced_recall_reason',
                        'cyber_policy', 'cyber_policy_weblink', 'data_breaches', 'pii_breach_pct',
                        'data_breach_impact', 'product_info_link', 'consumer_education',
                        'disruption_mechanism', 'product_info_display', 'product_info_display_details']:
                if key in extracted and extracted[key]:
                    defaults[key] = extracted[key]

            # Update corrective_actions_q6 from extraction if present
            if extracted.get('corrective_actions_q6'):
                defaults['corrective_actions_q6'] = extracted['corrective_actions_q6']

            # Update complaints data
            if 'complaints' in extracted:
                for category, data in extracted['complaints'].items():
                    if category in defaults['complaints']:
                        for field, value in data.items():
                            if value is not None:
                                defaults['complaints'][category][field] = value

        return defaults

    def generate(self) -> str:
        """
        Generate complete XBRL XML document using Jinja2 template.

        Returns:
            str: Complete XBRL XML document as string
        """
        logger.info("Generating XBRL document using template...")

        # Build template context
        context = self._build_template_context()

        # Create Jinja2 environment with SilentUndefined for graceful handling of missing variables
        env = Environment(loader=BaseLoader(), undefined=SilentUndefined)
        template = env.from_string(XBRL_TEMPLATE)

        # Render template with context
        try:
            xml = template.render(**context)
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            raise

        logger.info("XBRL document generated successfully")
        return xml

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the generated XBRL.

        Returns:
            Dict with counts of contexts, facts, etc.
        """
        return {
            'company_name': self.data.company.company_name,
            'cin': self._get_cin(),
            'reporting_period': f"{self._format_date(self.start_date_cy)} to {self._format_date(self.end_date_cy)}",
            'total_employees': self.data.employees_workers.employees.total.total,
            'total_workers': self.data.employees_workers.workers.total.total,
            'business_activities_count': len(self.data.business_activities),
            'products_services_count': len(self.data.products_services),
            'complaints_count': len(self.data.complaints),
            'principles_count': len(self.data.principles),
        }
