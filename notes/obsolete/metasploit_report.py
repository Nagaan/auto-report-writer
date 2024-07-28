from auto_report_writing.data_processing.xml_loader import load_xml
from auto_report_writing.report_generation.determine_classification import cvss_from_risk_level
from auto_report_writing.utils.message_utils import *

from xml.etree.ElementTree import Element, SubElement, ElementTree


def generate_metasploit_report(root):
    """
    Generates an XML structure with details of exploits for each host.
    """
    report = Element('metasploit_report')

    for host in root.findall('.//host'):
        address = host.find('address').text
        host_element = SubElement(report, 'host')
        SubElement(host_element, 'address', addr=address)

        exploits = host.findall('.//exploit')
        for exploit in exploits:
            exploit_id = exploit.get('id')
            name = exploit.find('name').text
            description = exploit.find('description').text
            result = exploit.find('result').text
            risk = exploit.find('risk').text
            cvss_score = cvss_from_risk_level(risk)

            exploit_element = SubElement(host_element, 'exploit', id=exploit_id)
            SubElement(exploit_element, 'name').text = name
            SubElement(exploit_element, 'risk').text = risk
            SubElement(exploit_element, 'cvss_score').text = f"{cvss_score}"
            SubElement(exploit_element, 'description').text = f"Description: {description}"
            SubElement(exploit_element, 'result').text = f"Result: {result}."

    return ElementTree(report)


def metasploit_report(file_path, output_file):
    """
    Processes the input Metasploit XML file and generates a Metasploit report XML.
    """
    try:
        tree, root = load_xml(file_path)

        if root is not None:
            report_tree = generate_metasploit_report(root)
            report_tree.write(output_file, encoding='utf-8', xml_declaration=True)

        else:
            print_failed_to_load_file()

    except Exception as e:
        print_error_processing_report(e)
