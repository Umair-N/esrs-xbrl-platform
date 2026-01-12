"""
BRSR XBRL Template

Complete Jinja2 template for generating SEBI-compliant XBRL from BRSR data.
Ported from the Jupyter notebook brsr_html_to_xml_v2_complete.ipynb
"""

XBRL_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xbrli:xbrl xmlns:xbrli="http://www.xbrl.org/2003/instance" 
            xmlns:in-capmkt="https://www.sebi.gov.in/xbrl/2025-05-31/in-capmkt" 
            xmlns:iso4217="http://www.xbrl.org/2003/iso4217" 
            xmlns:xbrldi="http://xbrl.org/2006/xbrldi" 
            xmlns:link="http://www.xbrl.org/2003/linkbase" 
            xmlns:xlink="http://www.w3.org/1999/xlink">
    
    <link:schemaRef xlink:href="in-capmkt-ent-2025-05-31.xsd" xlink:type="simple"/>

    <!-- ==================== CONTEXTS ==================== -->
    
    <xbrli:context id="DCYMain">
        <xbrli:entity>
            <xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:startDate>{{ start_date_cy }}</xbrli:startDate>
            <xbrli:endDate>{{ end_date_cy }}</xbrli:endDate>
        </xbrli:period>
    </xbrli:context>

    <xbrli:context id="ICYMain">
        <xbrli:entity>
            <xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{{ end_date_cy }}</xbrli:instant>
        </xbrli:period>
    </xbrli:context>

    <!-- ==================== SIMPLE GENDER CONTEXTS (for Parental Leave) ==================== -->
    <xbrli:context id="D_Male">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gender">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
    </xbrli:context>

    <!-- ==================== EMPLOYEE/WORKER CONTEXTS - TABLE A ==================== -->
    <!-- Permanent Employees -->
    <xbrli:context id="D_Gender_PermanentEmployees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_PermanentEmployees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentEmployees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentEmployees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Other Than Permanent Employees -->
    <xbrli:context id="D_Gender_OtherThanPermanentEmployees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_OtherThanPermanentEmployees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_OtherThanPermanentEmployees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_OtherThanPermanentEmployees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Total Employees -->
    <xbrli:context id="D_Gender_Employees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_Employees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_Employees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_Employees_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Permanent Workers -->
    <xbrli:context id="D_Gender_PermanentWorkers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_PermanentWorkers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentWorkers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentWorkers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Other Than Permanent Workers -->
    <xbrli:context id="D_Gender_OtherThanPermanentWorkers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_OtherThanPermanentWorkers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_OtherThanPermanentWorkers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_OtherThanPermanentWorkers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Total Workers -->
    <xbrli:context id="D_Gender_Workers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_Workers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_Workers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_Workers_TableA">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- ==================== DIFFERENTLY ABLED CONTEXTS - TABLE B ==================== -->
    <!-- Permanent Employees - Differently Abled -->
    <xbrli:context id="D_Gender_PermanentEmployees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_PermanentEmployees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentEmployees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentEmployees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Other Than Permanent Employees - Differently Abled -->
    <xbrli:context id="D_Gender_OtherThanPermanentEmployees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_OtherThanPermanentEmployees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_OtherThanPermanentEmployees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_OtherThanPermanentEmployees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Total Employees - Differently Abled -->
    <xbrli:context id="D_Gender_Employees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_Employees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_Employees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_Employees_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Permanent Workers - Differently Abled -->
    <xbrli:context id="D_Gender_PermanentWorkers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_PermanentWorkers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentWorkers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentWorkers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Other Than Permanent Workers - Differently Abled -->
    <xbrli:context id="D_Gender_OtherThanPermanentWorkers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_OtherThanPermanentWorkers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_OtherThanPermanentWorkers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_OtherThanPermanentWorkers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Total Workers - Differently Abled -->
    <xbrli:context id="D_Gender_Workers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_Workers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_Workers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_Workers_TableB">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:DifferentlyAbledEmployeesOrWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- ==================== TURNOVER RATE CONTEXTS ==================== -->
    <!-- Permanent Employees Turnover - CY -->
    <xbrli:context id="D_Male_PermanentEmployees_TableB_TurnOverRate_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentEmployees_TableB_TurnOverRate_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentEmployees_TableB_TurnOverRate_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gender_PermanentEmployees_TableB_TurnOverRate_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Permanent Employees Turnover - PY -->
    <xbrli:context id="D_Male_PermanentEmployees_TableB_TurnOverRate_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentEmployees_TableB_TurnOverRate_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentEmployees_TableB_TurnOverRate_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gender_PermanentEmployees_TableB_TurnOverRate_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Permanent Employees Turnover - PPY -->
    <xbrli:context id="D_Male_PermanentEmployees_TableB_TurnOverRate_PPY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_ppy }}</xbrli:startDate><xbrli:endDate>{{ end_date_ppy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentEmployees_TableB_TurnOverRate_PPY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_ppy }}</xbrli:startDate><xbrli:endDate>{{ end_date_ppy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentEmployees_TableB_TurnOverRate_PPY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_ppy }}</xbrli:startDate><xbrli:endDate>{{ end_date_ppy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gender_PermanentEmployees_TableB_TurnOverRate_PPY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_ppy }}</xbrli:startDate><xbrli:endDate>{{ end_date_ppy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Permanent Workers Turnover - CY -->
    <xbrli:context id="D_Male_PermanentWorkers_TableB_TurnOverRate_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentWorkers_TableB_TurnOverRate_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentWorkers_TableB_TurnOverRate_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gender_PermanentWorkers_TableB_TurnOverRate_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Permanent Workers Turnover - PY -->
    <xbrli:context id="D_Male_PermanentWorkers_TableB_TurnOverRate_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentWorkers_TableB_TurnOverRate_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentWorkers_TableB_TurnOverRate_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gender_PermanentWorkers_TableB_TurnOverRate_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Permanent Workers Turnover - PPY -->
    <xbrli:context id="D_Male_PermanentWorkers_TableB_TurnOverRate_PPY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_ppy }}</xbrli:startDate><xbrli:endDate>{{ end_date_ppy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentWorkers_TableB_TurnOverRate_PPY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_ppy }}</xbrli:startDate><xbrli:endDate>{{ end_date_ppy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentWorkers_TableB_TurnOverRate_PPY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_ppy }}</xbrli:startDate><xbrli:endDate>{{ end_date_ppy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gender_PermanentWorkers_TableB_TurnOverRate_PPY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_ppy }}</xbrli:startDate><xbrli:endDate>{{ end_date_ppy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TurnoverRateForEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Other dynamic contexts -->
    {% for ex in stock_exchanges %}
    <xbrli:context id="D_StockExchangeAxis{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:StockExchangeAxis"><in-capmkt:StockExchangeDomain>StockExchange{{ loop.index }}</in-capmkt:StockExchangeDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

    {% if assurance.has_assurance == "Yes" %}
    {% for assessor in assurance.assessors %}
    <xbrli:context id="D_AssessmentOrAssuranceProvider{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:AssessmentOrAssuranceProviderAxis"><in-capmkt:AssessmentOrAssuranceProviderDomain>AssessmentOrAssuranceProvider{{ loop.index }}</in-capmkt:AssessmentOrAssuranceProviderDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}
    {% endif %}

    {% for act in business_activities %}
    <xbrli:context id="D_BusinessActivities{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:DetailsOfBusinessActivitiesAccountingForNinetyPercentOfTheTurnoverAxis"><in-capmkt:DetailsOfBusinessActivitiesAccountingForNinetyPercentOfTheTurnoverDomain>BusinessActivity{{ loop.index }}</in-capmkt:DetailsOfBusinessActivitiesAccountingForNinetyPercentOfTheTurnoverDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

    {% for prod in products_services %}
    <xbrli:context id="D_ProductServiceSold{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:ProductsOrServicesSoldByTheEntityAccountingForNinetyPercentOfTheTurnoverAxis"><in-capmkt:ProductsOrServicesSoldByTheEntityAccountingForNinetyPercentOfTheTurnoverDomain>Product{{ loop.index }}</in-capmkt:ProductsOrServicesSoldByTheEntityAccountingForNinetyPercentOfTheTurnoverDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

    <!-- Location Contexts (Q19) -->
    <xbrli:context id="D_Plant_National">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:LocationAxis">in-capmkt:PlantsMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GeographicalAxis">in-capmkt:NationalMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Office_National">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:LocationAxis">in-capmkt:OfficesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GeographicalAxis">in-capmkt:NationalMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Location_National">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:LocationAxis">in-capmkt:TotalMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GeographicalAxis">in-capmkt:NationalMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Plant_International">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:LocationAxis">in-capmkt:PlantsMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GeographicalAxis">in-capmkt:InternationalMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Office_International">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:LocationAxis">in-capmkt:OfficesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GeographicalAxis">in-capmkt:InternationalMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Location_International">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:LocationAxis">in-capmkt:TotalMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GeographicalAxis">in-capmkt:InternationalMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    {% for sub in subsidiaries %}
    <xbrli:context id="D_HoldingSubsidiaryAssociateCompaniesAndJointVentures{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:HoldingSubsidiaryAssociateCompaniesAndJointVenturesAxis"><in-capmkt:HoldingSubsidiaryAssociateCompaniesAndJointVenturesDomain>Subsidiary{{ loop.index }}</in-capmkt:HoldingSubsidiaryAssociateCompaniesAndJointVenturesDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

    {% for issue in material_issues %}
    <xbrli:context id="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:EntitysMaterialResponsibleBusinessConductIssuesAxis"><in-capmkt:EntitysMaterialResponsibleBusinessConductIssuesDomain>MaterialIssue{{ loop.index }}</in-capmkt:EntitysMaterialResponsibleBusinessConductIssuesDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}



    <!-- SECTION B: MANAGEMENT AND PROCESS DISCLOSURES - Principle Contexts -->
    {% for p in section_b %}
    <xbrli:context id="D_Principle{{ p.num }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:NGRBCPrinciplesAxis">in-capmkt:Principle{{ p.num }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

    
    <!-- Training Program Segment Contexts -->
    <xbrli:context id="D_BoardOfDirectorsSegment">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TrainingProgramsSegmentAxis">in-capmkt:BoardOfDirectorsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_KeyManagerialPersonnelSegment">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TrainingProgramsSegmentAxis">in-capmkt:KeyManagerialPersonnelMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EmployeesOtherThanBoDAndKMPsSegment">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TrainingProgramsSegmentAxis">in-capmkt:EmployeesOtherThanBoDAndKMPsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_WorkersSegment">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TrainingProgramsSegmentAxis">in-capmkt:WorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    
    
    <!-- SUSTAINABILITY CONTEXTS -->
    <xbrli:context id="D_AwarenessProgrammesConductedForValueChainPartners1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:AwarenessProgrammesForValueChainPartnersAxis">in-capmkt:AwarenessProgrammesConductedForValueChainPartners1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_ProductOrService1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ProductOrServiceAxis">in-capmkt:ProductOrService1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:RecycledOrReusedInputMaterialAxis">in-capmkt:RecycledOrReusedInputMaterial1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices_PY1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ py_start }}</xbrli:startDate><xbrli:endDate>{{ py_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:RecycledOrReusedInputMaterialAxis">in-capmkt:RecycledOrReusedInputMaterial1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_PlasticsIncludingPackaging">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:WasteTypeAxis">in-capmkt:PlasticsIncludingPackagingMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_PlasticsIncludingPackaging_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ py_start }}</xbrli:startDate><xbrli:endDate>{{ py_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:WasteTypeAxis">in-capmkt:PlasticsIncludingPackagingMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EWaste">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:WasteTypeAxis">in-capmkt:EWasteMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EWaste_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ py_start }}</xbrli:startDate><xbrli:endDate>{{ py_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:WasteTypeAxis">in-capmkt:EWasteMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_HazardousWaste">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:WasteTypeAxis">in-capmkt:HazardousWasteMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_HazardousWaste_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ py_start }}</xbrli:startDate><xbrli:endDate>{{ py_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:WasteTypeAxis">in-capmkt:HazardousWasteMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherWaste1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:OtherWasteAxis">in-capmkt:OtherWaste1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherWaste_PY1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ py_start }}</xbrli:startDate><xbrli:endDate>{{ py_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:OtherWasteAxis">in-capmkt:OtherWaste1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- RECLAIMED PRODUCTS CONTEXTS -->
    {% for product in sustainability.reclaimed_products %}
    <xbrli:context id="D_ReclaimedProductsAndTheirPackaging{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ReclaimedProductsAndTheirPackagingAxis">in-capmkt:ReclaimedProductsAndTheirPackaging{{ loop.index }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

    <!-- FINES/PENALTIES CONTEXTS -->
    <xbrli:context id="D_PenaltyOrFine1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:PenaltyOrFineAxis">in-capmkt:PenaltyOrFine1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Settlement1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:SettlementAxis">in-capmkt:Settlement1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Compounding1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CompoundingFeeAxis">in-capmkt:Compounding1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Imprisonment1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ImprisonmentAxis">in-capmkt:Imprisonment1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Punishment1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:PunishmentAxis">in-capmkt:Punishment1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_AppealOrRevision1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:AppealOrRevisionAxis">in-capmkt:AppealOrRevision1Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- COMPLAINTS/GRIEVANCES CONTEXTS -->
    {% for complaint in complaints %}
    <!-- {{ complaint.stakeholder }} - CY Duration -->
    <xbrli:context id="D_ComplaintReceivedFrom{{ complaint.stakeholder }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis">in-capmkt:{{ complaint.stakeholder }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <!-- {{ complaint.stakeholder }} - CY Instant -->
    <xbrli:context id="I_ComplaintReceivedFrom{{ complaint.stakeholder }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis">in-capmkt:{{ complaint.stakeholder }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <!-- {{ complaint.stakeholder }} - PY Duration -->
    <xbrli:context id="D_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis">in-capmkt:{{ complaint.stakeholder }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <!-- {{ complaint.stakeholder }} - PY Instant -->
    <xbrli:context id="I_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis">in-capmkt:{{ complaint.stakeholder }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}


    <!-- PRINCIPLE 3 - Employee/Worker Well-being Contexts -->
    <!-- Employee Well-being Contexts - Table 1A -->
    {% for emp_type in ['PermanentEmployees', 'OtherThanPermanentEmployees'] %}
    {% for gender in ['Male', 'Female', 'Others', 'Total'] %}
    {% for benefit in ['HealthInsurance', 'AccidentInsurance', 'MaternityBenefits', 'PaternityBenefits', 'DayCareFacilities'] %}
    <xbrli:context id="D_{{ gender }}_{{ benefit }}_{{ emp_type }}_Table1A">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfBenefitsProvidedToEmployeesAndWorkersAxis">in-capmkt:{{ benefit }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfEmployeeAndWorkerAxis">in-capmkt:{{ emp_type }}Member</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    {% endfor %}
    {% endfor %}
    {% endfor %}

    <!-- Worker Well-being Contexts - Table 1B -->
    {% for worker_type in ['PermanentWorkers', 'OtherThanPermanentWorkers'] %}
    {% for gender in ['Male', 'Female', 'Others', 'Total'] %}
    {% for benefit in ['HealthInsurance', 'AccidentInsurance', 'MaternityBenefits', 'PaternityBenefits', 'DayCareFacilities'] %}
    <xbrli:context id="D_{{ gender }}_{{ benefit }}_{{ worker_type }}_Table1B">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfBenefitsProvidedToEmployeesAndWorkersAxis">in-capmkt:{{ benefit }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfEmployeeAndWorkerAxis">in-capmkt:{{ worker_type }}Member</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    {% endfor %}
    {% endfor %}
    {% endfor %}

    <!-- Total Employees/Workers Context -->
    {% for emp_type in ['PermanentEmployees', 'OtherThanPermanentEmployees'] %}
    {% for gender in ['Male', 'Female', 'Others', 'Total'] %}
    <xbrli:context id="D_{{ gender }}_Total_{{ emp_type }}_Table1A">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfEmployeeAndWorkerAxis">in-capmkt:{{ emp_type }}Member</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    {% endfor %}
    {% endfor %}

    {% for worker_type in ['PermanentWorkers', 'OtherThanPermanentWorkers'] %}
    {% for gender in ['Male', 'Female', 'Others', 'Total'] %}
    <xbrli:context id="D_{{ gender }}_Total_{{ worker_type }}_Table1B">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfEmployeeAndWorkerAxis">in-capmkt:{{ worker_type }}Member</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    {% endfor %}
    {% endfor %}

    <!-- Retirement Benefits Contexts (PF, Gratuity, ESI) -->
    <xbrli:context id="D_ProvidentFund">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfRetirementBenefitAxis">in-capmkt:PFMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_ProvidentFund_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfRetirementBenefitAxis">in-capmkt:PFMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gratuity">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfRetirementBenefitAxis">in-capmkt:GratuityMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gratuity_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfRetirementBenefitAxis">in-capmkt:GratuityMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_ESI">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfRetirementBenefitAxis">in-capmkt:ESIMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_ESI_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfRetirementBenefitAxis">in-capmkt:ESIMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherRetirementBenefits1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfRetirementBenefitAxis">in-capmkt:OthersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherRetirementBenefits_PY1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfRetirementBenefitAxis">in-capmkt:OthersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Energy Consumption Through Other Sources Contexts (Principle 6) -->
    <xbrli:context id="D_EnergyConsumptionThroughOtherSourceFromRenewableSources1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:EnergyConsumptionThroughOtherSourceFromRenewableSourcesAxis"><in-capmkt:EnergyConsumptionThroughOtherSourceFromRenewableSourcesDomain>OtherRenewable1</in-capmkt:EnergyConsumptionThroughOtherSourceFromRenewableSourcesDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EnergyConsumptionThroughOtherSourceFromRenewableSources_PY1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:EnergyConsumptionThroughOtherSourceFromRenewableSourcesAxis"><in-capmkt:EnergyConsumptionThroughOtherSourceFromRenewableSourcesDomain>OtherRenewable1</in-capmkt:EnergyConsumptionThroughOtherSourceFromRenewableSourcesDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EnergyConsumptionThroughOtherSourceFromNonRenewableSources1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:EnergyConsumptionThroughOtherSourceFromNonRenewableSourcesAxis"><in-capmkt:EnergyConsumptionThroughOtherSourceFromNonRenewableSourcesDomain>OtherNonRenewable1</in-capmkt:EnergyConsumptionThroughOtherSourceFromNonRenewableSourcesDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EnergyConsumptionThroughOtherSourceFromNonRenewableSources_PY1">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:typedMember dimension="in-capmkt:EnergyConsumptionThroughOtherSourceFromNonRenewableSourcesAxis"><in-capmkt:EnergyConsumptionThroughOtherSourceFromNonRenewableSourcesDomain>OtherNonRenewable1</in-capmkt:EnergyConsumptionThroughOtherSourceFromNonRenewableSourcesDomain></xbrldi:typedMember></xbrli:scenario>
    </xbrli:context>

    <!-- Parental Leave Contexts -->
    {% for gender in ['Male', 'Female', 'Others', 'Total'] %}
    {% for emp_type in ['PermanentEmployees', 'PermanentWorkers'] %}
    <xbrli:context id="D_ParentalLeave_{{ gender }}_{{ emp_type }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfEmployeeAndWorkerAxis">in-capmkt:{{ emp_type }}Member</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    {% endfor %}
    {% endfor %}

    <!-- Well-being Spending Context -->
    <xbrli:context id="D_WellbeingSpending_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
    </xbrli:context>
    <xbrli:context id="D_WellbeingSpending_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
    </xbrli:context>

    <!-- Accessibility Context -->
    <xbrli:context id="D_Accessibility">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
    </xbrli:context>


    
    <!-- Extended PRINCIPLE 3 Contexts -->
    <!-- Safety Incidents Contexts -->
    <xbrli:context id="D_Employees">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Employees_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Workers">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Workers_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Complaints Contexts -->
    <xbrli:context id="D_WorkingConditionsComplaints">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfComplaintAxis">in-capmkt:WorkingConditionsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_WorkingConditionsComplaints">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfComplaintAxis">in-capmkt:WorkingConditionsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_WorkingConditionsComplaints_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfComplaintAxis">in-capmkt:WorkingConditionsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_WorkingConditionsComplaints_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfComplaintAxis">in-capmkt:WorkingConditionsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_HealthSafetyComplaints">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfComplaintAxis">in-capmkt:HealthAndSafetyMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_HealthSafetyComplaints">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfComplaintAxis">in-capmkt:HealthAndSafetyMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_HealthSafetyComplaints_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfComplaintAxis">in-capmkt:HealthAndSafetyMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_HealthSafetyComplaints_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfComplaintAxis">in-capmkt:HealthAndSafetyMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PRINCIPLE 5: Complaint Category Contexts -->
    <!-- CY Contexts for 6 complaint categories -->
    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_1">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_1">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_1">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_2">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_2">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_2">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_3">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_3">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_3">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_4">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_4">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_4">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_6">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_6">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_6">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PY Contexts for 6 complaint categories -->
    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_1_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_1_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_1_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_2_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_2_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_2_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_3_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_3_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_3_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_4_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_4_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_4_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_6_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_6_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_6_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PRINCIPLE 5: Human Rights Contexts -->
    <!-- HR Training Contexts -->
    <xbrli:context id="D_PermanentEmployees_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherThanPermanentEmployees_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Employees_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:TotalEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_PermanentWorkers_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherThanPermanentWorkers_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Workers_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:TotalWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PY HR Training Contexts -->
    <xbrli:context id="D_PermanentEmployees_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherThanPermanentEmployees_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Employees_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:TotalEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_PermanentWorkers_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherThanPermanentWorkers_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Workers_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:TotalWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Median Remuneration Gender Contexts -->
    <xbrli:context id="D_Male_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PRINCIPLE 5: Other Assessments Contexts -->
    <xbrli:context id="D_OtherAssessments12">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfAssessmentsOfPlantsAndOfficesAxis">in-capmkt:OtherAssessmentsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherAssessmentOfValueChainPartners12">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:TypeOfAssessmentsOfValueChainPartnersAxis">in-capmkt:OtherAssessmentOfValueChainPartnerMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- ==================== PRINCIPLE 5: Minimum Wages Contexts ==================== -->
    <!-- CY Permanent Employees (Male=1, Female=2, Others=3, Total=4) -->
    <xbrli:context id="D_Total_1">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_2">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_3">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_4">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_1">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_2">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_3">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_4">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_1">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_2">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_3">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_4">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PY Permanent Employees -->
    <xbrli:context id="D_Total_1_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_2_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_3_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_4_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_1_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_2_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_3_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_4_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_1_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_2_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_3_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_4_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- CY Other Than Permanent Employees (_Other suffix) -->
    <xbrli:context id="D_Total_1_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_2_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_3_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_4_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_1_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_2_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_3_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_4_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_1_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_2_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_3_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_4_Other">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PY Other Than Permanent Employees (_Other_PY suffix) -->
    <xbrli:context id="D_Total_1_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_2_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_3_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_4_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_1_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_2_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_3_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_4_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_1_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_2_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_3_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_4_Other_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- CY Permanent Workers (_W suffix) -->
    <xbrli:context id="D_Total_1_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_2_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_3_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_4_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_1_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_2_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_3_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_4_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_1_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_2_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_3_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_4_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PY Permanent Workers (_W_PY suffix) -->
    <xbrli:context id="D_Total_1_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_2_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_3_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_4_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_1_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_2_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_3_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_4_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_1_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_2_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_3_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_4_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- CY Other Than Permanent Workers (_Other_W suffix) -->
    <xbrli:context id="D_Total_1_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_2_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_3_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_4_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_1_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_2_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_3_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_4_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_1_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_2_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_3_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_4_Other_W">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PY Other Than Permanent Workers (_Other_W_PY suffix) -->
    <xbrli:context id="D_Total_1_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_2_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_3_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Total_4_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:TotalMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_1_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_2_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_3_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_EqualToMinimumWage_4_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:EqualToMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_1_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_2_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_3_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_MoreThanMinimumWage_4_Other_W_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:MinimumWageTypeAxis">in-capmkt:MoreThanMinimumWageMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PRINCIPLE 5: Complaint Category Contexts -->
    <!-- CY Contexts for 6 complaint categories -->
    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_1">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_1">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_1">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_2">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_2">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_2">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_3">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_3">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_3">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_4">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_4">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_4">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_6">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_6">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_6">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PY Contexts for 6 complaint categories -->
    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_1_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_1_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_1_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:SexualHarassmentMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_2_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_2_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_2_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:DiscriminationAtWorkPlaceMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_3_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_3_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_3_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ChildLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_4_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_4_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_4_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:ForcedLabourMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:WagesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <xbrli:context id="D_NumberOfComplaintsFiledDuringTheYear_6_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_6_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_RemarksforComplaintsExplanatoryTextBlock_6_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ComplaintCategoryAxis">in-capmkt:OtherHumanRightsMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PRINCIPLE 5: Human Rights Contexts -->
    <!-- HR Training Contexts -->
    <xbrli:context id="D_PermanentEmployees_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherThanPermanentEmployees_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Employees_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:TotalEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_PermanentWorkers_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherThanPermanentWorkers_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Workers_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:TotalWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PY HR Training Contexts -->
    <xbrli:context id="D_PermanentEmployees_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherThanPermanentEmployees_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Employees_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:TotalEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_PermanentWorkers_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherThanPermanentWorkers_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:OtherThanPermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Workers_p5_PY">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesOrWorkersAxis">in-capmkt:TotalWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Median Remuneration Gender Contexts -->
    <xbrli:context id="D_Male_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_p5">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- PRINCIPLE 4: Stakeholder Group Contexts -->
    {% for stakeholder in stakeholder_data.stakeholder_groups %}
    <xbrli:context id="D_StakeHolderGroups{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupAxis">in-capmkt:StakeHolderGroups{{ loop.index }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

    <!-- Training Contexts -->
    {% for gender in ['Male', 'Female', 'Others'] %}
    <xbrli:context id="D_{{ gender }}_TotalEmployeesAndWorkers_Employees">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfTrainingAxis">in-capmkt:OnHealthAndSafetyMeasuresMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_OnSkillUpgradation_Employees">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfTrainingAxis">in-capmkt:OnSkillUpgradationMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_TotalEmployeesAndWorkers_Employees_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfTrainingAxis">in-capmkt:OnHealthAndSafetyMeasuresMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_TotalEmployeesAndWorkers_Workers">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfTrainingAxis">in-capmkt:OnHealthAndSafetyMeasuresMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_TotalEmployeesAndWorkers_Workers_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:TypeOfTrainingAxis">in-capmkt:OnHealthAndSafetyMeasuresMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <!-- Performance Contexts -->
    <xbrli:context id="D_{{ gender }}_Employees">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_Employees_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:EmployeesMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_Workers">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_{{ gender }}_Workers_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:{{ gender }}Member</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="in-capmkt:CategoryOfEmployeesAndWorkersAxis">in-capmkt:WorkersMember</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    {% endfor %}


    <!-- ==================== UNION MEMBERSHIP CONTEXTS ==================== -->
    <!-- Permanent Employees - Union Membership -->
    <xbrli:context id="D_Gender_PermanentEmployees">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gender_PermanentEmployees_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_PermanentEmployees">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_PermanentEmployees_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentEmployees">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentEmployees_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentEmployees">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentEmployees_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentEmployeesMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <!-- Permanent Workers - Union Membership -->
    <xbrli:context id="D_Gender_PermanentWorkers">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Gender_PermanentWorkers_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_PermanentWorkers">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Male_PermanentWorkers_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:MaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentWorkers">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_Female_PermanentWorkers_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:FemaleMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentWorkers">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    <xbrli:context id="D_OtherGender_PermanentWorkers_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:EmployeesOrWorkersAxis">in-capmkt:PermanentWorkersMember</xbrldi:explicitMember><xbrldi:explicitMember dimension="in-capmkt:GenderAxis">in-capmkt:OtherGenderMember</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>

    <!-- Units -->
    <xbrli:unit id="INR"><xbrli:measure>iso4217:INR</xbrli:measure></xbrli:unit>
    <xbrli:unit id="pure"><xbrli:measure>xbrli:pure</xbrli:measure></xbrli:unit>

    <!-- ==================== SECTION A: GENERAL DISCLOSURES ==================== -->
    
    <!-- I. Details of the Listed Entity -->
    <in-capmkt:CorporateIdentityNumber contextRef="DCYMain">{{ cin }}</in-capmkt:CorporateIdentityNumber>
    <in-capmkt:NameOfTheCompany contextRef="ICYMain">{{ company_name }}</in-capmkt:NameOfTheCompany>
    <in-capmkt:DateOfIncorporation contextRef="DCYMain">{{ incorporation_year }}</in-capmkt:DateOfIncorporation>
    <in-capmkt:AddressOfRegisteredOfficeOfCompany contextRef="DCYMain">{{ registered_address }}</in-capmkt:AddressOfRegisteredOfficeOfCompany>
    <in-capmkt:AddressOfCorporateOfficeOfCompany contextRef="DCYMain">{{ corporate_address }}</in-capmkt:AddressOfCorporateOfficeOfCompany>
    <in-capmkt:EMailOfTheCompany contextRef="DCYMain">{{ email }}</in-capmkt:EMailOfTheCompany>
    <in-capmkt:TelephoneOfCompany contextRef="DCYMain">{{ telephone }}</in-capmkt:TelephoneOfCompany>
    <in-capmkt:WebsiteOfCompany contextRef="DCYMain">{{ website }}</in-capmkt:WebsiteOfCompany>
    <in-capmkt:DateOfStartOfFinancialYear contextRef="DCYMain">{{ start_date_cy }}</in-capmkt:DateOfStartOfFinancialYear>
    <in-capmkt:DateOfEndOfFinancialYear contextRef="DCYMain">{{ end_date_cy }}</in-capmkt:DateOfEndOfFinancialYear>
    <in-capmkt:DateOfStartOfPreviousYear contextRef="DCYMain">{{ start_date_py }}</in-capmkt:DateOfStartOfPreviousYear>
    <in-capmkt:DateOfEndOfPreviousYear contextRef="DCYMain">{{ end_date_py }}</in-capmkt:DateOfEndOfPreviousYear>
    <in-capmkt:DateOfStartOfPriorToPreviousYear contextRef="DCYMain">{{ start_date_ppy }}</in-capmkt:DateOfStartOfPriorToPreviousYear>
    <in-capmkt:DateOfEndOfPriorToPreviousYear contextRef="DCYMain">{{ end_date_ppy }}</in-capmkt:DateOfEndOfPriorToPreviousYear>
    <in-capmkt:ValueOfSharesPaidUp contextRef="ICYMain" decimals="0" unitRef="INR">{{ (paid_up_capital * 10000000)|int }}</in-capmkt:ValueOfSharesPaidUp>
    <in-capmkt:NameOfContactPerson contextRef="DCYMain">{{ contact_person_name }}</in-capmkt:NameOfContactPerson>
    <in-capmkt:ContactNumberOfContactPerson contextRef="DCYMain">{{ contact_person_phone }}</in-capmkt:ContactNumberOfContactPerson>
    <in-capmkt:EMailOfContactPerson contextRef="DCYMain">{{ contact_person_email }}</in-capmkt:EMailOfContactPerson>
    <in-capmkt:ReportingBoundary contextRef="DCYMain">{{ reporting_boundary }}</in-capmkt:ReportingBoundary>

    <!-- Assurance -->
    <in-capmkt:WhetherTheCompanyHasUndertakenAssessmentOrAssuranceOfTheBRSRCore contextRef="DCYMain">{{ assurance.has_assurance }}</in-capmkt:WhetherTheCompanyHasUndertakenAssessmentOrAssuranceOfTheBRSRCore>
    {% if assurance.has_assurance == "Yes" %}
    {% if assurance.provider_name %}
    <in-capmkt:NameOfAssuranceProvider contextRef="DCYMain">{{ assurance.provider_name }}</in-capmkt:NameOfAssuranceProvider>
    {% endif %}
    {% if assurance.assurance_type %}
    <in-capmkt:TypeOfAssuranceObtained contextRef="DCYMain">{{ assurance.assurance_type }}</in-capmkt:TypeOfAssuranceObtained>
    {% endif %}
    {% if assurance.type_obtained %}
    <in-capmkt:TypeOfAssessmentOrAssuranceObtain contextRef="DCYMain">{{ assurance.type_obtained }}</in-capmkt:TypeOfAssessmentOrAssuranceObtain>
    {% endif %}
    {% for assessor in assurance.assessors %}
    {% if assessor.company_name %}
    <in-capmkt:NameOfTheCompanyOrLLPOrFirmOfAssessmentOrAssuranceProvider contextRef="D_AssessmentOrAssuranceProvider{{ loop.index }}">{{ assessor.company_name }}</in-capmkt:NameOfTheCompanyOrLLPOrFirmOfAssessmentOrAssuranceProvider>
    {% endif %}
    {% if assessor.company_id %}
    <in-capmkt:CompanyIDOrLLPIDOrFirmIDOfAssessmentOrAssuranceProvider contextRef="D_AssessmentOrAssuranceProvider{{ loop.index }}">{{ assessor.company_id }}</in-capmkt:CompanyIDOrLLPIDOrFirmIDOfAssessmentOrAssuranceProvider>
    {% endif %}
    {% if assessor.assessor_name %}
    <in-capmkt:NameOfTheAssessorOrAssurer contextRef="D_AssessmentOrAssuranceProvider{{ loop.index }}">{{ assessor.assessor_name }}</in-capmkt:NameOfTheAssessorOrAssurer>
    {% endif %}
    {% if assessor.designation %}
    <in-capmkt:DesignationOfAssessorOrAssurer contextRef="D_AssessmentOrAssuranceProvider{{ loop.index }}">{{ assessor.designation }}</in-capmkt:DesignationOfAssessorOrAssurer>
    {% endif %}
    {% if assessor.date_of_signing %}
    <in-capmkt:DateOfSigningByAssessorOrAssurer contextRef="D_AssessmentOrAssuranceProvider{{ loop.index }}">{{ assessor.date_of_signing }}</in-capmkt:DateOfSigningByAssessorOrAssurer>
    {% endif %}
    {% endfor %}
    {% if assurance.section_a %}
    <in-capmkt:TypeOfAssuranceForSectionAGeneralDisclosures contextRef="DCYMain">{{ assurance.section_a }}</in-capmkt:TypeOfAssuranceForSectionAGeneralDisclosures>
    {% endif %}
    {% if assurance.section_b %}
    <in-capmkt:TypeOfAssuranceForSectionBManagementAndProcessDisclosures contextRef="DCYMain">{{ assurance.section_b }}</in-capmkt:TypeOfAssuranceForSectionBManagementAndProcessDisclosures>
    {% endif %}
    {% if assurance.section_c %}
    <in-capmkt:TypeOfAssuranceForSectionCPrincipleWisePerformanceDisclosures contextRef="DCYMain">{{ assurance.section_c }}</in-capmkt:TypeOfAssuranceForSectionCPrincipleWisePerformanceDisclosures>
    {% endif %}
    {% endif %}

    {% for ex in stock_exchanges %}
    <in-capmkt:NameOfStockExchangeWhereTheCompanyIsListed contextRef="D_StockExchangeAxis{{ loop.index }}">{{ ex }}</in-capmkt:NameOfStockExchangeWhereTheCompanyIsListed>
    {% endfor %}

    <!-- II. Products/Services -->
    {% for act in business_activities %}
    <in-capmkt:DescriptionOfMainActivity contextRef="D_BusinessActivities{{ loop.index }}">{{ act.main_activity }}</in-capmkt:DescriptionOfMainActivity>
    <in-capmkt:DescriptionOfBusinessActivity contextRef="D_BusinessActivities{{ loop.index }}">{{ act.business_activity }}</in-capmkt:DescriptionOfBusinessActivity>
    <in-capmkt:PercentageOfTotalTurnoverForBusinessActivities contextRef="D_BusinessActivities{{ loop.index }}" decimals="INF" unitRef="pure">{{ act.turnover_pct }}</in-capmkt:PercentageOfTotalTurnoverForBusinessActivities>
    {% endfor %}

    {% for prod in products_services %}
    <in-capmkt:ProductOrServiceSoldByTheEntity contextRef="D_ProductServiceSold{{ loop.index }}">{{ prod.product }}</in-capmkt:ProductOrServiceSoldByTheEntity>
    <in-capmkt:NICCodeOfProductOrServiceSoldByTheEntity contextRef="D_ProductServiceSold{{ loop.index }}">{{ prod.nic_code }}</in-capmkt:NICCodeOfProductOrServiceSoldByTheEntity>
    <in-capmkt:PercentageOfTotalTurnoverForProductOrServiceSold contextRef="D_ProductServiceSold{{ loop.index }}" decimals="INF" unitRef="pure">{{ prod.turnover_pct }}</in-capmkt:PercentageOfTotalTurnoverForProductOrServiceSold>
    {% endfor %}

    <!-- III. Operations - Q19: Number of locations -->
    <!-- National locations -->
    <in-capmkt:NumberOfLocations contextRef="D_Plant_National" decimals="0" unitRef="pure">{{ locations.national.plants|int }}</in-capmkt:NumberOfLocations>
    <in-capmkt:NumberOfLocations contextRef="D_Office_National" decimals="0" unitRef="pure">{{ locations.national.offices|int }}</in-capmkt:NumberOfLocations>
    <in-capmkt:NumberOfLocations contextRef="D_Location_National" decimals="0" unitRef="pure">{{ locations.national.total|int }}</in-capmkt:NumberOfLocations>
    <!-- International locations -->
    <in-capmkt:NumberOfLocations contextRef="D_Plant_International" decimals="0" unitRef="pure">{{ locations.international.plants|int }}</in-capmkt:NumberOfLocations>
    <in-capmkt:NumberOfLocations contextRef="D_Office_International" decimals="0" unitRef="pure">{{ locations.international.offices|int }}</in-capmkt:NumberOfLocations>
    <in-capmkt:NumberOfLocations contextRef="D_Location_International" decimals="0" unitRef="pure">{{ locations.international.total|int }}</in-capmkt:NumberOfLocations>

    <!-- Q20: Markets served -->
    <!-- a. Number of states and countries -->
    <in-capmkt:NumberOfStatesWhereMarketServedByTheEntity contextRef="DCYMain" decimals="0" unitRef="pure">{{ markets.national_states_count|int }}</in-capmkt:NumberOfStatesWhereMarketServedByTheEntity>
    <in-capmkt:NumberOfCountriesWhereMarketServedByTheEntity contextRef="DCYMain" decimals="0" unitRef="pure">{{ markets.international_countries_count|int }}</in-capmkt:NumberOfCountriesWhereMarketServedByTheEntity>

    <!-- b. Contribution of exports as percentage of total turnover (Section A Q20b) -->
    <in-capmkt:PercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntity contextRef="DCYMain" decimals="INF" unitRef="pure">{{ markets.export_pct }}</in-capmkt:PercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntity>

    <!-- c. Brief on types of customers -->
    <in-capmkt:ABriefOnTypesOfCustomersExplanatoryTextBlock contextRef="DCYMain">{{ markets.customer_types_brief }}</in-capmkt:ABriefOnTypesOfCustomersExplanatoryTextBlock>

    <!-- ==================== IV. EMPLOYEES/WORKERS - TABLE A (All including Differently Abled) ==================== -->
    
    <!-- Permanent Employees -->
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_PermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.permanent.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_PermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.permanent.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_PermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.permanent.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_PermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.permanent.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_PermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.permanent.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_PermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.permanent.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_PermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.permanent.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

    <!-- Other Than Permanent Employees -->
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_OtherThanPermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.other.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_OtherThanPermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.other.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_OtherThanPermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.other.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_OtherThanPermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.other.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_OtherThanPermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.other.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_OtherThanPermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.other.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_OtherThanPermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.other.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <!-- Total Employees -->
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_Employees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.total.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_Employees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.total.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_Employees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.total.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_Employees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.total.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_Employees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.total.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_Employees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.total.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_Employees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.total.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

<!-- Permanent Workers -->
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_PermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.permanent.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_PermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.permanent.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_PermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.permanent.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_PermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.permanent.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_PermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.permanent.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_PermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.permanent.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_PermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.permanent.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

<!-- Other Than Permanent Workers -->
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_OtherThanPermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.other.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_OtherThanPermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.other.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_OtherThanPermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.other.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_OtherThanPermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.other.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_OtherThanPermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.other.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_OtherThanPermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.other.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_OtherThanPermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.other.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

<!-- Total Workers -->
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_Workers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.total.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_Workers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.total.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_Workers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.total.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_Workers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.total.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_Workers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.total.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_Workers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.total.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_Workers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.total.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

<!-- ==================== TABLE B: DIFFERENTLY ABLED EMPLOYEES/WORKERS ==================== -->

<!-- Permanent Employees - Differently Abled -->
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_PermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_PermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_PermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_PermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_PermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_PermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_PermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<!-- Other Than Permanent Employees - Differently Abled -->
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_OtherThanPermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.other.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_OtherThanPermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.other.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_OtherThanPermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.other.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_OtherThanPermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.other.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_OtherThanPermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.other.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_OtherThanPermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.other.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_OtherThanPermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.other.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<!-- Total Employees - Differently Abled -->
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_Employees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.total.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_Employees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.total.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_Employees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.total.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_Employees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.total.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_Employees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.total.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_Employees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.total.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_Employees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.total.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<!-- Permanent Workers - Differently Abled -->
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_PermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_PermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_PermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_PermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_PermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_PermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_PermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<!-- Other Than Permanent Workers - Differently Abled -->
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_OtherThanPermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.other.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_OtherThanPermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.other.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_OtherThanPermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.other.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_OtherThanPermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.other.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_OtherThanPermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.other.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_OtherThanPermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.other.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_OtherThanPermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.other.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<!-- Total Workers - Differently Abled -->
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_Workers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.total.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_Workers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.total.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_Workers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.total.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_Workers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.total.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_Workers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.total.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_Workers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.total.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_Workers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.total.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<!-- Board of Directors and KMP -->
<in-capmkt:TotalNumberOfBoardOfDirectors contextRef="DCYMain" decimals="0" unitRef="pure">{{ women_rep.board.total|int }}</in-capmkt:TotalNumberOfBoardOfDirectors>
<in-capmkt:NumberOfFemaleBoardOfDirectors contextRef="DCYMain" decimals="0" unitRef="pure">{{ women_rep.board.female|int }}</in-capmkt:NumberOfFemaleBoardOfDirectors>
<in-capmkt:PercentageOfFemaleBoardOfDirectors contextRef="DCYMain" decimals="INF" unitRef="pure">{{ women_rep.board.pct }}</in-capmkt:PercentageOfFemaleBoardOfDirectors>
<in-capmkt:TotalNumberOfKeyManagementPersonnel contextRef="DCYMain" decimals="0" unitRef="pure">{{ women_rep.kmp.total|int }}</in-capmkt:TotalNumberOfKeyManagementPersonnel>
<in-capmkt:NumberOfFemaleKeyManagementPersonnel contextRef="DCYMain" decimals="0" unitRef="pure">{{ women_rep.kmp.female|int }}</in-capmkt:NumberOfFemaleKeyManagementPersonnel>
<in-capmkt:PercentageOfFemaleKeyManagementPersonnel contextRef="DCYMain" decimals="INF" unitRef="pure">{{ women_rep.kmp.pct }}</in-capmkt:PercentageOfFemaleKeyManagementPersonnel>

<!-- ==================== TURNOVER RATES ==================== -->
<!-- Permanent Employees Turnover - CY -->
<in-capmkt:TurnoverRate contextRef="D_Male_PermanentEmployees_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.cy.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentEmployees_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.cy.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentEmployees_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.cy.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentEmployees_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.cy.total }}</in-capmkt:TurnoverRate>

<!-- Permanent Employees Turnover - PY -->
<in-capmkt:TurnoverRate contextRef="D_Male_PermanentEmployees_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.py.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentEmployees_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.py.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentEmployees_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.py.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentEmployees_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.py.total }}</in-capmkt:TurnoverRate>

<!-- Permanent Employees Turnover - PPY -->
<in-capmkt:TurnoverRate contextRef="D_Male_PermanentEmployees_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.ppy.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentEmployees_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.ppy.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentEmployees_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.ppy.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentEmployees_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.ppy.total }}</in-capmkt:TurnoverRate>

<!-- Permanent Workers Turnover - CY -->
<in-capmkt:TurnoverRate contextRef="D_Male_PermanentWorkers_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.cy.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentWorkers_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.cy.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentWorkers_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.cy.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentWorkers_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.cy.total }}</in-capmkt:TurnoverRate>

<!-- Permanent Workers Turnover - PY -->
<in-capmkt:TurnoverRate contextRef="D_Male_PermanentWorkers_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.py.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentWorkers_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.py.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentWorkers_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.py.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentWorkers_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.py.total }}</in-capmkt:TurnoverRate>

<!-- Permanent Workers Turnover - PPY -->
<in-capmkt:TurnoverRate contextRef="D_Male_PermanentWorkers_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.ppy.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentWorkers_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.ppy.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentWorkers_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.ppy.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentWorkers_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.ppy.total }}</in-capmkt:TurnoverRate>

<!-- V. Subsidiaries -->
{% for sub in subsidiaries %}
<in-capmkt:NameOfTheHoldingOrSubsidiaryAssociateCompaniesOrJointVentures contextRef="D_HoldingSubsidiaryAssociateCompaniesAndJointVentures{{ loop.index }}">{{ sub.name }}</in-capmkt:NameOfTheHoldingOrSubsidiaryAssociateCompaniesOrJointVentures>
<in-capmkt:CategoryOfCompany contextRef="D_HoldingSubsidiaryAssociateCompaniesAndJointVentures{{ loop.index }}">{{ sub.category }}</in-capmkt:CategoryOfCompany>
<in-capmkt:PercentageOfSharesHeldByListedEntity contextRef="D_HoldingSubsidiaryAssociateCompaniesAndJointVentures{{ loop.index }}" decimals="INF" unitRef="pure">{{ sub.shares_pct }}</in-capmkt:PercentageOfSharesHeldByListedEntity>
<in-capmkt:DoesCompanyParticipateInTheBusinessResponsibilityInitiativesOfTheListedEntity contextRef="D_HoldingSubsidiaryAssociateCompaniesAndJointVentures{{ loop.index }}">{{ 'true' if sub.participates == 'Yes' else 'false' }}</in-capmkt:DoesCompanyParticipateInTheBusinessResponsibilityInitiativesOfTheListedEntity>
{% endfor %}

<!-- VI. CSR -->
<in-capmkt:WhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013 contextRef="DCYMain">{{ csr.applicable }}</in-capmkt:WhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013>
<in-capmkt:Turnover contextRef="DCYMain" decimals="1" unitRef="INR">{{ csr.turnover }}</in-capmkt:Turnover>
<in-capmkt:NetWorth contextRef="DCYMain" decimals="2" unitRef="INR">{{ csr.net_worth }}</in-capmkt:NetWorth>

<!-- CSR Projects in Aspirational Districts (Principle 8, Leadership Indicator) -->
{% for project in csr.aspirational_districts %}
<in-capmkt:StateOfCSRProjectsUndertaken contextRef="{{ project.axis_id }}">{{ project.state }}</in-capmkt:StateOfCSRProjectsUndertaken>
<in-capmkt:AspirationalDistrictOfCSRProjectsUndertaken contextRef="{{ project.axis_id }}">{{ project.aspirational_district }}</in-capmkt:AspirationalDistrictOfCSRProjectsUndertaken>
<in-capmkt:AmountSpentForCSRProjectsUndertaken contextRef="{{ project.axis_id }}" decimals="0" unitRef="INR">{{ project.amount_spent }}</in-capmkt:AmountSpentForCSRProjectsUndertaken>
{% endfor %}


<!-- ==================== SECTION B: MANAGEMENT AND PROCESS DISCLOSURES ==================== -->
<!-- 1a. Whether policy covers each principle -->
{% for p in section_b %}
<in-capmkt:WhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs contextRef="D_Principle{{ p.num }}">{{ p.policy_covers }}</in-capmkt:WhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs>
{% endfor %}

<!-- 1b. Has policy been approved by Board -->
{% for p in section_b %}
<in-capmkt:HasThePolicyBeenApprovedByTheBoard contextRef="D_Principle{{ p.num }}">{{ p.board_approved }}</in-capmkt:HasThePolicyBeenApprovedByTheBoard>
{% endfor %}

<!-- 1c. Web Link of Policies -->
{% for p in section_b %}
<in-capmkt:WebLinkOfThePoliciesExplanatoryTextBlock contextRef="D_Principle{{ p.num }}">{{ p.web_link }}</in-capmkt:WebLinkOfThePoliciesExplanatoryTextBlock>
{% endfor %}

<!-- 2. Whether entity has translated policy into procedures -->
{% for p in section_b %}
<in-capmkt:WhetherTheEntityHasTranslatedThePolicyIntoProcedures contextRef="D_Principle{{ p.num }}">{{ p.translated_to_procedures }}</in-capmkt:WhetherTheEntityHasTranslatedThePolicyIntoProcedures>
{% endfor %}

<!-- 3. Do policies extend to value chain partners -->
{% for p in section_b %}
<in-capmkt:DoTheEnlistedPoliciesExtendToYourValueChainPartners contextRef="D_Principle{{ p.num }}">{{ p.extends_to_value_chain }}</in-capmkt:DoTheEnlistedPoliciesExtendToYourValueChainPartners>
{% endfor %}

<!-- 4. National/International codes/certifications -->
{% for p in section_b %}
<in-capmkt:NameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrincipleExplanatoryTextBlock contextRef="D_Principle{{ p.num }}">{{ p.codes_certifications if p.codes_certifications else 'NA' }}</in-capmkt:NameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrincipleExplanatoryTextBlock>
{% endfor %}

<!-- 5. Specific commitments, goals and targets -->
{% for p in section_b %}
<in-capmkt:SpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelinesExplanatoryTextBlock contextRef="D_Principle{{ p.num }}">{{ p.commitments_goals if p.commitments_goals else 'NA' }}</in-capmkt:SpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelinesExplanatoryTextBlock>
{% endfor %}

<!-- 6. Performance against commitments -->
{% for p in section_b %}
<in-capmkt:PerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMetExplanatoryTextBlock contextRef="D_Principle{{ p.num }}">{{ p.performance if p.performance else 'NA' }}</in-capmkt:PerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMetExplanatoryTextBlock>

<!-- ==================== PRINCIPLE 5: HUMAN RIGHTS ==================== -->

    <!-- Minimum Wages - CY Permanent Employees -->
    <!-- Male -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.male.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.male.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Female -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.female.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.female.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Other Gender -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.other.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.other.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Total -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.total.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.total.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

    <!-- Minimum Wages - PY Permanent Employees -->
    <!-- Male -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.male.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.male.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Female -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.female.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.female.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Other Gender -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.other.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.other.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Total -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.total.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.total.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

    <!-- Minimum Wages - CY Other Than Permanent Employees -->
    <!-- Male -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.male.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.male.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Female -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.female.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.female.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Other Gender -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.other.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.other.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Total -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.total.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.total.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

    <!-- Minimum Wages - PY Other Than Permanent Employees -->
    <!-- Male -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.male.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.male.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Female -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.female.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.female.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Other Gender -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.other.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.other.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Total -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.total.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.total.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

    <!-- Minimum Wages - CY Permanent Workers -->
    <!-- Male -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.male.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.male.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Female -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.female.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.female.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Other Gender -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.other.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.other.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Total -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.total.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.total.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

    <!-- Minimum Wages - PY Permanent Workers -->
    <!-- Male -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.male.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.male.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Female -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.female.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.female.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Other Gender -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.other.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.other.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Total -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.total.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.total.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

    <!-- Minimum Wages - CY Other Than Permanent Workers -->
    <!-- Male -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.male.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.male.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Female -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.female.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.female.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Other Gender -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.other.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.other.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Total -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.total.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.total.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

    <!-- Minimum Wages - PY Other Than Permanent Workers -->
    <!-- Male -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.male.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.male.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Female -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.female.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.female.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Other Gender -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.other.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.other.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <!-- Total -->
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.total.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.total.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

    <!-- Human Rights Training - Employees -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <!-- Human Rights Training - Employees PY -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <!-- Human Rights Training - Workers -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <!-- Human Rights Training - Workers PY -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <!-- Median Remuneration -->
    <in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages contextRef="D_Male_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.bod.male_num | int }}</in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors contextRef="D_Male_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.bod.male_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors>
    <in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages contextRef="D_Female_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.bod.female_num | int }}</in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors contextRef="D_Female_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.bod.female_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors>
    <in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages contextRef="D_OtherGender_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.bod.other_num | int }}</in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors contextRef="D_OtherGender_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.bod.other_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors>

    <in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages contextRef="D_Male_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.kmp.male_num | int }}</in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel contextRef="D_Male_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.kmp.male_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel>
    <in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages contextRef="D_Female_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.kmp.female_num | int }}</in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel contextRef="D_Female_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.kmp.female_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel>
    <in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages contextRef="D_OtherGender_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.kmp.other_num | int }}</in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel contextRef="D_OtherGender_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.kmp.other_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel>

    <in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages contextRef="D_Male_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.employees.male_num | int }}</in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP contextRef="D_Male_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.employees.male_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP>
    <in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages contextRef="D_Female_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.employees.female_num | int }}</in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP contextRef="D_Female_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.employees.female_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP>
    <in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages contextRef="D_OtherGender_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.employees.other_num | int }}</in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP contextRef="D_OtherGender_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.employees.other_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP>

    <in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages contextRef="D_Male_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.workers.male_num | int }}</in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers contextRef="D_Male_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.workers.male_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers>
    <in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages contextRef="D_Female_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.workers.female_num | int }}</in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers contextRef="D_Female_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.workers.female_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers>
    <in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages contextRef="D_OtherGender_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.workers.other_num | int }}</in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers contextRef="D_OtherGender_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.workers.other_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers>

    <!-- Gross Wages -->
    <in-capmkt:GrossWagesPaidToFemale contextRef="DCYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.female_cy }}</in-capmkt:GrossWagesPaidToFemale>
    <in-capmkt:GrossWagesPaidToFemale contextRef="DPYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.female_py }}</in-capmkt:GrossWagesPaidToFemale>
    <in-capmkt:TotalWagesPaid contextRef="DCYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.total_cy }}</in-capmkt:TotalWagesPaid>
    <in-capmkt:TotalWagesPaid contextRef="DPYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.total_py }}</in-capmkt:TotalWagesPaid>
    <in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.gross_wages.female_pct_cy }}</in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid>
    <in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid contextRef="DPYMain" decimals="INF" unitRef="pure">{{ human_rights_data.gross_wages.female_pct_py }}</in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid>
    <in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear contextRef="DCYMain" decimals="0" unitRef="pure">{{ human_rights_data.gross_wages.avg_female_emp_workers_cy | int }}</in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear>
    <in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear contextRef="DPYMain" decimals="0" unitRef="pure">{{ human_rights_data.gross_wages.avg_female_emp_workers_py | int }}</in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear>

    <!-- Focal Point and Internal Mechanisms -->
    <in-capmkt:DoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness contextRef="DCYMain">{{ human_rights_data.focal_point }}</in-capmkt:DoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness>
    <in-capmkt:DetailsOfFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusinessExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.focal_point_details | e }}</in-capmkt:DetailsOfFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusinessExplanatoryTextBlock>
    <in-capmkt:DescribeTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.internal_mechanisms | e }}</in-capmkt:DescribeTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesExplanatoryTextBlock>
    <in-capmkt:DoHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts contextRef="DCYMain">{{ human_rights_data.hr_in_contracts }}</in-capmkt:DoHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts>

<!-- ==================== PRINCIPLE 5: HUMAN RIGHTS ==================== -->
    <!-- Human Rights Training - Employees -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <!-- Human Rights Training - Employees PY -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <!-- Human Rights Training - Workers -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <!-- Human Rights Training - Workers PY -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <!-- Median Remuneration -->
    <in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages contextRef="D_Male_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.bod.male_num | int }}</in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors contextRef="D_Male_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.bod.male_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors>
    <in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages contextRef="D_Female_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.bod.female_num | int }}</in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors contextRef="D_Female_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.bod.female_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors>
    <in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages contextRef="D_OtherGender_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.bod.other_num | int }}</in-capmkt:NumberOfBoardOfDirectorsForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors contextRef="D_OtherGender_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.bod.other_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfBoardOfDirectors>

    <in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages contextRef="D_Male_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.kmp.male_num | int }}</in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel contextRef="D_Male_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.kmp.male_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel>
    <in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages contextRef="D_Female_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.kmp.female_num | int }}</in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel contextRef="D_Female_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.kmp.female_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel>
    <in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages contextRef="D_OtherGender_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.kmp.other_num | int }}</in-capmkt:NumberOfKeyManagerialPersonnelForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel contextRef="D_OtherGender_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.kmp.other_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfKeyManagerialPersonnel>

    <in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages contextRef="D_Male_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.employees.male_num | int }}</in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP contextRef="D_Male_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.employees.male_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP>
    <in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages contextRef="D_Female_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.employees.female_num | int }}</in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP contextRef="D_Female_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.employees.female_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP>
    <in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages contextRef="D_OtherGender_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.employees.other_num | int }}</in-capmkt:NumberOfEmployeesOtherThanBodAndKMPForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP contextRef="D_OtherGender_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.employees.other_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfEmployeesOtherThanBodAndKMP>

    <in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages contextRef="D_Male_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.workers.male_num | int }}</in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers contextRef="D_Male_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.workers.male_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers>
    <in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages contextRef="D_Female_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.workers.female_num | int }}</in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers contextRef="D_Female_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.workers.female_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers>
    <in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages contextRef="D_OtherGender_p5" decimals="0" unitRef="pure">{{ human_rights_data.median_remuneration.workers.other_num | int }}</in-capmkt:NumberOfWorkersForRemunerationOrSalaryOrWages>
    <in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers contextRef="D_OtherGender_p5" decimals="0" unitRef="INR">{{ human_rights_data.median_remuneration.workers.other_median | int }}</in-capmkt:MedianOfRemunerationOrSalaryOrWagesOfWorkers>

    <!-- Gross Wages -->
    <in-capmkt:GrossWagesPaidToFemale contextRef="DCYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.female_cy }}</in-capmkt:GrossWagesPaidToFemale>
    <in-capmkt:GrossWagesPaidToFemale contextRef="DPYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.female_py }}</in-capmkt:GrossWagesPaidToFemale>
    <in-capmkt:TotalWagesPaid contextRef="DCYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.total_cy }}</in-capmkt:TotalWagesPaid>
    <in-capmkt:TotalWagesPaid contextRef="DPYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.total_py }}</in-capmkt:TotalWagesPaid>
    <in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.gross_wages.female_pct_cy }}</in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid>
    <in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid contextRef="DPYMain" decimals="INF" unitRef="pure">{{ human_rights_data.gross_wages.female_pct_py }}</in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid>
    <in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear contextRef="DCYMain" decimals="0" unitRef="pure">{{ human_rights_data.gross_wages.avg_female_emp_workers_cy | int }}</in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear>
    <in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear contextRef="DPYMain" decimals="0" unitRef="pure">{{ human_rights_data.gross_wages.avg_female_emp_workers_py | int }}</in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear>

    <!-- Focal Point and Internal Mechanisms -->
    <in-capmkt:DoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness contextRef="DCYMain">{{ human_rights_data.focal_point }}</in-capmkt:DoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness>
    <in-capmkt:DetailsOfFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusinessExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.focal_point_details | e }}</in-capmkt:DetailsOfFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusinessExplanatoryTextBlock>
    <in-capmkt:DescribeTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.internal_mechanisms | e }}</in-capmkt:DescribeTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesExplanatoryTextBlock>
    <in-capmkt:DoHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts contextRef="DCYMain">{{ human_rights_data.hr_in_contracts }}</in-capmkt:DoHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts>

