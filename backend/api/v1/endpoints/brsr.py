"""
BRSR API Endpoints

Provides REST API for BRSR HTML to XBRL conversion.
"""

import logging
from typing import Optional
from datetime import date

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import Response

from schemas.brsr import (
    BRSRConversionRequest,
    BRSRConversionResponse,
    BRSRReportData,
    BRSRValidationResult,
)
from services.brsr import (
    BRSRService,
    get_brsr_service,
    BRSRXBRLValidator,
    BRSRXBRLComparator,
    validate_xbrl,
    compare_xbrl,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/brsr", tags=["BRSR"])


@router.post("/convert", response_model=BRSRConversionResponse)
async def convert_brsr_html(request: BRSRConversionRequest):
    """
    Convert BRSR HTML to XBRL XML.

    Accepts either HTML content directly or a file path.
    Returns XBRL XML along with parsed report data and statistics.
    """
    service = get_brsr_service()
    response = service.convert_from_request(request)

    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)

    return response


@router.post("/convert/file", response_model=BRSRConversionResponse)
async def convert_brsr_file(
    file: UploadFile = File(..., description="BRSR HTML file to convert"),
    start_date: Optional[date] = Form(None, description="Start date of reporting period (YYYY-MM-DD)"),
    end_date: Optional[date] = Form(None, description="End date of reporting period (YYYY-MM-DD)"),
    include_mapping: bool = Form(False, description="Include cell-to-tag mapping data"),
):
    """
    Convert uploaded BRSR HTML file to XBRL XML.

    Upload an HTML file and receive XBRL XML output.
    """
    if not file.filename or not file.filename.lower().endswith(('.html', '.htm')):
        raise HTTPException(
            status_code=400,
            detail="File must be an HTML file (.html or .htm)"
        )

    try:
        content = await file.read()
        html_content = content.decode('utf-8')
    except UnicodeDecodeError:
        # Try alternative encodings
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                html_content = content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise HTTPException(
                status_code=400,
                detail="Unable to decode file. Please ensure it's a valid HTML file with UTF-8 or common encoding."
            )

    service = get_brsr_service()
    response = service.convert(
        html_content=html_content,
        start_date=start_date,
        end_date=end_date,
        include_mapping=include_mapping,
    )

    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)

    return response


@router.post("/convert/file/xml")
async def convert_brsr_file_to_xml(
    file: UploadFile = File(..., description="BRSR HTML file to convert"),
    start_date: Optional[date] = Form(None, description="Start date of reporting period (YYYY-MM-DD)"),
    end_date: Optional[date] = Form(None, description="End date of reporting period (YYYY-MM-DD)"),
):
    """
    Convert uploaded BRSR HTML file and return raw XBRL XML.

    Returns the XBRL XML directly as a downloadable file.
    """
    if not file.filename or not file.filename.lower().endswith(('.html', '.htm')):
        raise HTTPException(
            status_code=400,
            detail="File must be an HTML file (.html or .htm)"
        )

    try:
        content = await file.read()
        html_content = content.decode('utf-8')
    except UnicodeDecodeError:
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                html_content = content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise HTTPException(
                status_code=400,
                detail="Unable to decode file."
            )

    service = get_brsr_service()
    response = service.convert(
        html_content=html_content,
        start_date=start_date,
        end_date=end_date,
    )

    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)

    # Generate filename from company name
    company_name = response.report_data.company.company_name if response.report_data else "brsr"
    safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in company_name).strip()
    safe_name = safe_name.replace(" ", "_")[:50] or "brsr_output"

    return Response(
        content=response.xbrl_content,
        media_type="application/xml",
        headers={
            "Content-Disposition": f'attachment; filename="{safe_name}.xml"'
        }
    )


@router.post("/validate", response_model=BRSRValidationResult)
async def validate_brsr_html(
    file: UploadFile = File(..., description="BRSR HTML file to validate"),
):
    """
    Validate BRSR HTML file structure.

    Checks if the file has the expected BRSR sections and structure.
    Returns validation results with any errors or warnings.
    """
    try:
        content = await file.read()
        html_content = content.decode('utf-8')
    except UnicodeDecodeError:
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                html_content = content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise HTTPException(
                status_code=400,
                detail="Unable to decode file."
            )

    service = get_brsr_service()
    return service.validate_html(html_content)


@router.post("/parse", response_model=BRSRReportData)
async def parse_brsr_html(
    file: UploadFile = File(..., description="BRSR HTML file to parse"),
):
    """
    Parse BRSR HTML file and return structured data.

    Returns all extracted data without generating XBRL XML.
    Useful for inspection and debugging.
    """
    try:
        content = await file.read()
        html_content = content.decode('utf-8')
    except UnicodeDecodeError:
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                html_content = content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise HTTPException(
                status_code=400,
                detail="Unable to decode file."
            )

    service = get_brsr_service()
    return service.parse_html(html_content)


