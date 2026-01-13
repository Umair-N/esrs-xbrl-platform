"""
BRSR Interactive Parser Service

Generates annotated HTML with data-id attributes and creates tag mappings
for interactive viewing and editing of XBRL-tagged BRSR reports.
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import date
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from schemas.brsr import (
    BRSRReportData,
    InteractiveConversionResponse,
    TagUpdateRequest,
    TagUpdateResponse,
)
from .html_parser import BRSRHTMLParser
from .xbrl_generator import BRSRXBRLGenerator

logger = logging.getLogger(__name__)


class XBRLTagExtractor:
    """Extract tag information from generated XBRL content."""

    # XBRL namespace prefixes
    NAMESPACES = {
        'in-capmkt': 'https://www.sebi.gov.in/xbrl/2025-05-31/in-capmkt',
        'xbrli': 'http://www.xbrl.org/2003/instance',
    }

    # Tag groups - related tags that should be shown together
    # When any tag from a group is matched, all tags in the group are returned
    TAG_GROUPS = {
        'financial_year_dates': [
            'in-capmkt:DateOfStartOfFinancialYear',
            'in-capmkt:DateOfEndOfFinancialYear',
            'in-capmkt:DateOfStartOfPreviousYear',
            'in-capmkt:DateOfEndOfPreviousYear',
            'in-capmkt:DateOfStartOfPriorToPreviousYear',
            'in-capmkt:DateOfEndOfPriorToPreviousYear',
        ],
        # Add more groups as needed, e.g.:
        # 'company_registration': [
        #     'in-capmkt:CINOfCompany',
        #     'in-capmkt:DateOfIncorporation',
        #     'in-capmkt:YearOfIncorporation',
        # ],
    }

    # Keywords that trigger showing all tags from a group
    GROUP_TRIGGER_KEYWORDS = {
        'financial_year_dates': [
            'financial year',
            'reporting period',
            'fy ',
            'f.y.',
            'fiscal year',
        ],
    }

    def __init__(self, xbrl_content: str):
        self.xbrl_content = xbrl_content
        self.value_to_tags: Dict[str, List[Dict[str, Any]]] = {}
        self.tag_to_info: Dict[str, Dict[str, Any]] = {}  # Maps tag name to its info
        self._parse_xbrl()

    def _parse_xbrl(self):
        """Parse XBRL and extract value-to-tag mappings."""
        try:
            # Parse XML
            root = ET.fromstring(self.xbrl_content)

            # Register namespaces
            for prefix, uri in self.NAMESPACES.items():
                ET.register_namespace(prefix, uri)

            # Find all elements with in-capmkt namespace
            for elem in root.iter():
                tag_name = elem.tag

                # Skip non-data elements
                if not tag_name or '}' not in tag_name:
                    continue

                # Extract namespace and local name
                ns, local_name = tag_name.rsplit('}', 1)
                ns = ns.lstrip('{')

                # Only process in-capmkt tags
                if 'in-capmkt' not in ns and 'capmkt' not in ns:
                    continue

                # Get tag value
                value = (elem.text or '').strip()
                if not value:
                    continue

                # Get attributes
                context_ref = elem.get('contextRef', '')
                unit_ref = elem.get('unitRef', '')
                decimals = elem.get('decimals', '')

                # Create full tag name
                full_tag = f"in-capmkt:{local_name}"

                # Create tag info
                tag_info = {
                    't': full_tag,
                    'v': value,
                    'c': context_ref,
                    'u': unit_ref if unit_ref else None,
                    'decimals': decimals if decimals else None,
                }

                # Store in tag_to_info for group lookups
                self.tag_to_info[full_tag] = tag_info

                # Normalize value for matching
                normalized_value = self._normalize_value(value)

                # Store mapping
                if normalized_value not in self.value_to_tags:
                    self.value_to_tags[normalized_value] = []
                self.value_to_tags[normalized_value].append(tag_info)

        except ET.ParseError as e:
            logger.error(f"Failed to parse XBRL: {e}")

    def _get_tag_group(self, tag_name: str) -> Optional[str]:
        """Get the group name that a tag belongs to, if any."""
        for group_name, tags in self.TAG_GROUPS.items():
            if tag_name in tags:
                return group_name
        return None

    def _get_all_group_tags(self, group_name: str) -> List[Dict[str, Any]]:
        """Get all tag infos for a given group."""
        group_tags = []
        for tag_name in self.TAG_GROUPS.get(group_name, []):
            if tag_name in self.tag_to_info:
                group_tags.append(self.tag_to_info[tag_name])
        return group_tags

    def _check_group_trigger(self, row_context: str, col_context: str) -> Optional[str]:
        """
        Check if the context triggers a tag group.

        Returns the group name if triggered, None otherwise.
        """
        combined_context = f"{row_context} {col_context}".lower()

        for group_name, keywords in self.GROUP_TRIGGER_KEYWORDS.items():
            for keyword in keywords:
                if keyword in combined_context:
                    return group_name

        return None

    @staticmethod
    def _normalize_value(value: str) -> str:
        """Normalize value for matching."""
        if not value:
            return ''

        # Remove whitespace and convert to lowercase
        normalized = re.sub(r'\s+', ' ', value).strip().lower()

        # Remove common formatting characters
        normalized = normalized.replace(',', '')  # Remove commas from numbers
        normalized = normalized.replace('₹', '')  # Remove rupee symbol
        normalized = normalized.replace('$', '')  # Remove dollar symbol
        normalized = normalized.replace('%', '')  # Remove percent symbol

        # Remove leading/trailing quotes
        normalized = normalized.strip('"\'')

        # Normalize dashes and hyphens
        normalized = re.sub(r'[–—−]', '-', normalized)

        return normalized.strip()

    @staticmethod
    def _extract_numeric(value: str) -> float:
        """Extract numeric value, handling Indian number formats (Crores, Lakhs)."""
        if not value:
            return 0.0

        value_lower = value.lower().replace(',', '').strip()

        # Extract the number part
        numbers = re.findall(r'[\d.]+', value_lower)
        if not numbers:
            return 0.0

        try:
            num = float(numbers[0])
        except ValueError:
            return 0.0

        # Check for Indian number units and scale accordingly
        if 'crore' in value_lower or 'cr' in value_lower:
            num *= 10000000  # 1 Crore = 10 million
        elif 'lakh' in value_lower or 'lac' in value_lower:
            num *= 100000  # 1 Lakh = 100 thousand
        elif 'million' in value_lower or 'mn' in value_lower:
            num *= 1000000
        elif 'billion' in value_lower or 'bn' in value_lower:
            num *= 1000000000
        elif 'thousand' in value_lower or 'k' in value_lower:
            num *= 1000

        return num

    @staticmethod
    def _numbers_match(num1: float, num2: float, tolerance: float = 0.01) -> bool:
        """Check if two numbers match within a tolerance (handles rounding)."""
        if num1 == 0 and num2 == 0:
            return True
        if num1 == 0 or num2 == 0:
            return False

        # Check if they're equal or one is a scaled version of another
        ratio = num1 / num2 if num2 != 0 else 0

        # Direct match within tolerance
        if abs(num1 - num2) / max(abs(num1), abs(num2)) < tolerance:
            return True

        # Check common scaling factors (Crores, Lakhs, etc.)
        scaling_factors = [1, 100, 1000, 100000, 10000000, 1000000, 1000000000]
        for factor in scaling_factors:
            if abs(num1 - num2 * factor) / max(abs(num1), 1) < tolerance:
                return True
            if abs(num2 - num1 * factor) / max(abs(num2), 1) < tolerance:
                return True

        return False

    def get_tags_for_value(
        self,
        value: str,
        row_context: str = '',
        col_context: str = '',
    ) -> List[Dict[str, Any]]:
        """
        Get XBRL tags that have the given value.

        When multiple tags match the same value, uses row_context and col_context
        to find the most relevant tag for this specific cell position.

        Special handling for tag groups: when the context triggers a group
        (e.g., "financial year" triggers the financial_year_dates group),
        all tags in that group are returned together.

        Args:
            value: The cell value to match
            row_context: Text from the row header (e.g., "Permanent Employees")
            col_context: Text from the column header (e.g., "Male", "Female")

        Returns:
            List of matching tags (may be multiple for grouped tags, single for normal)
        """
        if not value or not value.strip():
            return []

        # Check if context triggers a tag group (e.g., "financial year")
        triggered_group = self._check_group_trigger(row_context, col_context)
        if triggered_group:
            group_tags = self._get_all_group_tags(triggered_group)
            if group_tags:
                return group_tags

        normalized = self._normalize_value(value)
        candidate_tags: List[Dict[str, Any]] = []

        # Try exact match first
        if normalized in self.value_to_tags:
            candidate_tags = self.value_to_tags[normalized]

        # Try numeric match for number values (handles Crores, Lakhs, etc.)
        if not candidate_tags:
            numeric_value = self._extract_numeric(value)
            if numeric_value > 0:
                for stored_value, tags in self.value_to_tags.items():
                    stored_numeric = self._extract_numeric(stored_value)
                    if stored_numeric > 0 and self._numbers_match(numeric_value, stored_numeric):
                        candidate_tags = tags
                        break

        # Try partial match for longer text values
        if not candidate_tags and len(normalized) > 20:
            for stored_value, tags in self.value_to_tags.items():
                # Check if one contains the other
                if normalized in stored_value or stored_value in normalized:
                    candidate_tags = tags
                    break
                # Check if significant overlap (for truncated values)
                if len(stored_value) > 15:
                    # Compare first 50 chars
                    if normalized[:50] == stored_value[:50]:
                        candidate_tags = tags
                        break

        # No candidates found
        if not candidate_tags:
            return []

        # If only one candidate, check if it belongs to a group
        if len(candidate_tags) == 1:
            tag = candidate_tags[0]
            group_name = self._get_tag_group(tag.get('t', ''))
            if group_name:
                # Return all tags in the group
                return self._get_all_group_tags(group_name)
            return candidate_tags

        # Multiple candidates - use context to find the best match
        best_match = self._find_best_match(candidate_tags, row_context, col_context)
        if best_match:
            # Check if best match belongs to a group
            group_name = self._get_tag_group(best_match.get('t', ''))
            if group_name:
                return self._get_all_group_tags(group_name)
            return [best_match]
        return []

    def _find_best_match(
        self,
        candidates: List[Dict[str, Any]],
        row_context: str,
        col_context: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Find the best matching tag from candidates using row/column context.

        Uses the tag name to match against contextual keywords.
        E.g., tag 'NumberOfPermanentEmployeesMale' should match when:
        - row_context contains 'permanent' AND col_context contains 'male'
        """
        if not candidates:
            return None

        row_lower = row_context.lower() if row_context else ''
        col_lower = col_context.lower() if col_context else ''

        # Common keywords to match in tag names
        context_keywords = {
            # Gender keywords
            'male': ['male', 'men', 'm'],
            'female': ['female', 'women', 'f'],
            # Employee type keywords
            'permanent': ['permanent', 'perm'],
            'other': ['other', 'contractual', 'temporary', 'temp'],
            'worker': ['worker', 'labour', 'labor'],
            'employee': ['employee', 'staff'],
            # Period keywords
            'current': ['currentyear', 'cy', 'current'],
            'previous': ['previousyear', 'py', 'previous', 'prior'],
            # Total keywords
            'total': ['total', 'aggregate', 'sum'],
            # Percentage keywords
            'percent': ['percent', 'pct', 'percentage', '%'],
        }

        scored_candidates = []
        for tag in candidates:
            tag_name = tag.get('t', '').lower()
            score = 0

            # Score based on row context
            if row_lower:
                for keyword, patterns in context_keywords.items():
                    if any(kw in row_lower for kw in [keyword] + patterns):
                        if any(p in tag_name for p in patterns) or keyword in tag_name:
                            score += 10

            # Score based on column context
            if col_lower:
                for keyword, patterns in context_keywords.items():
                    if any(kw in col_lower for kw in [keyword] + patterns):
                        if any(p in tag_name for p in patterns) or keyword in tag_name:
                            score += 10

            # Extra score for highly specific matches
            # Check if row context words appear directly in tag name
            if row_lower:
                for word in row_lower.split():
                    if len(word) > 3 and word in tag_name:
                        score += 5

            if col_lower:
                for word in col_lower.split():
                    if len(word) > 3 and word in tag_name:
                        score += 5

            scored_candidates.append((score, tag))

        # Sort by score descending
        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        # Return best match, or first candidate if no context helped
        if scored_candidates:
            best_score, best_tag = scored_candidates[0]
            # If best score is 0, we couldn't disambiguate - return first
            if best_score == 0:
                return candidates[0]
            return best_tag

        return candidates[0] if candidates else None

    def get_all_tags(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all value-to-tag mappings."""
        return self.value_to_tags


class BRSRInteractiveParser:
    """
    Parser for generating interactive BRSR HTML with XBRL tag mappings.

    This service:
    1. Parses BRSR HTML and extracts data
    2. Generates XBRL to get actual tags
    3. Annotates HTML cells with data-id attributes
    4. Maps cell values to actual XBRL tags from generated output
    """

    PERIOD_FORMAT = '{} to {}'

    def __init__(
        self,
        html_content: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ):
        self.html_content = html_content
        self.soup = BeautifulSoup(html_content, 'html.parser')

        # Store provided dates (may be None - let BRSRXBRLGenerator handle defaults)
        # The generator will extract dates from the report's financial_year field if not provided
        self.start_date = start_date
        self.end_date = end_date
        self.period_str = ""  # Will be set after XBRL generation

        # Tracking
        self._cell_id = 0
        self._tag_mapping: Dict[str, List[Dict[str, Any]]] = {}
        self._report_data: Optional[BRSRReportData] = None
        self._xbrl_content: Optional[str] = None
        self._tag_extractor: Optional[XBRLTagExtractor] = None

        # Section tracking
        self._current_section = "Unknown"

    @staticmethod
    def clean_text(text: Optional[str]) -> str:
        """Clean and normalize text."""
        if text is None:
            return ''
        return re.sub(r'\s+', ' ', str(text)).strip()

    @staticmethod
    def normalize_value_for_xml(value: str) -> str:
        """
        Normalize cell values for XBRL output.
        Convert only NIL to "0", keep NA as "NA" in XML.

        Args:
            value: The cell value to normalize

        Returns:
            Normalized value suitable for XBRL
        """
        if not value:
            return value

        value_stripped = value.strip()
        value_upper = value_stripped.upper()

        # Convert only NIL variants to 0
        if value_upper in ['NIL', 'NILL']:
            return "0"

        # Keep NA, N/A, etc. as they are
        return value_stripped

    def _assign_cell_id(self) -> str:
        """Get next cell ID and increment counter."""
        cell_id = str(self._cell_id)
        self._cell_id += 1
        return cell_id

    def _detect_section(self, text: str) -> Optional[str]:
        """Detect which BRSR section we're in."""
        text_lower = text.lower()
        if 'section a' in text_lower or 'general disclosure' in text_lower:
            return 'Section A'
        elif 'section b' in text_lower or 'management and process' in text_lower:
            return 'Section B'
        elif 'section c' in text_lower or 'principle wise' in text_lower:
            return 'Section C'
        return None

    def _is_label_cell(self, cell_text: str, col_idx: int, cell_tag: str) -> bool:
        """
        Detect if a cell is a label/description cell (should not be clickable).

        Label cells typically:
        - Are in the first column and contain descriptive text
        - Are header cells (<th>)
        - Contain question-like text or field descriptions
        - Start with numbered/lettered list patterns (1., 2., a., i., etc.)
        - Don't contain actual data values

        Args:
            cell_text: The cleaned text content of the cell
            col_idx: Column index (0-based)
            cell_tag: The HTML tag name ('td' or 'th')

        Returns:
            True if the cell is a label, False if it's a value cell
        """
        # Header cells are labels
        if cell_tag.lower() == 'th':
            return True

        text_lower = cell_text.lower()

        # CRITICAL: First column cells are ALWAYS labels in BRSR tables
        # Never highlight anything in column 0 - it's always row labels/headers
        # Examples: "Permanent (D)", "Other than Permanent (E)", "National", "Male", etc.
        if col_idx == 0:
            return True  # Always treat column 0 as label - no exceptions

        # Note: Column 0 is already handled above, so we don't need serial number check here
        # Small numbers (1-2 digits) in other columns are most likely actual data values
        # NOT serial numbers (e.g., "28 plants", "10 offices")

<<<<<<< HEAD
=======
        # BRSR formula/category labels with parenthetical notation
        # These appear in "Particulars" columns and are labels, not values
        # Examples: "Permanent (D)", "Other than Permanent (E)", "Total employees (D + E)"
        if re.search(r'\([A-Z](?:\s*[+\-]\s*[A-Z])*\)$', cell_text.strip()):
            # Ends with (D), (E), (F), (G), (D + E), (F + G), etc.
            return True

        # BRSR category labels - standalone category values used as row labels
        # Examples: "Employees", "Workers", "Male", "Female"
        # These appear in "Category" columns and should NOT be highlighted
        # Note: "National"/"State" are NOT included as they are legitimate data in some tables
        # (e.g., trade associations reach, locations)
        category_labels = [
            'employees', 'workers', 'male', 'female', 'others', 'total',
            'permanent', 'other than permanent'
        ]
        if text_lower.strip() in category_labels:
            return True

>>>>>>> 618ccb24b2abb09cd9e58ff42780611248823db2
        # Cells starting with numbered/lettered list patterns are labels
        # Matches: "1.", "2.", "23.", "a.", "b.", "i.", "ii.", "(a)", "(1)", etc.
        list_pattern = re.match(
            r'^(\d+\.|[a-z]\.|[ivxlc]+\.|\(\d+\)|\([a-z]\)|\([ivxlc]+\))\s*.+',
            text_lower
        )
        if list_pattern:
            # This starts with a list pattern followed by text - it's a label
            # But verify it's not just a short value like "1. Yes" or "a. 2024"
            remaining_text = re.sub(r'^(\d+\.|[a-z]\.|[ivxlc]+\.|\(\d+\)|\([a-z]\)|\([ivxlc]+\))\s*', '', text_lower)
            if not self._looks_like_value(remaining_text):
                return True

        # Common label/question indicators - if found, it's a label
        label_indicators = [
            'whether',
            'specify',
            'provide',
            'details of',
            'name of',
            'list of',
            'description',
            'please indicate',
            'if yes',
            'if no',
            'in case of',
            'for which reporting',
            'financial year for which',
            'reporting period',
            'corporate identity',
            'registered office',
            'contact number',
            'email address',
            'website of',
            'total number of',
            'number of',
            'percentage of',
            'turnover',
            'disclosure',
            '(in rs.)',
            '(in inr)',
            '(in %)',
            'sr. no',
            's. no',
            'sl. no',
            'particulars',
            'category',
            'type of',
            'holding of',
            'market capitalisation',
            'authorised capital',
            'paid up capital',
        ]

        # Check if it looks like a label based on content
        # Only apply label indicators check to first column (col_idx == 0)
        # Value cells in other columns may legitimately contain these phrases
        if col_idx == 0:
            for indicator in label_indicators:
                if indicator in text_lower:
                    # If the indicator is found, it's a label unless it's clearly a value
                    if not self._looks_like_value(cell_text):
                        return True
                    # Even if it has some value patterns, if it's long text in first column, it's a label
                    if len(cell_text) > 20:
                        return True

        # First column cells that are descriptive are likely labels
        if col_idx == 0 and len(cell_text) > 30:
            # Check if it looks like a value (has numbers, dates, yes/no)
            if not self._looks_like_value(cell_text):
                return True

        # Cells with question marks are labels
        if '?' in cell_text:
            return True

        # Serial number patterns - just the number/letter alone
        if col_idx == 0:
            # Roman numerals, letters, or numbers as list items (standalone)
            if re.match(r'^[ivxlc]+\.?\s*$', text_lower):  # Roman numerals only
                return True
            if re.match(r'^[a-z]\.?\s*$', text_lower):  # Single letter
                return True
            # Treat standalone numbers as labels EXCEPT for "0" which is a valid data value
            if re.match(r'^\d+\.?\s*$', text_lower) and len(cell_text) < 5:
                # "0" is a valid value, not a label
                if text_lower.strip() != '0':
                    return True

        return False

    def _looks_like_value(self, text: str) -> bool:
        """
        Check if text looks like an actual data value.

        Values typically contain:
        - Numbers (with or without commas, decimals)
        - Dates
        - Yes/No responses
        - Percentages
        - Currency amounts
        - Short specific text (company names, URLs, etc.)
        """
        text_lower = text.lower().strip()

        # Yes/No values
        if text_lower in ['yes', 'no', 'na', 'n/a', 'nil', 'not applicable']:
            return True

        # Contains numbers (likely a numeric value)
        if re.search(r'\d', text):
            return True

        # Date patterns
        if re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text):
            return True
        if re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)', text_lower):
            return True

        # URL pattern
        if re.search(r'(www\.|\.com|\.in|\.org|http)', text_lower):
            return True

        # Email pattern
        if '@' in text and '.' in text:
            return True

        # Short text (likely a specific value like company name)
        if len(text) < 30 and not any(ind in text_lower for ind in ['whether', 'specify', 'provide', 'details']):
            return True

        return False

    def parse_and_annotate(self) -> Tuple[str, Dict[str, List[Dict[str, Any]]], BRSRReportData, str]:
        """
        Parse HTML, generate XBRL, annotate cells, and create tag mappings.

        Returns:
            Tuple of (annotated_html, tag_mapping, report_data, xbrl_content)
        """
        # Step 1: Parse HTML to get report data
        parser = BRSRHTMLParser(self.html_content)
        self._report_data = parser.parse()

        # Step 2: Generate XBRL to get actual tags
        # Pass dates to generator (if None, generator will extract from report's financial_year)
        generator = BRSRXBRLGenerator(
            report_data=self._report_data,
            start_date_cy=self.start_date,
            end_date_cy=self.end_date,
        )
        self._xbrl_content = generator.generate()

        # Update dates and period_str from generator (which may have parsed from report)
        self.start_date = generator.start_date_cy
        self.end_date = generator.end_date_cy
        self.period_str = self.PERIOD_FORMAT.format(
            self.start_date.strftime('%Y-%m-%d'),
            self.end_date.strftime('%Y-%m-%d')
        )

        # Step 3: Extract tags from XBRL
        self._tag_extractor = XBRLTagExtractor(self._xbrl_content)

        # Step 4: Create fresh soup for annotation
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

        # Step 5: Add CSS styling
        self._add_styling()

        # Step 6: Annotate tables with actual XBRL tags
        self._annotate_all_tables()

        # Step 7: Annotate specific paragraphs with data values
        # Only annotates Q20.b and Q20.c in Section A (exports & customers)
        self._annotate_paragraphs()

        # Get annotated HTML
        annotated_html = str(self.soup)

        logger.info(f"Annotation complete: {self._cell_id} cells, {len(self._tag_mapping)} mappings")

        return annotated_html, self._tag_mapping, self._report_data, self._xbrl_content

    def _add_styling(self):
        """Add CSS styling for interactive cells."""
        head = self.soup.find('head')
        if not head:
            head = self.soup.new_tag('head')
            if self.soup.html:
                self.soup.html.insert(0, head)
            else:
                self.soup.insert(0, head)

        style = self.soup.new_tag('style')
        style.string = """
            .xml-linked {
                cursor: pointer;
                background-color: #e3f2fd !important;
                transition: background 0.15s;
            }
            .xml-linked:hover {
                background-color: #bbdefb !important;
                outline: 2px solid #1976d2;
            }
            .xml-linked.has-tag {
                background-color: #c8e6c9 !important;
            }
            .xml-linked.has-tag:hover {
                background-color: #a5d6a7 !important;
                outline: 2px solid #388e3c;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
            }
            td, th {
                border: 1px solid #ddd;
                padding: 8px;
                font-size: 12px;
            }
            th {
                background-color: #f5f5f5;
            }
        """
        head.append(style)

    def _annotate_all_tables(self):
        """Annotate ALL table cells with data-id and create mappings using actual XBRL tags."""
        tables = self.soup.find_all('table')

        for table_idx, table in enumerate(tables):
            # Get table headers for context
            headers = []
            header_row = table.find('tr')
            if header_row:
                for th in header_row.find_all(['th', 'td']):
                    headers.append(self.clean_text(th.get_text()))

            # Track current table context
            table_text = self.clean_text(table.get_text())[:200]
            section = self._detect_section(table_text)
            if section:
                self._current_section = section

            # Process all rows
            rows = table.find_all('tr')
            for row_idx, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])

                # Get row context from first cell
                row_context = ""
                if cells:
                    row_context = self.clean_text(cells[0].get_text())

                for col_idx, cell in enumerate(cells):
                    cell_text = self.clean_text(cell.get_text())
                    cell_tag = cell.name  # 'td' or 'th'

                    # CRITICAL: Only highlight <td> cells, NEVER <th> cells
                    if cell_tag.lower() != 'td':
                        continue

                    # Skip only truly empty cells or dash separators
                    # Keep NA, NIL, N/A, 0 values - they should be tagged
                    if not cell_text or cell_text == '-':
                        continue

                    # Skip label/description cells - only annotate value cells
                    if self._is_label_cell(cell_text, col_idx, cell_tag):
                        continue

                    # Get column context from header
                    col_context = headers[col_idx] if col_idx < len(headers) else ""

                    # Assign cell ID and add class
                    cell_id = self._assign_cell_id()
                    cell['data-id'] = cell_id

                    # Handle existing class attribute
                    existing_class = cell.get('class', [])
                    if isinstance(existing_class, str):
                        existing_class = existing_class.split()
                    if 'xml-linked' not in existing_class:
                        existing_class.append('xml-linked')

                    # Look up actual XBRL tags for this value with context for disambiguation
                    # First try with the normalized value (NIL → 0) since XBRL may have normalized it
                    normalized_search_value = self.normalize_value_for_xml(cell_text)
                    xbrl_tags = self._tag_extractor.get_tags_for_value(
                        normalized_search_value,
                        row_context=row_context,
                        col_context=col_context,
                    ) if self._tag_extractor else []

                    # If no match with normalized value, try original value
                    if not xbrl_tags and normalized_search_value != cell_text and self._tag_extractor:
                        xbrl_tags = self._tag_extractor.get_tags_for_value(
                            cell_text,
                            row_context=row_context,
                            col_context=col_context,
                        )

                    if xbrl_tags:
                        # Found matching XBRL tags - use them
                        if 'has-tag' not in existing_class:
                            existing_class.append('has-tag')

                        # Add all matching tags to mapping
                        # Normalize the value for XML (NIL -> 0, keep NA as is)
                        normalized_value = self.normalize_value_for_xml(cell_text)

                        self._tag_mapping[cell_id] = []
                        for tag_info in xbrl_tags:
                            self._tag_mapping[cell_id].append({
                                't': tag_info['t'],
                                'v': normalized_value,  # Use normalized value for XML
                                'c': tag_info['c'],
                                'p': self.period_str,
                                'u': tag_info.get('u'),
                                'd': [],
                                's': f"{self._current_section}, Table {table_idx + 1}, Row {row_idx + 1}",
                            })
                    else:
                        # No XBRL tag found - create placeholder
                        # Normalize the value for XML (NIL -> 0, keep NA as is)
                        normalized_value = self.normalize_value_for_xml(cell_text)

                        self._tag_mapping[cell_id] = [{
                            't': self._infer_fallback_tag(cell_text, row_context, col_context),
                            'v': normalized_value,  # Use normalized value for XML
                            'c': 'DCYMain',
                            'p': self.period_str,
                            'u': None,
                            'd': [],
                            's': f"{self._current_section}, Table {table_idx + 1}, Row {row_idx + 1} (no XBRL match)",
                        }]

                    cell['class'] = existing_class

    def _infer_fallback_tag(self, cell_text: str, row_context: str, col_context: str) -> str:
        """Infer a fallback tag when no XBRL match is found."""
        text_lower = cell_text.lower().strip()

        # Check if numeric
        is_numeric = bool(re.match(r'^[\d,.\-\s%₹$]+$', text_lower.replace(',', '')))

        if is_numeric:
            return 'in-capmkt:NumericValue (unmatched)'
        return 'in-capmkt:TextValue (unmatched)'

    def _annotate_paragraphs(self):
        """
        Annotate ONLY specific paragraphs that contain data values.

        Currently enabled for:
        - Section A, Q20.b (exports contribution)
        - Section A, Q20.c (types of customers)
        """
        for p in self.soup.find_all('p'):
            text = self.clean_text(p.get_text())
            if not text:
                continue

            text_lower = text.lower()

            # HIGHLY SELECTIVE: Only tag specific paragraphs
            # Check if this is Section A, Q20.b or Q20.c
            is_q20_b = (
                ('contribution of export' in text_lower or 'exports contribute' in text_lower) and
                'turnover' in text_lower and
                '%' in text
            )
            is_q20_c = (
                ('types of customer' in text_lower or 'brief on types of customer' in text_lower) and
                ('years of presence' in text_lower or 'households' in text_lower or 'retail outlet' in text_lower)
            )

            # Only proceed if it's one of the specific paragraphs
            if not (is_q20_b or is_q20_c):
                continue

            # Only annotate if the paragraph has an actual XBRL tag match
            has_xbrl_match = self._tag_extractor and self._tag_extractor.get_tags_for_value(text[:200])

            if has_xbrl_match:
                section = self._detect_section(text)
                if section:
                    self._current_section = section

                # Annotate the paragraph
                cell_id = self._assign_cell_id()
                p['data-id'] = cell_id
                existing_class = p.get('class', [])
                if isinstance(existing_class, str):
                    existing_class = existing_class.split()
                if 'xml-linked' not in existing_class:
                    existing_class.append('xml-linked')

                # Extract context from paragraph: question part can help disambiguate
                question_context = ''
                if '?' in text:
                    question_context = text.split('?', 1)[0]

                # Try to find XBRL tag for this text - multiple strategies
                xbrl_tags = []
                if self._tag_extractor:
                    # Strategy 1: Try full text with context
                    xbrl_tags = self._tag_extractor.get_tags_for_value(
                        text,
                        row_context=question_context,
                        col_context=self._current_section,
                    )

                    # Strategy 2: Try first 200 chars
                    if not xbrl_tags:
                        xbrl_tags = self._tag_extractor.get_tags_for_value(
                            text[:200],
                            row_context=question_context,
                            col_context=self._current_section,
                        )

                    # Strategy 3: Try to extract answer portion after question mark
                    if not xbrl_tags and '?' in text:
                        answer_part = text.split('?', 1)[-1].strip()
                        if answer_part:
                            xbrl_tags = self._tag_extractor.get_tags_for_value(
                                answer_part[:200],
                                row_context=question_context,
                                col_context=self._current_section,
                            )

                    # Strategy 4: Try sentences containing percentages or numbers
                    if not xbrl_tags:
                        # Look for sentences with numeric data
                        sentences = re.split(r'[.!?]', text)
                        for sentence in sentences:
                            if re.search(r'\d+\.?\d*\s*%|\d{1,3}(?:,\d{3})*(?:\.\d+)?', sentence):
                                xbrl_tags = self._tag_extractor.get_tags_for_value(
                                    sentence.strip(),
                                    row_context=question_context,
                                    col_context=self._current_section,
                                )
                                if xbrl_tags:
                                    break

                if xbrl_tags:
                    if 'has-tag' not in existing_class:
                        existing_class.append('has-tag')
                    self._tag_mapping[cell_id] = []
                    for tag_info in xbrl_tags:
                        self._tag_mapping[cell_id].append({
                            't': tag_info['t'],
                            'v': tag_info['v'],
                            'c': tag_info['c'],
                            'p': self.period_str,
                            'u': tag_info.get('u'),
                            'd': [],
                            's': self._current_section,
                        })
                else:
                    self._tag_mapping[cell_id] = [{
                        't': 'in-capmkt:DisclosureText (unmatched)',
                        'v': text[:100] + ('...' if len(text) > 100 else ''),
                        'c': 'DCYMain',
                        'p': self.period_str,
                        'u': None,
                        'd': [],
                        's': self._current_section,
                    }]

                p['class'] = existing_class