<!-- HR Complaints - 6 Categories CY -->
    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_1" decimals="0" unitRef="pure">{{ human_rights_data.complaints.sexual_harassment.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_1" decimals="0" unitRef="pure">{{ human_rights_data.complaints.sexual_harassment.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_1">{{ human_rights_data.complaints.sexual_harassment.remarks_cy | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_2" decimals="0" unitRef="pure">{{ human_rights_data.complaints.discrimination.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_2" decimals="0" unitRef="pure">{{ human_rights_data.complaints.discrimination.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_2">{{ human_rights_data.complaints.discrimination.remarks_cy | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_3" decimals="0" unitRef="pure">{{ human_rights_data.complaints.child_labour.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_3" decimals="0" unitRef="pure">{{ human_rights_data.complaints.child_labour.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_3">{{ human_rights_data.complaints.child_labour.remarks_cy | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_4" decimals="0" unitRef="pure">{{ human_rights_data.complaints.forced_labour.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_4" decimals="0" unitRef="pure">{{ human_rights_data.complaints.forced_labour.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_4">{{ human_rights_data.complaints.forced_labour.remarks_cy | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_5" decimals="0" unitRef="pure">{{ human_rights_data.complaints.wages.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_5" decimals="0" unitRef="pure">{{ human_rights_data.complaints.wages.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_5">{{ human_rights_data.complaints.wages.remarks_cy | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_6" decimals="0" unitRef="pure">{{ human_rights_data.complaints.other.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_6" decimals="0" unitRef="pure">{{ human_rights_data.complaints.other.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_6">{{ human_rights_data.complaints.other.remarks_cy | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <!-- HR Complaints - 6 Categories PY -->
    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_1_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.sexual_harassment.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_1_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.sexual_harassment.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_1_PY">{{ human_rights_data.complaints.sexual_harassment.remarks_py | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_2_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.discrimination.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_2_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.discrimination.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_2_PY">{{ human_rights_data.complaints.discrimination.remarks_py | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_3_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.child_labour.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_3_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.child_labour.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_3_PY">{{ human_rights_data.complaints.child_labour.remarks_py | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_4_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.forced_labour.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_4_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.forced_labour.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_4_PY">{{ human_rights_data.complaints.forced_labour.remarks_py | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_5_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.wages.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_5_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.wages.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_5_PY">{{ human_rights_data.complaints.wages.remarks_py | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_NumberOfComplaintsFiledDuringTheYear_6_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.other.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_NumberOfComplaintsPendingResolutionAtTheEndOfYear_6_PY" decimals="0" unitRef="pure">{{ human_rights_data.complaints.other.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:RemarksforComplaintsExplanatoryTextBlock contextRef="D_RemarksforComplaintsExplanatoryTextBlock_6_PY">{{ human_rights_data.complaints.other.remarks_py | default('NA', true) }}</in-capmkt:RemarksforComplaintsExplanatoryTextBlock>

    <!-- POSH Data -->
    <in-capmkt:TotalComplaintsReportedUnderSexualHarassmentOfWomenAtWorkplace contextRef="DCYMain" decimals="0" unitRef="pure">{{ human_rights_data.posh.total_complaints_cy | int }}</in-capmkt:TotalComplaintsReportedUnderSexualHarassmentOfWomenAtWorkplace>
    <in-capmkt:TotalComplaintsReportedUnderSexualHarassmentOfWomenAtWorkplace contextRef="DPYMain" decimals="0" unitRef="pure">{{ human_rights_data.posh.total_complaints_py | int }}</in-capmkt:TotalComplaintsReportedUnderSexualHarassmentOfWomenAtWorkplace>
    <in-capmkt:PercentageOfComplaintsInRespectOfNumberOfEmployeesOrWorker contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.posh.pct_complaints_cy }}</in-capmkt:PercentageOfComplaintsInRespectOfNumberOfEmployeesOrWorker>
    <in-capmkt:PercentageOfComplaintsInRespectOfNumberOfEmployeesOrWorker contextRef="DPYMain" decimals="INF" unitRef="pure">{{ human_rights_data.posh.pct_complaints_py }}</in-capmkt:PercentageOfComplaintsInRespectOfNumberOfEmployeesOrWorker>
    <in-capmkt:ComplaintsOnPOSHUpHeld contextRef="DCYMain" decimals="0" unitRef="pure">{{ human_rights_data.posh.upheld_cy | int }}</in-capmkt:ComplaintsOnPOSHUpHeld>
    <in-capmkt:ComplaintsOnPOSHUpHeld contextRef="DPYMain" decimals="0" unitRef="pure">{{ human_rights_data.posh.upheld_py | int }}</in-capmkt:ComplaintsOnPOSHUpHeld>
    <in-capmkt:MechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCasesExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.mechanisms_prevent_adverse | e }}</in-capmkt:MechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCasesExplanatoryTextBlock>

    <!-- Plant/Office Assessments -->
    <in-capmkt:PercentageOfChildLabourOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.child_labour }}</in-capmkt:PercentageOfChildLabourOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:PercentageOfForcedLabourOrInvoluntaryLabourOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.forced_labour }}</in-capmkt:PercentageOfForcedLabourOrInvoluntaryLabourOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:PercentageOfSexualHarassmentOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.sexual_harassment }}</in-capmkt:PercentageOfSexualHarassmentOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:PercentageOfDiscriminationAtWorkPlaceOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.discrimination }}</in-capmkt:PercentageOfDiscriminationAtWorkPlaceOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:PercentageOfWagesOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.wages }}</in-capmkt:PercentageOfWagesOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOfficeExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.corrective_actions_plants | e }}</in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOfficeExplanatoryTextBlock>

    <!-- Other Assessments - Plants and Offices -->
    <in-capmkt:NameOfOtherAssessmentsOfPlantAndOffice contextRef="D_OtherAssessments12">{{ human_rights_data.other_assessments_plants.name | e }}</in-capmkt:NameOfOtherAssessmentsOfPlantAndOffice>
    <in-capmkt:PercentageOfOtherAssessmentsOfPlantAndOffice contextRef="D_OtherAssessments12" decimals="INF" unitRef="pure">{{ human_rights_data.other_assessments_plants.percentage }}</in-capmkt:PercentageOfOtherAssessmentsOfPlantAndOffice>

    <!-- Value Chain Assessments -->
    <in-capmkt:PercentageOfChildLabourOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.child_labour }}</in-capmkt:PercentageOfChildLabourOfValueChainPartnersP5>
    <in-capmkt:PercentageOfForcedLabourOrInvoluntaryLabourOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.forced_labour }}</in-capmkt:PercentageOfForcedLabourOrInvoluntaryLabourOfValueChainPartnersP5>
    <in-capmkt:PercentageOfSexualHarassmentOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.sexual_harassment }}</in-capmkt:PercentageOfSexualHarassmentOfValueChainPartnersP5>
    <in-capmkt:PercentageOfDiscriminationAtWorkPlaceOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.discrimination }}</in-capmkt:PercentageOfDiscriminationAtWorkPlaceOfValueChainPartnersP5>
    <in-capmkt:PercentageOfWagesOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.wages }}</in-capmkt:PercentageOfWagesOfValueChainPartnersP5>
    <in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartnerExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.corrective_actions_value_chain | e }}</in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartnerExplanatoryTextBlock>

    <!-- Other Assessments - Value Chain Partners -->
    <in-capmkt:NameOfOtherAssessmentOfValueChainPartner contextRef="D_OtherAssessmentOfValueChainPartners12">{{ human_rights_data.other_assessments_value_chain.name | e }}</in-capmkt:NameOfOtherAssessmentOfValueChainPartner>
    <in-capmkt:PercentageOfOtherAssessmentOfValueChainPartner contextRef="D_OtherAssessmentOfValueChainPartners12" decimals="INF" unitRef="pure">{{ human_rights_data.other_assessments_value_chain.percentage }}</in-capmkt:PercentageOfOtherAssessmentOfValueChainPartner>

    <!-- Business Process and Due Diligence -->
    <in-capmkt:DetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaintsExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.business_process_modified | e }}</in-capmkt:DetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaintsExplanatoryTextBlock>
    <in-capmkt:DetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConductedExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.hr_due_diligence | e }}</in-capmkt:DetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConductedExplanatoryTextBlock>
    <in-capmkt:IsThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">{{ 'true' if human_rights_data.differently_abled_accessible == 'Yes' else 'false' }}</in-capmkt:IsThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016>

    <!-- ==================== PRINCIPLE 6: ENVIRONMENT ==================== -->
    <!-- Energy Consumption -->
    <in-capmkt:WhetherDetailsOfTotalEnergyConsumptionAndEnergyIntensityApplicableToTheCompany contextRef="DCYMain">true</in-capmkt:WhetherDetailsOfTotalEnergyConsumptionAndEnergyIntensityApplicableToTheCompany>

    <!-- Revenue from Operations -->
    <in-capmkt:RevenueFromOperations contextRef="DCYMain" decimals="2" unitRef="INR">{{ environment_data.revenue_from_operations_cy }}</in-capmkt:RevenueFromOperations>
    <in-capmkt:RevenueFromOperations contextRef="DPYMain" decimals="2" unitRef="INR">{{ environment_data.revenue_from_operations_py }}</in-capmkt:RevenueFromOperations>

    <in-capmkt:TotalElectricityConsumptionFromRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.elec_renewable_cy }}</in-capmkt:TotalElectricityConsumptionFromRenewableSources>
    <in-capmkt:TotalElectricityConsumptionFromRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.elec_renewable_py }}</in-capmkt:TotalElectricityConsumptionFromRenewableSources>
    <in-capmkt:TotalFuelConsumptionFromRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.fuel_renewable_cy }}</in-capmkt:TotalFuelConsumptionFromRenewableSources>
    <in-capmkt:TotalFuelConsumptionFromRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.fuel_renewable_py }}</in-capmkt:TotalFuelConsumptionFromRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_renewable_cy }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_renewable_py }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources>

    <!-- Energy Other Sources - Renewable - With Dimension Context -->
    <in-capmkt:NameOfOtherParameterOfEnergyConsumptionThroughOtherSourceFromRenewableSources contextRef="D_EnergyConsumptionThroughOtherSourceFromRenewableSources1">{{ environment_data.energy.other_renewable_name_cy | default('Other renewable source', true) | e }}</in-capmkt:NameOfOtherParameterOfEnergyConsumptionThroughOtherSourceFromRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources contextRef="D_EnergyConsumptionThroughOtherSourceFromRenewableSources1" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_renewable_cy }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources>
    <in-capmkt:NameOfOtherParameterOfEnergyConsumptionThroughOtherSourceFromRenewableSources contextRef="D_EnergyConsumptionThroughOtherSourceFromRenewableSources_PY1">{{ environment_data.energy.other_renewable_name_py | default('Other renewable source', true) | e }}</in-capmkt:NameOfOtherParameterOfEnergyConsumptionThroughOtherSourceFromRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources contextRef="D_EnergyConsumptionThroughOtherSourceFromRenewableSources_PY1" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_renewable_py }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources>

    <in-capmkt:TotalEnergyConsumedFromRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.total_renewable_cy }}</in-capmkt:TotalEnergyConsumedFromRenewableSources>
    <in-capmkt:TotalEnergyConsumedFromRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.total_renewable_py }}</in-capmkt:TotalEnergyConsumedFromRenewableSources>

    <in-capmkt:TotalElectricityConsumptionFromNonRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.elec_nonrenewable_cy }}</in-capmkt:TotalElectricityConsumptionFromNonRenewableSources>
    <in-capmkt:TotalElectricityConsumptionFromNonRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.elec_nonrenewable_py }}</in-capmkt:TotalElectricityConsumptionFromNonRenewableSources>
    <in-capmkt:TotalFuelConsumptionFromNonRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.fuel_nonrenewable_cy }}</in-capmkt:TotalFuelConsumptionFromNonRenewableSources>
    <in-capmkt:TotalFuelConsumptionFromNonRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.fuel_nonrenewable_py }}</in-capmkt:TotalFuelConsumptionFromNonRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromNonRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_nonrenewable_cy }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromNonRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromNonRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_nonrenewable_py }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromNonRenewableSources>

    <!-- Energy Other Sources - Non-Renewable - With Dimension Context -->
    <in-capmkt:NameOfOtherParameterOfEnergyConsumptionThroughOtherSourceFromNonRenewableSources contextRef="D_EnergyConsumptionThroughOtherSourceFromNonRenewableSources1">{{ environment_data.energy.other_nonrenewable_name_cy | default('Other non-renewable source', true) | e }}</in-capmkt:NameOfOtherParameterOfEnergyConsumptionThroughOtherSourceFromNonRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromNonRenewableSources contextRef="D_EnergyConsumptionThroughOtherSourceFromNonRenewableSources1" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_nonrenewable_cy }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromNonRenewableSources>
    <in-capmkt:NameOfOtherParameterOfEnergyConsumptionThroughOtherSourceFromNonRenewableSources contextRef="D_EnergyConsumptionThroughOtherSourceFromNonRenewableSources_PY1">{{ environment_data.energy.other_nonrenewable_name_py | default('Other non-renewable source', true) | e }}</in-capmkt:NameOfOtherParameterOfEnergyConsumptionThroughOtherSourceFromNonRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromNonRenewableSources contextRef="D_EnergyConsumptionThroughOtherSourceFromNonRenewableSources_PY1" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_nonrenewable_py }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromNonRenewableSources>

    <in-capmkt:TotalEnergyConsumedFromNonRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.total_nonrenewable_cy }}</in-capmkt:TotalEnergyConsumedFromNonRenewableSources>
    <in-capmkt:TotalEnergyConsumedFromNonRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.total_nonrenewable_py }}</in-capmkt:TotalEnergyConsumedFromNonRenewableSources>

    <in-capmkt:TotalEnergyConsumedFromRenewableAndNonRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.total_energy_cy }}</in-capmkt:TotalEnergyConsumedFromRenewableAndNonRenewableSources>
    <in-capmkt:TotalEnergyConsumedFromRenewableAndNonRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.total_energy_py }}</in-capmkt:TotalEnergyConsumedFromRenewableAndNonRenewableSources>

    <in-capmkt:EnergyIntensityPerRupeeOfTurnover contextRef="DCYMain" decimals="INF" unitRef="GigajoulePerINR">{{ environment_data.energy.intensity_turnover_cy }}</in-capmkt:EnergyIntensityPerRupeeOfTurnover>
    <in-capmkt:EnergyIntensityPerRupeeOfTurnover contextRef="DPYMain" decimals="INF" unitRef="GigajoulePerINR">{{ environment_data.energy.intensity_turnover_py }}</in-capmkt:EnergyIntensityPerRupeeOfTurnover>
    <in-capmkt:EnergyIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity contextRef="DCYMain" decimals="INF" unitRef="GigajoulePerINR">{{ environment_data.energy.intensity_turnover_ppp_cy }}</in-capmkt:EnergyIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity>
    <in-capmkt:EnergyIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity contextRef="DPYMain" decimals="INF" unitRef="GigajoulePerINR">{{ environment_data.energy.intensity_turnover_ppp_py }}</in-capmkt:EnergyIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity>
    <in-capmkt:EnergyIntensityInTermOfPhysicalOutput contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.intensity_physical_cy }}</in-capmkt:EnergyIntensityInTermOfPhysicalOutput>
    <in-capmkt:EnergyIntensityInTermOfPhysicalOutput contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.intensity_physical_py }}</in-capmkt:EnergyIntensityInTermOfPhysicalOutput>
    <in-capmkt:EnergyIntensityTheRelevantMetricMayBeSelectedByTheEntity contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.intensity_optional_cy }}</in-capmkt:EnergyIntensityTheRelevantMetricMayBeSelectedByTheEntity>
    <in-capmkt:EnergyIntensityTheRelevantMetricMayBeSelectedByTheEntity contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.intensity_optional_py }}</in-capmkt:EnergyIntensityTheRelevantMetricMayBeSelectedByTheEntity>
    <in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForEnergyConsumptionUnderLeadershipIndicators contextRef="DCYMain">{{ 'true' if environment_data.energy.external_assessment == 'Yes' else 'false' }}</in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForEnergyConsumptionUnderLeadershipIndicators>
    <in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceForEnergyConsumptionExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.energy.external_agency | e }}</in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceForEnergyConsumptionExplanatoryTextBlock>
    <in-capmkt:DoesTheEntityHaveAnySitesOrFacilitiesIdentifiedAsDesignatedConsumersUnderThePerformanceAchieveAndTradeSchemeOfTheGovernmentOfIndia contextRef="DCYMain">{{ 'true' if environment_data.energy.pat_applicable == 'Yes' else 'false' }}</in-capmkt:DoesTheEntityHaveAnySitesOrFacilitiesIdentifiedAsDesignatedConsumersUnderThePerformanceAchieveAndTradeSchemeOfTheGovernmentOfIndia>
    <in-capmkt:DiscloseWhetherTargetsSetUnderThePatSchemeHaveBeenAchievedInCaseTargetsHaveNotBeenAchievedThenProvideTheRemedialActionTakenExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.energy.pat_details | e }}</in-capmkt:DiscloseWhetherTargetsSetUnderThePatSchemeHaveBeenAchievedInCaseTargetsHaveNotBeenAchievedThenProvideTheRemedialActionTakenExplanatoryTextBlock>
    <in-capmkt:DoesTheEntityHaveAnySitesOrFacilitiesIdentifiedAsLowZeroCarbonEmittingOrEnergyEfficientByAnExternalAgency contextRef="DCYMain">{{ 'true' if environment_data.energy.low_carbon_sites == 'Yes' else 'false' }}</in-capmkt:DoesTheEntityHaveAnySitesOrFacilitiesIdentifiedAsLowZeroCarbonEmittingOrEnergyEfficientByAnExternalAgency>
    <in-capmkt:NameOfTheExternalAgencyThatIdentifiedSiteOrFacilityAsLowZeroCarbonEmittingOrEnergyEfficientExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.energy.low_carbon_details | e }}</in-capmkt:NameOfTheExternalAgencyThatIdentifiedSiteOrFacilityAsLowZeroCarbonEmittingOrEnergyEfficientExplanatoryTextBlock>

    <!-- Water Withdrawal -->
    <in-capmkt:WaterWithdrawalBySurfaceWater contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.surface_cy }}</in-capmkt:WaterWithdrawalBySurfaceWater>
    <in-capmkt:WaterWithdrawalBySurfaceWater contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.surface_py }}</in-capmkt:WaterWithdrawalBySurfaceWater>
    <in-capmkt:WaterWithdrawalByGroundwater contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.groundwater_cy }}</in-capmkt:WaterWithdrawalByGroundwater>
    <in-capmkt:WaterWithdrawalByGroundwater contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.groundwater_py }}</in-capmkt:WaterWithdrawalByGroundwater>
    <in-capmkt:WaterWithdrawalByThirdPartyWater contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.thirdparty_cy }}</in-capmkt:WaterWithdrawalByThirdPartyWater>
    <in-capmkt:WaterWithdrawalByThirdPartyWater contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.thirdparty_py }}</in-capmkt:WaterWithdrawalByThirdPartyWater>
    <in-capmkt:WaterWithdrawalBySeawaterOrDesalinatedWater contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.seawater_cy }}</in-capmkt:WaterWithdrawalBySeawaterOrDesalinatedWater>
    <in-capmkt:WaterWithdrawalBySeawaterOrDesalinatedWater contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.seawater_py }}</in-capmkt:WaterWithdrawalBySeawaterOrDesalinatedWater>
    <in-capmkt:WaterWithdrawalByOthers contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.others_cy }}</in-capmkt:WaterWithdrawalByOthers>
    <in-capmkt:WaterWithdrawalByOthers contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.others_py }}</in-capmkt:WaterWithdrawalByOthers>
    <in-capmkt:TotalVolumeOfWaterWithdrawal contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.total_withdrawal_cy }}</in-capmkt:TotalVolumeOfWaterWithdrawal>
    <in-capmkt:TotalVolumeOfWaterWithdrawal contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.total_withdrawal_py }}</in-capmkt:TotalVolumeOfWaterWithdrawal>

    <!-- Water Withdrawal External Assessment -->
    <in-capmkt:AnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWaterWithdrawal contextRef="DCYMain">{{ 'true' if environment_data.water.external_assessment == 'Yes' else 'false' }}</in-capmkt:AnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWaterWithdrawal>
    <in-capmkt:NameOfTheExternalAgencyInCaseAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWaterWithdrawalExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.water.external_agency | e }}</in-capmkt:NameOfTheExternalAgencyInCaseAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWaterWithdrawalExplanatoryTextBlock>

    <in-capmkt:TotalVolumeOfWaterConsumption contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.total_consumption_cy }}</in-capmkt:TotalVolumeOfWaterConsumption>
    <in-capmkt:TotalVolumeOfWaterConsumption contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.total_consumption_py }}</in-capmkt:TotalVolumeOfWaterConsumption>
    <in-capmkt:WaterIntensityPerRupeeOfTurnover contextRef="DCYMain" decimals="INF" unitRef="KilolitersPerINR">{{ environment_data.water.intensity_turnover_cy }}</in-capmkt:WaterIntensityPerRupeeOfTurnover>
    <in-capmkt:WaterIntensityPerRupeeOfTurnover contextRef="DPYMain" decimals="INF" unitRef="KilolitersPerINR">{{ environment_data.water.intensity_turnover_py }}</in-capmkt:WaterIntensityPerRupeeOfTurnover>
    <in-capmkt:WaterIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity contextRef="DCYMain" decimals="INF" unitRef="KilolitersPerINR">{{ environment_data.water.intensity_turnover_ppp_cy }}</in-capmkt:WaterIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity>
    <in-capmkt:WaterIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity contextRef="DPYMain" decimals="INF" unitRef="KilolitersPerINR">{{ environment_data.water.intensity_turnover_ppp_py }}</in-capmkt:WaterIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity>
    <in-capmkt:WaterIntensityInTermOfPhysicalOutput contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.intensity_physical_cy }}</in-capmkt:WaterIntensityInTermOfPhysicalOutput>
    <in-capmkt:WaterIntensityInTermOfPhysicalOutput contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.intensity_physical_py }}</in-capmkt:WaterIntensityInTermOfPhysicalOutput>
    <in-capmkt:WaterIntensityTheRelevantMetricMayBeSelectedByTheEntity contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.intensity_optional_cy }}</in-capmkt:WaterIntensityTheRelevantMetricMayBeSelectedByTheEntity>
    <in-capmkt:WaterIntensityTheRelevantMetricMayBeSelectedByTheEntity contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.intensity_optional_py }}</in-capmkt:WaterIntensityTheRelevantMetricMayBeSelectedByTheEntity>
    <in-capmkt:HasTheEntityImplementedAMechanismForZeroLiquidDischarge contextRef="DCYMain">{{ environment_data.water.zld }}</in-capmkt:HasTheEntityImplementedAMechanismForZeroLiquidDischarge>
    <in-capmkt:DetailsOfCoverageAndImplementationIfForZeroLiquidDischargeExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.water.zld_details | e }}</in-capmkt:DetailsOfCoverageAndImplementationIfForZeroLiquidDischargeExplanatoryTextBlock>

    <!-- Water Discharge -->
    <in-capmkt:WaterDischargeToSurfaceWater contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_surface_cy }}</in-capmkt:WaterDischargeToSurfaceWater>
    <in-capmkt:WaterDischargeToSurfaceWater contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_surface_py }}</in-capmkt:WaterDischargeToSurfaceWater>
    <in-capmkt:WaterDischargeToSurfaceWaterWithOutTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_surface_no_treatment_cy }}</in-capmkt:WaterDischargeToSurfaceWaterWithOutTreatment>
    <in-capmkt:WaterDischargeToSurfaceWaterWithOutTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_surface_no_treatment_py }}</in-capmkt:WaterDischargeToSurfaceWaterWithOutTreatment>
    <in-capmkt:WaterDischargeToSurfaceWaterWithTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_surface_with_treatment_cy }}</in-capmkt:WaterDischargeToSurfaceWaterWithTreatment>
    <in-capmkt:WaterDischargeToSurfaceWaterWithTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_surface_with_treatment_py }}</in-capmkt:WaterDischargeToSurfaceWaterWithTreatment>
    <in-capmkt:WaterDischargeToGroundwater contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_groundwater_cy }}</in-capmkt:WaterDischargeToGroundwater>
    <in-capmkt:WaterDischargeToGroundwater contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_groundwater_py }}</in-capmkt:WaterDischargeToGroundwater>
    <in-capmkt:WaterDischargeToGroundwaterWithOutTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_groundwater_no_treatment_cy }}</in-capmkt:WaterDischargeToGroundwaterWithOutTreatment>
    <in-capmkt:WaterDischargeToGroundwaterWithOutTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_groundwater_no_treatment_py }}</in-capmkt:WaterDischargeToGroundwaterWithOutTreatment>
    <in-capmkt:WaterDischargeToGroundwaterWithTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_groundwater_with_treatment_cy }}</in-capmkt:WaterDischargeToGroundwaterWithTreatment>
    <in-capmkt:WaterDischargeToGroundwaterWithTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_groundwater_with_treatment_py }}</in-capmkt:WaterDischargeToGroundwaterWithTreatment>
    <in-capmkt:WaterDischargeToSeawater contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_seawater_cy }}</in-capmkt:WaterDischargeToSeawater>
    <in-capmkt:WaterDischargeToSeawater contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_seawater_py }}</in-capmkt:WaterDischargeToSeawater>
    <in-capmkt:WaterDischargeToSeawaterWithOutTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_seawater_no_treatment_cy }}</in-capmkt:WaterDischargeToSeawaterWithOutTreatment>
    <in-capmkt:WaterDischargeToSeawaterWithOutTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_seawater_no_treatment_py }}</in-capmkt:WaterDischargeToSeawaterWithOutTreatment>
    <in-capmkt:WaterDischargeToSeawaterWithTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_seawater_with_treatment_cy }}</in-capmkt:WaterDischargeToSeawaterWithTreatment>
    <in-capmkt:WaterDischargeToSeawaterWithTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_seawater_with_treatment_py }}</in-capmkt:WaterDischargeToSeawaterWithTreatment>
    <in-capmkt:WaterDischargeBySentToThirdParties contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_thirdparty_cy }}</in-capmkt:WaterDischargeBySentToThirdParties>
    <in-capmkt:WaterDischargeBySentToThirdParties contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_thirdparty_py }}</in-capmkt:WaterDischargeBySentToThirdParties>
    <in-capmkt:WaterDischargeBySentToThirdPartiesWithoutTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_thirdparty_no_treatment_cy }}</in-capmkt:WaterDischargeBySentToThirdPartiesWithoutTreatment>
    <in-capmkt:WaterDischargeBySentToThirdPartiesWithoutTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_thirdparty_no_treatment_py }}</in-capmkt:WaterDischargeBySentToThirdPartiesWithoutTreatment>
    <in-capmkt:WaterDischargeBySentToThirdPartiesWithTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_thirdparty_with_treatment_cy }}</in-capmkt:WaterDischargeBySentToThirdPartiesWithTreatment>
    <in-capmkt:WaterDischargeBySentToThirdPartiesWithTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_thirdparty_with_treatment_py }}</in-capmkt:WaterDischargeBySentToThirdPartiesWithTreatment>
    <in-capmkt:WaterDischargeToOthers contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_others_cy }}</in-capmkt:WaterDischargeToOthers>
    <in-capmkt:WaterDischargeToOthers contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_others_py }}</in-capmkt:WaterDischargeToOthers>
    <in-capmkt:WaterDischargeToOthersWithoutTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_others_no_treatment_cy }}</in-capmkt:WaterDischargeToOthersWithoutTreatment>
    <in-capmkt:WaterDischargeToOthersWithoutTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_others_no_treatment_py }}</in-capmkt:WaterDischargeToOthersWithoutTreatment>
    <in-capmkt:WaterDischargeToOthersWithTreatment contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_others_with_treatment_cy }}</in-capmkt:WaterDischargeToOthersWithTreatment>
    <in-capmkt:WaterDischargeToOthersWithTreatment contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.discharge_others_with_treatment_py }}</in-capmkt:WaterDischargeToOthersWithTreatment>
    <in-capmkt:TotalWaterDischargedInKilolitres contextRef="DCYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.total_discharge_cy }}</in-capmkt:TotalWaterDischargedInKilolitres>
    <in-capmkt:TotalWaterDischargedInKilolitres contextRef="DPYMain" decimals="INF" unitRef="Kiloliters">{{ environment_data.water.total_discharge_py }}</in-capmkt:TotalWaterDischargedInKilolitres>
    <in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWaterDischarged contextRef="DCYMain">{{ 'true' if environment_data.water.discharge_external_assessment == 'Yes' else 'false' }}</in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWaterDischarged>
    <in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceForWaterDischargedExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.water.discharge_external_agency | e }}</in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceForWaterDischargedExplanatoryTextBlock>

    <!-- Air Emissions -->
    <in-capmkt:WhetherDetailsOfAirEmissionsOtherThanGhgEmissionsByTheEntityIsApplicableToTheCompany contextRef="DCYMain">true</in-capmkt:WhetherDetailsOfAirEmissionsOtherThanGhgEmissionsByTheEntityIsApplicableToTheCompany>
    <in-capmkt:NOx contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.nox_cy }}</in-capmkt:NOx>
    <in-capmkt:NOx contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.nox_py }}</in-capmkt:NOx>
    <in-capmkt:SOx contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.sox_cy }}</in-capmkt:SOx>
    <in-capmkt:SOx contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.sox_py }}</in-capmkt:SOx>
    <in-capmkt:ParticulateMatter contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.pm_cy }}</in-capmkt:ParticulateMatter>
    <in-capmkt:ParticulateMatter contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.pm_py }}</in-capmkt:ParticulateMatter>
    <in-capmkt:PersistentOrganicPollutants contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.pop_cy }}</in-capmkt:PersistentOrganicPollutants>
    <in-capmkt:PersistentOrganicPollutants contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.pop_py }}</in-capmkt:PersistentOrganicPollutants>
    <in-capmkt:VolatileOrganicCompounds contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.voc_cy }}</in-capmkt:VolatileOrganicCompounds>
    <in-capmkt:VolatileOrganicCompounds contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.voc_py }}</in-capmkt:VolatileOrganicCompounds>
    <in-capmkt:HazardousAirPollutants contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.hap_cy }}</in-capmkt:HazardousAirPollutants>
    <in-capmkt:HazardousAirPollutants contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.air.hap_py }}</in-capmkt:HazardousAirPollutants>
    <in-capmkt:IndicateIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForAirEmissionsOtherThanGHGEmissions contextRef="DCYMain">{{ 'true' if environment_data.air.external_assessment == 'Yes' else 'false' }}</in-capmkt:IndicateIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForAirEmissionsOtherThanGHGEmissions>
    <in-capmkt:NameOfTheExternalAgencyIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForAirEmissionsOtherThanGHGEmissionsExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.air.external_agency | e }}</in-capmkt:NameOfTheExternalAgencyIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForAirEmissionsOtherThanGHGEmissionsExplanatoryTextBlock>

    <!-- GHG Emissions -->
    <in-capmkt:WhetherDetailsOfGreenHouseGasEmissionsAndItsIntensityIsApplicableToTheCompany contextRef="DCYMain">true</in-capmkt:WhetherDetailsOfGreenHouseGasEmissionsAndItsIntensityIsApplicableToTheCompany>
    <in-capmkt:TotalScope1Emissions contextRef="DCYMain" decimals="INF" unitRef="tCO2e">{{ environment_data.ghg.scope1_cy }}</in-capmkt:TotalScope1Emissions>
    <in-capmkt:TotalScope1Emissions contextRef="DPYMain" decimals="INF" unitRef="tCO2e">{{ environment_data.ghg.scope1_py }}</in-capmkt:TotalScope1Emissions>
    <in-capmkt:TotalScope2Emissions contextRef="DCYMain" decimals="INF" unitRef="tCO2e">{{ environment_data.ghg.scope2_cy }}</in-capmkt:TotalScope2Emissions>
    <in-capmkt:TotalScope2Emissions contextRef="DPYMain" decimals="INF" unitRef="tCO2e">{{ environment_data.ghg.scope2_py }}</in-capmkt:TotalScope2Emissions>
    <in-capmkt:TotalScope1AndScope2EmissionsIntensityPerRupeeOfTurnover contextRef="DCYMain" decimals="INF" unitRef="tCO2ePerINR">{{ environment_data.ghg.intensity_turnover_cy }}</in-capmkt:TotalScope1AndScope2EmissionsIntensityPerRupeeOfTurnover>
    <in-capmkt:TotalScope1AndScope2EmissionsIntensityPerRupeeOfTurnover contextRef="DPYMain" decimals="INF" unitRef="tCO2ePerINR">{{ environment_data.ghg.intensity_turnover_py }}</in-capmkt:TotalScope1AndScope2EmissionsIntensityPerRupeeOfTurnover>
    <in-capmkt:TotalScope1AndScope2EmissionsIntensityInTermOfPhysicalOutput contextRef="DCYMain" decimals="INF" unitRef="tCO2e">{{ environment_data.ghg.intensity_physical_cy }}</in-capmkt:TotalScope1AndScope2EmissionsIntensityInTermOfPhysicalOutput>
    <in-capmkt:TotalScope1AndScope2EmissionsIntensityInTermOfPhysicalOutput contextRef="DPYMain" decimals="INF" unitRef="tCO2e">{{ environment_data.ghg.intensity_physical_py }}</in-capmkt:TotalScope1AndScope2EmissionsIntensityInTermOfPhysicalOutput>
    <in-capmkt:TotalScope1AndScope2EmissionsIntensityPerRupeeOfTurnoverAdjustedForPurchasingPowerParity contextRef="DCYMain" decimals="INF" unitRef="tCO2ePerINR">{{ environment_data.ghg.intensity_turnover_ppp_cy }}</in-capmkt:TotalScope1AndScope2EmissionsIntensityPerRupeeOfTurnoverAdjustedForPurchasingPowerParity>
    <in-capmkt:TotalScope1AndScope2EmissionsIntensityPerRupeeOfTurnoverAdjustedForPurchasingPowerParity contextRef="DPYMain" decimals="INF" unitRef="tCO2ePerINR">{{ environment_data.ghg.intensity_turnover_ppp_py }}</in-capmkt:TotalScope1AndScope2EmissionsIntensityPerRupeeOfTurnoverAdjustedForPurchasingPowerParity>
    <in-capmkt:TotalScope1AndScope2EmissionsIntensityTheRelevantMetricMayBeSelectedByTheEntity contextRef="DCYMain" decimals="INF" unitRef="tCO2e">{{ environment_data.ghg.intensity_optional_cy }}</in-capmkt:TotalScope1AndScope2EmissionsIntensityTheRelevantMetricMayBeSelectedByTheEntity>
    <in-capmkt:TotalScope1AndScope2EmissionsIntensityTheRelevantMetricMayBeSelectedByTheEntity contextRef="DPYMain" decimals="INF" unitRef="tCO2e">{{ environment_data.ghg.intensity_optional_py }}</in-capmkt:TotalScope1AndScope2EmissionsIntensityTheRelevantMetricMayBeSelectedByTheEntity>
    <in-capmkt:WhetherAnyIndicateIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForGreenHouseGasEmissions contextRef="DCYMain">{{ 'true' if environment_data.ghg.external_assessment == 'Yes' else 'false' }}</in-capmkt:WhetherAnyIndicateIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForGreenHouseGasEmissions>
    <in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceForGreenHouseGasEmissionsExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.ghg.external_agency | e }}</in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceForGreenHouseGasEmissionsExplanatoryTextBlock>
    <in-capmkt:DoesTheEntityHaveAnyProjectRelatedToReducingGreenHouseGasEmission contextRef="DCYMain">{{ environment_data.ghg.has_reduction_project }}</in-capmkt:DoesTheEntityHaveAnyProjectRelatedToReducingGreenHouseGasEmission>
    <in-capmkt:DetailsOfProjectRelatedToReducingGreenHouseGasEmissionExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.ghg.reduction_project_details | e }}</in-capmkt:DetailsOfProjectRelatedToReducingGreenHouseGasEmissionExplanatoryTextBlock>
    {% if environment_data.ghg.has_reduction_project == 'Not Applicable' %}
    <in-capmkt:ProjectRelatedToReducingGreenHouseGasEmissionIsNotApplicableToTheEntityExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.ghg.reduction_project_na_explanation | e }}</in-capmkt:ProjectRelatedToReducingGreenHouseGasEmissionIsNotApplicableToTheEntityExplanatoryTextBlock>
    {% endif %}

    <!-- Waste -->
    <in-capmkt:PlasticWaste contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.plastic_cy }}</in-capmkt:PlasticWaste>
    <in-capmkt:PlasticWaste contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.plastic_py }}</in-capmkt:PlasticWaste>
    <in-capmkt:EWaste contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.ewaste_cy }}</in-capmkt:EWaste>
    <in-capmkt:EWaste contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.ewaste_py }}</in-capmkt:EWaste>
    <in-capmkt:BioMedicalWaste contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.biomedical_cy }}</in-capmkt:BioMedicalWaste>
    <in-capmkt:BioMedicalWaste contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.biomedical_py }}</in-capmkt:BioMedicalWaste>
    <in-capmkt:ConstructionAndDemolitionWaste contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.construction_cy }}</in-capmkt:ConstructionAndDemolitionWaste>
    <in-capmkt:ConstructionAndDemolitionWaste contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.construction_py }}</in-capmkt:ConstructionAndDemolitionWaste>
    <in-capmkt:BatteryWaste contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.battery_cy }}</in-capmkt:BatteryWaste>
    <in-capmkt:BatteryWaste contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.battery_py }}</in-capmkt:BatteryWaste>
    <in-capmkt:RadioactiveWaste contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.radioactive_cy }}</in-capmkt:RadioactiveWaste>
    <in-capmkt:RadioactiveWaste contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.radioactive_py }}</in-capmkt:RadioactiveWaste>
    <in-capmkt:OtherHazardousWaste contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.other_hazardous_cy }}</in-capmkt:OtherHazardousWaste>
    <in-capmkt:OtherHazardousWaste contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.other_hazardous_py }}</in-capmkt:OtherHazardousWaste>
    <in-capmkt:OtherNonHazardousWasteGenerated contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.other_nonhazardous_cy }}</in-capmkt:OtherNonHazardousWasteGenerated>
    <in-capmkt:OtherNonHazardousWasteGenerated contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.other_nonhazardous_py }}</in-capmkt:OtherNonHazardousWasteGenerated>
    <in-capmkt:TotalWasteGenerated contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.total_cy }}</in-capmkt:TotalWasteGenerated>
    <in-capmkt:TotalWasteGenerated contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.total_py }}</in-capmkt:TotalWasteGenerated>
    <in-capmkt:WasteIntensityPerRupeeOfTurnover contextRef="DCYMain" decimals="INF" unitRef="TonnePerINR">{{ environment_data.waste.intensity_turnover_cy }}</in-capmkt:WasteIntensityPerRupeeOfTurnover>
    <in-capmkt:WasteIntensityPerRupeeOfTurnover contextRef="DPYMain" decimals="INF" unitRef="TonnePerINR">{{ environment_data.waste.intensity_turnover_py }}</in-capmkt:WasteIntensityPerRupeeOfTurnover>
    <in-capmkt:WasteIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity contextRef="DCYMain" decimals="INF" unitRef="TonnePerINR">{{ environment_data.waste.intensity_turnover_ppp_cy }}</in-capmkt:WasteIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity>
    <in-capmkt:WasteIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity contextRef="DPYMain" decimals="INF" unitRef="TonnePerINR">{{ environment_data.waste.intensity_turnover_ppp_py }}</in-capmkt:WasteIntensityPerRupeeOfTurnoverAdjustingForPurchasingPowerParity>
    <in-capmkt:WasteIntensityInTermOfPhysicalOutput contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.intensity_physical_cy }}</in-capmkt:WasteIntensityInTermOfPhysicalOutput>
    <in-capmkt:WasteIntensityInTermOfPhysicalOutput contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.intensity_physical_py }}</in-capmkt:WasteIntensityInTermOfPhysicalOutput>
    <in-capmkt:WasteIntensityTheRelevantMetricMayBeSelectedByTheEntity contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.intensity_optional_cy }}</in-capmkt:WasteIntensityTheRelevantMetricMayBeSelectedByTheEntity>
    <in-capmkt:WasteIntensityTheRelevantMetricMayBeSelectedByTheEntity contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.intensity_optional_py }}</in-capmkt:WasteIntensityTheRelevantMetricMayBeSelectedByTheEntity>

    <!-- Waste Recovery and Disposal -->
    <in-capmkt:WasteRecoveredThroughRecycled contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.recycled_cy }}</in-capmkt:WasteRecoveredThroughRecycled>
    <in-capmkt:WasteRecoveredThroughRecycled contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.recycled_py }}</in-capmkt:WasteRecoveredThroughRecycled>
    <in-capmkt:WasteRecoveredThroughReUsed contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.reused_cy }}</in-capmkt:WasteRecoveredThroughReUsed>
    <in-capmkt:WasteRecoveredThroughReUsed contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.reused_py }}</in-capmkt:WasteRecoveredThroughReUsed>
    <in-capmkt:WasteRecoveredThroughOtherRecoveryOperations contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.other_recovery_cy }}</in-capmkt:WasteRecoveredThroughOtherRecoveryOperations>
    <in-capmkt:WasteRecoveredThroughOtherRecoveryOperations contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.other_recovery_py }}</in-capmkt:WasteRecoveredThroughOtherRecoveryOperations>
    <in-capmkt:TotalWasteRecovered contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.total_recovered_cy }}</in-capmkt:TotalWasteRecovered>
    <in-capmkt:TotalWasteRecovered contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.total_recovered_py }}</in-capmkt:TotalWasteRecovered>
    <in-capmkt:WasteDisposedByIncineration contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.incineration_cy }}</in-capmkt:WasteDisposedByIncineration>
    <in-capmkt:WasteDisposedByIncineration contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.incineration_py }}</in-capmkt:WasteDisposedByIncineration>
    <in-capmkt:WasteDisposedByLandfilling contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.landfill_cy }}</in-capmkt:WasteDisposedByLandfilling>
    <in-capmkt:WasteDisposedByLandfilling contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.landfill_py }}</in-capmkt:WasteDisposedByLandfilling>
    <in-capmkt:WasteDisposedByOtherDisposalOperations contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.other_disposal_cy }}</in-capmkt:WasteDisposedByOtherDisposalOperations>
    <in-capmkt:WasteDisposedByOtherDisposalOperations contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.other_disposal_py }}</in-capmkt:WasteDisposedByOtherDisposalOperations>
    <in-capmkt:TotalWasteDisposed contextRef="DCYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.total_disposed_cy }}</in-capmkt:TotalWasteDisposed>
    <in-capmkt:TotalWasteDisposed contextRef="DPYMain" decimals="INF" unitRef="Tonne">{{ environment_data.waste.total_disposed_py }}</in-capmkt:TotalWasteDisposed>
    <!-- Waste Management External Assessment -->
    <in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWasteManagement contextRef="DCYMain">{{ environment_data.waste.external_assessment }}</in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWasteManagement>
    <in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceRelatedToWasteManagementExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.waste.external_agency | e }}</in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceRelatedToWasteManagementExplanatoryTextBlock>
    <in-capmkt:DetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicalsExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.waste.waste_management_practices | e }}</in-capmkt:DetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicalsExplanatoryTextBlock>

    <!-- Other Environmental -->
    <in-capmkt:IsTheEntityCompliantWithTheApplicableEnvironmentalLaw contextRef="DCYMain">{{ environment_data.environmental_compliance }}</in-capmkt:IsTheEntityCompliantWithTheApplicableEnvironmentalLaw>
    <in-capmkt:IndicateIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForAreasOfWaterStress contextRef="DCYMain">{{ environment_data.water_stress_external_assessment }}</in-capmkt:IndicateIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForAreasOfWaterStress>
    <in-capmkt:WhetherTotalScope3EmissionsAndItsIntensityIsApplicableToTheCompany contextRef="DCYMain">{{ environment_data.scope3_applicable }}</in-capmkt:WhetherTotalScope3EmissionsAndItsIntensityIsApplicableToTheCompany>
    <in-capmkt:DetailsOfSignificantDirectAndIndirectImpactOfTheEntityOnBiodiversityInSuchAreasAlongWithPreventionAndRemediationActivitiesExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.biodiversity_impact | e }}</in-capmkt:DetailsOfSignificantDirectAndIndirectImpactOfTheEntityOnBiodiversityInSuchAreasAlongWithPreventionAndRemediationActivitiesExplanatoryTextBlock>
    <in-capmkt:DoesTheEntityHaveABusinessContinuityAndDisasterManagementPlan contextRef="DCYMain">{{ environment_data.disaster_plan }}</in-capmkt:DoesTheEntityHaveABusinessContinuityAndDisasterManagementPlan>
    <in-capmkt:DisclosureWebLinkOfEntityAtWhichBusinessContinuityAndDisasterManagementPlanIsPlaced contextRef="ICYMain">{{ environment_data.disaster_plan_weblink | e }}</in-capmkt:DisclosureWebLinkOfEntityAtWhichBusinessContinuityAndDisasterManagementPlanIsPlaced>
    <in-capmkt:DiscloseAnySignificantAdverseImpactToTheEnvironmentArisingFromTheValueChainOfTheEntityWhatMitigationOrAdaptationMeasuresHaveBeenTakenByTheEntityInThisRegardExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.value_chain_env_impact | e }}</in-capmkt:DiscloseAnySignificantAdverseImpactToTheEnvironmentArisingFromTheValueChainOfTheEntityWhatMitigationOrAdaptationMeasuresHaveBeenTakenByTheEntityInThisRegardExplanatoryTextBlock>
    <in-capmkt:PercentageOfValueChainPartnersByValueOfBusinessDoneWithSuchPartnersThatWereAssessedForEnvironmentalImpacts contextRef="DCYMain" decimals="INF" unitRef="pure">{{ environment_data.value_chain_env_assessment_pct }}</in-capmkt:PercentageOfValueChainPartnersByValueOfBusinessDoneWithSuchPartnersThatWereAssessedForEnvironmentalImpacts>
    <in-capmkt:NumberOfGreenCreditsHaveBeenGeneratedOrProcuredByTheListedEntity contextRef="DCYMain" decimals="0" unitRef="pure">{{ environment_data.green_credits_entity | int }}</in-capmkt:NumberOfGreenCreditsHaveBeenGeneratedOrProcuredByTheListedEntity>
    <in-capmkt:NumberOfGreenCreditsHaveBeenGeneratedOrProcuredByTheTopTenValueChainPartners contextRef="DCYMain" decimals="0" unitRef="pure">{{ environment_data.green_credits_value_chain | int }}</in-capmkt:NumberOfGreenCreditsHaveBeenGeneratedOrProcuredByTheTopTenValueChainPartners>

    <!-- ==================== PRINCIPLE 4: STAKEHOLDER ENGAGEMENT ==================== -->
    <!-- Process for identifying stakeholders -->
    <in-capmkt:DescribeTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntityExplanatoryTextBlock contextRef="DCYMain">{{ stakeholder_data.identification_process | e }}</in-capmkt:DescribeTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntityExplanatoryTextBlock>

    <!-- Stakeholder Groups -->
    {% for stakeholder in stakeholder_data.stakeholder_groups %}
    <!-- Stakeholder Group {{ loop.index }}: {{ stakeholder.name }} -->
    <in-capmkt:StakeholderGroup contextRef="D_StakeHolderGroups{{ loop.index }}">{{ stakeholder.name }}</in-capmkt:StakeholderGroup>
    <in-capmkt:WhetherIdentifiedAsVulnerableAndMarginalizedGroup contextRef="D_StakeHolderGroups{{ loop.index }}">{{ stakeholder.vulnerable_marginalized }}</in-capmkt:WhetherIdentifiedAsVulnerableAndMarginalizedGroup>
    <in-capmkt:ChannelsOfCommunication contextRef="D_StakeHolderGroups{{ loop.index }}">{{ stakeholder.channels }}</in-capmkt:ChannelsOfCommunication>
    <in-capmkt:DetailsOfOtherChannelsOfCommunication contextRef="D_StakeHolderGroups{{ loop.index }}">{{ stakeholder.channels_details | e }}</in-capmkt:DetailsOfOtherChannelsOfCommunication>
    <in-capmkt:FrequencyOfEngagement contextRef="D_StakeHolderGroups{{ loop.index }}">{{ stakeholder.frequency }}</in-capmkt:FrequencyOfEngagement>
    {% if stakeholder.frequency_details %}
    <in-capmkt:DetailsOfOtherFrequencyOfEngagement contextRef="D_StakeHolderGroups{{ loop.index }}">{{ stakeholder.frequency_details }}</in-capmkt:DetailsOfOtherFrequencyOfEngagement>
    {% endif %}
    <in-capmkt:PurposeAndScopeOfEngagementIncludingKeyTopicsAndConcernsRaisedDuringSuchEngagement contextRef="D_StakeHolderGroups{{ loop.index }}">{{ stakeholder.purpose_scope | e }}</in-capmkt:PurposeAndScopeOfEngagementIncludingKeyTopicsAndConcernsRaisedDuringSuchEngagement>
    {% endfor %}

    <!-- Leadership Indicators -->
    <in-capmkt:ProvideTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoardExplanatoryTextBlock contextRef="DCYMain">{{ stakeholder_data.consultation_process | e }}</in-capmkt:ProvideTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoardExplanatoryTextBlock>
    <in-capmkt:WhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics contextRef="DCYMain">{{ stakeholder_data.stakeholder_consultation_used if stakeholder_data.stakeholder_consultation_used else 'Yes' }}</in-capmkt:WhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics>
    <in-capmkt:DetailsOfInstancesAsToHowTheInputsReceivedFromStakeholdersOnTheseTopicsWereIncorporatedIntoPoliciesAndActivitiesOfTheEntityExplanatoryTextBlock contextRef="DCYMain">{{ stakeholder_data.stakeholder_consultation_details | e if stakeholder_data.stakeholder_consultation_details else '' }}</in-capmkt:DetailsOfInstancesAsToHowTheInputsReceivedFromStakeholdersOnTheseTopicsWereIncorporatedIntoPoliciesAndActivitiesOfTheEntityExplanatoryTextBlock>
    <in-capmkt:ProvideDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableMarginalizedStakeholderGroupsExplanatoryTextBlock contextRef="DCYMain">{{ stakeholder_data.vulnerable_marginalized_actions | e if stakeholder_data.vulnerable_marginalized_actions else 'NA' }}</in-capmkt:ProvideDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableMarginalizedStakeholderGroupsExplanatoryTextBlock>

