"""
BRSR XBRL Comparator Service

Compares generated XBRL against reference/sample files to verify correctness.
Useful for testing and debugging tag assignments.
"""

import logging
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from xml.etree import ElementTree as ET
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class FactDifference:
    """Represents a difference between two facts."""
    concept: str
    context: str
    difference_type: str  # 'missing', 'extra', 'value_mismatch', 'context_mismatch'
    expected_value: Optional[str] = None
    actual_value: Optional[str] = None
    message: str = ""


@dataclass
class ComparisonResult:
    """Result of comparing two XBRL documents."""
    is_match: bool = True
    total_facts_expected: int = 0
    total_facts_actual: int = 0
    matching_facts: int = 0
    differences: List[FactDifference] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)
    # Structure-only comparison fields
    structure_only: bool = False
    total_concepts_expected: int = 0
    total_concepts_actual: int = 0
    matching_concepts: int = 0
    missing_concepts: List[str] = field(default_factory=list)
    extra_concepts: List[str] = field(default_factory=list)
    common_concepts: List[str] = field(default_factory=list)

    @property
    def match_percentage(self) -> float:
        if self.structure_only:
            # For structure-only, compare concept coverage
            if self.total_concepts_expected == 0:
                return 100.0 if self.total_concepts_actual == 0 else 0.0
            return (self.matching_concepts / self.total_concepts_expected) * 100
        else:
            if self.total_facts_expected == 0:
                return 100.0 if self.total_facts_actual == 0 else 0.0
            return (self.matching_facts / self.total_facts_expected) * 100


@dataclass
class ParsedFact:
    """A parsed XBRL fact with all its attributes."""
    concept: str
    value: str
    context_ref: str
    unit_ref: Optional[str] = None
    decimals: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)


