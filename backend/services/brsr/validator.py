"""
BRSR XBRL Validator Service

Validates XBRL output against the in-capmkt taxonomy.
Provides multiple levels of validation:
1. Schema validation (XML structure)
2. Taxonomy validation (concept names, dimensions)
3. Business rule validation (required fields, value ranges)
"""

import re
import logging
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"      # Must fix - will fail filing
    WARNING = "warning"  # Should fix - may cause issues
    INFO = "info"        # Informational - optional improvements


@dataclass
class ValidationIssue:
    """A single validation issue found."""
    severity: ValidationSeverity
    code: str
    message: str
    element: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Complete validation result."""
    is_valid: bool = True
    issues: List[ValidationIssue] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)

    def add_error(self, code: str, message: str, **kwargs):
        self.issues.append(ValidationIssue(
            severity=ValidationSeverity.ERROR,
            code=code,
            message=message,
            **kwargs
        ))
        self.is_valid = False

    def add_warning(self, code: str, message: str, **kwargs):
        self.issues.append(ValidationIssue(
            severity=ValidationSeverity.WARNING,
            code=code,
            message=message,
            **kwargs
        ))

    def add_info(self, code: str, message: str, **kwargs):
        self.issues.append(ValidationIssue(
            severity=ValidationSeverity.INFO,
            code=code,
            message=message,
            **kwargs
        ))

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == ValidationSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == ValidationSeverity.WARNING)


class BRSRXBRLValidator:
    """
    Validates BRSR XBRL documents.

    Checks:
    - XML well-formedness
    - Namespace declarations
    - Context definitions
    - Concept names against known taxonomy
    - Dimensional validity
    - Required elements
    - Value types and formats
    """

    # Known valid concepts in the in-capmkt taxonomy
    # This is a subset - in production, load from taxonomy XSD
    VALID_CONCEPTS = {
        # Section A - General Disclosures
        'CorporateIdentityNumber',
        'NameOfListedEntity',
        'YearOfIncorporation',
        'RegisteredOfficeAddress',
        'CorporateOfficeAddress',
        'EmailAddress',
        'Telephone',
        'Website',
        'PaidUpCapital',
        'ReportingBoundary',
        'WhetherReportAssured',
        'NameOfAssuranceProvider',
        'TypeOfAssurance',

        # Employee/Worker concepts
        'NumberOfEmployeesOrWorkers',
        'PercentageOfEmployeesOrWorkers',
        'NumberOfDifferentlyAbledEmployeesOrWorkers',
        'PercentageOfDifferentlyAbledEmployeesOrWorkers',

        # Board and KMP
        'TotalNumberOfBoardOfDirectors',
        'NumberOfFemaleOnBoardOfDirectors',
        'PercentageOfFemaleOnBoardOfDirectors',
        'TotalNumberOfKeyManagementPersonnel',
        'NumberOfFemaleKeyManagementPersonnel',
        'PercentageOfFemaleKeyManagementPersonnel',

        # Complaints
        'NumberOfComplaintsFiledDuringTheYear',
        'NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear',

        # Sustainability
        'PercentageOfRAndDAndCapexInvestmentsInSpecificTechnologies',
        'NumberOfTradingHouses',
        'NumberOfDealersOrDistributors',

        # Turnover
        'TurnoverRateForPermanentEmployees',
        'TurnoverRateForPermanentWorkers',
    }

    # Valid dimension axes
    VALID_DIMENSIONS = {
        'EmployeesOrWorkersAxis',
        'DifferentlyAbledEmployeesOrWorkersAxis',
        'GenderAxis',
        'StakeholderGroupFromWhomComplaintIsReceivedAxis',
        'PrincipleAxis',
        'ReportingYearAxis',
    }

    # Valid dimension members
    VALID_MEMBERS = {
        # Employee/Worker categories
        'PermanentEmployeesMember',
        'OtherThanPermanentEmployeesMember',
        'EmployeesMember',
        'PermanentWorkersMember',
        'OtherThanPermanentWorkersMember',
        'WorkersMember',

        # Gender
        'MaleMember',
        'FemaleMember',
        'OtherGenderMember',

        # Stakeholders
        'CommunitiesMember',
        'InvestorsMember',
        'ShareholdersMember',
        'EmployeesAndWorkersMember',
        'CustomersMember',
        'ValueChainPartnersMember',
        'OtherMember',
    }

    # Required elements for a valid BRSR filing
    REQUIRED_CONCEPTS = {
        'CorporateIdentityNumber',
        'NameOfListedEntity',
    }

    # Expected namespaces
    EXPECTED_NAMESPACES = {
        'xbrli': 'http://www.xbrl.org/2003/instance',
        'in-capmkt': 'https://www.sebi.gov.in/xbrl/2025-05-31/in-capmkt',
        'xbrldi': 'http://xbrl.org/2006/xbrldi',
        'link': 'http://www.xbrl.org/2003/linkbase',
    }

    def __init__(self, xbrl_content: str):
        """
        Initialize validator with XBRL content.

        Args:
            xbrl_content: XBRL XML string to validate
        """
        self.content = xbrl_content
        self.result = ValidationResult()
        self._root: Optional[ET.Element] = None
        self._namespaces: Dict[str, str] = {}
        self._contexts: Set[str] = set()
        self._units: Set[str] = set()
        self._facts: List[ET.Element] = []

    def validate(self) -> ValidationResult:
        """
        Run all validations and return result.

        Returns:
            ValidationResult with all issues found
        """
        logger.info("Starting XBRL validation...")

        # Step 1: Parse XML
        if not self._parse_xml():
            return self.result

        # Step 2: Validate namespaces
        self._validate_namespaces()

        # Step 3: Extract and validate contexts
        self._extract_contexts()
        self._validate_contexts()

        # Step 4: Extract and validate units
        self._extract_units()

        # Step 5: Extract and validate facts
        self._extract_facts()
        self._validate_facts()

        # Step 6: Check required elements
        self._validate_required_elements()

        # Step 7: Validate dimensional consistency
        self._validate_dimensions()

        # Compile statistics
        self.result.statistics = {
            'context_count': len(self._contexts),
            'unit_count': len(self._units),
            'fact_count': len(self._facts),
            'error_count': self.result.error_count,
            'warning_count': self.result.warning_count,
        }

        logger.info(f"Validation complete. Errors: {self.result.error_count}, Warnings: {self.result.warning_count}")
        return self.result

    def _parse_xml(self) -> bool:
        """Parse XML and check well-formedness."""
        try:
            self._root = ET.fromstring(self.content)

            # Extract namespaces from root element
            for attr, value in self._root.attrib.items():
                if attr.startswith('{'):
                    continue
                if attr.startswith('xmlns:'):
                    prefix = attr.split(':')[1]
                    self._namespaces[prefix] = value
                elif attr == 'xmlns':
                    self._namespaces[''] = value

            return True
        except ET.ParseError as e:
            self.result.add_error(
                'XML_PARSE_ERROR',
                f"XML parsing failed: {str(e)}",
                suggestion="Check for unclosed tags, invalid characters, or encoding issues"
            )
            return False

    def _validate_namespaces(self):
        """Validate required namespace declarations."""
        for prefix, expected_uri in self.EXPECTED_NAMESPACES.items():
            if prefix not in self._namespaces:
                self.result.add_error(
                    'MISSING_NAMESPACE',
                    f"Missing required namespace: {prefix}",
                    suggestion=f"Add xmlns:{prefix}=\"{expected_uri}\" to root element"
                )
            elif self._namespaces[prefix] != expected_uri:
                self.result.add_warning(
                    'NAMESPACE_MISMATCH',
                    f"Namespace {prefix} has unexpected URI: {self._namespaces[prefix]}",
                    suggestion=f"Expected: {expected_uri}"
                )

    def _extract_contexts(self):
        """Extract all context IDs."""
        if self._root is None:
            return

        ns = {'xbrli': self.EXPECTED_NAMESPACES['xbrli']}
        for context in self._root.findall('.//xbrli:context', ns):
            context_id = context.get('id')
            if context_id:
                self._contexts.add(context_id)

    def _validate_contexts(self):
        """Validate context definitions."""
        if not self._contexts:
            self.result.add_error(
                'NO_CONTEXTS',
                "No contexts defined in document",
                suggestion="Add at least one xbrli:context element"
            )
            return

        # Check for required context types
        has_duration = any('D' in ctx for ctx in self._contexts)
        has_instant = any('I' in ctx for ctx in self._contexts)

        if not has_duration:
            self.result.add_warning(
                'NO_DURATION_CONTEXT',
                "No duration context found (contexts starting with 'D')",
                suggestion="Add duration contexts for period-based facts"
            )

        if not has_instant:
            self.result.add_warning(
                'NO_INSTANT_CONTEXT',
                "No instant context found (contexts starting with 'I')",
                suggestion="Add instant contexts for point-in-time facts"
            )

    def _extract_units(self):
        """Extract all unit IDs."""
        if self._root is None:
            return

        ns = {'xbrli': self.EXPECTED_NAMESPACES['xbrli']}
        for unit in self._root.findall('.//xbrli:unit', ns):
            unit_id = unit.get('id')
            if unit_id:
                self._units.add(unit_id)

    def _extract_facts(self):
        """Extract all fact elements."""
        if self._root is None:
            return

        # Facts are elements in the in-capmkt namespace
        ns_uri = self.EXPECTED_NAMESPACES.get('in-capmkt', '')
        for elem in self._root.iter():
            if elem.tag.startswith(f'{{{ns_uri}}}'):
                self._facts.append(elem)

    def _validate_facts(self):
        """Validate individual facts."""
        ns_uri = self.EXPECTED_NAMESPACES.get('in-capmkt', '')
        found_concepts = set()

        for fact in self._facts:
            # Extract concept name
            tag = fact.tag
            if tag.startswith(f'{{{ns_uri}}}'):
                concept = tag[len(f'{{{ns_uri}}}'):]
            else:
                concept = tag.split('}')[-1] if '}' in tag else tag

            found_concepts.add(concept)

            # Check if concept is known
            if concept not in self.VALID_CONCEPTS:
                self.result.add_warning(
                    'UNKNOWN_CONCEPT',
                    f"Concept '{concept}' not in known taxonomy list",
                    element=concept,
                    suggestion="Verify concept name against official SEBI taxonomy"
                )

            # Check contextRef
            context_ref = fact.get('contextRef')
            if context_ref is None:
                self.result.add_error(
                    'MISSING_CONTEXT_REF',
                    f"Fact '{concept}' missing contextRef attribute",
                    element=concept
                )
            elif context_ref not in self._contexts:
                self.result.add_error(
                    'INVALID_CONTEXT_REF',
                    f"Fact '{concept}' references undefined context: {context_ref}",
                    element=concept,
                    suggestion=f"Define context '{context_ref}' or use an existing context"
                )

            # Check unitRef for numeric concepts
            unit_ref = fact.get('unitRef')
            if unit_ref and unit_ref not in self._units:
                self.result.add_error(
                    'INVALID_UNIT_REF',
                    f"Fact '{concept}' references undefined unit: {unit_ref}",
                    element=concept
                )

            # Validate numeric values
            decimals = fact.get('decimals')
            if decimals is not None:
                try:
                    value = fact.text
                    if value:
                        float(value)
                except ValueError:
                    self.result.add_error(
                        'INVALID_NUMERIC_VALUE',
                        f"Fact '{concept}' has invalid numeric value: {fact.text}",
                        element=concept
                    )

        self.result.statistics['concepts_used'] = list(found_concepts)

    def _validate_required_elements(self):
        """Check that required elements are present."""
        ns_uri = self.EXPECTED_NAMESPACES.get('in-capmkt', '')
        found_concepts = set()

        for fact in self._facts:
            tag = fact.tag
            if tag.startswith(f'{{{ns_uri}}}'):
                concept = tag[len(f'{{{ns_uri}}}'):]
                found_concepts.add(concept)

        for required in self.REQUIRED_CONCEPTS:
            if required not in found_concepts:
                self.result.add_error(
                    'MISSING_REQUIRED',
                    f"Required concept '{required}' not found in document",
                    suggestion=f"Add <in-capmkt:{required}> element with appropriate value"
                )

    def _validate_dimensions(self):
        """Validate dimensional members in contexts."""
        if self._root is None:
            return

        ns = {
            'xbrli': self.EXPECTED_NAMESPACES['xbrli'],
            'xbrldi': self.EXPECTED_NAMESPACES.get('xbrldi', 'http://xbrl.org/2006/xbrldi'),
        }

        for context in self._root.findall('.//xbrli:context', ns):
            context_id = context.get('id', 'unknown')

            # Check scenario/segment for dimensional members
            for explicit_member in context.findall('.//xbrldi:explicitMember', ns):
                dimension = explicit_member.get('dimension', '')
                member_text = explicit_member.text or ''

                # Extract dimension name (remove namespace prefix)
                dim_name = dimension.split(':')[-1] if ':' in dimension else dimension

                # Extract member name
                member_name = member_text.split(':')[-1] if ':' in member_text else member_text

                # Validate dimension
                if dim_name and dim_name not in self.VALID_DIMENSIONS:
                    self.result.add_warning(
                        'UNKNOWN_DIMENSION',
                        f"Unknown dimension '{dim_name}' in context '{context_id}'",
                        element=context_id,
                        suggestion="Check dimension name against SEBI taxonomy"
                    )

                # Validate member
                if member_name and member_name not in self.VALID_MEMBERS:
                    self.result.add_warning(
                        'UNKNOWN_MEMBER',
                        f"Unknown member '{member_name}' for dimension '{dim_name}' in context '{context_id}'",
                        element=context_id,
                        suggestion="Check member name against SEBI taxonomy"
                    )

    def get_summary(self) -> str:
        """Get a human-readable validation summary."""
        lines = [
            "=" * 60,
            "BRSR XBRL Validation Report",
            "=" * 60,
            "",
            f"Status: {'VALID' if self.result.is_valid else 'INVALID'}",
            "",
            "Statistics:",
            f"  - Contexts: {self.result.statistics.get('context_count', 0)}",
            f"  - Units: {self.result.statistics.get('unit_count', 0)}",
            f"  - Facts: {self.result.statistics.get('fact_count', 0)}",
            f"  - Errors: {self.result.error_count}",
            f"  - Warnings: {self.result.warning_count}",
            "",
        ]

        if self.result.issues:
            lines.append("Issues Found:")
            lines.append("-" * 40)

            for issue in self.result.issues:
                severity_label = "[ERROR]" if issue.severity == ValidationSeverity.ERROR else "[WARNING]" if issue.severity == ValidationSeverity.WARNING else "[INFO]"
                lines.append(f"{severity_label} [{issue.code}] {issue.message}")
                if issue.element:
                    lines.append(f"   Element: {issue.element}")
                if issue.suggestion:
                    lines.append(f"   Suggestion: {issue.suggestion}")
                lines.append("")
        else:
            lines.append("No issues found!")

        return "\n".join(lines)


def validate_xbrl(xbrl_content: str) -> ValidationResult:
    """
    Convenience function to validate XBRL content.

    Args:
        xbrl_content: XBRL XML string

    Returns:
        ValidationResult with all validation issues
    """
    validator = BRSRXBRLValidator(xbrl_content)
    return validator.validate()


def validate_xbrl_file(file_path: str) -> ValidationResult:
    """
    Validate XBRL from file.

    Args:
        file_path: Path to XBRL file

    Returns:
        ValidationResult with all validation issues
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return validate_xbrl(content)