<!-- ==================== GOVERNANCE, LEADERSHIP AND OVERSIGHT ==================== -->
<!-- 7. Statement by director responsible for business responsibility report -->
<in-capmkt:StatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievementsExplanatoryTextBlock contextRef="DCYMain">{{ governance.director_statement | e }}</in-capmkt:StatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievementsExplanatoryTextBlock>

<!-- 8. Details of highest authority responsible for implementation -->
<in-capmkt:DetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicyExplanatoryTextBlock contextRef="DCYMain">{{ governance.highest_authority | e }}</in-capmkt:DetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicyExplanatoryTextBlock>

<!-- 9. Committee responsible for sustainability-related issues -->
<in-capmkt:DoesTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues contextRef="DCYMain">{{ governance.has_esg_committee }}</in-capmkt:DoesTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues>
<in-capmkt:DetailsOfSpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssuesExplanatoryTextBlock contextRef="DCYMain">{{ governance.esg_committee | e }}</in-capmkt:DetailsOfSpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssuesExplanatoryTextBlock>

<!-- 10. Review undertaken by - Performance against policies -->
{% for p in governance.principles %}
<in-capmkt:PerformanceAgainstAbovePoliciesAndFollowUpActionIndicateWhetherReviewWasUndertakenBy contextRef="D_Principle{{ loop.index }}">{{ p.performance_review_by }}</in-capmkt:PerformanceAgainstAbovePoliciesAndFollowUpActionIndicateWhetherReviewWasUndertakenBy>
{% endfor %}

