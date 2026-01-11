"""
BRSR Service

Main service orchestrating BRSR HTML parsing and XBRL generation.
Provides high-level API for BRSR report conversion.
"""

import logging
from typing import Optional, Dict, Any, Tuple
from datetime import date
from pathlib import Path

from schemas.brsr import (
    BRSRReportData,
    BRSRConversionRequest,
    BRSRConversionResponse,
    BRSRValidationResult,
)
from .html_parser import BRSRHTMLParser
from .xbrl_generator import BRSRXBRLGenerator

logger = logging.getLogger(__name__)


class BRSRService:
    """
    High-level service for BRSR report processing.

    Orchestrates:
    - HTML file loading and parsing
    - Data extraction and validation
    - XBRL XML generation
    - Cell-to-tag mapping generation
    """

    def __init__(self):
        """Initialize BRSR service."""
        self._parser: Optional[BRSRHTMLParser] = None
        self._generator: Optional[BRSRXBRLGenerator] = None
        self._report_data: Optional[BRSRReportData] = None

    def load_html_file(self, file_path: str) -> str:
        """
        Load HTML content from file.

        Args:
            file_path: Path to HTML file

        Returns:
            str: HTML content

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not readable
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.suffix.lower() in ['.html', '.htm']:
            logger.warning(f"File {file_path} may not be an HTML file")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encodings
            for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    with open(path, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue

            raise ValueError(f"Unable to read file with supported encodings: {file_path}")

    def parse_html(self, html_content: str) -> BRSRReportData:
        """
        Parse HTML content and extract BRSR data.

        Args:
            html_content: Raw HTML string

        Returns:
            BRSRReportData: Extracted report data
        """
        logger.info("Parsing BRSR HTML content...")

        self._parser = BRSRHTMLParser(html_content)
        self._report_data = self._parser.parse()

        logger.info(f"Parsing complete. Company: {self._report_data.company.company_name}")
        return self._report_data

    def validate_html(self, html_content: str) -> BRSRValidationResult:
        """
        Validate HTML content structure.

        Args:
            html_content: Raw HTML string

        Returns:
            BRSRValidationResult: Validation results
        """
        parser = BRSRHTMLParser(html_content)
        return parser.validate()

    def generate_xbrl(
        self,
        report_data: Optional[BRSRReportData] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> str:
        """
        Generate XBRL XML from report data.

        Args:
            report_data: Parsed report data (uses cached if not provided)
            start_date: Start date of reporting period
            end_date: End date of reporting period

        Returns:
            str: XBRL XML content

        Raises:
            ValueError: If no report data available
        """
        data = report_data or self._report_data

        if data is None:
            raise ValueError("No report data available. Parse HTML first or provide report_data.")

        self._generator = BRSRXBRLGenerator(
            report_data=data,
            start_date_cy=start_date,
            end_date_cy=end_date,
        )

        return self._generator.generate()

    def convert(
        self,
        html_content: Optional[str] = None,
        file_path: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_mapping: bool = False,
    ) -> BRSRConversionResponse:
        """
        Complete conversion from HTML to XBRL.

        Args:
            html_content: HTML content as string
            file_path: Path to HTML file (used if html_content not provided)
            start_date: Start date of reporting period
            end_date: End date of reporting period
            include_mapping: Whether to include cell-to-tag mapping

        Returns:
            BRSRConversionResponse: Conversion results
        """
        try:
            # Load HTML if file path provided
            if html_content is None:
                if file_path is None:
                    return BRSRConversionResponse(
                        success=False,
                        message="Either html_content or file_path must be provided"
                    )
                html_content = self.load_html_file(file_path)

            # Validate
            validation = self.validate_html(html_content)
            if not validation.is_valid:
                return BRSRConversionResponse(
                    success=False,
                    message=f"Validation failed: {', '.join(validation.errors)}",
                    statistics={
                        'validation_errors': validation.errors,
                        'validation_warnings': validation.warnings,
                    }
                )

            # Parse
            report_data = self.parse_html(html_content)

            # Generate XBRL
            xbrl_content = self.generate_xbrl(
                report_data=report_data,
                start_date=start_date,
                end_date=end_date,
            )

            # Get statistics
            statistics = self._generator.get_statistics() if self._generator else {}
            statistics.update({
                'sections_found': validation.sections_found,
                'table_count': validation.table_count,
                'warnings': validation.warnings,
            })

            # Build response
            response = BRSRConversionResponse(
                success=True,
                message="Conversion completed successfully",
                xbrl_content=xbrl_content,
                report_data=report_data,
                statistics=statistics,
            )

            # Include mapping if requested
            if include_mapping:
                response.mapping_data = self._generate_mapping(report_data)

            logger.info(f"Conversion complete for {report_data.company.company_name}")
            return response

        except FileNotFoundError as e:
            return BRSRConversionResponse(
                success=False,
                message=str(e)
            )
        except Exception as e:
            logger.error(f"Conversion failed: {e}", exc_info=True)
            return BRSRConversionResponse(
                success=False,
                message=f"Conversion failed: {str(e)}"
            )

    def _generate_mapping(self, report_data: BRSRReportData) -> Dict[str, Any]:
        """
        Generate cell-to-tag mapping data.

        This creates a mapping structure that can be used by interactive viewers
        to link HTML table cells to their corresponding XBRL tags.

        Args:
            report_data: Parsed report data

        Returns:
            Dict mapping cell IDs to XBRL tag information
        """
        mapping = {}
        cell_id = 0

        emp = report_data.employees_workers

        # Employee/Worker mappings
        emp_categories = [
            ('Permanent Employees', emp.employees.permanent, 'PermanentEmployees', 'TableA'),
            ('Other Employees', emp.employees.other, 'OtherThanPermanentEmployees', 'TableA'),
            ('Total Employees', emp.employees.total, 'Employees', 'TableA'),
            ('Permanent Workers', emp.workers.permanent, 'PermanentWorkers', 'TableA'),
            ('Other Workers', emp.workers.other, 'OtherThanPermanentWorkers', 'TableA'),
            ('Total Workers', emp.workers.total, 'Workers', 'TableA'),
        ]

        for label, breakdown, cat_id, table in emp_categories:
            # Total
            mapping[str(cell_id)] = [{
                't': 'in-capmkt:NumberOfEmployeesOrWorkers',
                'v': str(breakdown.total),
                'c': f'D_Gender_{cat_id}_{table}',
                'd': [f'in-capmkt:EmployeesOrWorkersAxis=in-capmkt:{cat_id}Member'],
                'u': 'pure',
                'label': f'{label} - Total'
            }]
            cell_id += 1

            # Male
            mapping[str(cell_id)] = [{
                't': 'in-capmkt:NumberOfEmployeesOrWorkers',
                'v': str(breakdown.male),
                'c': f'D_Male_{cat_id}_{table}',
                'd': [
                    f'in-capmkt:EmployeesOrWorkersAxis=in-capmkt:{cat_id}Member',
                    'in-capmkt:GenderAxis=in-capmkt:MaleMember'
                ],
                'u': 'pure',
                'label': f'{label} - Male'
            }]
            cell_id += 1

            # Female
            mapping[str(cell_id)] = [{
                't': 'in-capmkt:NumberOfEmployeesOrWorkers',
                'v': str(breakdown.female),
                'c': f'D_Female_{cat_id}_{table}',
                'd': [
                    f'in-capmkt:EmployeesOrWorkersAxis=in-capmkt:{cat_id}Member',
                    'in-capmkt:GenderAxis=in-capmkt:FemaleMember'
                ],
                'u': 'pure',
                'label': f'{label} - Female'
            }]
            cell_id += 1

        # Complaints mappings
        stakeholder_labels = {
            'Communities': 'Communities',
            'Investors': 'Investors',
            'Shareholders': 'Shareholders',
            'EmployeesAndWorkers': 'Employees and Workers',
            'Customers': 'Customers',
            'ValueChainPartners': 'Value Chain Partners',
            'Other': 'Other',
        }

        for complaint in report_data.complaints:
            if complaint.stakeholder in stakeholder_labels:
                label = stakeholder_labels[complaint.stakeholder]

                mapping[str(cell_id)] = [{
                    't': 'in-capmkt:NumberOfComplaintsFiledDuringTheYear',
                    'v': str(complaint.filed_cy),
                    'c': f'I_ComplaintReceivedFrom{complaint.stakeholder}_CY',
                    'd': [f'in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis=in-capmkt:{complaint.stakeholder}Member'],
                    'u': 'pure',
                    'label': f'{label} - Complaints Filed (CY)'
                }]
                cell_id += 1

                mapping[str(cell_id)] = [{
                    't': 'in-capmkt:NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear',
                    'v': str(complaint.pending_cy),
                    'c': f'I_ComplaintReceivedFrom{complaint.stakeholder}_CY',
                    'd': [f'in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis=in-capmkt:{complaint.stakeholder}Member'],
                    'u': 'pure',
                    'label': f'{label} - Complaints Pending (CY)'
                }]
                cell_id += 1

        return mapping

    def convert_from_request(self, request: BRSRConversionRequest) -> BRSRConversionResponse:
        """
        Convert using a request model.

        Args:
            request: Conversion request with parameters

        Returns:
            BRSRConversionResponse: Conversion results
        """
        return self.convert(
            html_content=request.html_content,
            file_path=request.file_path,
            start_date=request.reporting_period_start,
            end_date=request.reporting_period_end,
            include_mapping=request.include_mapping,
        )


# Singleton instance
_brsr_service: Optional[BRSRService] = None


def get_brsr_service() -> BRSRService:
    """Get or create BRSR service instance."""
    global _brsr_service
    if _brsr_service is None:
        _brsr_service = BRSRService()
    return _brsr_service