@router.get("/taxonomy-info")
async def get_brsr_taxonomy_info():
    """
    Get information about the BRSR XBRL taxonomy.

    Returns namespace, schema reference, and supported elements.
    """
    return {
        "taxonomy_name": "SEBI BRSR Taxonomy",
        "namespace": "https://www.sebi.gov.in/xbrl/2025-05-31/in-capmkt",
        "namespace_prefix": "in-capmkt",
        "schema_ref": "in-capmkt-ent-2025-05-31.xsd",
        "supported_sections": [
            "Section A: General Disclosures (Q1-Q27)",
            "Section B: Management and Process Disclosures (P1-P9)",
            "Section C: Principle-wise Performance Disclosure",
        ],
        "supported_dimensions": [
            "EmployeesOrWorkersAxis",
            "DifferentlyAbledEmployeesOrWorkersAxis",
            "GenderAxis",
            "StakeholderGroupFromWhomComplaintIsReceivedAxis",
        ],
        "version": "2025-05-31",
        "regulator": "Securities and Exchange Board of India (SEBI)",
    }


# =============================================================================
# XBRL Validation and Comparison Endpoints
# =============================================================================

@router.post("/validate-xbrl")
async def validate_xbrl_file(
    file: UploadFile = File(..., description="XBRL XML file to validate"),
):
    """
    Validate generated XBRL XML against the BRSR taxonomy.

    Checks:
    - XML well-formedness
    - Required namespace declarations
    - Valid concept names
    - Context references
    - Dimensional validity
    - Required elements

    Returns detailed validation report with errors and warnings.
    """
    if not file.filename or not file.filename.lower().endswith('.xml'):
        raise HTTPException(
            status_code=400,
            detail="File must be an XML file (.xml)"
        )

    try:
        content = await file.read()
        xbrl_content = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Unable to decode file. Please ensure it's a valid UTF-8 XML file."
        )

    validator = BRSRXBRLValidator(xbrl_content)
    result = validator.validate()

    return {
        "is_valid": result.is_valid,
        "error_count": result.error_count,
        "warning_count": result.warning_count,
        "statistics": result.statistics,
        "issues": [
            {
                "severity": issue.severity.value,
                "code": issue.code,
                "message": issue.message,
                "element": issue.element,
                "suggestion": issue.suggestion,
            }
            for issue in result.issues
        ],
        "summary": validator.get_summary(),
    }


@router.post("/validate-xbrl/text")
async def validate_xbrl_file_text(
    file: UploadFile = File(..., description="XBRL XML file to validate"),
):
    """
    Validate XBRL and return human-readable text report.

    Returns a formatted text summary of validation results.
    """
    if not file.filename or not file.filename.lower().endswith('.xml'):
        raise HTTPException(
            status_code=400,
            detail="File must be an XML file (.xml)"
        )

    try:
        content = await file.read()
        xbrl_content = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Unable to decode file."
        )

    validator = BRSRXBRLValidator(xbrl_content)
    validator.validate()

    return Response(
        content=validator.get_summary(),
        media_type="text/plain",
    )


@router.post("/compare")
async def compare_xbrl_files(
    expected_file: UploadFile = File(..., description="Reference/expected XBRL file"),
    actual_file: UploadFile = File(..., description="Generated/actual XBRL file to compare"),
    ignore_whitespace: bool = Form(True, description="Ignore whitespace differences"),
    ignore_decimals: bool = Form(False, description="Ignore small numeric differences"),
    structure_only: bool = Form(False, description="Compare only tags/concepts used, ignore values"),
):
    """
    Compare two XBRL files to find differences.

    Use this to verify your generated XBRL against a known valid reference file.

    Returns:
    - Match status and percentage
    - List of differences (missing, extra, or mismatched facts)
    - Statistics on concepts used

    When structure_only=True:
    - Only compares which concepts/tags are used
    - Ignores actual values (useful for comparing files from different companies)
    - Returns matching, missing, and extra concepts
    """
    for f, name in [(expected_file, "expected"), (actual_file, "actual")]:
        if not f.filename or not f.filename.lower().endswith('.xml'):
            raise HTTPException(
                status_code=400,
                detail=f"{name.title()} file must be an XML file (.xml)"
            )

    try:
        expected_content = (await expected_file.read()).decode('utf-8')
        actual_content = (await actual_file.read()).decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Unable to decode files. Please ensure they are valid UTF-8 XML files."
        )

    comparator = BRSRXBRLComparator(
        expected_content,
        actual_content,
        ignore_whitespace=ignore_whitespace,
        ignore_decimals=ignore_decimals,
        structure_only=structure_only,
    )
    result = comparator.compare()

    response = {
        "is_match": result.is_match,
        "match_percentage": round(result.match_percentage, 2),
        "total_facts_expected": result.total_facts_expected,
        "total_facts_actual": result.total_facts_actual,
        "matching_facts": result.matching_facts,
        "statistics": result.statistics,
        "differences": [
            {
                "concept": diff.concept,
                "context": diff.context,
                "type": diff.difference_type,
                "expected_value": diff.expected_value,
                "actual_value": diff.actual_value,
                "message": diff.message,
            }
            for diff in result.differences[:100]  # Limit to 100 differences
        ],
        "total_differences": len(result.differences),
        "structure_only": structure_only,
    }

    # Add structure-only specific fields
    if structure_only:
        response.update({
            "total_concepts_expected": result.total_concepts_expected,
            "total_concepts_actual": result.total_concepts_actual,
            "matching_concepts": result.matching_concepts,
            "missing_concepts": result.missing_concepts,
            "extra_concepts": result.extra_concepts,
            "common_concepts": result.common_concepts,
        })

    return response