<!-- 10. Review undertaken by - Compliance with statutory requirements -->
{% for p in governance.principles %}
<in-capmkt:ComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesIndicateWhetherReviewWasUndertakenBy contextRef="D_Principle{{ loop.index }}">{{ p.compliance_review_by }}</in-capmkt:ComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesIndicateWhetherReviewWasUndertakenBy>
{% endfor %}

<!-- 10. Frequency - Performance against policies -->
{% for p in governance.principles %}
<in-capmkt:PerformanceAgainstAbovePoliciesAndFollowUpActionFrequency contextRef="D_Principle{{ loop.index }}">{{ p.performance_frequency }}</in-capmkt:PerformanceAgainstAbovePoliciesAndFollowUpActionFrequency>
{% endfor %}

<!-- 10. Description of Other Frequency - Performance against policies (when frequency is "Any other") -->
{% for p in governance.principles %}
<in-capmkt:DescriptionOfOtherFrequencyForPerformanceAgainstAbovePoliciesAndFollowUpAction contextRef="D_Principle{{ loop.index }}">{{ p.performance_frequency_other }}</in-capmkt:DescriptionOfOtherFrequencyForPerformanceAgainstAbovePoliciesAndFollowUpAction>
{% endfor %}

<!-- 10. Frequency - Compliance with statutory requirements -->
{% for p in governance.principles %}
<in-capmkt:ComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesFrequency contextRef="D_Principle{{ loop.index }}">{{ p.compliance_frequency }}</in-capmkt:ComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesFrequency>
{% endfor %}