def convert_interactive(
    html_content: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> InteractiveConversionResponse:
    """
    Convert BRSR HTML to interactive format with tag mappings.

    Args:
        html_content: Raw HTML string
        start_date: Start date of reporting period
        end_date: End date of reporting period

    Returns:
        InteractiveConversionResponse with annotated HTML, mapping, and XBRL
    """
    try:
        parser = BRSRInteractiveParser(html_content, start_date, end_date)
        annotated_html, tag_mapping, report_data, xbrl_content = parser.parse_and_annotate()

        # Get statistics
        statistics = {
            'total_cells': parser._cell_id,
            'total_mappings': len(tag_mapping),
            'cells_with_xbrl_tags': sum(1 for tags in tag_mapping.values()
                                         if tags and not tags[0]['t'].endswith('(unmatched)')),
        }

        return InteractiveConversionResponse(
            success=True,
            message="Interactive conversion completed successfully",
            annotated_html=annotated_html,
            tag_mapping=tag_mapping,
            xbrl_content=xbrl_content,
            report_data=report_data,
            statistics=statistics,
        )

    except Exception as e:
        logger.error(f"Interactive conversion failed: {e}", exc_info=True)
        return InteractiveConversionResponse(
            success=False,
            message=f"Conversion failed: {str(e)}",
        )


def update_xbrl_tags(
    request: TagUpdateRequest,
) -> TagUpdateResponse:
    """
    Update XBRL content based on tag updates.

    Supports two types of updates:
    1. Value updates: Change the value inside a tag
    2. Tag name updates: Change the tag name itself (e.g., in-capmkt:WebsiteOfCompany -> in-capmkt:CorporateWebsite)

    Args:
        request: TagUpdateRequest with original XBRL and updates

    Returns:
        TagUpdateResponse with updated XBRL content
    """
    try:
        xbrl_content = request.original_xbrl
        changes_applied = 0

        for update in request.updates:
            old_value = update.get('old_value', '')
            new_value = update.get('new_value', '')
            tag_name = update.get('tag', '')
            new_tag = update.get('new_tag', '')  # New tag name if user wants to rename

            # Handle tag name change
            if new_tag and new_tag != tag_name:
                if tag_name and ':' in tag_name and ':' in new_tag:
                    # Extract old and new local names
                    old_prefix, old_local = tag_name.split(':', 1)
                    new_prefix, new_local = new_tag.split(':', 1)

                    # Remove (unmatched) suffix if present
                    old_local = old_local.replace(' (unmatched)', '')
                    new_local = new_local.replace(' (unmatched)', '')

                    # Find the tag and replace both opening and closing tags
                    # Pattern matches: <prefix:LocalName ...>value</prefix:LocalName>
                    # We need to preserve the value (whether it's old_value or different)
                    pattern = rf'(<{re.escape(old_prefix)}:{re.escape(old_local)})(\s[^>]*)?(>)([^<]*)(</){re.escape(old_prefix)}:{re.escape(old_local)}(>)'

                    def replace_tag_name(match):
                        opening_tag = f'<{new_prefix}:{new_local}'
                        attrs = match.group(2) or ''
                        gt = match.group(3)
                        value = match.group(4)
                        closing_slash = match.group(5)
                        closing_gt = match.group(6)
                        return f'{opening_tag}{attrs}{gt}{value}{closing_slash}{new_prefix}:{new_local}{closing_gt}'

                    new_content = re.sub(pattern, replace_tag_name, xbrl_content, count=1)
                    if new_content != xbrl_content:
                        xbrl_content = new_content
                        changes_applied += 1
                        # Update the tag_name for subsequent value change if needed
                        tag_name = new_tag

            # Handle value change
            if old_value and new_value and old_value != new_value:
                # Try to find and replace the value within the specific tag
                if tag_name and ':' in tag_name:
                    # Extract local name from tag (e.g., "in-capmkt:CompanyName" -> "CompanyName")
                    prefix, local_name = tag_name.split(':', 1)
                    # Remove (unmatched) suffix if present
                    local_name = local_name.replace(' (unmatched)', '')

                    # Create pattern to match the tag with the old value
                    # Match: <prefix:LocalName ...>old_value</prefix:LocalName>
                    pattern = rf'(<{re.escape(prefix)}:{re.escape(local_name)}[^>]*>){re.escape(old_value)}(</{re.escape(prefix)}:{re.escape(local_name)}>)'
                    replacement = rf'\g<1>{new_value}\g<2>'

                    new_content = re.sub(pattern, replacement, xbrl_content, count=1)
                    if new_content != xbrl_content:
                        xbrl_content = new_content
                        changes_applied += 1
                        continue

                # Fallback: Simple string replacement
                pattern = f'>{re.escape(old_value)}<'
                replacement = f'>{new_value}<'

                new_content = re.sub(pattern, replacement, xbrl_content, count=1)
                if new_content != xbrl_content:
                    xbrl_content = new_content
                    changes_applied += 1

        return TagUpdateResponse(
            success=True,
            message=f"Applied {changes_applied} changes",
            updated_xbrl=xbrl_content,
            changes_applied=changes_applied,
        )

    except Exception as e:
        logger.error(f"XBRL update failed: {e}", exc_info=True)
        return TagUpdateResponse(
            success=False,
            message=f"Update failed: {str(e)}",
        )
