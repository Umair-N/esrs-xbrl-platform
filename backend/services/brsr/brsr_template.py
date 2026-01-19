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

    <xbrli:context id="DPYMain">
        <xbrli:entity>
            <xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:startDate>{{ start_date_py }}</xbrli:startDate>
            <xbrli:endDate>{{ end_date_py }}</xbrli:endDate>
        </xbrli:period>
    </xbrli:context>

    <xbrli:context id="IPYMain">
        <xbrli:entity>
            <xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{{ end_date_py }}</xbrli:instant>
        </xbrli:period>
    </xbrli:context>

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

            {% for i in range(1, 10) %}
    <xbrli:context id="D_Principle{{ i }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:NGRBCPrinciplesAxis">in-capmkt:Principle{{ i }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

    
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

        {% for product in sustainability.reclaimed_products %}
    <xbrli:context id="D_ReclaimedProductsAndTheirPackaging{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ fy_start }}</xbrli:startDate><xbrli:endDate>{{ fy_end }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:ReclaimedProductsAndTheirPackagingAxis">in-capmkt:ReclaimedProductsAndTheirPackaging{{ loop.index }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

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

        {% for complaint in complaints %}
        <xbrli:context id="D_ComplaintReceivedFrom{{ complaint.stakeholder }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis">in-capmkt:{{ complaint.stakeholder }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
        <xbrli:context id="I_ComplaintReceivedFrom{{ complaint.stakeholder }}">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_cy }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis">in-capmkt:{{ complaint.stakeholder }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
        <xbrli:context id="D_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis">in-capmkt:{{ complaint.stakeholder }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
        <xbrli:context id="I_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>{{ end_date_py }}</xbrli:instant></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupFromWhomComplaintIsReceivedAxis">in-capmkt:{{ complaint.stakeholder }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

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

        <xbrli:context id="D_WellbeingSpending_CY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
    </xbrli:context>
    <xbrli:context id="D_WellbeingSpending_PY">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_py }}</xbrli:startDate><xbrli:endDate>{{ end_date_py }}</xbrli:endDate></xbrli:period>
    </xbrli:context>

        <xbrli:context id="D_Accessibility">
        <xbrli:entity><xbrli:identifier scheme="https://www.sebi.gov.in/in-capmkt/CorporateIdentityNumber">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date }}</xbrli:startDate><xbrli:endDate>{{ end_date }}</xbrli:endDate></xbrli:period>
    </xbrli:context>

    
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

        {% for stakeholder in stakeholder_data.stakeholder_groups %}
    <xbrli:context id="D_StakeHolderGroups{{ loop.index }}">
        <xbrli:entity><xbrli:identifier scheme="http://www.sebi.gov.in">{{ cin }}</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
        <xbrli:scenario><xbrldi:explicitMember dimension="in-capmkt:StakeholderGroupAxis">in-capmkt:StakeHolderGroups{{ loop.index }}Member</xbrldi:explicitMember></xbrli:scenario>
    </xbrli:context>
    {% endfor %}

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

        <xbrli:unit id="INR"><xbrli:measure>iso4217:INR</xbrli:measure></xbrli:unit>
    <xbrli:unit id="pure"><xbrli:measure>xbrli:pure</xbrli:measure></xbrli:unit>
    <xbrli:unit id="tCO2e"><xbrli:measure>in-capmkt:tCO2e</xbrli:measure></xbrli:unit>
    <xbrli:unit id="Tonne"><xbrli:measure>in-capmkt:Tonne</xbrli:measure></xbrli:unit>
    <xbrli:unit id="Gigajoule"><xbrli:measure>in-capmkt:Gigajoule</xbrli:measure></xbrli:unit>
    <xbrli:unit id="Kiloliters"><xbrli:measure>in-capmkt:Kiloliters</xbrli:measure></xbrli:unit>
    <xbrli:unit id="TonnePerINR">
        <xbrli:divide>
            <xbrli:unitNumerator><xbrli:measure>in-capmkt:Tonne</xbrli:measure></xbrli:unitNumerator>
            <xbrli:unitDenominator><xbrli:measure>iso4217:INR</xbrli:measure></xbrli:unitDenominator>
        </xbrli:divide>
    </xbrli:unit>
    <xbrli:unit id="KilolitersPerINR">
        <xbrli:divide>
            <xbrli:unitNumerator><xbrli:measure>in-capmkt:Kiloliters</xbrli:measure></xbrli:unitNumerator>
            <xbrli:unitDenominator><xbrli:measure>iso4217:INR</xbrli:measure></xbrli:unitDenominator>
        </xbrli:divide>
    </xbrli:unit>
    <xbrli:unit id="GigajoulePerINR">
        <xbrli:divide>
            <xbrli:unitNumerator><xbrli:measure>in-capmkt:Gigajoule</xbrli:measure></xbrli:unitNumerator>
            <xbrli:unitDenominator><xbrli:measure>iso4217:INR</xbrli:measure></xbrli:unitDenominator>
        </xbrli:divide>
    </xbrli:unit>
    <xbrli:unit id="tCO2ePerINR">
        <xbrli:divide>
            <xbrli:unitNumerator><xbrli:measure>in-capmkt:tCO2e</xbrli:measure></xbrli:unitNumerator>
            <xbrli:unitDenominator><xbrli:measure>iso4217:INR</xbrli:measure></xbrli:unitDenominator>
        </xbrli:divide>
    </xbrli:unit>

            
    {% if data.get('assurance_sub_type_for_address_of_corporate_office_of_company') is not none %}
    <in-capmkt:AssuranceSubTypeForAddressOfCorporateOfficeOfCompany contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_address_of_corporate_office_of_company', '') }}
    </in-capmkt:AssuranceSubTypeForAddressOfCorporateOfficeOfCompany>
    {% endif %}

        {% if data.get('assurance_sub_type_for_address_of_registered_office_of_company') is not none %}
    <in-capmkt:AssuranceSubTypeForAddressOfRegisteredOfficeOfCompany contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_address_of_registered_office_of_company', '') }}
    </in-capmkt:AssuranceSubTypeForAddressOfRegisteredOfficeOfCompany>
    {% endif %}

        {% if data.get('assurance_sub_type_for_corporate_identity_number') is not none %}
    <in-capmkt:AssuranceSubTypeForCorporateIdentityNumber contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_corporate_identity_number', '') }}
    </in-capmkt:AssuranceSubTypeForCorporateIdentityNumber>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_the_stock_exchange_where_the_company_is_listed') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTheStockExchangeWhereTheCompanyIsListed contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_the_stock_exchange_where_the_company_is_listed', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTheStockExchangeWhereTheCompanyIsListed>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_waste_management_practices_adopted_in_your_establishments_and_the_strategy_adopted_by_company_to_reduce_usage_of_hazardous_and_toxic_chemicals') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicals contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_waste_management_practices_adopted_in_your_establishments_and_the_strategy_adopted_by_company_to_reduce_usage_of_hazardous_and_toxic_chemicals', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicals>
    {% endif %}

        {% if data.get('assurance_sub_type_for_e_mail_of_the_company') is not none %}
    <in-capmkt:AssuranceSubTypeForEMailOfTheCompany contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_e_mail_of_the_company', '') }}
    </in-capmkt:AssuranceSubTypeForEMailOfTheCompany>
    {% endif %}

        {% if data.get('assurance_sub_type_for_name_and_contact_details_of_the_contact_person_in_case_of_any_queries_on_the_brsr_report') is not none %}
    <in-capmkt:AssuranceSubTypeForNameAndContactDetailsOfTheContactPersonInCaseOfAnyQueriesOnTheBRSRReport contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_name_and_contact_details_of_the_contact_person_in_case_of_any_queries_on_the_brsr_report', '') }}
    </in-capmkt:AssuranceSubTypeForNameAndContactDetailsOfTheContactPersonInCaseOfAnyQueriesOnTheBRSRReport>
    {% endif %}

        {% if data.get('assurance_sub_type_for_name_of_the_company') is not none %}
    <in-capmkt:AssuranceSubTypeForNameOfTheCompany contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_name_of_the_company', '') }}
    </in-capmkt:AssuranceSubTypeForNameOfTheCompany>
    {% endif %}

        {% if data.get('assurance_sub_type_for_names_of_holding_subsidiary_associate_companies_joint_ventures') is not none %}
    <in-capmkt:AssuranceSubTypeForNamesOfHoldingSubsidiaryAssociateCompaniesJointVentures contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_names_of_holding_subsidiary_associate_companies_joint_ventures', '') }}
    </in-capmkt:AssuranceSubTypeForNamesOfHoldingSubsidiaryAssociateCompaniesJointVentures>
    {% endif %}

        {% if data.get('assurance_sub_type_for_telephone_of_company') is not none %}
    <in-capmkt:AssuranceSubTypeForTelephoneOfCompany contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_telephone_of_company', '') }}
    </in-capmkt:AssuranceSubTypeForTelephoneOfCompany>
    {% endif %}

        {% if data.get('assurance_sub_type_for_the_entity_has_undertaken_any_specific_initiatives_or_used_innovative_technology_or_solutions_to_improve_resource_efficiency') is not none %}
    <in-capmkt:AssuranceSubTypeForTheEntityHasUndertakenAnySpecificInitiativesOrUsedInnovativeTechnologyOrSolutionsToImproveResourceEfficiency contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_the_entity_has_undertaken_any_specific_initiatives_or_used_innovative_technology_or_solutions_to_improve_resource_efficiency', '') }}
    </in-capmkt:AssuranceSubTypeForTheEntityHasUndertakenAnySpecificInitiativesOrUsedInnovativeTechnologyOrSolutionsToImproveResourceEfficiency>
    {% endif %}

        {% if data.get('assurance_sub_type_for_the_entity_have_procedures_in_place_for_sustainable_sourcing_and_percentage_of_inputs_were_sourced_sustainably') is not none %}
    <in-capmkt:AssuranceSubTypeForTheEntityHaveProceduresInPlaceForSustainableSourcingAndPercentageOfInputsWereSourcedSustainably contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_the_entity_have_procedures_in_place_for_sustainable_sourcing_and_percentage_of_inputs_were_sourced_sustainably', '') }}
    </in-capmkt:AssuranceSubTypeForTheEntityHaveProceduresInPlaceForSustainableSourcingAndPercentageOfInputsWereSourcedSustainably>
    {% endif %}

        {% if data.get('assurance_sub_type_for_website_of_company') is not none %}
    <in-capmkt:AssuranceSubTypeForWebsiteOfCompany contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_website_of_company', '') }}
    </in-capmkt:AssuranceSubTypeForWebsiteOfCompany>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_csr_is_applicable_as_per_section135_of_companies_act2013') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013 contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_csr_is_applicable_as_per_section135_of_companies_act2013', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_have_any_project_related_to_reducing_green_house_gas_emission') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveAnyProjectRelatedToReducingGreenHouseGasEmission contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_have_any_project_related_to_reducing_green_house_gas_emission', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveAnyProjectRelatedToReducingGreenHouseGasEmission>
    {% endif %}

        {% if data.get('assurance_sub_type_for_year_of_incorporation') is not none %}
    <in-capmkt:AssuranceSubTypeForYearOfIncorporation contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_year_of_incorporation', '') }}
    </in-capmkt:AssuranceSubTypeForYearOfIncorporation>
    {% endif %}

        {% if data.get('assurance_sub_type_for_data_breaches_information_like_number_of_instances_of_data_breaches_along_with_impact_and_percentage_of_data_breaches_involving_personally_identifiable_information_of_customers') is not none %}
    <in-capmkt:AssuranceSubTypeForDataBreachesInformationLikeNumberOfInstancesOfDataBreachesAlongWithImpactAndPercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomers contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_data_breaches_information_like_number_of_instances_of_data_breaches_along_with_impact_and_percentage_of_data_breaches_involving_personally_identifiable_information_of_customers', '') }}
    </in-capmkt:AssuranceSubTypeForDataBreachesInformationLikeNumberOfInstancesOfDataBreachesAlongWithImpactAndPercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomers>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_air_emissions_other_than_ghg_emissions_by_the_entity') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfAirEmissionsOtherThanGhgEmissionsByTheEntity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_air_emissions_other_than_ghg_emissions_by_the_entity', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfAirEmissionsOtherThanGhgEmissionsByTheEntity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_complaints_made_by_employees_and_workers_as_per_p3') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfComplaintsMadeByEmployeesAndWorkersAsPerP3 contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_details_of_complaints_made_by_employees_and_workers_as_per_p3', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfComplaintsMadeByEmployeesAndWorkersAsPerP3>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_complaints_made_by_employees_and_workers_as_per_p5') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfComplaintsMadeByEmployeesAndWorkersAsPerP5 contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_details_of_complaints_made_by_employees_and_workers_as_per_p5', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfComplaintsMadeByEmployeesAndWorkersAsPerP5>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_employees_as_at_the_end_of_financial_year') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfEmployeesAsAtTheEndOfFinancialYear contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_details_of_employees_as_at_the_end_of_financial_year', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfEmployeesAsAtTheEndOfFinancialYear>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_measures_for_the_well_being_of_employees_and_workers_and_spending_on_it') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfMeasuresForTheWellBeingOfEmployeesAndWorkersAndSpendingOnIt contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_details_of_measures_for_the_well_being_of_employees_and_workers_and_spending_on_it', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfMeasuresForTheWellBeingOfEmployeesAndWorkersAndSpendingOnIt>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_minimum_wages_paid_to_employees_and_workers') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfMinimumWagesPaidToEmployeesAndWorkers contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_details_of_minimum_wages_paid_to_employees_and_workers', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfMinimumWagesPaidToEmployeesAndWorkers>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_number_of_consumer_complaints_p9') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfNumberOfConsumerComplaintsP9 contextRef="D_Principle9">
        {{ data.get('assurance_sub_type_for_details_of_number_of_consumer_complaints_p9', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfNumberOfConsumerComplaintsP9>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_performance_and_career_development_reviews_of_employees_and_worker') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfPerformanceAndCareerDevelopmentReviewsOfEmployeesAndWorker contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_details_of_performance_and_career_development_reviews_of_employees_and_worker', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfPerformanceAndCareerDevelopmentReviewsOfEmployeesAndWorker>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_training_given_to_employees_and_workers') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTrainingGivenToEmployeesAndWorkers contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_details_of_training_given_to_employees_and_workers', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTrainingGivenToEmployeesAndWorkers>
    {% endif %}

        {% if data.get('assurance_sub_type_for_employees_and_workers_who_have_been_provided_training_on_human_rights_issues_and_policies_of_the_entity') is not none %}
    <in-capmkt:AssuranceSubTypeForEmployeesAndWorkersWhoHaveBeenProvidedTrainingOnHumanRightsIssuesAndPoliciesOfTheEntity contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_employees_and_workers_who_have_been_provided_training_on_human_rights_issues_and_policies_of_the_entity', '') }}
    </in-capmkt:AssuranceSubTypeForEmployeesAndWorkersWhoHaveBeenProvidedTrainingOnHumanRightsIssuesAndPoliciesOfTheEntity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_job_creation_in_smaller_towns_disclose_wages_paid_to_persons_employed_including_employees_or_workers_employed_on_a_permanent_or_non_permanent_or_on_contract_basis') is not none %}
    <in-capmkt:AssuranceSubTypeForJobCreationInSmallerTownsDiscloseWagesPaidToPersonsEmployedIncludingEmployeesOrWorkersEmployedOnAPermanentOrNonPermanentOrOnContractBasis contextRef="D_Gender_PermanentEmployees_TableA">
        {{ data.get('assurance_sub_type_for_job_creation_in_smaller_towns_disclose_wages_paid_to_persons_employed_including_employees_or_workers_employed_on_a_permanent_or_non_permanent_or_on_contract_basis', '') }}
    </in-capmkt:AssuranceSubTypeForJobCreationInSmallerTownsDiscloseWagesPaidToPersonsEmployedIncludingEmployeesOrWorkersEmployedOnAPermanentOrNonPermanentOrOnContractBasis>
    {% endif %}

        {% if data.get('assurance_sub_type_for_number_of_days_of_accounts_payables') is not none %}
    <in-capmkt:AssuranceSubTypeForNumberOfDaysOfAccountsPayables contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_number_of_days_of_accounts_payables', '') }}
    </in-capmkt:AssuranceSubTypeForNumberOfDaysOfAccountsPayables>
    {% endif %}

        {% if data.get('assurance_sub_type_for_number_of_directors_or_km_ps_or_employees_or_workers_against_whom_disciplinary_action_was_taken_by_any_law_enforcement_agency_for_the_charges_of_bribery_or_corruption') is not none %}
    <in-capmkt:AssuranceSubTypeForNumberOfDirectorsOrKMPsOrEmployeesOrWorkersAgainstWhomDisciplinaryActionWasTakenByAnyLawEnforcementAgencyForTheChargesOfBriberyOrCorruption contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_number_of_directors_or_km_ps_or_employees_or_workers_against_whom_disciplinary_action_was_taken_by_any_law_enforcement_agency_for_the_charges_of_bribery_or_corruption', '') }}
    </in-capmkt:AssuranceSubTypeForNumberOfDirectorsOrKMPsOrEmployeesOrWorkersAgainstWhomDisciplinaryActionWasTakenByAnyLawEnforcementAgencyForTheChargesOfBriberyOrCorruption>
    {% endif %}

        {% if data.get('assurance_sub_type_for_percentage_coverage_by_training_and_awareness_programs_on_any_of_the_principles_during_the_financial_year_for_bod_or_kmp_or_employee_or_worker') is not none %}
    <in-capmkt:AssuranceSubTypeForPercentageCoverageByTrainingAndAwarenessProgramsOnAnyOfThePrinciplesDuringTheFinancialYearForBODOrKMPOrEmployeeOrWorker contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_percentage_coverage_by_training_and_awareness_programs_on_any_of_the_principles_during_the_financial_year_for_bod_or_kmp_or_employee_or_worker', '') }}
    </in-capmkt:AssuranceSubTypeForPercentageCoverageByTrainingAndAwarenessProgramsOnAnyOfThePrinciplesDuringTheFinancialYearForBODOrKMPOrEmployeeOrWorker>
    {% endif %}

        {% if data.get('assurance_sub_type_for_return_to_work_and_retention_rates_of_permanent_employees_and_workers_that_took_parental_leave') is not none %}
    <in-capmkt:AssuranceSubTypeForReturnToWorkAndRetentionRatesOfPermanentEmployeesAndWorkersThatTookParentalLeave contextRef="D_Gender_PermanentEmployees_TableA">
        {{ data.get('assurance_sub_type_for_return_to_work_and_retention_rates_of_permanent_employees_and_workers_that_took_parental_leave', '') }}
    </in-capmkt:AssuranceSubTypeForReturnToWorkAndRetentionRatesOfPermanentEmployeesAndWorkersThatTookParentalLeave>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_is_there_a_mechanism_available_to_receive_and_redress_grievances_for_the_following_categories_of_employees_and_worker') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherIsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_whether_is_there_a_mechanism_available_to_receive_and_redress_grievances_for_the_following_categories_of_employees_and_worker', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherIsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_extend_any_life_insurance_or_any_compensatory_package_in_the_event_of_death_of_employees') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_whether_the_entity_extend_any_life_insurance_or_any_compensatory_package_in_the_event_of_death_of_employees', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_actions_taken_to_mitigate_any_negative_social_impacts_identified_in_the_social_impact_assessments') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfActionsTakenToMitigateAnyNegativeSocialImpactsIdentifiedInTheSocialImpactAssessments contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_actions_taken_to_mitigate_any_negative_social_impacts_identified_in_the_social_impact_assessments', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfActionsTakenToMitigateAnyNegativeSocialImpactsIdentifiedInTheSocialImpactAssessments>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_beneficiaries_of_csr_projects') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfBeneficiariesOfCSRProjects contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_beneficiaries_of_csr_projects', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfBeneficiariesOfCSRProjects>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_csr_projects_undertaken_in_designated_aspirational_districts_as_identified_by_government_bodies') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfCSRProjectsUndertakenInDesignatedAspirationalDistrictsAsIdentifiedByGovernmentBodies contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_csr_projects_undertaken_in_designated_aspirational_districts_as_identified_by_government_bodies', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfCSRProjectsUndertakenInDesignatedAspirationalDistrictsAsIdentifiedByGovernmentBodies>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_environmental_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfEnvironmentalImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLaws contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_environmental_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfEnvironmentalImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLaws>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_social_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfSocialImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLaws contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_social_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfSocialImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLaws>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_have_a_specified_committee_of_the_board_or_director_responsible_for_decision_making_on_sustainability_related_issues') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_have_a_specified_committee_of_the_board_or_director_responsible_for_decision_making_on_sustainability_related_issues', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues>
    {% endif %}

        {% if data.get('assurance_sub_type_for_complaints_or_grievances_on_any_of_the_principles_under_the_national_guidelines_on_responsible_business_conduct') is not none %}
    <in-capmkt:AssuranceSubTypeForComplaintsOrGrievancesOnAnyOfThePrinciplesUnderTheNationalGuidelinesOnResponsibleBusinessConduct contextRef="D_Location">
        {{ data.get('assurance_sub_type_for_complaints_or_grievances_on_any_of_the_principles_under_the_national_guidelines_on_responsible_business_conduct', '') }}
    </in-capmkt:AssuranceSubTypeForComplaintsOrGrievancesOnAnyOfThePrinciplesUnderTheNationalGuidelinesOnResponsibleBusinessConduct>
    {% endif %}

        {% if data.get('assurance_sub_type_for_describe_the_processes_in_place_to_safely_reclaim_your_products_for_reusing_recycling_and_disposing_at_the_end_of_life_for_plastics_including_packaging_e_waste_hazardous_waste_and_other_waste') is not none %}
    <in-capmkt:AssuranceSubTypeForDescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingEWasteHazardousWasteAndOtherWaste contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_describe_the_processes_in_place_to_safely_reclaim_your_products_for_reusing_recycling_and_disposing_at_the_end_of_life_for_plastics_including_packaging_e_waste_hazardous_waste_and_other_waste', '') }}
    </in-capmkt:AssuranceSubTypeForDescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingEWasteHazardousWasteAndOtherWaste>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_a_business_process_being_modified_or_introduced_as_a_result_of_addressing_human_rights_grievances_or_complaints') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaints contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_a_business_process_being_modified_or_introduced_as_a_result_of_addressing_human_rights_grievances_or_complaints', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaints>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_any_corrective_actions_taken_or_underway_on_issues_relating_to_advertising_and_delivery_of_essential_services_or_cyber_security_and_data_privacy_or_recalls_or_penalty_or_action_taken_by_regulatory_authorities_on_safety_of_products_or_services') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServices contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_any_corrective_actions_taken_or_underway_on_issues_relating_to_advertising_and_delivery_of_essential_services_or_cyber_security_and_data_privacy_or_recalls_or_penalty_or_action_taken_by_regulatory_authorities_on_safety_of_products_or_services', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServices>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_business_activities_accounting_for_ninety_percent_of_the_turnover') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfBusinessActivitiesAccountingForNinetyPercentOfTheTurnover contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_business_activities_accounting_for_ninety_percent_of_the_turnover', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfBusinessActivitiesAccountingForNinetyPercentOfTheTurnover>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_instances_of_product_recalls_on_account_of_safety_issues') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfInstancesOfProductRecallsOnAccountOfSafetyIssues contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_instances_of_product_recalls_on_account_of_safety_issues', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfInstancesOfProductRecallsOnAccountOfSafetyIssues>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_percentage_of_recycled_or_reused_input_material_to_total_material_by_value_used_in_production_or_providing_services') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfPercentageOfRecycledOrReusedInputMaterialToTotalMaterialByValueUsedInProductionOrProvidingServices contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_percentage_of_recycled_or_reused_input_material_to_total_material_by_value_used_in_production_or_providing_services', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfPercentageOfRecycledOrReusedInputMaterialToTotalMaterialByValueUsedInProductionOrProvidingServices>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_reclaimed_products_and_their_packaging_materials_for_each_product_category') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfReclaimedProductsAndTheirPackagingMaterialsForEachProductCategory contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_reclaimed_products_and_their_packaging_materials_for_each_product_category', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfReclaimedProductsAndTheirPackagingMaterialsForEachProductCategory>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_significant_social_or_environmental_concerns_from_production_or_disposal_of_product_or_service_with_action_taken_to_mitigate_the_same') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfSignificantSocialOrEnvironmentalConcernsFromProductionOrDisposalOfProductOrServiceWithActionTakenToMitigateTheSame contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_significant_social_or_environmental_concerns_from_production_or_disposal_of_product_or_service_with_action_taken_to_mitigate_the_same', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfSignificantSocialOrEnvironmentalConcernsFromProductionOrDisposalOfProductOrServiceWithActionTakenToMitigateTheSame>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_the_highest_authority_responsible_for_implementation_and_oversight_of_the_business_responsibility_policy') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicy contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_the_highest_authority_responsible_for_implementation_and_oversight_of_the_business_responsibility_policy', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicy>
    {% endif %}

        {% if data.get('assurance_sub_type_for_human_rights_requirements_form_part_of_your_business_agreements_and_contracts') is not none %}
    <in-capmkt:AssuranceSubTypeForHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_human_rights_requirements_form_part_of_your_business_agreements_and_contracts', '') }}
    </in-capmkt:AssuranceSubTypeForHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts>
    {% endif %}

        {% if data.get('assurance_sub_type_for_mechanisms_in_place_to_inform_consumers_of_any_risk_of_disruption_or_discontinuation_of_essential_services') is not none %}
    <in-capmkt:AssuranceSubTypeForMechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServices contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_mechanisms_in_place_to_inform_consumers_of_any_risk_of_disruption_or_discontinuation_of_essential_services', '') }}
    </in-capmkt:AssuranceSubTypeForMechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServices>
    {% endif %}

        {% if data.get('assurance_sub_type_for_overview_of_the_entitys_material_responsible_business_conduct_issues') is not none %}
    <in-capmkt:AssuranceSubTypeForOverviewOfTheEntitysMaterialResponsibleBusinessConductIssues contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_overview_of_the_entitys_material_responsible_business_conduct_issues', '') }}
    </in-capmkt:AssuranceSubTypeForOverviewOfTheEntitysMaterialResponsibleBusinessConductIssues>
    {% endif %}

        {% if data.get('assurance_sub_type_for_percentage_of_contribution_of_exports_in_the_total_turnover_of_the_entity') is not none %}
    <in-capmkt:AssuranceSubTypeForPercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_percentage_of_contribution_of_exports_in_the_total_turnover_of_the_entity', '') }}
    </in-capmkt:AssuranceSubTypeForPercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_percentage_of_value_chain_partners_by_value_of_business_done_with_such_partners_that_were_assessed_for_environmental_impacts') is not none %}
    <in-capmkt:AssuranceSubTypeForPercentageOfValueChainPartnersByValueOfBusinessDoneWithSuchPartnersThatWereAssessedForEnvironmentalImpacts contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_percentage_of_value_chain_partners_by_value_of_business_done_with_such_partners_that_were_assessed_for_environmental_impacts', '') }}
    </in-capmkt:AssuranceSubTypeForPercentageOfValueChainPartnersByValueOfBusinessDoneWithSuchPartnersThatWereAssessedForEnvironmentalImpacts>
    {% endif %}

        {% if data.get('assurance_sub_type_for_products_or_services_sold_by_the_entity_accounting_for_ninety_percent_of_the_turnover') is not none %}
    <in-capmkt:AssuranceSubTypeForProductsOrServicesSoldByTheEntityAccountingForNinetyPercentOfTheTurnover contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_products_or_services_sold_by_the_entity_accounting_for_ninety_percent_of_the_turnover', '') }}
    </in-capmkt:AssuranceSubTypeForProductsOrServicesSoldByTheEntityAccountingForNinetyPercentOfTheTurnover>
    {% endif %}

        {% if data.get('assurance_sub_type_for_statement_by_director_responsible_for_the_business_responsibility_report_highlighting_esg_related_challenges_targets_and_achievements') is not none %}
    <in-capmkt:AssuranceSubTypeForStatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievements contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_statement_by_director_responsible_for_the_business_responsibility_report_highlighting_esg_related_challenges_targets_and_achievements', '') }}
    </in-capmkt:AssuranceSubTypeForStatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievements>
    {% endif %}

        {% if data.get('assurance_sub_type_for_steps_taken_to_inform_and_educate_consumers_about_safe_and_responsible_usage_of_products_and_or_services') is not none %}
    <in-capmkt:AssuranceSubTypeForStepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServices contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_steps_taken_to_inform_and_educate_consumers_about_safe_and_responsible_usage_of_products_and_or_services', '') }}
    </in-capmkt:AssuranceSubTypeForStepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServices>
    {% endif %}

        {% if data.get('assurance_sub_type_for_the_products_and_packaging_reclaimed_at_end_of_life_of_products_amount_reused_or_recycled_or_safely_disposed') is not none %}
    <in-capmkt:AssuranceSubTypeForTheProductsAndPackagingReclaimedAtEndOfLifeOfProductsAmountReusedOrRecycledOrSafelyDisposed contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_the_products_and_packaging_reclaimed_at_end_of_life_of_products_amount_reused_or_recycled_or_safely_disposed', '') }}
    </in-capmkt:AssuranceSubTypeForTheProductsAndPackagingReclaimedAtEndOfLifeOfProductsAmountReusedOrRecycledOrSafelyDisposed>
    {% endif %}

        {% if data.get('assurance_sub_type_for_turnover_of_products_and_or_services_as_a_percentage_of_turnover_from_all_products_or_service_that_carry_information_about_as_a_percentage_to_total_turnover') is not none %}
    <in-capmkt:AssuranceSubTypeForTurnoverOfProductsAndOrServicesAsAPercentageOfTurnoverFromAllProductsOrServiceThatCarryInformationAboutAsAPercentageToTotalTurnover contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_turnover_of_products_and_or_services_as_a_percentage_of_turnover_from_all_products_or_service_that_carry_information_about_as_a_percentage_to_total_turnover', '') }}
    </in-capmkt:AssuranceSubTypeForTurnoverOfProductsAndOrServicesAsAPercentageOfTurnoverFromAllProductsOrServiceThatCarryInformationAboutAsAPercentageToTotalTurnover>
    {% endif %}

        {% if data.get('assurance_sub_type_for_turnover_rate_for_permanent_employees_and_workers_disclose_trends_for_past_three_years') is not none %}
    <in-capmkt:AssuranceSubTypeForTurnoverRateForPermanentEmployeesAndWorkersDiscloseTrendsForPastThreeYears contextRef="D_Gender_PermanentEmployees_TableA">
        {{ data.get('assurance_sub_type_for_turnover_rate_for_permanent_employees_and_workers_disclose_trends_for_past_three_years', '') }}
    </in-capmkt:AssuranceSubTypeForTurnoverRateForPermanentEmployeesAndWorkersDiscloseTrendsForPastThreeYears>
    {% endif %}

        {% if data.get('assurance_sub_type_for_weblink_where_information_on_products_and_services_of_the_entity_can_be_accessed') is not none %}
    <in-capmkt:AssuranceSubTypeForWeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessed contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_weblink_where_information_on_products_and_services_of_the_entity_can_be_accessed', '') }}
    </in-capmkt:AssuranceSubTypeForWeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessed>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_do_you_have_a_focal_point_responsible_for_addressing_human_rights_impacts_or_issues_caused_or_contributed_to_by_the_business') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherDoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_do_you_have_a_focal_point_responsible_for_addressing_human_rights_impacts_or_issues_caused_or_contributed_to_by_the_business', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherDoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_conducted_life_cycle_perspective_or_assessments_for_any_of_its_products_or_for_its_services') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_conducted_life_cycle_perspective_or_assessments_for_any_of_its_products_or_for_its_services', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_display_product_information_on_the_product_over_and_above_what_is_mandated_as_per_local_laws') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_display_product_information_on_the_product_over_and_above_what_is_mandated_as_per_local_laws', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_have_a_business_continuity_and_disaster_management_plan') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveABusinessContinuityAndDisasterManagementPlan contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_have_a_business_continuity_and_disaster_management_plan', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveABusinessContinuityAndDisasterManagementPlan>
    {% endif %}

        {% if data.get('assurance_sub_type_for_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p3') is not none %}
    <in-capmkt:AssuranceSubTypeForAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP3 contextRef="D_Principle3">
        {{ data.get('assurance_sub_type_for_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p3', '') }}
    </in-capmkt:AssuranceSubTypeForAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP3>
    {% endif %}

        {% if data.get('assurance_sub_type_for_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p5') is not none %}
    <in-capmkt:AssuranceSubTypeForAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP5 contextRef="D_Principle5">
        {{ data.get('assurance_sub_type_for_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p5', '') }}
    </in-capmkt:AssuranceSubTypeForAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP5>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_of_your_plants_and_offices_that_were_assessed') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessed contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_of_your_plants_and_offices_that_were_assessed', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessed>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_plant_and_office') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOffice contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_plant_and_office', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOffice>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_number_of_locations_where_plants_and_or_operations_or_offices_of_the_entity_are_situated') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfNumberOfLocationsWherePlantsAndOrOperationsOrOfficesOfTheEntityAreSituated contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_number_of_locations_where_plants_and_or_operations_or_offices_of_the_entity_are_situated', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfNumberOfLocationsWherePlantsAndOrOperationsOrOfficesOfTheEntityAreSituated>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_operations_or_offices_in_or_around_ecologically_sensitive_areas_where_environmental_approvals_or_clearances_are_required') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfOperationsOrOfficesInOrAroundEcologicallySensitiveAreasWhereEnvironmentalApprovalsOrClearancesAreRequired contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_operations_or_offices_in_or_around_ecologically_sensitive_areas_where_environmental_approvals_or_clearances_are_required', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfOperationsOrOfficesInOrAroundEcologicallySensitiveAreasWhereEnvironmentalApprovalsOrClearancesAreRequired>
    {% endif %}

        {% if data.get('assurance_sub_type_for_name_of_the_national_and_international_codes_or_certifications_or_labels_or_standards_adopted_by_your_entity_and_mapped_to_each_principle') is not none %}
    <in-capmkt:AssuranceSubTypeForNameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrinciple contextRef="D_Location">
        {{ data.get('assurance_sub_type_for_name_of_the_national_and_international_codes_or_certifications_or_labels_or_standards_adopted_by_your_entity_and_mapped_to_each_principle', '') }}
    </in-capmkt:AssuranceSubTypeForNameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrinciple>
    {% endif %}

        {% if data.get('assurance_sub_type_for_number_of_locations_where_markets_served_by_the_entity') is not none %}
    <in-capmkt:AssuranceSubTypeForNumberOfLocationsWhereMarketsServedByTheEntity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_number_of_locations_where_markets_served_by_the_entity', '') }}
    </in-capmkt:AssuranceSubTypeForNumberOfLocationsWhereMarketsServedByTheEntity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_the_premises_or_offices_of_the_entity_accessible_to_differently_abled_employees_and_workers_and_steps_are_being_taken_by_the_entity_if_the_premises_or_offices_of_the_entity_not_accessible') is not none %}
    <in-capmkt:AssuranceSubTypeForThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkersAndStepsAreBeingTakenByTheEntityIfThePremisesOrOfficesOfTheEntityNotAccessible contextRef="D_Gender_Employees_TableA">
        {{ data.get('assurance_sub_type_for_the_premises_or_offices_of_the_entity_accessible_to_differently_abled_employees_and_workers_and_steps_are_being_taken_by_the_entity_if_the_premises_or_offices_of_the_entity_not_accessible', '') }}
    </in-capmkt:AssuranceSubTypeForThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkersAndStepsAreBeingTakenByTheEntityIfThePremisesOrOfficesOfTheEntityNotAccessible>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_premise_or_office_of_the_entity_accessible_to_differently_abled_visitors_as_per_the_requirements_of_the_rights_of_persons_with_disabilities_act2016') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_premise_or_office_of_the_entity_accessible_to_differently_abled_visitors_as_per_the_requirements_of_the_rights_of_persons_with_disabilities_act2016', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016>
    {% endif %}

        {% if data.get('assurance_sub_type_for_markets_served_by_the_entity') is not none %}
    <in-capmkt:AssuranceSubTypeForMarketsServedByTheEntity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_markets_served_by_the_entity', '') }}
    </in-capmkt:AssuranceSubTypeForMarketsServedByTheEntity>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_have_any_project_related_to_reducing_green_house_gas_emission') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityHaveAnyProjectRelatedToReducingGreenHouseGasEmission contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_have_any_project_related_to_reducing_green_house_gas_emission') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityHaveAnyProjectRelatedToReducingGreenHouseGasEmission>
    {% endif %}

        {% if data.get('contact_number_of_auditor') is not none %}
    <in-capmkt:ContactNumberOfAuditor contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('contact_number_of_auditor', '') }}
    </in-capmkt:ContactNumberOfAuditor>
    {% endif %}

        {% if data.get('country_of_other_stock_exchange') is not none %}
    <in-capmkt:CountryOfOtherStockExchange contextRef="DCYMain">
        {{ data.get('country_of_other_stock_exchange', '') }}
    </in-capmkt:CountryOfOtherStockExchange>
    {% endif %}

        {% if data.get('debentures_excluding_refinancing') is not none %}
    <in-capmkt:DebenturesExcludingRefinancing contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('debentures_excluding_refinancing', '') }}
    </in-capmkt:DebenturesExcludingRefinancing>
    {% endif %}

        {% if data.get('debt_servicing') is not none %}
    <in-capmkt:DebtServicing contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('debt_servicing', '') }}
    </in-capmkt:DebtServicing>
    {% endif %}

        {% if data.get('description_of_other_stock_exchange_where_the_company_is_listed') is not none %}
    <in-capmkt:DescriptionOfOtherStockExchangeWhereTheCompanyIsListed contextRef="DCYMain">
        {{ data.get('description_of_other_stock_exchange_where_the_company_is_listed', '') }}
    </in-capmkt:DescriptionOfOtherStockExchangeWhereTheCompanyIsListed>
    {% endif %}

        {% if data.get('email_id_of_auditor') is not none %}
    <in-capmkt:EmailIDOfAuditor contextRef="ICYMain">
        {{ data.get('email_id_of_auditor', '') }}
    </in-capmkt:EmailIDOfAuditor>
    {% endif %}

        {% if data.get('have_there_been_defaults_or_delays_in_servicing_any_other_debt_security_issued_by_the_issuer') is not none %}
    <in-capmkt:HaveThereBeenDefaultsOrDelaysInServicingAnyOtherDebtSecurityIssuedByTheIssuer contextRef="DCYMain">
        {{ 'true' if data.get('have_there_been_defaults_or_delays_in_servicing_any_other_debt_security_issued_by_the_issuer') else 'false' }}
    </in-capmkt:HaveThereBeenDefaultsOrDelaysInServicingAnyOtherDebtSecurityIssuedByTheIssuer>
    {% endif %}

        {% if data.get('liabilities_excluding_refinancing') is not none %}
    <in-capmkt:LiabilitiesExcludingRefinancing contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('liabilities_excluding_refinancing', '') }}
    </in-capmkt:LiabilitiesExcludingRefinancing>
    {% endif %}

        {% if data.get('net_debt_repayment_excluding_refinancing') is not none %}
    <in-capmkt:NetDebtRepaymentExcludingRefinancing contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('net_debt_repayment_excluding_refinancing', '') }}
    </in-capmkt:NetDebtRepaymentExcludingRefinancing>
    {% endif %}

        {% if data.get('other_obligations_excluding_refinancing') is not none %}
    <in-capmkt:OtherObligationsExcludingRefinancing contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_obligations_excluding_refinancing', '') }}
    </in-capmkt:OtherObligationsExcludingRefinancing>
    {% endif %}

        {% if data.get('other_such_instrument_excluding_refinancing') is not none %}
    <in-capmkt:OtherSuchInstrumentExcludingRefinancing contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_such_instrument_excluding_refinancing', '') }}
    </in-capmkt:OtherSuchInstrumentExcludingRefinancing>
    {% endif %}

        {% if data.get('pan_of_auditor') is not none %}
    <in-capmkt:PANOfAuditor contextRef="DCYMain">
        {{ data.get('pan_of_auditor', '') }}
    </in-capmkt:PANOfAuditor>
    {% endif %}

        {% if data.get('pan_of_client') is not none %}
    <in-capmkt:PANOfClient contextRef="DCYMain">
        {{ data.get('pan_of_client', '') }}
    </in-capmkt:PANOfClient>
    {% endif %}

        {% if data.get('premiums_excluding_refinancing') is not none %}
    <in-capmkt:PremiumsExcludingRefinancing contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('premiums_excluding_refinancing', '') }}
    </in-capmkt:PremiumsExcludingRefinancing>
    {% endif %}

        {% if data.get('redemption_of_preference_shares_excluding_refinancing') is not none %}
    <in-capmkt:RedemptionOfPreferenceSharesExcludingRefinancing contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('redemption_of_preference_shares_excluding_refinancing', '') }}
    </in-capmkt:RedemptionOfPreferenceSharesExcludingRefinancing>
    {% endif %}

        {% if data.get('total_revenue_of_the_company') is not none %}
    <in-capmkt:TotalRevenueOfTheCompany contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('total_revenue_of_the_company', '') }}
    </in-capmkt:TotalRevenueOfTheCompany>
    {% endif %}

        {% if data.get('type_of_assurance_for_details_of_holding_subsidiary_and_associate_companies_including_joint_ventures') is not none %}
    <in-capmkt:TypeOfAssuranceForDetailsOfHoldingSubsidiaryAndAssociateCompaniesIncludingJointVentures contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_details_of_holding_subsidiary_and_associate_companies_including_joint_ventures', '') }}
    </in-capmkt:TypeOfAssuranceForDetailsOfHoldingSubsidiaryAndAssociateCompaniesIncludingJointVentures>
    {% endif %}

        {% if data.get('type_of_assurance_for_governance_leadership_and_oversight') is not none %}
    <in-capmkt:TypeOfAssuranceForGovernanceLeadershipAndOversight contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_governance_leadership_and_oversight', '') }}
    </in-capmkt:TypeOfAssuranceForGovernanceLeadershipAndOversight>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_is_there_a_mechanism_available_to_receive_and_redress_grievances_for_the_following_categories_of_employees_and_worker') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherIsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('assurer_has_assured_whether_is_there_a_mechanism_available_to_receive_and_redress_grievances_for_the_following_categories_of_employees_and_worker') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherIsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_extend_any_life_insurance_or_any_compensatory_package_in_the_event_of_death_of_employees') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_extend_any_life_insurance_or_any_compensatory_package_in_the_event_of_death_of_employees') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees>
    {% endif %}

        {% if data.get('cash_and_cash_equivalent_other_than_unclaimed_dividend_including_short_term_treasury_investments') is not none %}
    <in-capmkt:CashAndCashEquivalentOtherThanUnclaimedDividendIncludingShortTermTreasuryInvestments contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('cash_and_cash_equivalent_other_than_unclaimed_dividend_including_short_term_treasury_investments', '') }}
    </in-capmkt:CashAndCashEquivalentOtherThanUnclaimedDividendIncludingShortTermTreasuryInvestments>
    {% endif %}

        {% if data.get('processes_for_workers_to_report_the_work_related_hazards_and_to_remove_themselves_from_such_risks_is_not_applicable_explanatory_text_block') is not none %}
    <in-capmkt:ProcessesForWorkersToReportTheWorkRelatedHazardsAndToRemoveThemselvesFromSuchRisksIsNotApplicableExplanatoryTextBlock contextRef="D_Gender_Workers_TableA" escape="true">
        {{ data.get('processes_for_workers_to_report_the_work_related_hazards_and_to_remove_themselves_from_such_risks_is_not_applicable_explanatory_text_block', '') }}
    </in-capmkt:ProcessesForWorkersToReportTheWorkRelatedHazardsAndToRemoveThemselvesFromSuchRisksIsNotApplicableExplanatoryTextBlock>
    {% endif %}

        {% if data.get('registration_number_of_audit_firm') is not none %}
    <in-capmkt:RegistrationNumberOfAuditFirm contextRef="ICYMain">
        {{ data.get('registration_number_of_audit_firm', '') }}
    </in-capmkt:RegistrationNumberOfAuditFirm>
    {% endif %}

        {% if data.get('registration_number_of_auditor') is not none %}
    <in-capmkt:RegistrationNumberOfAuditor contextRef="ICYMain">
        {{ data.get('registration_number_of_auditor', '') }}
    </in-capmkt:RegistrationNumberOfAuditor>
    {% endif %}

        {% if data.get('type_of_assurance_for_details_of_employees') is not none %}
    <in-capmkt:TypeOfAssuranceForDetailsOfEmployees contextRef="D_Gender_Employees_TableA">
        {{ data.get('type_of_assurance_for_details_of_employees', '') }}
    </in-capmkt:TypeOfAssuranceForDetailsOfEmployees>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_have_a_specified_committee_of_the_board_or_director_responsible_for_decision_making_on_sustainability_related_issues') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_have_a_specified_committee_of_the_board_or_director_responsible_for_decision_making_on_sustainability_related_issues') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues>
    {% endif %}

        {% if data.get('csr_project') is not none %}
    <in-capmkt:CSRProject contextRef="DCYMain">
        {{ data.get('csr_project', '') }}
    </in-capmkt:CSRProject>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_a_specified_committee_for_decision_making_on_sustainability_related_issues_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableASpecifiedCommitteeForDecisionMakingOnSustainabilityRelatedIssuesExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_a_specified_committee_for_decision_making_on_sustainability_related_issues_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableASpecifiedCommitteeForDecisionMakingOnSustainabilityRelatedIssuesExplanatoryTextBlock>
    {% endif %}

        {% if data.get('type_of_assurance_for_details_of_csr') is not none %}
    <in-capmkt:TypeOfAssuranceForDetailsOfCSR contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_details_of_csr', '') }}
    </in-capmkt:TypeOfAssuranceForDetailsOfCSR>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_do_you_have_a_focal_point_responsible_for_addressing_human_rights_impacts_or_issues_caused_or_contributed_to_by_the_business') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherDoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_do_you_have_a_focal_point_responsible_for_addressing_human_rights_impacts_or_issues_caused_or_contributed_to_by_the_business') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherDoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_conducted_life_cycle_perspective_or_assessments_for_any_of_its_products_or_for_its_services') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_conducted_life_cycle_perspective_or_assessments_for_any_of_its_products_or_for_its_services') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_display_product_information_on_the_product_over_and_above_what_is_mandated_as_per_local_laws') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_display_product_information_on_the_product_over_and_above_what_is_mandated_as_per_local_laws') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_have_a_business_continuity_and_disaster_management_plan') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityHaveABusinessContinuityAndDisasterManagementPlan contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_have_a_business_continuity_and_disaster_management_plan') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityHaveABusinessContinuityAndDisasterManagementPlan>
    {% endif %}

        {% if data.get('debt_service_coverage_ratio') is not none %}
    <in-capmkt:DebtServiceCoverageRatio contextRef="DCYMain">
        {{ data.get('debt_service_coverage_ratio', '') }}
    </in-capmkt:DebtServiceCoverageRatio>
    {% endif %}

        {% if data.get('did_your_entity_carry_out_any_survey_with_regard_to_consumer_satisfaction_relating_to_the_major_products_or_services_of_the_entity_significant_locations_of_operation_of_the_entity_or_the_entity_as_a_whole') is not none %}
    <in-capmkt:DidYourEntityCarryOutAnySurveyWithRegardToConsumerSatisfactionRelatingToTheMajorProductsOrServicesOfTheEntitySignificantLocationsOfOperationOfTheEntityOrTheEntityAsAWhole contextRef="DCYMain">
        {{ data.get('did_your_entity_carry_out_any_survey_with_regard_to_consumer_satisfaction_relating_to_the_major_products_or_services_of_the_entity_significant_locations_of_operation_of_the_entity_or_the_entity_as_a_whole', '') }}
    </in-capmkt:DidYourEntityCarryOutAnySurveyWithRegardToConsumerSatisfactionRelatingToTheMajorProductsOrServicesOfTheEntitySignificantLocationsOfOperationOfTheEntityOrTheEntityAsAWhole>
    {% endif %}

        {% if data.get('human_rights_requirements_form_part_of_your_business_agreements_and_contracts_is_not_applicable_explanatory_text_block') is not none %}
    <in-capmkt:HumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContractsIsNotApplicableExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('human_rights_requirements_form_part_of_your_business_agreements_and_contracts_is_not_applicable_explanatory_text_block', '') }}
    </in-capmkt:HumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContractsIsNotApplicableExplanatoryTextBlock>
    {% endif %}

        {% if data.get('interest_service_coverage_ratio') is not none %}
    <in-capmkt:InterestServiceCoverageRatio contextRef="DCYMain">
        {{ data.get('interest_service_coverage_ratio', '') }}
    </in-capmkt:InterestServiceCoverageRatio>
    {% endif %}

        {% if data.get('nic_code_of_product_or_service_of_conducted_lifecycle_perspective') is not none %}
    <in-capmkt:NICCodeOfProductOrServiceOfConductedLifecyclePerspective contextRef="DCYMain">
        {{ data.get('nic_code_of_product_or_service_of_conducted_lifecycle_perspective', '') }}
    </in-capmkt:NICCodeOfProductOrServiceOfConductedLifecyclePerspective>
    {% endif %}

        {% if data.get('name_of_product_or_service_of_conducted_lifecycle_perspective') is not none %}
    <in-capmkt:NameOfProductOrServiceOfConductedLifecyclePerspective contextRef="DCYMain">
        {{ data.get('name_of_product_or_service_of_conducted_lifecycle_perspective', '') }}
    </in-capmkt:NameOfProductOrServiceOfConductedLifecyclePerspective>
    {% endif %}

        {% if data.get('the_entity_does_not_consider_the_principles_material_to_its_business') is not none %}
    <in-capmkt:TheEntityDoesNotConsiderThePrinciplesMaterialToItsBusiness contextRef="DCYMain">
        {{ 'true' if data.get('the_entity_does_not_consider_the_principles_material_to_its_business') else 'false' }}
    </in-capmkt:TheEntityDoesNotConsiderThePrinciplesMaterialToItsBusiness>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_a_business_continuity_and_disaster_management_plan_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableABusinessContinuityAndDisasterManagementPlanExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_a_business_continuity_and_disaster_management_plan_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableABusinessContinuityAndDisasterManagementPlanExplanatoryTextBlock>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_carry_out_any_survey_with_regard_to_consumer_satisfaction_relating_to_the_major_products_or_services_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableCarryOutAnySurveyWithRegardToConsumerSatisfactionRelatingToTheMajorProductsOrServicesExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_carry_out_any_survey_with_regard_to_consumer_satisfaction_relating_to_the_major_products_or_services_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableCarryOutAnySurveyWithRegardToConsumerSatisfactionRelatingToTheMajorProductsOrServicesExplanatoryTextBlock>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_conducted_life_cycle_perspective_or_assessments_for_any_of_its_products_or_for_its_services_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServicesExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_conducted_life_cycle_perspective_or_assessments_for_any_of_its_products_or_for_its_services_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServicesExplanatoryTextBlock>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_product_information_on_the_product_over_and_above_what_is_mandated_as_per_local_laws_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLawsExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_product_information_on_the_product_over_and_above_what_is_mandated_as_per_local_laws_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLawsExplanatoryTextBlock>
    {% endif %}

        {% if data.get('total_scope3_emissions_per_rupee_of_turnover') is not none %}
    <in-capmkt:TotalScope3EmissionsPerRupeeOfTurnover contextRef="DCYMain">
        {{ data.get('total_scope3_emissions_per_rupee_of_turnover', '') }}
    </in-capmkt:TotalScope3EmissionsPerRupeeOfTurnover>
    {% endif %}

        {% if data.get('type_of_assurance_for_details_of_products_or_services') is not none %}
    <in-capmkt:TypeOfAssuranceForDetailsOfProductsOrServices contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_details_of_products_or_services', '') }}
    </in-capmkt:TypeOfAssuranceForDetailsOfProductsOrServices>
    {% endif %}

        {% if data.get('unit_of_total_scope1_and_scope2_emissions_per_rupee_of_turnover') is not none %}
    <in-capmkt:UnitOfTotalScope1AndScope2EmissionsPerRupeeOfTurnover contextRef="DCYMain">
        {{ data.get('unit_of_total_scope1_and_scope2_emissions_per_rupee_of_turnover', '') }}
    </in-capmkt:UnitOfTotalScope1AndScope2EmissionsPerRupeeOfTurnover>
    {% endif %}

        {% if data.get('unit_of_total_scope3_emissions_per_rupee_of_turnover') is not none %}
    <in-capmkt:UnitOfTotalScope3EmissionsPerRupeeOfTurnover contextRef="DCYMain">
        {{ data.get('unit_of_total_scope3_emissions_per_rupee_of_turnover', '') }}
    </in-capmkt:UnitOfTotalScope3EmissionsPerRupeeOfTurnover>
    {% endif %}

        {% if data.get('water_intensity_per_rupee_of_turnover_per_area') is not none %}
    <in-capmkt:WaterIntensityPerRupeeOfTurnoverPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_intensity_per_rupee_of_turnover_per_area', '') }}
    </in-capmkt:WaterIntensityPerRupeeOfTurnoverPerArea>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_premise_or_office_of_the_entity_accessible_to_differently_abled_visitors_as_per_the_requirements_of_the_rights_of_persons_with_disabilities_act2016') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_premise_or_office_of_the_entity_accessible_to_differently_abled_visitors_as_per_the_requirements_of_the_rights_of_persons_with_disabilities_act2016') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016>
    {% endif %}

        {% if data.get('location_of_operations_or_offices') is not none %}
    <in-capmkt:LocationOfOperationsOrOffices contextRef="DCYMain">
        {{ data.get('location_of_operations_or_offices', '') }}
    </in-capmkt:LocationOfOperationsOrOffices>
    {% endif %}

        {% if data.get('proceeds_from_sale_of_investments_or_assets_or_sale_of_shares_of_sp_vs_not_distributed_pursuant_to_an_earlier_plan_to_re_invest_as_per_regulation1816_d_of_the_reitinvit_regulations_if_such_proceeds_are_not_intended_to_be_invested_subsequently') is not none %}
    <in-capmkt:ProceedsFromSaleOfInvestmentsOrAssetsOrSaleOfSharesOfSPVsNotDistributedPursuantToAnEarlierPlanToReInvestAsPerRegulation1816DOfTheREITINVITRegulationsIfSuchProceedsAreNotIntendedToBeInvestedSubsequently contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('proceeds_from_sale_of_investments_or_assets_or_sale_of_shares_of_sp_vs_not_distributed_pursuant_to_an_earlier_plan_to_re_invest_as_per_regulation1816_d_of_the_reitinvit_regulations_if_such_proceeds_are_not_intended_to_be_invested_subsequently', '') }}
    </in-capmkt:ProceedsFromSaleOfInvestmentsOrAssetsOrSaleOfSharesOfSPVsNotDistributedPursuantToAnEarlierPlanToReInvestAsPerRegulation1816DOfTheREITINVITRegulationsIfSuchProceedsAreNotIntendedToBeInvestedSubsequently>
    {% endif %}

        {% if data.get('the_premises_or_offices_of_the_entity_accessible_to_differently_abled_employees_and_workers_are_not_applicable_explanatory_text_block') is not none %}
    <in-capmkt:ThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkersAreNotApplicableExplanatoryTextBlock contextRef="D_Gender_Employees_TableA" escape="true">
        {{ data.get('the_premises_or_offices_of_the_entity_accessible_to_differently_abled_employees_and_workers_are_not_applicable_explanatory_text_block', '') }}
    </in-capmkt:ThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkersAreNotApplicableExplanatoryTextBlock>
    {% endif %}

        {% if data.get('level_of_rounding_used_in_financial_statements') is not none %}
    <in-capmkt:LevelOfRoundingUsedInFinancialStatements contextRef="DCYMain">
        {{ data.get('level_of_rounding_used_in_financial_statements', '') }}
    </in-capmkt:LevelOfRoundingUsedInFinancialStatements>
    {% endif %}

        {% if data.get('state_of_project') is not none %}
    <in-capmkt:StateOfProject contextRef="DCYMain">
        {{ data.get('state_of_project', '') }}
    </in-capmkt:StateOfProject>
    {% endif %}

        {% if data.get('number_of_active_corporate_clients_during_audit_period') is not none %}
    <in-capmkt:NumberOfActiveCorporateClientsDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_active_corporate_clients_during_audit_period', '') }}
    </in-capmkt:NumberOfActiveCorporateClientsDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_corporate_clients_registered_during_audit_period') is not none %}
    <in-capmkt:NumberOfCorporateClientsRegisteredDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_corporate_clients_registered_during_audit_period', '') }}
    </in-capmkt:NumberOfCorporateClientsRegisteredDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_a_ps_inspected_during_the_audit_period') is not none %}
    <in-capmkt:NumberOfAPsInspectedDuringTheAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_a_ps_inspected_during_the_audit_period', '') }}
    </in-capmkt:NumberOfAPsInspectedDuringTheAuditPeriod>
    {% endif %}

        {% if data.get('number_of_active_clients_during_audit_period') is not none %}
    <in-capmkt:NumberOfActiveClientsDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_active_clients_during_audit_period', '') }}
    </in-capmkt:NumberOfActiveClientsDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_active_clients_who_are_trust_during_audit_period') is not none %}
    <in-capmkt:NumberOfActiveClientsWhoAreTrustDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_active_clients_who_are_trust_during_audit_period', '') }}
    </in-capmkt:NumberOfActiveClientsWhoAreTrustDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_active_individual_clients_during_audit_period') is not none %}
    <in-capmkt:NumberOfActiveIndividualClientsDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_active_individual_clients_during_audit_period', '') }}
    </in-capmkt:NumberOfActiveIndividualClientsDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_active_institutional_clients_during_audit_period') is not none %}
    <in-capmkt:NumberOfActiveInstitutionalClientsDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_active_institutional_clients_during_audit_period', '') }}
    </in-capmkt:NumberOfActiveInstitutionalClientsDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_active_other_clients_during_audit_period') is not none %}
    <in-capmkt:NumberOfActiveOtherClientsDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_active_other_clients_during_audit_period', '') }}
    </in-capmkt:NumberOfActiveOtherClientsDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_active_partnership_clients_during_audit_period') is not none %}
    <in-capmkt:NumberOfActivePartnershipClientsDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_active_partnership_clients_during_audit_period', '') }}
    </in-capmkt:NumberOfActivePartnershipClientsDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_active_retail_clients_during_audit_period') is not none %}
    <in-capmkt:NumberOfActiveRetailClientsDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_active_retail_clients_during_audit_period', '') }}
    </in-capmkt:NumberOfActiveRetailClientsDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_bank_accounts_operated_during_the_audit_period') is not none %}
    <in-capmkt:NumberOfBankAccountsOperatedDuringTheAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_bank_accounts_operated_during_the_audit_period', '') }}
    </in-capmkt:NumberOfBankAccountsOperatedDuringTheAuditPeriod>
    {% endif %}

        {% if data.get('number_of_branches_at_the_beginning_of_the_audit_period') is not none %}
    <in-capmkt:NumberOfBranchesAtTheBeginningOfTheAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_branches_at_the_beginning_of_the_audit_period', '') }}
    </in-capmkt:NumberOfBranchesAtTheBeginningOfTheAuditPeriod>
    {% endif %}

        {% if data.get('number_of_branches_closed_during_the_audit_period') is not none %}
    <in-capmkt:NumberOfBranchesClosedDuringTheAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_branches_closed_during_the_audit_period', '') }}
    </in-capmkt:NumberOfBranchesClosedDuringTheAuditPeriod>
    {% endif %}

        {% if data.get('number_of_branches_inspected_during_the_audit_period') is not none %}
    <in-capmkt:NumberOfBranchesInspectedDuringTheAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_branches_inspected_during_the_audit_period', '') }}
    </in-capmkt:NumberOfBranchesInspectedDuringTheAuditPeriod>
    {% endif %}

        {% if data.get('number_of_branches_opened_during_the_audit_period') is not none %}
    <in-capmkt:NumberOfBranchesOpenedDuringTheAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_branches_opened_during_the_audit_period', '') }}
    </in-capmkt:NumberOfBranchesOpenedDuringTheAuditPeriod>
    {% endif %}

        {% if data.get('number_of_client_in_sampling_criteria') is not none %}
    <in-capmkt:NumberOfClientInSamplingCriteria contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_client_in_sampling_criteria', '') }}
    </in-capmkt:NumberOfClientInSamplingCriteria>
    {% endif %}

        {% if data.get('number_of_clients_registered_during_the_audit_period') is not none %}
    <in-capmkt:NumberOfClientsRegisteredDuringTheAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_clients_registered_during_the_audit_period', '') }}
    </in-capmkt:NumberOfClientsRegisteredDuringTheAuditPeriod>
    {% endif %}

        {% if data.get('number_of_clients_who_are_trust_registered_during_audit_period') is not none %}
    <in-capmkt:NumberOfClientsWhoAreTrustRegisteredDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_clients_who_are_trust_registered_during_audit_period', '') }}
    </in-capmkt:NumberOfClientsWhoAreTrustRegisteredDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_dp_accounts_operated_during_the_audit_period') is not none %}
    <in-capmkt:NumberOfDPAccountsOperatedDuringTheAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_dp_accounts_operated_during_the_audit_period', '') }}
    </in-capmkt:NumberOfDPAccountsOperatedDuringTheAuditPeriod>
    {% endif %}

        {% if data.get('number_of_dates_to_be_verified') is not none %}
    <in-capmkt:NumberOfDatesToBeVerified contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_dates_to_be_verified', '') }}
    </in-capmkt:NumberOfDatesToBeVerified>
    {% endif %}

        {% if data.get('number_of_individual_clients_registered_during_audit_period') is not none %}
    <in-capmkt:NumberOfIndividualClientsRegisteredDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_individual_clients_registered_during_audit_period', '') }}
    </in-capmkt:NumberOfIndividualClientsRegisteredDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_instances_where_non_compliance_observed') is not none %}
    <in-capmkt:NumberOfInstancesWhereNonComplianceObserved contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_instances_where_non_compliance_observed', '') }}
    </in-capmkt:NumberOfInstancesWhereNonComplianceObserved>
    {% endif %}

        {% if data.get('number_of_institutional_clients_registered_during_audit_period') is not none %}
    <in-capmkt:NumberOfInstitutionalClientsRegisteredDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_institutional_clients_registered_during_audit_period', '') }}
    </in-capmkt:NumberOfInstitutionalClientsRegisteredDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_other_clients_registered_during_audit_period') is not none %}
    <in-capmkt:NumberOfOtherClientsRegisteredDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_other_clients_registered_during_audit_period', '') }}
    </in-capmkt:NumberOfOtherClientsRegisteredDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_partnership_clients_registered_during_audit_period') is not none %}
    <in-capmkt:NumberOfPartnershipClientsRegisteredDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_partnership_clients_registered_during_audit_period', '') }}
    </in-capmkt:NumberOfPartnershipClientsRegisteredDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_persons_benefitted_from_csr_projects') is not none %}
    <in-capmkt:NumberOfPersonsBenefittedFromCSRProjects contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_persons_benefitted_from_csr_projects', '') }}
    </in-capmkt:NumberOfPersonsBenefittedFromCSRProjects>
    {% endif %}

        {% if data.get('number_of_project_affected_families') is not none %}
    <in-capmkt:NumberOfProjectAffectedFamilies contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_project_affected_families', '') }}
    </in-capmkt:NumberOfProjectAffectedFamilies>
    {% endif %}

        {% if data.get('number_of_retail_clients_registered_during_audit_period') is not none %}
    <in-capmkt:NumberOfRetailClientsRegisteredDuringAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_retail_clients_registered_during_audit_period', '') }}
    </in-capmkt:NumberOfRetailClientsRegisteredDuringAuditPeriod>
    {% endif %}

        {% if data.get('number_of_sub_brokers_inspected_during_the_audit_period') is not none %}
    <in-capmkt:NumberOfSubBrokersInspectedDuringTheAuditPeriod contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_sub_brokers_inspected_during_the_audit_period', '') }}
    </in-capmkt:NumberOfSubBrokersInspectedDuringTheAuditPeriod>
    {% endif %}

        {% if data.get('number_of_sub_points_where_the_auditor_has_filled_nc') is not none %}
    <in-capmkt:NumberOfSubPointsWhereTheAuditorHasFilledNC contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('number_of_sub_points_where_the_auditor_has_filled_nc', '') }}
    </in-capmkt:NumberOfSubPointsWhereTheAuditorHasFilledNC>
    {% endif %}

        {% if data.get('number_of_units_outstanding') is not none %}
    <in-capmkt:NumberOfUnitsOutstanding contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('number_of_units_outstanding', '') }}
    </in-capmkt:NumberOfUnitsOutstanding>
    {% endif %}

        {% if data.get('number_of_well_being_of_employees') is not none %}
    <in-capmkt:NumberOfWellBeingOfEmployees contextRef="D_Gender_Employees_TableA" unitRef="pure" decimals="2">
        {{ data.get('number_of_well_being_of_employees', '') }}
    </in-capmkt:NumberOfWellBeingOfEmployees>
    {% endif %}

        {% if data.get('number_of_well_being_of_workers') is not none %}
    <in-capmkt:NumberOfWellBeingOfWorkers contextRef="D_Gender_Workers_TableA" unitRef="pure" decimals="2">
        {{ data.get('number_of_well_being_of_workers', '') }}
    </in-capmkt:NumberOfWellBeingOfWorkers>
    {% endif %}

        {% if data.get('percentage_of_cost_incurred_on_well_being_measures_with_respect_to_total_revenue_of_the_company') is not none %}
    <in-capmkt:PercentageOfCostIncurredOnWellBeingMeasuresWithRespectToTotalRevenueOfTheCompany contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_cost_incurred_on_well_being_measures_with_respect_to_total_revenue_of_the_company', '') }}
    </in-capmkt:PercentageOfCostIncurredOnWellBeingMeasuresWithRespectToTotalRevenueOfTheCompany>
    {% endif %}

        {% if data.get('percentage_of_well_being_of_employees') is not none %}
    <in-capmkt:PercentageOfWellBeingOfEmployees contextRef="D_Gender_Employees_TableA" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_well_being_of_employees', '') }}
    </in-capmkt:PercentageOfWellBeingOfEmployees>
    {% endif %}

        {% if data.get('percentage_of_well_being_of_workers') is not none %}
    <in-capmkt:PercentageOfWellBeingOfWorkers contextRef="D_Gender_Workers_TableA" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_well_being_of_workers', '') }}
    </in-capmkt:PercentageOfWellBeingOfWorkers>
    {% endif %}

        {% if data.get('percentage_of_holding') is not none %}
    <in-capmkt:PercentageOfHolding contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_holding', '') }}
    </in-capmkt:PercentageOfHolding>
    {% endif %}

        {% if data.get('percentage_of_total_turnover_contributed_for_conducted_lifecycle_perspective') is not none %}
    <in-capmkt:PercentageOfTotalTurnoverContributedForConductedLifecyclePerspective contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_total_turnover_contributed_for_conducted_lifecycle_perspective', '') }}
    </in-capmkt:PercentageOfTotalTurnoverContributedForConductedLifecyclePerspective>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_address_of_corporate_office_of_company') is not none %}
    <in-capmkt:RemarksForAssuranceOfAddressOfCorporateOfficeOfCompany contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_address_of_corporate_office_of_company', '') }}
    </in-capmkt:RemarksForAssuranceOfAddressOfCorporateOfficeOfCompany>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_address_of_registered_office_of_company') is not none %}
    <in-capmkt:RemarksForAssuranceOfAddressOfRegisteredOfficeOfCompany contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_address_of_registered_office_of_company', '') }}
    </in-capmkt:RemarksForAssuranceOfAddressOfRegisteredOfficeOfCompany>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_corporate_identity_number') is not none %}
    <in-capmkt:RemarksForAssuranceOfCorporateIdentityNumber contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_corporate_identity_number', '') }}
    </in-capmkt:RemarksForAssuranceOfCorporateIdentityNumber>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_the_stock_exchange_where_the_company_is_listed') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTheStockExchangeWhereTheCompanyIsListed contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_the_stock_exchange_where_the_company_is_listed', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTheStockExchangeWhereTheCompanyIsListed>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_waste_management_practices_adopted_in_your_establishments_and_the_strategy_adopted_by_company_to_reduce_usage_of_hazardous_and_toxic_chemicals') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicals contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_waste_management_practices_adopted_in_your_establishments_and_the_strategy_adopted_by_company_to_reduce_usage_of_hazardous_and_toxic_chemicals', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicals>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_e_mail_of_the_company') is not none %}
    <in-capmkt:RemarksForAssuranceOfEMailOfTheCompany contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_e_mail_of_the_company', '') }}
    </in-capmkt:RemarksForAssuranceOfEMailOfTheCompany>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_name_and_contact_details_of_the_contact_person_in_case_of_any_queries_on_the_brsr_report') is not none %}
    <in-capmkt:RemarksForAssuranceOfNameAndContactDetailsOfTheContactPersonInCaseOfAnyQueriesOnTheBRSRReport contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_name_and_contact_details_of_the_contact_person_in_case_of_any_queries_on_the_brsr_report', '') }}
    </in-capmkt:RemarksForAssuranceOfNameAndContactDetailsOfTheContactPersonInCaseOfAnyQueriesOnTheBRSRReport>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_name_of_the_company') is not none %}
    <in-capmkt:RemarksForAssuranceOfNameOfTheCompany contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_name_of_the_company', '') }}
    </in-capmkt:RemarksForAssuranceOfNameOfTheCompany>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_names_of_holding_subsidiary_associate_companies_joint_ventures') is not none %}
    <in-capmkt:RemarksForAssuranceOfNamesOfHoldingSubsidiaryAssociateCompaniesJointVentures contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_names_of_holding_subsidiary_associate_companies_joint_ventures', '') }}
    </in-capmkt:RemarksForAssuranceOfNamesOfHoldingSubsidiaryAssociateCompaniesJointVentures>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_telephone_of_company') is not none %}
    <in-capmkt:RemarksForAssuranceOfTelephoneOfCompany contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_telephone_of_company', '') }}
    </in-capmkt:RemarksForAssuranceOfTelephoneOfCompany>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_the_entity_has_undertaken_any_specific_initiatives_or_used_innovative_technology_or_solutions_to_improve_resource_efficiency') is not none %}
    <in-capmkt:RemarksForAssuranceOfTheEntityHasUndertakenAnySpecificInitiativesOrUsedInnovativeTechnologyOrSolutionsToImproveResourceEfficiency contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_the_entity_has_undertaken_any_specific_initiatives_or_used_innovative_technology_or_solutions_to_improve_resource_efficiency', '') }}
    </in-capmkt:RemarksForAssuranceOfTheEntityHasUndertakenAnySpecificInitiativesOrUsedInnovativeTechnologyOrSolutionsToImproveResourceEfficiency>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_the_entity_have_procedures_in_place_for_sustainable_sourcing_and_percentage_of_inputs_were_sourced_sustainably') is not none %}
    <in-capmkt:RemarksForAssuranceOfTheEntityHaveProceduresInPlaceForSustainableSourcingAndPercentageOfInputsWereSourcedSustainably contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_the_entity_have_procedures_in_place_for_sustainable_sourcing_and_percentage_of_inputs_were_sourced_sustainably', '') }}
    </in-capmkt:RemarksForAssuranceOfTheEntityHaveProceduresInPlaceForSustainableSourcingAndPercentageOfInputsWereSourcedSustainably>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_website_of_company') is not none %}
    <in-capmkt:RemarksForAssuranceOfWebsiteOfCompany contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_website_of_company', '') }}
    </in-capmkt:RemarksForAssuranceOfWebsiteOfCompany>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_csr_is_applicable_as_per_section135_of_companies_act2013') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013 contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_csr_is_applicable_as_per_section135_of_companies_act2013', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_have_any_project_related_to_reducing_green_house_gas_emission') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveAnyProjectRelatedToReducingGreenHouseGasEmission contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_have_any_project_related_to_reducing_green_house_gas_emission', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveAnyProjectRelatedToReducingGreenHouseGasEmission>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_year_of_incorporation') is not none %}
    <in-capmkt:RemarksForAssuranceOfYearOfIncorporation contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_year_of_incorporation', '') }}
    </in-capmkt:RemarksForAssuranceOfYearOfIncorporation>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_data_breaches_information_like_number_of_instances_of_data_breaches_along_with_impact_and_percentage_of_data_breaches_involving_personally_identifiable_information_of_customers') is not none %}
    <in-capmkt:RemarksForAssuranceOfDataBreachesInformationLikeNumberOfInstancesOfDataBreachesAlongWithImpactAndPercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomers contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_data_breaches_information_like_number_of_instances_of_data_breaches_along_with_impact_and_percentage_of_data_breaches_involving_personally_identifiable_information_of_customers', '') }}
    </in-capmkt:RemarksForAssuranceOfDataBreachesInformationLikeNumberOfInstancesOfDataBreachesAlongWithImpactAndPercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomers>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_air_emissions_other_than_ghg_emissions_by_the_entity') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfAirEmissionsOtherThanGhgEmissionsByTheEntity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_air_emissions_other_than_ghg_emissions_by_the_entity', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfAirEmissionsOtherThanGhgEmissionsByTheEntity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_complaints_made_by_employees_and_workers_as_per_p3') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfComplaintsMadeByEmployeesAndWorkersAsPerP3 contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_details_of_complaints_made_by_employees_and_workers_as_per_p3', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfComplaintsMadeByEmployeesAndWorkersAsPerP3>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_complaints_made_by_employees_and_workers_as_per_p5') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfComplaintsMadeByEmployeesAndWorkersAsPerP5 contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_details_of_complaints_made_by_employees_and_workers_as_per_p5', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfComplaintsMadeByEmployeesAndWorkersAsPerP5>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_employees_as_at_the_end_of_financial_year') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfEmployeesAsAtTheEndOfFinancialYear contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_details_of_employees_as_at_the_end_of_financial_year', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfEmployeesAsAtTheEndOfFinancialYear>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_measures_for_the_well_being_of_employees_and_workers_and_spending_on_it') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfMeasuresForTheWellBeingOfEmployeesAndWorkersAndSpendingOnIt contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_details_of_measures_for_the_well_being_of_employees_and_workers_and_spending_on_it', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfMeasuresForTheWellBeingOfEmployeesAndWorkersAndSpendingOnIt>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_minimum_wages_paid_to_employees_and_workers') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfMinimumWagesPaidToEmployeesAndWorkers contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_details_of_minimum_wages_paid_to_employees_and_workers', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfMinimumWagesPaidToEmployeesAndWorkers>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_number_of_consumer_complaints_p9') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfNumberOfConsumerComplaintsP9 contextRef="D_Principle9">
        {{ data.get('remarks_for_assurance_of_details_of_number_of_consumer_complaints_p9', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfNumberOfConsumerComplaintsP9>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_performance_and_career_development_reviews_of_employees_and_worker') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfPerformanceAndCareerDevelopmentReviewsOfEmployeesAndWorker contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_details_of_performance_and_career_development_reviews_of_employees_and_worker', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfPerformanceAndCareerDevelopmentReviewsOfEmployeesAndWorker>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_training_given_to_employees_and_workers') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTrainingGivenToEmployeesAndWorkers contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_details_of_training_given_to_employees_and_workers', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTrainingGivenToEmployeesAndWorkers>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_employees_and_workers_who_have_been_provided_training_on_human_rights_issues_and_policies_of_the_entity') is not none %}
    <in-capmkt:RemarksForAssuranceOfEmployeesAndWorkersWhoHaveBeenProvidedTrainingOnHumanRightsIssuesAndPoliciesOfTheEntity contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_employees_and_workers_who_have_been_provided_training_on_human_rights_issues_and_policies_of_the_entity', '') }}
    </in-capmkt:RemarksForAssuranceOfEmployeesAndWorkersWhoHaveBeenProvidedTrainingOnHumanRightsIssuesAndPoliciesOfTheEntity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_job_creation_in_smaller_towns_disclose_wages_paid_to_persons_employed_including_employees_or_workers_employed_on_a_permanent_or_non_permanent_or_on_contract_basis') is not none %}
    <in-capmkt:RemarksForAssuranceOfJobCreationInSmallerTownsDiscloseWagesPaidToPersonsEmployedIncludingEmployeesOrWorkersEmployedOnAPermanentOrNonPermanentOrOnContractBasis contextRef="D_Gender_PermanentEmployees_TableA">
        {{ data.get('remarks_for_assurance_of_job_creation_in_smaller_towns_disclose_wages_paid_to_persons_employed_including_employees_or_workers_employed_on_a_permanent_or_non_permanent_or_on_contract_basis', '') }}
    </in-capmkt:RemarksForAssuranceOfJobCreationInSmallerTownsDiscloseWagesPaidToPersonsEmployedIncludingEmployeesOrWorkersEmployedOnAPermanentOrNonPermanentOrOnContractBasis>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_number_of_days_of_accounts_payables') is not none %}
    <in-capmkt:RemarksForAssuranceOfNumberOfDaysOfAccountsPayables contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_number_of_days_of_accounts_payables', '') }}
    </in-capmkt:RemarksForAssuranceOfNumberOfDaysOfAccountsPayables>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_number_of_directors_or_km_ps_or_employees_or_workers_against_whom_disciplinary_action_was_taken_by_any_law_enforcement_agency_for_the_charges_of_bribery_or_corruption') is not none %}
    <in-capmkt:RemarksForAssuranceOfNumberOfDirectorsOrKMPsOrEmployeesOrWorkersAgainstWhomDisciplinaryActionWasTakenByAnyLawEnforcementAgencyForTheChargesOfBriberyOrCorruption contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_number_of_directors_or_km_ps_or_employees_or_workers_against_whom_disciplinary_action_was_taken_by_any_law_enforcement_agency_for_the_charges_of_bribery_or_corruption', '') }}
    </in-capmkt:RemarksForAssuranceOfNumberOfDirectorsOrKMPsOrEmployeesOrWorkersAgainstWhomDisciplinaryActionWasTakenByAnyLawEnforcementAgencyForTheChargesOfBriberyOrCorruption>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_percentage_coverage_by_training_and_awareness_programs_on_any_of_the_principles_during_the_financial_year_for_bod_or_kmp_or_employee_or_worker') is not none %}
    <in-capmkt:RemarksForAssuranceOfPercentageCoverageByTrainingAndAwarenessProgramsOnAnyOfThePrinciplesDuringTheFinancialYearForBODOrKMPOrEmployeeOrWorker contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_percentage_coverage_by_training_and_awareness_programs_on_any_of_the_principles_during_the_financial_year_for_bod_or_kmp_or_employee_or_worker', '') }}
    </in-capmkt:RemarksForAssuranceOfPercentageCoverageByTrainingAndAwarenessProgramsOnAnyOfThePrinciplesDuringTheFinancialYearForBODOrKMPOrEmployeeOrWorker>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_return_to_work_and_retention_rates_of_permanent_employees_and_workers_that_took_parental_leave') is not none %}
    <in-capmkt:RemarksForAssuranceOfReturnToWorkAndRetentionRatesOfPermanentEmployeesAndWorkersThatTookParentalLeave contextRef="D_Gender_PermanentEmployees_TableA">
        {{ data.get('remarks_for_assurance_of_return_to_work_and_retention_rates_of_permanent_employees_and_workers_that_took_parental_leave', '') }}
    </in-capmkt:RemarksForAssuranceOfReturnToWorkAndRetentionRatesOfPermanentEmployeesAndWorkersThatTookParentalLeave>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_is_there_a_mechanism_available_to_receive_and_redress_grievances_for_the_following_categories_of_employees_and_worker') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherIsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_whether_is_there_a_mechanism_available_to_receive_and_redress_grievances_for_the_following_categories_of_employees_and_worker', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherIsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_extend_any_life_insurance_or_any_compensatory_package_in_the_event_of_death_of_employees') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_extend_any_life_insurance_or_any_compensatory_package_in_the_event_of_death_of_employees', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_actions_taken_to_mitigate_any_negative_social_impacts_identified_in_the_social_impact_assessments') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfActionsTakenToMitigateAnyNegativeSocialImpactsIdentifiedInTheSocialImpactAssessments contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_actions_taken_to_mitigate_any_negative_social_impacts_identified_in_the_social_impact_assessments', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfActionsTakenToMitigateAnyNegativeSocialImpactsIdentifiedInTheSocialImpactAssessments>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_beneficiaries_of_csr_projects') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfBeneficiariesOfCSRProjects contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_beneficiaries_of_csr_projects', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfBeneficiariesOfCSRProjects>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_csr_projects_undertaken_in_designated_aspirational_districts_as_identified_by_government_bodies') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfCSRProjectsUndertakenInDesignatedAspirationalDistrictsAsIdentifiedByGovernmentBodies contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_csr_projects_undertaken_in_designated_aspirational_districts_as_identified_by_government_bodies', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfCSRProjectsUndertakenInDesignatedAspirationalDistrictsAsIdentifiedByGovernmentBodies>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_environmental_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfEnvironmentalImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLaws contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_environmental_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfEnvironmentalImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLaws>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_social_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfSocialImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLaws contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_social_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfSocialImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLaws>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_have_a_specified_committee_of_the_board_or_director_responsible_for_decision_making_on_sustainability_related_issues') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_have_a_specified_committee_of_the_board_or_director_responsible_for_decision_making_on_sustainability_related_issues', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_complaints_or_grievances_on_any_of_the_principles_under_the_national_guidelines_on_responsible_business_conduct') is not none %}
    <in-capmkt:RemarksForAssuranceOfComplaintsOrGrievancesOnAnyOfThePrinciplesUnderTheNationalGuidelinesOnResponsibleBusinessConduct contextRef="D_Location">
        {{ data.get('remarks_for_assurance_of_complaints_or_grievances_on_any_of_the_principles_under_the_national_guidelines_on_responsible_business_conduct', '') }}
    </in-capmkt:RemarksForAssuranceOfComplaintsOrGrievancesOnAnyOfThePrinciplesUnderTheNationalGuidelinesOnResponsibleBusinessConduct>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_describe_the_processes_in_place_to_safely_reclaim_your_products_for_reusing_recycling_and_disposing_at_the_end_of_life_for_plastics_including_packaging_e_waste_hazardous_waste_and_other_waste') is not none %}
    <in-capmkt:RemarksForAssuranceOfDescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingEWasteHazardousWasteAndOtherWaste contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_describe_the_processes_in_place_to_safely_reclaim_your_products_for_reusing_recycling_and_disposing_at_the_end_of_life_for_plastics_including_packaging_e_waste_hazardous_waste_and_other_waste', '') }}
    </in-capmkt:RemarksForAssuranceOfDescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingEWasteHazardousWasteAndOtherWaste>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_a_business_process_being_modified_or_introduced_as_a_result_of_addressing_human_rights_grievances_or_complaints') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaints contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_a_business_process_being_modified_or_introduced_as_a_result_of_addressing_human_rights_grievances_or_complaints', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaints>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_any_corrective_actions_taken_or_underway_on_issues_relating_to_advertising_and_delivery_of_essential_services_or_cyber_security_and_data_privacy_or_recalls_or_penalty_or_action_taken_by_regulatory_authorities_on_safety_of_products_or_services') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServices contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_any_corrective_actions_taken_or_underway_on_issues_relating_to_advertising_and_delivery_of_essential_services_or_cyber_security_and_data_privacy_or_recalls_or_penalty_or_action_taken_by_regulatory_authorities_on_safety_of_products_or_services', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServices>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_business_activities_accounting_for_ninety_percent_of_the_turnover') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfBusinessActivitiesAccountingForNinetyPercentOfTheTurnover contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_business_activities_accounting_for_ninety_percent_of_the_turnover', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfBusinessActivitiesAccountingForNinetyPercentOfTheTurnover>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_instances_of_product_recalls_on_account_of_safety_issues') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfInstancesOfProductRecallsOnAccountOfSafetyIssues contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_instances_of_product_recalls_on_account_of_safety_issues', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfInstancesOfProductRecallsOnAccountOfSafetyIssues>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_percentage_of_recycled_or_reused_input_material_to_total_material_by_value_used_in_production_or_providing_services') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfPercentageOfRecycledOrReusedInputMaterialToTotalMaterialByValueUsedInProductionOrProvidingServices contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_percentage_of_recycled_or_reused_input_material_to_total_material_by_value_used_in_production_or_providing_services', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfPercentageOfRecycledOrReusedInputMaterialToTotalMaterialByValueUsedInProductionOrProvidingServices>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_reclaimed_products_and_their_packaging_materials_for_each_product_category') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfReclaimedProductsAndTheirPackagingMaterialsForEachProductCategory contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_reclaimed_products_and_their_packaging_materials_for_each_product_category', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfReclaimedProductsAndTheirPackagingMaterialsForEachProductCategory>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_significant_social_or_environmental_concerns_from_production_or_disposal_of_product_or_service_with_action_taken_to_mitigate_the_same') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfSignificantSocialOrEnvironmentalConcernsFromProductionOrDisposalOfProductOrServiceWithActionTakenToMitigateTheSame contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_significant_social_or_environmental_concerns_from_production_or_disposal_of_product_or_service_with_action_taken_to_mitigate_the_same', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfSignificantSocialOrEnvironmentalConcernsFromProductionOrDisposalOfProductOrServiceWithActionTakenToMitigateTheSame>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_the_highest_authority_responsible_for_implementation_and_oversight_of_the_business_responsibility_policy') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicy contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_the_highest_authority_responsible_for_implementation_and_oversight_of_the_business_responsibility_policy', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicy>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_human_rights_requirements_form_part_of_your_business_agreements_and_contracts') is not none %}
    <in-capmkt:RemarksForAssuranceOfHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_human_rights_requirements_form_part_of_your_business_agreements_and_contracts', '') }}
    </in-capmkt:RemarksForAssuranceOfHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_mechanisms_in_place_to_inform_consumers_of_any_risk_of_disruption_or_discontinuation_of_essential_services') is not none %}
    <in-capmkt:RemarksForAssuranceOfMechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServices contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_mechanisms_in_place_to_inform_consumers_of_any_risk_of_disruption_or_discontinuation_of_essential_services', '') }}
    </in-capmkt:RemarksForAssuranceOfMechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServices>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_overview_of_the_entitys_material_responsible_business_conduct_issues') is not none %}
    <in-capmkt:RemarksForAssuranceOfOverviewOfTheEntitysMaterialResponsibleBusinessConductIssues contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_overview_of_the_entitys_material_responsible_business_conduct_issues', '') }}
    </in-capmkt:RemarksForAssuranceOfOverviewOfTheEntitysMaterialResponsibleBusinessConductIssues>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_percentage_of_contribution_of_exports_in_the_total_turnover_of_the_entity') is not none %}
    <in-capmkt:RemarksForAssuranceOfPercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_percentage_of_contribution_of_exports_in_the_total_turnover_of_the_entity', '') }}
    </in-capmkt:RemarksForAssuranceOfPercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_percentage_of_value_chain_partners_by_value_of_business_done_with_such_partners_that_were_assessed_for_environmental_impacts') is not none %}
    <in-capmkt:RemarksForAssuranceOfPercentageOfValueChainPartnersByValueOfBusinessDoneWithSuchPartnersThatWereAssessedForEnvironmentalImpacts contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_percentage_of_value_chain_partners_by_value_of_business_done_with_such_partners_that_were_assessed_for_environmental_impacts', '') }}
    </in-capmkt:RemarksForAssuranceOfPercentageOfValueChainPartnersByValueOfBusinessDoneWithSuchPartnersThatWereAssessedForEnvironmentalImpacts>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_products_or_services_sold_by_the_entity_accounting_for_ninety_percent_of_the_turnover') is not none %}
    <in-capmkt:RemarksForAssuranceOfProductsOrServicesSoldByTheEntityAccountingForNinetyPercentOfTheTurnover contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_products_or_services_sold_by_the_entity_accounting_for_ninety_percent_of_the_turnover', '') }}
    </in-capmkt:RemarksForAssuranceOfProductsOrServicesSoldByTheEntityAccountingForNinetyPercentOfTheTurnover>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_statement_by_director_responsible_for_the_business_responsibility_report_highlighting_esg_related_challenges_targets_and_achievements') is not none %}
    <in-capmkt:RemarksForAssuranceOfStatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievements contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_statement_by_director_responsible_for_the_business_responsibility_report_highlighting_esg_related_challenges_targets_and_achievements', '') }}
    </in-capmkt:RemarksForAssuranceOfStatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievements>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_steps_taken_to_inform_and_educate_consumers_about_safe_and_responsible_usage_of_products_and_or_services') is not none %}
    <in-capmkt:RemarksForAssuranceOfStepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServices contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_steps_taken_to_inform_and_educate_consumers_about_safe_and_responsible_usage_of_products_and_or_services', '') }}
    </in-capmkt:RemarksForAssuranceOfStepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServices>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_the_products_and_packaging_reclaimed_at_end_of_life_of_products_amount_reused_or_recycled_or_safely_disposed') is not none %}
    <in-capmkt:RemarksForAssuranceOfTheProductsAndPackagingReclaimedAtEndOfLifeOfProductsAmountReusedOrRecycledOrSafelyDisposed contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_the_products_and_packaging_reclaimed_at_end_of_life_of_products_amount_reused_or_recycled_or_safely_disposed', '') }}
    </in-capmkt:RemarksForAssuranceOfTheProductsAndPackagingReclaimedAtEndOfLifeOfProductsAmountReusedOrRecycledOrSafelyDisposed>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_turnover_of_products_and_or_services_as_a_percentage_of_turnover_from_all_products_or_service_that_carry_information_about_as_a_percentage_to_total_turnover') is not none %}
    <in-capmkt:RemarksForAssuranceOfTurnoverOfProductsAndOrServicesAsAPercentageOfTurnoverFromAllProductsOrServiceThatCarryInformationAboutAsAPercentageToTotalTurnover contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_turnover_of_products_and_or_services_as_a_percentage_of_turnover_from_all_products_or_service_that_carry_information_about_as_a_percentage_to_total_turnover', '') }}
    </in-capmkt:RemarksForAssuranceOfTurnoverOfProductsAndOrServicesAsAPercentageOfTurnoverFromAllProductsOrServiceThatCarryInformationAboutAsAPercentageToTotalTurnover>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_turnover_rate_for_permanent_employees_and_workers_disclose_trends_for_past_three_years') is not none %}
    <in-capmkt:RemarksForAssuranceOfTurnoverRateForPermanentEmployeesAndWorkersDiscloseTrendsForPastThreeYears contextRef="D_Gender_PermanentEmployees_TableA">
        {{ data.get('remarks_for_assurance_of_turnover_rate_for_permanent_employees_and_workers_disclose_trends_for_past_three_years', '') }}
    </in-capmkt:RemarksForAssuranceOfTurnoverRateForPermanentEmployeesAndWorkersDiscloseTrendsForPastThreeYears>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_weblink_where_information_on_products_and_services_of_the_entity_can_be_accessed') is not none %}
    <in-capmkt:RemarksForAssuranceOfWeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessed contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_weblink_where_information_on_products_and_services_of_the_entity_can_be_accessed', '') }}
    </in-capmkt:RemarksForAssuranceOfWeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessed>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_do_you_have_a_focal_point_responsible_for_addressing_human_rights_impacts_or_issues_caused_or_contributed_to_by_the_business') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherDoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_do_you_have_a_focal_point_responsible_for_addressing_human_rights_impacts_or_issues_caused_or_contributed_to_by_the_business', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherDoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_conducted_life_cycle_perspective_or_assessments_for_any_of_its_products_or_for_its_services') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_conducted_life_cycle_perspective_or_assessments_for_any_of_its_products_or_for_its_services', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_display_product_information_on_the_product_over_and_above_what_is_mandated_as_per_local_laws') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_display_product_information_on_the_product_over_and_above_what_is_mandated_as_per_local_laws', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_have_a_business_continuity_and_disaster_management_plan') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveABusinessContinuityAndDisasterManagementPlan contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_have_a_business_continuity_and_disaster_management_plan', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveABusinessContinuityAndDisasterManagementPlan>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p3') is not none %}
    <in-capmkt:RemarksForAssuranceOfAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP3 contextRef="D_Principle3">
        {{ data.get('remarks_for_assurance_of_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p3', '') }}
    </in-capmkt:RemarksForAssuranceOfAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP3>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p5') is not none %}
    <in-capmkt:RemarksForAssuranceOfAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP5 contextRef="D_Principle5">
        {{ data.get('remarks_for_assurance_of_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p5', '') }}
    </in-capmkt:RemarksForAssuranceOfAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP5>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_of_your_plants_and_offices_that_were_assessed') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessed contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_of_your_plants_and_offices_that_were_assessed', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessed>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_plant_and_office') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOffice contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_plant_and_office', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOffice>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_number_of_locations_where_plants_and_or_operations_or_offices_of_the_entity_are_situated') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfNumberOfLocationsWherePlantsAndOrOperationsOrOfficesOfTheEntityAreSituated contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_number_of_locations_where_plants_and_or_operations_or_offices_of_the_entity_are_situated', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfNumberOfLocationsWherePlantsAndOrOperationsOrOfficesOfTheEntityAreSituated>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_operations_or_offices_in_or_around_ecologically_sensitive_areas_where_environmental_approvals_or_clearances_are_required') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfOperationsOrOfficesInOrAroundEcologicallySensitiveAreasWhereEnvironmentalApprovalsOrClearancesAreRequired contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_operations_or_offices_in_or_around_ecologically_sensitive_areas_where_environmental_approvals_or_clearances_are_required', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfOperationsOrOfficesInOrAroundEcologicallySensitiveAreasWhereEnvironmentalApprovalsOrClearancesAreRequired>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_name_of_the_national_and_international_codes_or_certifications_or_labels_or_standards_adopted_by_your_entity_and_mapped_to_each_principle') is not none %}
    <in-capmkt:RemarksForAssuranceOfNameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrinciple contextRef="D_Location">
        {{ data.get('remarks_for_assurance_of_name_of_the_national_and_international_codes_or_certifications_or_labels_or_standards_adopted_by_your_entity_and_mapped_to_each_principle', '') }}
    </in-capmkt:RemarksForAssuranceOfNameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrinciple>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_number_of_locations_where_markets_served_by_the_entity') is not none %}
    <in-capmkt:RemarksForAssuranceOfNumberOfLocationsWhereMarketsServedByTheEntity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_number_of_locations_where_markets_served_by_the_entity', '') }}
    </in-capmkt:RemarksForAssuranceOfNumberOfLocationsWhereMarketsServedByTheEntity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_the_premises_or_offices_of_the_entity_accessible_to_differently_abled_employees_and_workers_and_steps_are_being_taken_by_the_entity_if_the_premises_or_offices_of_the_entity_not_accessible') is not none %}
    <in-capmkt:RemarksForAssuranceOfThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkersAndStepsAreBeingTakenByTheEntityIfThePremisesOrOfficesOfTheEntityNotAccessible contextRef="D_Gender_Employees_TableA">
        {{ data.get('remarks_for_assurance_of_the_premises_or_offices_of_the_entity_accessible_to_differently_abled_employees_and_workers_and_steps_are_being_taken_by_the_entity_if_the_premises_or_offices_of_the_entity_not_accessible', '') }}
    </in-capmkt:RemarksForAssuranceOfThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkersAndStepsAreBeingTakenByTheEntityIfThePremisesOrOfficesOfTheEntityNotAccessible>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_premise_or_office_of_the_entity_accessible_to_differently_abled_visitors_as_per_the_requirements_of_the_rights_of_persons_with_disabilities_act2016') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_premise_or_office_of_the_entity_accessible_to_differently_abled_visitors_as_per_the_requirements_of_the_rights_of_persons_with_disabilities_act2016', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_markets_served_by_the_entity') is not none %}
    <in-capmkt:RemarksForAssuranceOfMarketsServedByTheEntity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_markets_served_by_the_entity', '') }}
    </in-capmkt:RemarksForAssuranceOfMarketsServedByTheEntity>
    {% endif %}

        {% if data.get('whether_address_of_corporate_office_of_company_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherAddressOfCorporateOfficeOfCompanyIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_address_of_corporate_office_of_company_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherAddressOfCorporateOfficeOfCompanyIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_address_of_registered_office_of_company_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherAddressOfRegisteredOfficeOfCompanyIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_address_of_registered_office_of_company_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherAddressOfRegisteredOfficeOfCompanyIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_csr_is_applicable_as_per_section135_of_companies_act2013_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013IsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_csr_is_applicable_as_per_section135_of_companies_act2013_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013IsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_corporate_identity_number_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherCorporateIdentityNumberIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_corporate_identity_number_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherCorporateIdentityNumberIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_the_stock_exchange_where_the_company_is_listed_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTheStockExchangeWhereTheCompanyIsListedIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_the_stock_exchange_where_the_company_is_listed_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTheStockExchangeWhereTheCompanyIsListedIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_waste_management_practices_adopted_in_your_establishments_and_the_strategy_adopted_by_company_to_reduce_usage_of_hazardous_and_toxic_chemicals_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicalsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_waste_management_practices_adopted_in_your_establishments_and_the_strategy_adopted_by_company_to_reduce_usage_of_hazardous_and_toxic_chemicals_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicalsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_e_mail_of_the_company_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherEMailOfTheCompanyIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_e_mail_of_the_company_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherEMailOfTheCompanyIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_name_and_contact_details_of_the_contact_person_in_case_of_any_queries_on_the_brsr_report_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherNameAndContactDetailsOfTheContactPersonInCaseOfAnyQueriesOnTheBRSRReportIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_name_and_contact_details_of_the_contact_person_in_case_of_any_queries_on_the_brsr_report_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherNameAndContactDetailsOfTheContactPersonInCaseOfAnyQueriesOnTheBRSRReportIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_name_of_the_company_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherNameOfTheCompanyIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_name_of_the_company_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherNameOfTheCompanyIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_names_of_holding_subsidiary_associate_companies_joint_ventures_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherNamesOfHoldingSubsidiaryAssociateCompaniesJointVenturesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_names_of_holding_subsidiary_associate_companies_joint_ventures_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherNamesOfHoldingSubsidiaryAssociateCompaniesJointVenturesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_telephone_of_company_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTelephoneOfCompanyIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_telephone_of_company_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTelephoneOfCompanyIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_entity_has_undertaken_any_specific_initiatives_or_used_innovative_technology_or_solutions_to_improve_resource_efficiency_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTheEntityHasUndertakenAnySpecificInitiativesOrUsedInnovativeTechnologyOrSolutionsToImproveResourceEfficiencyIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_entity_has_undertaken_any_specific_initiatives_or_used_innovative_technology_or_solutions_to_improve_resource_efficiency_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTheEntityHasUndertakenAnySpecificInitiativesOrUsedInnovativeTechnologyOrSolutionsToImproveResourceEfficiencyIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_entity_have_procedures_in_place_for_sustainable_sourcing_and_percentage_of_inputs_were_sourced_sustainably_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTheEntityHaveProceduresInPlaceForSustainableSourcingAndPercentageOfInputsWereSourcedSustainablyIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_entity_have_procedures_in_place_for_sustainable_sourcing_and_percentage_of_inputs_were_sourced_sustainably_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTheEntityHaveProceduresInPlaceForSustainableSourcingAndPercentageOfInputsWereSourcedSustainablyIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_website_of_company_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherWebsiteOfCompanyIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_website_of_company_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherWebsiteOfCompanyIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_year_of_incorporation_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherYearOfIncorporationIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_year_of_incorporation_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherYearOfIncorporationIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_data_breaches_information_like_number_of_instances_of_data_breaches_along_with_impact_and_percentage_of_data_breaches_involving_personally_identifiable_information_of_customers_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDataBreachesInformationLikeNumberOfInstancesOfDataBreachesAlongWithImpactAndPercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomersIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_data_breaches_information_like_number_of_instances_of_data_breaches_along_with_impact_and_percentage_of_data_breaches_involving_personally_identifiable_information_of_customers_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDataBreachesInformationLikeNumberOfInstancesOfDataBreachesAlongWithImpactAndPercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_air_emissions_other_than_ghg_emissions_by_the_entity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfAirEmissionsOtherThanGhgEmissionsByTheEntityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_air_emissions_other_than_ghg_emissions_by_the_entity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfAirEmissionsOtherThanGhgEmissionsByTheEntityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_complaints_made_by_employees_and_workers_is_assured_by_assurer_as_per_p3') is not none %}
    <in-capmkt:WhetherDetailsOfComplaintsMadeByEmployeesAndWorkersIsAssuredByAssurerAsPerP3 contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_details_of_complaints_made_by_employees_and_workers_is_assured_by_assurer_as_per_p3') else 'false' }}
    </in-capmkt:WhetherDetailsOfComplaintsMadeByEmployeesAndWorkersIsAssuredByAssurerAsPerP3>
    {% endif %}

        {% if data.get('whether_details_of_complaints_made_by_employees_and_workers_is_assured_by_assurer_as_per_p5') is not none %}
    <in-capmkt:WhetherDetailsOfComplaintsMadeByEmployeesAndWorkersIsAssuredByAssurerAsPerP5 contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_details_of_complaints_made_by_employees_and_workers_is_assured_by_assurer_as_per_p5') else 'false' }}
    </in-capmkt:WhetherDetailsOfComplaintsMadeByEmployeesAndWorkersIsAssuredByAssurerAsPerP5>
    {% endif %}

        {% if data.get('whether_details_of_employees_as_at_the_end_of_financial_year_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfEmployeesAsAtTheEndOfFinancialYearIsAssuredByAssurer contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_details_of_employees_as_at_the_end_of_financial_year_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfEmployeesAsAtTheEndOfFinancialYearIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_measures_for_the_well_being_of_employees_and_workers_and_spending_on_it_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfMeasuresForTheWellBeingOfEmployeesAndWorkersAndSpendingOnItIsAssuredByAssurer contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_details_of_measures_for_the_well_being_of_employees_and_workers_and_spending_on_it_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfMeasuresForTheWellBeingOfEmployeesAndWorkersAndSpendingOnItIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_minimum_wages_paid_to_employees_and_workers_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfMinimumWagesPaidToEmployeesAndWorkersIsAssuredByAssurer contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_details_of_minimum_wages_paid_to_employees_and_workers_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfMinimumWagesPaidToEmployeesAndWorkersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_number_of_consumer_complaints_p9_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfNumberOfConsumerComplaintsP9IsAssuredByAssurer contextRef="D_Principle9">
        {{ 'true' if data.get('whether_details_of_number_of_consumer_complaints_p9_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfNumberOfConsumerComplaintsP9IsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_performance_and_career_development_reviews_of_employees_and_worker_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfPerformanceAndCareerDevelopmentReviewsOfEmployeesAndWorkerIsAssuredByAssurer contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_details_of_performance_and_career_development_reviews_of_employees_and_worker_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfPerformanceAndCareerDevelopmentReviewsOfEmployeesAndWorkerIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_training_given_to_employees_and_workers_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTrainingGivenToEmployeesAndWorkersIsAssuredByAssurer contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_details_of_training_given_to_employees_and_workers_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTrainingGivenToEmployeesAndWorkersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_employees_and_workers_who_have_been_provided_training_on_human_rights_issues_and_policies_of_the_entity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherEmployeesAndWorkersWhoHaveBeenProvidedTrainingOnHumanRightsIssuesAndPoliciesOfTheEntityIsAssuredByAssurer contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_employees_and_workers_who_have_been_provided_training_on_human_rights_issues_and_policies_of_the_entity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherEmployeesAndWorkersWhoHaveBeenProvidedTrainingOnHumanRightsIssuesAndPoliciesOfTheEntityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_job_creation_in_smaller_towns_disclose_wages_paid_to_persons_employed_including_employees_or_workers_employed_on_a_permanent_or_non_permanent_or_on_contract_basis_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherJobCreationInSmallerTownsDiscloseWagesPaidToPersonsEmployedIncludingEmployeesOrWorkersEmployedOnAPermanentOrNonPermanentOrOnContractBasisIsAssuredByAssurer contextRef="D_Gender_PermanentEmployees_TableA">
        {{ 'true' if data.get('whether_job_creation_in_smaller_towns_disclose_wages_paid_to_persons_employed_including_employees_or_workers_employed_on_a_permanent_or_non_permanent_or_on_contract_basis_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherJobCreationInSmallerTownsDiscloseWagesPaidToPersonsEmployedIncludingEmployeesOrWorkersEmployedOnAPermanentOrNonPermanentOrOnContractBasisIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_number_of_days_of_accounts_payables_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherNumberOfDaysOfAccountsPayablesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_number_of_days_of_accounts_payables_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherNumberOfDaysOfAccountsPayablesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_number_of_directors_or_km_ps_or_employees_or_workers_against_whom_disciplinary_action_was_taken_by_any_law_enforcement_agency_for_the_charges_of_bribery_or_corruption_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherNumberOfDirectorsOrKMPsOrEmployeesOrWorkersAgainstWhomDisciplinaryActionWasTakenByAnyLawEnforcementAgencyForTheChargesOfBriberyOrCorruptionIsAssuredByAssurer contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_number_of_directors_or_km_ps_or_employees_or_workers_against_whom_disciplinary_action_was_taken_by_any_law_enforcement_agency_for_the_charges_of_bribery_or_corruption_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherNumberOfDirectorsOrKMPsOrEmployeesOrWorkersAgainstWhomDisciplinaryActionWasTakenByAnyLawEnforcementAgencyForTheChargesOfBriberyOrCorruptionIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_percentage_coverage_by_training_and_awareness_programs_on_any_of_the_principles_during_the_financial_year_for_bod_or_kmp_or_employee_or_worker_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherPercentageCoverageByTrainingAndAwarenessProgramsOnAnyOfThePrinciplesDuringTheFinancialYearForBODOrKMPOrEmployeeOrWorkerIsAssuredByAssurer contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_percentage_coverage_by_training_and_awareness_programs_on_any_of_the_principles_during_the_financial_year_for_bod_or_kmp_or_employee_or_worker_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherPercentageCoverageByTrainingAndAwarenessProgramsOnAnyOfThePrinciplesDuringTheFinancialYearForBODOrKMPOrEmployeeOrWorkerIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_return_to_work_and_retention_rates_of_permanent_employees_and_workers_that_took_parental_leave_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherReturnToWorkAndRetentionRatesOfPermanentEmployeesAndWorkersThatTookParentalLeaveIsAssuredByAssurer contextRef="D_Gender_PermanentEmployees_TableA">
        {{ 'true' if data.get('whether_return_to_work_and_retention_rates_of_permanent_employees_and_workers_that_took_parental_leave_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherReturnToWorkAndRetentionRatesOfPermanentEmployeesAndWorkersThatTookParentalLeaveIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_actions_taken_to_mitigate_any_negative_social_impacts_identified_in_the_social_impact_assessments_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfActionsTakenToMitigateAnyNegativeSocialImpactsIdentifiedInTheSocialImpactAssessmentsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_actions_taken_to_mitigate_any_negative_social_impacts_identified_in_the_social_impact_assessments_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfActionsTakenToMitigateAnyNegativeSocialImpactsIdentifiedInTheSocialImpactAssessmentsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_beneficiaries_of_csr_projects_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfBeneficiariesOfCSRProjectsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_beneficiaries_of_csr_projects_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfBeneficiariesOfCSRProjectsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_csr_projects_undertaken_in_designated_aspirational_districts_as_identified_by_government_bodies_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfCSRProjectsUndertakenInDesignatedAspirationalDistrictsAsIdentifiedByGovernmentBodiesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_csr_projects_undertaken_in_designated_aspirational_districts_as_identified_by_government_bodies_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfCSRProjectsUndertakenInDesignatedAspirationalDistrictsAsIdentifiedByGovernmentBodiesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_environmental_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfEnvironmentalImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLawsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_environmental_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfEnvironmentalImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLawsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_social_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfSocialImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLawsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_social_impact_assessments_of_projects_undertaken_by_the_entity_based_on_applicable_laws_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfSocialImpactAssessmentsOfProjectsUndertakenByTheEntityBasedOnApplicableLawsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_complaints_or_grievances_on_any_of_the_principles_under_the_national_guidelines_on_responsible_business_conduct_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherComplaintsOrGrievancesOnAnyOfThePrinciplesUnderTheNationalGuidelinesOnResponsibleBusinessConductIsAssuredByAssurer contextRef="D_Location">
        {{ 'true' if data.get('whether_complaints_or_grievances_on_any_of_the_principles_under_the_national_guidelines_on_responsible_business_conduct_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherComplaintsOrGrievancesOnAnyOfThePrinciplesUnderTheNationalGuidelinesOnResponsibleBusinessConductIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_describe_the_processes_in_place_to_safely_reclaim_your_products_for_reusing_recycling_and_disposing_at_the_end_of_life_for_plastics_including_packaging_e_waste_hazardous_waste_and_other_waste_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingEWasteHazardousWasteAndOtherWasteIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_describe_the_processes_in_place_to_safely_reclaim_your_products_for_reusing_recycling_and_disposing_at_the_end_of_life_for_plastics_including_packaging_e_waste_hazardous_waste_and_other_waste_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingEWasteHazardousWasteAndOtherWasteIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_a_business_process_being_modified_or_introduced_as_a_result_of_addressing_human_rights_grievances_or_complaints_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaintsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_a_business_process_being_modified_or_introduced_as_a_result_of_addressing_human_rights_grievances_or_complaints_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaintsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_any_corrective_actions_taken_or_underway_on_issues_relating_to_advertising_and_delivery_of_essential_services_or_cyber_security_and_data_privacy_or_recalls_or_penalty_or_action_taken_by_regulatory_authorities_on_safety_of_products_or_services_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServicesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_any_corrective_actions_taken_or_underway_on_issues_relating_to_advertising_and_delivery_of_essential_services_or_cyber_security_and_data_privacy_or_recalls_or_penalty_or_action_taken_by_regulatory_authorities_on_safety_of_products_or_services_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServicesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_business_activities_accounting_for_ninety_percent_of_the_turnover_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfBusinessActivitiesAccountingForNinetyPercentOfTheTurnoverIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_business_activities_accounting_for_ninety_percent_of_the_turnover_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfBusinessActivitiesAccountingForNinetyPercentOfTheTurnoverIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_instances_of_product_recalls_on_account_of_safety_issues_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfInstancesOfProductRecallsOnAccountOfSafetyIssuesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_instances_of_product_recalls_on_account_of_safety_issues_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfInstancesOfProductRecallsOnAccountOfSafetyIssuesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_percentage_of_recycled_or_reused_input_material_to_total_material_by_value_used_in_production_or_providing_services_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfPercentageOfRecycledOrReusedInputMaterialToTotalMaterialByValueUsedInProductionOrProvidingServicesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_percentage_of_recycled_or_reused_input_material_to_total_material_by_value_used_in_production_or_providing_services_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfPercentageOfRecycledOrReusedInputMaterialToTotalMaterialByValueUsedInProductionOrProvidingServicesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_reclaimed_products_and_their_packaging_materials_for_each_product_category_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfReclaimedProductsAndTheirPackagingMaterialsForEachProductCategoryIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_reclaimed_products_and_their_packaging_materials_for_each_product_category_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfReclaimedProductsAndTheirPackagingMaterialsForEachProductCategoryIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_significant_social_or_environmental_concerns_from_production_or_disposal_of_product_or_service_with_action_taken_to_mitigate_the_same_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfSignificantSocialOrEnvironmentalConcernsFromProductionOrDisposalOfProductOrServiceWithActionTakenToMitigateTheSameIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_significant_social_or_environmental_concerns_from_production_or_disposal_of_product_or_service_with_action_taken_to_mitigate_the_same_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfSignificantSocialOrEnvironmentalConcernsFromProductionOrDisposalOfProductOrServiceWithActionTakenToMitigateTheSameIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_the_highest_authority_responsible_for_implementation_and_oversight_of_the_business_responsibility_policy_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicyIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_the_highest_authority_responsible_for_implementation_and_oversight_of_the_business_responsibility_policy_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicyIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_human_rights_requirements_form_part_of_your_business_agreements_and_contracts_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContractsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_human_rights_requirements_form_part_of_your_business_agreements_and_contracts_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContractsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_mechanisms_in_place_to_inform_consumers_of_any_risk_of_disruption_or_discontinuation_of_essential_services_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherMechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServicesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_mechanisms_in_place_to_inform_consumers_of_any_risk_of_disruption_or_discontinuation_of_essential_services_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherMechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServicesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_overview_of_the_entitys_material_responsible_business_conduct_issues_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherOverviewOfTheEntitysMaterialResponsibleBusinessConductIssuesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_overview_of_the_entitys_material_responsible_business_conduct_issues_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherOverviewOfTheEntitysMaterialResponsibleBusinessConductIssuesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_percentage_of_contribution_of_exports_in_the_total_turnover_of_the_entity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherPercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_percentage_of_contribution_of_exports_in_the_total_turnover_of_the_entity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherPercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_percentage_of_value_chain_partners_by_value_of_business_done_with_such_partners_that_were_assessed_for_environmental_impacts_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherPercentageOfValueChainPartnersByValueOfBusinessDoneWithSuchPartnersThatWereAssessedForEnvironmentalImpactsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_percentage_of_value_chain_partners_by_value_of_business_done_with_such_partners_that_were_assessed_for_environmental_impacts_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherPercentageOfValueChainPartnersByValueOfBusinessDoneWithSuchPartnersThatWereAssessedForEnvironmentalImpactsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_products_or_services_sold_by_the_entity_accounting_for_ninety_percent_of_the_turnover_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherProductsOrServicesSoldByTheEntityAccountingForNinetyPercentOfTheTurnoverIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_products_or_services_sold_by_the_entity_accounting_for_ninety_percent_of_the_turnover_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherProductsOrServicesSoldByTheEntityAccountingForNinetyPercentOfTheTurnoverIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_statement_by_director_responsible_for_the_business_responsibility_report_highlighting_esg_related_challenges_targets_and_achievements_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherStatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievementsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_statement_by_director_responsible_for_the_business_responsibility_report_highlighting_esg_related_challenges_targets_and_achievements_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherStatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievementsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_steps_taken_to_inform_and_educate_consumers_about_safe_and_responsible_usage_of_products_and_or_services_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherStepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServicesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_steps_taken_to_inform_and_educate_consumers_about_safe_and_responsible_usage_of_products_and_or_services_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherStepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServicesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_products_and_packaging_reclaimed_at_end_of_life_of_products_amount_reused_or_recycled_or_safely_disposed_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTheProductsAndPackagingReclaimedAtEndOfLifeOfProductsAmountReusedOrRecycledOrSafelyDisposedIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_products_and_packaging_reclaimed_at_end_of_life_of_products_amount_reused_or_recycled_or_safely_disposed_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTheProductsAndPackagingReclaimedAtEndOfLifeOfProductsAmountReusedOrRecycledOrSafelyDisposedIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_turnover_of_products_and_or_services_as_a_percentage_of_turnover_from_all_products_or_service_that_carry_information_about_as_a_percentage_to_total_turnover_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTurnoverOfProductsAndOrServicesAsAPercentageOfTurnoverFromAllProductsOrServiceThatCarryInformationAboutAsAPercentageToTotalTurnoverIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_turnover_of_products_and_or_services_as_a_percentage_of_turnover_from_all_products_or_service_that_carry_information_about_as_a_percentage_to_total_turnover_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTurnoverOfProductsAndOrServicesAsAPercentageOfTurnoverFromAllProductsOrServiceThatCarryInformationAboutAsAPercentageToTotalTurnoverIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_turnover_rate_for_permanent_employees_and_workers_disclose_trends_for_past_three_years_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTurnoverRateForPermanentEmployeesAndWorkersDiscloseTrendsForPastThreeYearsIsAssuredByAssurer contextRef="D_Gender_PermanentEmployees_TableA">
        {{ 'true' if data.get('whether_turnover_rate_for_permanent_employees_and_workers_disclose_trends_for_past_three_years_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTurnoverRateForPermanentEmployeesAndWorkersDiscloseTrendsForPastThreeYearsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_weblink_where_information_on_products_and_services_of_the_entity_can_be_accessed_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherWeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessedIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_weblink_where_information_on_products_and_services_of_the_entity_can_be_accessed_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherWeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessedIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_any_steps_are_being_taken_by_the_entity_if_the_premises_or_offices_of_the_entity_not_accessible_to_differently_abled_employees_and_workers_explanatory_text_block') is not none %}
    <in-capmkt:WhetherAnyStepsAreBeingTakenByTheEntityIfThePremisesOrOfficesOfTheEntityNotAccessibleToDifferentlyAbledEmployeesAndWorkersExplanatoryTextBlock contextRef="D_Gender_Employees_TableA" escape="true">
        {{ data.get('whether_any_steps_are_being_taken_by_the_entity_if_the_premises_or_offices_of_the_entity_not_accessible_to_differently_abled_employees_and_workers_explanatory_text_block', '') }}
    </in-capmkt:WhetherAnyStepsAreBeingTakenByTheEntityIfThePremisesOrOfficesOfTheEntityNotAccessibleToDifferentlyAbledEmployeesAndWorkersExplanatoryTextBlock>
    {% endif %}

        {% if data.get('whether_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p3_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP3IsAssuredByAssurer contextRef="D_Principle3">
        {{ 'true' if data.get('whether_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p3_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP3IsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p5_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP5IsAssuredByAssurer contextRef="D_Principle5">
        {{ 'true' if data.get('whether_assessments_of_your_plants_and_offices_that_were_assessed_for_the_year_p5_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherAssessmentsOfYourPlantsAndOfficesThatWereAssessedForTheYearP5IsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_of_your_plants_and_offices_that_were_assessed_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessedIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_of_your_plants_and_offices_that_were_assessed_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessedIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_plant_and_office_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOfficeIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_plant_and_office_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOfficeIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_number_of_locations_where_plants_and_or_operations_or_offices_of_the_entity_are_situated_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfNumberOfLocationsWherePlantsAndOrOperationsOrOfficesOfTheEntityAreSituatedIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_number_of_locations_where_plants_and_or_operations_or_offices_of_the_entity_are_situated_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfNumberOfLocationsWherePlantsAndOrOperationsOrOfficesOfTheEntityAreSituatedIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_operations_or_offices_in_or_around_ecologically_sensitive_areas_where_environmental_approvals_or_clearances_are_required_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfOperationsOrOfficesInOrAroundEcologicallySensitiveAreasWhereEnvironmentalApprovalsOrClearancesAreRequiredIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_operations_or_offices_in_or_around_ecologically_sensitive_areas_where_environmental_approvals_or_clearances_are_required_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfOperationsOrOfficesInOrAroundEcologicallySensitiveAreasWhereEnvironmentalApprovalsOrClearancesAreRequiredIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_name_of_the_national_and_international_codes_or_certifications_or_labels_or_standards_adopted_by_your_entity_and_mapped_to_each_principle_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherNameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrincipleIsAssuredByAssurer contextRef="D_Location">
        {{ 'true' if data.get('whether_name_of_the_national_and_international_codes_or_certifications_or_labels_or_standards_adopted_by_your_entity_and_mapped_to_each_principle_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherNameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrincipleIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_number_of_locations_where_markets_served_by_the_entity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherNumberOfLocationsWhereMarketsServedByTheEntityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_number_of_locations_where_markets_served_by_the_entity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherNumberOfLocationsWhereMarketsServedByTheEntityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_premises_or_offices_of_the_entity_accessible_to_differently_abled_employees_and_workers_and_steps_are_being_taken_by_the_entity_if_the_premises_or_offices_of_the_entity_not_accessible_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkersAndStepsAreBeingTakenByTheEntityIfThePremisesOrOfficesOfTheEntityNotAccessibleIsAssuredByAssurer contextRef="D_Gender_Employees_TableA">
        {{ 'true' if data.get('whether_the_premises_or_offices_of_the_entity_accessible_to_differently_abled_employees_and_workers_and_steps_are_being_taken_by_the_entity_if_the_premises_or_offices_of_the_entity_not_accessible_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkersAndStepsAreBeingTakenByTheEntityIfThePremisesOrOfficesOfTheEntityNotAccessibleIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_markets_served_by_the_entity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherMarketsServedByTheEntityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_markets_served_by_the_entity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherMarketsServedByTheEntityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('date_of_environmental_impact_assessments') is not none %}
    <in-capmkt:DateOfEnvironmentalImpactAssessments contextRef="DCYMain">
        {{ data.get('date_of_environmental_impact_assessments', '') }}
    </in-capmkt:DateOfEnvironmentalImpactAssessments>
    {% endif %}

        {% if data.get('date_on_which_statement_was_sent') is not none %}
    <in-capmkt:DateOnWhichStatementWasSent contextRef="DCYMain">
        {{ data.get('date_on_which_statement_was_sent', '') }}
    </in-capmkt:DateOnWhichStatementWasSent>
    {% endif %}

        {% if data.get('amount_invested_in_advanced_to_any_of_the_portfolio_assets_or_spv_for_service_of_debt_or_interest_as_may_be_deemed_necessary_by_the_manager') is not none %}
    <in-capmkt:AmountInvestedInAdvancedToAnyOfThePortfolioAssetsOrSPVForServiceOfDebtOrInterestAsMayBeDeemedNecessaryByTheManager contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_invested_in_advanced_to_any_of_the_portfolio_assets_or_spv_for_service_of_debt_or_interest_as_may_be_deemed_necessary_by_the_manager', '') }}
    </in-capmkt:AmountInvestedInAdvancedToAnyOfThePortfolioAssetsOrSPVForServiceOfDebtOrInterestAsMayBeDeemedNecessaryByTheManager>
    {% endif %}

        {% if data.get('details_if_the_employees_or_worker_of_the_entity_have_access_to_non_occupational_medical_and_healthcare_services_is_not_applicable_explanatory_text_block') is not none %}
    <in-capmkt:DetailsIfTheEmployeesOrWorkerOfTheEntityHaveAccessToNonOccupationalMedicalAndHealthcareServicesIsNotApplicableExplanatoryTextBlock contextRef="D_Gender_Employees_TableA" escape="true">
        {{ data.get('details_if_the_employees_or_worker_of_the_entity_have_access_to_non_occupational_medical_and_healthcare_services_is_not_applicable_explanatory_text_block', '') }}
    </in-capmkt:DetailsIfTheEmployeesOrWorkerOfTheEntityHaveAccessToNonOccupationalMedicalAndHealthcareServicesIsNotApplicableExplanatoryTextBlock>
    {% endif %}

        {% if data.get('assurance_sub_type_for_a_preferential_procurement_policy_where_preference_to_purchase_from_suppliers_comprising_marginalized_or_vulnerable_groups_and_its_percentage_of_total_procurement_by_value_does_it_constitute') is not none %}
    <in-capmkt:AssuranceSubTypeForAPreferentialProcurementPolicyWherePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroupsAndItsPercentageOfTotalProcurementByValueDoesItConstitute contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_a_preferential_procurement_policy_where_preference_to_purchase_from_suppliers_comprising_marginalized_or_vulnerable_groups_and_its_percentage_of_total_procurement_by_value_does_it_constitute', '') }}
    </in-capmkt:AssuranceSubTypeForAPreferentialProcurementPolicyWherePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroupsAndItsPercentageOfTotalProcurementByValueDoesItConstitute>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_and_weblink_of_an_anti_corruption_or_anti_bribery_policy_is_place') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsAndWeblinkOfAnAntiCorruptionOrAntiBriberyPolicyIsPlace contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_and_weblink_of_an_anti_corruption_or_anti_bribery_policy_is_place', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsAndWeblinkOfAnAntiCorruptionOrAntiBriberyPolicyIsPlace>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_public_policy_positions_advocated_by_the_entity') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfPublicPolicyPositionsAdvocatedByTheEntity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_public_policy_positions_advocated_by_the_entity', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfPublicPolicyPositionsAdvocatedByTheEntity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_has_translated_the_policy_into_procedures') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityHasTranslatedThePolicyIntoProcedures contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_has_translated_the_policy_into_procedures', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityHasTranslatedThePolicyIntoProcedures>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_have_a_framework_or_policy_on_cyber_security_and_risks_related_to_data_privacy') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_have_a_framework_or_policy_on_cyber_security_and_risks_related_to_data_privacy', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_have_an_equal_opportunity_policy_as_per_the_rights_of_persons_with_disabilities_act2016') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_have_an_equal_opportunity_policy_as_per_the_rights_of_persons_with_disabilities_act2016', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_your_entitys_policy_or_policies_cover_each_principle_and_its_core_elements_of_the_ngrb_cs') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_your_entitys_policy_or_policies_cover_each_principle_and_its_core_elements_of_the_ngrb_cs', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs>
    {% endif %}

        {% if data.get('assurance_sub_type_for_describe_the_mechanisms_to_receive_and_redress_grievances_of_the_community') is not none %}
    <in-capmkt:AssuranceSubTypeForDescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_describe_the_mechanisms_to_receive_and_redress_grievances_of_the_community', '') }}
    </in-capmkt:AssuranceSubTypeForDescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_instances_of_engagement_with_and_actions_taken_to_address_the_concerns_of_vulnerable_or_marginalized_stakeholder_groups') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableOrMarginalizedStakeholderGroups contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_instances_of_engagement_with_and_actions_taken_to_address_the_concerns_of_vulnerable_or_marginalized_stakeholder_groups', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableOrMarginalizedStakeholderGroups>
    {% endif %}

        {% if data.get('assurance_sub_type_for_list_stakeholder_groups_identified_as_key_for_your_entity_and_the_frequency_of_engagement_with_each_stakeholder_group') is not none %}
    <in-capmkt:AssuranceSubTypeForListStakeholderGroupsIdentifiedAsKeyForYourEntityAndTheFrequencyOfEngagementWithEachStakeholderGroup contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_list_stakeholder_groups_identified_as_key_for_your_entity_and_the_frequency_of_engagement_with_each_stakeholder_group', '') }}
    </in-capmkt:AssuranceSubTypeForListStakeholderGroupsIdentifiedAsKeyForYourEntityAndTheFrequencyOfEngagementWithEachStakeholderGroup>
    {% endif %}

        {% if data.get('assurance_sub_type_for_mechanisms_to_prevent_adverse_consequences_to_the_complainant_in_discrimination_and_harassment_cases') is not none %}
    <in-capmkt:AssuranceSubTypeForMechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCases contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_mechanisms_to_prevent_adverse_consequences_to_the_complainant_in_discrimination_and_harassment_cases', '') }}
    </in-capmkt:AssuranceSubTypeForMechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCases>
    {% endif %}

        {% if data.get('assurance_sub_type_for_the_entity_implemented_a_mechanism_for_zero_liquid_discharge') is not none %}
    <in-capmkt:AssuranceSubTypeForTheEntityImplementedAMechanismForZeroLiquidDischarge contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_the_entity_implemented_a_mechanism_for_zero_liquid_discharge', '') }}
    </in-capmkt:AssuranceSubTypeForTheEntityImplementedAMechanismForZeroLiquidDischarge>
    {% endif %}

        {% if data.get('assurance_sub_type_for_the_internal_mechanisms_in_place_to_redress_grievances_related_to_human_rights_issues') is not none %}
    <in-capmkt:AssuranceSubTypeForTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssues contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_the_internal_mechanisms_in_place_to_redress_grievances_related_to_human_rights_issues', '') }}
    </in-capmkt:AssuranceSubTypeForTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssues>
    {% endif %}

        {% if data.get('assurance_sub_type_for_the_mechanisms_in_place_to_receive_and_respond_to_consumer_complaints_and_feedback') is not none %}
    <in-capmkt:AssuranceSubTypeForTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedback contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_the_mechanisms_in_place_to_receive_and_respond_to_consumer_complaints_and_feedback', '') }}
    </in-capmkt:AssuranceSubTypeForTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedback>
    {% endif %}

        {% if data.get('assurance_sub_type_for_the_processes_for_consultation_between_stakeholders_and_the_board_on_economic_environmental_and_social_topics_or_if_consultation_is_delegated_how_is_feedback_from_such_consultations_provided_to_the_board') is not none %}
    <in-capmkt:AssuranceSubTypeForTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoard contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_the_processes_for_consultation_between_stakeholders_and_the_board_on_economic_environmental_and_social_topics_or_if_consultation_is_delegated_how_is_feedback_from_such_consultations_provided_to_the_board', '') }}
    </in-capmkt:AssuranceSubTypeForTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoard>
    {% endif %}

        {% if data.get('assurance_sub_type_for_the_processes_for_identifying_key_stakeholder_groups_of_the_entity') is not none %}
    <in-capmkt:AssuranceSubTypeForTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_the_processes_for_identifying_key_stakeholder_groups_of_the_entity', '') }}
    </in-capmkt:AssuranceSubTypeForTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_stakeholder_consultation_is_used_to_support_the_identification_and_management_of_environmental_and_social_topics') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_stakeholder_consultation_is_used_to_support_the_identification_and_management_of_environmental_and_social_topics', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_has_translated_the_policy_into_procedures') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityHasTranslatedThePolicyIntoProcedures contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_has_translated_the_policy_into_procedures') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityHasTranslatedThePolicyIntoProcedures>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_have_a_framework_or_policy_on_cyber_security_and_risks_related_to_data_privacy') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_have_a_framework_or_policy_on_cyber_security_and_risks_related_to_data_privacy') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_have_an_equal_opportunity_policy_as_per_the_rights_of_persons_with_disabilities_act2016') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_have_an_equal_opportunity_policy_as_per_the_rights_of_persons_with_disabilities_act2016') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_your_entitys_policy_or_policies_cover_each_principle_and_its_core_elements_of_the_ngrb_cs') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_your_entitys_policy_or_policies_cover_each_principle_and_its_core_elements_of_the_ngrb_cs') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs>
    {% endif %}

        {% if data.get('public_policy_advocated') is not none %}
    <in-capmkt:PublicPolicyAdvocated contextRef="DCYMain">
        {{ data.get('public_policy_advocated', '') }}
    </in-capmkt:PublicPolicyAdvocated>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_a_framework_or_policy_on_cyber_security_and_risks_related_to_data_privacy_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacyExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_a_framework_or_policy_on_cyber_security_and_risks_related_to_data_privacy_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacyExplanatoryTextBlock>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_a_preferential_procurement_policy_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableAPreferentialProcurementPolicyExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_a_preferential_procurement_policy_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableAPreferentialProcurementPolicyExplanatoryTextBlock>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_an_equal_opportunity_policy_as_per_the_rights_of_persons_with_disabilities_act2016_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_an_equal_opportunity_policy_as_per_the_rights_of_persons_with_disabilities_act2016_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('type_of_assurance_for_policy_and_management_processes') is not none %}
    <in-capmkt:TypeOfAssuranceForPolicyAndManagementProcesses contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_policy_and_management_processes', '') }}
    </in-capmkt:TypeOfAssuranceForPolicyAndManagementProcesses>
    {% endif %}

        {% if data.get('web_link_public_policy_position_advocated') is not none %}
    <in-capmkt:WebLinkPublicPolicyPositionAdvocated contextRef="DCYMain">
        {{ data.get('web_link_public_policy_position_advocated', '') }}
    </in-capmkt:WebLinkPublicPolicyPositionAdvocated>
    {% endif %}

        {% if data.get('description_of_other_committee_for_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification') is not none %}
    <in-capmkt:DescriptionOfOtherCommitteeForComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectification contextRef="DCYMain">
        {{ data.get('description_of_other_committee_for_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification', '') }}
    </in-capmkt:DescriptionOfOtherCommitteeForComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectification>
    {% endif %}

        {% if data.get('description_of_other_committee_for_performance_against_above_policies_and_follow_up_action') is not none %}
    <in-capmkt:DescriptionOfOtherCommitteeForPerformanceAgainstAbovePoliciesAndFollowUpAction contextRef="DCYMain">
        {{ data.get('description_of_other_committee_for_performance_against_above_policies_and_follow_up_action', '') }}
    </in-capmkt:DescriptionOfOtherCommitteeForPerformanceAgainstAbovePoliciesAndFollowUpAction>
    {% endif %}

        {% if data.get('a_mechanism_for_zero_liquid_discharge_is_not_applicable_to_the_entity_explanatory_text_block') is not none %}
    <in-capmkt:AMechanismForZeroLiquidDischargeIsNotApplicableToTheEntityExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('a_mechanism_for_zero_liquid_discharge_is_not_applicable_to_the_entity_explanatory_text_block', '') }}
    </in-capmkt:AMechanismForZeroLiquidDischargeIsNotApplicableToTheEntityExplanatoryTextBlock>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_stakeholder_consultation_is_used_to_support_the_identification_and_management_of_environmental_and_social_topics') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_stakeholder_consultation_is_used_to_support_the_identification_and_management_of_environmental_and_social_topics') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics>
    {% endif %}

        {% if data.get('name_of_stake_holder_group') is not none %}
    <in-capmkt:NameOfStakeHolderGroup contextRef="ICYMain">
        {{ data.get('name_of_stake_holder_group', '') }}
    </in-capmkt:NameOfStakeHolderGroup>
    {% endif %}

        {% if data.get('details_for_the_entity_have_not_applicable_an_anti_corruption_or_anti_bribery_policy_explanatory_text_block') is not none %}
    <in-capmkt:DetailsForTheEntityHaveNotApplicableAnAntiCorruptionOrAntiBriberyPolicyExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_for_the_entity_have_not_applicable_an_anti_corruption_or_anti_bribery_policy_explanatory_text_block', '') }}
    </in-capmkt:DetailsForTheEntityHaveNotApplicableAnAntiCorruptionOrAntiBriberyPolicyExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_the_entity_has_not_applicable_translated_the_policy_into_procedures_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfTheEntityHasNotApplicableTranslatedThePolicyIntoProceduresExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_the_entity_has_not_applicable_translated_the_policy_into_procedures_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfTheEntityHasNotApplicableTranslatedThePolicyIntoProceduresExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_the_policy_is_not_applicable_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfThePolicyIsNotApplicableExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_the_policy_is_not_applicable_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfThePolicyIsNotApplicableExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_your_entitys_policy_or_policies_has_not_applicable_each_principle_and_its_core_elements_of_the_ngrb_cs_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfYourEntitysPolicyOrPoliciesHasNotApplicableEachPrincipleAndItsCoreElementsOfTheNGRBCsExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_your_entitys_policy_or_policies_has_not_applicable_each_principle_and_its_core_elements_of_the_ngrb_cs_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfYourEntitysPolicyOrPoliciesHasNotApplicableEachPrincipleAndItsCoreElementsOfTheNGRBCsExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_for_grievance_redressal_mechanism_in_place_is_not_applicable_explanatory_text_block') is not none %}
    <in-capmkt:DetailsForGrievanceRedressalMechanismInPlaceIsNotApplicableExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_for_grievance_redressal_mechanism_in_place_is_not_applicable_explanatory_text_block', '') }}
    </in-capmkt:DetailsForGrievanceRedressalMechanismInPlaceIsNotApplicableExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_instances_of_engagement_with_and_actions_taken_to_address_the_concerns_of_vulnerable_marginalized_stakeholder_groups_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableMarginalizedStakeholderGroupsExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_instances_of_engagement_with_and_actions_taken_to_address_the_concerns_of_vulnerable_marginalized_stakeholder_groups_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableMarginalizedStakeholderGroupsExplanatoryTextBlock>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_a_preferential_procurement_policy_where_preference_to_purchase_from_suppliers_comprising_marginalized_or_vulnerable_groups_and_its_percentage_of_total_procurement_by_value_does_it_constitute') is not none %}
    <in-capmkt:RemarksForAssuranceOfAPreferentialProcurementPolicyWherePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroupsAndItsPercentageOfTotalProcurementByValueDoesItConstitute contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_a_preferential_procurement_policy_where_preference_to_purchase_from_suppliers_comprising_marginalized_or_vulnerable_groups_and_its_percentage_of_total_procurement_by_value_does_it_constitute', '') }}
    </in-capmkt:RemarksForAssuranceOfAPreferentialProcurementPolicyWherePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroupsAndItsPercentageOfTotalProcurementByValueDoesItConstitute>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_and_weblink_of_an_anti_corruption_or_anti_bribery_policy_is_place') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsAndWeblinkOfAnAntiCorruptionOrAntiBriberyPolicyIsPlace contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_and_weblink_of_an_anti_corruption_or_anti_bribery_policy_is_place', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsAndWeblinkOfAnAntiCorruptionOrAntiBriberyPolicyIsPlace>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_public_policy_positions_advocated_by_the_entity') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfPublicPolicyPositionsAdvocatedByTheEntity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_public_policy_positions_advocated_by_the_entity', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfPublicPolicyPositionsAdvocatedByTheEntity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_has_translated_the_policy_into_procedures') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityHasTranslatedThePolicyIntoProcedures contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_has_translated_the_policy_into_procedures', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityHasTranslatedThePolicyIntoProcedures>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_have_a_framework_or_policy_on_cyber_security_and_risks_related_to_data_privacy') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_have_a_framework_or_policy_on_cyber_security_and_risks_related_to_data_privacy', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_have_an_equal_opportunity_policy_as_per_the_rights_of_persons_with_disabilities_act2016') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_have_an_equal_opportunity_policy_as_per_the_rights_of_persons_with_disabilities_act2016', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_your_entitys_policy_or_policies_cover_each_principle_and_its_core_elements_of_the_ngrb_cs') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_your_entitys_policy_or_policies_cover_each_principle_and_its_core_elements_of_the_ngrb_cs', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_describe_the_mechanisms_to_receive_and_redress_grievances_of_the_community') is not none %}
    <in-capmkt:RemarksForAssuranceOfDescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_describe_the_mechanisms_to_receive_and_redress_grievances_of_the_community', '') }}
    </in-capmkt:RemarksForAssuranceOfDescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_instances_of_engagement_with_and_actions_taken_to_address_the_concerns_of_vulnerable_or_marginalized_stakeholder_groups') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableOrMarginalizedStakeholderGroups contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_instances_of_engagement_with_and_actions_taken_to_address_the_concerns_of_vulnerable_or_marginalized_stakeholder_groups', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableOrMarginalizedStakeholderGroups>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_list_stakeholder_groups_identified_as_key_for_your_entity_and_the_frequency_of_engagement_with_each_stakeholder_group') is not none %}
    <in-capmkt:RemarksForAssuranceOfListStakeholderGroupsIdentifiedAsKeyForYourEntityAndTheFrequencyOfEngagementWithEachStakeholderGroup contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_list_stakeholder_groups_identified_as_key_for_your_entity_and_the_frequency_of_engagement_with_each_stakeholder_group', '') }}
    </in-capmkt:RemarksForAssuranceOfListStakeholderGroupsIdentifiedAsKeyForYourEntityAndTheFrequencyOfEngagementWithEachStakeholderGroup>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_mechanisms_to_prevent_adverse_consequences_to_the_complainant_in_discrimination_and_harassment_cases') is not none %}
    <in-capmkt:RemarksForAssuranceOfMechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCases contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_mechanisms_to_prevent_adverse_consequences_to_the_complainant_in_discrimination_and_harassment_cases', '') }}
    </in-capmkt:RemarksForAssuranceOfMechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCases>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_the_entity_implemented_a_mechanism_for_zero_liquid_discharge') is not none %}
    <in-capmkt:RemarksForAssuranceOfTheEntityImplementedAMechanismForZeroLiquidDischarge contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_the_entity_implemented_a_mechanism_for_zero_liquid_discharge', '') }}
    </in-capmkt:RemarksForAssuranceOfTheEntityImplementedAMechanismForZeroLiquidDischarge>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_the_internal_mechanisms_in_place_to_redress_grievances_related_to_human_rights_issues') is not none %}
    <in-capmkt:RemarksForAssuranceOfTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssues contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_the_internal_mechanisms_in_place_to_redress_grievances_related_to_human_rights_issues', '') }}
    </in-capmkt:RemarksForAssuranceOfTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssues>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_the_mechanisms_in_place_to_receive_and_respond_to_consumer_complaints_and_feedback') is not none %}
    <in-capmkt:RemarksForAssuranceOfTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedback contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_the_mechanisms_in_place_to_receive_and_respond_to_consumer_complaints_and_feedback', '') }}
    </in-capmkt:RemarksForAssuranceOfTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedback>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_the_processes_for_consultation_between_stakeholders_and_the_board_on_economic_environmental_and_social_topics_or_if_consultation_is_delegated_how_is_feedback_from_such_consultations_provided_to_the_board') is not none %}
    <in-capmkt:RemarksForAssuranceOfTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoard contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_the_processes_for_consultation_between_stakeholders_and_the_board_on_economic_environmental_and_social_topics_or_if_consultation_is_delegated_how_is_feedback_from_such_consultations_provided_to_the_board', '') }}
    </in-capmkt:RemarksForAssuranceOfTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoard>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_the_processes_for_identifying_key_stakeholder_groups_of_the_entity') is not none %}
    <in-capmkt:RemarksForAssuranceOfTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_the_processes_for_identifying_key_stakeholder_groups_of_the_entity', '') }}
    </in-capmkt:RemarksForAssuranceOfTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_stakeholder_consultation_is_used_to_support_the_identification_and_management_of_environmental_and_social_topics') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_stakeholder_consultation_is_used_to_support_the_identification_and_management_of_environmental_and_social_topics', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics>
    {% endif %}

        {% if data.get('whether_a_preferential_procurement_policy_where_preference_to_purchase_from_suppliers_comprising_marginalized_or_vulnerable_groups_and_its_percentage_of_total_procurement_by_value_does_it_constitute_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherAPreferentialProcurementPolicyWherePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroupsAndItsPercentageOfTotalProcurementByValueDoesItConstituteIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_a_preferential_procurement_policy_where_preference_to_purchase_from_suppliers_comprising_marginalized_or_vulnerable_groups_and_its_percentage_of_total_procurement_by_value_does_it_constitute_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherAPreferentialProcurementPolicyWherePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroupsAndItsPercentageOfTotalProcurementByValueDoesItConstituteIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_and_weblink_of_an_anti_corruption_or_anti_bribery_policy_is_place_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsAndWeblinkOfAnAntiCorruptionOrAntiBriberyPolicyIsPlaceIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_and_weblink_of_an_anti_corruption_or_anti_bribery_policy_is_place_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsAndWeblinkOfAnAntiCorruptionOrAntiBriberyPolicyIsPlaceIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_public_policy_positions_advocated_by_the_entity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfPublicPolicyPositionsAdvocatedByTheEntityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_public_policy_positions_advocated_by_the_entity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfPublicPolicyPositionsAdvocatedByTheEntityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_any_regulatory_action_taken_against_internal_auditor_or_partner_or_director') is not none %}
    <in-capmkt:WhetherAnyRegulatoryActionTakenAgainstInternalAuditorOrPartnerORDirector contextRef="DCYMain">
        {{ 'true' if data.get('whether_any_regulatory_action_taken_against_internal_auditor_or_partner_or_director') else 'false' }}
    </in-capmkt:WhetherAnyRegulatoryActionTakenAgainstInternalAuditorOrPartnerORDirector>
    {% endif %}

        {% if data.get('whether_describe_the_mechanisms_to_receive_and_redress_grievances_of_the_community_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_describe_the_mechanisms_to_receive_and_redress_grievances_of_the_community_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_instances_of_engagement_with_and_actions_taken_to_address_the_concerns_of_vulnerable_or_marginalized_stakeholder_groups_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableOrMarginalizedStakeholderGroupsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_instances_of_engagement_with_and_actions_taken_to_address_the_concerns_of_vulnerable_or_marginalized_stakeholder_groups_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableOrMarginalizedStakeholderGroupsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_list_stakeholder_groups_identified_as_key_for_your_entity_and_the_frequency_of_engagement_with_each_stakeholder_group_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherListStakeholderGroupsIdentifiedAsKeyForYourEntityAndTheFrequencyOfEngagementWithEachStakeholderGroupIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_list_stakeholder_groups_identified_as_key_for_your_entity_and_the_frequency_of_engagement_with_each_stakeholder_group_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherListStakeholderGroupsIdentifiedAsKeyForYourEntityAndTheFrequencyOfEngagementWithEachStakeholderGroupIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_mechanisms_to_prevent_adverse_consequences_to_the_complainant_in_discrimination_and_harassment_cases_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherMechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCasesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_mechanisms_to_prevent_adverse_consequences_to_the_complainant_in_discrimination_and_harassment_cases_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherMechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCasesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_entity_implemented_a_mechanism_for_zero_liquid_discharge_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTheEntityImplementedAMechanismForZeroLiquidDischargeIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_entity_implemented_a_mechanism_for_zero_liquid_discharge_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTheEntityImplementedAMechanismForZeroLiquidDischargeIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_internal_mechanisms_in_place_to_redress_grievances_related_to_human_rights_issues_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_internal_mechanisms_in_place_to_redress_grievances_related_to_human_rights_issues_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_mechanisms_in_place_to_receive_and_respond_to_consumer_complaints_and_feedback_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedbackIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_mechanisms_in_place_to_receive_and_respond_to_consumer_complaints_and_feedback_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedbackIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_processes_for_consultation_between_stakeholders_and_the_board_on_economic_environmental_and_social_topics_or_if_consultation_is_delegated_how_is_feedback_from_such_consultations_provided_to_the_board_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoardIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_processes_for_consultation_between_stakeholders_and_the_board_on_economic_environmental_and_social_topics_or_if_consultation_is_delegated_how_is_feedback_from_such_consultations_provided_to_the_board_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoardIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_processes_for_identifying_key_stakeholder_groups_of_the_entity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_processes_for_identifying_key_stakeholder_groups_of_the_entity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_any_corrective_action_taken_or_underway_on_issues_related_to_fines_or_penalties_or_action_taken_by_regulators_or_law_enforcement_agencies_or_judicial_institutions_on_cases_of_corruption_and_conflicts_of_interest') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterest contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_any_corrective_action_taken_or_underway_on_issues_related_to_fines_or_penalties_or_action_taken_by_regulators_or_law_enforcement_agencies_or_judicial_institutions_on_cases_of_corruption_and_conflicts_of_interest', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterest>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_complaints_with_regard_to_conflict_of_interest') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfComplaintsWithRegardToConflictOfInterest contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_complaints_with_regard_to_conflict_of_interest', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfComplaintsWithRegardToConflictOfInterest>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_waste_collection_plan_is_in_line_with_the_extended_producer_responsibility_plan_submitted_to_pollution_control_boards_and_steps_taken_to_address_the_waste_collection_plan_if_not_submitted') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoardsAndStepsTakenToAddressTheWasteCollectionPlanIfNotSubmitted contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_waste_collection_plan_is_in_line_with_the_extended_producer_responsibility_plan_submitted_to_pollution_control_boards_and_steps_taken_to_address_the_waste_collection_plan_if_not_submitted', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoardsAndStepsTakenToAddressTheWasteCollectionPlanIfNotSubmitted>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_on_assessment_of_value_chain_partners') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOnAssessmentOfValueChainPartners contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_on_assessment_of_value_chain_partners', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOnAssessmentOfValueChainPartners>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_retirement_benefits') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfRetirementBenefits contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_retirement_benefits', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfRetirementBenefits>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_safety_related_incidents') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfSafetyRelatedIncidents contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_safety_related_incidents', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfSafetyRelatedIncidents>
    {% endif %}

        {% if data.get('assurance_sub_type_for_health_and_safety_management_system') is not none %}
    <in-capmkt:AssuranceSubTypeForHealthAndSafetyManagementSystem contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_health_and_safety_management_system', '') }}
    </in-capmkt:AssuranceSubTypeForHealthAndSafetyManagementSystem>
    {% endif %}

        {% if data.get('assurance_sub_type_for_measures_taken_by_the_entity_to_ensure_a_safe_and_healthy_work_place') is not none %}
    <in-capmkt:AssuranceSubTypeForMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlace contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_measures_taken_by_the_entity_to_ensure_a_safe_and_healthy_work_place', '') }}
    </in-capmkt:AssuranceSubTypeForMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlace>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_provide_transition_assistance_programs_to_facilitate_continued_employability_and_the_management_of_career_endings_resulting_from_retirement_or_termination_of_employment') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_provide_transition_assistance_programs_to_facilitate_continued_employability_and_the_management_of_career_endings_resulting_from_retirement_or_termination_of_employment', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment>
    {% endif %}

        {% if data.get('assurance_sub_type_for_complaints_filed_under_the_sexual_harassment_of_women_at_workplace') is not none %}
    <in-capmkt:AssuranceSubTypeForComplaintsFiledUnderTheSexualHarassmentOfWomenAtWorkplace contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_complaints_filed_under_the_sexual_harassment_of_women_at_workplace', '') }}
    </in-capmkt:AssuranceSubTypeForComplaintsFiledUnderTheSexualHarassmentOfWomenAtWorkplace>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_median_of_remuneration_or_salary_or_wages_and_wages_paid_to_female') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfMedianOfRemunerationOrSalaryOrWagesAndWagesPaidToFemale contextRef="D_Gender">
        {{ data.get('assurance_sub_type_for_details_of_median_of_remuneration_or_salary_or_wages_and_wages_paid_to_female', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfMedianOfRemunerationOrSalaryOrWagesAndWagesPaidToFemale>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_the_scope_and_coverage_of_any_human_rights_due_diligence_conducted') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConducted contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_the_scope_and_coverage_of_any_human_rights_due_diligence_conducted', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConducted>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_green_house_gas_emissions_and_its_intensity') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfGreenHouseGasEmissionsAndItsIntensity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_green_house_gas_emissions_and_its_intensity', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfGreenHouseGasEmissionsAndItsIntensity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_significant_direct_and_indirect_impact_of_the_entity_on_biodiversity_in_such_areas_along_with_prevention_and_remediation_activities') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfSignificantDirectAndIndirectImpactOfTheEntityOnBiodiversityInSuchAreasAlongWithPreventionAndRemediationActivities contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_significant_direct_and_indirect_impact_of_the_entity_on_biodiversity_in_such_areas_along_with_prevention_and_remediation_activities', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfSignificantDirectAndIndirectImpactOfTheEntityOnBiodiversityInSuchAreasAlongWithPreventionAndRemediationActivities>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_the_disclosures_related_to_water_discharged') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTheDisclosuresRelatedToWaterDischarged contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_the_disclosures_related_to_water_discharged', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTheDisclosuresRelatedToWaterDischarged>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_the_disclosures_related_to_water_withdrawal') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTheDisclosuresRelatedToWaterWithdrawal contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_the_disclosures_related_to_water_withdrawal', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTheDisclosuresRelatedToWaterWithdrawal>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_total_energy_consumption_in_joules_or_multiples_and_energy_intensity') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTotalEnergyConsumptionInJoulesOrMultiplesAndEnergyIntensity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_total_energy_consumption_in_joules_or_multiples_and_energy_intensity', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTotalEnergyConsumptionInJoulesOrMultiplesAndEnergyIntensity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_total_scope3_emissions_and_its_intensity') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTotalScope3EmissionsAndItsIntensity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_total_scope3_emissions_and_its_intensity', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTotalScope3EmissionsAndItsIntensity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_related_to_waste_management_by_the_entity') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsRelatedToWasteManagementByTheEntity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_related_to_waste_management_by_the_entity', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsRelatedToWasteManagementByTheEntity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_disclose_any_significant_adverse_impact_to_the_environment_arising_from_the_value_chain_of_the_entity_what_mitigation_or_adaptation_measures_have_been_taken_by_the_entity_in_this_regard') is not none %}
    <in-capmkt:AssuranceSubTypeForDiscloseAnySignificantAdverseImpactToTheEnvironmentArisingFromTheValueChainOfTheEntityWhatMitigationOrAdaptationMeasuresHaveBeenTakenByTheEntityInThisRegard contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_disclose_any_significant_adverse_impact_to_the_environment_arising_from_the_value_chain_of_the_entity_what_mitigation_or_adaptation_measures_have_been_taken_by_the_entity_in_this_regard', '') }}
    </in-capmkt:AssuranceSubTypeForDiscloseAnySignificantAdverseImpactToTheEnvironmentArisingFromTheValueChainOfTheEntityWhatMitigationOrAdaptationMeasuresHaveBeenTakenByTheEntityInThisRegard>
    {% endif %}

        {% if data.get('assurance_sub_type_for_water_withdrawal_or_consumption_and_discharge_in_areas_of_water_stress_in_kilolitres') is not none %}
    <in-capmkt:AssuranceSubTypeForWaterWithdrawalOrConsumptionAndDischargeInAreasOfWaterStressInKilolitres contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_water_withdrawal_or_consumption_and_discharge_in_areas_of_water_stress_in_kilolitres', '') }}
    </in-capmkt:AssuranceSubTypeForWaterWithdrawalOrConsumptionAndDischargeInAreasOfWaterStressInKilolitres>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_compliant_with_the_applicable_environmental_law') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityCompliantWithTheApplicableEnvironmentalLaw contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_compliant_with_the_applicable_environmental_law', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityCompliantWithTheApplicableEnvironmentalLaw>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_the_benefits_derived_and_shared_from_the_intellectual_properties_owned_or_acquired') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTheBenefitsDerivedAndSharedFromTheIntellectualPropertiesOwnedOrAcquired contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_the_benefits_derived_and_shared_from_the_intellectual_properties_owned_or_acquired', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTheBenefitsDerivedAndSharedFromTheIntellectualPropertiesOwnedOrAcquired>
    {% endif %}

        {% if data.get('assurance_sub_type_for_a_brief_on_types_of_customers') is not none %}
    <in-capmkt:AssuranceSubTypeForABriefOnTypesOfCustomers contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_a_brief_on_types_of_customers', '') }}
    </in-capmkt:AssuranceSubTypeForABriefOnTypesOfCustomers>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_have_any_sites_or_facilities_identified_as_designated_consumers_under_the_performance_achieve_and_trade_scheme_of_the_government_of_india') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveAnySitesOrFacilitiesIdentifiedAsDesignatedConsumersUnderThePerformanceAchieveAndTradeSchemeOfTheGovernmentOfIndia contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_have_any_sites_or_facilities_identified_as_designated_consumers_under_the_performance_achieve_and_trade_scheme_of_the_government_of_india', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityHaveAnySitesOrFacilitiesIdentifiedAsDesignatedConsumersUnderThePerformanceAchieveAndTradeSchemeOfTheGovernmentOfIndia>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_any_corrective_action_taken_or_underway_on_issues_related_to_fines_or_penalties_or_action_taken_by_regulators_or_law_enforcement_agencies_or_judicial_institutions_on_cases_of_corruption_and_conflicts_of_interest') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterest contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_any_corrective_action_taken_or_underway_on_issues_related_to_fines_or_penalties_or_action_taken_by_regulators_or_law_enforcement_agencies_or_judicial_institutions_on_cases_of_corruption_and_conflicts_of_interest', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterest>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_complaints_with_regard_to_conflict_of_interest') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfComplaintsWithRegardToConflictOfInterest contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_complaints_with_regard_to_conflict_of_interest', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfComplaintsWithRegardToConflictOfInterest>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_waste_collection_plan_is_in_line_with_the_extended_producer_responsibility_plan_submitted_to_pollution_control_boards_and_steps_taken_to_address_the_waste_collection_plan_if_not_submitted') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoardsAndStepsTakenToAddressTheWasteCollectionPlanIfNotSubmitted contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_waste_collection_plan_is_in_line_with_the_extended_producer_responsibility_plan_submitted_to_pollution_control_boards_and_steps_taken_to_address_the_waste_collection_plan_if_not_submitted', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoardsAndStepsTakenToAddressTheWasteCollectionPlanIfNotSubmitted>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_on_assessment_of_value_chain_partners') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOnAssessmentOfValueChainPartners contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_on_assessment_of_value_chain_partners', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOnAssessmentOfValueChainPartners>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_retirement_benefits') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfRetirementBenefits contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_retirement_benefits', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfRetirementBenefits>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_safety_related_incidents') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfSafetyRelatedIncidents contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_safety_related_incidents', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfSafetyRelatedIncidents>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_health_and_safety_management_system') is not none %}
    <in-capmkt:RemarksForAssuranceOfHealthAndSafetyManagementSystem contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_health_and_safety_management_system', '') }}
    </in-capmkt:RemarksForAssuranceOfHealthAndSafetyManagementSystem>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_measures_taken_by_the_entity_to_ensure_a_safe_and_healthy_work_place') is not none %}
    <in-capmkt:RemarksForAssuranceOfMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlace contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_measures_taken_by_the_entity_to_ensure_a_safe_and_healthy_work_place', '') }}
    </in-capmkt:RemarksForAssuranceOfMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlace>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_provide_transition_assistance_programs_to_facilitate_continued_employability_and_the_management_of_career_endings_resulting_from_retirement_or_termination_of_employment') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_provide_transition_assistance_programs_to_facilitate_continued_employability_and_the_management_of_career_endings_resulting_from_retirement_or_termination_of_employment', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_complaints_filed_under_the_sexual_harassment_of_women_at_workplace') is not none %}
    <in-capmkt:RemarksForAssuranceOfComplaintsFiledUnderTheSexualHarassmentOfWomenAtWorkplace contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_complaints_filed_under_the_sexual_harassment_of_women_at_workplace', '') }}
    </in-capmkt:RemarksForAssuranceOfComplaintsFiledUnderTheSexualHarassmentOfWomenAtWorkplace>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_median_of_remuneration_or_salary_or_wages_and_wages_paid_to_female') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfMedianOfRemunerationOrSalaryOrWagesAndWagesPaidToFemale contextRef="D_Gender">
        {{ data.get('remarks_for_assurance_of_details_of_median_of_remuneration_or_salary_or_wages_and_wages_paid_to_female', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfMedianOfRemunerationOrSalaryOrWagesAndWagesPaidToFemale>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_the_scope_and_coverage_of_any_human_rights_due_diligence_conducted') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConducted contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_the_scope_and_coverage_of_any_human_rights_due_diligence_conducted', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConducted>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_green_house_gas_emissions_and_its_intensity') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfGreenHouseGasEmissionsAndItsIntensity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_green_house_gas_emissions_and_its_intensity', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfGreenHouseGasEmissionsAndItsIntensity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_significant_direct_and_indirect_impact_of_the_entity_on_biodiversity_in_such_areas_along_with_prevention_and_remediation_activities') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfSignificantDirectAndIndirectImpactOfTheEntityOnBiodiversityInSuchAreasAlongWithPreventionAndRemediationActivities contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_significant_direct_and_indirect_impact_of_the_entity_on_biodiversity_in_such_areas_along_with_prevention_and_remediation_activities', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfSignificantDirectAndIndirectImpactOfTheEntityOnBiodiversityInSuchAreasAlongWithPreventionAndRemediationActivities>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_the_disclosures_related_to_water_discharged') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTheDisclosuresRelatedToWaterDischarged contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_the_disclosures_related_to_water_discharged', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTheDisclosuresRelatedToWaterDischarged>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_the_disclosures_related_to_water_withdrawal') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTheDisclosuresRelatedToWaterWithdrawal contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_the_disclosures_related_to_water_withdrawal', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTheDisclosuresRelatedToWaterWithdrawal>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_total_energy_consumption_in_joules_or_multiples_and_energy_intensity') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTotalEnergyConsumptionInJoulesOrMultiplesAndEnergyIntensity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_total_energy_consumption_in_joules_or_multiples_and_energy_intensity', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTotalEnergyConsumptionInJoulesOrMultiplesAndEnergyIntensity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_total_scope3_emissions_and_its_intensity') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTotalScope3EmissionsAndItsIntensity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_total_scope3_emissions_and_its_intensity', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTotalScope3EmissionsAndItsIntensity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_related_to_waste_management_by_the_entity') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsRelatedToWasteManagementByTheEntity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_related_to_waste_management_by_the_entity', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsRelatedToWasteManagementByTheEntity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_disclose_any_significant_adverse_impact_to_the_environment_arising_from_the_value_chain_of_the_entity_what_mitigation_or_adaptation_measures_have_been_taken_by_the_entity_in_this_regard') is not none %}
    <in-capmkt:RemarksForAssuranceOfDiscloseAnySignificantAdverseImpactToTheEnvironmentArisingFromTheValueChainOfTheEntityWhatMitigationOrAdaptationMeasuresHaveBeenTakenByTheEntityInThisRegard contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_disclose_any_significant_adverse_impact_to_the_environment_arising_from_the_value_chain_of_the_entity_what_mitigation_or_adaptation_measures_have_been_taken_by_the_entity_in_this_regard', '') }}
    </in-capmkt:RemarksForAssuranceOfDiscloseAnySignificantAdverseImpactToTheEnvironmentArisingFromTheValueChainOfTheEntityWhatMitigationOrAdaptationMeasuresHaveBeenTakenByTheEntityInThisRegard>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_water_withdrawal_or_consumption_and_discharge_in_areas_of_water_stress_in_kilolitres') is not none %}
    <in-capmkt:RemarksForAssuranceOfWaterWithdrawalOrConsumptionAndDischargeInAreasOfWaterStressInKilolitres contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_water_withdrawal_or_consumption_and_discharge_in_areas_of_water_stress_in_kilolitres', '') }}
    </in-capmkt:RemarksForAssuranceOfWaterWithdrawalOrConsumptionAndDischargeInAreasOfWaterStressInKilolitres>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_compliant_with_the_applicable_environmental_law') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityCompliantWithTheApplicableEnvironmentalLaw contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_compliant_with_the_applicable_environmental_law', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityCompliantWithTheApplicableEnvironmentalLaw>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_the_benefits_derived_and_shared_from_the_intellectual_properties_owned_or_acquired') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTheBenefitsDerivedAndSharedFromTheIntellectualPropertiesOwnedOrAcquired contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_the_benefits_derived_and_shared_from_the_intellectual_properties_owned_or_acquired', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTheBenefitsDerivedAndSharedFromTheIntellectualPropertiesOwnedOrAcquired>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_a_brief_on_types_of_customers') is not none %}
    <in-capmkt:RemarksForAssuranceOfABriefOnTypesOfCustomers contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_a_brief_on_types_of_customers', '') }}
    </in-capmkt:RemarksForAssuranceOfABriefOnTypesOfCustomers>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_have_any_sites_or_facilities_identified_as_designated_consumers_under_the_performance_achieve_and_trade_scheme_of_the_government_of_india') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveAnySitesOrFacilitiesIdentifiedAsDesignatedConsumersUnderThePerformanceAchieveAndTradeSchemeOfTheGovernmentOfIndia contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_have_any_sites_or_facilities_identified_as_designated_consumers_under_the_performance_achieve_and_trade_scheme_of_the_government_of_india', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityHaveAnySitesOrFacilitiesIdentifiedAsDesignatedConsumersUnderThePerformanceAchieveAndTradeSchemeOfTheGovernmentOfIndia>
    {% endif %}

        {% if data.get('whether_details_of_any_corrective_action_taken_or_underway_on_issues_related_to_fines_or_penalties_or_action_taken_by_regulators_or_law_enforcement_agencies_or_judicial_institutions_on_cases_of_corruption_and_conflicts_of_interest_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterestIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_any_corrective_action_taken_or_underway_on_issues_related_to_fines_or_penalties_or_action_taken_by_regulators_or_law_enforcement_agencies_or_judicial_institutions_on_cases_of_corruption_and_conflicts_of_interest_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterestIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_complaints_with_regard_to_conflict_of_interest_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfComplaintsWithRegardToConflictOfInterestIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_complaints_with_regard_to_conflict_of_interest_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfComplaintsWithRegardToConflictOfInterestIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_on_assessment_of_value_chain_partners_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOnAssessmentOfValueChainPartnersIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_on_assessment_of_value_chain_partners_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOnAssessmentOfValueChainPartnersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_retirement_benefits_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfRetirementBenefitsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_retirement_benefits_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfRetirementBenefitsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_safety_related_incidents_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfSafetyRelatedIncidentsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_safety_related_incidents_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfSafetyRelatedIncidentsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_health_and_safety_management_system_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherHealthAndSafetyManagementSystemIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_health_and_safety_management_system_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherHealthAndSafetyManagementSystemIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_measures_taken_by_the_entity_to_ensure_a_safe_and_healthy_work_place_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlaceIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_measures_taken_by_the_entity_to_ensure_a_safe_and_healthy_work_place_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlaceIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_complaints_filed_under_the_sexual_harassment_of_women_at_workplace_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherComplaintsFiledUnderTheSexualHarassmentOfWomenAtWorkplaceIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_complaints_filed_under_the_sexual_harassment_of_women_at_workplace_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherComplaintsFiledUnderTheSexualHarassmentOfWomenAtWorkplaceIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_median_of_remuneration_or_salary_or_wages_and_wages_paid_to_female_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfMedianOfRemunerationOrSalaryOrWagesAndWagesPaidToFemaleIsAssuredByAssurer contextRef="D_Gender">
        {{ 'true' if data.get('whether_details_of_median_of_remuneration_or_salary_or_wages_and_wages_paid_to_female_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfMedianOfRemunerationOrSalaryOrWagesAndWagesPaidToFemaleIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_the_scope_and_coverage_of_any_human_rights_due_diligence_conducted_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConductedIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_the_scope_and_coverage_of_any_human_rights_due_diligence_conducted_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConductedIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_any_independent_assessment_or_evaluation_or_assurance_has_been_carried_out_by_an_external_agency_for_total_scope3_emissions') is not none %}
    <in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForTotalScope3Emissions contextRef="DCYMain">
        {{ 'true' if data.get('whether_any_independent_assessment_or_evaluation_or_assurance_has_been_carried_out_by_an_external_agency_for_total_scope3_emissions') else 'false' }}
    </in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForTotalScope3Emissions>
    {% endif %}

        {% if data.get('whether_details_of_green_house_gas_emissions_and_its_intensity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfGreenHouseGasEmissionsAndItsIntensityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_green_house_gas_emissions_and_its_intensity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfGreenHouseGasEmissionsAndItsIntensityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_significant_direct_and_indirect_impact_of_the_entity_on_biodiversity_in_such_areas_along_with_prevention_and_remediation_activities_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfSignificantDirectAndIndirectImpactOfTheEntityOnBiodiversityInSuchAreasAlongWithPreventionAndRemediationActivitiesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_significant_direct_and_indirect_impact_of_the_entity_on_biodiversity_in_such_areas_along_with_prevention_and_remediation_activities_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfSignificantDirectAndIndirectImpactOfTheEntityOnBiodiversityInSuchAreasAlongWithPreventionAndRemediationActivitiesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_the_disclosures_related_to_water_discharged_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTheDisclosuresRelatedToWaterDischargedIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_the_disclosures_related_to_water_discharged_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTheDisclosuresRelatedToWaterDischargedIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_the_disclosures_related_to_water_withdrawal_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTheDisclosuresRelatedToWaterWithdrawalIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_the_disclosures_related_to_water_withdrawal_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTheDisclosuresRelatedToWaterWithdrawalIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_total_energy_consumption_in_joules_or_multiples_and_energy_intensity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTotalEnergyConsumptionInJoulesOrMultiplesAndEnergyIntensityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_total_energy_consumption_in_joules_or_multiples_and_energy_intensity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTotalEnergyConsumptionInJoulesOrMultiplesAndEnergyIntensityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_total_scope3_emissions_and_its_intensity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTotalScope3EmissionsAndItsIntensityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_total_scope3_emissions_and_its_intensity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTotalScope3EmissionsAndItsIntensityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_related_to_waste_management_by_the_entity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsRelatedToWasteManagementByTheEntityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_related_to_waste_management_by_the_entity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsRelatedToWasteManagementByTheEntityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_disclose_any_significant_adverse_impact_to_the_environment_arising_from_the_value_chain_of_the_entity_what_mitigation_or_adaptation_measures_have_been_taken_by_the_entity_in_this_regard_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDiscloseAnySignificantAdverseImpactToTheEnvironmentArisingFromTheValueChainOfTheEntityWhatMitigationOrAdaptationMeasuresHaveBeenTakenByTheEntityInThisRegardIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_disclose_any_significant_adverse_impact_to_the_environment_arising_from_the_value_chain_of_the_entity_what_mitigation_or_adaptation_measures_have_been_taken_by_the_entity_in_this_regard_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDiscloseAnySignificantAdverseImpactToTheEnvironmentArisingFromTheValueChainOfTheEntityWhatMitigationOrAdaptationMeasuresHaveBeenTakenByTheEntityInThisRegardIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_conditions_of_environmental_approval_or_clearance_are_being_complied_with') is not none %}
    <in-capmkt:WhetherTheConditionsOfEnvironmentalApprovalOrClearanceAreBeingCompliedWith contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_conditions_of_environmental_approval_or_clearance_are_being_complied_with') else 'false' }}
    </in-capmkt:WhetherTheConditionsOfEnvironmentalApprovalOrClearanceAreBeingCompliedWith>
    {% endif %}

        {% if data.get('whether_water_withdrawal_or_consumption_and_discharge_in_areas_of_water_stress_in_kilolitres_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherWaterWithdrawalOrConsumptionAndDischargeInAreasOfWaterStressInKilolitresIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_water_withdrawal_or_consumption_and_discharge_in_areas_of_water_stress_in_kilolitres_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherWaterWithdrawalOrConsumptionAndDischargeInAreasOfWaterStressInKilolitresIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_the_benefits_derived_and_shared_from_the_intellectual_properties_owned_or_acquired_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTheBenefitsDerivedAndSharedFromTheIntellectualPropertiesOwnedOrAcquiredIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_the_benefits_derived_and_shared_from_the_intellectual_properties_owned_or_acquired_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTheBenefitsDerivedAndSharedFromTheIntellectualPropertiesOwnedOrAcquiredIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_a_brief_on_types_of_customers_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherABriefOnTypesOfCustomersIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_a_brief_on_types_of_customers_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherABriefOnTypesOfCustomersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_waste_collection_plan_is_in_line_with_the_extended_producer_responsibility_plan_submitted_to_pollution_control_boards_and_steps_taken_to_address_the_waste_collection_plan_if_not_submitted') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoardsAndStepsTakenToAddressTheWasteCollectionPlanIfNotSubmitted contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_waste_collection_plan_is_in_line_with_the_extended_producer_responsibility_plan_submitted_to_pollution_control_boards_and_steps_taken_to_address_the_waste_collection_plan_if_not_submitted') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoardsAndStepsTakenToAddressTheWasteCollectionPlanIfNotSubmitted>
    {% endif %}

        {% if data.get('boundary_for_which_the_life_cycle_perspective_or_assessment_was_conducted') is not none %}
    <in-capmkt:BoundaryForWhichTheLifeCyclePerspectiveOrAssessmentWasConducted contextRef="DCYMain">
        {{ data.get('boundary_for_which_the_life_cycle_perspective_or_assessment_was_conducted', '') }}
    </in-capmkt:BoundaryForWhichTheLifeCyclePerspectiveOrAssessmentWasConducted>
    {% endif %}

        {% if data.get('web_link_of_results_of_life_cycle_assessments') is not none %}
    <in-capmkt:WebLinkOfResultsOfLifeCycleAssessments contextRef="DCYMain">
        {{ data.get('web_link_of_results_of_life_cycle_assessments', '') }}
    </in-capmkt:WebLinkOfResultsOfLifeCycleAssessments>
    {% endif %}

        {% if data.get('web_link_of_results_of_life_cycle_assessments_p6') is not none %}
    <in-capmkt:WebLinkOfResultsOfLifeCycleAssessmentsP6 contextRef="D_Principle6">
        {{ data.get('web_link_of_results_of_life_cycle_assessments_p6', '') }}
    </in-capmkt:WebLinkOfResultsOfLifeCycleAssessmentsP6>
    {% endif %}

        {% if data.get('an_occupational_health_and_safety_management_system_has_been_not_applicable_to_the_entity_explanatory_text_block') is not none %}
    <in-capmkt:AnOccupationalHealthAndSafetyManagementSystemHasBeenNotApplicableToTheEntityExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('an_occupational_health_and_safety_management_system_has_been_not_applicable_to_the_entity_explanatory_text_block', '') }}
    </in-capmkt:AnOccupationalHealthAndSafetyManagementSystemHasBeenNotApplicableToTheEntityExplanatoryTextBlock>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_provide_transition_assistance_programs_to_facilitate_continued_employability_and_the_management_of_career_endings_resulting_from_retirement_or_termination_of_employment') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_provide_transition_assistance_programs_to_facilitate_continued_employability_and_the_management_of_career_endings_resulting_from_retirement_or_termination_of_employment') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_transition_assistance_programs_to_facilitate_continued_employability_and_the_management_of_career_endings_resulting_from_retirement_or_termination_of_employment_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmploymentExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_transition_assistance_programs_to_facilitate_continued_employability_and_the_management_of_career_endings_resulting_from_retirement_or_termination_of_employment_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmploymentExplanatoryTextBlock>
    {% endif %}

        {% if data.get('change_in_frequency_of_payment') is not none %}
    <in-capmkt:ChangeInFrequencyOfPayment contextRef="DCYMain">
        {{ 'true' if data.get('change_in_frequency_of_payment') else 'false' }}
    </in-capmkt:ChangeInFrequencyOfPayment>
    {% endif %}

        {% if data.get('description_of_other_frequency_for_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification_of_any_non_compliances') is not none %}
    <in-capmkt:DescriptionOfOtherFrequencyForComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliances contextRef="DCYMain">
        {{ data.get('description_of_other_frequency_for_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification_of_any_non_compliances', '') }}
    </in-capmkt:DescriptionOfOtherFrequencyForComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliances>
    {% endif %}

        {% if data.get('frequency_of_interest_payments') is not none %}
    <in-capmkt:FrequencyOfInterestPayments contextRef="ICYMain">
        {{ data.get('frequency_of_interest_payments', '') }}
    </in-capmkt:FrequencyOfInterestPayments>
    {% endif %}

        {% if data.get('frequency_of_review_by_board') is not none %}
    <in-capmkt:FrequencyOfReviewByBoard contextRef="DCYMain">
        {{ data.get('frequency_of_review_by_board', '') }}
    </in-capmkt:FrequencyOfReviewByBoard>
    {% endif %}

        {% if data.get('interest_payment_frequency') is not none %}
    <in-capmkt:InterestPaymentFrequency contextRef="ICYMain">
        {{ data.get('interest_payment_frequency', '') }}
    </in-capmkt:InterestPaymentFrequency>
    {% endif %}

        {% if data.get('disclose_wages_paid_to_persons_employed') is not none %}
    <in-capmkt:DiscloseWagesPaidToPersonsEmployed contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('disclose_wages_paid_to_persons_employed', '') }}
    </in-capmkt:DiscloseWagesPaidToPersonsEmployed>
    {% endif %}

        {% if data.get('any_independent_assessment_or_evaluation_or_assurance_has_been_carried_out_by_an_external_agency_for_energy_consumption') is not none %}
    <in-capmkt:AnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForEnergyConsumption contextRef="DCYMain">
        {{ 'true' if data.get('any_independent_assessment_or_evaluation_or_assurance_has_been_carried_out_by_an_external_agency_for_energy_consumption') else 'false' }}
    </in-capmkt:AnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForEnergyConsumption>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_compliant_with_the_applicable_environmental_law') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityCompliantWithTheApplicableEnvironmentalLaw contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_compliant_with_the_applicable_environmental_law') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityCompliantWithTheApplicableEnvironmentalLaw>
    {% endif %}

        {% if data.get('energy_consumption_through_other_sources') is not none %}
    <in-capmkt:EnergyConsumptionThroughOtherSources contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('energy_consumption_through_other_sources', '') }}
    </in-capmkt:EnergyConsumptionThroughOtherSources>
    {% endif %}

        {% if data.get('name_of_other_emissions') is not none %}
    <in-capmkt:NameOfOtherEmissions contextRef="DCYMain">
        {{ data.get('name_of_other_emissions', '') }}
    </in-capmkt:NameOfOtherEmissions>
    {% endif %}

        {% if data.get('name_of_the_external_agency_if_any_independent_assessment_or_evaluation_or_assurance_has_been_carried_out_by_an_external_agency_for_areas_of_water_stress_explanatory_text_block') is not none %}
    <in-capmkt:NameOfTheExternalAgencyIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForAreasOfWaterStressExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('name_of_the_external_agency_if_any_independent_assessment_or_evaluation_or_assurance_has_been_carried_out_by_an_external_agency_for_areas_of_water_stress_explanatory_text_block', '') }}
    </in-capmkt:NameOfTheExternalAgencyIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForAreasOfWaterStressExplanatoryTextBlock>
    {% endif %}

        {% if data.get('name_of_the_external_agency_if_any_independent_assessment_or_evaluation_or_assurance_has_been_carried_out_by_an_external_agency_for_energy_consumption_explanatory_text_block') is not none %}
    <in-capmkt:NameOfTheExternalAgencyIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForEnergyConsumptionExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('name_of_the_external_agency_if_any_independent_assessment_or_evaluation_or_assurance_has_been_carried_out_by_an_external_agency_for_energy_consumption_explanatory_text_block', '') }}
    </in-capmkt:NameOfTheExternalAgencyIfAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForEnergyConsumptionExplanatoryTextBlock>
    {% endif %}

        {% if data.get('name_of_the_external_agency_that_undertook_independent_assessment_or_evaluation_or_assurance_for_total_scope3_emissions_explanatory_text_block') is not none %}
    <in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceForTotalScope3EmissionsExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('name_of_the_external_agency_that_undertook_independent_assessment_or_evaluation_or_assurance_for_total_scope3_emissions_explanatory_text_block', '') }}
    </in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceForTotalScope3EmissionsExplanatoryTextBlock>
    {% endif %}

        {% if data.get('other_emissions') is not none %}
    <in-capmkt:OtherEmissions contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('other_emissions', '') }}
    </in-capmkt:OtherEmissions>
    {% endif %}

        {% if data.get('reasons_and_corrective_action_taken_if_the_conditions_of_environmental_approval_or_clearance_are_not_being_complied_with') is not none %}
    <in-capmkt:ReasonsAndCorrectiveActionTakenIfTheConditionsOfEnvironmentalApprovalOrClearanceAreNotBeingCompliedWith contextRef="DCYMain">
        {{ data.get('reasons_and_corrective_action_taken_if_the_conditions_of_environmental_approval_or_clearance_are_not_being_complied_with', '') }}
    </in-capmkt:ReasonsAndCorrectiveActionTakenIfTheConditionsOfEnvironmentalApprovalOrClearanceAreNotBeingCompliedWith>
    {% endif %}

        {% if data.get('steps_taken_to_address_the_waste_collection_plan_explanatory_text_block') is not none %}
    <in-capmkt:StepsTakenToAddressTheWasteCollectionPlanExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('steps_taken_to_address_the_waste_collection_plan_explanatory_text_block', '') }}
    </in-capmkt:StepsTakenToAddressTheWasteCollectionPlanExplanatoryTextBlock>
    {% endif %}

        {% if data.get('the_entity_has_not_applicable_environmental_law_explanatory_text_block') is not none %}
    <in-capmkt:TheEntityHasNotApplicableEnvironmentalLawExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_entity_has_not_applicable_environmental_law_explanatory_text_block', '') }}
    </in-capmkt:TheEntityHasNotApplicableEnvironmentalLawExplanatoryTextBlock>
    {% endif %}

        {% if data.get('total_energy_consumption') is not none %}
    <in-capmkt:TotalEnergyConsumption contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('total_energy_consumption', '') }}
    </in-capmkt:TotalEnergyConsumption>
    {% endif %}

        {% if data.get('total_scope1_and_scope2_emission_intensity') is not none %}
    <in-capmkt:TotalScope1AndScope2EmissionIntensity contextRef="DCYMain">
        {{ data.get('total_scope1_and_scope2_emission_intensity', '') }}
    </in-capmkt:TotalScope1AndScope2EmissionIntensity>
    {% endif %}

        {% if data.get('total_scope3_emission_intensity_the_relevant_metric_may_be_selected_by_the_entity') is not none %}
    <in-capmkt:TotalScope3EmissionIntensityTheRelevantMetricMayBeSelectedByTheEntity contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('total_scope3_emission_intensity_the_relevant_metric_may_be_selected_by_the_entity', '') }}
    </in-capmkt:TotalScope3EmissionIntensityTheRelevantMetricMayBeSelectedByTheEntity>
    {% endif %}

        {% if data.get('total_scope3_emissions') is not none %}
    <in-capmkt:TotalScope3Emissions contextRef="DCYMain">
        {{ data.get('total_scope3_emissions', '') }}
    </in-capmkt:TotalScope3Emissions>
    {% endif %}

        {% if data.get('total_volume_of_water_consumption_per_area') is not none %}
    <in-capmkt:TotalVolumeOfWaterConsumptionPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('total_volume_of_water_consumption_per_area', '') }}
    </in-capmkt:TotalVolumeOfWaterConsumptionPerArea>
    {% endif %}

        {% if data.get('total_volume_of_water_withdrawal_per_area') is not none %}
    <in-capmkt:TotalVolumeOfWaterWithdrawalPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('total_volume_of_water_withdrawal_per_area', '') }}
    </in-capmkt:TotalVolumeOfWaterWithdrawalPerArea>
    {% endif %}

        {% if data.get('total_water_discharged_in_kilolitres_per_area') is not none %}
    <in-capmkt:TotalWaterDischargedInKilolitresPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('total_water_discharged_in_kilolitres_per_area', '') }}
    </in-capmkt:TotalWaterDischargedInKilolitresPerArea>
    {% endif %}

        {% if data.get('unit_of_hazardous_air_pollutants') is not none %}
    <in-capmkt:UnitOfHazardousAirPollutants contextRef="DCYMain">
        {{ data.get('unit_of_hazardous_air_pollutants', '') }}
    </in-capmkt:UnitOfHazardousAirPollutants>
    {% endif %}

        {% if data.get('unit_of_n_ox') is not none %}
    <in-capmkt:UnitOfNOx contextRef="DCYMain">
        {{ data.get('unit_of_n_ox', '') }}
    </in-capmkt:UnitOfNOx>
    {% endif %}

        {% if data.get('unit_of_other_emissions') is not none %}
    <in-capmkt:UnitOfOtherEmissions contextRef="DCYMain">
        {{ data.get('unit_of_other_emissions', '') }}
    </in-capmkt:UnitOfOtherEmissions>
    {% endif %}

        {% if data.get('unit_of_particulate_matter') is not none %}
    <in-capmkt:UnitOfParticulateMatter contextRef="DCYMain">
        {{ data.get('unit_of_particulate_matter', '') }}
    </in-capmkt:UnitOfParticulateMatter>
    {% endif %}

        {% if data.get('unit_of_s_ox') is not none %}
    <in-capmkt:UnitOfSOx contextRef="DCYMain">
        {{ data.get('unit_of_s_ox', '') }}
    </in-capmkt:UnitOfSOx>
    {% endif %}

        {% if data.get('unit_of_total_scope1_and_scope2_emission_intensity') is not none %}
    <in-capmkt:UnitOfTotalScope1AndScope2EmissionIntensity contextRef="DCYMain">
        {{ data.get('unit_of_total_scope1_and_scope2_emission_intensity', '') }}
    </in-capmkt:UnitOfTotalScope1AndScope2EmissionIntensity>
    {% endif %}

        {% if data.get('unit_of_total_scope1_emissions') is not none %}
    <in-capmkt:UnitOfTotalScope1Emissions contextRef="DCYMain">
        {{ data.get('unit_of_total_scope1_emissions', '') }}
    </in-capmkt:UnitOfTotalScope1Emissions>
    {% endif %}

        {% if data.get('unit_of_total_scope2_emissions') is not none %}
    <in-capmkt:UnitOfTotalScope2Emissions contextRef="DCYMain">
        {{ data.get('unit_of_total_scope2_emissions', '') }}
    </in-capmkt:UnitOfTotalScope2Emissions>
    {% endif %}

        {% if data.get('unit_of_total_scope3_emission_intensity') is not none %}
    <in-capmkt:UnitOfTotalScope3EmissionIntensity contextRef="DCYMain">
        {{ data.get('unit_of_total_scope3_emission_intensity', '') }}
    </in-capmkt:UnitOfTotalScope3EmissionIntensity>
    {% endif %}

        {% if data.get('unit_of_total_scope3_emissions') is not none %}
    <in-capmkt:UnitOfTotalScope3Emissions contextRef="DCYMain">
        {{ data.get('unit_of_total_scope3_emissions', '') }}
    </in-capmkt:UnitOfTotalScope3Emissions>
    {% endif %}

        {% if data.get('waste_intensity_the_relevant_metric_may_be_selected_by_the_entity_per_area') is not none %}
    <in-capmkt:WasteIntensityTheRelevantMetricMayBeSelectedByTheEntityPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('waste_intensity_the_relevant_metric_may_be_selected_by_the_entity_per_area', '') }}
    </in-capmkt:WasteIntensityTheRelevantMetricMayBeSelectedByTheEntityPerArea>
    {% endif %}

        {% if data.get('water_discharge_by_sent_to_third_parties_per_area') is not none %}
    <in-capmkt:WaterDischargeBySentToThirdPartiesPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_by_sent_to_third_parties_per_area', '') }}
    </in-capmkt:WaterDischargeBySentToThirdPartiesPerArea>
    {% endif %}

        {% if data.get('water_discharge_by_sent_to_third_parties_with_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeBySentToThirdPartiesWithTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_by_sent_to_third_parties_with_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeBySentToThirdPartiesWithTreatmentPerArea>
    {% endif %}

        {% if data.get('water_discharge_by_sent_to_third_parties_without_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeBySentToThirdPartiesWithoutTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_by_sent_to_third_parties_without_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeBySentToThirdPartiesWithoutTreatmentPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_groundwater_per_area') is not none %}
    <in-capmkt:WaterDischargeToGroundwaterPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_groundwater_per_area', '') }}
    </in-capmkt:WaterDischargeToGroundwaterPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_groundwater_with_out_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeToGroundwaterWithOutTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_groundwater_with_out_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeToGroundwaterWithOutTreatmentPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_groundwater_with_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeToGroundwaterWithTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_groundwater_with_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeToGroundwaterWithTreatmentPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_others_per_area') is not none %}
    <in-capmkt:WaterDischargeToOthersPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_others_per_area', '') }}
    </in-capmkt:WaterDischargeToOthersPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_others_with_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeToOthersWithTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_others_with_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeToOthersWithTreatmentPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_others_without_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeToOthersWithoutTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_others_without_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeToOthersWithoutTreatmentPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_seawater_per_area') is not none %}
    <in-capmkt:WaterDischargeToSeawaterPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_seawater_per_area', '') }}
    </in-capmkt:WaterDischargeToSeawaterPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_seawater_with_out_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeToSeawaterWithOutTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_seawater_with_out_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeToSeawaterWithOutTreatmentPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_seawater_with_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeToSeawaterWithTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_seawater_with_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeToSeawaterWithTreatmentPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_surface_water_per_area') is not none %}
    <in-capmkt:WaterDischargeToSurfaceWaterPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_surface_water_per_area', '') }}
    </in-capmkt:WaterDischargeToSurfaceWaterPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_surface_water_with_out_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeToSurfaceWaterWithOutTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_surface_water_with_out_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeToSurfaceWaterWithOutTreatmentPerArea>
    {% endif %}

        {% if data.get('water_discharge_to_surface_water_with_treatment_per_area') is not none %}
    <in-capmkt:WaterDischargeToSurfaceWaterWithTreatmentPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_discharge_to_surface_water_with_treatment_per_area', '') }}
    </in-capmkt:WaterDischargeToSurfaceWaterWithTreatmentPerArea>
    {% endif %}

        {% if data.get('water_withdrawal_by_groundwater_per_area') is not none %}
    <in-capmkt:WaterWithdrawalByGroundwaterPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_withdrawal_by_groundwater_per_area', '') }}
    </in-capmkt:WaterWithdrawalByGroundwaterPerArea>
    {% endif %}

        {% if data.get('water_withdrawal_by_others_per_area') is not none %}
    <in-capmkt:WaterWithdrawalByOthersPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_withdrawal_by_others_per_area', '') }}
    </in-capmkt:WaterWithdrawalByOthersPerArea>
    {% endif %}

        {% if data.get('water_withdrawal_by_seawater_or_desalinated_water_per_area') is not none %}
    <in-capmkt:WaterWithdrawalBySeawaterOrDesalinatedWaterPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_withdrawal_by_seawater_or_desalinated_water_per_area', '') }}
    </in-capmkt:WaterWithdrawalBySeawaterOrDesalinatedWaterPerArea>
    {% endif %}

        {% if data.get('water_withdrawal_by_surface_water_per_area') is not none %}
    <in-capmkt:WaterWithdrawalBySurfaceWaterPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_withdrawal_by_surface_water_per_area', '') }}
    </in-capmkt:WaterWithdrawalBySurfaceWaterPerArea>
    {% endif %}

        {% if data.get('water_withdrawal_by_third_party_water_per_area') is not none %}
    <in-capmkt:WaterWithdrawalByThirdPartyWaterPerArea contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('water_withdrawal_by_third_party_water_per_area', '') }}
    </in-capmkt:WaterWithdrawalByThirdPartyWaterPerArea>
    {% endif %}

        {% if data.get('method_resorted_for_such_advocacy') is not none %}
    <in-capmkt:MethodResortedForSuchAdvocacy contextRef="DCYMain">
        {{ data.get('method_resorted_for_such_advocacy', '') }}
    </in-capmkt:MethodResortedForSuchAdvocacy>
    {% endif %}

        {% if data.get('basis_of_calculating_benefit_share') is not none %}
    <in-capmkt:BasisOfCalculatingBenefitShare contextRef="DCYMain">
        {{ data.get('basis_of_calculating_benefit_share', '') }}
    </in-capmkt:BasisOfCalculatingBenefitShare>
    {% endif %}

        {% if data.get('benefit_shared') is not none %}
    <in-capmkt:BenefitShared contextRef="DCYMain">
        {{ 'true' if data.get('benefit_shared') else 'false' }}
    </in-capmkt:BenefitShared>
    {% endif %}

        {% if data.get('corrective_action_taken_for_negative_social_impact_identified') is not none %}
    <in-capmkt:CorrectiveActionTakenForNegativeSocialImpactIdentified contextRef="DCYMain">
        {{ data.get('corrective_action_taken_for_negative_social_impact_identified', '') }}
    </in-capmkt:CorrectiveActionTakenForNegativeSocialImpactIdentified>
    {% endif %}

        {% if data.get('from_which_marginalized_or_vulnerable_groups_do_you_procure') is not none %}
    <in-capmkt:FromWhichMarginalizedOrVulnerableGroupsDoYouProcure contextRef="DCYMain">
        {{ data.get('from_which_marginalized_or_vulnerable_groups_do_you_procure', '') }}
    </in-capmkt:FromWhichMarginalizedOrVulnerableGroupsDoYouProcure>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_have_any_sites_or_facilities_identified_as_designated_consumers_under_the_performance_achieve_and_trade_scheme_of_the_government_of_india') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityHaveAnySitesOrFacilitiesIdentifiedAsDesignatedConsumersUnderThePerformanceAchieveAndTradeSchemeOfTheGovernmentOfIndia contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_have_any_sites_or_facilities_identified_as_designated_consumers_under_the_performance_achieve_and_trade_scheme_of_the_government_of_india') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityHaveAnySitesOrFacilitiesIdentifiedAsDesignatedConsumersUnderThePerformanceAchieveAndTradeSchemeOfTheGovernmentOfIndia>
    {% endif %}

        {% if data.get('amount_of_cost_incurred_on_well_being_measures') is not none %}
    <in-capmkt:AmountOfCostIncurredOnWellBeingMeasures contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_of_cost_incurred_on_well_being_measures', '') }}
    </in-capmkt:AmountOfCostIncurredOnWellBeingMeasures>
    {% endif %}

        {% if data.get('details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_on_assessment_of_value_chain_partners_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOnAssessmentOfValueChainPartnersExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_any_corrective_action_taken_or_underway_to_address_safety_related_incidents_on_assessment_of_value_chain_partners_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOnAssessmentOfValueChainPartnersExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_change_in_frequency') is not none %}
    <in-capmkt:DetailsOfChangeInFrequency contextRef="ICYMain">
        {{ data.get('details_of_change_in_frequency', '') }}
    </in-capmkt:DetailsOfChangeInFrequency>
    {% endif %}

        {% if data.get('details_of_other_frequency') is not none %}
    <in-capmkt:DetailsOfOtherFrequency contextRef="ICYMain">
        {{ data.get('details_of_other_frequency', '') }}
    </in-capmkt:DetailsOfOtherFrequency>
    {% endif %}

        {% if data.get('details_of_negative_social_impact_identified') is not none %}
    <in-capmkt:DetailsOfNegativeSocialImpactIdentified contextRef="DCYMain">
        {{ data.get('details_of_negative_social_impact_identified', '') }}
    </in-capmkt:DetailsOfNegativeSocialImpactIdentified>
    {% endif %}

        {% if data.get('percentage_of_health_and_safety_practices_of_value_chain_partners_p3') is not none %}
    <in-capmkt:PercentageOfHealthAndSafetyPracticesOfValueChainPartnersP3 contextRef="D_Principle3" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_health_and_safety_practices_of_value_chain_partners_p3', '') }}
    </in-capmkt:PercentageOfHealthAndSafetyPracticesOfValueChainPartnersP3>
    {% endif %}

        {% if data.get('percentage_of_beneficiaries_from_vulnerable_and_marginalized_groups') is not none %}
    <in-capmkt:PercentageOfBeneficiariesFromVulnerableAndMarginalizedGroups contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_beneficiaries_from_vulnerable_and_marginalized_groups', '') }}
    </in-capmkt:PercentageOfBeneficiariesFromVulnerableAndMarginalizedGroups>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle1_essential_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple1EssentialIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle1_essential_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple1EssentialIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle1_leadership_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple1LeadershipIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle1_leadership_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple1LeadershipIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle2_essential_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple2EssentialIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle2_essential_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple2EssentialIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle2_leadership_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple2LeadershipIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle2_leadership_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple2LeadershipIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle3_essential_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple3EssentialIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle3_essential_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple3EssentialIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle3_leadership_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple3LeadershipIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle3_leadership_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple3LeadershipIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle4_essential_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple4EssentialIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle4_essential_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple4EssentialIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle4_leadership_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple4LeadershipIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle4_leadership_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple4LeadershipIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle5_essential_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple5EssentialIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle5_essential_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple5EssentialIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle5_leadership_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple5LeadershipIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle5_leadership_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple5LeadershipIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle6_essential_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple6EssentialIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle6_essential_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple6EssentialIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle6_leadership_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple6LeadershipIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle6_leadership_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple6LeadershipIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle7_essential_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple7EssentialIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle7_essential_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple7EssentialIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle7_leadership_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple7LeadershipIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle7_leadership_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple7LeadershipIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle8_essential_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple8EssentialIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle8_essential_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple8EssentialIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle8_leadership_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple8LeadershipIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle8_leadership_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple8LeadershipIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle9_essential_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple9EssentialIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle9_essential_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple9EssentialIndicators>
    {% endif %}

        {% if data.get('type_of_assurance_for_principle9_leadership_indicators') is not none %}
    <in-capmkt:TypeOfAssuranceForPrinciple9LeadershipIndicators contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_principle9_leadership_indicators', '') }}
    </in-capmkt:TypeOfAssuranceForPrinciple9LeadershipIndicators>
    {% endif %}

        {% if data.get('acquisition_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs') is not none %}
    <in-capmkt:AcquisitionFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('acquisition_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs', '') }}
    </in-capmkt:AcquisitionFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs>
    {% endif %}

        {% if data.get('applicable_capital_gains_and_other_taxes_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs') is not none %}
    <in-capmkt:ApplicableCapitalGainsAndOtherTaxesFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('applicable_capital_gains_and_other_taxes_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs', '') }}
    </in-capmkt:ApplicableCapitalGainsAndOtherTaxesFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_enlisted_policies_extend_to_your_value_chain_partners') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEnlistedPoliciesExtendToYourValueChainPartners contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_enlisted_policies_extend_to_your_value_chain_partners') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEnlistedPoliciesExtendToYourValueChainPartners>
    {% endif %}

        {% if data.get('cash_flows_received_from_sp_vs_and_investment_entity') is not none %}
    <in-capmkt:CashFlowsReceivedFromSPVsAndInvestmentEntity contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('cash_flows_received_from_sp_vs_and_investment_entity', '') }}
    </in-capmkt:CashFlowsReceivedFromSPVsAndInvestmentEntity>
    {% endif %}

        {% if data.get('cash_released_from_dsra_or_mmra_or_any_other_reserve_as_deemed_necessary_by_the_investment_manager') is not none %}
    <in-capmkt:CashReleasedFromDSRAOrMMRAOrAnyOtherReserveAsDeemedNecessaryByTheInvestmentManager contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('cash_released_from_dsra_or_mmra_or_any_other_reserve_as_deemed_necessary_by_the_investment_manager', '') }}
    </in-capmkt:CashReleasedFromDSRAOrMMRAOrAnyOtherReserveAsDeemedNecessaryByTheInvestmentManager>
    {% endif %}

        {% if data.get('directly_attributable_transaction_costs_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs') is not none %}
    <in-capmkt:DirectlyAttributableTransactionCostsFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('directly_attributable_transaction_costs_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs', '') }}
    </in-capmkt:DirectlyAttributableTransactionCostsFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs>
    {% endif %}

        {% if data.get('dividends_net_of_applicable_taxes_received_from_sp_vs_and_investment_entity') is not none %}
    <in-capmkt:DividendsNetOfApplicableTaxesReceivedFromSPVsAndInvestmentEntity contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('dividends_net_of_applicable_taxes_received_from_sp_vs_and_investment_entity', '') }}
    </in-capmkt:DividendsNetOfApplicableTaxesReceivedFromSPVsAndInvestmentEntity>
    {% endif %}

        {% if data.get('interest_amount_non_convertible_preference_shares') is not none %}
    <in-capmkt:InterestAmountNonConvertiblePreferenceShares contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('interest_amount_non_convertible_preference_shares', '') }}
    </in-capmkt:InterestAmountNonConvertiblePreferenceShares>
    {% endif %}

        {% if data.get('interest_amount_to_be_paid_on_due_date') is not none %}
    <in-capmkt:InterestAmountToBePaidOnDueDate contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('interest_amount_to_be_paid_on_due_date', '') }}
    </in-capmkt:InterestAmountToBePaidOnDueDate>
    {% endif %}

        {% if data.get('interest_received_from_sp_vs_and_investment_entity') is not none %}
    <in-capmkt:InterestReceivedFromSPVsAndInvestmentEntity contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('interest_received_from_sp_vs_and_investment_entity', '') }}
    </in-capmkt:InterestReceivedFromSPVsAndInvestmentEntity>
    {% endif %}

        {% if data.get('investment_manager_fees') is not none %}
    <in-capmkt:InvestmentManagerFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('investment_manager_fees', '') }}
    </in-capmkt:InvestmentManagerFees>
    {% endif %}

        {% if data.get('investments_as_permitted_under_the_reitinvit_regulations_from_fund_raised_through_external_lenders_or_bankers') is not none %}
    <in-capmkt:InvestmentsAsPermittedUnderTheREITINVITRegulationsFromFundRaisedThroughExternalLendersOrBankers contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('investments_as_permitted_under_the_reitinvit_regulations_from_fund_raised_through_external_lenders_or_bankers', '') }}
    </in-capmkt:InvestmentsAsPermittedUnderTheREITINVITRegulationsFromFundRaisedThroughExternalLendersOrBankers>
    {% endif %}

        {% if data.get('investments_as_permitted_under_the_reitinvit_regulations_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs') is not none %}
    <in-capmkt:InvestmentsAsPermittedUnderTheREITINVITRegulationsFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('investments_as_permitted_under_the_reitinvit_regulations_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs', '') }}
    </in-capmkt:InvestmentsAsPermittedUnderTheREITINVITRegulationsFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs>
    {% endif %}

        {% if data.get('mtm_loss_amount') is not none %}
    <in-capmkt:MTMLossAmount contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('mtm_loss_amount', '') }}
    </in-capmkt:MTMLossAmount>
    {% endif %}

        {% if data.get('net_asset_value') is not none %}
    <in-capmkt:NetAssetValue contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('net_asset_value', '') }}
    </in-capmkt:NetAssetValue>
    {% endif %}

        {% if data.get('other_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs') is not none %}
    <in-capmkt:OtherFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs', '') }}
    </in-capmkt:OtherFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs>
    {% endif %}

        {% if data.get('other_received_from_sp_vs_and_investment_entity') is not none %}
    <in-capmkt:OtherReceivedFromSPVsAndInvestmentEntity contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_received_from_sp_vs_and_investment_entity', '') }}
    </in-capmkt:OtherReceivedFromSPVsAndInvestmentEntity>
    {% endif %}

        {% if data.get('out_of_the_total_amount_of_distribution_declared_including_amount_in_the_form_of_amortization_of_spv_level_debt') is not none %}
    <in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredIncludingAmountInTheFormOfAmortizationOfSPVLevelDebt contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('out_of_the_total_amount_of_distribution_declared_including_amount_in_the_form_of_amortization_of_spv_level_debt', '') }}
    </in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredIncludingAmountInTheFormOfAmortizationOfSPVLevelDebt>
    {% endif %}

        {% if data.get('out_of_the_total_amount_of_distribution_declared_including_amount_per_unit_in_the_form_of_amortization_of_spv_level_debt') is not none %}
    <in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredIncludingAmountPerUnitInTheFormOfAmortizationOfSPVLevelDebt contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('out_of_the_total_amount_of_distribution_declared_including_amount_per_unit_in_the_form_of_amortization_of_spv_level_debt', '') }}
    </in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredIncludingAmountPerUnitInTheFormOfAmortizationOfSPVLevelDebt>
    {% endif %}

        {% if data.get('out_of_the_total_amount_of_distribution_declared_the_amount_in_form_of_other_income') is not none %}
    <in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountInFormOfOtherIncome contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('out_of_the_total_amount_of_distribution_declared_the_amount_in_form_of_other_income', '') }}
    </in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountInFormOfOtherIncome>
    {% endif %}

        {% if data.get('out_of_the_total_amount_of_distribution_declared_the_amount_in_the_form_of_dividend') is not none %}
    <in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountInTheFormOfDividend contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('out_of_the_total_amount_of_distribution_declared_the_amount_in_the_form_of_dividend', '') }}
    </in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountInTheFormOfDividend>
    {% endif %}

        {% if data.get('out_of_the_total_amount_of_distribution_declared_the_amount_in_the_form_of_interest_less_taxes') is not none %}
    <in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountInTheFormOfInterestLessTaxes contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('out_of_the_total_amount_of_distribution_declared_the_amount_in_the_form_of_interest_less_taxes', '') }}
    </in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountInTheFormOfInterestLessTaxes>
    {% endif %}

        {% if data.get('out_of_the_total_amount_of_distribution_declared_the_amount_per_unit_in_form_of_other_income') is not none %}
    <in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountPerUnitInFormOfOtherIncome contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('out_of_the_total_amount_of_distribution_declared_the_amount_per_unit_in_form_of_other_income', '') }}
    </in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountPerUnitInFormOfOtherIncome>
    {% endif %}

        {% if data.get('out_of_the_total_amount_of_distribution_declared_the_amount_per_unit_in_the_form_of_dividend') is not none %}
    <in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountPerUnitInTheFormOfDividend contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('out_of_the_total_amount_of_distribution_declared_the_amount_per_unit_in_the_form_of_dividend', '') }}
    </in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountPerUnitInTheFormOfDividend>
    {% endif %}

        {% if data.get('out_of_the_total_amount_of_distribution_declared_the_amount_per_unit_in_the_form_of_interest_less_taxes') is not none %}
    <in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountPerUnitInTheFormOfInterestLessTaxes contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('out_of_the_total_amount_of_distribution_declared_the_amount_per_unit_in_the_form_of_interest_less_taxes', '') }}
    </in-capmkt:OutOfTheTotalAmountOfDistributionDeclaredTheAmountPerUnitInTheFormOfInterestLessTaxes>
    {% endif %}

        {% if data.get('outstanding_amount') is not none %}
    <in-capmkt:OutstandingAmount contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('outstanding_amount', '') }}
    </in-capmkt:OutstandingAmount>
    {% endif %}

        {% if data.get('principal_amount_of_non_convertible_preference_shares') is not none %}
    <in-capmkt:PrincipalAmountOfNonConvertiblePreferenceShares contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('principal_amount_of_non_convertible_preference_shares', '') }}
    </in-capmkt:PrincipalAmountOfNonConvertiblePreferenceShares>
    {% endif %}

        {% if data.get('proceeds_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs_liquidation_of_any_other_asset_or_investment_including_cash_equivalents_or_any_form_of_fund_raise_at_reitinvit_level_adjusted') is not none %}
    <in-capmkt:ProceedsFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVsLiquidationOfAnyOtherAssetOrInvestmentIncludingCashEquivalentsOrAnyFormOfFundRaiseAtREITINVITLevelAdjusted contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('proceeds_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs_liquidation_of_any_other_asset_or_investment_including_cash_equivalents_or_any_form_of_fund_raise_at_reitinvit_level_adjusted', '') }}
    </in-capmkt:ProceedsFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVsLiquidationOfAnyOtherAssetOrInvestmentIncludingCashEquivalentsOrAnyFormOfFundRaiseAtREITINVITLevelAdjusted>
    {% endif %}

        {% if data.get('related_debts_settled_or_due_to_be_settled_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs') is not none %}
    <in-capmkt:RelatedDebtsSettledOrDueToBeSettledFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('related_debts_settled_or_due_to_be_settled_from_sale_of_investments_assets_or_sale_of_shares_of_sp_vs', '') }}
    </in-capmkt:RelatedDebtsSettledOrDueToBeSettledFromSaleOfInvestmentsAssetsOrSaleOfSharesOfSPVs>
    {% endif %}

        {% if data.get('the_enlisted_policies_do_not_applicable_extend_to_your_value_chain_partners_explanatory_text_block') is not none %}
    <in-capmkt:TheEnlistedPoliciesDoNotApplicableExtendToYourValueChainPartnersExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_enlisted_policies_do_not_applicable_extend_to_your_value_chain_partners_explanatory_text_block', '') }}
    </in-capmkt:TheEnlistedPoliciesDoNotApplicableExtendToYourValueChainPartnersExplanatoryTextBlock>
    {% endif %}

        {% if data.get('what_percentage_of_total_procurement_by_value_does_it_constitute') is not none %}
    <in-capmkt:WhatPercentageOfTotalProcurementByValueDoesItConstitute contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('what_percentage_of_total_procurement_by_value_does_it_constitute', '') }}
    </in-capmkt:WhatPercentageOfTotalProcurementByValueDoesItConstitute>
    {% endif %}

        {% if data.get('clearing_number') is not none %}
    <in-capmkt:ClearingNumber contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('clearing_number', '') }}
    </in-capmkt:ClearingNumber>
    {% endif %}

        {% if data.get('eia_notification_number') is not none %}
    <in-capmkt:EIANotificationNumber contextRef="DCYMain">
        {{ data.get('eia_notification_number', '') }}
    </in-capmkt:EIANotificationNumber>
    {% endif %}

        {% if data.get('sebi_registration_number_for_cdx') is not none %}
    <in-capmkt:SEBIRegistrationNumberForCDX contextRef="DCYMain">
        {{ data.get('sebi_registration_number_for_cdx', '') }}
    </in-capmkt:SEBIRegistrationNumberForCDX>
    {% endif %}

        {% if data.get('sebi_registration_number_for_cash') is not none %}
    <in-capmkt:SEBIRegistrationNumberForCash contextRef="DCYMain">
        {{ data.get('sebi_registration_number_for_cash', '') }}
    </in-capmkt:SEBIRegistrationNumberForCash>
    {% endif %}

        {% if data.get('sebi_registration_number_for_debt') is not none %}
    <in-capmkt:SEBIRegistrationNumberForDebt contextRef="DCYMain">
        {{ data.get('sebi_registration_number_for_debt', '') }}
    </in-capmkt:SEBIRegistrationNumberForDebt>
    {% endif %}

        {% if data.get('sebi_registration_number_for_derivatives') is not none %}
    <in-capmkt:SEBIRegistrationNumberForDerivatives contextRef="DCYMain">
        {{ data.get('sebi_registration_number_for_derivatives', '') }}
    </in-capmkt:SEBIRegistrationNumberForDerivatives>
    {% endif %}

        {% if data.get('sia_notification_number') is not none %}
    <in-capmkt:SIANotificationNumber contextRef="DCYMain">
        {{ data.get('sia_notification_number', '') }}
    </in-capmkt:SIANotificationNumber>
    {% endif %}

        {% if data.get('total_consideration_of_the_asset_acquired') is not none %}
    <in-capmkt:TotalConsiderationOfTheAssetAcquired contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('total_consideration_of_the_asset_acquired', '') }}
    </in-capmkt:TotalConsiderationOfTheAssetAcquired>
    {% endif %}

        {% if data.get('total_consideration_of_the_asset_disposed_off') is not none %}
    <in-capmkt:TotalConsiderationOfTheAssetDisposedOff contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('total_consideration_of_the_asset_disposed_off', '') }}
    </in-capmkt:TotalConsiderationOfTheAssetDisposedOff>
    {% endif %}

        {% if data.get('total_electricity_consumption') is not none %}
    <in-capmkt:TotalElectricityConsumption contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('total_electricity_consumption', '') }}
    </in-capmkt:TotalElectricityConsumption>
    {% endif %}

        {% if data.get('total_fuel_consumption') is not none %}
    <in-capmkt:TotalFuelConsumption contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('total_fuel_consumption', '') }}
    </in-capmkt:TotalFuelConsumption>
    {% endif %}

        {% if data.get('total_wage_cost') is not none %}
    <in-capmkt:TotalWageCost contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('total_wage_cost', '') }}
    </in-capmkt:TotalWageCost>
    {% endif %}

        {% if data.get('algo_facility') is not none %}
    <in-capmkt:ALGOFacility contextRef="DCYMain">
        {{ 'true' if data.get('algo_facility') else 'false' }}
    </in-capmkt:ALGOFacility>
    {% endif %}

        {% if data.get('acquisition_from_fund_raised_through_external_lenders_or_bankers') is not none %}
    <in-capmkt:AcquisitionFromFundRaisedThroughExternalLendersOrBankers contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('acquisition_from_fund_raised_through_external_lenders_or_bankers', '') }}
    </in-capmkt:AcquisitionFromFundRaisedThroughExternalLendersOrBankers>
    {% endif %}

        {% if data.get('actual_date_of_interest_payment') is not none %}
    <in-capmkt:ActualDateOfInterestPayment contextRef="DCYMain">
        {{ data.get('actual_date_of_interest_payment', '') }}
    </in-capmkt:ActualDateOfInterestPayment>
    {% endif %}

        {% if data.get('actual_date_of_redemption') is not none %}
    <in-capmkt:ActualDateOfRedemption contextRef="DCYMain">
        {{ data.get('actual_date_of_redemption', '') }}
    </in-capmkt:ActualDateOfRedemption>
    {% endif %}

        {% if data.get('actual_payment_date') is not none %}
    <in-capmkt:ActualPaymentDate contextRef="DCYMain">
        {{ data.get('actual_payment_date', '') }}
    </in-capmkt:ActualPaymentDate>
    {% endif %}

        {% if data.get('address_of_the_audit_firm') is not none %}
    <in-capmkt:AddressOfTheAuditFirm contextRef="DCYMain">
        {{ data.get('address_of_the_audit_firm', '') }}
    </in-capmkt:AddressOfTheAuditFirm>
    {% endif %}

        {% if data.get('address_of_the_auditor') is not none %}
    <in-capmkt:AddressOfTheAuditor contextRef="DCYMain">
        {{ data.get('address_of_the_auditor', '') }}
    </in-capmkt:AddressOfTheAuditor>
    {% endif %}

        {% if data.get('aggregate_consolidated_borrowing') is not none %}
    <in-capmkt:AggregateConsolidatedBorrowing contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('aggregate_consolidated_borrowing', '') }}
    </in-capmkt:AggregateConsolidatedBorrowing>
    {% endif %}

        {% if data.get('aggregate_consolidated_borrowing_along_with_interest_payable') is not none %}
    <in-capmkt:AggregateConsolidatedBorrowingAlongWithInterestPayable contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('aggregate_consolidated_borrowing_along_with_interest_payable', '') }}
    </in-capmkt:AggregateConsolidatedBorrowingAlongWithInterestPayable>
    {% endif %}

        {% if data.get('any_fines_or_penalties_or_action_taken_by_regulatory_agencies_such_as_pollution_control_boards_or_by_courts') is not none %}
    <in-capmkt:AnyFinesOrPenaltiesOrActionTakenByRegulatoryAgenciesSuchAsPollutionControlBoardsOrByCourts contextRef="DCYMain">
        {{ data.get('any_fines_or_penalties_or_action_taken_by_regulatory_agencies_such_as_pollution_control_boards_or_by_courts', '') }}
    </in-capmkt:AnyFinesOrPenaltiesOrActionTakenByRegulatoryAgenciesSuchAsPollutionControlBoardsOrByCourts>
    {% endif %}

        {% if data.get('any_other_reasons_if_policies_not_cover_each_principle_and_its_core_elements_of_the_ngrb_cs_explanatory_text_block') is not none %}
    <in-capmkt:AnyOtherReasonsIfPoliciesNotCoverEachPrincipleAndItsCoreElementsOfTheNGRBCsExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('any_other_reasons_if_policies_not_cover_each_principle_and_its_core_elements_of_the_ngrb_cs_explanatory_text_block', '') }}
    </in-capmkt:AnyOtherReasonsIfPoliciesNotCoverEachPrincipleAndItsCoreElementsOfTheNGRBCsExplanatoryTextBlock>
    {% endif %}

        {% if data.get('applicable_capital_gains_and_other_taxes_from_fund_raised_through_external_lenders_or_bankers') is not none %}
    <in-capmkt:ApplicableCapitalGainsAndOtherTaxesFromFundRaisedThroughExternalLendersOrBankers contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('applicable_capital_gains_and_other_taxes_from_fund_raised_through_external_lenders_or_bankers', '') }}
    </in-capmkt:ApplicableCapitalGainsAndOtherTaxesFromFundRaisedThroughExternalLendersOrBankers>
    {% endif %}

        {% if data.get('are_you_stock_broker_or_auditor') is not none %}
    <in-capmkt:AreYouStockBrokerOrAuditor contextRef="DCYMain">
        {{ data.get('are_you_stock_broker_or_auditor', '') }}
    </in-capmkt:AreYouStockBrokerOrAuditor>
    {% endif %}

        {% if data.get('asset_cover_available_in_case_of_non_convertible_debt_securities_explanatory_text_block') is not none %}
    <in-capmkt:AssetCoverAvailableInCaseOfNonConvertibleDebtSecuritiesExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('asset_cover_available_in_case_of_non_convertible_debt_securities_explanatory_text_block', '') }}
    </in-capmkt:AssetCoverAvailableInCaseOfNonConvertibleDebtSecuritiesExplanatoryTextBlock>
    {% endif %}

        {% if data.get('assets') is not none %}
    <in-capmkt:Assets contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('assets', '') }}
    </in-capmkt:Assets>
    {% endif %}

        {% if data.get('assets_on_which_charge_is_created_by_loan_or_ecb') is not none %}
    <in-capmkt:AssetsOnWhichChargeIsCreatedByLoanOrECB contextRef="ICYMain">
        {{ data.get('assets_on_which_charge_is_created_by_loan_or_ecb', '') }}
    </in-capmkt:AssetsOnWhichChargeIsCreatedByLoanOrECB>
    {% endif %}

        {% if data.get('assets_on_which_charge_is_created_by_nc_ds') is not none %}
    <in-capmkt:AssetsOnWhichChargeIsCreatedByNCDs contextRef="ICYMain">
        {{ data.get('assets_on_which_charge_is_created_by_nc_ds', '') }}
    </in-capmkt:AssetsOnWhichChargeIsCreatedByNCDs>
    {% endif %}

        {% if data.get('assets_on_which_charge_is_created_by_preference_share') is not none %}
    <in-capmkt:AssetsOnWhichChargeIsCreatedByPreferenceShare contextRef="ICYMain">
        {{ data.get('assets_on_which_charge_is_created_by_preference_share', '') }}
    </in-capmkt:AssetsOnWhichChargeIsCreatedByPreferenceShare>
    {% endif %}

        {% if data.get('assurer_has_assured_whether_the_entity_has_carried_out_independent_assessment_evaluation_of_the_working_of_its_policies_by_an_external_agency') is not none %}
    <in-capmkt:AssurerHasAssuredWhetherTheEntityHasCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency contextRef="DCYMain">
        {{ 'true' if data.get('assurer_has_assured_whether_the_entity_has_carried_out_independent_assessment_evaluation_of_the_working_of_its_policies_by_an_external_agency') else 'false' }}
    </in-capmkt:AssurerHasAssuredWhetherTheEntityHasCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency>
    {% endif %}

        {% if data.get('audit_date') is not none %}
    <in-capmkt:AuditDate contextRef="DCYMain">
        {{ data.get('audit_date', '') }}
    </in-capmkt:AuditDate>
    {% endif %}

        {% if data.get('audited_by') is not none %}
    <in-capmkt:AuditedBy contextRef="DCYMain">
        {{ data.get('audited_by', '') }}
    </in-capmkt:AuditedBy>
    {% endif %}

        {% if data.get('audited_segments') is not none %}
    <in-capmkt:AuditedSegments contextRef="DCYMain">
        {{ data.get('audited_segments', '') }}
    </in-capmkt:AuditedSegments>
    {% endif %}

        {% if data.get('auditor_fees') is not none %}
    <in-capmkt:AuditorFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('auditor_fees', '') }}
    </in-capmkt:AuditorFees>
    {% endif %}

        {% if data.get('brief_of_any_issues_related_to_anti_competitive_conduct_by_the_entity') is not none %}
    <in-capmkt:BriefOfAnyIssuesRelatedToAntiCompetitiveConductByTheEntity contextRef="DCYMain">
        {{ data.get('brief_of_any_issues_related_to_anti_competitive_conduct_by_the_entity', '') }}
    </in-capmkt:BriefOfAnyIssuesRelatedToAntiCompetitiveConductByTheEntity>
    {% endif %}

        {% if data.get('brief_of_the_case_for_intellectual_property_related_disputes') is not none %}
    <in-capmkt:BriefOfTheCaseForIntellectualPropertyRelatedDisputes contextRef="DCYMain">
        {{ data.get('brief_of_the_case_for_intellectual_property_related_disputes', '') }}
    </in-capmkt:BriefOfTheCaseForIntellectualPropertyRelatedDisputes>
    {% endif %}

        {% if data.get('csar_audited_by') is not none %}
    <in-capmkt:CSARAuditedBy contextRef="DCYMain">
        {{ data.get('csar_audited_by', '') }}
    </in-capmkt:CSARAuditedBy>
    {% endif %}

        {% if data.get('csar_undertaking') is not none %}
    <in-capmkt:CSARUndertaking contextRef="DCYMain">
        {{ 'true' if data.get('csar_undertaking') else 'false' }}
    </in-capmkt:CSARUndertaking>
    {% endif %}

        {% if data.get('capital') is not none %}
    <in-capmkt:Capital contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('capital', '') }}
    </in-capmkt:Capital>
    {% endif %}

        {% if data.get('capital_held_by_other_shareholders') is not none %}
    <in-capmkt:CapitalHeldByOtherShareholders contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('capital_held_by_other_shareholders', '') }}
    </in-capmkt:CapitalHeldByOtherShareholders>
    {% endif %}

        {% if data.get('capital_held_by_reitsinvits_directly_or_indirectly') is not none %}
    <in-capmkt:CapitalHeldByREITSINVITSDirectlyOrIndirectly contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('capital_held_by_reitsinvits_directly_or_indirectly', '') }}
    </in-capmkt:CapitalHeldByREITSINVITSDirectlyOrIndirectly>
    {% endif %}

        {% if data.get('capital_redemption_reserve') is not none %}
    <in-capmkt:CapitalRedemptionReserve contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('capital_redemption_reserve', '') }}
    </in-capmkt:CapitalRedemptionReserve>
    {% endif %}

        {% if data.get('capitalisation') is not none %}
    <in-capmkt:Capitalisation contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('capitalisation', '') }}
    </in-capmkt:Capitalisation>
    {% endif %}

        {% if data.get('category') is not none %}
    <in-capmkt:Category contextRef="DCYMain">
        {{ data.get('category', '') }}
    </in-capmkt:Category>
    {% endif %}

        {% if data.get('class_of_security_reits_or_invits') is not none %}
    <in-capmkt:ClassOfSecurityREITSOrINVITS contextRef="DCYMain">
        {{ data.get('class_of_security_reits_or_invits', '') }}
    </in-capmkt:ClassOfSecurityREITSOrINVITS>
    {% endif %}

        {% if data.get('closing_date') is not none %}
    <in-capmkt:ClosingDate contextRef="DCYMain">
        {{ data.get('closing_date', '') }}
    </in-capmkt:ClosingDate>
    {% endif %}

        {% if data.get('code_of_client') is not none %}
    <in-capmkt:CodeOfClient contextRef="DCYMain">
        {{ data.get('code_of_client', '') }}
    </in-capmkt:CodeOfClient>
    {% endif %}

        {% if data.get('compliance_status') is not none %}
    <in-capmkt:ComplianceStatus contextRef="DCYMain">
        {{ data.get('compliance_status', '') }}
    </in-capmkt:ComplianceStatus>
    {% endif %}

        {% if data.get('corrective_action_report_to_be_submitted') is not none %}
    <in-capmkt:CorrectiveActionReportToBeSubmitted contextRef="DCYMain">
        {{ 'true' if data.get('corrective_action_report_to_be_submitted') else 'false' }}
    </in-capmkt:CorrectiveActionReportToBeSubmitted>
    {% endif %}

        {% if data.get('corrective_action_taken_for_any_issues_related_to_anti_competitive_conduct_by_the_entity') is not none %}
    <in-capmkt:CorrectiveActionTakenForAnyIssuesRelatedToAntiCompetitiveConductByTheEntity contextRef="DCYMain">
        {{ data.get('corrective_action_taken_for_any_issues_related_to_anti_competitive_conduct_by_the_entity', '') }}
    </in-capmkt:CorrectiveActionTakenForAnyIssuesRelatedToAntiCompetitiveConductByTheEntity>
    {% endif %}

        {% if data.get('corrective_action_taken_for_initiative') is not none %}
    <in-capmkt:CorrectiveActionTakenForInitiative contextRef="DCYMain">
        {{ data.get('corrective_action_taken_for_initiative', '') }}
    </in-capmkt:CorrectiveActionTakenForInitiative>
    {% endif %}

        {% if data.get('corrective_action_taken_for_intellectual_property_related_disputes') is not none %}
    <in-capmkt:CorrectiveActionTakenForIntellectualPropertyRelatedDisputes contextRef="DCYMain">
        {{ data.get('corrective_action_taken_for_intellectual_property_related_disputes', '') }}
    </in-capmkt:CorrectiveActionTakenForIntellectualPropertyRelatedDisputes>
    {% endif %}

        {% if data.get('corrective_action_taken_for_non_compliance') is not none %}
    <in-capmkt:CorrectiveActionTakenForNonCompliance contextRef="DCYMain">
        {{ data.get('corrective_action_taken_for_non_compliance', '') }}
    </in-capmkt:CorrectiveActionTakenForNonCompliance>
    {% endif %}

        {% if data.get('coupon_rate') is not none %}
    <in-capmkt:CouponRate contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('coupon_rate', '') }}
    </in-capmkt:CouponRate>
    {% endif %}

        {% if data.get('credit_rating') is not none %}
    <in-capmkt:CreditRating contextRef="ICYMain">
        {{ data.get('credit_rating', '') }}
    </in-capmkt:CreditRating>
    {% endif %}

        {% if data.get('current_car_status') is not none %}
    <in-capmkt:CurrentCARStatus contextRef="DCYMain">
        {{ data.get('current_car_status', '') }}
    </in-capmkt:CurrentCARStatus>
    {% endif %}

        {% if data.get('current_for_status') is not none %}
    <in-capmkt:CurrentFORStatus contextRef="DCYMain">
        {{ data.get('current_for_status', '') }}
    </in-capmkt:CurrentFORStatus>
    {% endif %}

        {% if data.get('current_finding') is not none %}
    <in-capmkt:CurrentFinding contextRef="DCYMain">
        {{ data.get('current_finding', '') }}
    </in-capmkt:CurrentFinding>
    {% endif %}

        {% if data.get('current_maturitiesof_long_term_borrowings') is not none %}
    <in-capmkt:CurrentMaturitiesofLongTermBorrowings contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('current_maturitiesof_long_term_borrowings', '') }}
    </in-capmkt:CurrentMaturitiesofLongTermBorrowings>
    {% endif %}

        {% if data.get('dma_facility') is not none %}
    <in-capmkt:DMAFacility contextRef="DCYMain">
        {{ 'true' if data.get('dma_facility') else 'false' }}
    </in-capmkt:DMAFacility>
    {% endif %}

        {% if data.get('deadline_for_corrective_action') is not none %}
    <in-capmkt:DeadlineForCorrectiveAction contextRef="DCYMain">
        {{ data.get('deadline_for_corrective_action', '') }}
    </in-capmkt:DeadlineForCorrectiveAction>
    {% endif %}

        {% if data.get('deadline_for_the_revised_corrective_action') is not none %}
    <in-capmkt:DeadlineForTheRevisedCorrectiveAction contextRef="DCYMain">
        {{ data.get('deadline_for_the_revised_corrective_action', '') }}
    </in-capmkt:DeadlineForTheRevisedCorrectiveAction>
    {% endif %}

        {% if data.get('debenture_redemption_reserve') is not none %}
    <in-capmkt:DebentureRedemptionReserve contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('debenture_redemption_reserve', '') }}
    </in-capmkt:DebentureRedemptionReserve>
    {% endif %}

        {% if data.get('debit_balance') is not none %}
    <in-capmkt:DebitBalance contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('debit_balance', '') }}
    </in-capmkt:DebitBalance>
    {% endif %}

        {% if data.get('debt_equity_ratio') is not none %}
    <in-capmkt:DebtEquityRatio contextRef="DCYMain">
        {{ data.get('debt_equity_ratio', '') }}
    </in-capmkt:DebtEquityRatio>
    {% endif %}

        {% if data.get('default_details') is not none %}
    <in-capmkt:DefaultDetails contextRef="ICYMain">
        {{ data.get('default_details', '') }}
    </in-capmkt:DefaultDetails>
    {% endif %}

        {% if data.get('deferred_payment_liability') is not none %}
    <in-capmkt:DeferredPaymentLiability contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('deferred_payment_liability', '') }}
    </in-capmkt:DeferredPaymentLiability>
    {% endif %}

        {% if data.get('deferred_payment_of_reitinvit_hold_co_spv') is not none %}
    <in-capmkt:DeferredPaymentOfREITINVITHoldCoSPV contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('deferred_payment_of_reitinvit_hold_co_spv', '') }}
    </in-capmkt:DeferredPaymentOfREITINVITHoldCoSPV>
    {% endif %}

        {% if data.get('department') is not none %}
    <in-capmkt:Department contextRef="DCYMain">
        {{ data.get('department', '') }}
    </in-capmkt:Department>
    {% endif %}

        {% if data.get('description_of_finding_or_observation') is not none %}
    <in-capmkt:DescriptionOfFindingOrObservation contextRef="DCYMain">
        {{ data.get('description_of_finding_or_observation', '') }}
    </in-capmkt:DescriptionOfFindingOrObservation>
    {% endif %}

        {% if data.get('description_of_presentation_currency') is not none %}
    <in-capmkt:DescriptionOfPresentationCurrency contextRef="DCYMain">
        {{ data.get('description_of_presentation_currency', '') }}
    </in-capmkt:DescriptionOfPresentationCurrency>
    {% endif %}

        {% if data.get('designation_of_auditor') is not none %}
    <in-capmkt:DesignationOfAuditor contextRef="DCYMain">
        {{ data.get('designation_of_auditor', '') }}
    </in-capmkt:DesignationOfAuditor>
    {% endif %}

        {% if data.get('designation_of_signatory_person') is not none %}
    <in-capmkt:DesignationOfSignatoryPerson contextRef="ICYMain">
        {{ data.get('designation_of_signatory_person', '') }}
    </in-capmkt:DesignationOfSignatoryPerson>
    {% endif %}

        {% if data.get('deviations') is not none %}
    <in-capmkt:Deviations contextRef="DCYMain">
        {{ data.get('deviations', '') }}
    </in-capmkt:Deviations>
    {% endif %}

        {% if data.get('directly_attributable_transaction_costs_from_fund_raised_through_external_lenders_or_bankers') is not none %}
    <in-capmkt:DirectlyAttributableTransactionCostsFromFundRaisedThroughExternalLendersOrBankers contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('directly_attributable_transaction_costs_from_fund_raised_through_external_lenders_or_bankers', '') }}
    </in-capmkt:DirectlyAttributableTransactionCostsFromFundRaisedThroughExternalLendersOrBankers>
    {% endif %}

        {% if data.get('district_of_project') is not none %}
    <in-capmkt:DistrictOfProject contextRef="DCYMain">
        {{ data.get('district_of_project', '') }}
    </in-capmkt:DistrictOfProject>
    {% endif %}

        {% if data.get('due_date_for_redemption_or_maturity') is not none %}
    <in-capmkt:DueDateForRedemptionOrMaturity contextRef="DCYMain">
        {{ data.get('due_date_for_redemption_or_maturity', '') }}
    </in-capmkt:DueDateForRedemptionOrMaturity>
    {% endif %}

        {% if data.get('due_date_of_interest_or_redemption') is not none %}
    <in-capmkt:DueDateOfInterestOrRedemption contextRef="DCYMain">
        {{ data.get('due_date_of_interest_or_redemption', '') }}
    </in-capmkt:DueDateOfInterestOrRedemption>
    {% endif %}

        {% if data.get('due_date_of_interest_payment') is not none %}
    <in-capmkt:DueDateOfInterestPayment contextRef="DCYMain">
        {{ data.get('due_date_of_interest_payment', '') }}
    </in-capmkt:DueDateOfInterestPayment>
    {% endif %}

        {% if data.get('due_date_of_the_payment_of_distribution') is not none %}
    <in-capmkt:DueDateOfThePaymentOfDistribution contextRef="DCYMain">
        {{ data.get('due_date_of_the_payment_of_distribution', '') }}
    </in-capmkt:DueDateOfThePaymentOfDistribution>
    {% endif %}

        {% if data.get('earningpershare') is not none %}
    <in-capmkt:Earningpershare contextRef="DCYMain">
        {{ data.get('earningpershare', '') }}
    </in-capmkt:Earningpershare>
    {% endif %}

        {% if data.get('end_time_of_board_meeting') is not none %}
    <in-capmkt:EndTimeOfBoardMeeting contextRef="DCYMain">
        {{ data.get('end_time_of_board_meeting', '') }}
    </in-capmkt:EndTimeOfBoardMeeting>
    {% endif %}

        {% if data.get('expense_in_the_nature_of_capital_expenditure_or_repair_at_reitinvit_level_or_portfolio_asset') is not none %}
    <in-capmkt:ExpenseInTheNatureOfCapitalExpenditureOrRepairAtREITINVITLevelOrPortfolioAsset contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('expense_in_the_nature_of_capital_expenditure_or_repair_at_reitinvit_level_or_portfolio_asset', '') }}
    </in-capmkt:ExpenseInTheNatureOfCapitalExpenditureOrRepairAtREITINVITLevelOrPortfolioAsset>
    {% endif %}

        {% if data.get('facilities_provided') is not none %}
    <in-capmkt:FacilitiesProvided contextRef="DCYMain">
        {{ data.get('facilities_provided', '') }}
    </in-capmkt:FacilitiesProvided>
    {% endif %}

        {% if data.get('fees') is not none %}
    <in-capmkt:Fees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('fees', '') }}
    </in-capmkt:Fees>
    {% endif %}

        {% if data.get('filing_for_sar_or_car_or_for') is not none %}
    <in-capmkt:FilingForSAROrCAROrFOR contextRef="DCYMain">
        {{ data.get('filing_for_sar_or_car_or_for', '') }}
    </in-capmkt:FilingForSAROrCAROrFOR>
    {% endif %}

        {% if data.get('financial_details_explanatory_text_block') is not none %}
    <in-capmkt:FinancialDetailsExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('financial_details_explanatory_text_block', '') }}
    </in-capmkt:FinancialDetailsExplanatoryTextBlock>
    {% endif %}

        {% if data.get('follow_up_audit_required') is not none %}
    <in-capmkt:FollowUpAuditRequired contextRef="DCYMain">
        {{ 'true' if data.get('follow_up_audit_required') else 'false' }}
    </in-capmkt:FollowUpAuditRequired>
    {% endif %}

        {% if data.get('funds_raised_through_debt_consolidated_during_the_period') is not none %}
    <in-capmkt:FundsRaisedThroughDebtConsolidatedDuringThePeriod contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('funds_raised_through_debt_consolidated_during_the_period', '') }}
    </in-capmkt:FundsRaisedThroughDebtConsolidatedDuringThePeriod>
    {% endif %}

        {% if data.get('ibt_facility') is not none %}
    <in-capmkt:IBTFacility contextRef="DCYMain">
        {{ 'true' if data.get('ibt_facility') else 'false' }}
    </in-capmkt:IBTFacility>
    {% endif %}

        {% if data.get('i_further_confirm_that_all_the_branches_where_algo_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') is not none %}
    <in-capmkt:IFurtherConfirmThatAllTheBranchesWhereALGOFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments contextRef="DCYMain">
        {{ 'true' if data.get('i_further_confirm_that_all_the_branches_where_algo_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') else 'false' }}
    </in-capmkt:IFurtherConfirmThatAllTheBranchesWhereALGOFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments>
    {% endif %}

        {% if data.get('i_further_confirm_that_all_the_branches_where_dma_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') is not none %}
    <in-capmkt:IFurtherConfirmThatAllTheBranchesWhereDMAFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments contextRef="DCYMain">
        {{ 'true' if data.get('i_further_confirm_that_all_the_branches_where_dma_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') else 'false' }}
    </in-capmkt:IFurtherConfirmThatAllTheBranchesWhereDMAFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments>
    {% endif %}

        {% if data.get('i_further_confirm_that_all_the_branches_where_ibt_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') is not none %}
    <in-capmkt:IFurtherConfirmThatAllTheBranchesWhereIBTFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments contextRef="DCYMain">
        {{ 'true' if data.get('i_further_confirm_that_all_the_branches_where_ibt_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') else 'false' }}
    </in-capmkt:IFurtherConfirmThatAllTheBranchesWhereIBTFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments>
    {% endif %}

        {% if data.get('i_further_confirm_that_all_the_branches_where_iml_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') is not none %}
    <in-capmkt:IFurtherConfirmThatAllTheBranchesWhereIMLFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments contextRef="DCYMain">
        {{ 'true' if data.get('i_further_confirm_that_all_the_branches_where_iml_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') else 'false' }}
    </in-capmkt:IFurtherConfirmThatAllTheBranchesWhereIMLFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments>
    {% endif %}

        {% if data.get('i_further_confirm_that_all_the_branches_where_sor_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') is not none %}
    <in-capmkt:IFurtherConfirmThatAllTheBranchesWhereSORFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments contextRef="DCYMain">
        {{ 'true' if data.get('i_further_confirm_that_all_the_branches_where_sor_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') else 'false' }}
    </in-capmkt:IFurtherConfirmThatAllTheBranchesWhereSORFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments>
    {% endif %}

        {% if data.get('i_further_confirm_that_all_the_branches_where_stwt_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') is not none %}
    <in-capmkt:IFurtherConfirmThatAllTheBranchesWhereSTWTFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments contextRef="DCYMain">
        {{ 'true' if data.get('i_further_confirm_that_all_the_branches_where_stwt_facility_is_provided_have_been_audited_and_consolidated_report_has_been_submitted_for_all_segments') else 'false' }}
    </in-capmkt:IFurtherConfirmThatAllTheBranchesWhereSTWTFacilityIsProvidedHaveBeenAuditedAndConsolidatedReportHasBeenSubmittedForAllSegments>
    {% endif %}

        {% if data.get('iml_facility') is not none %}
    <in-capmkt:IMLFacility contextRef="DCYMain">
        {{ 'true' if data.get('iml_facility') else 'false' }}
    </in-capmkt:IMLFacility>
    {% endif %}

        {% if data.get('i_or_we_have_conducted_the_internal_audit_report_for_half_year_ended_as_per_the_exchange_notice_and_guidelines_please_find_enclosed_herewith_the_audit_report_and_audit_certificate_for_your_consideration_and_necessary_action') is not none %}
    <in-capmkt:IOrWeHaveConductedTheInternalAuditReportForHalfYearEndedAsPerTheExchangeNoticeAndGuidelinesPleaseFindEnclosedHerewithTheAuditReportAndAuditCertificateForYourConsiderationAndNecessaryAction contextRef="DCYMain">
        {{ 'true' if data.get('i_or_we_have_conducted_the_internal_audit_report_for_half_year_ended_as_per_the_exchange_notice_and_guidelines_please_find_enclosed_herewith_the_audit_report_and_audit_certificate_for_your_consideration_and_necessary_action') else 'false' }}
    </in-capmkt:IOrWeHaveConductedTheInternalAuditReportForHalfYearEndedAsPerTheExchangeNoticeAndGuidelinesPleaseFindEnclosedHerewithTheAuditReportAndAuditCertificateForYourConsiderationAndNecessaryAction>
    {% endif %}

        {% if data.get('isin') is not none %}
    <in-capmkt:ISIN contextRef="ICYMain">
        {{ data.get('isin', '') }}
    </in-capmkt:ISIN>
    {% endif %}

        {% if data.get('isin_of_borrowing_or_debt') is not none %}
    <in-capmkt:ISINOfBorrowingOrDebt contextRef="ICYMain">
        {{ data.get('isin_of_borrowing_or_debt', '') }}
    </in-capmkt:ISINOfBorrowingOrDebt>
    {% endif %}

        {% if data.get('impact_analysis') is not none %}
    <in-capmkt:ImpactAnalysis contextRef="DCYMain">
        {{ data.get('impact_analysis', '') }}
    </in-capmkt:ImpactAnalysis>
    {% endif %}

        {% if data.get('income_tax_net_of_refund_and_tds_and_other_taxes_paid_as_applicable_to_the_extent_not_already_considered_including_provision_for_tax') is not none %}
    <in-capmkt:IncomeTaxNetOfRefundAndTDSAndOtherTaxesPaidAsApplicableToTheExtentNotAlreadyConsideredIncludingProvisionForTax contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('income_tax_net_of_refund_and_tds_and_other_taxes_paid_as_applicable_to_the_extent_not_already_considered_including_provision_for_tax', '') }}
    </in-capmkt:IncomeTaxNetOfRefundAndTDSAndOtherTaxesPaidAsApplicableToTheExtentNotAlreadyConsideredIncludingProvisionForTax>
    {% endif %}

        {% if data.get('initiative_undertaken') is not none %}
    <in-capmkt:InitiativeUndertaken contextRef="DCYMain">
        {{ data.get('initiative_undertaken', '') }}
    </in-capmkt:InitiativeUndertaken>
    {% endif %}

        {% if data.get('instrumentsentirelyequityinnature') is not none %}
    <in-capmkt:Instrumentsentirelyequityinnature contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('instrumentsentirelyequityinnature', '') }}
    </in-capmkt:Instrumentsentirelyequityinnature>
    {% endif %}

        {% if data.get('intellectual_property_based_on_traditional_knowledge') is not none %}
    <in-capmkt:IntellectualPropertyBasedOnTraditionalKnowledge contextRef="DCYMain">
        {{ data.get('intellectual_property_based_on_traditional_knowledge', '') }}
    </in-capmkt:IntellectualPropertyBasedOnTraditionalKnowledge>
    {% endif %}

        {% if data.get('interest_accruedanddue') is not none %}
    <in-capmkt:InterestAccruedanddue contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('interest_accruedanddue', '') }}
    </in-capmkt:InterestAccruedanddue>
    {% endif %}

        {% if data.get('interest_accruedbutnotdue') is not none %}
    <in-capmkt:InterestAccruedbutnotdue contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('interest_accruedbutnotdue', '') }}
    </in-capmkt:InterestAccruedbutnotdue>
    {% endif %}

        {% if data.get('interest_or_redemption') is not none %}
    <in-capmkt:InterestOrRedemption contextRef="DCYMain">
        {{ data.get('interest_or_redemption', '') }}
    </in-capmkt:InterestOrRedemption>
    {% endif %}

        {% if data.get('interest_paid_on_external_debt') is not none %}
    <in-capmkt:InterestPaidOnExternalDebt contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('interest_paid_on_external_debt', '') }}
    </in-capmkt:InterestPaidOnExternalDebt>
    {% endif %}

        {% if data.get('issue_price_per_unit') is not none %}
    <in-capmkt:IssuePricePerUnit contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('issue_price_per_unit', '') }}
    </in-capmkt:IssuePricePerUnit>
    {% endif %}

        {% if data.get('issue_size') is not none %}
    <in-capmkt:IssueSize contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('issue_size', '') }}
    </in-capmkt:IssueSize>
    {% endif %}

        {% if data.get('it_is_planned_to_be_done_in_the_next_financial_year') is not none %}
    <in-capmkt:ItIsPlannedToBeDoneInTheNextFinancialYear contextRef="DCYMain">
        {{ 'true' if data.get('it_is_planned_to_be_done_in_the_next_financial_year') else 'false' }}
    </in-capmkt:ItIsPlannedToBeDoneInTheNextFinancialYear>
    {% endif %}

        {% if data.get('legal_and_professional_fees') is not none %}
    <in-capmkt:LegalAndProfessionalFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('legal_and_professional_fees', '') }}
    </in-capmkt:LegalAndProfessionalFees>
    {% endif %}

        {% if data.get('lending_to_sp_vs_as_may_be_deemed_necessary_by_the_manager') is not none %}
    <in-capmkt:LendingToSPVsAsMayBeDeemedNecessaryByTheManager contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('lending_to_sp_vs_as_may_be_deemed_necessary_by_the_manager', '') }}
    </in-capmkt:LendingToSPVsAsMayBeDeemedNecessaryByTheManager>
    {% endif %}

        {% if data.get('liabilities') is not none %}
    <in-capmkt:Liabilities contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('liabilities', '') }}
    </in-capmkt:Liabilities>
    {% endif %}

        {% if data.get('listing_fees') is not none %}
    <in-capmkt:ListingFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('listing_fees', '') }}
    </in-capmkt:ListingFees>
    {% endif %}

        {% if data.get('loansfrom_reitinvi_tsoranyotherinter_spv_borrowings') is not none %}
    <in-capmkt:LoansfromREITINVITsoranyotherinterSPVBorrowings contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('loansfrom_reitinvi_tsoranyotherinter_spv_borrowings', '') }}
    </in-capmkt:LoansfromREITINVITsoranyotherinterSPVBorrowings>
    {% endif %}

        {% if data.get('long_term_borrowings') is not none %}
    <in-capmkt:LongTermBorrowings contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('long_term_borrowings', '') }}
    </in-capmkt:LongTermBorrowings>
    {% endif %}

        {% if data.get('msei_symbol') is not none %}
    <in-capmkt:MSEISymbol contextRef="ICYMain">
        {{ data.get('msei_symbol', '') }}
    </in-capmkt:MSEISymbol>
    {% endif %}

        {% if data.get('mode_of_audit') is not none %}
    <in-capmkt:ModeOfAudit contextRef="DCYMain">
        {{ data.get('mode_of_audit', '') }}
    </in-capmkt:ModeOfAudit>
    {% endif %}

        {% if data.get('nse_symbol') is not none %}
    <in-capmkt:NSESymbol contextRef="ICYMain">
        {{ data.get('nse_symbol', '') }}
    </in-capmkt:NSESymbol>
    {% endif %}

        {% if data.get('name_and_brief_details_of_project') is not none %}
    <in-capmkt:NameAndBriefDetailsOfProject contextRef="DCYMain">
        {{ data.get('name_and_brief_details_of_project', '') }}
    </in-capmkt:NameAndBriefDetailsOfProject>
    {% endif %}

        {% if data.get('name_and_brief_details_of_project_sia') is not none %}
    <in-capmkt:NameAndBriefDetailsOfProjectSIA contextRef="DCYMain">
        {{ data.get('name_and_brief_details_of_project_sia', '') }}
    </in-capmkt:NameAndBriefDetailsOfProjectSIA>
    {% endif %}

        {% if data.get('name_of_audit_firm') is not none %}
    <in-capmkt:NameOfAuditFirm contextRef="ICYMain">
        {{ data.get('name_of_audit_firm', '') }}
    </in-capmkt:NameOfAuditFirm>
    {% endif %}

        {% if data.get('name_of_auditor') is not none %}
    <in-capmkt:NameOfAuditor contextRef="ICYMain">
        {{ data.get('name_of_auditor', '') }}
    </in-capmkt:NameOfAuditor>
    {% endif %}

        {% if data.get('name_of_authority') is not none %}
    <in-capmkt:NameOfAuthority contextRef="DCYMain">
        {{ data.get('name_of_authority', '') }}
    </in-capmkt:NameOfAuthority>
    {% endif %}

        {% if data.get('name_of_authority_for_intellectual_property_related_disputes') is not none %}
    <in-capmkt:NameOfAuthorityForIntellectualPropertyRelatedDisputes contextRef="DCYMain">
        {{ data.get('name_of_authority_for_intellectual_property_related_disputes', '') }}
    </in-capmkt:NameOfAuthorityForIntellectualPropertyRelatedDisputes>
    {% endif %}

        {% if data.get('name_of_client') is not none %}
    <in-capmkt:NameOfClient contextRef="DCYMain">
        {{ data.get('name_of_client', '') }}
    </in-capmkt:NameOfClient>
    {% endif %}

        {% if data.get('name_of_credit_rating_agency') is not none %}
    <in-capmkt:NameOfCreditRatingAgency contextRef="ICYMain">
        {{ data.get('name_of_credit_rating_agency', '') }}
    </in-capmkt:NameOfCreditRatingAgency>
    {% endif %}

        {% if data.get('name_of_invit_or_hold_co_or_sp_vs') is not none %}
    <in-capmkt:NameOfINVITOrHoldCoOrSPVs contextRef="ICYMain">
        {{ data.get('name_of_invit_or_hold_co_or_sp_vs', '') }}
    </in-capmkt:NameOfINVITOrHoldCoOrSPVs>
    {% endif %}

        {% if data.get('name_of_other_shareholder') is not none %}
    <in-capmkt:NameOfOtherShareholder contextRef="ICYMain">
        {{ data.get('name_of_other_shareholder', '') }}
    </in-capmkt:NameOfOtherShareholder>
    {% endif %}

        {% if data.get('name_of_project_for_which_rehabilitation_and_resettlement_is_on_going') is not none %}
    <in-capmkt:NameOfProjectForWhichRehabilitationAndResettlementIsOnGoing contextRef="DCYMain">
        {{ data.get('name_of_project_for_which_rehabilitation_and_resettlement_is_on_going', '') }}
    </in-capmkt:NameOfProjectForWhichRehabilitationAndResettlementIsOnGoing>
    {% endif %}

        {% if data.get('name_of_signatory') is not none %}
    <in-capmkt:NameOfSignatory contextRef="ICYMain">
        {{ data.get('name_of_signatory', '') }}
    </in-capmkt:NameOfSignatory>
    {% endif %}

        {% if data.get('name_of_the_agency_if_the_entity_carried_out_independent_assessment_evaluation_of_the_working_of_its_policies_by_an_external_agency_explanatory_text_block') is not none %}
    <in-capmkt:NameOfTheAgencyIfTheEntityCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgencyExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('name_of_the_agency_if_the_entity_carried_out_independent_assessment_evaluation_of_the_working_of_its_policies_by_an_external_agency_explanatory_text_block', '') }}
    </in-capmkt:NameOfTheAgencyIfTheEntityCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgencyExplanatoryTextBlock>
    {% endif %}

        {% if data.get('name_of_the_area') is not none %}
    <in-capmkt:NameOfTheArea contextRef="DCYMain">
        {{ data.get('name_of_the_area', '') }}
    </in-capmkt:NameOfTheArea>
    {% endif %}

        {% if data.get('name_of_the_external_agency') is not none %}
    <in-capmkt:NameOfTheExternalAgency contextRef="DCYMain">
        {{ data.get('name_of_the_external_agency', '') }}
    </in-capmkt:NameOfTheExternalAgency>
    {% endif %}

        {% if data.get('name_of_the_lender_of_loan_or_ec_bs') is not none %}
    <in-capmkt:NameOfTheLenderOfLoanOrECBs contextRef="ICYMain">
        {{ data.get('name_of_the_lender_of_loan_or_ec_bs', '') }}
    </in-capmkt:NameOfTheLenderOfLoanOrECBs>
    {% endif %}

        {% if data.get('name_of_the_lender_of_preference_share') is not none %}
    <in-capmkt:NameOfTheLenderOfPreferenceShare contextRef="ICYMain">
        {{ data.get('name_of_the_lender_of_preference_share', '') }}
    </in-capmkt:NameOfTheLenderOfPreferenceShare>
    {% endif %}

        {% if data.get('name_of_the_parties_from_whom_the_asset_was_acquired') is not none %}
    <in-capmkt:NameOfThePartiesFromWhomTheAssetWasAcquired contextRef="ICYMain">
        {{ data.get('name_of_the_parties_from_whom_the_asset_was_acquired', '') }}
    </in-capmkt:NameOfThePartiesFromWhomTheAssetWasAcquired>
    {% endif %}

        {% if data.get('name_of_the_parties_to_whom_the_asset_was_disposed_off') is not none %}
    <in-capmkt:NameOfThePartiesToWhomTheAssetWasDisposedOff contextRef="ICYMain">
        {{ data.get('name_of_the_parties_to_whom_the_asset_was_disposed_off', '') }}
    </in-capmkt:NameOfThePartiesToWhomTheAssetWasDisposedOff>
    {% endif %}

        {% if data.get('name_or_details_of_the_law_or_regulation_or_guidelines_which_was_not_complied_with') is not none %}
    <in-capmkt:NameOrDetailsOfTheLawOrRegulationOrGuidelinesWhichWasNotCompliedWith contextRef="DCYMain">
        {{ data.get('name_or_details_of_the_law_or_regulation_or_guidelines_which_was_not_complied_with', '') }}
    </in-capmkt:NameOrDetailsOfTheLawOrRegulationOrGuidelinesWhichWasNotCompliedWith>
    {% endif %}

        {% if data.get('nameof_holdcos') is not none %}
    <in-capmkt:NameofHoldcos contextRef="ICYMain">
        {{ data.get('nameof_holdcos', '') }}
    </in-capmkt:NameofHoldcos>
    {% endif %}

        {% if data.get('nameof_holdcos_or_sv_ps') is not none %}
    <in-capmkt:NameofHoldcosOrSVPs contextRef="ICYMain">
        {{ data.get('nameof_holdcos_or_sv_ps', '') }}
    </in-capmkt:NameofHoldcosOrSVPs>
    {% endif %}

        {% if data.get('nameof_sv_ps') is not none %}
    <in-capmkt:NameofSVPs contextRef="ICYMain">
        {{ data.get('nameof_sv_ps', '') }}
    </in-capmkt:NameofSVPs>
    {% endif %}

        {% if data.get('nature_of_debt_security_issued') is not none %}
    <in-capmkt:NatureOfDebtSecurityIssued contextRef="ICYMain">
        {{ data.get('nature_of_debt_security_issued', '') }}
    </in-capmkt:NatureOfDebtSecurityIssued>
    {% endif %}

        {% if data.get('nature_of_issue') is not none %}
    <in-capmkt:NatureOfIssue contextRef="DCYMain">
        {{ data.get('nature_of_issue', '') }}
    </in-capmkt:NatureOfIssue>
    {% endif %}

        {% if data.get('nature_of_operations') is not none %}
    <in-capmkt:NatureOfOperations contextRef="DCYMain">
        {{ data.get('nature_of_operations', '') }}
    </in-capmkt:NatureOfOperations>
    {% endif %}

        {% if data.get('nature_of_report_standalone_consolidated') is not none %}
    <in-capmkt:NatureOfReportStandaloneConsolidated contextRef="DCYMain">
        {{ data.get('nature_of_report_standalone_consolidated', '') }}
    </in-capmkt:NatureOfReportStandaloneConsolidated>
    {% endif %}

        {% if data.get('nature_of_the_asset_acquired') is not none %}
    <in-capmkt:NatureOfTheAssetAcquired contextRef="DCYMain">
        {{ data.get('nature_of_the_asset_acquired', '') }}
    </in-capmkt:NatureOfTheAssetAcquired>
    {% endif %}

        {% if data.get('nature_of_the_asset_disposed_off') is not none %}
    <in-capmkt:NatureOfTheAssetDisposedOff contextRef="DCYMain">
        {{ data.get('nature_of_the_asset_disposed_off', '') }}
    </in-capmkt:NatureOfTheAssetDisposedOff>
    {% endif %}

        {% if data.get('net_assets') is not none %}
    <in-capmkt:NetAssets contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('net_assets', '') }}
    </in-capmkt:NetAssets>
    {% endif %}

        {% if data.get('net_debt') is not none %}
    <in-capmkt:NetDebt contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('net_debt', '') }}
    </in-capmkt:NetDebt>
    {% endif %}

        {% if data.get('net_distributable_cash_flows') is not none %}
    <in-capmkt:NetDistributableCashFlows contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('net_distributable_cash_flows', '') }}
    </in-capmkt:NetDistributableCashFlows>
    {% endif %}

        {% if data.get('net_lending_to_sp_vs_not_included_above_as_may_be_deemed_necessary_by_the_manager') is not none %}
    <in-capmkt:NetLendingToSPVsNotIncludedAboveAsMayBeDeemedNecessaryByTheManager contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('net_lending_to_sp_vs_not_included_above_as_may_be_deemed_necessary_by_the_manager', '') }}
    </in-capmkt:NetLendingToSPVsNotIncludedAboveAsMayBeDeemedNecessaryByTheManager>
    {% endif %}

        {% if data.get('net_profit_after_tax') is not none %}
    <in-capmkt:NetProfitAfterTax contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('net_profit_after_tax', '') }}
    </in-capmkt:NetProfitAfterTax>
    {% endif %}

        {% if data.get('next_due_date_of_payment_of_interest_or_dividend') is not none %}
    <in-capmkt:NextDueDateOfPaymentOfInterestOrDividend contextRef="DCYMain">
        {{ data.get('next_due_date_of_payment_of_interest_or_dividend', '') }}
    </in-capmkt:NextDueDateOfPaymentOfInterestOrDividend>
    {% endif %}

        {% if data.get('notes_general_disclosure_explanatory_text_block') is not none %}
    <in-capmkt:NotesGeneralDisclosureExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_general_disclosure_explanatory_text_block', '') }}
    </in-capmkt:NotesGeneralDisclosureExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_management_and_process_disclosures_explanatory_text_block') is not none %}
    <in-capmkt:NotesManagementAndProcessDisclosuresExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_management_and_process_disclosures_explanatory_text_block', '') }}
    </in-capmkt:NotesManagementAndProcessDisclosuresExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_principle1_explanatory_text_block') is not none %}
    <in-capmkt:NotesPrinciple1ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_principle1_explanatory_text_block', '') }}
    </in-capmkt:NotesPrinciple1ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_principle2_explanatory_text_block') is not none %}
    <in-capmkt:NotesPrinciple2ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_principle2_explanatory_text_block', '') }}
    </in-capmkt:NotesPrinciple2ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_principle3_explanatory_text_block') is not none %}
    <in-capmkt:NotesPrinciple3ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_principle3_explanatory_text_block', '') }}
    </in-capmkt:NotesPrinciple3ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_principle4_explanatory_text_block') is not none %}
    <in-capmkt:NotesPrinciple4ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_principle4_explanatory_text_block', '') }}
    </in-capmkt:NotesPrinciple4ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_principle5_explanatory_text_block') is not none %}
    <in-capmkt:NotesPrinciple5ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_principle5_explanatory_text_block', '') }}
    </in-capmkt:NotesPrinciple5ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_principle6_explanatory_text_block') is not none %}
    <in-capmkt:NotesPrinciple6ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_principle6_explanatory_text_block', '') }}
    </in-capmkt:NotesPrinciple6ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_principle7_explanatory_text_block') is not none %}
    <in-capmkt:NotesPrinciple7ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_principle7_explanatory_text_block', '') }}
    </in-capmkt:NotesPrinciple7ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_principle8_explanatory_text_block') is not none %}
    <in-capmkt:NotesPrinciple8ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_principle8_explanatory_text_block', '') }}
    </in-capmkt:NotesPrinciple8ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('notes_principle9_explanatory_text_block') is not none %}
    <in-capmkt:NotesPrinciple9ExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('notes_principle9_explanatory_text_block', '') }}
    </in-capmkt:NotesPrinciple9ExplanatoryTextBlock>
    {% endif %}

        {% if data.get('observation_audited_by') is not none %}
    <in-capmkt:ObservationAuditedBy contextRef="DCYMain">
        {{ data.get('observation_audited_by', '') }}
    </in-capmkt:ObservationAuditedBy>
    {% endif %}

        {% if data.get('other_adjustments_including_but_not_limited_to_net_changes_in_security_deposits_or_working_capital_or_non_cash_item_etc_as_may_be_deemed_necessary_by_the_manager') is not none %}
    <in-capmkt:OtherAdjustmentsIncludingButNotLimitedToNetChangesInSecurityDepositsOrWorkingCapitalOrNonCashItemEtcAsMayBeDeemedNecessaryByTheManager contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_adjustments_including_but_not_limited_to_net_changes_in_security_deposits_or_working_capital_or_non_cash_item_etc_as_may_be_deemed_necessary_by_the_manager', '') }}
    </in-capmkt:OtherAdjustmentsIncludingButNotLimitedToNetChangesInSecurityDepositsOrWorkingCapitalOrNonCashItemEtcAsMayBeDeemedNecessaryByTheManager>
    {% endif %}

        {% if data.get('other_equity') is not none %}
    <in-capmkt:OtherEquity contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_equity', '') }}
    </in-capmkt:OtherEquity>
    {% endif %}

        {% if data.get('other_expense_accruing_or_paid_at_the_trust_level_and_not_captured_herein') is not none %}
    <in-capmkt:OtherExpenseAccruingOrPaidAtTheTrustLevelAndNotCapturedHerein contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_expense_accruing_or_paid_at_the_trust_level_and_not_captured_herein', '') }}
    </in-capmkt:OtherExpenseAccruingOrPaidAtTheTrustLevelAndNotCapturedHerein>
    {% endif %}

        {% if data.get('other_expenses') is not none %}
    <in-capmkt:OtherExpenses contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_expenses', '') }}
    </in-capmkt:OtherExpenses>
    {% endif %}

        {% if data.get('other_from_fund_raised_through_external_lenders_or_bankers') is not none %}
    <in-capmkt:OtherFromFundRaisedThroughExternalLendersOrBankers contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_from_fund_raised_through_external_lenders_or_bankers', '') }}
    </in-capmkt:OtherFromFundRaisedThroughExternalLendersOrBankers>
    {% endif %}

        {% if data.get('other_income_received_or_receivable_by_of_the_trust_and_not_captured_herein') is not none %}
    <in-capmkt:OtherIncomeReceivedOrReceivableByOfTheTrustAndNotCapturedHerein contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_income_received_or_receivable_by_of_the_trust_and_not_captured_herein', '') }}
    </in-capmkt:OtherIncomeReceivedOrReceivableByOfTheTrustAndNotCapturedHerein>
    {% endif %}

        {% if data.get('other_item_not_included_above') is not none %}
    <in-capmkt:OtherItemNotIncludedAbove contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_item_not_included_above', '') }}
    </in-capmkt:OtherItemNotIncludedAbove>
    {% endif %}

        {% if data.get('other_item_of_non_cash_expense_or_non_cash_income_net_of_actual_cash_flows_for_these_items') is not none %}
    <in-capmkt:OtherItemOfNonCashExpenseOrNonCashIncomeNetOfActualCashFlowsForTheseItems contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_item_of_non_cash_expense_or_non_cash_income_net_of_actual_cash_flows_for_these_items', '') }}
    </in-capmkt:OtherItemOfNonCashExpenseOrNonCashIncomeNetOfActualCashFlowsForTheseItems>
    {% endif %}

        {% if data.get('other_maybe_deemed_necessary_by_the_manager') is not none %}
    <in-capmkt:OtherMaybeDeemedNecessaryByTheManager contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('other_maybe_deemed_necessary_by_the_manager', '') }}
    </in-capmkt:OtherMaybeDeemedNecessaryByTheManager>
    {% endif %}

        {% if data.get('outcome_of_the_initiative') is not none %}
    <in-capmkt:OutcomeOfTheInitiative contextRef="DCYMain">
        {{ data.get('outcome_of_the_initiative', '') }}
    </in-capmkt:OutcomeOfTheInitiative>
    {% endif %}

        {% if data.get('outlook') is not none %}
    <in-capmkt:Outlook contextRef="ICYMain">
        {{ data.get('outlook', '') }}
    </in-capmkt:Outlook>
    {% endif %}

        {% if data.get('outstanding_funds_raised_through_debt_consolidated') is not none %}
    <in-capmkt:OutstandingFundsRaisedThroughDebtConsolidated contextRef="ICYMain" unitRef="pure" decimals="2">
        {{ data.get('outstanding_funds_raised_through_debt_consolidated', '') }}
    </in-capmkt:OutstandingFundsRaisedThroughDebtConsolidated>
    {% endif %}

        {% if data.get('owned_or_acquired') is not none %}
    <in-capmkt:OwnedOrAcquired contextRef="DCYMain">
        {{ 'true' if data.get('owned_or_acquired') else 'false' }}
    </in-capmkt:OwnedOrAcquired>
    {% endif %}

        {% if data.get('place_of_signatory') is not none %}
    <in-capmkt:PlaceOfSignatory contextRef="ICYMain">
        {{ data.get('place_of_signatory', '') }}
    </in-capmkt:PlaceOfSignatory>
    {% endif %}

        {% if data.get('preliminary_audit_date') is not none %}
    <in-capmkt:PreliminaryAuditDate contextRef="DCYMain">
        {{ data.get('preliminary_audit_date', '') }}
    </in-capmkt:PreliminaryAuditDate>
    {% endif %}

        {% if data.get('preliminary_audit_period') is not none %}
    <in-capmkt:PreliminaryAuditPeriod contextRef="DCYMain">
        {{ data.get('preliminary_audit_period', '') }}
    </in-capmkt:PreliminaryAuditPeriod>
    {% endif %}

        {% if data.get('preliminary_corrective_action') is not none %}
    <in-capmkt:PreliminaryCorrectiveAction contextRef="DCYMain">
        {{ data.get('preliminary_corrective_action', '') }}
    </in-capmkt:PreliminaryCorrectiveAction>
    {% endif %}

        {% if data.get('preliminary_status') is not none %}
    <in-capmkt:PreliminaryStatus contextRef="DCYMain">
        {{ data.get('preliminary_status', '') }}
    </in-capmkt:PreliminaryStatus>
    {% endif %}

        {% if data.get('previous_due_date_of_payment_of_interest_or_dividend') is not none %}
    <in-capmkt:PreviousDueDateOfPaymentOfInterestOrDividend contextRef="DCYMain">
        {{ data.get('previous_due_date_of_payment_of_interest_or_dividend', '') }}
    </in-capmkt:PreviousDueDateOfPaymentOfInterestOrDividend>
    {% endif %}

        {% if data.get('proceeds_from_buy_backs_capital_reduction_net_of_applicable_taxes') is not none %}
    <in-capmkt:ProceedsFromBuyBacksCapitalReductionNetOfApplicableTaxes contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('proceeds_from_buy_backs_capital_reduction_net_of_applicable_taxes', '') }}
    </in-capmkt:ProceedsFromBuyBacksCapitalReductionNetOfApplicableTaxes>
    {% endif %}

        {% if data.get('proceeds_from_fund_raised_through_external_lenders_or_bankers_by_issue_of_units_or_ncd_or_preference_share_capital_at_reitinvit_level_adjusted') is not none %}
    <in-capmkt:ProceedsFromFundRaisedThroughExternalLendersOrBankersByIssueOfUnitsOrNCDOrPreferenceShareCapitalAtREITINVITLevelAdjusted contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('proceeds_from_fund_raised_through_external_lenders_or_bankers_by_issue_of_units_or_ncd_or_preference_share_capital_at_reitinvit_level_adjusted', '') }}
    </in-capmkt:ProceedsFromFundRaisedThroughExternalLendersOrBankersByIssueOfUnitsOrNCDOrPreferenceShareCapitalAtREITINVITLevelAdjusted>
    {% endif %}

        {% if data.get('proceeds_reinvested_or_planned_to_be_reinvested_as_per_regulation1816_d_of_the_reitinvit_regulations') is not none %}
    <in-capmkt:ProceedsReinvestedOrPlannedToBeReinvestedAsPerRegulation1816DOfTheREITINVITRegulations contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('proceeds_reinvested_or_planned_to_be_reinvested_as_per_regulation1816_d_of_the_reitinvit_regulations', '') }}
    </in-capmkt:ProceedsReinvestedOrPlannedToBeReinvestedAsPerRegulation1816DOfTheREITINVITRegulations>
    {% endif %}

        {% if data.get('proceeds_reinvested_or_planned_to_be_reinvested_as_per_regulation1816_d_of_the_reit_regulations_or_regulation187_a_of_invit_regulations') is not none %}
    <in-capmkt:ProceedsReinvestedOrPlannedToBeReinvestedAsPerRegulation1816DOfTheREITRegulationsOrRegulation187AOfINVITRegulations contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('proceeds_reinvested_or_planned_to_be_reinvested_as_per_regulation1816_d_of_the_reit_regulations_or_regulation187_a_of_invit_regulations', '') }}
    </in-capmkt:ProceedsReinvestedOrPlannedToBeReinvestedAsPerRegulation1816DOfTheREITRegulationsOrRegulation187AOfINVITRegulations>
    {% endif %}

        {% if data.get('project_manager_fees') is not none %}
    <in-capmkt:ProjectManagerFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('project_manager_fees', '') }}
    </in-capmkt:ProjectManagerFees>
    {% endif %}

        {% if data.get('provide_details_of_the_non_compliance') is not none %}
    <in-capmkt:ProvideDetailsOfTheNonCompliance contextRef="DCYMain">
        {{ data.get('provide_details_of_the_non_compliance', '') }}
    </in-capmkt:ProvideDetailsOfTheNonCompliance>
    {% endif %}

        {% if data.get('quantity_of_outstanding_redeemable_preference_shares') is not none %}
    <in-capmkt:QuantityOfOutstandingRedeemablePreferenceShares contextRef="DCYMain">
        {{ data.get('quantity_of_outstanding_redeemable_preference_shares', '') }}
    </in-capmkt:QuantityOfOutstandingRedeemablePreferenceShares>
    {% endif %}

        {% if data.get('quantity_redeemed') is not none %}
    <in-capmkt:QuantityRedeemed contextRef="ICYMain">
        {{ data.get('quantity_redeemed', '') }}
    </in-capmkt:QuantityRedeemed>
    {% endif %}

        {% if data.get('reitinvit_management_fees') is not none %}
    <in-capmkt:REITINVITManagementFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('reitinvit_management_fees', '') }}
    </in-capmkt:REITINVITManagementFees>
    {% endif %}

        {% if data.get('raised_during_the_period_funds_raised_through_debt_consolidated') is not none %}
    <in-capmkt:RaisedDuringThePeriodFundsRaisedThroughDebtConsolidated contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('raised_during_the_period_funds_raised_through_debt_consolidated', '') }}
    </in-capmkt:RaisedDuringThePeriodFundsRaisedThroughDebtConsolidated>
    {% endif %}

        {% if data.get('rating') is not none %}
    <in-capmkt:Rating contextRef="DCYMain">
        {{ data.get('rating', '') }}
    </in-capmkt:Rating>
    {% endif %}

        {% if data.get('rating_action') is not none %}
    <in-capmkt:RatingAction contextRef="ICYMain">
        {{ data.get('rating_action', '') }}
    </in-capmkt:RatingAction>
    {% endif %}

        {% if data.get('rating_fees') is not none %}
    <in-capmkt:RatingFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('rating_fees', '') }}
    </in-capmkt:RatingFees>
    {% endif %}

        {% if data.get('reason_for_non_payment_or_delay_in_payment') is not none %}
    <in-capmkt:ReasonForNonPaymentOrDelayInPayment contextRef="ICYMain">
        {{ data.get('reason_for_non_payment_or_delay_in_payment', '') }}
    </in-capmkt:ReasonForNonPaymentOrDelayInPayment>
    {% endif %}

        {% if data.get('reason_for_redemption') is not none %}
    <in-capmkt:ReasonForRedemption contextRef="ICYMain">
        {{ data.get('reason_for_redemption', '') }}
    </in-capmkt:ReasonForRedemption>
    {% endif %}

        {% if data.get('record_date') is not none %}
    <in-capmkt:RecordDate contextRef="DCYMain">
        {{ data.get('record_date', '') }}
    </in-capmkt:RecordDate>
    {% endif %}

        {% if data.get('record_date_of_interest_payment') is not none %}
    <in-capmkt:RecordDateOfInterestPayment contextRef="DCYMain">
        {{ data.get('record_date_of_interest_payment', '') }}
    </in-capmkt:RecordDateOfInterestPayment>
    {% endif %}

        {% if data.get('redemption_date_due_to_call_option') is not none %}
    <in-capmkt:RedemptionDateDueToCALLOption contextRef="DCYMain">
        {{ data.get('redemption_date_due_to_call_option', '') }}
    </in-capmkt:RedemptionDateDueToCALLOption>
    {% endif %}

        {% if data.get('redemption_date_due_to_put_option') is not none %}
    <in-capmkt:RedemptionDateDueToPUTOption contextRef="DCYMain">
        {{ data.get('redemption_date_due_to_put_option', '') }}
    </in-capmkt:RedemptionDateDueToPUTOption>
    {% endif %}

        {% if data.get('redemption_proceeds_from_preference_shares_or_any_other_similar_instrument') is not none %}
    <in-capmkt:RedemptionProceedsFromPreferenceSharesOrAnyOtherSimilarInstrument contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('redemption_proceeds_from_preference_shares_or_any_other_similar_instrument', '') }}
    </in-capmkt:RedemptionProceedsFromPreferenceSharesOrAnyOtherSimilarInstrument>
    {% endif %}

        {% if data.get('reimbursement_of_expenses_to_im') is not none %}
    <in-capmkt:ReimbursementOfExpensesToIM contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('reimbursement_of_expenses_to_im', '') }}
    </in-capmkt:ReimbursementOfExpensesToIM>
    {% endif %}

        {% if data.get('related_debts_settled_or_due_to_be_settled_from_sale_proceeds_from_fund_raised_through_external_lenders_or_bankers') is not none %}
    <in-capmkt:RelatedDebtsSettledOrDueToBeSettledFromSaleProceedsFromFundRaisedThroughExternalLendersOrBankers contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('related_debts_settled_or_due_to_be_settled_from_sale_proceeds_from_fund_raised_through_external_lenders_or_bankers', '') }}
    </in-capmkt:RelatedDebtsSettledOrDueToBeSettledFromSaleProceedsFromFundRaisedThroughExternalLendersOrBankers>
    {% endif %}

        {% if data.get('repaid_during_the_period_funds_raised_through_debt_consolidated') is not none %}
    <in-capmkt:RepaidDuringThePeriodFundsRaisedThroughDebtConsolidated contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('repaid_during_the_period_funds_raised_through_debt_consolidated', '') }}
    </in-capmkt:RepaidDuringThePeriodFundsRaisedThroughDebtConsolidated>
    {% endif %}

        {% if data.get('repayment_of_shareholder_debt_reitinvit_funding_net_of_additional_debt_extended_to_the_sp_vs') is not none %}
    <in-capmkt:RepaymentOfShareholderDebtREITINVITFundingNetOfAdditionalDebtExtendedToTheSPVs contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('repayment_of_shareholder_debt_reitinvit_funding_net_of_additional_debt_extended_to_the_sp_vs', '') }}
    </in-capmkt:RepaymentOfShareholderDebtREITINVITFundingNetOfAdditionalDebtExtendedToTheSPVs>
    {% endif %}

        {% if data.get('reporting_quarter') is not none %}
    <in-capmkt:ReportingQuarter contextRef="DCYMain">
        {{ data.get('reporting_quarter', '') }}
    </in-capmkt:ReportingQuarter>
    {% endif %}

        {% if data.get('reserve_and_surplus') is not none %}
    <in-capmkt:ReserveAndSurplus contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('reserve_and_surplus', '') }}
    </in-capmkt:ReserveAndSurplus>
    {% endif %}

        {% if data.get('revised_corrective_action') is not none %}
    <in-capmkt:RevisedCorrectiveAction contextRef="DCYMain">
        {{ data.get('revised_corrective_action', '') }}
    </in-capmkt:RevisedCorrectiveAction>
    {% endif %}

        {% if data.get('risk_rating_of_findings') is not none %}
    <in-capmkt:RiskRatingOfFindings contextRef="DCYMain">
        {{ data.get('risk_rating_of_findings', '') }}
    </in-capmkt:RiskRatingOfFindings>
    {% endif %}

        {% if data.get('root_cause_analysis') is not none %}
    <in-capmkt:RootCauseAnalysis contextRef="DCYMain">
        {{ data.get('root_cause_analysis', '') }}
    </in-capmkt:RootCauseAnalysis>
    {% endif %}

        {% if data.get('sar_audited_by') is not none %}
    <in-capmkt:SARAuditedBy contextRef="DCYMain">
        {{ data.get('sar_audited_by', '') }}
    </in-capmkt:SARAuditedBy>
    {% endif %}

        {% if data.get('sor_facility') is not none %}
    <in-capmkt:SORFacility contextRef="DCYMain">
        {{ 'true' if data.get('sor_facility') else 'false' }}
    </in-capmkt:SORFacility>
    {% endif %}

        {% if data.get('stwt_facility') is not none %}
    <in-capmkt:STWTFacility contextRef="DCYMain">
        {{ 'true' if data.get('stwt_facility') else 'false' }}
    </in-capmkt:STWTFacility>
    {% endif %}

        {% if data.get('scrip_code') is not none %}
    <in-capmkt:ScripCode contextRef="ICYMain">
        {{ data.get('scrip_code', '') }}
    </in-capmkt:ScripCode>
    {% endif %}

        {% if data.get('secondment_fees') is not none %}
    <in-capmkt:SecondmentFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('secondment_fees', '') }}
    </in-capmkt:SecondmentFees>
    {% endif %}

        {% if data.get('shareholders_funds') is not none %}
    <in-capmkt:ShareholdersFunds contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('shareholders_funds', '') }}
    </in-capmkt:ShareholdersFunds>
    {% endif %}

        {% if data.get('shorttermborrowings') is not none %}
    <in-capmkt:Shorttermborrowings contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('shorttermborrowings', '') }}
    </in-capmkt:Shorttermborrowings>
    {% endif %}

        {% if data.get('specify_other_rating_action') is not none %}
    <in-capmkt:SpecifyOtherRatingAction contextRef="ICYMain">
        {{ data.get('specify_other_rating_action', '') }}
    </in-capmkt:SpecifyOtherRatingAction>
    {% endif %}

        {% if data.get('start_time_of_board_meeting') is not none %}
    <in-capmkt:StartTimeOfBoardMeeting contextRef="DCYMain">
        {{ data.get('start_time_of_board_meeting', '') }}
    </in-capmkt:StartTimeOfBoardMeeting>
    {% endif %}

        {% if data.get('status_or_nature_of_finding') is not none %}
    <in-capmkt:StatusOrNatureOfFinding contextRef="DCYMain">
        {{ data.get('status_or_nature_of_finding', '') }}
    </in-capmkt:StatusOrNatureOfFinding>
    {% endif %}

        {% if data.get('suggested_corrective_action') is not none %}
    <in-capmkt:SuggestedCorrectiveAction contextRef="DCYMain">
        {{ data.get('suggested_corrective_action', '') }}
    </in-capmkt:SuggestedCorrectiveAction>
    {% endif %}

        {% if data.get('tenure_of_loan_or_ecb') is not none %}
    <in-capmkt:TenureOfLoanOrECB contextRef="ICYMain">
        {{ data.get('tenure_of_loan_or_ecb', '') }}
    </in-capmkt:TenureOfLoanOrECB>
    {% endif %}

        {% if data.get('tenure_of_nc_ds') is not none %}
    <in-capmkt:TenureOfNCDs contextRef="ICYMain">
        {{ data.get('tenure_of_nc_ds', '') }}
    </in-capmkt:TenureOfNCDs>
    {% endif %}

        {% if data.get('tenure_of_preference_share') is not none %}
    <in-capmkt:TenureOfPreferenceShare contextRef="ICYMain">
        {{ data.get('tenure_of_preference_share', '') }}
    </in-capmkt:TenureOfPreferenceShare>
    {% endif %}

        {% if data.get('the_entity_does_not_have_the_financial_or_human_and_technical_resources_available_for_the_task') is not none %}
    <in-capmkt:TheEntityDoesNotHaveTheFinancialOrHumanAndTechnicalResourcesAvailableForTheTask contextRef="DCYMain">
        {{ 'true' if data.get('the_entity_does_not_have_the_financial_or_human_and_technical_resources_available_for_the_task') else 'false' }}
    </in-capmkt:TheEntityDoesNotHaveTheFinancialOrHumanAndTechnicalResourcesAvailableForTheTask>
    {% endif %}

        {% if data.get('the_entity_is_not_at_a_stage_where_it_is_in_a_position_to_formulate_and_implement_the_policies_on_specified_principles') is not none %}
    <in-capmkt:TheEntityIsNotAtAStageWhereItIsInAPositionToFormulateAndImplementThePoliciesOnSpecifiedPrinciples contextRef="DCYMain">
        {{ 'true' if data.get('the_entity_is_not_at_a_stage_where_it_is_in_a_position_to_formulate_and_implement_the_policies_on_specified_principles') else 'false' }}
    </in-capmkt:TheEntityIsNotAtAStageWhereItIsInAPositionToFormulateAndImplementThePoliciesOnSpecifiedPrinciples>
    {% endif %}

        {% if data.get('the_extent_and_nature_of_security_created_and_maintained_with_respect_to_its_secured_listed_non_convertible_debt_securities_explanatory_text_block') is not none %}
    <in-capmkt:TheExtentAndNatureOfSecurityCreatedAndMaintainedWithRespectToItsSecuredListedNonConvertibleDebtSecuritiesExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('the_extent_and_nature_of_security_created_and_maintained_with_respect_to_its_secured_listed_non_convertible_debt_securities_explanatory_text_block', '') }}
    </in-capmkt:TheExtentAndNatureOfSecurityCreatedAndMaintainedWithRespectToItsSecuredListedNonConvertibleDebtSecuritiesExplanatoryTextBlock>
    {% endif %}

        {% if data.get('trademark_license_fees') is not none %}
    <in-capmkt:TrademarkLicenseFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('trademark_license_fees', '') }}
    </in-capmkt:TrademarkLicenseFees>
    {% endif %}

        {% if data.get('trustee_fees') is not none %}
    <in-capmkt:TrusteeFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('trustee_fees', '') }}
    </in-capmkt:TrusteeFees>
    {% endif %}

        {% if data.get('type_of_assurance_for_details_of_operations') is not none %}
    <in-capmkt:TypeOfAssuranceForDetailsOfOperations contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_details_of_operations', '') }}
    </in-capmkt:TypeOfAssuranceForDetailsOfOperations>
    {% endif %}

        {% if data.get('type_of_assurance_for_details_of_the_listed_entity') is not none %}
    <in-capmkt:TypeOfAssuranceForDetailsOfTheListedEntity contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_details_of_the_listed_entity', '') }}
    </in-capmkt:TypeOfAssuranceForDetailsOfTheListedEntity>
    {% endif %}

        {% if data.get('type_of_assurance_for_transparency_and_disclosures_compliances') is not none %}
    <in-capmkt:TypeOfAssuranceForTransparencyAndDisclosuresCompliances contextRef="DCYMain">
        {{ data.get('type_of_assurance_for_transparency_and_disclosures_compliances', '') }}
    </in-capmkt:TypeOfAssuranceForTransparencyAndDisclosuresCompliances>
    {% endif %}

        {% if data.get('type_of_nc_ds') is not none %}
    <in-capmkt:TypeOfNCDs contextRef="ICYMain">
        {{ data.get('type_of_nc_ds', '') }}
    </in-capmkt:TypeOfNCDs>
    {% endif %}

        {% if data.get('type_of_operations') is not none %}
    <in-capmkt:TypeOfOperations contextRef="ICYMain">
        {{ data.get('type_of_operations', '') }}
    </in-capmkt:TypeOfOperations>
    {% endif %}

        {% if data.get('type_of_partial_redemption') is not none %}
    <in-capmkt:TypeOfPartialRedemption contextRef="DCYMain">
        {{ data.get('type_of_partial_redemption', '') }}
    </in-capmkt:TypeOfPartialRedemption>
    {% endif %}

        {% if data.get('type_of_redemption') is not none %}
    <in-capmkt:TypeOfRedemption contextRef="DCYMain">
        {{ data.get('type_of_redemption', '') }}
    </in-capmkt:TypeOfRedemption>
    {% endif %}

        {% if data.get('type_of_redemption_based_on_quantity') is not none %}
    <in-capmkt:TypeOfRedemptionBasedOnQuantity contextRef="DCYMain">
        {{ data.get('type_of_redemption_based_on_quantity', '') }}
    </in-capmkt:TypeOfRedemptionBasedOnQuantity>
    {% endif %}

        {% if data.get('type_of_tor') is not none %}
    <in-capmkt:TypeOfTOR contextRef="DCYMain">
        {{ data.get('type_of_tor', '') }}
    </in-capmkt:TypeOfTOR>
    {% endif %}

        {% if data.get('type_of_trading') is not none %}
    <in-capmkt:TypeOfTrading contextRef="DCYMain">
        {{ data.get('type_of_trading', '') }}
    </in-capmkt:TypeOfTrading>
    {% endif %}

        {% if data.get('type_of_transaction_of_the_asset_acquired') is not none %}
    <in-capmkt:TypeOfTransactionOfTheAssetAcquired contextRef="DCYMain">
        {{ data.get('type_of_transaction_of_the_asset_acquired', '') }}
    </in-capmkt:TypeOfTransactionOfTheAssetAcquired>
    {% endif %}

        {% if data.get('type_of_transaction_of_the_asset_disposed_off') is not none %}
    <in-capmkt:TypeOfTransactionOfTheAssetDisposedOff contextRef="DCYMain">
        {{ data.get('type_of_transaction_of_the_asset_disposed_off', '') }}
    </in-capmkt:TypeOfTransactionOfTheAssetDisposedOff>
    {% endif %}

        {% if data.get('undertaking') is not none %}
    <in-capmkt:Undertaking contextRef="DCYMain">
        {{ 'true' if data.get('undertaking') else 'false' }}
    </in-capmkt:Undertaking>
    {% endif %}

        {% if data.get('unit_of_persistent_organic_pollutants') is not none %}
    <in-capmkt:UnitOfPersistentOrganicPollutants contextRef="DCYMain">
        {{ data.get('unit_of_persistent_organic_pollutants', '') }}
    </in-capmkt:UnitOfPersistentOrganicPollutants>
    {% endif %}

        {% if data.get('unit_of_volatile_organic_compounds') is not none %}
    <in-capmkt:UnitOfVolatileOrganicCompounds contextRef="DCYMain">
        {{ data.get('unit_of_volatile_organic_compounds', '') }}
    </in-capmkt:UnitOfVolatileOrganicCompounds>
    {% endif %}

        {% if data.get('units_of_issue_size') is not none %}
    <in-capmkt:UnitsOfIssueSize contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('units_of_issue_size', '') }}
    </in-capmkt:UnitsOfIssueSize>
    {% endif %}

        {% if data.get('valuation_of_the_asset_acquired') is not none %}
    <in-capmkt:ValuationOfTheAssetAcquired contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('valuation_of_the_asset_acquired', '') }}
    </in-capmkt:ValuationOfTheAssetAcquired>
    {% endif %}

        {% if data.get('valuation_of_the_asset_disposed') is not none %}
    <in-capmkt:ValuationOfTheAssetDisposed contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('valuation_of_the_asset_disposed', '') }}
    </in-capmkt:ValuationOfTheAssetDisposed>
    {% endif %}

        {% if data.get('verification_status') is not none %}
    <in-capmkt:VerificationStatus contextRef="ICYMain">
        {{ data.get('verification_status', '') }}
    </in-capmkt:VerificationStatus>
    {% endif %}

        {% if data.get('verification_status_of_debenture_trustee') is not none %}
    <in-capmkt:VerificationStatusOfDebentureTrustee contextRef="DCYMain">
        {{ 'true' if data.get('verification_status_of_debenture_trustee') else 'false' }}
    </in-capmkt:VerificationStatusOfDebentureTrustee>
    {% endif %}

        {% if data.get('verified_by') is not none %}
    <in-capmkt:VerifiedBy contextRef="DCYMain">
        {{ data.get('verified_by', '') }}
    </in-capmkt:VerifiedBy>
    {% endif %}

        {% if data.get('we_have_taken_management_explanations_wherever_the_information_available_on_the_underlying_documents_were_not_sufficient_to_arrive_at_a_decision_on_the_level_of_compliance') is not none %}
    <in-capmkt:WeHaveTakenManagementExplanationsWhereverTheInformationAvailableOnTheUnderlyingDocumentsWereNotSufficientToArriveAtADecisionOnTheLevelOfCompliance contextRef="DCYMain">
        {{ 'true' if data.get('we_have_taken_management_explanations_wherever_the_information_available_on_the_underlying_documents_were_not_sufficient_to_arrive_at_a_decision_on_the_level_of_compliance') else 'false' }}
    </in-capmkt:WeHaveTakenManagementExplanationsWhereverTheInformationAvailableOnTheUnderlyingDocumentsWereNotSufficientToArriveAtADecisionOnTheLevelOfCompliance>
    {% endif %}

        {% if data.get('web_link_for_details_of_initiative_taken_by_entity') is not none %}
    <in-capmkt:WebLinkForDetailsOfInitiativeTakenByEntity contextRef="DCYMain">
        {{ data.get('web_link_for_details_of_initiative_taken_by_entity', '') }}
    </in-capmkt:WebLinkForDetailsOfInitiativeTakenByEntity>
    {% endif %}

        {% if data.get('web_link_of_sia_of_projects') is not none %}
    <in-capmkt:WebLinkOfSIAOfProjects contextRef="DCYMain">
        {{ data.get('web_link_of_sia_of_projects', '') }}
    </in-capmkt:WebLinkOfSIAOfProjects>
    {% endif %}

        {% if data.get('amount_held_by_other_shareholders') is not none %}
    <in-capmkt:AmountHeldByOtherShareholders contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_held_by_other_shareholders', '') }}
    </in-capmkt:AmountHeldByOtherShareholders>
    {% endif %}

        {% if data.get('amount_invested_in_fixed_deposits_or_mutual_funds_or_any_other_liquid_instruments_by_the_trust') is not none %}
    <in-capmkt:AmountInvestedInFixedDepositsOrMutualFundsOrAnyOtherLiquidInstrumentsByTheTrust contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_invested_in_fixed_deposits_or_mutual_funds_or_any_other_liquid_instruments_by_the_trust', '') }}
    </in-capmkt:AmountInvestedInFixedDepositsOrMutualFundsOrAnyOtherLiquidInstrumentsByTheTrust>
    {% endif %}

        {% if data.get('amount_of_default') is not none %}
    <in-capmkt:AmountOfDefault contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_of_default', '') }}
    </in-capmkt:AmountOfDefault>
    {% endif %}

        {% if data.get('amount_of_interest_paid') is not none %}
    <in-capmkt:AmountOfInterestPaid contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_of_interest_paid', '') }}
    </in-capmkt:AmountOfInterestPaid>
    {% endif %}

        {% if data.get('amount_of_issue_size') is not none %}
    <in-capmkt:AmountOfIssueSize contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_of_issue_size', '') }}
    </in-capmkt:AmountOfIssueSize>
    {% endif %}

        {% if data.get('amount_raised_by_loan_or_ecb') is not none %}
    <in-capmkt:AmountRaisedByLoanOrECB contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_raised_by_loan_or_ecb', '') }}
    </in-capmkt:AmountRaisedByLoanOrECB>
    {% endif %}

        {% if data.get('amount_raised_by_nc_ds') is not none %}
    <in-capmkt:AmountRaisedByNCDs contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_raised_by_nc_ds', '') }}
    </in-capmkt:AmountRaisedByNCDs>
    {% endif %}

        {% if data.get('amount_raised_by_preference_share') is not none %}
    <in-capmkt:AmountRaisedByPreferenceShare contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_raised_by_preference_share', '') }}
    </in-capmkt:AmountRaisedByPreferenceShare>
    {% endif %}

        {% if data.get('amount_redeemed') is not none %}
    <in-capmkt:AmountRedeemed contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_redeemed', '') }}
    </in-capmkt:AmountRedeemed>
    {% endif %}

        {% if data.get('amount_to_be_kept_aside_for_dsra_or_mmra_or_any_other_reserve_requirements_as_deemed_necessary_by_the_investment_manager') is not none %}
    <in-capmkt:AmountToBeKeptAsideForDSRAOrMMRAOrAnyOtherReserveRequirementsAsDeemedNecessaryByTheInvestmentManager contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amount_to_be_kept_aside_for_dsra_or_mmra_or_any_other_reserve_requirements_as_deemed_necessary_by_the_investment_manager', '') }}
    </in-capmkt:AmountToBeKeptAsideForDSRAOrMMRAOrAnyOtherReserveRequirementsAsDeemedNecessaryByTheInvestmentManager>
    {% endif %}

        {% if data.get('amounts_paid_to_pa_fs') is not none %}
    <in-capmkt:AmountsPaidToPAFs contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('amounts_paid_to_pa_fs', '') }}
    </in-capmkt:AmountsPaidToPAFs>
    {% endif %}

        {% if data.get('value_of_outstanding_redeemable_preference_shares') is not none %}
    <in-capmkt:ValueOfOutstandingRedeemablePreferenceShares contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('value_of_outstanding_redeemable_preference_shares', '') }}
    </in-capmkt:ValueOfOutstandingRedeemablePreferenceShares>
    {% endif %}

        {% if data.get('value_of_reitinvit_assets_gross_asset_value') is not none %}
    <in-capmkt:ValueOfREITINVITAssetsGrossAssetValue contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('value_of_reitinvit_assets_gross_asset_value', '') }}
    </in-capmkt:ValueOfREITINVITAssetsGrossAssetValue>
    {% endif %}

        {% if data.get('valuer_fees') is not none %}
    <in-capmkt:ValuerFees contextRef="DCYMain" unitRef="INR" decimals="2">
        {{ data.get('valuer_fees', '') }}
    </in-capmkt:ValuerFees>
    {% endif %}

        {% if data.get('assurance_sub_type_for_awareness_programmes_conducted_for_value_chain_partners_on_any_of_the_principles_during_the_financial_year') is not none %}
    <in-capmkt:AssuranceSubTypeForAwarenessProgrammesConductedForValueChainPartnersOnAnyOfThePrinciplesDuringTheFinancialYear contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_awareness_programmes_conducted_for_value_chain_partners_on_any_of_the_principles_during_the_financial_year', '') }}
    </in-capmkt:AssuranceSubTypeForAwarenessProgrammesConductedForValueChainPartnersOnAnyOfThePrinciplesDuringTheFinancialYear>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_value_chain_partner') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartner contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_value_chain_partner', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartner>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_concentration_of_purchases_and_sales_with_trading_houses_dealers_and_related_parties_along_with_loans_and_advances_and_investments_with_related_parties') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfConcentrationOfPurchasesAndSalesWithTradingHousesDealersAndRelatedPartiesAlongWithLoansAndAdvancesAndInvestmentsWithRelatedParties contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_concentration_of_purchases_and_sales_with_trading_houses_dealers_and_related_parties_along_with_loans_and_advances_and_investments_with_related_parties', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfConcentrationOfPurchasesAndSalesWithTradingHousesDealersAndRelatedPartiesAlongWithLoansAndAdvancesAndInvestmentsWithRelatedParties>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_measures_undertaken_by_the_entity_to_ensure_that_statutory_dues_have_been_deducted_and_deposited_by_the_value_chain_partners') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartners contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_measures_undertaken_by_the_entity_to_ensure_that_statutory_dues_have_been_deducted_and_deposited_by_the_value_chain_partners', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartners>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_on_assessment_of_value_chain_partners_p3') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOnAssessmentOfValueChainPartnersP3 contextRef="D_Principle3">
        {{ data.get('assurance_sub_type_for_details_on_assessment_of_value_chain_partners_p3', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOnAssessmentOfValueChainPartnersP3>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_on_assessment_of_value_chain_partners_p5') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOnAssessmentOfValueChainPartnersP5 contextRef="D_Principle5">
        {{ data.get('assurance_sub_type_for_details_on_assessment_of_value_chain_partners_p5', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOnAssessmentOfValueChainPartnersP5>
    {% endif %}

        {% if data.get('assurance_sub_type_for_green_credits_have_been_generated_or_procured_by_the_listed_entity_and_top_ten_value_chain_partners_is_assured_by_assurer') is not none %}
    <in-capmkt:AssuranceSubTypeForGreenCreditsHaveBeenGeneratedOrProcuredByTheListedEntityAndTopTenValueChainPartnersIsAssuredByAssurer contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_green_credits_have_been_generated_or_procured_by_the_listed_entity_and_top_ten_value_chain_partners_is_assured_by_assurer', '') }}
    </in-capmkt:AssuranceSubTypeForGreenCreditsHaveBeenGeneratedOrProcuredByTheListedEntityAndTopTenValueChainPartnersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('assurance_sub_type_for_percentage_of_input_material_inputs_to_total_inputs_by_value_sourced_from_suppliers') is not none %}
    <in-capmkt:AssuranceSubTypeForPercentageOfInputMaterialInputsToTotalInputsByValueSourcedFromSuppliers contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_percentage_of_input_material_inputs_to_total_inputs_by_value_sourced_from_suppliers', '') }}
    </in-capmkt:AssuranceSubTypeForPercentageOfInputMaterialInputsToTotalInputsByValueSourcedFromSuppliers>
    {% endif %}

        {% if data.get('assurance_sub_type_for_percentage_of_r_and_d_and_capital_expenditure_investments_in_specific_technologies') is not none %}
    <in-capmkt:AssuranceSubTypeForPercentageOfRAndDAndCapitalExpenditureInvestmentsInSpecificTechnologies contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_percentage_of_r_and_d_and_capital_expenditure_investments_in_specific_technologies', '') }}
    </in-capmkt:AssuranceSubTypeForPercentageOfRAndDAndCapitalExpenditureInvestmentsInSpecificTechnologies>
    {% endif %}

        {% if data.get('assurance_sub_type_for_value_of_shares_paid_up') is not none %}
    <in-capmkt:AssuranceSubTypeForValueOfSharesPaidUp contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_value_of_shares_paid_up', '') }}
    </in-capmkt:AssuranceSubTypeForValueOfSharesPaidUp>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_enlisted_policies_extend_to_your_value_chain_partners') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEnlistedPoliciesExtendToYourValueChainPartners contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_enlisted_policies_extend_to_your_value_chain_partners', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEnlistedPoliciesExtendToYourValueChainPartners>
    {% endif %}

        {% if data.get('assurance_sub_type_for_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification_of_any_non_compliances') is not none %}
    <in-capmkt:AssuranceSubTypeForComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliances contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification_of_any_non_compliances', '') }}
    </in-capmkt:AssuranceSubTypeForComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliances>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_corrective_action_taken_or_underway_on_any_issues_related_to_anti_competitive_conduct_by_the_entity_based_on_adverse_orders_from_regulatory_authorities') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfCorrectiveActionTakenOrUnderwayOnAnyIssuesRelatedToAntiCompetitiveConductByTheEntityBasedOnAdverseOrdersFromRegulatoryAuthorities contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_corrective_action_taken_or_underway_on_any_issues_related_to_anti_competitive_conduct_by_the_entity_based_on_adverse_orders_from_regulatory_authorities', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfCorrectiveActionTakenOrUnderwayOnAnyIssuesRelatedToAntiCompetitiveConductByTheEntityBasedOnAdverseOrdersFromRegulatoryAuthorities>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_corrective_actions_taken_or_underway_based_on_any_adverse_order_in_intellectual_property_related_disputes_wherein_usage_of_traditional_knowledge_is_involved') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfCorrectiveActionsTakenOrUnderwayBasedOnAnyAdverseOrderInIntellectualPropertyRelatedDisputesWhereinUsageOfTraditionalKnowledgeIsInvolved contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_corrective_actions_taken_or_underway_based_on_any_adverse_order_in_intellectual_property_related_disputes_wherein_usage_of_traditional_knowledge_is_involved', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfCorrectiveActionsTakenOrUnderwayBasedOnAnyAdverseOrderInIntellectualPropertyRelatedDisputesWhereinUsageOfTraditionalKnowledgeIsInvolved>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_financial_year_for_which_reporting_is_being_done') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfFinancialYearForWhichReportingIsBeingDone contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_financial_year_for_which_reporting_is_being_done', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfFinancialYearForWhichReportingIsBeingDone>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_fines_or_penalties_or_punishment_or_award_or_compounding_fees_or_settlement') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfFinesOrPenaltiesOrPunishmentOrAwardOrCompoundingFeesOrSettlement contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_fines_or_penalties_or_punishment_or_award_or_compounding_fees_or_settlement', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfFinesOrPenaltiesOrPunishmentOrAwardOrCompoundingFeesOrSettlement>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_projects_for_which_ongoing_rehabilitation_and_resettlement_is_being_undertaken_by_entity') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfProjectsForWhichOngoingRehabilitationAndResettlementIsBeingUndertakenByEntity contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_projects_for_which_ongoing_rehabilitation_and_resettlement_is_being_undertaken_by_entity', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfProjectsForWhichOngoingRehabilitationAndResettlementIsBeingUndertakenByEntity>
    {% endif %}

        {% if data.get('assurance_sub_type_for_details_of_the_appeal_or_revision_preferred_in_cases_where_monetary_or_non_monetary_action_has_been_appealed') is not none %}
    <in-capmkt:AssuranceSubTypeForDetailsOfTheAppealOrRevisionPreferredInCasesWhereMonetaryOrNonMonetaryActionHasBeenAppealed contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_details_of_the_appeal_or_revision_preferred_in_cases_where_monetary_or_non_monetary_action_has_been_appealed', '') }}
    </in-capmkt:AssuranceSubTypeForDetailsOfTheAppealOrRevisionPreferredInCasesWhereMonetaryOrNonMonetaryActionHasBeenAppealed>
    {% endif %}

        {% if data.get('assurance_sub_type_for_participation_or_inclusion_or_representation_of_women') is not none %}
    <in-capmkt:AssuranceSubTypeForParticipationOrInclusionOrRepresentationOfWomen contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_participation_or_inclusion_or_representation_of_women', '') }}
    </in-capmkt:AssuranceSubTypeForParticipationOrInclusionOrRepresentationOfWomen>
    {% endif %}

        {% if data.get('assurance_sub_type_for_performance_against_above_policies_and_follow_up_action') is not none %}
    <in-capmkt:AssuranceSubTypeForPerformanceAgainstAbovePoliciesAndFollowUpAction contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_performance_against_above_policies_and_follow_up_action', '') }}
    </in-capmkt:AssuranceSubTypeForPerformanceAgainstAbovePoliciesAndFollowUpAction>
    {% endif %}

        {% if data.get('assurance_sub_type_for_performance_of_the_entity_against_the_specific_commitments_goals_and_targets_along_with_reasons_in_case_the_same_are_not_met') is not none %}
    <in-capmkt:AssuranceSubTypeForPerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMet contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_performance_of_the_entity_against_the_specific_commitments_goals_and_targets_along_with_reasons_in_case_the_same_are_not_met', '') }}
    </in-capmkt:AssuranceSubTypeForPerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMet>
    {% endif %}

        {% if data.get('assurance_sub_type_for_reasons_if_policies_not_cover_each_principle_and_its_core_elements_of_the_ngrb_cs') is not none %}
    <in-capmkt:AssuranceSubTypeForReasonsIfPoliciesNotCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_reasons_if_policies_not_cover_each_principle_and_its_core_elements_of_the_ngrb_cs', '') }}
    </in-capmkt:AssuranceSubTypeForReasonsIfPoliciesNotCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs>
    {% endif %}

        {% if data.get('assurance_sub_type_for_reporting_boundary') is not none %}
    <in-capmkt:AssuranceSubTypeForReportingBoundary contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_reporting_boundary', '') }}
    </in-capmkt:AssuranceSubTypeForReportingBoundary>
    {% endif %}

        {% if data.get('assurance_sub_type_for_specific_commitments_goals_and_targets_set_by_the_entity_with_defined_timelines') is not none %}
    <in-capmkt:AssuranceSubTypeForSpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelines contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_specific_commitments_goals_and_targets_set_by_the_entity_with_defined_timelines', '') }}
    </in-capmkt:AssuranceSubTypeForSpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelines>
    {% endif %}

        {% if data.get('assurance_sub_type_for_whether_the_entity_has_carried_out_independent_assessment_evaluation_of_the_working_of_its_policies_by_an_external_agency') is not none %}
    <in-capmkt:AssuranceSubTypeForWhetherTheEntityHasCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency contextRef="DCYMain">
        {{ data.get('assurance_sub_type_for_whether_the_entity_has_carried_out_independent_assessment_evaluation_of_the_working_of_its_policies_by_an_external_agency', '') }}
    </in-capmkt:AssuranceSubTypeForWhetherTheEntityHasCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency>
    {% endif %}

        {% if data.get('percentage_of_investments_in_related_parties_in_total_investments') is not none %}
    <in-capmkt:PercentageOfInvestmentsInRelatedPartiesInTotalInvestments contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_investments_in_related_parties_in_total_investments', '') }}
    </in-capmkt:PercentageOfInvestmentsInRelatedPartiesInTotalInvestments>
    {% endif %}

        {% if data.get('percentage_of_purchases_from_related_parties_in_total_purchases_for_share_of_related_party_transactions') is not none %}
    <in-capmkt:PercentageOfPurchasesFromRelatedPartiesInTotalPurchasesForShareOfRelatedPartyTransactions contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_purchases_from_related_parties_in_total_purchases_for_share_of_related_party_transactions', '') }}
    </in-capmkt:PercentageOfPurchasesFromRelatedPartiesInTotalPurchasesForShareOfRelatedPartyTransactions>
    {% endif %}

        {% if data.get('percentage_of_sales_to_related_parties_in_total_sales_for_share_of_related_party_transactions') is not none %}
    <in-capmkt:PercentageOfSalesToRelatedPartiesInTotalSalesForShareOfRelatedPartyTransactions contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_sales_to_related_parties_in_total_sales_for_share_of_related_party_transactions', '') }}
    </in-capmkt:PercentageOfSalesToRelatedPartiesInTotalSalesForShareOfRelatedPartyTransactions>
    {% endif %}

        {% if data.get('percentage_of_working_conditions_of_value_chain_partners_p3') is not none %}
    <in-capmkt:PercentageOfWorkingConditionsOfValueChainPartnersP3 contextRef="D_Principle3" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_working_conditions_of_value_chain_partners_p3', '') }}
    </in-capmkt:PercentageOfWorkingConditionsOfValueChainPartnersP3>
    {% endif %}

        {% if data.get('percentage_of_job_creation') is not none %}
    <in-capmkt:PercentageOfJobCreation contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_job_creation', '') }}
    </in-capmkt:PercentageOfJobCreation>
    {% endif %}

        {% if data.get('percentage_of_loans_and_advances_given_to_related_parties_in_total_loans_and_advances') is not none %}
    <in-capmkt:PercentageOfLoansAndAdvancesGivenToRelatedPartiesInTotalLoansAndAdvances contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_loans_and_advances_given_to_related_parties_in_total_loans_and_advances', '') }}
    </in-capmkt:PercentageOfLoansAndAdvancesGivenToRelatedPartiesInTotalLoansAndAdvances>
    {% endif %}

        {% if data.get('percentage_of_pa_fs_covered_by_rehabilitation_and_resettlement') is not none %}
    <in-capmkt:PercentageOfPAFsCoveredByRehabilitationAndResettlement contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_pa_fs_covered_by_rehabilitation_and_resettlement', '') }}
    </in-capmkt:PercentageOfPAFsCoveredByRehabilitationAndResettlement>
    {% endif %}

        {% if data.get('percentage_of_proportion_of_a_in_comparison_to_b') is not none %}
    <in-capmkt:PercentageOfProportionOfAInComparisonToB contextRef="DCYMain" unitRef="pure" decimals="2">
        {{ data.get('percentage_of_proportion_of_a_in_comparison_to_b', '') }}
    </in-capmkt:PercentageOfProportionOfAInComparisonToB>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_awareness_programmes_conducted_for_value_chain_partners_on_any_of_the_principles_during_the_financial_year') is not none %}
    <in-capmkt:RemarksForAssuranceOfAwarenessProgrammesConductedForValueChainPartnersOnAnyOfThePrinciplesDuringTheFinancialYear contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_awareness_programmes_conducted_for_value_chain_partners_on_any_of_the_principles_during_the_financial_year', '') }}
    </in-capmkt:RemarksForAssuranceOfAwarenessProgrammesConductedForValueChainPartnersOnAnyOfThePrinciplesDuringTheFinancialYear>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_value_chain_partner') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartner contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_value_chain_partner', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartner>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_concentration_of_purchases_and_sales_with_trading_houses_dealers_and_related_parties_along_with_loans_and_advances_and_investments_with_related_parties') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfConcentrationOfPurchasesAndSalesWithTradingHousesDealersAndRelatedPartiesAlongWithLoansAndAdvancesAndInvestmentsWithRelatedParties contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_concentration_of_purchases_and_sales_with_trading_houses_dealers_and_related_parties_along_with_loans_and_advances_and_investments_with_related_parties', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfConcentrationOfPurchasesAndSalesWithTradingHousesDealersAndRelatedPartiesAlongWithLoansAndAdvancesAndInvestmentsWithRelatedParties>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_measures_undertaken_by_the_entity_to_ensure_that_statutory_dues_have_been_deducted_and_deposited_by_the_value_chain_partners') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartners contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_measures_undertaken_by_the_entity_to_ensure_that_statutory_dues_have_been_deducted_and_deposited_by_the_value_chain_partners', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartners>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_on_assessment_of_value_chain_partners_p3') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOnAssessmentOfValueChainPartnersP3 contextRef="D_Principle3">
        {{ data.get('remarks_for_assurance_of_details_on_assessment_of_value_chain_partners_p3', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOnAssessmentOfValueChainPartnersP3>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_on_assessment_of_value_chain_partners_p5') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOnAssessmentOfValueChainPartnersP5 contextRef="D_Principle5">
        {{ data.get('remarks_for_assurance_of_details_on_assessment_of_value_chain_partners_p5', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOnAssessmentOfValueChainPartnersP5>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_green_credits_have_been_generated_or_procured_by_the_listed_entity_and_top_ten_value_chain_partners_is_assured_by_assurer') is not none %}
    <in-capmkt:RemarksForAssuranceOfGreenCreditsHaveBeenGeneratedOrProcuredByTheListedEntityAndTopTenValueChainPartnersIsAssuredByAssurer contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_green_credits_have_been_generated_or_procured_by_the_listed_entity_and_top_ten_value_chain_partners_is_assured_by_assurer', '') }}
    </in-capmkt:RemarksForAssuranceOfGreenCreditsHaveBeenGeneratedOrProcuredByTheListedEntityAndTopTenValueChainPartnersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_percentage_of_input_material_inputs_to_total_inputs_by_value_sourced_from_suppliers') is not none %}
    <in-capmkt:RemarksForAssuranceOfPercentageOfInputMaterialInputsToTotalInputsByValueSourcedFromSuppliers contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_percentage_of_input_material_inputs_to_total_inputs_by_value_sourced_from_suppliers', '') }}
    </in-capmkt:RemarksForAssuranceOfPercentageOfInputMaterialInputsToTotalInputsByValueSourcedFromSuppliers>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_percentage_of_r_and_d_and_capital_expenditure_investments_in_specific_technologies') is not none %}
    <in-capmkt:RemarksForAssuranceOfPercentageOfRAndDAndCapitalExpenditureInvestmentsInSpecificTechnologies contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_percentage_of_r_and_d_and_capital_expenditure_investments_in_specific_technologies', '') }}
    </in-capmkt:RemarksForAssuranceOfPercentageOfRAndDAndCapitalExpenditureInvestmentsInSpecificTechnologies>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_value_of_shares_paid_up') is not none %}
    <in-capmkt:RemarksForAssuranceOfValueOfSharesPaidUp contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_value_of_shares_paid_up', '') }}
    </in-capmkt:RemarksForAssuranceOfValueOfSharesPaidUp>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_enlisted_policies_extend_to_your_value_chain_partners') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEnlistedPoliciesExtendToYourValueChainPartners contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_enlisted_policies_extend_to_your_value_chain_partners', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEnlistedPoliciesExtendToYourValueChainPartners>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification_of_any_non_compliances') is not none %}
    <in-capmkt:RemarksForAssuranceOfComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliances contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification_of_any_non_compliances', '') }}
    </in-capmkt:RemarksForAssuranceOfComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliances>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_corrective_action_taken_or_underway_on_any_issues_related_to_anti_competitive_conduct_by_the_entity_based_on_adverse_orders_from_regulatory_authorities') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfCorrectiveActionTakenOrUnderwayOnAnyIssuesRelatedToAntiCompetitiveConductByTheEntityBasedOnAdverseOrdersFromRegulatoryAuthorities contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_corrective_action_taken_or_underway_on_any_issues_related_to_anti_competitive_conduct_by_the_entity_based_on_adverse_orders_from_regulatory_authorities', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfCorrectiveActionTakenOrUnderwayOnAnyIssuesRelatedToAntiCompetitiveConductByTheEntityBasedOnAdverseOrdersFromRegulatoryAuthorities>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_corrective_actions_taken_or_underway_based_on_any_adverse_order_in_intellectual_property_related_disputes_wherein_usage_of_traditional_knowledge_is_involved') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfCorrectiveActionsTakenOrUnderwayBasedOnAnyAdverseOrderInIntellectualPropertyRelatedDisputesWhereinUsageOfTraditionalKnowledgeIsInvolved contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_corrective_actions_taken_or_underway_based_on_any_adverse_order_in_intellectual_property_related_disputes_wherein_usage_of_traditional_knowledge_is_involved', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfCorrectiveActionsTakenOrUnderwayBasedOnAnyAdverseOrderInIntellectualPropertyRelatedDisputesWhereinUsageOfTraditionalKnowledgeIsInvolved>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_financial_year_for_which_reporting_is_being_done') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfFinancialYearForWhichReportingIsBeingDone contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_financial_year_for_which_reporting_is_being_done', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfFinancialYearForWhichReportingIsBeingDone>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_fines_or_penalties_or_punishment_or_award_or_compounding_fees_or_settlement') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfFinesOrPenaltiesOrPunishmentOrAwardOrCompoundingFeesOrSettlement contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_fines_or_penalties_or_punishment_or_award_or_compounding_fees_or_settlement', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfFinesOrPenaltiesOrPunishmentOrAwardOrCompoundingFeesOrSettlement>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_projects_for_which_ongoing_rehabilitation_and_resettlement_is_being_undertaken_by_entity') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfProjectsForWhichOngoingRehabilitationAndResettlementIsBeingUndertakenByEntity contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_projects_for_which_ongoing_rehabilitation_and_resettlement_is_being_undertaken_by_entity', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfProjectsForWhichOngoingRehabilitationAndResettlementIsBeingUndertakenByEntity>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_details_of_the_appeal_or_revision_preferred_in_cases_where_monetary_or_non_monetary_action_has_been_appealed') is not none %}
    <in-capmkt:RemarksForAssuranceOfDetailsOfTheAppealOrRevisionPreferredInCasesWhereMonetaryOrNonMonetaryActionHasBeenAppealed contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_details_of_the_appeal_or_revision_preferred_in_cases_where_monetary_or_non_monetary_action_has_been_appealed', '') }}
    </in-capmkt:RemarksForAssuranceOfDetailsOfTheAppealOrRevisionPreferredInCasesWhereMonetaryOrNonMonetaryActionHasBeenAppealed>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_participation_or_inclusion_or_representation_of_women') is not none %}
    <in-capmkt:RemarksForAssuranceOfParticipationOrInclusionOrRepresentationOfWomen contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_participation_or_inclusion_or_representation_of_women', '') }}
    </in-capmkt:RemarksForAssuranceOfParticipationOrInclusionOrRepresentationOfWomen>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_performance_against_above_policies_and_follow_up_action') is not none %}
    <in-capmkt:RemarksForAssuranceOfPerformanceAgainstAbovePoliciesAndFollowUpAction contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_performance_against_above_policies_and_follow_up_action', '') }}
    </in-capmkt:RemarksForAssuranceOfPerformanceAgainstAbovePoliciesAndFollowUpAction>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_performance_of_the_entity_against_the_specific_commitments_goals_and_targets_along_with_reasons_in_case_the_same_are_not_met') is not none %}
    <in-capmkt:RemarksForAssuranceOfPerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMet contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_performance_of_the_entity_against_the_specific_commitments_goals_and_targets_along_with_reasons_in_case_the_same_are_not_met', '') }}
    </in-capmkt:RemarksForAssuranceOfPerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMet>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_reasons_if_policies_not_cover_each_principle_and_its_core_elements_of_the_ngrb_cs') is not none %}
    <in-capmkt:RemarksForAssuranceOfReasonsIfPoliciesNotCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_reasons_if_policies_not_cover_each_principle_and_its_core_elements_of_the_ngrb_cs', '') }}
    </in-capmkt:RemarksForAssuranceOfReasonsIfPoliciesNotCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_reporting_boundary') is not none %}
    <in-capmkt:RemarksForAssuranceOfReportingBoundary contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_reporting_boundary', '') }}
    </in-capmkt:RemarksForAssuranceOfReportingBoundary>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_specific_commitments_goals_and_targets_set_by_the_entity_with_defined_timelines') is not none %}
    <in-capmkt:RemarksForAssuranceOfSpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelines contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_specific_commitments_goals_and_targets_set_by_the_entity_with_defined_timelines', '') }}
    </in-capmkt:RemarksForAssuranceOfSpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelines>
    {% endif %}

        {% if data.get('remarks_for_assurance_of_whether_the_entity_has_carried_out_independent_assessment_evaluation_of_the_working_of_its_policies_by_an_external_agency') is not none %}
    <in-capmkt:RemarksForAssuranceOfWhetherTheEntityHasCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency contextRef="DCYMain">
        {{ data.get('remarks_for_assurance_of_whether_the_entity_has_carried_out_independent_assessment_evaluation_of_the_working_of_its_policies_by_an_external_agency', '') }}
    </in-capmkt:RemarksForAssuranceOfWhetherTheEntityHasCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency>
    {% endif %}

        {% if data.get('remarks_in_case_of_observation') is not none %}
    <in-capmkt:RemarksInCaseOfObservation contextRef="DCYMain">
        {{ data.get('remarks_in_case_of_observation', '') }}
    </in-capmkt:RemarksInCaseOfObservation>
    {% endif %}

        {% if data.get('remarks_of_the_asset_acquired') is not none %}
    <in-capmkt:RemarksOfTheAssetAcquired contextRef="ICYMain">
        {{ data.get('remarks_of_the_asset_acquired', '') }}
    </in-capmkt:RemarksOfTheAssetAcquired>
    {% endif %}

        {% if data.get('remarks_of_the_asset_disposed_off') is not none %}
    <in-capmkt:RemarksOfTheAssetDisposedOff contextRef="ICYMain">
        {{ data.get('remarks_of_the_asset_disposed_off', '') }}
    </in-capmkt:RemarksOfTheAssetDisposedOff>
    {% endif %}

        {% if data.get('whether_awareness_programmes_conducted_for_value_chain_partners_on_any_of_the_principles_during_the_financial_year_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherAwarenessProgrammesConductedForValueChainPartnersOnAnyOfThePrinciplesDuringTheFinancialYearIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_awareness_programmes_conducted_for_value_chain_partners_on_any_of_the_principles_during_the_financial_year_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherAwarenessProgrammesConductedForValueChainPartnersOnAnyOfThePrinciplesDuringTheFinancialYearIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_value_chain_partner_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartnerIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_any_corrective_actions_taken_or_underway_to_address_significant_risks_or_concerns_arising_from_the_assessments_of_value_chain_partner_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartnerIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_concentration_of_purchases_and_sales_with_trading_houses_dealers_and_related_parties_along_with_loans_and_advances_and_investments_with_related_parties_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfConcentrationOfPurchasesAndSalesWithTradingHousesDealersAndRelatedPartiesAlongWithLoansAndAdvancesAndInvestmentsWithRelatedPartiesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_concentration_of_purchases_and_sales_with_trading_houses_dealers_and_related_parties_along_with_loans_and_advances_and_investments_with_related_parties_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfConcentrationOfPurchasesAndSalesWithTradingHousesDealersAndRelatedPartiesAlongWithLoansAndAdvancesAndInvestmentsWithRelatedPartiesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_measures_undertaken_by_the_entity_to_ensure_that_statutory_dues_have_been_deducted_and_deposited_by_the_value_chain_partners_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartnersIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_measures_undertaken_by_the_entity_to_ensure_that_statutory_dues_have_been_deducted_and_deposited_by_the_value_chain_partners_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartnersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_on_assessment_of_value_chain_partners_p3_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOnAssessmentOfValueChainPartnersP3IsAssuredByAssurer contextRef="D_Principle3">
        {{ 'true' if data.get('whether_details_on_assessment_of_value_chain_partners_p3_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOnAssessmentOfValueChainPartnersP3IsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_on_assessment_of_value_chain_partners_p5_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOnAssessmentOfValueChainPartnersP5IsAssuredByAssurer contextRef="D_Principle5">
        {{ 'true' if data.get('whether_details_on_assessment_of_value_chain_partners_p5_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOnAssessmentOfValueChainPartnersP5IsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_green_credits_have_been_generated_or_procured_by_the_listed_entity_and_top_ten_value_chain_partners_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherGreenCreditsHaveBeenGeneratedOrProcuredByTheListedEntityAndTopTenValueChainPartnersIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_green_credits_have_been_generated_or_procured_by_the_listed_entity_and_top_ten_value_chain_partners_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherGreenCreditsHaveBeenGeneratedOrProcuredByTheListedEntityAndTopTenValueChainPartnersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_percentage_of_input_material_inputs_to_total_inputs_by_value_sourced_from_suppliers_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherPercentageOfInputMaterialInputsToTotalInputsByValueSourcedFromSuppliersIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_percentage_of_input_material_inputs_to_total_inputs_by_value_sourced_from_suppliers_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherPercentageOfInputMaterialInputsToTotalInputsByValueSourcedFromSuppliersIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_percentage_of_r_and_d_and_capital_expenditure_investments_in_specific_technologies_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherPercentageOfRAndDAndCapitalExpenditureInvestmentsInSpecificTechnologiesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_percentage_of_r_and_d_and_capital_expenditure_investments_in_specific_technologies_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherPercentageOfRAndDAndCapitalExpenditureInvestmentsInSpecificTechnologiesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_value_of_shares_paid_up_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherValueOfSharesPaidUpIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_value_of_shares_paid_up_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherValueOfSharesPaidUpIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_any_adverse_observation_pointed_in_iar') is not none %}
    <in-capmkt:WhetherAnyAdverseObservationPointedInIAR contextRef="DCYMain">
        {{ 'true' if data.get('whether_any_adverse_observation_pointed_in_iar') else 'false' }}
    </in-capmkt:WhetherAnyAdverseObservationPointedInIAR>
    {% endif %}

        {% if data.get('whether_any_high_risk_issue_observed') is not none %}
    <in-capmkt:WhetherAnyHighRiskIssueObserved contextRef="DCYMain">
        {{ 'true' if data.get('whether_any_high_risk_issue_observed') else 'false' }}
    </in-capmkt:WhetherAnyHighRiskIssueObserved>
    {% endif %}

        {% if data.get('whether_auditor_comments_accepted') is not none %}
    <in-capmkt:WhetherAuditorCommentsAccepted contextRef="DCYMain">
        {{ 'true' if data.get('whether_auditor_comments_accepted') else 'false' }}
    </in-capmkt:WhetherAuditorCommentsAccepted>
    {% endif %}

        {% if data.get('whether_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification_of_any_non_compliances_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_compliance_with_statutory_requirements_of_relevance_to_the_principles_and_rectification_of_any_non_compliances_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_conducted_by_independent_external_agency') is not none %}
    <in-capmkt:WhetherConductedByIndependentExternalAgency contextRef="DCYMain">
        {{ 'true' if data.get('whether_conducted_by_independent_external_agency') else 'false' }}
    </in-capmkt:WhetherConductedByIndependentExternalAgency>
    {% endif %}

        {% if data.get('whether_conducted_by_independent_external_agency_for_sia') is not none %}
    <in-capmkt:WhetherConductedByIndependentExternalAgencyForSIA contextRef="DCYMain">
        {{ 'true' if data.get('whether_conducted_by_independent_external_agency_for_sia') else 'false' }}
    </in-capmkt:WhetherConductedByIndependentExternalAgencyForSIA>
    {% endif %}

        {% if data.get('whether_conducted_by_independent_external_agency_p6') is not none %}
    <in-capmkt:WhetherConductedByIndependentExternalAgencyP6 contextRef="D_Principle6">
        {{ 'true' if data.get('whether_conducted_by_independent_external_agency_p6') else 'false' }}
    </in-capmkt:WhetherConductedByIndependentExternalAgencyP6>
    {% endif %}

        {% if data.get('whether_details_of_corrective_action_taken_or_underway_on_any_issues_related_to_anti_competitive_conduct_by_the_entity_based_on_adverse_orders_from_regulatory_authorities_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfCorrectiveActionTakenOrUnderwayOnAnyIssuesRelatedToAntiCompetitiveConductByTheEntityBasedOnAdverseOrdersFromRegulatoryAuthoritiesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_corrective_action_taken_or_underway_on_any_issues_related_to_anti_competitive_conduct_by_the_entity_based_on_adverse_orders_from_regulatory_authorities_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfCorrectiveActionTakenOrUnderwayOnAnyIssuesRelatedToAntiCompetitiveConductByTheEntityBasedOnAdverseOrdersFromRegulatoryAuthoritiesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_corrective_actions_taken_or_underway_based_on_any_adverse_order_in_intellectual_property_related_disputes_wherein_usage_of_traditional_knowledge_is_involved_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfCorrectiveActionsTakenOrUnderwayBasedOnAnyAdverseOrderInIntellectualPropertyRelatedDisputesWhereinUsageOfTraditionalKnowledgeIsInvolvedIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_corrective_actions_taken_or_underway_based_on_any_adverse_order_in_intellectual_property_related_disputes_wherein_usage_of_traditional_knowledge_is_involved_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfCorrectiveActionsTakenOrUnderwayBasedOnAnyAdverseOrderInIntellectualPropertyRelatedDisputesWhereinUsageOfTraditionalKnowledgeIsInvolvedIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_financial_year_for_which_reporting_is_being_done_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfFinancialYearForWhichReportingIsBeingDoneIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_financial_year_for_which_reporting_is_being_done_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfFinancialYearForWhichReportingIsBeingDoneIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_fines_or_penalties_or_punishment_or_award_or_compounding_fees_or_settlement_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfFinesOrPenaltiesOrPunishmentOrAwardOrCompoundingFeesOrSettlementIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_fines_or_penalties_or_punishment_or_award_or_compounding_fees_or_settlement_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfFinesOrPenaltiesOrPunishmentOrAwardOrCompoundingFeesOrSettlementIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_projects_for_which_ongoing_rehabilitation_and_resettlement_is_being_undertaken_by_entity_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfProjectsForWhichOngoingRehabilitationAndResettlementIsBeingUndertakenByEntityIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_projects_for_which_ongoing_rehabilitation_and_resettlement_is_being_undertaken_by_entity_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfProjectsForWhichOngoingRehabilitationAndResettlementIsBeingUndertakenByEntityIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_details_of_the_appeal_or_revision_preferred_in_cases_where_monetary_or_non_monetary_action_has_been_appealed_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherDetailsOfTheAppealOrRevisionPreferredInCasesWhereMonetaryOrNonMonetaryActionHasBeenAppealedIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_details_of_the_appeal_or_revision_preferred_in_cases_where_monetary_or_non_monetary_action_has_been_appealed_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherDetailsOfTheAppealOrRevisionPreferredInCasesWhereMonetaryOrNonMonetaryActionHasBeenAppealedIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_earlier_rating_applicable') is not none %}
    <in-capmkt:WhetherEarlierRatingApplicable contextRef="DCYMain">
        {{ 'true' if data.get('whether_earlier_rating_applicable') else 'false' }}
    </in-capmkt:WhetherEarlierRatingApplicable>
    {% endif %}

        {% if data.get('whether_high_risk_issue') is not none %}
    <in-capmkt:WhetherHighRiskIssue contextRef="DCYMain">
        {{ 'true' if data.get('whether_high_risk_issue') else 'false' }}
    </in-capmkt:WhetherHighRiskIssue>
    {% endif %}

        {% if data.get('whether_interest_payment_or_redemption_payment_made') is not none %}
    <in-capmkt:WhetherInterestPaymentOrRedemptionPaymentMade contextRef="DCYMain">
        {{ 'true' if data.get('whether_interest_payment_or_redemption_payment_made') else 'false' }}
    </in-capmkt:WhetherInterestPaymentOrRedemptionPaymentMade>
    {% endif %}

        {% if data.get('whether_it_is_a_related_party_transaction_of_the_asset_acquired') is not none %}
    <in-capmkt:WhetherItIsARelatedPartyTransactionOfTheAssetAcquired contextRef="DCYMain">
        {{ 'true' if data.get('whether_it_is_a_related_party_transaction_of_the_asset_acquired') else 'false' }}
    </in-capmkt:WhetherItIsARelatedPartyTransactionOfTheAssetAcquired>
    {% endif %}

        {% if data.get('whether_it_is_a_related_party_transaction_of_the_asset_disposed_off') is not none %}
    <in-capmkt:WhetherItIsARelatedPartyTransactionOfTheAssetDisposedOff contextRef="DCYMain">
        {{ 'true' if data.get('whether_it_is_a_related_party_transaction_of_the_asset_disposed_off') else 'false' }}
    </in-capmkt:WhetherItIsARelatedPartyTransactionOfTheAssetDisposedOff>
    {% endif %}

        {% if data.get('whether_participation_or_inclusion_or_representation_of_women_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherParticipationOrInclusionOrRepresentationOfWomenIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_participation_or_inclusion_or_representation_of_women_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherParticipationOrInclusionOrRepresentationOfWomenIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_performance_against_above_policies_and_follow_up_action_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherPerformanceAgainstAbovePoliciesAndFollowUpActionIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_performance_against_above_policies_and_follow_up_action_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherPerformanceAgainstAbovePoliciesAndFollowUpActionIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_performance_of_the_entity_against_the_specific_commitments_goals_and_targets_along_with_reasons_in_case_the_same_are_not_met_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherPerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMetIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_performance_of_the_entity_against_the_specific_commitments_goals_and_targets_along_with_reasons_in_case_the_same_are_not_met_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherPerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMetIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_reasons_if_policies_not_cover_each_principle_and_its_core_elements_of_the_ngrb_cs_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherReasonsIfPoliciesNotCoverEachPrincipleAndItsCoreElementsOfTheNGRBCsIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_reasons_if_policies_not_cover_each_principle_and_its_core_elements_of_the_ngrb_cs_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherReasonsIfPoliciesNotCoverEachPrincipleAndItsCoreElementsOfTheNGRBCsIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_reporting_boundary_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherReportingBoundaryIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_reporting_boundary_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherReportingBoundaryIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_results_are_audited_or_unaudited') is not none %}
    <in-capmkt:WhetherResultsAreAuditedOrUnaudited contextRef="DCYMain">
        {{ data.get('whether_results_are_audited_or_unaudited', '') }}
    </in-capmkt:WhetherResultsAreAuditedOrUnaudited>
    {% endif %}

        {% if data.get('whether_specific_commitments_goals_and_targets_set_by_the_entity_with_defined_timelines_is_assured_by_assurer') is not none %}
    <in-capmkt:WhetherSpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelinesIsAssuredByAssurer contextRef="DCYMain">
        {{ 'true' if data.get('whether_specific_commitments_goals_and_targets_set_by_the_entity_with_defined_timelines_is_assured_by_assurer') else 'false' }}
    </in-capmkt:WhetherSpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelinesIsAssuredByAssurer>
    {% endif %}

        {% if data.get('whether_the_interest_or_dividend_has_been_paid_or_not') is not none %}
    <in-capmkt:WhetherTheInterestOrDividendHasBeenPaidOrNot contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_interest_or_dividend_has_been_paid_or_not') else 'false' }}
    </in-capmkt:WhetherTheInterestOrDividendHasBeenPaidOrNot>
    {% endif %}

        {% if data.get('whether_the_non_compliance_or_work_in_progress_or_observation_or_suggestion_accepted_by_the_management') is not none %}
    <in-capmkt:WhetherTheNonComplianceOrWorkInProgressOrObservationOrSuggestionAcceptedByTheManagement contextRef="DCYMain">
        {{ 'true' if data.get('whether_the_non_compliance_or_work_in_progress_or_observation_or_suggestion_accepted_by_the_management') else 'false' }}
    </in-capmkt:WhetherTheNonComplianceOrWorkInProgressOrObservationOrSuggestionAcceptedByTheManagement>
    {% endif %}

        {% if data.get('access_controlmember') is not none %}
    <in-capmkt:AccessControlmember contextRef="DCYMain">
        {{ data.get('access_controlmember', '') }}
    </in-capmkt:AccessControlmember>
    {% endif %}

        {% if data.get('appeal_or_revisiondomain') is not none %}
    <in-capmkt:AppealOrRevisiondomain contextRef="DCYMain">
        {{ data.get('appeal_or_revisiondomain', '') }}
    </in-capmkt:AppealOrRevisiondomain>
    {% endif %}

        {% if data.get('date_by_which_payment_of_distribution_is_completed') is not none %}
    <in-capmkt:DateByWhichPaymentOfDistributionIsCompleted contextRef="DCYMain">
        {{ data.get('date_by_which_payment_of_distribution_is_completed', '') }}
    </in-capmkt:DateByWhichPaymentOfDistributionIsCompleted>
    {% endif %}

        {% if data.get('date_by_which_wip_issue_will_be_complied') is not none %}
    <in-capmkt:DateByWhichWIPIssueWillBeComplied contextRef="DCYMain">
        {{ data.get('date_by_which_wip_issue_will_be_complied', '') }}
    </in-capmkt:DateByWhichWIPIssueWillBeComplied>
    {% endif %}

        {% if data.get('date_of_allotment_of_securities') is not none %}
    <in-capmkt:DateOfAllotmentOfSecurities contextRef="DCYMain">
        {{ data.get('date_of_allotment_of_securities', '') }}
    </in-capmkt:DateOfAllotmentOfSecurities>
    {% endif %}

        {% if data.get('date_of_audit') is not none %}
    <in-capmkt:DateOfAudit contextRef="DCYMain">
        {{ data.get('date_of_audit', '') }}
    </in-capmkt:DateOfAudit>
    {% endif %}

        {% if data.get('date_of_board_approval') is not none %}
    <in-capmkt:DateOfBoardApproval contextRef="DCYMain">
        {{ data.get('date_of_board_approval', '') }}
    </in-capmkt:DateOfBoardApproval>
    {% endif %}

        {% if data.get('date_of_board_meeting_when_financial_results_were_approved') is not none %}
    <in-capmkt:DateOfBoardMeetingWhenFinancialResultsWereApproved contextRef="DCYMain">
        {{ data.get('date_of_board_meeting_when_financial_results_were_approved', '') }}
    </in-capmkt:DateOfBoardMeetingWhenFinancialResultsWereApproved>
    {% endif %}

        {% if data.get('date_of_credit_rating') is not none %}
    <in-capmkt:DateOfCreditRating contextRef="DCYMain">
        {{ data.get('date_of_credit_rating', '') }}
    </in-capmkt:DateOfCreditRating>
    {% endif %}

        {% if data.get('date_of_default') is not none %}
    <in-capmkt:DateOfDefault contextRef="DCYMain">
        {{ data.get('date_of_default', '') }}
    </in-capmkt:DateOfDefault>
    {% endif %}

        {% if data.get('date_of_end_of_audit_period') is not none %}
    <in-capmkt:DateOfEndOfAuditPeriod contextRef="DCYMain">
        {{ data.get('date_of_end_of_audit_period', '') }}
    </in-capmkt:DateOfEndOfAuditPeriod>
    {% endif %}

        {% if data.get('date_of_end_of_board_meeting') is not none %}
    <in-capmkt:DateOfEndOfBoardMeeting contextRef="DCYMain">
        {{ data.get('date_of_end_of_board_meeting', '') }}
    </in-capmkt:DateOfEndOfBoardMeeting>
    {% endif %}

        {% if data.get('date_of_end_of_reporting_period') is not none %}
    <in-capmkt:DateOfEndOfReportingPeriod contextRef="DCYMain">
        {{ data.get('date_of_end_of_reporting_period', '') }}
    </in-capmkt:DateOfEndOfReportingPeriod>
    {% endif %}

        {% if data.get('date_of_interest_payment_or_redemption_payment') is not none %}
    <in-capmkt:DateOfInterestPaymentOrRedemptionPayment contextRef="DCYMain">
        {{ data.get('date_of_interest_payment_or_redemption_payment', '') }}
    </in-capmkt:DateOfInterestPaymentOrRedemptionPayment>
    {% endif %}

        {% if data.get('date_of_issue') is not none %}
    <in-capmkt:DateOfIssue contextRef="DCYMain">
        {{ data.get('date_of_issue', '') }}
    </in-capmkt:DateOfIssue>
    {% endif %}

        {% if data.get('date_of_last_interest_payment') is not none %}
    <in-capmkt:DateOfLastInterestPayment contextRef="DCYMain">
        {{ data.get('date_of_last_interest_payment', '') }}
    </in-capmkt:DateOfLastInterestPayment>
    {% endif %}

        {% if data.get('date_of_meeting_of_board_of_the_manager_or_im_or_unitholders_approval_for_assets_acquired') is not none %}
    <in-capmkt:DateOfMeetingOfBoardOfTheManagerOrIMOrUnitholdersApprovalForAssetsAcquired contextRef="DCYMain">
        {{ data.get('date_of_meeting_of_board_of_the_manager_or_im_or_unitholders_approval_for_assets_acquired', '') }}
    </in-capmkt:DateOfMeetingOfBoardOfTheManagerOrIMOrUnitholdersApprovalForAssetsAcquired>
    {% endif %}

        {% if data.get('date_of_meeting_of_board_of_the_manager_or_im_or_unitholders_approval_for_assets_disposed_off') is not none %}
    <in-capmkt:DateOfMeetingOfBoardOfTheManagerOrImOrUnitholdersApprovalForAssetsDisposedOff contextRef="DCYMain">
        {{ data.get('date_of_meeting_of_board_of_the_manager_or_im_or_unitholders_approval_for_assets_disposed_off', '') }}
    </in-capmkt:DateOfMeetingOfBoardOfTheManagerOrImOrUnitholdersApprovalForAssetsDisposedOff>
    {% endif %}

        {% if data.get('date_of_notification') is not none %}
    <in-capmkt:DateOfNotification contextRef="DCYMain">
        {{ data.get('date_of_notification', '') }}
    </in-capmkt:DateOfNotification>
    {% endif %}

        {% if data.get('date_of_report') is not none %}
    <in-capmkt:DateOfReport contextRef="ICYMain">
        {{ data.get('date_of_report', '') }}
    </in-capmkt:DateOfReport>
    {% endif %}

        {% if data.get('date_of_signatory') is not none %}
    <in-capmkt:DateOfSignatory contextRef="DCYMain">
        {{ data.get('date_of_signatory', '') }}
    </in-capmkt:DateOfSignatory>
    {% endif %}

        {% if data.get('date_of_start_of_audit_period') is not none %}
    <in-capmkt:DateOfStartOfAuditPeriod contextRef="DCYMain">
        {{ data.get('date_of_start_of_audit_period', '') }}
    </in-capmkt:DateOfStartOfAuditPeriod>
    {% endif %}

        {% if data.get('date_of_start_of_board_meeting') is not none %}
    <in-capmkt:DateOfStartOfBoardMeeting contextRef="DCYMain">
        {{ data.get('date_of_start_of_board_meeting', '') }}
    </in-capmkt:DateOfStartOfBoardMeeting>
    {% endif %}

        {% if data.get('date_of_unitholders_approval') is not none %}
    <in-capmkt:DateOfUnitholdersApproval contextRef="DCYMain">
        {{ data.get('date_of_unitholders_approval', '') }}
    </in-capmkt:DateOfUnitholdersApproval>
    {% endif %}

        {% if data.get('date_of_verification') is not none %}
    <in-capmkt:DateOfVerification contextRef="DCYMain">
        {{ data.get('date_of_verification', '') }}
    </in-capmkt:DateOfVerification>
    {% endif %}

        {% if data.get('date_on_which_position_taken_in_cd_segment') is not none %}
    <in-capmkt:DateOnWhichPositionTakenInCDSegment contextRef="DCYMain">
        {{ data.get('date_on_which_position_taken_in_cd_segment', '') }}
    </in-capmkt:DateOnWhichPositionTakenInCDSegment>
    {% endif %}

        {% if data.get('date_on_which_prior_intimation_of_the_meeting_for_considering_financial_results_was_informed_to_the_exchange') is not none %}
    <in-capmkt:DateOnWhichPriorIntimationOfTheMeetingForConsideringFinancialResultsWasInformedToTheExchange contextRef="DCYMain">
        {{ data.get('date_on_which_prior_intimation_of_the_meeting_for_considering_financial_results_was_informed_to_the_exchange', '') }}
    </in-capmkt:DateOnWhichPriorIntimationOfTheMeetingForConsideringFinancialResultsWasInformedToTheExchange>
    {% endif %}

        {% if data.get('date_on_which_the_asset_was_acquired') is not none %}
    <in-capmkt:DateOnWhichTheAssetWasAcquired contextRef="DCYMain">
        {{ data.get('date_on_which_the_asset_was_acquired', '') }}
    </in-capmkt:DateOnWhichTheAssetWasAcquired>
    {% endif %}

        {% if data.get('date_on_which_the_asset_was_disposed_off') is not none %}
    <in-capmkt:DateOnWhichTheAssetWasDisposedOff contextRef="DCYMain">
        {{ data.get('date_on_which_the_asset_was_disposed_off', '') }}
    </in-capmkt:DateOnWhichTheAssetWasDisposedOff>
    {% endif %}

        {% if data.get('dateof_board_meeting_in_which_the_distribution_declared') is not none %}
    <in-capmkt:DateofBoardMeetingInWhichTheDistributionDeclared contextRef="DCYMain">
        {{ data.get('dateof_board_meeting_in_which_the_distribution_declared', '') }}
    </in-capmkt:DateofBoardMeetingInWhichTheDistributionDeclared>
    {% endif %}

        {% if data.get('details_of_aggregate_consolidated_borrowing_as_per_sebireitinvit_regulations_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfAggregateConsolidatedBorrowingAsPerSEBIREITINVITRegulationsExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_aggregate_consolidated_borrowing_as_per_sebireitinvit_regulations_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfAggregateConsolidatedBorrowingAsPerSEBIREITINVITRegulationsExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_assets_acquired_during_the_reporting_period_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfAssetsAcquiredDuringTheReportingPeriodExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_assets_acquired_during_the_reporting_period_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfAssetsAcquiredDuringTheReportingPeriodExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_assets_disposed_off_during_the_reporting_period_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfAssetsDisposedOffDuringTheReportingPeriodExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_assets_disposed_off_during_the_reporting_period_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfAssetsDisposedOffDuringTheReportingPeriodExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_borrowing_or_debt_raised_during_the_period_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfBorrowingOrDebtRaisedDuringThePeriodExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_borrowing_or_debt_raised_during_the_period_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfBorrowingOrDebtRaisedDuringThePeriodExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_capital_raised_during_the_period_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfCapitalRaisedDuringThePeriodExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_capital_raised_during_the_period_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfCapitalRaisedDuringThePeriodExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_funds_raised_through_debt_consolidated_basis_explanatory_text_block') is not none %}
    <in-capmkt:DetailsOfFundsRaisedThroughDebtConsolidatedBasisExplanatoryTextBlock contextRef="DCYMain" escape="true">
        {{ data.get('details_of_funds_raised_through_debt_consolidated_basis_explanatory_text_block', '') }}
    </in-capmkt:DetailsOfFundsRaisedThroughDebtConsolidatedBasisExplanatoryTextBlock>
    {% endif %}

        {% if data.get('details_of_listing_of_securities') is not none %}
    <in-capmkt:DetailsOfListingOfSecurities contextRef="ICYMain">
        {{ data.get('details_of_listing_of_securities', '') }}
    </in-capmkt:DetailsOfListingOfSecurities>
    {% endif %}

        {% if data.get('details_of_other_reason_for_redemption') is not none %}
    <in-capmkt:DetailsOfOtherReasonForRedemption contextRef="ICYMain">
        {{ data.get('details_of_other_reason_for_redemption', '') }}
    </in-capmkt:DetailsOfOtherReasonForRedemption>
    {% endif %}

        {% if data.get('details_of_outstanding_redeemable_preference_shares') is not none %}
    <in-capmkt:DetailsOfOutstandingRedeemablePreferenceShares contextRef="DCYMain">
        {{ data.get('details_of_outstanding_redeemable_preference_shares', '') }}
    </in-capmkt:DetailsOfOutstandingRedeemablePreferenceShares>
    {% endif %}

        
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

            <in-capmkt:NumberOfLocations contextRef="D_Plant_National" decimals="0" unitRef="pure">{{ locations.national.plants|int }}</in-capmkt:NumberOfLocations>
    <in-capmkt:NumberOfLocations contextRef="D_Office_National" decimals="0" unitRef="pure">{{ locations.national.offices|int }}</in-capmkt:NumberOfLocations>
    <in-capmkt:NumberOfLocations contextRef="D_Location_National" decimals="0" unitRef="pure">{{ locations.national.total|int }}</in-capmkt:NumberOfLocations>
        <in-capmkt:NumberOfLocations contextRef="D_Plant_International" decimals="0" unitRef="pure">{{ locations.international.plants|int }}</in-capmkt:NumberOfLocations>
    <in-capmkt:NumberOfLocations contextRef="D_Office_International" decimals="0" unitRef="pure">{{ locations.international.offices|int }}</in-capmkt:NumberOfLocations>
    <in-capmkt:NumberOfLocations contextRef="D_Location_International" decimals="0" unitRef="pure">{{ locations.international.total|int }}</in-capmkt:NumberOfLocations>

            <in-capmkt:NumberOfStatesWhereMarketServedByTheEntity contextRef="DCYMain" decimals="0" unitRef="pure">{{ markets.national_states_count|int }}</in-capmkt:NumberOfStatesWhereMarketServedByTheEntity>
    <in-capmkt:NumberOfCountriesWhereMarketServedByTheEntity contextRef="DCYMain" decimals="0" unitRef="pure">{{ markets.international_countries_count|int }}</in-capmkt:NumberOfCountriesWhereMarketServedByTheEntity>

        <in-capmkt:PercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntity contextRef="DCYMain" decimals="INF" unitRef="pure">{{ markets.export_pct }}</in-capmkt:PercentageOfContributionOfExportsInTheTotalTurnoverOfTheEntity>

        <in-capmkt:ABriefOnTypesOfCustomersExplanatoryTextBlock contextRef="DCYMain">{{ markets.customer_types_brief }}</in-capmkt:ABriefOnTypesOfCustomersExplanatoryTextBlock>

        
        <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_PermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.permanent.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_PermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.permanent.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_PermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.permanent.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_PermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.permanent.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_PermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.permanent.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_PermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.permanent.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_PermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.permanent.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

        <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_OtherThanPermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.other.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_OtherThanPermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.other.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_OtherThanPermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.other.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_OtherThanPermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.other.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_OtherThanPermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.other.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_OtherThanPermanentEmployees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.other.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_OtherThanPermanentEmployees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.other.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
    <in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_Employees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.total.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_Employees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.total.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_Employees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.total.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_Employees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.total.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_Employees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.total.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_Employees_TableA" decimals="0" unitRef="pure">{{ emp_workers.employees.total.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_Employees_TableA" decimals="INF" unitRef="pure">{{ emp_workers.employees.total.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_PermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.permanent.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_PermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.permanent.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_PermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.permanent.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_PermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.permanent.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_PermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.permanent.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_PermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.permanent.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_PermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.permanent.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_OtherThanPermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.other.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_OtherThanPermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.other.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_OtherThanPermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.other.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_OtherThanPermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.other.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_OtherThanPermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.other.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_OtherThanPermanentWorkers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.other.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_OtherThanPermanentWorkers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.other.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Gender_Workers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.total.total|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_Workers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.total.male|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Male_Workers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.total.male_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_Workers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.total.female|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_Female_Workers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.total.female_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_Workers_TableA" decimals="0" unitRef="pure">{{ emp_workers.workers.total.other|int }}</in-capmkt:NumberOfEmployeesOrWorkersIncludingDifferentlyAbled>
<in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled contextRef="D_OtherGender_Workers_TableA" decimals="INF" unitRef="pure">{{ emp_workers.workers.total.other_pct }}</in-capmkt:PercentageOfEmployeesOrWorkersIncludingDifferentlyAbled>

<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_PermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_PermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_PermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_PermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_PermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_PermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_PermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.permanent.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_OtherThanPermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.other.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_OtherThanPermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.other.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_OtherThanPermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.other.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_OtherThanPermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.other.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_OtherThanPermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.other.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_OtherThanPermanentEmployees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.other.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_OtherThanPermanentEmployees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.other.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_Employees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.total.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_Employees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.total.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_Employees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.total.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_Employees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.total.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_Employees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.total.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_Employees_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_employees.total.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_Employees_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_employees.total.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_PermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_PermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_PermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_PermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_PermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_PermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_PermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.permanent.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_OtherThanPermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.other.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_OtherThanPermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.other.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_OtherThanPermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.other.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_OtherThanPermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.other.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_OtherThanPermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.other.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_OtherThanPermanentWorkers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.other.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_OtherThanPermanentWorkers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.other.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Gender_Workers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.total.total|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_Workers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.total.male|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Male_Workers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.total.male_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_Workers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.total.female|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_Female_Workers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.total.female_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_Workers_TableB" decimals="0" unitRef="pure">{{ emp_workers.differently_abled_workers.total.other|int }}</in-capmkt:NumberOfDifferentlyAbledEmployeesOrWorkers>
<in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers contextRef="D_OtherGender_Workers_TableB" decimals="INF" unitRef="pure">{{ emp_workers.differently_abled_workers.total.other_pct }}</in-capmkt:PercentageOfDifferentlyAbledEmployeesOrWorkers>

<in-capmkt:TotalNumberOfBoardOfDirectors contextRef="DCYMain" decimals="0" unitRef="pure">{{ women_rep.board.total|int }}</in-capmkt:TotalNumberOfBoardOfDirectors>
<in-capmkt:NumberOfFemaleBoardOfDirectors contextRef="DCYMain" decimals="0" unitRef="pure">{{ women_rep.board.female|int }}</in-capmkt:NumberOfFemaleBoardOfDirectors>
<in-capmkt:PercentageOfFemaleBoardOfDirectors contextRef="DCYMain" decimals="INF" unitRef="pure">{{ women_rep.board.pct }}</in-capmkt:PercentageOfFemaleBoardOfDirectors>
<in-capmkt:TotalNumberOfKeyManagementPersonnel contextRef="DCYMain" decimals="0" unitRef="pure">{{ women_rep.kmp.total|int }}</in-capmkt:TotalNumberOfKeyManagementPersonnel>
<in-capmkt:NumberOfFemaleKeyManagementPersonnel contextRef="DCYMain" decimals="0" unitRef="pure">{{ women_rep.kmp.female|int }}</in-capmkt:NumberOfFemaleKeyManagementPersonnel>
<in-capmkt:PercentageOfFemaleKeyManagementPersonnel contextRef="DCYMain" decimals="INF" unitRef="pure">{{ women_rep.kmp.pct }}</in-capmkt:PercentageOfFemaleKeyManagementPersonnel>

<in-capmkt:TurnoverRate contextRef="D_Male_PermanentEmployees_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.cy.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentEmployees_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.cy.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentEmployees_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.cy.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentEmployees_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.cy.total }}</in-capmkt:TurnoverRate>

<in-capmkt:TurnoverRate contextRef="D_Male_PermanentEmployees_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.py.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentEmployees_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.py.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentEmployees_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.py.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentEmployees_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.py.total }}</in-capmkt:TurnoverRate>

<in-capmkt:TurnoverRate contextRef="D_Male_PermanentEmployees_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.ppy.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentEmployees_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.ppy.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentEmployees_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.ppy.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentEmployees_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.employees.ppy.total }}</in-capmkt:TurnoverRate>

<in-capmkt:TurnoverRate contextRef="D_Male_PermanentWorkers_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.cy.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentWorkers_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.cy.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentWorkers_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.cy.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentWorkers_TableB_TurnOverRate_CY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.cy.total }}</in-capmkt:TurnoverRate>

<in-capmkt:TurnoverRate contextRef="D_Male_PermanentWorkers_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.py.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentWorkers_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.py.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentWorkers_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.py.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentWorkers_TableB_TurnOverRate_PY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.py.total }}</in-capmkt:TurnoverRate>

<in-capmkt:TurnoverRate contextRef="D_Male_PermanentWorkers_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.ppy.male }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Female_PermanentWorkers_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.ppy.female }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_OtherGender_PermanentWorkers_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.ppy.other }}</in-capmkt:TurnoverRate>
<in-capmkt:TurnoverRate contextRef="D_Gender_PermanentWorkers_TableB_TurnOverRate_PPY" decimals="INF" unitRef="pure">{{ turnover_rates.workers.ppy.total }}</in-capmkt:TurnoverRate>

{% for sub in subsidiaries %}
<in-capmkt:NameOfTheHoldingOrSubsidiaryAssociateCompaniesOrJointVentures contextRef="D_HoldingSubsidiaryAssociateCompaniesAndJointVentures{{ loop.index }}">{{ sub.name }}</in-capmkt:NameOfTheHoldingOrSubsidiaryAssociateCompaniesOrJointVentures>
<in-capmkt:CategoryOfCompany contextRef="D_HoldingSubsidiaryAssociateCompaniesAndJointVentures{{ loop.index }}">{{ sub.category }}</in-capmkt:CategoryOfCompany>
<in-capmkt:PercentageOfSharesHeldByListedEntity contextRef="D_HoldingSubsidiaryAssociateCompaniesAndJointVentures{{ loop.index }}" decimals="INF" unitRef="pure">{{ sub.shares_pct }}</in-capmkt:PercentageOfSharesHeldByListedEntity>
<in-capmkt:DoesCompanyParticipateInTheBusinessResponsibilityInitiativesOfTheListedEntity contextRef="D_HoldingSubsidiaryAssociateCompaniesAndJointVentures{{ loop.index }}">{{ 'true' if sub.participates == 'Yes' else 'false' }}</in-capmkt:DoesCompanyParticipateInTheBusinessResponsibilityInitiativesOfTheListedEntity>
{% endfor %}

<in-capmkt:WhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013 contextRef="DCYMain">{{ csr.applicable }}</in-capmkt:WhetherCSRIsApplicableAsPerSection135OfCompaniesAct2013>
<in-capmkt:Turnover contextRef="DCYMain" decimals="1" unitRef="INR">{{ csr.turnover }}</in-capmkt:Turnover>
<in-capmkt:NetWorth contextRef="DCYMain" decimals="2" unitRef="INR">{{ csr.net_worth }}</in-capmkt:NetWorth>

{% for project in csr.aspirational_districts %}
<in-capmkt:StateOfCSRProjectsUndertaken contextRef="{{ project.axis_id }}">{{ project.state }}</in-capmkt:StateOfCSRProjectsUndertaken>
<in-capmkt:AspirationalDistrictOfCSRProjectsUndertaken contextRef="{{ project.axis_id }}">{{ project.aspirational_district }}</in-capmkt:AspirationalDistrictOfCSRProjectsUndertaken>
<in-capmkt:AmountSpentForCSRProjectsUndertaken contextRef="{{ project.axis_id }}" decimals="0" unitRef="INR">{{ project.amount_spent }}</in-capmkt:AmountSpentForCSRProjectsUndertaken>
{% endfor %}

{% for p in section_b %}
<in-capmkt:WhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs contextRef="D_Principle{{ p.num }}">{{ p.policy_covers }}</in-capmkt:WhetherYourEntitysPolicyOrPoliciesCoverEachPrincipleAndItsCoreElementsOfTheNGRBCs>
{% endfor %}

{% for p in section_b %}
<in-capmkt:HasThePolicyBeenApprovedByTheBoard contextRef="D_Principle{{ p.num }}">{{ p.board_approved }}</in-capmkt:HasThePolicyBeenApprovedByTheBoard>
{% endfor %}

{% for p in section_b %}
<in-capmkt:WebLinkOfThePoliciesExplanatoryTextBlock contextRef="D_Principle{{ p.num }}">{{ p.web_link }}</in-capmkt:WebLinkOfThePoliciesExplanatoryTextBlock>
{% endfor %}

{% for p in section_b %}
<in-capmkt:WhetherTheEntityHasTranslatedThePolicyIntoProcedures contextRef="D_Principle{{ p.num }}">{{ p.translated_to_procedures }}</in-capmkt:WhetherTheEntityHasTranslatedThePolicyIntoProcedures>
{% endfor %}

{% for p in section_b %}
<in-capmkt:DoTheEnlistedPoliciesExtendToYourValueChainPartners contextRef="D_Principle{{ p.num }}">{{ p.extends_to_value_chain }}</in-capmkt:DoTheEnlistedPoliciesExtendToYourValueChainPartners>
{% endfor %}

{% for p in section_b %}
<in-capmkt:NameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrincipleExplanatoryTextBlock contextRef="D_Principle{{ p.num }}">{{ p.codes_certifications if p.codes_certifications else 'NA' }}</in-capmkt:NameOfTheNationalAndInternationalCodesOrCertificationsOrLabelsOrStandardsAdoptedByYourEntityAndMappedToEachPrincipleExplanatoryTextBlock>
{% endfor %}

{% for p in section_b %}
<in-capmkt:SpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelinesExplanatoryTextBlock contextRef="D_Principle{{ p.num }}">{{ p.commitments_goals if p.commitments_goals else 'NA' }}</in-capmkt:SpecificCommitmentsGoalsAndTargetsSetByTheEntityWithDefinedTimelinesExplanatoryTextBlock>
{% endfor %}

{% for p in section_b %}
<in-capmkt:PerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMetExplanatoryTextBlock contextRef="D_Principle{{ p.num }}">{{ p.performance if p.performance else 'NA' }}</in-capmkt:PerformanceOfTheEntityAgainstTheSpecificCommitmentsGoalsAndTargetsAlongWithReasonsInCaseTheSameAreNotMetExplanatoryTextBlock>

            <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.male.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.male.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.female.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.female.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.other.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.other.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.total.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.total.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

            <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.male.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.male.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.male.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.female.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.female.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.female.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.other.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.other.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.other.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.total.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_emp.total.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_emp.total.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

            <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.male.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.male.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.female.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.female.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.other.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.other.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.total.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.total.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

            <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.male.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.male.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.male.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.female.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.female.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.female.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.other.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.other.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.other.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.total.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_emp.total.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_emp.total.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

            <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.male.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.male.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.female.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.female.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.other.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.other.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.total.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_W" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_W" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.total.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

            <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.male.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.male.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.male.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.female.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.female.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.female.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.other.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.other.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.other.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.total.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.perm_workers.total.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.perm_workers.total.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

            <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.male.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.male.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.female.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.female.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.other.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.other.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.total_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.equal_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.total.equal_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_W" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.more_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_W" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.total.more_pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

            <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_1_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_1_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.male.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.male.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_1_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.male.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_2_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_2_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.female.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.female.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_2_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.female.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_3_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_3_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.other.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.other.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_3_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.other.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
        <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_Total_4_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.total_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.equal_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_EqualToMinimumWage_4_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.total.equal_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_W_PY" decimals="0" unitRef="pure">{{ minimum_wages.other_workers.total.more_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersRelatedToMinimumWages>
    <in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages contextRef="D_MoreThanMinimumWage_4_Other_W_PY" decimals="INF" unitRef="pure">{{ minimum_wages.other_workers.total.more_pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersRelatedToMinimumWages>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

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

        <in-capmkt:GrossWagesPaidToFemale contextRef="DCYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.female_cy }}</in-capmkt:GrossWagesPaidToFemale>
    <in-capmkt:GrossWagesPaidToFemale contextRef="DPYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.female_py }}</in-capmkt:GrossWagesPaidToFemale>
    <in-capmkt:TotalWagesPaid contextRef="DCYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.total_cy }}</in-capmkt:TotalWagesPaid>
    <in-capmkt:TotalWagesPaid contextRef="DPYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.total_py }}</in-capmkt:TotalWagesPaid>
    <in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.gross_wages.female_pct_cy }}</in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid>
    <in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid contextRef="DPYMain" decimals="INF" unitRef="pure">{{ human_rights_data.gross_wages.female_pct_py }}</in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid>
    <in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear contextRef="DCYMain" decimals="0" unitRef="pure">{{ human_rights_data.gross_wages.avg_female_emp_workers_cy | int }}</in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear>
    <in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear contextRef="DPYMain" decimals="0" unitRef="pure">{{ human_rights_data.gross_wages.avg_female_emp_workers_py | int }}</in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear>

        <in-capmkt:DoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness contextRef="DCYMain">{{ human_rights_data.focal_point }}</in-capmkt:DoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness>
    <in-capmkt:DetailsOfFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusinessExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.focal_point_details | e }}</in-capmkt:DetailsOfFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusinessExplanatoryTextBlock>
    <in-capmkt:DescribeTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.internal_mechanisms | e }}</in-capmkt:DescribeTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesExplanatoryTextBlock>
    <in-capmkt:DoHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts contextRef="DCYMain">{{ human_rights_data.hr_in_contracts }}</in-capmkt:DoHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_employees.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentEmployees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentEmployees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_employees.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Employees_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_employees.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.covered_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_workers.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_PermanentWorkers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.permanent_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.other_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_OtherThanPermanentWorkers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.other_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

    <in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForTrainingOnHumanRightsIssues>
    <in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="0" unitRef="pure">{{ human_rights_data.hr_training.total_workers.covered_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>
    <in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues contextRef="D_Workers_p5_PY" decimals="INF" unitRef="pure">{{ human_rights_data.hr_training.total_workers.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersCoveredForProvidedTrainingOnHumanRightsIssues>

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

        <in-capmkt:GrossWagesPaidToFemale contextRef="DCYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.female_cy }}</in-capmkt:GrossWagesPaidToFemale>
    <in-capmkt:GrossWagesPaidToFemale contextRef="DPYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.female_py }}</in-capmkt:GrossWagesPaidToFemale>
    <in-capmkt:TotalWagesPaid contextRef="DCYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.total_cy }}</in-capmkt:TotalWagesPaid>
    <in-capmkt:TotalWagesPaid contextRef="DPYMain" decimals="2" unitRef="INR">{{ human_rights_data.gross_wages.total_py }}</in-capmkt:TotalWagesPaid>
    <in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.gross_wages.female_pct_cy }}</in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid>
    <in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid contextRef="DPYMain" decimals="INF" unitRef="pure">{{ human_rights_data.gross_wages.female_pct_py }}</in-capmkt:PercentageOfGrossWagesPaidToFemaleToTotalWagesPaid>
    <in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear contextRef="DCYMain" decimals="0" unitRef="pure">{{ human_rights_data.gross_wages.avg_female_emp_workers_cy | int }}</in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear>
    <in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear contextRef="DPYMain" decimals="0" unitRef="pure">{{ human_rights_data.gross_wages.avg_female_emp_workers_py | int }}</in-capmkt:AverageNumberOfFemaleEmployeesOrWorkersAtTheBeginningOfTheYearAndAsAtEndOfTheYear>

        <in-capmkt:DoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness contextRef="DCYMain">{{ human_rights_data.focal_point }}</in-capmkt:DoYouHaveAFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusiness>
    <in-capmkt:DetailsOfFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusinessExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.focal_point_details | e }}</in-capmkt:DetailsOfFocalPointResponsibleForAddressingHumanRightsImpactsOrIssuesCausedOrContributedToByTheBusinessExplanatoryTextBlock>
    <in-capmkt:DescribeTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.internal_mechanisms | e }}</in-capmkt:DescribeTheInternalMechanismsInPlaceToRedressGrievancesRelatedToHumanRightsIssuesExplanatoryTextBlock>
    <in-capmkt:DoHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts contextRef="DCYMain">{{ human_rights_data.hr_in_contracts }}</in-capmkt:DoHumanRightsRequirementsFormPartOfYourBusinessAgreementsAndContracts>

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

        <in-capmkt:TotalComplaintsReportedUnderSexualHarassmentOfWomenAtWorkplace contextRef="DCYMain" decimals="0" unitRef="pure">{{ human_rights_data.posh.total_complaints_cy | int }}</in-capmkt:TotalComplaintsReportedUnderSexualHarassmentOfWomenAtWorkplace>
    <in-capmkt:TotalComplaintsReportedUnderSexualHarassmentOfWomenAtWorkplace contextRef="DPYMain" decimals="0" unitRef="pure">{{ human_rights_data.posh.total_complaints_py | int }}</in-capmkt:TotalComplaintsReportedUnderSexualHarassmentOfWomenAtWorkplace>
    <in-capmkt:PercentageOfComplaintsInRespectOfNumberOfEmployeesOrWorker contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.posh.pct_complaints_cy }}</in-capmkt:PercentageOfComplaintsInRespectOfNumberOfEmployeesOrWorker>
    <in-capmkt:PercentageOfComplaintsInRespectOfNumberOfEmployeesOrWorker contextRef="DPYMain" decimals="INF" unitRef="pure">{{ human_rights_data.posh.pct_complaints_py }}</in-capmkt:PercentageOfComplaintsInRespectOfNumberOfEmployeesOrWorker>
    <in-capmkt:ComplaintsOnPOSHUpHeld contextRef="DCYMain" decimals="0" unitRef="pure">{{ human_rights_data.posh.upheld_cy | int }}</in-capmkt:ComplaintsOnPOSHUpHeld>
    <in-capmkt:ComplaintsOnPOSHUpHeld contextRef="DPYMain" decimals="0" unitRef="pure">{{ human_rights_data.posh.upheld_py | int }}</in-capmkt:ComplaintsOnPOSHUpHeld>
    <in-capmkt:MechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCasesExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.mechanisms_prevent_adverse | e }}</in-capmkt:MechanismsToPreventAdverseConsequencesToTheComplainantInDiscriminationAndHarassmentCasesExplanatoryTextBlock>

        <in-capmkt:PercentageOfChildLabourOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.child_labour }}</in-capmkt:PercentageOfChildLabourOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:PercentageOfForcedLabourOrInvoluntaryLabourOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.forced_labour }}</in-capmkt:PercentageOfForcedLabourOrInvoluntaryLabourOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:PercentageOfSexualHarassmentOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.sexual_harassment }}</in-capmkt:PercentageOfSexualHarassmentOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:PercentageOfDiscriminationAtWorkPlaceOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.discrimination }}</in-capmkt:PercentageOfDiscriminationAtWorkPlaceOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:PercentageOfWagesOfYourPlantsAndOfficesThatWereAssessedP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.plant_assessments.wages }}</in-capmkt:PercentageOfWagesOfYourPlantsAndOfficesThatWereAssessedP5>
    <in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOfficeExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.corrective_actions_plants | e }}</in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfPlantAndOfficeExplanatoryTextBlock>

        <in-capmkt:NameOfOtherAssessmentsOfPlantAndOffice contextRef="D_OtherAssessments12">{{ human_rights_data.other_assessments_plants.name | e }}</in-capmkt:NameOfOtherAssessmentsOfPlantAndOffice>
    <in-capmkt:PercentageOfOtherAssessmentsOfPlantAndOffice contextRef="D_OtherAssessments12" decimals="INF" unitRef="pure">{{ human_rights_data.other_assessments_plants.percentage }}</in-capmkt:PercentageOfOtherAssessmentsOfPlantAndOffice>

        <in-capmkt:PercentageOfChildLabourOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.child_labour }}</in-capmkt:PercentageOfChildLabourOfValueChainPartnersP5>
    <in-capmkt:PercentageOfForcedLabourOrInvoluntaryLabourOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.forced_labour }}</in-capmkt:PercentageOfForcedLabourOrInvoluntaryLabourOfValueChainPartnersP5>
    <in-capmkt:PercentageOfSexualHarassmentOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.sexual_harassment }}</in-capmkt:PercentageOfSexualHarassmentOfValueChainPartnersP5>
    <in-capmkt:PercentageOfDiscriminationAtWorkPlaceOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.discrimination }}</in-capmkt:PercentageOfDiscriminationAtWorkPlaceOfValueChainPartnersP5>
    <in-capmkt:PercentageOfWagesOfValueChainPartnersP5 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ human_rights_data.value_chain_assessments.wages }}</in-capmkt:PercentageOfWagesOfValueChainPartnersP5>
    <in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartnerExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.corrective_actions_value_chain | e }}</in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayToAddressSignificantRisksOrConcernsArisingFromTheAssessmentsOfValueChainPartnerExplanatoryTextBlock>

        <in-capmkt:NameOfOtherAssessmentOfValueChainPartner contextRef="D_OtherAssessmentOfValueChainPartners12">{{ human_rights_data.other_assessments_value_chain.name | e }}</in-capmkt:NameOfOtherAssessmentOfValueChainPartner>
    <in-capmkt:PercentageOfOtherAssessmentOfValueChainPartner contextRef="D_OtherAssessmentOfValueChainPartners12" decimals="INF" unitRef="pure">{{ human_rights_data.other_assessments_value_chain.percentage }}</in-capmkt:PercentageOfOtherAssessmentOfValueChainPartner>

        <in-capmkt:DetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaintsExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.business_process_modified | e }}</in-capmkt:DetailsOfABusinessProcessBeingModifiedOrIntroducedAsAResultOfAddressingHumanRightsGrievancesOrComplaintsExplanatoryTextBlock>
    <in-capmkt:DetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConductedExplanatoryTextBlock contextRef="DCYMain">{{ human_rights_data.hr_due_diligence | e }}</in-capmkt:DetailsOfTheScopeAndCoverageOfAnyHumanRightsDueDiligenceConductedExplanatoryTextBlock>
    <in-capmkt:IsThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">{{ 'true' if human_rights_data.differently_abled_accessible == 'Yes' else 'false' }}</in-capmkt:IsThePremiseOrOfficeOfTheEntityAccessibleToDifferentlyAbledVisitorsAsPerTheRequirementsOfTheRightsOfPersonsWithDisabilitiesAct2016>

            <in-capmkt:WhetherDetailsOfTotalEnergyConsumptionAndEnergyIntensityApplicableToTheCompany contextRef="DCYMain">true</in-capmkt:WhetherDetailsOfTotalEnergyConsumptionAndEnergyIntensityApplicableToTheCompany>

        <in-capmkt:RevenueFromOperations contextRef="DCYMain" decimals="2" unitRef="INR">{{ environment_data.revenue_from_operations_cy }}</in-capmkt:RevenueFromOperations>
    <in-capmkt:RevenueFromOperations contextRef="DPYMain" decimals="2" unitRef="INR">{{ environment_data.revenue_from_operations_py }}</in-capmkt:RevenueFromOperations>

    <in-capmkt:TotalElectricityConsumptionFromRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.elec_renewable_cy }}</in-capmkt:TotalElectricityConsumptionFromRenewableSources>
    <in-capmkt:TotalElectricityConsumptionFromRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.elec_renewable_py }}</in-capmkt:TotalElectricityConsumptionFromRenewableSources>
    <in-capmkt:TotalFuelConsumptionFromRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.fuel_renewable_cy }}</in-capmkt:TotalFuelConsumptionFromRenewableSources>
    <in-capmkt:TotalFuelConsumptionFromRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.fuel_renewable_py }}</in-capmkt:TotalFuelConsumptionFromRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources contextRef="DCYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_renewable_cy }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources>
    <in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources contextRef="DPYMain" decimals="INF" unitRef="Gigajoule">{{ environment_data.energy.other_renewable_py }}</in-capmkt:EnergyConsumptionThroughOtherSourcesFromRenewableSources>

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
        <in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWasteManagement contextRef="DCYMain">{{ environment_data.waste.external_assessment }}</in-capmkt:WhetherAnyIndependentAssessmentOrEvaluationOrAssuranceHasBeenCarriedOutByAnExternalAgencyForWasteManagement>
    <in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceRelatedToWasteManagementExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.waste.external_agency | e }}</in-capmkt:NameOfTheExternalAgencyThatUndertookIndependentAssessmentOrEvaluationOrAssuranceRelatedToWasteManagementExplanatoryTextBlock>
    <in-capmkt:DetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicalsExplanatoryTextBlock contextRef="DCYMain">{{ environment_data.waste.waste_management_practices | e }}</in-capmkt:DetailsOfWasteManagementPracticesAdoptedInYourEstablishmentsAndTheStrategyAdoptedByCompanyToReduceUsageOfHazardousAndToxicChemicalsExplanatoryTextBlock>

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

            <in-capmkt:DescribeTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntityExplanatoryTextBlock contextRef="DCYMain">{{ stakeholder_data.identification_process | e }}</in-capmkt:DescribeTheProcessesForIdentifyingKeyStakeholderGroupsOfTheEntityExplanatoryTextBlock>

        {% for stakeholder in stakeholder_data.stakeholder_groups %}
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

        <in-capmkt:ProvideTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoardExplanatoryTextBlock contextRef="DCYMain">{{ stakeholder_data.consultation_process | e }}</in-capmkt:ProvideTheProcessesForConsultationBetweenStakeholdersAndTheBoardOnEconomicEnvironmentalAndSocialTopicsOrIfConsultationIsDelegatedHowIsFeedbackFromSuchConsultationsProvidedToTheBoardExplanatoryTextBlock>
    <in-capmkt:WhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics contextRef="DCYMain">{{ stakeholder_data.stakeholder_consultation_used if stakeholder_data.stakeholder_consultation_used else 'Yes' }}</in-capmkt:WhetherStakeholderConsultationIsUsedToSupportTheIdentificationAndManagementOfEnvironmentalAndSocialTopics>
    <in-capmkt:DetailsOfInstancesAsToHowTheInputsReceivedFromStakeholdersOnTheseTopicsWereIncorporatedIntoPoliciesAndActivitiesOfTheEntityExplanatoryTextBlock contextRef="DCYMain">{{ stakeholder_data.stakeholder_consultation_details | e if stakeholder_data.stakeholder_consultation_details else '' }}</in-capmkt:DetailsOfInstancesAsToHowTheInputsReceivedFromStakeholdersOnTheseTopicsWereIncorporatedIntoPoliciesAndActivitiesOfTheEntityExplanatoryTextBlock>
    <in-capmkt:ProvideDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableMarginalizedStakeholderGroupsExplanatoryTextBlock contextRef="DCYMain">{{ stakeholder_data.vulnerable_marginalized_actions | e if stakeholder_data.vulnerable_marginalized_actions else 'NA' }}</in-capmkt:ProvideDetailsOfInstancesOfEngagementWithAndActionsTakenToAddressTheConcernsOfVulnerableMarginalizedStakeholderGroupsExplanatoryTextBlock>

<in-capmkt:StatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievementsExplanatoryTextBlock contextRef="DCYMain">{{ governance.director_statement | e }}</in-capmkt:StatementByDirectorResponsibleForTheBusinessResponsibilityReportHighlightingESGRelatedChallengesTargetsAndAchievementsExplanatoryTextBlock>

<in-capmkt:DetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicyExplanatoryTextBlock contextRef="DCYMain">{{ governance.highest_authority | e }}</in-capmkt:DetailsOfTheHighestAuthorityResponsibleForImplementationAndOversightOfTheBusinessResponsibilityPolicyExplanatoryTextBlock>

<in-capmkt:DoesTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues contextRef="DCYMain">{{ governance.has_esg_committee }}</in-capmkt:DoesTheEntityHaveASpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssues>
<in-capmkt:DetailsOfSpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssuesExplanatoryTextBlock contextRef="DCYMain">{{ governance.esg_committee | e }}</in-capmkt:DetailsOfSpecifiedCommitteeOfTheBoardOrDirectorResponsibleForDecisionMakingOnSustainabilityRelatedIssuesExplanatoryTextBlock>

{% for p in governance.principles %}
<in-capmkt:PerformanceAgainstAbovePoliciesAndFollowUpActionIndicateWhetherReviewWasUndertakenBy contextRef="D_Principle{{ loop.index }}">{{ p.performance_review_by }}</in-capmkt:PerformanceAgainstAbovePoliciesAndFollowUpActionIndicateWhetherReviewWasUndertakenBy>
{% endfor %}

{% for p in governance.principles %}
<in-capmkt:ComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesIndicateWhetherReviewWasUndertakenBy contextRef="D_Principle{{ loop.index }}">{{ p.compliance_review_by }}</in-capmkt:ComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesIndicateWhetherReviewWasUndertakenBy>
{% endfor %}

{% for p in governance.principles %}
<in-capmkt:PerformanceAgainstAbovePoliciesAndFollowUpActionFrequency contextRef="D_Principle{{ loop.index }}">{{ p.performance_frequency }}</in-capmkt:PerformanceAgainstAbovePoliciesAndFollowUpActionFrequency>
{% endfor %}

{% for p in governance.principles %}
<in-capmkt:DescriptionOfOtherFrequencyForPerformanceAgainstAbovePoliciesAndFollowUpAction contextRef="D_Principle{{ loop.index }}">{{ p.performance_frequency_other }}</in-capmkt:DescriptionOfOtherFrequencyForPerformanceAgainstAbovePoliciesAndFollowUpAction>
{% endfor %}

{% for p in governance.principles %}
<in-capmkt:ComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesFrequency contextRef="D_Principle{{ loop.index }}">{{ p.compliance_frequency }}</in-capmkt:ComplianceWithStatutoryRequirementsOfRelevanceToThePrinciplesAndRectificationOfAnyNonCompliancesFrequency>
{% endfor %}

{% for p in governance.principles %}
<in-capmkt:HasTheEntityCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency contextRef="D_Principle{{ loop.index }}">{{ p.independent_assessment }}</in-capmkt:HasTheEntityCarriedOutIndependentAssessmentEvaluationOfTheWorkingOfItsPoliciesByAnExternalAgency>
{% endfor %}

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

<in-capmkt:NGRBCPrincipleForPenaltyOrFine contextRef="D_PenaltyOrFine1">{{ fines_penalties.penalty_fine.ngrbc }}</in-capmkt:NGRBCPrincipleForPenaltyOrFine>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForPenaltyOrFine contextRef="D_PenaltyOrFine1">{{ fines_penalties.penalty_fine.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForPenaltyOrFine>
<in-capmkt:AmountOfFinesOrPenalties contextRef="D_PenaltyOrFine1" decimals="0" unitRef="INR">{{ fines_penalties.penalty_fine.amount }}</in-capmkt:AmountOfFinesOrPenalties>
<in-capmkt:BriefOfTheMonetaryCaseForPenaltyOrFineExplanatoryTextBlock contextRef="D_PenaltyOrFine1">{{ fines_penalties.penalty_fine.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForPenaltyOrFineExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForPenaltyOrFine contextRef="D_PenaltyOrFine1">{{ fines_penalties.penalty_fine.appeal }}</in-capmkt:HasAnAppealBeenPreferredForPenaltyOrFine>

<in-capmkt:NGRBCPrincipleForSettlement contextRef="D_Settlement1">{{ fines_penalties.settlement.ngrbc }}</in-capmkt:NGRBCPrincipleForSettlement>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForSettlement contextRef="D_Settlement1">{{ fines_penalties.settlement.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForSettlement>
<in-capmkt:AmountOfSettlement contextRef="D_Settlement1" decimals="0" unitRef="INR">{{ fines_penalties.settlement.amount }}</in-capmkt:AmountOfSettlement>
<in-capmkt:BriefOfTheMonetaryCaseForSettlementExplanatoryTextBlock contextRef="D_Settlement1">{{ fines_penalties.settlement.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForSettlementExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForSettlement contextRef="D_Settlement1">{{ fines_penalties.settlement.appeal }}</in-capmkt:HasAnAppealBeenPreferredForSettlement>

<in-capmkt:NGRBCPrincipleForCompoundingFee contextRef="D_Compounding1">{{ fines_penalties.compounding.ngrbc }}</in-capmkt:NGRBCPrincipleForCompoundingFee>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForCompoundingFee contextRef="D_Compounding1">{{ fines_penalties.compounding.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForCompoundingFee>
<in-capmkt:AmountOfCompoundingFee contextRef="D_Compounding1" decimals="0" unitRef="INR">{{ fines_penalties.compounding.amount }}</in-capmkt:AmountOfCompoundingFee>
<in-capmkt:BriefOfTheMonetaryCaseForCompoundingFeeExplanatoryTextBlock contextRef="D_Compounding1">{{ fines_penalties.compounding.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForCompoundingFeeExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForCompoundingFee contextRef="D_Compounding1">{{ fines_penalties.compounding.appeal }}</in-capmkt:HasAnAppealBeenPreferredForCompoundingFee>

<in-capmkt:NGRBCPrincipleForImprisonment contextRef="D_Imprisonment1">{{ fines_penalties.imprisonment.ngrbc }}</in-capmkt:NGRBCPrincipleForImprisonment>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForImprisonment contextRef="D_Imprisonment1">{{ fines_penalties.imprisonment.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForImprisonment>
<in-capmkt:BriefOfTheMonetaryCaseForImprisonmentExplanatoryTextBlock contextRef="D_Imprisonment1">{{ fines_penalties.imprisonment.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForImprisonmentExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForImprisonment contextRef="D_Imprisonment1">{{ fines_penalties.imprisonment.appeal }}</in-capmkt:HasAnAppealBeenPreferredForImprisonment>

<in-capmkt:NGRBCPrincipleForPunishment contextRef="D_Punishment1">{{ fines_penalties.punishment.ngrbc }}</in-capmkt:NGRBCPrincipleForPunishment>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForPunishment contextRef="D_Punishment1">{{ fines_penalties.punishment.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutionsForPunishment>
<in-capmkt:BriefOfTheMonetaryCaseForPunishmentExplanatoryTextBlock contextRef="D_Punishment1">{{ fines_penalties.punishment.brief | e }}</in-capmkt:BriefOfTheMonetaryCaseForPunishmentExplanatoryTextBlock>
<in-capmkt:HasAnAppealBeenPreferredForPunishment contextRef="D_Punishment1">{{ fines_penalties.punishment.appeal }}</in-capmkt:HasAnAppealBeenPreferredForPunishment>

<in-capmkt:DetailsOfTheCase contextRef="D_AppealOrRevision1">{{ fines_penalties.appeal_revision.details }}</in-capmkt:DetailsOfTheCase>
<in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutions contextRef="D_AppealOrRevision1">{{ fines_penalties.appeal_revision.agency }}</in-capmkt:NameOfTheRegulatoryOrEnforcementAgenciesOrJudicialInstitutions>

<in-capmkt:DoesTheEntityHaveAnAntiCorruptionOrAntiBriberyPolicy contextRef="DCYMain">{{ fines_penalties.anti_corruption.has_policy }}</in-capmkt:DoesTheEntityHaveAnAntiCorruptionOrAntiBriberyPolicy>
<in-capmkt:AntiCorruptionOrAntiBriberyPolicyExplanatoryTextBlock contextRef="DCYMain">{{ fines_penalties.anti_corruption.policy_details | e }}</in-capmkt:AntiCorruptionOrAntiBriberyPolicyExplanatoryTextBlock>
<in-capmkt:WebLinkAtAntiCorruptionOrAntiBriberyPolicyIsPlace contextRef="ICYMain">{{ fines_penalties.anti_corruption.web_link }}</in-capmkt:WebLinkAtAntiCorruptionOrAntiBriberyPolicyIsPlace>

<in-capmkt:NumberOfDirectorsAgainstWhomDisciplinaryActionWasTaken contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_cy.directors }}</in-capmkt:NumberOfDirectorsAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfDirectorsAgainstWhomDisciplinaryActionWasTaken contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_py.directors }}</in-capmkt:NumberOfDirectorsAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfKMPsAgainstWhomDisciplinaryActionWasTaken contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_cy.kmps }}</in-capmkt:NumberOfKMPsAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfKMPsAgainstWhomDisciplinaryActionWasTaken contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_py.kmps }}</in-capmkt:NumberOfKMPsAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfEmployeesAgainstWhomDisciplinaryActionWasTaken contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_cy.employees }}</in-capmkt:NumberOfEmployeesAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfEmployeesAgainstWhomDisciplinaryActionWasTaken contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_py.employees }}</in-capmkt:NumberOfEmployeesAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfWorkersAgainstWhomDisciplinaryActionWasTaken contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_cy.workers }}</in-capmkt:NumberOfWorkersAgainstWhomDisciplinaryActionWasTaken>
<in-capmkt:NumberOfWorkersAgainstWhomDisciplinaryActionWasTaken contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.disciplinary_py.workers }}</in-capmkt:NumberOfWorkersAgainstWhomDisciplinaryActionWasTaken>

<in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.conflict_directors_cy.number }}</in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors>
<in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors contextRef="DCYMain">{{ fines_penalties.conflict_directors_cy.remarks }}</in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors>
<in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.conflict_directors_py.number }}</in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors>
<in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors contextRef="DPYMain">{{ fines_penalties.conflict_directors_py.remarks }}</in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheDirectors>
<in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKMPs contextRef="DCYMain" decimals="0" unitRef="pure">{{ fines_penalties.conflict_kmps_cy.number }}</in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKMPs>
<in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKmps contextRef="DCYMain">{{ fines_penalties.conflict_kmps_cy.remarks }}</in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKmps>
<in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKMPs contextRef="DPYMain" decimals="0" unitRef="pure">{{ fines_penalties.conflict_kmps_py.number }}</in-capmkt:NumberOfComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKMPs>
<in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKmps contextRef="DPYMain">{{ fines_penalties.conflict_kmps_py.remarks }}</in-capmkt:RemarksInCaseComplaintsReceivedInRelationToIssuesOfConflictOfInterestOfTheKmps>

<in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterestExplanatoryTextBlock contextRef="DCYMain">{{ fines_penalties.corrective_action }}</in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayOnIssuesRelatedToFinesOrPenaltiesOrActionTakenByRegulatorsOrLawEnforcementAgenciesOrJudicialInstitutionsOnCasesOfCorruptionAndConflictsOfInterestExplanatoryTextBlock>

<in-capmkt:DoesTheEntityHaveProcessesInPlaceToAvoidOrManageConflictOfInterestsInvolvingMembersOfTheBoard contextRef="DCYMain">{{ fines_penalties.conflict_process.has_process }}</in-capmkt:DoesTheEntityHaveProcessesInPlaceToAvoidOrManageConflictOfInterestsInvolvingMembersOfTheBoard>
<in-capmkt:DetailsOfTheEntityHaveProcessesInPlaceToAvoidOrManageConflictOfInterestsInvolvingMembersOfTheBoardExplanatoryTextBlock contextRef="DCYMain">{{ fines_penalties.conflict_process.details | e }}</in-capmkt:DetailsOfTheEntityHaveProcessesInPlaceToAvoidOrManageConflictOfInterestsInvolvingMembersOfTheBoardExplanatoryTextBlock>

<in-capmkt:TotalNumberOfAwarenessProgrammesHeld contextRef="D_AwarenessProgrammesConductedForValueChainPartners1" decimals="0" unitRef="pure">{{ sustainability.value_chain_awareness.count }}</in-capmkt:TotalNumberOfAwarenessProgrammesHeld>
<in-capmkt:TopicsOrPrinciplesCoveredUnderTheTraining contextRef="D_AwarenessProgrammesConductedForValueChainPartners1">{{ sustainability.value_chain_awareness.topics | e }}</in-capmkt:TopicsOrPrinciplesCoveredUnderTheTraining>
<in-capmkt:PercentageOfValueChainPartnersCoveredUnderTheAwarenessProgrammes contextRef="D_AwarenessProgrammesConductedForValueChainPartners1" decimals="INF" unitRef="pure">{{ sustainability.value_chain_awareness.coverage }}</in-capmkt:PercentageOfValueChainPartnersCoveredUnderTheAwarenessProgrammes>

<in-capmkt:PercentageOfRAndD contextRef="DCYMain" decimals="INF" unitRef="pure">{{ sustainability.rd_cy }}</in-capmkt:PercentageOfRAndD>
<in-capmkt:PercentageOfRAndD contextRef="DPYMain" decimals="INF" unitRef="pure">{{ sustainability.rd_py }}</in-capmkt:PercentageOfRAndD>
<in-capmkt:DetailsOfImprovementsInEnvironmentalAndSocialImpactsDueToRAndD contextRef="DCYMain">{{ sustainability.rd_improvements | e }}</in-capmkt:DetailsOfImprovementsInEnvironmentalAndSocialImpactsDueToRAndD>

<in-capmkt:PercentageOfCapex contextRef="DCYMain" decimals="INF" unitRef="pure">{{ sustainability.capex_cy }}</in-capmkt:PercentageOfCapex>
<in-capmkt:PercentageOfCapex contextRef="DPYMain" decimals="INF" unitRef="pure">{{ sustainability.capex_py }}</in-capmkt:PercentageOfCapex>
<in-capmkt:DetailsOfImprovementsInEnvironmentalAndSocialImpactsDueToCapex contextRef="DCYMain">{{ sustainability.capex_improvements | e }}</in-capmkt:DetailsOfImprovementsInEnvironmentalAndSocialImpactsDueToCapex>

<in-capmkt:DoesTheEntityHaveProceduresInPlaceForSustainableSourcing contextRef="DCYMain">{{ sustainability.has_sustainable_sourcing }}</in-capmkt:DoesTheEntityHaveProceduresInPlaceForSustainableSourcing>
<in-capmkt:PercentageOfInputsWereSourcedSustainably contextRef="DCYMain" decimals="INF" unitRef="pure">{{ sustainability.sustainable_sourcing_pct }}</in-capmkt:PercentageOfInputsWereSourcedSustainably>

<in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingExplanatoryTextBlock contextRef="DCYMain">{{ sustainability.eol_plastics | e }}</in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForPlasticsIncludingPackagingExplanatoryTextBlock>
<in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForEWasteExplanatoryTextBlock contextRef="DCYMain">{{ sustainability.eol_ewaste | e }}</in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForEWasteExplanatoryTextBlock>
<in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForHazardousWasteExplanatoryTextBlock contextRef="DCYMain">{{ sustainability.eol_hazardous | e }}</in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForHazardousWasteExplanatoryTextBlock>
<in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForOtherWasteExplanatoryTextBlock contextRef="DCYMain">{{ sustainability.eol_other | e }}</in-capmkt:DescribeTheProcessesInPlaceToSafelyReclaimYourProductsForReusingRecyclingAndDisposingAtTheEndOfLifeForOtherWasteExplanatoryTextBlock>

<in-capmkt:WhetherExtendedProducerResponsibilityIsApplicableToTheEntitySActivities contextRef="DCYMain">{{ sustainability.epr_applicable }}</in-capmkt:WhetherExtendedProducerResponsibilityIsApplicableToTheEntitySActivities>
<in-capmkt:WhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoards contextRef="DCYMain">{{ sustainability.epr_waste_plan_aligned }}</in-capmkt:WhetherTheWasteCollectionPlanIsInLineWithTheExtendedProducerResponsibilityPlanSubmittedToPollutionControlBoards>

<in-capmkt:HasTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices contextRef="DCYMain">{{ sustainability.has_lca }}</in-capmkt:HasTheEntityConductedLifeCyclePerspectiveOrAssessmentsForAnyOfItsProductsOrForItsServices>

{% for product in sustainability.product_risks %}
<in-capmkt:NameOfProductOrService contextRef="D_ProductOrService1">{{ product.name }}</in-capmkt:NameOfProductOrService>
<in-capmkt:DescriptionOfTheRiskOrConcern contextRef="D_ProductOrService1">{{ product.description | e }}</in-capmkt:DescriptionOfTheRiskOrConcern>
<in-capmkt:ActionTaken contextRef="D_ProductOrService1">{{ product.action | e }}</in-capmkt:ActionTaken>
{% endfor %}

<in-capmkt:IndicateInPutMaterial contextRef="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices1">{{ sustainability.recycled_input_cy.material }}</in-capmkt:IndicateInPutMaterial>
<in-capmkt:RecycledOrReUsedInPutMaterialToTotalMaterial contextRef="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices1" decimals="INF" unitRef="pure">{{ sustainability.recycled_input_cy.percentage }}</in-capmkt:RecycledOrReUsedInPutMaterialToTotalMaterial>
<in-capmkt:IndicateInPutMaterial contextRef="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices_PY1">{{ sustainability.recycled_input_py.material }}</in-capmkt:IndicateInPutMaterial>
<in-capmkt:RecycledOrReUsedInPutMaterialToTotalMaterial contextRef="D_RecycledOrReusedInputMaterialUsedInProductionOrProvidingServices_PY1" decimals="INF" unitRef="pure">{{ sustainability.recycled_input_py.percentage }}</in-capmkt:RecycledOrReUsedInPutMaterialToTotalMaterial>

<in-capmkt:AmountOfReUsed contextRef="D_PlasticsIncludingPackaging" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_cy.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_PlasticsIncludingPackaging" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_cy.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_PlasticsIncludingPackaging" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_cy.disposed }}</in-capmkt:AmountOfSafelyDisposed>
<in-capmkt:AmountOfReUsed contextRef="D_PlasticsIncludingPackaging_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_py.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_PlasticsIncludingPackaging_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_py.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_PlasticsIncludingPackaging_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_plastics_py.disposed }}</in-capmkt:AmountOfSafelyDisposed>

<in-capmkt:AmountOfReUsed contextRef="D_EWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_cy.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_EWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_cy.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_EWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_cy.disposed }}</in-capmkt:AmountOfSafelyDisposed>
<in-capmkt:AmountOfReUsed contextRef="D_EWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_py.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_EWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_py.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_EWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_ewaste_py.disposed }}</in-capmkt:AmountOfSafelyDisposed>

<in-capmkt:AmountOfReUsed contextRef="D_HazardousWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_cy.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_HazardousWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_cy.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_HazardousWaste" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_cy.disposed }}</in-capmkt:AmountOfSafelyDisposed>
<in-capmkt:AmountOfReUsed contextRef="D_HazardousWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_py.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_HazardousWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_py.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_HazardousWaste_PY" decimals="INF" unitRef="Tonne">{{ sustainability.waste_hazardous_py.disposed }}</in-capmkt:AmountOfSafelyDisposed>

<in-capmkt:NameOfOtherWaste contextRef="D_OtherWaste1">{{ sustainability.waste_other_cy.name }}</in-capmkt:NameOfOtherWaste>
<in-capmkt:AmountOfReUsed contextRef="D_OtherWaste1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_cy.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_OtherWaste1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_cy.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_OtherWaste1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_cy.disposed }}</in-capmkt:AmountOfSafelyDisposed>
<in-capmkt:NameOfOtherWaste contextRef="D_OtherWaste_PY1">{{ sustainability.waste_other_py.name }}</in-capmkt:NameOfOtherWaste>
<in-capmkt:AmountOfReUsed contextRef="D_OtherWaste_PY1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_py.reused }}</in-capmkt:AmountOfReUsed>
<in-capmkt:AmountOfRecycled contextRef="D_OtherWaste_PY1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_py.recycled }}</in-capmkt:AmountOfRecycled>
<in-capmkt:AmountOfSafelyDisposed contextRef="D_OtherWaste_PY1" decimals="INF" unitRef="Tonne">{{ sustainability.waste_other_py.disposed }}</in-capmkt:AmountOfSafelyDisposed>

{% for product in sustainability.reclaimed_products %}
<in-capmkt:IndicateProductCategory contextRef="D_ReclaimedProductsAndTheirPackaging{{ loop.index }}">{{ product.category | e }}</in-capmkt:IndicateProductCategory>
<in-capmkt:ReclaimedProductsAndTheirPackagingMaterialsAsPercentageOfTotalProductsSoldInRespectiveCategory contextRef="D_ReclaimedProductsAndTheirPackaging{{ loop.index }}" decimals="INF" unitRef="pure">{{ product.percentage }}</in-capmkt:ReclaimedProductsAndTheirPackagingMaterialsAsPercentageOfTotalProductsSoldInRespectiveCategory>
{% endfor %}

<in-capmkt:AmountOfAccountsPayableDuringTheYear contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.accounts_payable_cy }}</in-capmkt:AmountOfAccountsPayableDuringTheYear>
<in-capmkt:AmountOfAccountsPayableDuringTheYear contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.accounts_payable_py }}</in-capmkt:AmountOfAccountsPayableDuringTheYear>
<in-capmkt:CostOfGoodsOrServicesProcuredDuringTheYear contextRef="DCYMain" decimals="0" unitRef="INR">{{ accounts_data.cost_of_goods_cy }}</in-capmkt:CostOfGoodsOrServicesProcuredDuringTheYear>
<in-capmkt:CostOfGoodsOrServicesProcuredDuringTheYear contextRef="DPYMain" decimals="0" unitRef="INR">{{ accounts_data.cost_of_goods_py }}</in-capmkt:CostOfGoodsOrServicesProcuredDuringTheYear>
<in-capmkt:NumberOfDaysOfAccountsPayable contextRef="DCYMain">{{ accounts_data.days_payable_cy }}</in-capmkt:NumberOfDaysOfAccountsPayable>
<in-capmkt:NumberOfDaysOfAccountsPayable contextRef="DPYMain">{{ accounts_data.days_payable_py }}</in-capmkt:NumberOfDaysOfAccountsPayable>

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

{% for complaint in complaints %}
<in-capmkt:GrievanceRedressalMechanismInPlace contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}">{{ complaint.has_mechanism }}</in-capmkt:GrievanceRedressalMechanismInPlace>
<in-capmkt:WebLinkForGrievanceRedressPolicy contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}">{{ complaint.web_link if complaint.web_link else '0' }}</in-capmkt:WebLinkForGrievanceRedressPolicy>
<in-capmkt:NumberOfComplaintsFiledFromStakeHolderGroupDuringTheYear contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}" decimals="0" unitRef="pure">{{ complaint.filed_cy|int }}</in-capmkt:NumberOfComplaintsFiledFromStakeHolderGroupDuringTheYear>
<in-capmkt:NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear contextRef="I_ComplaintReceivedFrom{{ complaint.stakeholder }}" decimals="0" unitRef="pure">{{ complaint.pending_cy|int }}</in-capmkt:NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear>
<in-capmkt:RemarksStakeHolderGroupFromWhomComplaintIsReceived contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}">{{ complaint.remarks_cy if complaint.remarks_cy else '0' }}</in-capmkt:RemarksStakeHolderGroupFromWhomComplaintIsReceived>
<in-capmkt:NumberOfComplaintsFiledFromStakeHolderGroupDuringTheYear contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY" decimals="0" unitRef="pure">{{ complaint.filed_py|int }}</in-capmkt:NumberOfComplaintsFiledFromStakeHolderGroupDuringTheYear>
<in-capmkt:NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear contextRef="I_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY" decimals="0" unitRef="pure">{{ complaint.pending_py|int }}</in-capmkt:NumberOfComplaintsPendingFromStakeHolderGroupResolutionAtTheEndOfYear>
<in-capmkt:RemarksStakeHolderGroupFromWhomComplaintIsReceived contextRef="D_ComplaintReceivedFrom{{ complaint.stakeholder }}_PY">{{ complaint.remarks_py if complaint.remarks_py else '0' }}</in-capmkt:RemarksStakeHolderGroupFromWhomComplaintIsReceived>
{% endfor %}

{% for issue in material_issues %}
<in-capmkt:MaterialIssueIdentified contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.issue }}</in-capmkt:MaterialIssueIdentified>
<in-capmkt:IndicateWhetherRiskOrOpportunity contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.risk_or_opp }}</in-capmkt:IndicateWhetherRiskOrOpportunity>
<in-capmkt:RationaleForIdentifyingTheRiskOpportunity contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.rationale }}</in-capmkt:RationaleForIdentifyingTheRiskOpportunity>
<in-capmkt:InCaseOfRiskApproachToAdaptOrMitigate contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.mitigation }}</in-capmkt:InCaseOfRiskApproachToAdaptOrMitigate>
<in-capmkt:FinancialImplicationsOfTheRiskOrOpportunity contextRef="D_EntitysMaterialResponsibleBusinessConductIssues{{ loop.index }}">{{ issue.financial_impact }}</in-capmkt:FinancialImplicationsOfTheRiskOrOpportunity>
{% endfor %}

            
        {% set emp_map = {'permanent': 'PermanentEmployees', 'other_than_permanent': 'OtherThanPermanentEmployees'} %}
    {% set gender_map = {'male': 'Male', 'female': 'Female', 'others': 'Others', 'total': 'Total'} %}
    {% set benefit_map = {'health': 'HealthInsurance', 'accident': 'AccidentInsurance', 'maternity': 'MaternityBenefits', 'paternity': 'PaternityBenefits', 'daycare': 'DayCareFacilities'} %}

    {% for emp_key, emp_type in emp_map.items() %}
    {% for gender_key, gender in gender_map.items() %}
        <in-capmkt:TotalNumberOfEmployeesOrWorkers contextRef="D_{{ gender }}_Total_{{ emp_type }}_Table1A" decimals="0" unitRef="pure">{{ employee_wellbeing.employees[emp_key][gender_key].get('total', 0) | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkers>

    {% for benefit_key, benefit in benefit_map.items() %}
        <in-capmkt:NumberOfWellBeingOfEmployeesOrWorkers contextRef="D_{{ gender }}_{{ benefit }}_{{ emp_type }}_Table1A" decimals="0" unitRef="pure">{{ employee_wellbeing.employees[emp_key][gender_key].get(benefit_key + '_num', 0) | int }}</in-capmkt:NumberOfWellBeingOfEmployeesOrWorkers>
    <in-capmkt:PercentageOfWellBeingOfEmployeesOrWorkers contextRef="D_{{ gender }}_{{ benefit }}_{{ emp_type }}_Table1A" decimals="INF" unitRef="pure">{{ employee_wellbeing.employees[emp_key][gender_key].get(benefit_key + '_pct', 0) }}</in-capmkt:PercentageOfWellBeingOfEmployeesOrWorkers>
    {% endfor %}
    {% endfor %}
    {% endfor %}

        {% set worker_map = {'permanent': 'PermanentWorkers', 'other_than_permanent': 'OtherThanPermanentWorkers'} %}

    {% for worker_key, worker_type in worker_map.items() %}
    {% for gender_key, gender in gender_map.items() %}
        <in-capmkt:TotalNumberOfEmployeesOrWorkers contextRef="D_{{ gender }}_Total_{{ worker_type }}_Table1B" decimals="0" unitRef="pure">{{ employee_wellbeing.workers[worker_key][gender_key].get('total', 0) | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkers>

    {% for benefit_key, benefit in benefit_map.items() %}
        <in-capmkt:NumberOfWellBeingOfEmployeesOrWorkers contextRef="D_{{ gender }}_{{ benefit }}_{{ worker_type }}_Table1B" decimals="0" unitRef="pure">{{ employee_wellbeing.workers[worker_key][gender_key].get(benefit_key + '_num', 0) | int }}</in-capmkt:NumberOfWellBeingOfEmployeesOrWorkers>
    <in-capmkt:PercentageOfWellBeingOfEmployeesOrWorkers contextRef="D_{{ gender }}_{{ benefit }}_{{ worker_type }}_Table1B" decimals="INF" unitRef="pure">{{ employee_wellbeing.workers[worker_key][gender_key].get(benefit_key + '_pct', 0) }}</in-capmkt:PercentageOfWellBeingOfEmployeesOrWorkers>
    {% endfor %}
    {% endfor %}
    {% endfor %}

        <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_ProvidentFund" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.pf.emp_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_ProvidentFund" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.pf.worker_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_ProvidentFund">{{ employee_wellbeing.retirement_benefits.pf.deposited_cy }}</in-capmkt:DeductedAndDepositedWithTheAuthority>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_ProvidentFund_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.pf.emp_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_ProvidentFund_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.pf.worker_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_ProvidentFund_PY">{{ employee_wellbeing.retirement_benefits.pf.deposited_py }}</in-capmkt:DeductedAndDepositedWithTheAuthority>

        <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_Gratuity" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.gratuity.emp_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_Gratuity" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.gratuity.worker_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_Gratuity">{{ employee_wellbeing.retirement_benefits.gratuity.deposited_cy }}</in-capmkt:DeductedAndDepositedWithTheAuthority>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_Gratuity_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.gratuity.emp_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_Gratuity_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.gratuity.worker_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_Gratuity_PY">{{ employee_wellbeing.retirement_benefits.gratuity.deposited_py }}</in-capmkt:DeductedAndDepositedWithTheAuthority>

        <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_ESI" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.esi.emp_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_ESI" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.esi.worker_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_ESI">{{ employee_wellbeing.retirement_benefits.esi.deposited_cy }}</in-capmkt:DeductedAndDepositedWithTheAuthority>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_ESI_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.esi.emp_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_ESI_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.esi.worker_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_ESI_PY">{{ employee_wellbeing.retirement_benefits.esi.deposited_py }}</in-capmkt:DeductedAndDepositedWithTheAuthority>

        <in-capmkt:NameOfOtherRetirementBenefits contextRef="D_OtherRetirementBenefits1">{{ employee_wellbeing.retirement_benefits.others.name_cy | e }}</in-capmkt:NameOfOtherRetirementBenefits>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_OtherRetirementBenefits1" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.others.emp_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_OtherRetirementBenefits1" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.others.worker_cy }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_OtherRetirementBenefits1">{{ employee_wellbeing.retirement_benefits.others.deposited_cy }}</in-capmkt:DeductedAndDepositedWithTheAuthority>
    <in-capmkt:NameOfOtherRetirementBenefits contextRef="D_OtherRetirementBenefits_PY1">{{ employee_wellbeing.retirement_benefits.others.name_py | e }}</in-capmkt:NameOfOtherRetirementBenefits>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees contextRef="D_OtherRetirementBenefits_PY1" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.others.emp_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalEmployees>
    <in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker contextRef="D_OtherRetirementBenefits_PY1" decimals="INF" unitRef="pure">{{ employee_wellbeing.retirement_benefits.others.worker_py }}</in-capmkt:NumberOfEmployeesCoveredAsPercentageOfTotalWorker>
    <in-capmkt:DeductedAndDepositedWithTheAuthority contextRef="D_OtherRetirementBenefits_PY1">{{ employee_wellbeing.retirement_benefits.others.deposited_py }}</in-capmkt:DeductedAndDepositedWithTheAuthority>

        <in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave contextRef="D_Male" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.male.emp_return }}</in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave contextRef="D_Male" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.male.emp_retention }}</in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave>
    <in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave contextRef="D_Male" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.male.worker_return }}</in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave contextRef="D_Male" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.male.worker_retention }}</in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave>

        <in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave contextRef="D_Female" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.female.emp_return }}</in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave contextRef="D_Female" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.female.emp_retention }}</in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave>
    <in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave contextRef="D_Female" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.female.worker_return }}</in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave contextRef="D_Female" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.female.worker_retention }}</in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave>

        <in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave contextRef="D_OtherGender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.others.emp_return }}</in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave contextRef="D_OtherGender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.others.emp_retention }}</in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave>
    <in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave contextRef="D_OtherGender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.others.worker_return }}</in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave contextRef="D_OtherGender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.others.worker_retention }}</in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave>

        <in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave contextRef="D_Gender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.total.emp_return }}</in-capmkt:ReturnToWorkRatePermanentEmployeesThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave contextRef="D_Gender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.total.emp_retention }}</in-capmkt:RetentionRatesPermanentEmployeesThatTookParentalLeave>
    <in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave contextRef="D_Gender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.total.worker_return }}</in-capmkt:ReturnToWorkRatePermanentWorkersThatTookParentalLeave>
    <in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave contextRef="D_Gender" decimals="INF" unitRef="pure">{{ employee_wellbeing.parental_leave.total.worker_retention }}</in-capmkt:RetentionRatesPermanentWorkersThatTookParentalLeave>

        <in-capmkt:CostIncurredOnWellbeingMeasuresAsPercentageOfTotalRevenue contextRef="D_WellbeingSpending_CY" decimals="INF" unitRef="pure">{{ employee_wellbeing.wellbeing_spending['cy'] }}</in-capmkt:CostIncurredOnWellbeingMeasuresAsPercentageOfTotalRevenue>
    <in-capmkt:CostIncurredOnWellbeingMeasuresAsPercentageOfTotalRevenue contextRef="D_WellbeingSpending_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.wellbeing_spending['py'] }}</in-capmkt:CostIncurredOnWellbeingMeasuresAsPercentageOfTotalRevenue>

        <in-capmkt:AreThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkers contextRef="DCYMain">Yes</in-capmkt:AreThePremisesOrOfficesOfTheEntityAccessibleToDifferentlyAbledEmployeesAndWorkers>

        <in-capmkt:DoesTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016 contextRef="DCYMain">{{ employee_wellbeing.equal_opportunity.has_policy }}</in-capmkt:DoesTheEntityHaveAnEqualOpportunityPolicyAsPerTheRightsOfPersonsWithDisabilitiesAct2016>
    <in-capmkt:WebLinkOfEqualOppertunityPolicyTextBlock contextRef="DCYMain">{{ employee_wellbeing.equal_opportunity.web_link }}</in-capmkt:WebLinkOfEqualOppertunityPolicyTextBlock>

        <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker contextRef="DCYMain">{{ employee_wellbeing.grievance.has_mechanism }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForTheFollowingCategoriesOfEmployeesAndWorker>
    <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForPermanentWorkers contextRef="DCYMain">{{ employee_wellbeing.grievance.permanent_workers.available }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForPermanentWorkers>
    <in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForPermanentWorkersExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.grievance.permanent_workers.details | e }}</in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForPermanentWorkersExplanatoryTextBlock>
    <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentWorkers contextRef="DCYMain">{{ employee_wellbeing.grievance.other_workers.available }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentWorkers>
    <in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentWorkersExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.grievance.other_workers.details | e }}</in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentWorkersExplanatoryTextBlock>
    <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForPermanentEmployees contextRef="DCYMain">{{ employee_wellbeing.grievance.permanent_employees.available }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForPermanentEmployees>
    <in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForPermanentEmployeesExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.grievance.permanent_employees.details | e }}</in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForPermanentEmployeesExplanatoryTextBlock>
    <in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentEmployees contextRef="DCYMain">{{ employee_wellbeing.grievance.other_employees.available }}</in-capmkt:IsThereAMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentEmployees>
    <in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentEmployeesExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.grievance.other_employees.details | e }}</in-capmkt:DetailsOfMechanismAvailableToReceiveAndRedressGrievancesForOtherThanPermanentEmployeesExplanatoryTextBlock>

        <in-capmkt:WhetherAnOccupationalHealthAndSafetyManagementSystemHasBeenImplementedByTheEntity contextRef="DCYMain">{{ employee_wellbeing.ohs.implemented }}</in-capmkt:WhetherAnOccupationalHealthAndSafetyManagementSystemHasBeenImplementedByTheEntity>
    <in-capmkt:DetailsOfOccupationalHealthAndSafetyManagementSystemExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.ohs.coverage | e }}</in-capmkt:DetailsOfOccupationalHealthAndSafetyManagementSystemExplanatoryTextBlock>
    <in-capmkt:DesclosureOfTheProcessesUsedToIdentifyWorkRelatedHazardsAndAssessRisksOnARoutineAndNonRoutineBasisByTheEntityExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.ohs.hazard_process | e }}</in-capmkt:DesclosureOfTheProcessesUsedToIdentifyWorkRelatedHazardsAndAssessRisksOnARoutineAndNonRoutineBasisByTheEntityExplanatoryTextBlock>
    <in-capmkt:WhetherYouHaveProcessesForWorkersToReportTheWorkRelatedHazardsAndToRemoveThemselvesFromSuchRisks contextRef="DCYMain">{{ employee_wellbeing.ohs.worker_report_process }}</in-capmkt:WhetherYouHaveProcessesForWorkersToReportTheWorkRelatedHazardsAndToRemoveThemselvesFromSuchRisks>
    <in-capmkt:DoTheEmployeesOrWorkerOfTheEntityHaveAccessToNonOccupationalMedicalAndHealthcareServices contextRef="DCYMain">{{ employee_wellbeing.ohs.non_occupational_access }}</in-capmkt:DoTheEmployeesOrWorkerOfTheEntityHaveAccessToNonOccupationalMedicalAndHealthcareServices>

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

        <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_WorkingConditionsComplaints" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.working_conditions.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_WorkingConditionsComplaints" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.working_conditions.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_WorkingConditionsComplaints_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.working_conditions.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_WorkingConditionsComplaints_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.working_conditions.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>

    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_HealthSafetyComplaints" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.health_safety.filed_cy | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_HealthSafetyComplaints" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.health_safety.pending_cy | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>
    <in-capmkt:NumberOfComplaintsFiledDuringTheYear contextRef="D_HealthSafetyComplaints_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.health_safety.filed_py | int }}</in-capmkt:NumberOfComplaintsFiledDuringTheYear>
    <in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear contextRef="I_HealthSafetyComplaints_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.complaints.health_safety.pending_py | int }}</in-capmkt:NumberOfComplaintsPendingResolutionAtTheEndOfYear>

        <in-capmkt:PercentageOfHealthAndSafetyPracticesOfYourPlantsAndOfficesThatWereAssessedP3 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ employee_wellbeing.assessments.health_safety_pct }}</in-capmkt:PercentageOfHealthAndSafetyPracticesOfYourPlantsAndOfficesThatWereAssessedP3>
    <in-capmkt:PercentageOfWorkingConditionsOfYourPlantsAndOfficesThatWereAssessedP3 contextRef="DCYMain" decimals="INF" unitRef="pure">{{ employee_wellbeing.assessments.working_conditions_pct }}</in-capmkt:PercentageOfWorkingConditionsOfYourPlantsAndOfficesThatWereAssessedP3>

        <in-capmkt:DescribeTheMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlaceExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.safe_workplace_measures | e }}</in-capmkt:DescribeTheMeasuresTakenByTheEntityToEnsureASafeAndHealthyWorkPlaceExplanatoryTextBlock>

        <in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessedExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.corrective_actions_safety | e }}</in-capmkt:DetailsOfAnyCorrectiveActionTakenOrUnderwayToAddressSafetyRelatedIncidentsOfYourPlantsAndOfficesThatWereAssessedExplanatoryTextBlock>

        <in-capmkt:DoesTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees contextRef="DCYMain">{{ employee_wellbeing.life_insurance.employees }}</in-capmkt:DoesTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfEmployees>
    <in-capmkt:DoesTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfWorkers contextRef="DCYMain">{{ employee_wellbeing.life_insurance.workers }}</in-capmkt:DoesTheEntityExtendAnyLifeInsuranceOrAnyCompensatoryPackageInTheEventOfDeathOfWorkers>

        <in-capmkt:DetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartnersExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.statutory_dues_measures | e }}</in-capmkt:DetailsOfMeasuresUndertakenByTheEntityToEnsureThatStatutoryDuesHaveBeenDeductedAndDepositedByTheValueChainPartnersExplanatoryTextBlock>

        <in-capmkt:TotalNumberOfAffectedEmployees contextRef="DCYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.affected_employees_cy | int }}</in-capmkt:TotalNumberOfAffectedEmployees>
    <in-capmkt:TotalNumberOfAffectedEmployees contextRef="DPYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.affected_employees_py | int }}</in-capmkt:TotalNumberOfAffectedEmployees>
    <in-capmkt:TotalNumberOfAffectedWorkers contextRef="DCYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.affected_workers_cy | int }}</in-capmkt:TotalNumberOfAffectedWorkers>
    <in-capmkt:TotalNumberOfAffectedWorkers contextRef="DPYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.affected_workers_py | int }}</in-capmkt:TotalNumberOfAffectedWorkers>

        <in-capmkt:NumberOfEmployeesOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment contextRef="DCYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.rehabilitated_employees_cy | int }}</in-capmkt:NumberOfEmployeesOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment>
    <in-capmkt:NumberOfEmployeesOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment contextRef="DPYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.rehabilitated_employees_py | int }}</in-capmkt:NumberOfEmployeesOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment>
    <in-capmkt:NumberOfWorkersOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment contextRef="DCYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.rehabilitated_workers_cy | int }}</in-capmkt:NumberOfWorkersOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment>
    <in-capmkt:NumberOfWorkersOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment contextRef="DPYMain" decimals="0" unitRef="pure">{{ employee_wellbeing.rehabilitated_workers_py | int }}</in-capmkt:NumberOfWorkersOrWhoseFamilyMembersRehabilitatedAndPlacedInSuitableEmployment>

        <in-capmkt:DoesTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment contextRef="DCYMain">{{ employee_wellbeing.transition_assistance }}</in-capmkt:DoesTheEntityProvideTransitionAssistanceProgramsToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmployment>
    <in-capmkt:DetailsOfTransitionAssistanceProgramsProvidedToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmploymentExplanatoryTextBlock contextRef="DCYMain">{{ employee_wellbeing.transition_assistance_details | e }}</in-capmkt:DetailsOfTransitionAssistanceProgramsProvidedToFacilitateContinuedEmployabilityAndTheManagementOfCareerEndingsResultingFromRetirementOrTerminationOfEmploymentExplanatoryTextBlock>

        {% set training_genders = [('male', 'Male'), ('female', 'Female'), ('others', 'Others')] %}
    {% for gender_key, gender in training_genders %}
        <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_TotalEmployeesAndWorkers_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].total_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].hs_num_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].hs_pct_cy }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnSkillUpgradation_Employees" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].skill_num_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnSkillUpgradation_Employees" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].skill_pct_cy }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
        <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_TotalEmployeesAndWorkers_Employees_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].total_py | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].hs_num_py | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Employees_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.employees[gender_key].hs_pct_py }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
        <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_TotalEmployeesAndWorkers_Workers" decimals="0" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].total_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers" decimals="0" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].hs_num_cy | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].hs_pct_cy }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
        <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_TotalEmployeesAndWorkers_Workers_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].total_py | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:NumberOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers_PY" decimals="0" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].hs_num_py | int }}</in-capmkt:NumberOfTrainedEmployeesOrWorkers>
    <in-capmkt:PercentageOfTrainedEmployeesOrWorkers contextRef="D_{{ gender }}_OnHealthAndSafetyMeasures_Workers_PY" decimals="INF" unitRef="pure">{{ employee_wellbeing.training.workers[gender_key].hs_pct_py }}</in-capmkt:PercentageOfTrainedEmployeesOrWorkers>
    {% endfor %}

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

        <in-capmkt:DescriptionOfAccessibilityOfWorkplaces contextRef="D_Accessibility">{{ employee_wellbeing.accessibility | e }}</in-capmkt:DescriptionOfAccessibilityOfWorkplaces>

            <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Gender_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.total.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Gender_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.total.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Gender_PermanentEmployees" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.total.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Gender_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.total.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Gender_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.total.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Gender_PermanentEmployees_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.total.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Male_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.male.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Male_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.male.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Male_PermanentEmployees" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.male.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Male_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.male.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Male_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.male.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Male_PermanentEmployees_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.male.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Female_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.female.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Female_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.female.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Female_PermanentEmployees" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.female.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Female_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.female.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Female_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.female.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Female_PermanentEmployees_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.female.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_OtherGender_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.other.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_OtherGender_PermanentEmployees" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.other.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_OtherGender_PermanentEmployees" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.other.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_OtherGender_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.other.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_OtherGender_PermanentEmployees_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_employees.other.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_OtherGender_PermanentEmployees_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_employees.other.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Gender_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.total.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Gender_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.total.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Gender_PermanentWorkers" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.total.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Gender_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.total.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Gender_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.total.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Gender_PermanentWorkers_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.total.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Male_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.male.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Male_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.male.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Male_PermanentWorkers" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.male.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Male_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.male.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Male_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.male.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Male_PermanentWorkers_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.male.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Female_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.female.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Female_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.female.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Female_PermanentWorkers" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.female.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_Female_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.female.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_Female_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.female.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_Female_PermanentWorkers_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.female.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_OtherGender_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.other.total_cy | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_OtherGender_PermanentWorkers" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.other.members_cy | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_OtherGender_PermanentWorkers" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.other.pct_cy }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>
        <in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership contextRef="D_OtherGender_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.other.total_py | int }}</in-capmkt:TotalNumberOfEmployeesOrWorkersForMembership>
    <in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion contextRef="D_OtherGender_PermanentWorkers_PY" decimals="0" unitRef="pure">{{ union_membership.permanent_workers.other.members_py | int }}</in-capmkt:NumberOfEmployeesOrWorkersArePartOfAssociationsOrUnion>
    <in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee contextRef="D_OtherGender_PermanentWorkers_PY" decimals="INF" unitRef="pure">{{ union_membership.permanent_workers.other.pct_py }}</in-capmkt:PercentageOfEmployeesOrWorkersArePartOfAssociationsOrUnionOfTotalNumberOfEmployee>

        {% for i in range(1, 21) %}
    <xbrli:context id="D_IndustryChambersOrAssociations{{ i }}">
      <xbrli:entity><xbrli:identifier scheme="http://www.mca.gov.in/CIN">{{ cin }}</xbrli:identifier></xbrli:entity>
      <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
    </xbrli:context>
    {% endfor %}

        {% for project in csr.aspirational_districts %}
    <xbrli:context id="{{ project.axis_id }}">
      <xbrli:entity><xbrli:identifier scheme="http://www.mca.gov.in/CIN">{{ cin }}</xbrli:identifier></xbrli:entity>
      <xbrli:period><xbrli:startDate>{{ start_date_cy }}</xbrli:startDate><xbrli:endDate>{{ end_date_cy }}</xbrli:endDate></xbrli:period>
    </xbrli:context>
    {% endfor %}

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

        <in-capmkt:NumberOfAffiliationsWithTradeAndIndustryChambersOrAssociations contextRef="DCYMain" decimals="0" unitRef="pure">{{ p789_data.p7.num_affiliations }}</in-capmkt:NumberOfAffiliationsWithTradeAndIndustryChambersOrAssociations>

    {% for affiliation in p789_data.p7.affiliations %}
    <in-capmkt:NameOfTheTradeAndIndustryChambersOrAssociations contextRef="D_IndustryChambersOrAssociations{{ loop.index }}">{{ affiliation.name | e }}</in-capmkt:NameOfTheTradeAndIndustryChambersOrAssociations>
    <in-capmkt:ReachOfTradeAndIndustryChambersOrAssociations contextRef="D_IndustryChambersOrAssociations{{ loop.index }}">{{ affiliation.reach }}</in-capmkt:ReachOfTradeAndIndustryChambersOrAssociations>
    {% endfor %}

        <in-capmkt:DescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunityExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p8.community_grievance_mechanism | e }}</in-capmkt:DescribeTheMechanismsToReceiveAndRedressGrievancesOfTheCommunityExplanatoryTextBlock>
    <in-capmkt:PercentageOfDirectlySourcedFromMSMEsOrSmallProducers contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p8.msme_sourcing_cy }}</in-capmkt:PercentageOfDirectlySourcedFromMSMEsOrSmallProducers>
    <in-capmkt:PercentageOfDirectlySourcedFromMSMEsOrSmallProducers contextRef="DPYMain" decimals="INF" unitRef="pure">{{ p789_data.p8.msme_sourcing_py }}</in-capmkt:PercentageOfDirectlySourcedFromMSMEsOrSmallProducers>
    <in-capmkt:PercentageOfSourcedDirectlyFromWithinTheDistrictAndNeighbouringDistricts contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p8.local_sourcing_cy }}</in-capmkt:PercentageOfSourcedDirectlyFromWithinTheDistrictAndNeighbouringDistricts>
    <in-capmkt:PercentageOfSourcedDirectlyFromWithinTheDistrictAndNeighbouringDistricts contextRef="DPYMain" decimals="INF" unitRef="pure">{{ p789_data.p8.local_sourcing_py }}</in-capmkt:PercentageOfSourcedDirectlyFromWithinTheDistrictAndNeighbouringDistricts>
    <in-capmkt:DoYouHaveAPreferentialProcurementPolicyWhereYouGivePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroups contextRef="DCYMain">{{ p789_data.p8.preferential_procurement }}</in-capmkt:DoYouHaveAPreferentialProcurementPolicyWhereYouGivePreferenceToPurchaseFromSuppliersComprisingMarginalizedOrVulnerableGroups>

        <in-capmkt:DescribeTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedbackExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.complaint_mechanism | e }}</in-capmkt:DescribeTheMechanismsInPlaceToReceiveAndRespondToConsumerComplaintsAndFeedbackExplanatoryTextBlock>
    <in-capmkt:EnvironmentalAndSocialParametersRelevantToTheProductAsAPercentageToTotalTurnover contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p9.env_social_pct }}</in-capmkt:EnvironmentalAndSocialParametersRelevantToTheProductAsAPercentageToTotalTurnover>
    <in-capmkt:SafeAndResponsibleUsageAsAPercentageToTotalTurnover contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p9.safe_usage_pct }}</in-capmkt:SafeAndResponsibleUsageAsAPercentageToTotalTurnover>
    <in-capmkt:RecyclingAndOrSafeDisposalAsAPercentageToTotalTurnover contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p9.recycling_pct }}</in-capmkt:RecyclingAndOrSafeDisposalAsAPercentageToTotalTurnover>

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

        <in-capmkt:NumberOfVoluntaryRecalls contextRef="DCYMain" decimals="0" unitRef="pure">{{ p789_data.p9.voluntary_recalls }}</in-capmkt:NumberOfVoluntaryRecalls>
    <in-capmkt:ReasonsForVoluntaryRecall contextRef="DCYMain">{{ p789_data.p9.voluntary_recall_reason }}</in-capmkt:ReasonsForVoluntaryRecall>
    <in-capmkt:NumberOfForcedRecalls contextRef="DCYMain" decimals="0" unitRef="pure">{{ p789_data.p9.forced_recalls }}</in-capmkt:NumberOfForcedRecalls>
    <in-capmkt:ReasonsForForcedRecall contextRef="DCYMain">{{ p789_data.p9.forced_recall_reason }}</in-capmkt:ReasonsForForcedRecall>

        <in-capmkt:DoesTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy contextRef="DCYMain">{{ p789_data.p9.cyber_policy }}</in-capmkt:DoesTheEntityHaveAFrameworkOrPolicyOnCyberSecurityAndRisksRelatedToDataPrivacy>
    <in-capmkt:WebLinkOfThePolicyOnCyberSecurityAndRisksRelatedToDataPrivacy contextRef="DCYMain">{{ p789_data.p9.cyber_policy_weblink | e }}</in-capmkt:WebLinkOfThePolicyOnCyberSecurityAndRisksRelatedToDataPrivacy>
    <in-capmkt:NumberOfInstancesOfDataBreachesAlongWithImpact contextRef="DCYMain" decimals="0" unitRef="pure">{{ p789_data.p9.data_breaches }}</in-capmkt:NumberOfInstancesOfDataBreachesAlongWithImpact>
    <in-capmkt:PercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomers contextRef="DCYMain" decimals="INF" unitRef="pure">{{ p789_data.p9.pii_breach_pct }}</in-capmkt:PercentageOfDataBreachesInvolvingPersonallyIdentifiableInformationOfCustomers>
    <in-capmkt:DetailsOfImpactOfDataBreachesExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.data_breach_impact | default('NA') | e }}</in-capmkt:DetailsOfImpactOfDataBreachesExplanatoryTextBlock>

        <in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServicesExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.corrective_actions_q6 | e }}</in-capmkt:DetailsOfAnyCorrectiveActionsTakenOrUnderwayOnIssuesRelatingToAdvertisingAndDeliveryOfEssentialServicesOrCyberSecurityAndDataPrivacyOrRecallsOrPenaltyOrActionTakenByRegulatoryAuthoritiesOnSafetyOfProductsOrServicesExplanatoryTextBlock>

        <in-capmkt:WeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessedExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.product_info_link | e }}</in-capmkt:WeblinkWhereInformationOnProductsAndServicesOfTheEntityCanBeAccessedExplanatoryTextBlock>
    <in-capmkt:StepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServicesExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.consumer_education | e }}</in-capmkt:StepsTakenToInformAndEducateConsumersAboutSafeAndResponsibleUsageOfProductsAndOrServicesExplanatoryTextBlock>
    <in-capmkt:MechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServicesExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.disruption_mechanism | default('') | e }}</in-capmkt:MechanismsInPlaceToInformConsumersOfAnyRiskOfDisruptionOrDiscontinuationOfEssentialServicesExplanatoryTextBlock>
    <in-capmkt:DoesTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws contextRef="DCYMain">{{ p789_data.p9.product_info_display }}</in-capmkt:DoesTheEntityDisplayProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLaws>
    <in-capmkt:DetailsOfProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLawsExplanatoryTextBlock contextRef="DCYMain">{{ p789_data.p9.product_info_display_details | default('') | e }}</in-capmkt:DetailsOfProductInformationOnTheProductOverAndAboveWhatIsMandatedAsPerLocalLawsExplanatoryTextBlock>

</xbrli:xbrl>
'''