<!-- 11. Independent assessment/evaluation by external agency -->
{% for p in governance.principles %}
<in-capmkt:HasTheEntityCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency contextRef="D_Principle{{ loop.index }}">{{ p.independent_assessment }}</in-capmkt:HasTheEntityCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency>
{% endfor %}

<!-- 12. Training and awareness programs -->
<in-capmkt:TotalNumberOfTrainingAndAwarenessProgramsHeld contextRef="D_BoardOfDirectorsSegment" decimals="0" unitRef="pure">{{ training.board_of_directors.count }}</in-capmkt:TotalNumberOfTrainingAndAwarenessProgramsHeld>
<in-capmkt:TopicsOrPrinciplesCoveredUnderTheTrainingAndItsImpact contextRef="D_BoardOfDirectorsSegment">{{ training.board_of_directors.topics }}</in-capmkt:TopicsOrPrinciplesCoveredUnderTheTrainingAndItsImpact>
<in-capmkt:PercentageOfPersonsInRespectiveCategoryCoveredByTheAwarenessProgrammes contextRef="D_BoardOfDirectorsSegment" decimals="INF" unitRef="pure">{{ training.board_of_directors.coverage }}</in-capmkt:PercentageOfPersonsInRespectiveCategoryCoveredByTheAwarenessProgrammes>

<in-capmkt:TotalNumberOfTrainingAndAwarenessProgramsHeld contextRef="D_KeyManagerialPersonnelSegment" decimals="0" unitRef="pure">{{ training.kmp.count }}</in-capmkt:TotalNumberOfTrainingAndAwarenessProgramsHeld>
<in-capmkt:TopicsOrPrinciplesCoveredUnderTheTrainingAndItsImpact contextRef="D_KeyManagerialPersonnelSegment">{{ training.kmp.topics }}</in-capmkt:TopicsOrPrinciplesCoveredUnderTheTrainingAndItsImpact>
<in-capmkt:PercentageOfPersonsInRespectiveCategoryCoveredByTheAwarenessProgrammes contextRef="D_KeyManagerialPersonnelSegment" decimals="INF" unitRef="pure">{{ training.kmp.coverage }}</in-capmkt:PercentageOfPersonsInRespectiveCategoryCoveredByTheAwarenessProgrammes>

<in-capmkt:TotalNumberOfTrainingAndAwarenessProgramsHeld contextRef="D_EmployeesOtherThanBoDAndKMPsSegment" decimals="0" unitRef="pure">{{ training.employees.count }}</in-capmkt:TotalNumberOfTrainingAndAwarenessProgramsHeld>
<in-capmkt:TopicsOrPrinciplesCoveredUnderTheTrainingAndItsImpact contextRef="D_EmployeesOtherThanBoDAndKMPsSegment">{{ training.employees.topics }}</in-capmkt:TopicsOrPrinciplesCoveredUnderTheTrainingAndItsImpact>
<in-capmkt:PercentageOfPersonsInRespectiveCategoryCoveredByTheAwarenessProgrammes contextRef="D_EmployeesOtherThanBoDAndKMPsSegment" decimals="INF" unitRef="pure">{{ training.employees.coverage }}</in-capmkt:PercentageOfPersonsInRespectiveCategoryCoveredByTheAwarenessProgrammes>