@router.post("/compare/text")
async def compare_xbrl_files_text(
    expected_file: UploadFile = File(..., description="Reference/expected XBRL file"),
    actual_file: UploadFile = File(..., description="Generated/actual XBRL file"),
):
    """
    Compare XBRL files and return human-readable text report.
    """
    try:
        expected_content = (await expected_file.read()).decode('utf-8')
        actual_content = (await actual_file.read()).decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Unable to decode files."
        )

    comparator = BRSRXBRLComparator(expected_content, actual_content)
    comparator.compare()

    return Response(
        content=comparator.get_summary(),
        media_type="text/plain",
    )


# =============================================================================
# Interactive Viewer Endpoints
# =============================================================================

@router.post("/convert/interactive")
async def convert_brsr_interactive(
    file: UploadFile = File(..., description="BRSR HTML file to convert"),
    start_date: Optional[date] = Form(None, description="Start date of reporting period (YYYY-MM-DD)"),
    end_date: Optional[date] = Form(None, description="End date of reporting period (YYYY-MM-DD)"),
):
    """
    Convert BRSR HTML to interactive format with tag mappings.

    Returns:
    - annotated_html: HTML with data-id attributes on tagged cells
    - tag_mapping: Dictionary mapping cell IDs to XBRL tag information
    - xbrl_content: Generated XBRL XML
    - statistics: Conversion statistics

    This endpoint is designed for the interactive viewer which allows users
    to click on cells and see associated XBRL tags.
    """
    from services.brsr import convert_interactive

    if not file.filename or not file.filename.lower().endswith(('.html', '.htm')):
        raise HTTPException(
            status_code=400,
            detail="File must be an HTML file (.html or .htm)"
        )

    try:
        content = await file.read()
        html_content = content.decode('utf-8')
    except UnicodeDecodeError:
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                html_content = content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise HTTPException(
                status_code=400,
                detail="Unable to decode file. Please ensure it's a valid HTML file."
            )

    response = convert_interactive(
        html_content=html_content,
        start_date=start_date,
        end_date=end_date,
    )

    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)

    return {
        "success": response.success,
        "message": response.message,
        "annotated_html": response.annotated_html,
        "tag_mapping": response.tag_mapping,
        "xbrl_content": response.xbrl_content,
        "statistics": response.statistics,
    }


@router.post("/update-tags")
async def update_brsr_tags(
    original_xbrl: str = Form(..., description="Original XBRL content"),
    updates: str = Form(..., description="JSON array of updates: [{cell_id, tag, old_value, new_value}]"),
):
    """
    Update XBRL content based on tag/value changes.

    Accepts the original XBRL content and a list of updates to apply.
    Returns the updated XBRL content.

    Updates format:
    [
        {
            "cell_id": "123",
            "tag": "in-capmkt:CompanyName",
            "old_value": "Old Company Name",
            "new_value": "New Company Name"
        }
    ]
    """
    import json
    from services.brsr import update_xbrl_tags
    from schemas.brsr import TagUpdateRequest

    try:
        updates_list = json.loads(updates)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON format for updates"
        )

    request = TagUpdateRequest(
        original_xbrl=original_xbrl,
        updates=updates_list,
    )

    response = update_xbrl_tags(request)

    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)

    return {
        "success": response.success,
        "message": response.message,
        "updated_xbrl": response.updated_xbrl,
        "changes_applied": response.changes_applied,
    }


@router.post("/update-tags/download")
async def download_updated_xbrl(
    original_xbrl: str = Form(..., description="Original XBRL content"),
    updates: str = Form(..., description="JSON array of updates"),
    filename: str = Form("brsr_updated.xml", description="Output filename"),
):
    """
    Update XBRL and return as downloadable file.

    Same as /update-tags but returns the XML directly as a download.
    """
    import json
    from services.brsr import update_xbrl_tags
    from schemas.brsr import TagUpdateRequest

    try:
        updates_list = json.loads(updates)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON format for updates"
        )

    request = TagUpdateRequest(
        original_xbrl=original_xbrl,
        updates=updates_list,
    )

    response = update_xbrl_tags(request)

    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)

    # Sanitize filename
    safe_filename = "".join(c if c.isalnum() or c in " -_." else "" for c in filename).strip()
    if not safe_filename.endswith('.xml'):
        safe_filename += '.xml'

    return Response(
        content=response.updated_xbrl,
        media_type="application/xml",
        headers={
            "Content-Disposition": f'attachment; filename="{safe_filename}"'
        }
    )