class BRSRXBRLComparator:
    """
    Compares two XBRL documents to find differences.

    Useful for:
    - Verifying generated output against known valid samples
    - Debugging tag assignments
    - Regression testing
    """

    NAMESPACES = {
        'xbrli': 'http://www.xbrl.org/2003/instance',
        'in-capmkt': 'https://www.sebi.gov.in/xbrl/2025-05-31/in-capmkt',
        'xbrldi': 'http://xbrl.org/2006/xbrldi',
    }

    def __init__(
        self,
        expected_content: str,
        actual_content: str,
        ignore_whitespace: bool = True,
        ignore_decimals: bool = False,
        structure_only: bool = False,
    ):
        """
        Initialize comparator with two XBRL documents.

        Args:
            expected_content: Reference/expected XBRL content
            actual_content: Generated/actual XBRL content
            ignore_whitespace: Ignore whitespace differences in values
            ignore_decimals: Ignore decimal precision differences
            structure_only: Only compare which concepts/tags are used, ignore values
        """
        self.expected_content = expected_content
        self.actual_content = actual_content
        self.ignore_whitespace = ignore_whitespace
        self.ignore_decimals = ignore_decimals
        self.structure_only = structure_only

        self._expected_root: Optional[ET.Element] = None
        self._actual_root: Optional[ET.Element] = None
        self._expected_facts: List[ParsedFact] = []
        self._actual_facts: List[ParsedFact] = []

    def compare(self) -> ComparisonResult:
        """
        Compare the two XBRL documents.

        Returns:
            ComparisonResult with all differences found
        """
        result = ComparisonResult()
        result.structure_only = self.structure_only

        # Parse both documents
        try:
            self._expected_root = ET.fromstring(self.expected_content)
            self._actual_root = ET.fromstring(self.actual_content)
        except ET.ParseError as e:
            result.is_match = False
            result.differences.append(FactDifference(
                concept="",
                context="",
                difference_type="parse_error",
                message=f"Failed to parse XML: {str(e)}"
            ))
            return result

        # Extract facts from both
        self._expected_facts = self._extract_facts(self._expected_root)
        self._actual_facts = self._extract_facts(self._actual_root)

        result.total_facts_expected = len(self._expected_facts)
        result.total_facts_actual = len(self._actual_facts)

        if self.structure_only:
            # Structure-only comparison: just compare which concepts are used
            return self._compare_structure(result)
        else:
            # Full comparison: compare concepts + contexts + values
            return self._compare_full(result)

    def _compare_structure(self, result: ComparisonResult) -> ComparisonResult:
        """Compare only the structure (which concepts are used), ignoring values."""
        # Get unique concepts from both documents
        expected_concepts = set(f.concept for f in self._expected_facts)
        actual_concepts = set(f.concept for f in self._actual_facts)

        # Calculate structure metrics
        common = expected_concepts & actual_concepts
        missing = expected_concepts - actual_concepts
        extra = actual_concepts - expected_concepts

        result.total_concepts_expected = len(expected_concepts)
        result.total_concepts_actual = len(actual_concepts)
        result.matching_concepts = len(common)
        result.common_concepts = sorted(list(common))
        result.missing_concepts = sorted(list(missing))
        result.extra_concepts = sorted(list(extra))

        # Create differences for missing/extra concepts
        for concept in missing:
            result.differences.append(FactDifference(
                concept=concept,
                context="",
                difference_type="missing",
                message=f"Concept not found in your file"
            ))

        for concept in extra:
            result.differences.append(FactDifference(
                concept=concept,
                context="",
                difference_type="extra",
                message=f"Extra concept in your file (not in reference)"
            ))

        result.is_match = len(missing) == 0 and len(extra) == 0
        result.matching_facts = result.matching_concepts  # For compatibility

        # Compile statistics
        result.statistics = {
            'expected_concepts': sorted(list(expected_concepts)),
            'actual_concepts': sorted(list(actual_concepts)),
            'common_concepts': sorted(list(common)),
            'missing_count': len(missing),
            'extra_count': len(extra),
            'mismatch_count': 0,  # No value mismatches in structure-only mode
            'structure_match_percentage': result.match_percentage,
        }

        return result

    def _compare_full(self, result: ComparisonResult) -> ComparisonResult:
        """Full comparison: compare concepts + contexts + values."""
        # Build lookup maps
        expected_map = self._build_fact_map(self._expected_facts)
        actual_map = self._build_fact_map(self._actual_facts)

        # Find matching and differing facts
        all_keys = set(expected_map.keys()) | set(actual_map.keys())

        for key in all_keys:
            expected_fact = expected_map.get(key)
            actual_fact = actual_map.get(key)

            if expected_fact is None:
                # Extra fact in actual
                result.differences.append(FactDifference(
                    concept=actual_fact.concept,
                    context=actual_fact.context_ref,
                    difference_type="extra",
                    actual_value=actual_fact.value,
                    message=f"Extra fact in generated output"
                ))
                result.is_match = False

            elif actual_fact is None:
                # Missing fact in actual
                result.differences.append(FactDifference(
                    concept=expected_fact.concept,
                    context=expected_fact.context_ref,
                    difference_type="missing",
                    expected_value=expected_fact.value,
                    message=f"Missing fact in generated output"
                ))
                result.is_match = False

            else:
                # Both exist - compare values
                if self._values_match(expected_fact.value, actual_fact.value):
                    result.matching_facts += 1
                else:
                    result.differences.append(FactDifference(
                        concept=expected_fact.concept,
                        context=expected_fact.context_ref,
                        difference_type="value_mismatch",
                        expected_value=expected_fact.value,
                        actual_value=actual_fact.value,
                        message=f"Value mismatch"
                    ))
                    result.is_match = False

        # Compile statistics
        result.statistics = {
            'expected_concepts': list(set(f.concept for f in self._expected_facts)),
            'actual_concepts': list(set(f.concept for f in self._actual_facts)),
            'missing_count': sum(1 for d in result.differences if d.difference_type == 'missing'),
            'extra_count': sum(1 for d in result.differences if d.difference_type == 'extra'),
            'mismatch_count': sum(1 for d in result.differences if d.difference_type == 'value_mismatch'),
        }

        return result

    def _extract_facts(self, root: ET.Element) -> List[ParsedFact]:
        """Extract all facts from an XBRL document."""
        facts = []
        ns_uri = self.NAMESPACES.get('in-capmkt', '')

        for elem in root.iter():
            # Check if this is a fact element (in in-capmkt namespace)
            if elem.tag.startswith(f'{{{ns_uri}}}'):
                concept = elem.tag[len(f'{{{ns_uri}}}'):]

                fact = ParsedFact(
                    concept=concept,
                    value=elem.text.strip() if elem.text else '',
                    context_ref=elem.get('contextRef', ''),
                    unit_ref=elem.get('unitRef'),
                    decimals=elem.get('decimals'),
                )

                # Extract dimensions from context (if needed)
                # This is simplified - full implementation would parse contexts

                facts.append(fact)

        return facts

    def _build_fact_map(self, facts: List[ParsedFact]) -> Dict[str, ParsedFact]:
        """Build a map of facts keyed by concept+context."""
        fact_map = {}
        for fact in facts:
            key = f"{fact.concept}::{fact.context_ref}"
            fact_map[key] = fact
        return fact_map

    def _values_match(self, expected: str, actual: str) -> bool:
        """Check if two values match, with optional tolerance."""
        if self.ignore_whitespace:
            expected = expected.strip()
            actual = actual.strip()

        if expected == actual:
            return True

        # Try numeric comparison
        if self.ignore_decimals:
            try:
                exp_num = float(expected)
                act_num = float(actual)
                return abs(exp_num - act_num) < 0.01  # 1% tolerance
            except ValueError:
                pass

        return False

    def get_summary(self) -> str:
        """Get a human-readable comparison summary."""
        result = self.compare()

        if result.structure_only:
            return self._get_structure_summary(result)
        else:
            return self._get_full_summary(result)

    def _get_structure_summary(self, result: ComparisonResult) -> str:
        """Get summary for structure-only comparison."""
        lines = [
            "=" * 60,
            "BRSR XBRL Structure Comparison Report",
            "(Comparing tags/concepts only, ignoring values)",
            "=" * 60,
            "",
            f"Structure Match: {result.match_percentage:.1f}%",
            "",
            "Concept Counts:",
            f"  - Reference file concepts: {result.total_concepts_expected}",
            f"  - Your file concepts: {result.total_concepts_actual}",
            f"  - Matching concepts: {result.matching_concepts}",
            f"  - Missing from your file: {len(result.missing_concepts)}",
            f"  - Extra in your file: {len(result.extra_concepts)}",
            "",
        ]

        if result.common_concepts:
            lines.append(f"Matching Concepts ({len(result.common_concepts)}):")
            lines.append("-" * 40)
            for concept in result.common_concepts[:15]:
                lines.append(f"   • {concept}")
            if len(result.common_concepts) > 15:
                lines.append(f"   ... and {len(result.common_concepts) - 15} more")
            lines.append("")

        if result.missing_concepts:
            lines.append(f"Missing from Your File ({len(result.missing_concepts)}):")
            lines.append("-" * 40)
            for concept in result.missing_concepts:
                lines.append(f"   • {concept}")
            lines.append("")

        if result.extra_concepts:
            lines.append(f"Extra in Your File ({len(result.extra_concepts)}):")
            lines.append("-" * 40)
            for concept in result.extra_concepts:
                lines.append(f"   • {concept}")
            lines.append("")

        if not result.missing_concepts and not result.extra_concepts:
            lines.append("Perfect structure match! All concepts aligned.")

        return "\n".join(lines)

    def _get_full_summary(self, result: ComparisonResult) -> str:
        """Get summary for full comparison (concepts + values)."""
        lines = [
            "=" * 60,
            "BRSR XBRL Comparison Report",
            "=" * 60,
            "",
            f"Status: {'MATCH' if result.is_match else 'DIFFERENCES FOUND'}",
            f"Match Rate: {result.match_percentage:.1f}%",
            "",
            "Counts:",
            f"  - Expected facts: {result.total_facts_expected}",
            f"  - Actual facts: {result.total_facts_actual}",
            f"  - Matching: {result.matching_facts}",
            f"  - Missing: {result.statistics.get('missing_count', 0)}",
            f"  - Extra: {result.statistics.get('extra_count', 0)}",
            f"  - Mismatched: {result.statistics.get('mismatch_count', 0)}",
            "",
        ]

        if result.differences:
            lines.append("Differences:")
            lines.append("-" * 40)

            for diff in result.differences[:20]:  # Limit to first 20
                diff_label = f"[{diff.difference_type.upper()}]"
                lines.append(f"{diff_label} {diff.concept}")
                lines.append(f"   Context: {diff.context}")
                if diff.expected_value:
                    lines.append(f"   Expected: {diff.expected_value[:50]}")
                if diff.actual_value:
                    lines.append(f"   Actual: {diff.actual_value[:50]}")
                lines.append("")

            if len(result.differences) > 20:
                lines.append(f"... and {len(result.differences) - 20} more differences")
        else:
            lines.append("No differences found!")

        return "\n".join(lines)


def compare_xbrl(expected: str, actual: str, **kwargs) -> ComparisonResult:
    """
    Compare two XBRL documents.

    Args:
        expected: Reference XBRL content
        actual: Generated XBRL content
        **kwargs: Additional options (ignore_whitespace, ignore_decimals)

    Returns:
        ComparisonResult with differences
    """
    comparator = BRSRXBRLComparator(expected, actual, **kwargs)
    return comparator.compare()


def compare_xbrl_files(expected_path: str, actual_path: str, **kwargs) -> ComparisonResult:
    """
    Compare two XBRL files.

    Args:
        expected_path: Path to reference file
        actual_path: Path to generated file
        **kwargs: Additional options

    Returns:
        ComparisonResult with differences
    """
    with open(expected_path, 'r', encoding='utf-8') as f:
        expected = f.read()
    with open(actual_path, 'r', encoding='utf-8') as f:
        actual = f.read()

    return compare_xbrl(expected, actual, **kwargs)