<in-capmkt:TotalNumberOfTrainingAndAwarenessProgramsHeld contextRef="D_WorkersSegment" decimals="0" unitRef="pure">{{ training.workers.count }}</in-capmkt:TotalNumberOfTrainingAndAwarenessProgramsHeld>
<in-capmkt:TopicsOrPrinciplesCoveredUnderTheTrainingAndItsImpact contextRef="D_WorkersSegment">{{ training.workers.topics }}</in-capmkt:TopicsOrPrinciplesCoveredUnderTheTrainingAndItsImpact>
<in-capmkt:PercentageOfPersonsInRespectiveCategoryCoveredByTheAwarenessProgrammes contextRef="D_WorkersSegment" decimals="INF" unitRef="pure">{{ training.workers.coverage }}</in-capmkt:PercentageOfPersonsInRespectiveCategoryCoveredByTheAwarenessProgrammes>

<!-- ==================== FINES / PENALTIES / PUNISHMENT / SETTLEMENT ==================== -->
<!-- Penalty/Fine -->
<in-capmkt:NGRBCPrincipleForPenaltyOrFine contextRef="D_PenaltyOrFine1">{{ fines_penalties.penalty_fine.ngrbc }}</in-capmkt:NGRBCPrincipleForPenaltyOrFine>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForPenaltyOrFine contextRef="D_PenaltyOrFine1">{{ fines_penalties.penalty_fine.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForPenaltyOrFine>
<in-capmkt:AmountOfFinesOrPenalties contextRef="D_PenaltyOrFine1" decimals="0" unitRef="INR">{{ fines_penalties.penalty_fine.amount }}</in-capmkt:AmountOfFinesOrPenalties>
<in-capmkt:BriefOfTheMonetaryCaseForPenaltyOrFineExplanatoryTextBlock contextRef="D_PenaltyOrFine1">{{ fines_penalties.penalty_fine.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForPenaltyOrFineExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForPenaltyOrFine contextRef="D_PenaltyOrFine1">{{ fines_penalties.penalty_fine.appeal }}</in-capmkt:HasAnAppealBeenPreferredForPenaltyOrFine>

<!-- Settlement -->
<in-capmkt:NGRBCPrincipleForSettlement contextRef="D_Settlement1">{{ fines_penalties.settlement.ngrbc }}</in-capmkt:NGRBCPrincipleForSettlement>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForSettlement contextRef="D_Settlement1">{{ fines_penalties.settlement.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForSettlement>
<in-capmkt:AmountOfSettlement contextRef="D_Settlement1" decimals="0" unitRef="INR">{{ fines_penalties.settlement.amount }}</in-capmkt:AmountOfSettlement>
<in-capmkt:BriefOfTheMonetaryCaseForSettlementExplanatoryTextBlock contextRef="D_Settlement1">{{ fines_penalties.settlement.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForSettlementExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForSettlement contextRef="D_Settlement1">{{ fines_penalties.settlement.appeal }}</in-capmkt:HasAnAppealBeenPreferredForSettlement>

<!-- Compounding Fee -->
<in-capmkt:NGRBCPrincipleForCompoundingFee contextRef="D_Compounding1">{{ fines_penalties.compounding.ngrbc }}</in-capmkt:NGRBCPrincipleForCompoundingFee>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForCompoundingFee contextRef="D_Compounding1">{{ fines_penalties.compounding.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForCompoundingFee>
<in-capmkt:AmountOfCompoundingFee contextRef="D_Compounding1" decimals="0" unitRef="INR">{{ fines_penalties.compounding.amount }}</in-capmkt:AmountOfCompoundingFee>
<in-capmkt:BriefOfTheMonetaryCaseForCompoundingFeeExplanatoryTextBlock contextRef="D_Compounding1">{{ fines_penalties.compounding.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForCompoundingFeeExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForCompoundingFee contextRef="D_Compounding1">{{ fines_penalties.compounding.appeal }}</in-capmkt:HasAnAppealBeenPreferredForCompoundingFee>

<!-- Imprisonment -->
<in-capmkt:NGRBCPrincipleForImprisonment contextRef="D_Imprisonment1">{{ fines_penalties.imprisonment.ngrbc }}</in-capmkt:NGRBCPrincipleForImprisonment>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForImprisonment contextRef="D_Imprisonment1">{{ fines_penalties.imprisonment.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForImprisonment>
<in-capmkt:BriefOfTheMonetaryCaseForImprisonmentExplanatoryTextBlock contextRef="D_Imprisonment1">{{ fines_penalties.imprisonment.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForImprisonmentExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForImprisonment contextRef="D_Imprisonment1">{{ fines_penalties.imprisonment.appeal }}</in-capmkt:HasAnAppealBeenPreferredForImprisonment>

<!-- Punishment -->
<in-capmkt:NGRBCPrincipleForPunishment contextRef="D_Punishment1">{{ fines_penalties.punishment.ngrbc }}</in-capmkt:NGRBCPrincipleForPunishment>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForPunishment contextRef="D_Punishment1">{{ fines_penalties.punishment.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForPunishment>
<in-capmkt:BriefOfTheMonetaryCaseForPunishmentExplanatoryTextBlock contextRef="D_Punishment1">{{ fines_penalties.punishment.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForPunishmentExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForPunishment contextRef="D_Punishment1">{{ fines_penalties.punishment.appeal }}</in-capmkt:HasAnAppealBeenPreferredForPunishment>

<!-- Appeal/Revision -->
<in-capmkt:DetailsOfTheCase contextRef="D_AppealOrRevision1">{{ fines_penalties.appeal_revision.details }}</in-capmkt:DetailsOfTheCase>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutions contextRef="D_AppealOrRevision1">{{ fines_penalties.appeal_revision.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutions>

<!-- Anti-Corruption/Anti-Bribery Policy (Principle 1 Q4) -->
<in-capmkt:DoesTheEntityHaveAnAntiCorruptionOrAntiBriberyPolicy contextRef="DCYMain">{{ fines_penalties.anti_corruption.has_policy }}</in-capmkt:DoesTheEntityHaveAnAntiCorruptionOrAntiBriberyPolicy>
<in-capmkt:AntiCorruptionOrAntiBriberyPolicyExplanatoryTextBlock contextRef="DCYMain">{{ fines_penalties.anti_corruption.policy_details | e }}</in-capmkt:AntiCorruptionOrAntiBriberyPolicyExplanatoryTextBlock>
<in-capmkt:WebLinkAtAntiCorruptionOrAntiBriberyPolicyIsPlace contextRef="ICYMain">{{ fines_penalties.anti_corruption.web_link }}</in-capmkt:WebLinkAtAntiCorruptionOrAntiBriberyPolicyIsPlace>

<!-- Disciplinary Actions -->
<in-capmkt:NumberOfDirectorsAgainstWhomDisciplinaryActionWasTaken contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_cy.directors }}</in-capmkt:NumberOfDirectorsAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfDirectorsAgainstWhomDisciplinaryActionWasTaken contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_py.directors }}</in-capmkt:NumberOfDirectorsAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfKMPsAgainstWhomDisciplinaryActionWasTaken contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_cy.kmps }}</in-capmkt:NumberOfKMPsAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfKMPsAgainstWhomDisciplinaryActionWasTaken contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_py.kmps }}</in-capmkt:NumberOfKMPsAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfEmployeesAgainstWhomDisciplinaryActionWasTaken contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_cy.employees }}</in-capmkt:NumberOfEmployeesAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfEmployeesAgainstWhomDisciplinaryActionWasTaken contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_py.employees }}</in-capmkt:NumberOfEmployeesAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfWorkersAgainstWhomDisciplinaryActionWasTaken contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_cy.workers }}</in-capmkt:NumberOfWorkersAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfWorkersAgainstWhomDisciplinaryActionWasTaken contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_py.workers }}</in-capmkt:NumberOfWorkersAgainstWhomDisciplinaryActionWasTaken>

<!-- Conflict of Interest Complaints -->
<in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.conflict_directors_cy.number }}</in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors>
<in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors contextRef="DCYMain">{{ fines_penalties.conflict_directors_cy.remarks }}</in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors>
<in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.conflict_directors_py.number }}</in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors>
<in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors contextRef="DPYMain">{{ fines_penalties.conflict_directors_py.remarks }}</in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors>
<in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKMPs contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.conflict_kmps_cy.number }}</in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKMPs>
<in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKmps contextRef="DCYMain">{{ fines_penalties.conflict_kmps_cy.remarks }}</in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKmps>
<in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKMPs contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.conflict_kmps_py.number }}</in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKMPs>
<in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKmps contextRef="DPYMain">{{ fines_penalties.conflict_kmps_py.remarks }}</in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKmps>

<!-- Corrective Action -->
<in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterestExplanatoryTextBlock contextRef="DCYMain">{{ fines_penalties.corrective_action }}</in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterestExplanatoryTextBlock>

<!-- Conflict of Interest Management Process -->
<in-capmkt:DoesTheEntityHaveProcessesInPlaceToAvoidOrManageConflictOfInterestsInvolvingMembersOfTheBoard contextRef="DCYMain">{{ fines_penalties.conflict_process.has_process }}</in-capmkt:DoesTheEntityHaveProcessesInPlaceToAvoidOrManageConflictOfInterestsInvolvingMembersOfTheBoard>
<in-capmkt:DetailsOfTheEntityHaveProcessesInPlaceToAvoidOrManageConflictOfInterestsInvolvingMembersOfTheBoardExplanatoryTextBlock contextRef="DCYMain">{{ fines_penalties.conflict_process.details | e }}</in-capmkt:DetailsOfTheEntityHaveProcessesInPlaceToAvoidOrManageConflictOfInterestsInvolvingMembersOfTheBoardExplanatoryTextBlock>

<!-- ==================== SUSTAINABILITY DATA ==================== -->
<!-- Value Chain Partner Awareness -->
<in-capmkt:TotalNumberOfAwarenessProgrammesHeld contextRef="D_AwarenessProgrammesConductedForValueChainPartners1" decimals="0" unitRef="pure">{{ sustainability.value_chain_awareness.count }}</in-capmkt:TotalNumberOfAwarenessProgrammesHeld>
<in-capmkt:TopicsOrPrinciplesCoveredUnderTheTraining contextRef="D_AwarenessProgrammesConductedForValueChainPartners1">{{ sustainability.value_chain_awareness.topics | e }}</in-capmkt:TopicsOrPrinciplesCoveredUnderTheTraining>
<in-capmkt:PercentageOfValueChainPartnersCoveredUnderTheAwarenessProgrammes contextRef="D_AwarenessProgrammesConductedForValueChainPartners1" decimals="INF" unitRef="pure">{{ sustainability.value_chain_awareness.coverage }}</in-capmkt:PercentageOfValueChainPartnersCoveredUnderTheAwarenessProgrammes>

<!-- R&D Percentage -->
<in-capmkt:PercentageOfRAndD contextRef="DCYMain" decimals="INF" unitRef="pure">{{ sustainability.rd_cy }}</in-capmkt:PercentageOfRAndD>
<in-capmkt:PercentageOfRAndD contextRef="DPYMain" decimals="INF" unitRef="pure">{{ sustainability.rd_py }}</in-capmkt:PercentageOfRAndD>
<in-capmkt:DetailsOfImprovementsInEnvironmentalAndSocialImpactsDueToRAndD contextRef="DCYMain">{{ sustainability.rd_improvements | e }}</in-capmkt:DetailsOfImprovementsInEnvironmentalAndSocialImpactsDueToRAndD>

<!-- Capex Percentage -->
<in-capmkt:PercentageOfCapex contextRef="DCYMain" decimals="INF" unitRef="pure">{{ sustainability.capex_cy }}</in-capmkt:PercentageOfCapex>
<in-capmkt:PercentageOfCapex contextRef="DPYMain" decimals="INF" unitRef="pure">{{ sustainability.capex_py }}</in-capmkt:PercentageOfCapex>
<in-capmkt:DetailsOfImprovementsInEnvironmentalAndSocialImpactsDueToCapex contextRef="DCYMain">{{ sustainability.capex_improvements | e }}</in-capmkt:DetailsOfImprovementsInEnvironmentalAndSocialImpactsDueToCapex>

<!-- Sustainable Sourcing -->
<in-capmkt:DoesTheEntityHaveProceduresInPlaceForSustainableSourcing contextRef="DCYMain">{{ sustainability.has_sustainable_sourcing }}</in-capmkt:DoesTheEntityHaveProceduresInPlaceForSustainableSourcing>
<in-capmkt:PercentageOfInputsWereSourcedSustainably contextRef="DCYMain" decimals="INF" unitRef="pure">{{ sustainability.sustainable_sourcing_pct }}</in-capmkt:PercentageOfInputsWereSourcedSustainably>

<!-- End of Life Processes -->
<in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingExplanatoryTextBlock contextRef="DCYMain">{{ sustainability.eol_plastics | e }}</in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingExplanatoryTextBlock>
<in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForEWasteExplanatoryTextBlock contextRef="DCYMain">{{ sustainability.eol_ewaste | e }}</in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForEWasteExplanatoryTextBlock>
<in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForHazardousWasteExplanatoryTextBlock contextRef="DCYMain">{{ sustainability.eol_hazardous | e }}</in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForHazardousWasteExplanatoryTextBlock>
<in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForOtherWasteExplanatoryTextBlock contextRef="DCYMain">{{ sustainability.eol_other | e }}</in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForOtherWasteExplanatoryTextBlock>

<!-- Extended Producer Responsibility -->
<in-capmkt:WhetherExtendedProducerResponsibilityIsApplicableToTheEntitySActivities contextRef="DCYMain">{{ sustainability.epr_applicable }}</in-capmkt:WhetherExtendedProducerResponsibilityIsApplicableToTheEntitySActivities>
<in-capmkt:WhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoards contextRef="DCYMain">{{ sustainability.epr_waste_plan_aligned }}</in-capmkt:WhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoards>

<!-- Life Cycle Assessment -->
<in-capmkt:HasTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices contextRef="DCYMain">{{ sustainability.has_lca }}</in-capmkt:HasTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices>

<!-- Product/Service Risks -->
{% for product in sustainability.product_risks %}
<in-capmkt:NameOfProductOrService contextRef="D_ProductOrService1">{{ product.name }}</in-capmkt:NameOfProductOrService>
<in-capmkt:DescriptionOfTheRiskOrConcern contextRef="D_ProductOrService1">{{ product.description | e }}</in-capmkt:DescriptionOfTheRiskOrConcern>
<in-capmkt:ActionTaken contextRef="D_ProductOrService1">{{ product.action | e }}</in-capmkt:ActionTaken>
{% endfor %}

<!-- Recycled/Reused Input Materials -->
<in-capmkt:IndicateInPutMaterial contextRef="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices1">{{ sustainability.recycled_input_cy.material }}</in-capmkt:IndicateInPutMaterial>
<in-capmkt:RecycledOrReUsedInPutMaterialToTotalMaterial contextRef="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices1" decimals="INF" unitRef="pure">{{ sustainability.recycled_input_cy.percentage }}</in-capmkt:RecycledOrReUsedInPutMaterialToTotalMaterial>
<in-capmkt:IndicateInPutMaterial contextRef="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices_PY1">{{ sustainability.recycled_input_py.material }}</in-capmkt:IndicateInPutMaterial>
<in-capmkt:RecycledOrReUsedInPutMaterialToTotalMaterial contextRef="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices_PY1" decimals="INF" unitRef="pure">{{ sustainability.recycled_input_py.percentage }}</in-capmkt:RecycledOrReUsedInPutMaterialToTotalMaterial>

<!-- Waste Reclamation - Plastics -->
<in-capmkt:AmountOfReUsed contextRef="D_PlasticsIncludingPackaging" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_cy.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_PlasticsIncludingPackaging" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_cy.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_PlasticsIncludingPackaging" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_cy.disposed }}</in-capmkt:AmountOfSafelyDisposed>
<in-capmkt:AmountOfReUsed contextRef="D_PlasticsIncludingPackaging_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_py.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_PlasticsIncludingPackaging_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_py.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_PlasticsIncludingPackaging_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_py.disposed }}</in-capmkt:AmountOfSafelyDisposed>

<!-- Waste Reclamation - E-Waste -->
<in-capmkt:AmountOfReUsed contextRef="D_EWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_cy.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_EWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_cy.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_EWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_cy.disposed }}</in-capmkt:AmountOfSafelyDisposed>
<in-capmkt:AmountOfReUsed contextRef="D_EWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_py.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_EWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_py.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_EWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_py.disposed }}</in-capmkt:AmountOfSafelyDisposed>

<!-- Waste Reclamation - Hazardous -->
<in-capmkt:AmountOfReUsed contextRef="D_HazardousWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_cy.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_HazardousWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_cy.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_HazardousWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_cy.disposed }}</in-capmkt:AmountOfSafelyDisposed>
<in-capmkt:AmountOfReUsed contextRef="D_HazardousWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_py.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_HazardousWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_py.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_HazardousWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_py.disposed }}</in-capmkt:AmountOfSafelyDisposed>

<!-- Waste Reclamation - Other Waste -->
<in-capmkt:NameOfOtherWaste contextRef="D_OtherWaste1">{{ sustainability.waste_other_cy.name }}</in-capmkt:NameOfOtherWaste>
<in-capmkt:AmountOfReUsed contextRef="D_OtherWaste1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_cy.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_OtherWaste1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_cy.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_OtherWaste1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_cy.disposed }}</in-capmkt:AmountOfSafelyDisposed>
<in-capmkt:NameOfOtherWaste contextRef="D_OtherWaste_PY1">{{ sustainability.waste_other_py.name }}</in-capmkt:NameOfOtherWaste>
<in-capmkt:AmountOfReUsed contextRef="D_OtherWaste_PY1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_py.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_OtherWaste_PY1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_py.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_OtherWaste_PY1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_py.disposed }}</in-capmkt:AmountOfSafelyDisposed>

<!-- Reclaimed Products and Packaging Materials -->
{% for product in sustainability.reclaimed_products %}
<in-capmkt:IndicateProductCategory contextRef="D_ReclaimedProductsAndTheirPackaging{{ loop.index }}">{{ product.category | e }}</in-capmkt:IndicateProductCategory>
<in-capmkt:ReclaimedProductsAndTheirPackagingMaterialsAsPercentageOfTotalProductsSoldInRespectiveCategory contextRef="D_ReclaimedProductsAndTheirPackaging{{ loop.index }}" decimals="INF" unitRef="pure">{{ product.percentage }}</in-capmkt:ReclaimedProductsAndTheirPackagingMaterialsAsPercentageOfTotalProductsSoldInRespectiveCategory>
{% endfor %}

<!-- ==================== ACCOUNTS PAYABLE & CONCENTRATION DATA ==================== -->
<!-- Accounts Payable -->
<in-capmkt:AmountOfAccountsPayableDuringTheYear contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.accounts_payable_cy }}</in-capmkt:AmountOfAccountsPayableDuringTheYear>
<in-capmkt:AmountOfAccountsPayableDuringTheYear contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.accounts_payable_py }}</in-capmkt:AmountOfAccountsPayableDuringTheYear>
<in-capmkt:CostOfGoodsOrServicesProcuredDuringTheYear contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.cost_of_goods_cy }}</in-capmkt:CostOfGoodsOrServicesProcuredDuringTheYear>
<in-capmkt:CostOfGoodsOrServicesProcuredDuringTheYear contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.cost_of_goods_py }}</in-capmkt:CostOfGoodsOrServicesProcuredDuringTheYear>
<in-capmkt:NumberOfDaysOfAccountsPayable contextRef="DCYMain">{{ accounts_data.days_payable_cy }}</in-capmkt:NumberOfDaysOfAccountsPayable>
<in-capmkt:NumberOfDaysOfAccountsPayable contextRef="DPYMain">{{ accounts_data.days_payable_py }}</in-capmkt:NumberOfDaysOfAccountsPayable>

<!-- Concentration of Purchases - Trading Houses -->
<in-capmkt:AmountOfPurchasesFromTradingHouses contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.trading_purchases_cy }}</in-capmkt:AmountOfPurchasesFromTradingHouses>
<in-capmkt:AmountOfPurchasesFromTradingHouses contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.trading_purchases_py }}</in-capmkt:AmountOfPurchasesFromTradingHouses>
<in-capmkt:AmountOfTotalPurchases contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.total_purchases_cy }}</in-capmkt:AmountOfTotalPurchases>
<in-capmkt:AmountOfTotalPurchases contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.total_purchases_py }}</in-capmkt:AmountOfTotalPurchases>
<in-capmkt:PercentageOfPurchasesFromTradingHousesInTotalPurchasesForConcentrationOfPurchases contextRef="DCYMain" decimals="INF" unitRef="pure">{{ accounts_data.trading_purchases_pct_cy }}</in-capmkt:PercentageOfPurchasesFromTradingHousesInTotalPurchasesForConcentrationOfPurchases>
<in-capmkt:PercentageOfPurchasesFromTradingHousesInTotalPurchasesForConcentrationOfPurchases contextRef="DPYMain" decimals="INF" unitRef="pure">{{ accounts_data.trading_purchases_pct_py }}</in-capmkt:PercentageOfPurchasesFromTradingHousesInTotalPurchasesForConcentrationOfPurchases>
<in-capmkt:NumberOfTradingHousesWherePurchasesAreMade contextRef="DCYMain" decimals="0" unitRef="pure">{{ accounts_data.num_trading_houses_cy }}</in-capmkt:NumberOfTradingHousesWherePurchasesAreMade>
<in-capmkt:NumberOfTradingHousesWherePurchasesAreMade contextRef="DPYMain" decimals="0" unitRef="pure">{{ accounts_data.num_trading_houses_py }}</in-capmkt:NumberOfTradingHousesWherePurchasesAreMade>
<in-capmkt:AmountOfPurchasesFromTopTenTradingHouses contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.top10_trading_purchases_cy }}</in-capmkt:AmountOfPurchasesFromTopTenTradingHouses>
<in-capmkt:AmountOfPurchasesFromTopTenTradingHouses contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.top10_trading_purchases_py }}</in-capmkt:AmountOfPurchasesFromTopTenTradingHouses>
<in-capmkt:AmountOfTotalPurchasesFromTradingHouses contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.total_trading_purchases_cy }}</in-capmkt:AmountOfTotalPurchasesFromTradingHouses>
<in-capmkt:AmountOfTotalPurchasesFromTradingHouses contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.total_trading_purchases_py }}</in-capmkt:AmountOfTotalPurchasesFromTradingHouses>
<in-capmkt:PercentageOfPurchasesFromTopTenTradingHousesInTotalPurchasesFromTradingHouses contextRef="DCYMain" decimals="INF" unitRef="pure">{{ accounts_data.top10_trading_pct_cy }}</in-capmkt:PercentageOfPurchasesFromTopTenTradingHousesInTotalPurchasesFromTradingHouses>
<in-capmkt:PercentageOfPurchasesFromTopTenTradingHousesInTotalPurchasesFromTradingHouses contextRef="DPYMain" decimals="INF" unitRef="pure">{{ accounts_data.top10_trading_pct_py }}</in-capmkt:PercentageOfPurchasesFromTopTenTradingHousesInTotalPurchasesFromTradingHouses>

