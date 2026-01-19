"""
BRSR (Business Responsibility & Sustainability Report) Services

This module provides services for:
- Parsing BRSR HTML reports
- Extracting structured data
- Generating SEBI-compliant XBRL XML
- Validating XBRL output
- Comparing XBRL documents
- Interactive viewing with tag mappings
"""

from .html_parser import BRSRHTMLParser
from .xbrl_generator import BRSRXBRLGenerator
from .brsr_service import BRSRService, get_brsr_service
from .validator import BRSRXBRLValidator, validate_xbrl, validate_xbrl_file, ValidationResult
from .comparator import BRSRXBRLComparator, compare_xbrl, compare_xbrl_files, ComparisonResult
from .interactive_parser import (
    BRSRInteractiveParser,
    convert_interactive,
    update_xbrl_tags,
)

__all__ = [
    "BRSRHTMLParser",
    "BRSRXBRLGenerator",
    "BRSRService",
    "get_brsr_service",
    "BRSRXBRLValidator",
    "validate_xbrl",
    "validate_xbrl_file",
    "ValidationResult",
    "BRSRXBRLComparator",
    "compare_xbrl",
    "compare_xbrl_files",
    "ComparisonResult",
    "BRSRInteractiveParser",
    "convert_interactive",
    "update_xbrl_tags",
]
