from auto_report_writing.data_processing.xml_loader import load_xml
from auto_report_writing.report_generation.determine_classification import cvss_from_risk_level
from auto_report_writing.report_generation.generate_recommendations import generate_recommendations_name
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
            recommendations = generate_recommendations_name(name)

            exploit_element = SubElement(host_element, 'exploit', id=exploit_id)
            SubElement(exploit_element, 'name').text = name
            SubElement(exploit_element, 'risk').text = risk
            SubElement(exploit_element, 'cvss_score').text = f"{cvss_score}"
            SubElement(exploit_element, 'description').text = f"Description: {description}"
            SubElement(exploit_element, 'result').text = f"Result: {result}."
            SubElement(exploit_element, 'recommendations').text = recommendations

    return ElementTree(report)


def count_hosts(root):
    """
    Counts the number of hosts in the given Metasploit XML root.
    """
    return len(root.findall('.//host'))


def count_exploits_per_host(root):
    """
    Counts the number of exploits for each host in the given Metasploit XML root.
    """
    host_exploit_counts = []

    for host in root.findall('.//host'):
        host_address = host.find('address').text
        exploits = host.findall('.//exploit')
        exploit_count = len(exploits) if exploits is not None else 0
        host_exploit_counts.append((host_address, exploit_count))

    return host_exploit_counts


def print_exploit_details(root):
    """
    Prints details for each exploit in the given Metasploit XML root.
    """
    host_count = count_hosts(root)
    exploits_per_host = count_exploits_per_host(root)
    total_exploits_per_host = sum(exploit_count for _, exploit_count in exploits_per_host)
    print_exploit_report_details(host_count, total_exploits_per_host)

    for host_address, exploit_count in exploits_per_host:
        print_exploit_details_for_host(host_address, exploit_count)

        for host in root.findall('.//host'):
            address = host.find('address').text

            if address == host_address:
                exploits = host.findall('.//exploit')

                for exploit in exploits:
                    name = exploit.find('name').text
                    description = exploit.find('description').text
                    result = exploit.find('result').text
                    risk_classification = exploit.find('risk').text
                    cvss_score = cvss_from_risk_level(risk_classification)
                    recommendations = generate_recommendations_name(name)

                    print_vulnerability_details(name, risk_classification, cvss_score, description, result, recommendations)

                break

        else:
            print_no_exploits_found(host_address)


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