<!-- Concentration of Sales - Dealers/Distributors -->
<in-capmkt:AmountOfSalesToDealersOrDistributors contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.dealer_sales_cy }}</in-capmkt:AmountOfSalesToDealersOrDistributors>
<in-capmkt:AmountOfSalesToDealersOrDistributors contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.dealer_sales_py }}</in-capmkt:AmountOfSalesToDealersOrDistributors>
<in-capmkt:AmountOfTotalSales contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.total_sales_cy }}</in-capmkt:AmountOfTotalSales>
<in-capmkt:AmountOfTotalSales contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.total_sales_py }}</in-capmkt:AmountOfTotalSales>
<in-capmkt:PercentageOfSalesToDealersOrDistributorsInTotalSales contextRef="DCYMain" decimals="INF" unitRef="pure">{{ accounts_data.dealer_sales_pct_cy }}</in-capmkt:PercentageOfSalesToDealersOrDistributorsInTotalSales>
<in-capmkt:PercentageOfSalesToDealersOrDistributorsInTotalSales contextRef="DPYMain" decimals="INF" unitRef="pure">{{ accounts_data.dealer_sales_pct_py }}</in-capmkt:PercentageOfSalesToDealersOrDistributorsInTotalSales>
<in-capmkt:NumberOfDealersOrDistributorsToWhomSalesAreMade contextRef="DCYMain" decimals="0" unitRef="pure">{{ accounts_data.num_dealers_cy }}</in-capmkt:NumberOfDealersOrDistributorsToWhomSalesAreMade>
<in-capmkt:NumberOfDealersOrDistributorsToWhomSalesAreMade contextRef="DPYMain" decimals="0" unitRef="pure">{{ accounts_data.num_dealers_py }}</in-capmkt:NumberOfDealersOrDistributorsToWhomSalesAreMade>
<in-capmkt:AmountOfSalesToTopTenDealersOrDistributors contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.top10_dealer_sales_cy }}</in-capmkt:AmountOfSalesToTopTenDealersOrDistributors>
<in-capmkt:AmountOfSalesToTopTenDealersOrDistributors contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.top10_dealer_sales_py }}</in-capmkt:AmountOfSalesToTopTenDealersOrDistributors>
<in-capmkt:AmountOfTotalSalesToDealersOrDistributors contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.total_dealer_sales_cy }}</in-capmkt:AmountOfTotalSalesToDealersOrDistributors>
<in-capmkt:AmountOfTotalSalesToDealersOrDistributors contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.total_dealer_sales_py }}</in-capmkt:AmountOfTotalSalesToDealersOrDistributors>
<in-capmkt:PercentageOfSalesToTopTenDealersOrDistributorsInTotalSalesToDealersOrDistributors contextRef="DCYMain" decimals="INF" unitRef="pure">{{ accounts_data.top10_dealer_pct_cy }}</in-capmkt:PercentageOfSalesToTopTenDealersOrDistributorsInTotalSalesToDealersOrDistributors>
<in-capmkt:PercentageOfSalesToTopTenDealersOrDistributorsInTotalSalesToDealersOrDistributors contextRef="DPYMain" decimals="INF" unitRef="pure">{{ accounts_data.top10_dealer_pct_py }}</in-capmkt:PercentageOfSalesToTopTenDealersOrDistributorsInTotalSalesToDealersOrDistributors>

<!-- Related Party Transactions -->
<in-capmkt:AmountOfPurchasesFromRelatedParties contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_purchases_cy }}</in-capmkt:AmountOfPurchasesFromRelatedParties>
<in-capmkt:AmountOfPurchasesFromRelatedParties contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_purchases_py }}</in-capmkt:AmountOfPurchasesFromRelatedParties>
<in-capmkt:AmountOfTotalPurchasesForShareOfRelatedPartyTransactions contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_total_purchases_cy }}</in-capmkt:AmountOfTotalPurchasesForShareOfRelatedPartyTransactions>
<in-capmkt:AmountOfTotalPurchasesForShareOfRelatedPartyTransactions contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_total_purchases_py }}</in-capmkt:AmountOfTotalPurchasesForShareOfRelatedPartyTransactions>
<in-capmkt:AmountOfSalesToRelatedParties contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_sales_cy }}</in-capmkt:AmountOfSalesToRelatedParties>
<in-capmkt:AmountOfSalesToRelatedParties contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_sales_py }}</in-capmkt:AmountOfSalesToRelatedParties>
<in-capmkt:AmountOfTotalSalesForShareOfRelatedPartyTransactions contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_total_sales_cy }}</in-capmkt:AmountOfTotalSalesForShareOfRelatedPartyTransactions>
<in-capmkt:AmountOfTotalSalesForShareOfRelatedPartyTransactions contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_total_sales_py }}</in-capmkt:AmountOfTotalSalesForShareOfRelatedPartyTransactions>
<in-capmkt:AmountOfLoansAndAdvancesGivenToRelatedParties contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_loans_cy }}</in-capmkt:AmountOfLoansAndAdvancesGivenToRelatedParties>
<in-capmkt:AmountOfLoansAndAdvancesGivenToRelatedParties contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_loans_py }}</in-capmkt:AmountOfLoansAndAdvancesGivenToRelatedParties>
<in-capmkt:AmountOfTotalLoansAndAdvances contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_total_loans_cy }}</in-capmkt:AmountOfTotalLoansAndAdvances>
<in-capmkt:AmountOfTotalLoansAndAdvances contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_total_loans_py }}</in-capmkt:AmountOfTotalLoansAndAdvances>
<in-capmkt:AmountOfInvestmentsInRelatedParties contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_investments_cy }}</in-capmkt:AmountOfInvestmentsInRelatedParties>
<in-capmkt:AmountOfInvestmentsInRelatedParties contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_investments_py }}</in-capmkt:AmountOfInvestmentsInRelatedParties>
<in-capmkt:AmountOfTotalInvestments contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_total_investments_cy }}</in-capmkt:AmountOfTotalInvestments>
<in-capmkt:AmountOfTotalInvestments contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.rpt_total_investments_py }}</in-capmkt:AmountOfTotalInvestments>








{% endfor %}

<!-- VII. Transparency and Disclosures - Complaints/Grievances -->
{% for complaint in complaints %}
<!-- {{ complaint.stakeholder }} -->
<in-capmkt:GrievanceRedressalMechanismInPlace contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}">{{ complaint.has_mechanism }}</in-capmkt:GrievanceRedressalMechanismInPlace>
<in-capmkt:WebLinkForGrievanceRedressPolicy contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}">{{ complaint.web_link if complaint.web_link else '0' }}</in-capmkt:WebLinkForGrievanceRedressPolicy>
<in-capmkt:NumberOfComplaintsFiledFromStakeHolderGroupDuringTheYear contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}" decimals="0" unitRef="pure">{{ complaint.filed_cy|int }}</in-capmkt:NumberOfComplaintsFiledFromStakeHolderGroupDuringTheYear>
<in-capmkt:NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear contextRef="I_ComplaintReceivedFrom{{ complaint.stakeholder }}" decimals="0" unitRef="pure">{{ complaint.pending_cy|int }}</in-capmkt:NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear>
<in-capmkt:RemarksStakeHolderGroupFromWhomComplaintIsReceived contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}">{{ complaint.remarks_cy if complaint.remarks_cy else '0' }}</in-capmkt:RemarksStakeHolderGroupFromWhomComplaintIsReceived>
<in-capmkt:NumberOfComplaintsFiledFromStakeHolderGroupDuringTheYear contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY" decimals="0" unitRef="pure">{{ complaint.filed_py|int }}</in-capmkt:NumberOfComplaintsFiledFromStakeHolderGroupDuringTheYear>
<in-capmkt:NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear contextRef="I_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY" decimals="0" unitRef="pure">{{ complaint.pending_py|int }}</in-capmkt:NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear>
<in-capmkt:RemarksStakeHolderGroupFromWhomComplaintIsReceived contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY">{{ complaint.remarks_py if complaint.remarks_py else '0' }}</in-capmkt:RemarksStakeHolderGroupFromWhomComplaintIsReceived>
{% endfor %}

<!-- VIII. Material Issues - Overview of entity's material responsible business conduct issues -->
{% for issue in material_issues %}
<in-capmkt:MaterialIssueIdentified contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.issue }}</in-capmkt:MaterialIssueIdentified>
<in-capmkt:IndicateWhetherRiskOrOpportunity contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.risk_or_opp }}</in-capmkt:IndicateWhetherRiskOrOpportunity>
<in-capmkt:RationaleForIdentifyingTheRiskOpportunity contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.rationale }}</in-capmkt:RationaleForIdentifyingTheRiskOpportunity>
<in-capmkt:InCaseOfRiskApproachToAdaptOrMitigate contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.mitigation }}</in-capmkt:InCaseOfRiskApproachToAdaptOrMitigate>
<in-capmkt:FinancialImplicationsOfTheRiskOrOpportunity contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.financial_impact }}</in-capmkt:FinancialImplicationsOfTheRiskOrOpportunity>
{% endfor %}

