import xml.etree.ElementTree as ET


def generate_report(nmap_xml):
    tree = ET.parse(nmap_xml)
    root = tree.getroot()

    # Create the root for the new XML
    report_root = ET.Element("Report")

    # Add the Pen Testing Tool Name
    pen_tool = ET.SubElement(report_root, "PenTestingToolName")
    pen_tool.text = "Nmap"

    for host in root.findall('host'):
        address = host.find('address').get('addr')

        # Add Host Element
        host_element = ET.SubElement(report_root, "Host")
        host_ip = ET.SubElement(host_element, "IP")
        host_ip.text = address

        for port in host.findall('ports/port'):
            port_id = port.get('portid')
            service_name = port.find('service').get('name')
            service_product = port.find('service').get('product', '')
            service_version = port.find('service').get('version', '')
            service_extrainfo = port.find('service').get('extrainfo', '')
            script_output = port.findall('script')

            # Generate Vulnerability Name
            vulnerability_name = f"{service_product} {service_version}".strip()

            # Generate Risk Level (simplified logic for this example)
            risk_level = "Medium"
            if "OpenSSH" in service_product and "7.9" in service_version:
                risk_level = "Medium"

            # Generate CVSS Score (simplified logic for this example)
            cvss_score = "5.0"
            if risk_level == "Medium":
                cvss_score = "5.0"

            # Add Vulnerability Element
            vulnerability = ET.SubElement(host_element, "Vulnerability")

            vuln_name = ET.SubElement(vulnerability, "VulnerabilityName")
            vuln_name.text = vulnerability_name

            vuln_risk = ET.SubElement(vulnerability, "RiskLevel")
            vuln_risk.text = risk_level

            vuln_cvss = ET.SubElement(vulnerability, "CVSSScore")
            vuln_cvss.text = cvss_score

            vuln_details = ET.SubElement(vulnerability, "VulnerabilityDetails")

            # Add all other elements in <port> that are not already added
            for element in port:
                if element.tag not in ['state', 'service', 'script']:
                    detail = ET.SubElement(vuln_details, element.tag)
                    detail.text = element.text if element.text else ''
                    for attr, value in element.attrib.items():
                        detail.set(attr, value)

            # Add service details to VulnerabilityDetails
            service_details = {
                "Port": port_id,
                "Service": service_name,
                "Product": service_product,
                "Version": service_version,
                "ExtraInfo": service_extrainfo,
            }
            for key, value in service_details.items():
                if value:  # Only add if value is not empty
                    detail = ET.SubElement(vuln_details, key)
                    detail.text = value

            # Add script output
            if script_output:
                script_element = ET.SubElement(vuln_details, "ScriptOutput")
                for script in script_output:
                    script_id = script.get('id')
                    script_text = script.get('output')
                    script_detail = ET.SubElement(script_element, script_id.replace("-", "_"))
                    script_detail.text = script_text

    # Create the new XML tree and write to a file
    new_tree = ET.ElementTree(report_root)
    new_tree.write("restructured_report.xml", encoding='utf-8', xml_declaration=True)


# Path to the original nmap XML file
nmap_xml_path = "auto_report_writing/report_generation/report_templates/nmap_output.xml"
generate_report(nmap_xml_path)