<!-- Section B & C -->

    <!-- ========================================= -->
    <!-- PRINCIPLE 3 - Employee/Worker Well-being -->
    <!-- ========================================= -->

    <!-- Employee Well-being Data - Table 1A - Permanent Employees -->
    {% set emp_map = {'permanent': 'PermanentEmployees', 'other_than_permanent': 'OtherThanPermanentEmployees'} %}
    {% set gender_map = {'male': 'Male', 'female': 'Female', 'others': 'Others', 'total': 'Total'} %}
    {% set benefit_map = {'health': 'HealthInsurance', 'accident': 'AccidentInsurance', 'maternity': 'MaternityBenefits', 'paternity': 'PaternityBenefits', 'daycare': 'DayCareFacilities'} %}

    {% for emp_key, emp_type in emp_map.items() %}
    {% for gender_key, gender in gender_map.items() %}
    <!-- {{ gender }} {{ emp_type }} Total -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkers contextRef="D_{{ gender }}_Total_{{ emp_type }}_Table1A" decimals="0" unitRef="pure">{{ employee_wellbeing.employees[emp_key][gender_key].get('total', 0) | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkers>

    {% for benefit_key, benefit in benefit_map.items() %}
    <!-- {{ gender }} {{ emp_type }} {{ benefit }} -->
    <in-capmkt:NumberOfWellBeingOfEmployeesOrWorkers contextRef="D_{{ gender }}_{{ benefit }}_{{ emp_type }}_Table1A" decimals="0" unitRef="pure">{{ employee_wellbeing.employees[emp_key][gender_key].get(benefit_key + '_num', 0) | int }}</in-capmkt:NumberOfWellBeingOfEmployeesOrWorkers>
    <in-capmkt:PercentageOfWellBeingOfEmployeesOrWorkers contextRef="D_{{ gender }}_{{ benefit }}_{{ emp_type }}_Table1A" decimals="INF" unitRef="pure">{{ employee_wellbeing.employees[emp_key][gender_key].get(benefit_key + '_pct', 0) }}</in-capmkt:PercentageOfWellBeingOfEmployeesOrWorkers>
    {% endfor %}
    {% endfor %}
    {% endfor %}

    <!-- Worker Well-being Data - Table 1B -->
    {% set worker_map = {'permanent': 'PermanentWorkers', 'other_than_permanent': 'OtherThanPermanentWorkers'} %}

    {% for worker_key, worker_type in worker_map.items() %}
    {% for gender_key, gender in gender_map.items() %}
    <!-- {{ gender }} {{ worker_type }} Total -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkers contextRef="D_{{ gender }}_Total_{{ worker_type }}_Table1B" decimals="0" unitRef="pure">{{ employee_wellbeing.workers[worker_key][gender_key].get('total', 0) | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkers>

    {% for benefit_key, benefit in benefit_map.items() %}
    <!-- {{ gender }} {{ worker_type }} {{ benefit }} -->
    <in-capmkt:NumberOfWellBeingOfEmployeesOrWorkers contextRef="D_{{ gender }}_{{ benefit }}_{{ worker_type }}_Table1B" decimals="0" unitRef="pure">{{ employee_wellbeing.workers[worker_key][gender_key].get(benefit_key + '_num', 0) | int }}</in-capmkt:NumberOfWellBeingOfEmployeesOrWorkers>
    <in-capmkt:PercentageOfWellBeingOfEmployeesOrWorkers contextRef="D_{{ gender }}_{{ benefit }}_{{ worker_type }}_Table1B" decimals="INF" unitRef="pure">{{ employee_wellbeing.workers[worker_key][gender_key].get(benefit_key + '_pct', 0) }}</in-capmkt:PercentageOfWellBeingOfEmployeesOrWorkers>
    {% endfor %}
    {% endfor %}
    {% endfor %}

    <!-- Retirement Benefits - Provident Fund (PF) -->
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_ProvidentFund" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.pf.emp_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_ProvidentFund" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.pf.worker_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_ProvidentFund">{{ employee_wellbeing.retirement_benefits.pf.deposited_cy }}</in-capmkt:DeductedAndDepositedWithTheAuthority>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_ProvidentFund_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.pf.emp_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_ProvidentFund_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.pf.worker_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_ProvidentFund_PY">{{ employee_wellbeing.retirement_benefits.pf.deposited_py }}</in-capmkt:DeductedAndDepositedWithTheAuthority>

    <!-- Retirement Benefits - Gratuity -->
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_Gratuity" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.gratuity.emp_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_Gratuity" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.gratuity.worker_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_Gratuity">{{ employee_wellbeing.retirement_benefits.gratuity.deposited_cy }}</in-capmkt:DeductedAndDepositedWithTheAuthority>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_Gratuity_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.gratuity.emp_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_Gratuity_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.gratuity.worker_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_Gratuity_PY">{{ employee_wellbeing.retirement_benefits.gratuity.deposited_py }}</in-capmkt:DeductedAndDepositedWithTheAuthority>

    <!-- Retirement Benefits - ESI -->
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_ESI" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.esi.emp_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_ESI" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.esi.worker_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_ESI">{{ employee_wellbeing.retirement_benefits.esi.deposited_cy }}</in-capmkt:DeductedAndDepositedWithTheAuthority>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_ESI_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.esi.emp_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_ESI_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.esi.worker_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_ESI_PY">{{ employee_wellbeing.retirement_benefits.esi.deposited_py }}</in-capmkt:DeductedAndDepositedWithTheAuthority>

    <!-- Retirement Benefits - Others -->
    <in-capmkt:NameOfOtherRetirementBenefits contextRef="D_OtherRetirementBenefits1">{{ employee_wellbeing.retirement_benefits.others.name_cy | e }}</in-capmkt:NameOfOtherRetirementBenefits>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_OtherRetirementBenefits1" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.others.emp_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_OtherRetirementBenefits1" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.others.worker_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_OtherRetirementBenefits1">{{ employee_wellbeing.retirement_benefits.others.deposited_cy }}</in-capmkt:DeductedAndDepositedWithTheAuthority>
    <in-capmkt:NameOfOtherRetirementBenefits contextRef="D_OtherRetirementBenefits_PY1">{{ employee_wellbeing.retirement_benefits.others.name_py | e }}</in-capmkt:NameOfOtherRetirementBenefits>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_OtherRetirementBenefits_PY1" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.others.emp_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_OtherRetirementBenefits_PY1" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.others.worker_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_OtherRetirementBenefits_PY1">{{ employee_wellbeing.retirement_benefits.others.deposited_py }}</in-capmkt:DeductedAndDepositedWithTheAuthority>

    <!-- Parental Leave Return/Retention Rates - Male -->
    <in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave contextRef="D_Male" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.male.emp_return }}</in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave contextRef="D_Male" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.male.emp_retention }}</in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave>
    <in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave contextRef="D_Male" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.male.worker_return }}</in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave contextRef="D_Male" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.male.worker_retention }}</in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave>

    <!-- Parental Leave Return/Retention Rates - Female -->
    <in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave contextRef="D_Female" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.female.emp_return }}</in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave contextRef="D_Female" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.female.emp_retention }}</in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave>
    <in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave contextRef="D_Female" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.female.worker_return }}</in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave contextRef="D_Female" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.female.worker_retention }}</in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave>

    <!-- Parental Leave Return/Retention Rates - Other Gender -->
    <in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave contextRef="D_OtherGender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.others.emp_return }}</in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave contextRef="D_OtherGender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.others.emp_retention }}</in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave>
    <in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave contextRef="D_OtherGender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.others.worker_return }}</in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave contextRef="D_OtherGender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.others.worker_retention }}</in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave>

    <!-- Parental Leave Return/Retention Rates - Total -->
    <in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave contextRef="D_Gender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.total.emp_return }}</in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave contextRef="D_Gender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.total.emp_retention }}</in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave>
    <in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave contextRef="D_Gender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.total.worker_return }}</in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave contextRef="D_Gender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.total.worker_retention }}</in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave>

    <!-- Well-being Spending -->
    <in-capmkt:CostIncurredOnWellbeingMeasuresAsPercentageOfTotalRevenue contextRef="D_WellbeingSpending_CY" decimals="INF" unitRef="pure">{{ employee_wellbeing.wellbeing_spending['cy'] }}</in-capmkt:CostIncurredOnWellbeingMeasuresAsPercentageOfTotalRevenue>
    <in-capmkt:CostIncurredOnWellbeingMeasuresAsPercentageOfTotalRevenue contextRef="D_WellbeingSpending_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.wellbeing_spending['py'] }}</in-capmkt:CostIncurredOnWellbeingMeasuresAsPercentageOfTotalRevenue>

    <!-- Accessibility -->
    <in-capmkt:AreThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkers contextRef="DCYMain">Yes</in-capmkt:AreThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkers>

    <!-- Equal Opportunity Policy (Principle 3) -->
    <in-capmkt:DoesTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">{{ employee_wellbeing.equal_opportunity.has_policy }}</in-capmkt:DoesTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016>
    <in-capmkt:WebLinkOfEqualOppertunityPolicyTextBlock contextRef="DCYMain">{{ employee_wellbeing.equal_opportunity.web_link }}</in-capmkt:WebLinkOfEqualOppertunityPolicyTextBlock>

    <!-- Grievance Mechanism (Principle 3 Q6) -->
    <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker contextRef="DCYMain">{{ employee_wellbeing.grievance.has_mechanism }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker>
    <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForPermanentWorkers contextRef="DCYMain">{{ employee_wellbeing.grievance.permanent_workers.available }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForPermanentWorkers>
    <in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForPermanentWorkersExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.grievance.permanent_workers.details | e }}</in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForPermanentWorkersExplanatoryTextBlock>
    <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentWorkers contextRef="DCYMain">{{ employee_wellbeing.grievance.other_workers.available }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentWorkers>
    <in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentWorkersExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.grievance.other_workers.details | e }}</in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentWorkersExplanatoryTextBlock>
    <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForPermanentEmployees contextRef="DCYMain">{{ employee_wellbeing.grievance.permanent_employees.available }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForPermanentEmployees>
    <in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForPermanentEmployeesExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.grievance.permanent_employees.details | e }}</in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForPermanentEmployeesExplanatoryTextBlock>
    <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentEmployees contextRef="DCYMain">{{ employee_wellbeing.grievance.other_employees.available }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentEmployees>
    <in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentEmployeesExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.grievance.other_employees.details | e }}</in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentEmployeesExplanatoryTextBlock>

    <!-- OHS Management System -->
    <in-capmkt:WhetherAnOccupationalHealthAndSafetyManagementSystemHasBeenImplementedByTheEntity contextRef="DCYMain">{{ employee_wellbeing.ohs.implemented }}</in-capmkt:WhetherAnOccupationalHealthAndSafetyManagementSystemHasBeenImplementedByTheEntity>
    <in-capmkt:DetailsOfOccupationalHealthAndSafetyManagementSystemExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.ohs.coverage | e }}</in-capmkt:DetailsOfOccupationalHealthAndSafetyManagementSystemExplanatoryTextBlock>
    <in-capmkt:DesclosureOfTheProcessesUsedToIdentifyWorkRelatedHazardsAndAssessRisksOnARoutineAndNonRoutineBasisByTheEntityExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.ohs.hazard_process | e }}</in-capmkt:DesclosureOfTheProcessesUsedToIdentifyWorkRelatedHazardsAndAssessRisksOnARoutineAndNonRoutineBasisByTheEntityExplanatoryTextBlock>
    <in-capmkt:WhetherYouHaveProcessesForWorkersToReportTheWorkRelatedHazardsAndToRemoveThemselvesFromSuchRisks contextRef="DCYMain">{{ employee_wellbeing.ohs.worker_report_process }}</in-capmkt:WhetherYouHaveProcessesForWorkersToReportTheWorkRelatedHazardsAndToRemoveThemselvesFromSuchRisks>
    <in-capmkt:DoTheEmployeesOrWorkerOfTheEntityHaveAccessToNonOccupationalMedicalAndHealthcareServices contextRef="DCYMain">{{ employee_wellbeing.ohs.non_occupational_access }}</in-capmkt:DoTheEmployeesOrWorkerOfTheEntityHaveAccessToNonOccupationalMedicalAndHealthcareServices>

    <!-- Safety Incidents -->
    <in-capmkt:LostTimeInjuryFrequencyRatePerOneMillionPersonHoursWorked contextRef="D_Employees" decimals="INF" unitRef="pure">{{ employee_wellbeing.safety_incidents.ltifr_emp_cy }}</in-capmkt:LostTimeInjuryFrequencyRatePerOneMillionPersonHoursWorked>
    <in-capmkt:LostTimeInjuryFrequencyRatePerOneMillionPersonHoursWorked contextRef="D_Employees_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.safety_incidents.ltifr_emp_py }}</in-capmkt:LostTimeInjuryFrequencyRatePerOneMillionPersonHoursWorked>
    <in-capmkt:LostTimeInjuryFrequencyRatePerOneMillionPersonHoursWorked contextRef="D_Workers" decimals="INF" unitRef="pure">{{ employee_wellbeing.safety_incidents.ltifr_worker_cy }}</in-capmkt:LostTimeInjuryFrequencyRatePerOneMillionPersonHoursWorked>
    <in-capmkt:LostTimeInjuryFrequencyRatePerOneMillionPersonHoursWorked contextRef="D_Workers_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.safety_incidents.ltifr_worker_py }}</in-capmkt:LostTimeInjuryFrequencyRatePerOneMillionPersonHoursWorked>

    <in-capmkt:TotalRecordableWorkRelatedInjuries contextRef="D_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.injuries_emp_cy | int }}</in-capmkt:TotalRecordableWorkRelatedInjuries>
    <in-capmkt:TotalRecordableWorkRelatedInjuries contextRef="D_Employees_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.injuries_emp_py | int }}</in-capmkt:TotalRecordableWorkRelatedInjuries>
    <in-capmkt:TotalRecordableWorkRelatedInjuries contextRef="D_Workers" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.injuries_worker_cy | int }}</in-capmkt:TotalRecordableWorkRelatedInjuries>
    <in-capmkt:TotalRecordableWorkRelatedInjuries contextRef="D_Workers_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.injuries_worker_py | int }}</in-capmkt:TotalRecordableWorkRelatedInjuries>

    <in-capmkt:NumberOfFatalities contextRef="D_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.fatalities_emp_cy | int }}</in-capmkt:NumberOfFatalities>
    <in-capmkt:NumberOfFatalities contextRef="D_Employees_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.fatalities_emp_py | int }}</in-capmkt:NumberOfFatalities>
    <in-capmkt:NumberOfFatalities contextRef="D_Workers" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.fatalities_worker_cy | int }}</in-capmkt:NumberOfFatalities>
    <in-capmkt:NumberOfFatalities contextRef="D_Workers_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.fatalities_worker_py | int }}</in-capmkt:NumberOfFatalities>

    <in-capmkt:HighConsequenceWorkRelatedInjuryOrIllHealthExcludingFatalities contextRef="D_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.high_consequence_emp_cy | int }}</in-capmkt:HighConsequenceWorkRelatedInjuryOrIllHealthExcludingFatalities>
    <in-capmkt:HighConsequenceWorkRelatedInjuryOrIllHealthExcludingFatalities contextRef="D_Employees_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.high_consequence_emp_py | int }}</in-capmkt:HighConsequenceWorkRelatedInjuryOrIllHealthExcludingFatalities>
    <in-capmkt:HighConsequenceWorkRelatedInjuryOrIllHealthExcludingFatalities contextRef="D_Workers" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.high_consequence_worker_cy | int }}</in-capmkt:HighConsequenceWorkRelatedInjuryOrIllHealthExcludingFatalities>
    <in-capmkt:HighConsequenceWorkRelatedInjuryOrIllHealthExcludingFatalities contextRef="D_Workers_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.safety_incidents.high_consequence_worker_py | int }}</in-capmkt:HighConsequenceWorkRelatedInjuryOrIllHealthExcludingFatalities>

    <!-- Complaints -->
    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_WorkingConditionsComplaints" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.working_conditions.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_WorkingConditionsComplaints" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.working_conditions.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_WorkingConditionsComplaints_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.working_conditions.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_WorkingConditionsComplaints_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.working_conditions.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_HealthSafetyComplaints" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.health_safety.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_HealthSafetyComplaints" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.health_safety.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_HealthSafetyComplaints_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.health_safety.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_HealthSafetyComplaints_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.health_safety.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>

    <!-- Assessments -->
    <in-capmkt:PercentageOfHealthAndSafetyPracticesOfYourPlantsAndOfficesThatWereAssessedP3 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ employee_wellbeing.assessments.health_safety_pct }}</in-capmkt:PercentageOfHealthAndSafetyPracticesOfYourPlantsAndOfficesThatWereAssessedP3>
    <in-capmkt:PercentageOfWorkingConditionsOfYourPlantsAndOfficesThatWereAssessedP3 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ employee_wellbeing.assessments.working_conditions_pct }}</in-capmkt:PercentageOfWorkingConditionsOfYourPlantsAndOfficesThatWereAssessedP3>

    <!-- Safe and Healthy Workplace Measures (P3 Q12) -->
    <in-capmkt:DescribeTheMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlaceExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.safe_workplace_measures | e }}</in-capmkt:DescribeTheMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlaceExplanatoryTextBlock>

    <!-- Corrective Actions for Safety-Related Incidents (P3 Q15) -->
    <in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessedExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.corrective_actions_safety | e }}</in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessedExplanatoryTextBlock>

    <!-- Life Insurance -->
    <in-capmkt:DoesTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees contextRef="DCYMain">{{ employee_wellbeing.life_insurance.employees }}</in-capmkt:DoesTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees>
    <in-capmkt:DoesTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfWorkers contextRef="DCYMain">{{ employee_wellbeing.life_insurance.workers }}</in-capmkt:DoesTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfWorkers>

    <!-- Statutory Dues for Value Chain Partners -->
    <in-capmkt:DetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartnersExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.statutory_dues_measures | e }}</in-capmkt:DetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartnersExplanatoryTextBlock>

    <!-- Affected Employees/Workers (High Consequence Injuries) -->
    <in-capmkt:TotalNumberOfAffectedEmployees contextRef="DCYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.affected_employees_cy | int }}</in-capmkt:TotalNumberOfAffectedEmployees>
    <in-capmkt:TotalNumberOfAffectedEmployees contextRef="DPYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.affected_employees_py | int }}</in-capmkt:TotalNumberOfAffectedEmployees>
    <in-capmkt:TotalNumberOfAffectedWorkers contextRef="DCYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.affected_workers_cy | int }}</in-capmkt:TotalNumberOfAffectedWorkers>
    <in-capmkt:TotalNumberOfAffectedWorkers contextRef="DPYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.affected_workers_py | int }}</in-capmkt:TotalNumberOfAffectedWorkers>

    <!-- Rehabilitated Employees/Workers -->
    <in-capmkt:NumberOfEmployeesOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment contextRef="DCYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.rehabilitated_employees_cy | int }}</in-capmkt:NumberOfEmployeesOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment>
    <in-capmkt:NumberOfEmployeesOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment contextRef="DPYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.rehabilitated_employees_py | int }}</in-capmkt:NumberOfEmployeesOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment>
    <in-capmkt:NumberOfWorkersOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment contextRef="DCYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.rehabilitated_workers_cy | int }}</in-capmkt:NumberOfWorkersOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment>
    <in-capmkt:NumberOfWorkersOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment contextRef="DPYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.rehabilitated_workers_py | int }}</in-capmkt:NumberOfWorkersOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment>

    <!-- Transition Assistance Programs -->
    <in-capmkt:DoesTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment contextRef="DCYMain">{{ employee_wellbeing.transition_assistance }}</in-capmkt:DoesTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment>
    <in-capmkt:DetailsOfTransitionAssistanceProgramsProvidedToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmploymentExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.transition_assistance_details | e }}</in-capmkt:DetailsOfTransitionAssistanceProgramsProvidedToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmploymentExplanatoryTextBlock>

    <!-- Training Data -->
    {% set training_genders = [('male', 'Male'), ('female', 'Female'), ('others', 'Others')] %}
    {% for gender_key, gender in training_genders %}
    <!-- {{ gender }} Employees Training -->
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_TotalEmployeesAndWorkers_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].total_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].hs_num_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].hs_pct_cy }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnSkillUpgradation_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].skill_num_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnSkillUpgradation_Employees" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].skill_pct_cy }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
    <!-- {{ gender }} Employees Training PY -->
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_TotalEmployeesAndWorkers_Employees_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].total_py | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].hs_num_py | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].hs_pct_py }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
    <!-- {{ gender }} Workers Training -->
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_TotalEmployeesAndWorkers_Workers" decimals="0" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].total_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers" decimals="0" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].hs_num_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].hs_pct_cy }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
    <!-- {{ gender }} Workers Training PY -->
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_TotalEmployeesAndWorkers_Workers_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].total_py | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].hs_num_py | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].hs_pct_py }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
    {% endfor %}

    <!-- Performance and Career Development -->
    {% for gender_key, gender in training_genders %}
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.performance.employees[gender_key].total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForPerformanceAndCareerDevelopment>
    <in-capmkt:NumberOfEmployeesOrWorkerForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.performance.employees[gender_key].reviewed_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkerForPerformanceAndCareerDevelopment>
    <in-capmkt:PercentageOfEmployeesOrWorkerForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Employees" decimals="INF" unitRef="pure">{{ employee_wellbeing.performance.employees[gender_key].pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkerForPerformanceAndCareerDevelopment>
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Employees_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.performance.employees[gender_key].total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForPerformanceAndCareerDevelopment>
    <in-capmkt:NumberOfEmployeesOrWorkerForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Employees_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.performance.employees[gender_key].reviewed_py | int }}</in-capmkt:NumberOfEmployeesOrWorkerForPerformanceAndCareerDevelopment>
    <in-capmkt:PercentageOfEmployeesOrWorkerForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Employees_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.performance.employees[gender_key].pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkerForPerformanceAndCareerDevelopment>
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Workers" decimals="0" unitRef="pure">{{ employee_wellbeing.performance.workers[gender_key].total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForPerformanceAndCareerDevelopment>
    <in-capmkt:NumberOfEmployeesOrWorkerForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Workers" decimals="0" unitRef="pure">{{ employee_wellbeing.performance.workers[gender_key].reviewed_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkerForPerformanceAndCareerDevelopment>
    <in-capmkt:PercentageOfEmployeesOrWorkerForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Workers" decimals="INF" unitRef="pure">{{ employee_wellbeing.performance.workers[gender_key].pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkerForPerformanceAndCareerDevelopment>
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Workers_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.performance.workers[gender_key].total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForPerformanceAndCareerDevelopment>
    <in-capmkt:NumberOfEmployeesOrWorkerForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Workers_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.performance.workers[gender_key].reviewed_py | int }}</in-capmkt:NumberOfEmployeesOrWorkerForPerformanceAndCareerDevelopment>
    <in-capmkt:PercentageOfEmployeesOrWorkerForPerformanceAndCareerDevelopment contextRef="D_{{ gender }}_Workers_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.performance.workers[gender_key].pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkerForPerformanceAndCareerDevelopment>
    {% endfor %}


    <!-- Accessibility -->
    <in-capmkt:DescriptionOfAccessibilityOfWorkplaces contextRef="D_Accessibility">{{ employee_wellbeing.accessibility | e }}</in-capmkt:DescriptionOfAccessibilityOfWorkplaces>

    <!-- ==================== UNION MEMBERSHIP (Principle 3 Q7) ==================== -->
    <!-- Permanent Employees - Total (CY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Gender_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.total.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Gender_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.total.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Gender_PermanentEmployees" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.total.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
    <!-- Permanent Employees - Total (PY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Gender_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.total.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Gender_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.total.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Gender_PermanentEmployees_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.total.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

    <!-- Permanent Employees - Male (CY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Male_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.male.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Male_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.male.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Male_PermanentEmployees" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.male.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
    <!-- Permanent Employees - Male (PY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Male_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.male.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Male_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.male.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Male_PermanentEmployees_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.male.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

    <!-- Permanent Employees - Female (CY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Female_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.female.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Female_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.female.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Female_PermanentEmployees" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.female.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
    <!-- Permanent Employees - Female (PY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Female_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.female.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Female_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.female.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Female_PermanentEmployees_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.female.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

    <!-- Permanent Employees - Other Gender (CY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_OtherGender_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.other.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_OtherGender_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.other.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_OtherGender_PermanentEmployees" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.other.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
    <!-- Permanent Employees - Other Gender (PY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_OtherGender_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.other.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_OtherGender_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.other.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_OtherGender_PermanentEmployees_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.other.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

    <!-- Permanent Workers - Total (CY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Gender_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.total.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Gender_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.total.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Gender_PermanentWorkers" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.total.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
    <!-- Permanent Workers - Total (PY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Gender_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.total.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Gender_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.total.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Gender_PermanentWorkers_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.total.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

    <!-- Permanent Workers - Male (CY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Male_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.male.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Male_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.male.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Male_PermanentWorkers" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.male.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
    <!-- Permanent Workers - Male (PY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Male_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.male.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Male_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.male.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Male_PermanentWorkers_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.male.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

    <!-- Permanent Workers - Female (CY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Female_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.female.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Female_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.female.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Female_PermanentWorkers" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.female.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
    <!-- Permanent Workers - Female (PY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Female_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.female.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Female_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.female.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Female_PermanentWorkers_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.female.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

    <!-- Permanent Workers - Other Gender (CY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_OtherGender_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.other.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_OtherGender_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.other.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_OtherGender_PermanentWorkers" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.other.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
    <!-- Permanent Workers - Other Gender (PY) -->
    <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_OtherGender_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.other.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_OtherGender_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.other.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_OtherGender_PermanentWorkers_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.other.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>


    <!-- PRINCIPLE 7 - Trade/Industry Chamber Affiliations Contexts -->
    {% for i in range(1, 21) %}
    <xbrli:context id="D_IndustryChambersOrAssociations{{ i }}">
      <xbrli:entity><xbrli:identifier scheme="http://www.mca.gov.in/CIN">{{ cin }}</xbrli:identifier></xbrli:entity>
      <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
    </xbrli:context>
    {% endfor %}

    <!-- CSR Projects in Aspirational Districts Contexts -->
    {% for project in csr.aspirational_districts %}
    <xbrli:context id="{{ project.axis_id }}">
      <xbrli:entity><xbrli:identifier scheme="http://www.mca.gov.in/CIN">{{ cin }}</xbrli:identifier></xbrli:entity>
      <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
    </xbrli:context>
    {% endfor %}

    <!-- PRINCIPLE 9 - Consumer Complaints Contexts -->
    {% for cat in ['DataPrivacy', 'Advertising', 'CyberSecurity', 'DeliveryOfEssentialServices', 'RestrictiveTradePractices', 'UnfairTradePractices', 'Other'] %}
    <xbrli:context id="D_{{ cat }}">
      <xbrli:entity><xbrli:identifier scheme="http://www.mca.gov.in/CIN">{{ cin }}</xbrli:identifier></xbrli:entity>
      <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
    </xbrli:context>
    <xbrli:context id="I_{{ cat }}">
      <xbrli:entity><xbrli:identifier scheme="http://www.mca.gov.in/CIN">{{ cin }}</xbrli:identifier></xbrli:entity>
      <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
    </xbrli:context>
    <xbrli:context id="D_{{ cat }}_PY">
      <xbrli:entity><xbrli:identifier scheme="http://www.mca.gov.in/CIN">{{ cin }}</xbrli:identifier></xbrli:entity>
      <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
    </xbrli:context>
    <xbrli:context id="I_{{ cat }}_PY">
      <xbrli:entity><xbrli:identifier scheme="http://www.mca.gov.in/CIN">{{ cin }}</xbrli:identifier></xbrli:entity>
      <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
    </xbrli:context>
    {% endfor %}


    <!-- ==================== PRINCIPLE 7: POLICY ADVOCACY ==================== -->
    <in-capmkt:NumberOfAffiliationsWithTradeAndIndustryChambersOrAssociations contextRef="DCYMain" decimals="0" unitRef="pure">{{ p789_data.p7.num_affiliations }}</in-capmkt:NumberOfAffiliationsWithTradeAndIndustryChambersOrAssociations>

    {% for affiliation in p789_data.p7.affiliations %}
    <in-capmkt:NameOfTheTradeAndIndustryChambersOrAssociations contextRef="D_IndustryChambersOrAssociations{{ loop.index }}">{{ affiliation.name | e }}</in-capmkt:NameOfTheTradeAndIndustryChambersOrAssociations>
    <in-capmkt:ReachOfTradeAndIndustryChambersOrAssociations contextRef="D_IndustryChambersOrAssociations{{ loop.index }}">{{ affiliation.reach }}</in-capmkt:ReachOfTradeAndIndustryChambersOrAssociations>
    {% endfor %}

    <!-- ==================== PRINCIPLE 8: INCLUSIVE GROWTH ==================== -->
    <in-capmkt:DescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunityExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p8.community_grievance_mechanism | e }}</in-capmkt:DescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunityExplanatoryTextBlock>
    <in-capmkt:PercentageOfDirectlySourcedFromMSMEsOrSmallProducers contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p8.msme_sourcing_cy }}</in-capmkt:PercentageOfDirectlySourcedFromMSMEsOrSmallProducers>
    <in-capmkt:PercentageOfDirectlySourcedFromMSMEsOrSmallProducers contextRef="DPYMain" decimals="INF" unitRef="pure">{{ p789_data.p8.msme_sourcing_py }}</in-capmkt:PercentageOfDirectlySourcedFromMSMEsOrSmallProducers>
    <in-capmkt:PercentageOfSourcedDirectlyFromWithinTheDistrictAndNeighbouringDistricts contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p8.local_sourcing_cy }}</in-capmkt:PercentageOfSourcedDirectlyFromWithinTheDistrictAndNeighbouringDistricts>
    <in-capmkt:PercentageOfSourcedDirectlyFromWithinTheDistrictAndNeighbouringDistricts contextRef="DPYMain" decimals="INF" unitRef="pure">{{ p789_data.p8.local_sourcing_py }}</in-capmkt:PercentageOfSourcedDirectlyFromWithinTheDistrictAndNeighbouringDistricts>
    <in-capmkt:DoYouHaveAPreferentialProcurementPolicyWhereYouGivePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroups contextRef="DCYMain">{{ p789_data.p8.preferential_procurement }}</in-capmkt:DoYouHaveAPreferentialProcurementPolicyWhereYouGivePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroups>

    <!-- ==================== PRINCIPLE 9: CONSUMER RESPONSIBILITY ==================== -->
    <in-capmkt:DescribeTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedbackExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.complaint_mechanism | e }}</in-capmkt:DescribeTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedbackExplanatoryTextBlock>
    <in-capmkt:EnvironmentalAndSocialParametersRelevantToTheProductAsAPercentageToTotalTurnover contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p9.env_social_pct }}</in-capmkt:EnvironmentalAndSocialParametersRelevantToTheProductAsAPercentageToTotalTurnover>
    <in-capmkt:SafeAndResponsibleUsageAsAPercentageToTotalTurnover contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p9.safe_usage_pct }}</in-capmkt:SafeAndResponsibleUsageAsAPercentageToTotalTurnover>
    <in-capmkt:RecyclingAndOrSafeDisposalAsAPercentageToTotalTurnover contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p9.recycling_pct }}</in-capmkt:RecyclingAndOrSafeDisposalAsAPercentageToTotalTurnover>

    <!-- Consumer Complaints CY -->
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_DataPrivacy" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.data_privacy.received_cy }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_DataPrivacy" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.data_privacy.pending_cy }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_DataPrivacy">{{ p789_data.p9.complaints.data_privacy.remark_cy | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_Advertising" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.advertising.received_cy }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_Advertising" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.advertising.pending_cy }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_Advertising">{{ p789_data.p9.complaints.advertising.remark_cy | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_CyberSecurity" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.cyber_security.received_cy }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_CyberSecurity" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.cyber_security.pending_cy }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_CyberSecurity">{{ p789_data.p9.complaints.cyber_security.remark_cy | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_DeliveryOfEssentialServices" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.essential_services.received_cy }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_DeliveryOfEssentialServices" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.essential_services.pending_cy }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_DeliveryOfEssentialServices">{{ p789_data.p9.complaints.essential_services.remark_cy | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_RestrictiveTradePractices" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.restrictive_trade.received_cy }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_RestrictiveTradePractices" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.restrictive_trade.pending_cy }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_RestrictiveTradePractices">{{ p789_data.p9.complaints.restrictive_trade.remark_cy | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_UnfairTradePractices" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.unfair_trade.received_cy }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_UnfairTradePractices" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.unfair_trade.pending_cy }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_UnfairTradePractices">{{ p789_data.p9.complaints.unfair_trade.remark_cy | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_Other" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.other.received_cy }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_Other" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.other.pending_cy }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_Other">{{ p789_data.p9.complaints.other.remark_cy | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>

    <!-- Consumer Complaints PY -->
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_DataPrivacy_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.data_privacy.received_py }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_DataPrivacy_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.data_privacy.pending_py }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_DataPrivacy_PY">{{ p789_data.p9.complaints.data_privacy.remark_py | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_Advertising_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.advertising.received_py }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_Advertising_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.advertising.pending_py }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_Advertising_PY">{{ p789_data.p9.complaints.advertising.remark_py | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_CyberSecurity_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.cyber_security.received_py }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_CyberSecurity_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.cyber_security.pending_py }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_CyberSecurity_PY">{{ p789_data.p9.complaints.cyber_security.remark_py | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_DeliveryOfEssentialServices_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.essential_services.received_py }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_DeliveryOfEssentialServices_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.essential_services.pending_py }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_DeliveryOfEssentialServices_PY">{{ p789_data.p9.complaints.essential_services.remark_py | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_RestrictiveTradePractices_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.restrictive_trade.received_py }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_RestrictiveTradePractices_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.restrictive_trade.pending_py }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_RestrictiveTradePractices_PY">{{ p789_data.p9.complaints.restrictive_trade.remark_py | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_UnfairTradePractices_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.unfair_trade.received_py }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_UnfairTradePractices_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.unfair_trade.pending_py }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_UnfairTradePractices_PY">{{ p789_data.p9.complaints.unfair_trade.remark_py | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>
    <in-capmkt:ConsumerComplaintsReceivedDuringTheYear contextRef="D_Other_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.other.received_py }}</in-capmkt:ConsumerComplaintsReceivedDuringTheYear>
    <in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear contextRef="I_Other_PY" decimals="0" unitRef="pure">{{ p789_data.p9.complaints.other.pending_py }}</in-capmkt:ConsumerComplaintsPendingResolutionAtEndOfYear>
    <in-capmkt:RemarkForConsumerComplaints contextRef="D_Other_PY">{{ p789_data.p9.complaints.other.remark_py | default('NA') }}</in-capmkt:RemarkForConsumerComplaints>

    <!-- Product Recalls -->
    <in-capmkt:NumberOfVoluntaryRecalls contextRef="DCYMain" decimals="0" unitRef="pure">{{ p789_data.p9.voluntary_recalls }}</in-capmkt:NumberOfVoluntaryRecalls>
    <in-capmkt:ReasonsForVoluntaryRecall contextRef="DCYMain">{{ p789_data.p9.voluntary_recall_reason }}</in-capmkt:ReasonsForVoluntaryRecall>
    <in-capmkt:NumberOfForcedRecalls contextRef="DCYMain" decimals="0" unitRef="pure">{{ p789_data.p9.forced_recalls }}</in-capmkt:NumberOfForcedRecalls>
    <in-capmkt:ReasonsForForcedRecall contextRef="DCYMain">{{ p789_data.p9.forced_recall_reason }}</in-capmkt:ReasonsForForcedRecall>

    <!-- Cyber Security (Principle 9 Q5) -->
    <in-capmkt:DoesTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy contextRef="DCYMain">{{ p789_data.p9.cyber_policy }}</in-capmkt:DoesTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy>
    <in-capmkt:WebLinkOfThePolicyOnCyberSecurityAndRisksRelatedToDataPrivacy contextRef="DCYMain">{{ p789_data.p9.cyber_policy_weblink | e }}</in-capmkt:WebLinkOfThePolicyOnCyberSecurityAndRisksRelatedToDataPrivacy>
    <in-capmkt:NumberOfInstancesOfDataBreachesAlongWithImpact contextRef="DCYMain" decimals="0" unitRef="pure">{{ p789_data.p9.data_breaches }}</in-capmkt:NumberOfInstancesOfDataBreachesAlongWithImpact>
    <in-capmkt:PercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomers contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p9.pii_breach_pct }}</in-capmkt:PercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomers>
    <in-capmkt:DetailsOfImpactOfDataBreachesExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.data_breach_impact | default('NA') | e }}</in-capmkt:DetailsOfImpactOfDataBreachesExplanatoryTextBlock>

    <!-- Corrective Actions (Principle 9 Q6) -->
    <in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServicesExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.corrective_actions_q6 | e }}</in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServicesExplanatoryTextBlock>

    <!-- Product Information -->
    <in-capmkt:WeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessedExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.product_info_link | e }}</in-capmkt:WeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessedExplanatoryTextBlock>
    <in-capmkt:StepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServicesExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.consumer_education | e }}</in-capmkt:StepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServicesExplanatoryTextBlock>
    <in-capmkt:MechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServicesExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.disruption_mechanism | default('') | e }}</in-capmkt:MechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServicesExplanatoryTextBlock>
    <in-capmkt:DoesTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws contextRef="DCYMain">{{ p789_data.p9.product_info_display }}</in-capmkt:DoesTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws>
    <in-capmkt:DetailsOfProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLawsExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.product_info_display_details | default('') | e }}</in-capmkt:DetailsOfProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLawsExplanatoryTextBlock>

</xbrli:xbrl>
'''