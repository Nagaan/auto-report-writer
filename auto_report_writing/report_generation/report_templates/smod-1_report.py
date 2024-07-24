from determine_classification import cvss_from_risk_level, risk_level_from_name
from generate_recommendations import generate_recommendations_name

from xml.etree.ElementTree import Element, SubElement, ElementTree
import xml.etree.ElementTree as EleTree


def generate_smod1_report(root):
    """
    Generates an XML structure with details of vulnerabilities from SMOD-1 data.
    """
    report = Element('smod1_report')

    for attempt in root.findall('.//attempt'):
        vulnerability = attempt.find('vulnerability').text
        risk_level = risk_level_from_name(vulnerability)
        cvss_score = cvss_from_risk_level(risk_level)
        recommendations = generate_recommendations_name(vulnerability)

        attempt_element = SubElement(report, 'attempt')
        SubElement(attempt_element, 'vulnerability').text = vulnerability
        SubElement(attempt_element, 'risk_level').text = risk_level
        SubElement(attempt_element, 'cvss_score').text = f"{cvss_score}"

        details_element = SubElement(attempt_element, 'details')
        for child in attempt:
            if child.tag not in ['target', 'device', 'vulnerability', 'result', 'timestamp', 'commands']:
                detail_element = SubElement(details_element, child.tag)
                detail_element.text = child.text
            elif child.tag == 'commands':
                commands_element = SubElement(details_element, 'commands')
                for cmd in child.findall('command'):
                    command_element = SubElement(commands_element, 'command')
                    command_element.text = cmd.text

        SubElement(attempt_element, 'recommendations').text = recommendations

    return ElementTree(report)


def print_smod1_details(root):
    """
    Prints details for each vulnerability in the given SMOD-1 XML root.
    """
    for attempt in root.findall('.//attempt'):
        vulnerability = attempt.find('vulnerability').text
        risk_level = risk_level_from_name(vulnerability)
        cvss_score = cvss_from_risk_level(risk_level)
        recommendations = generate_recommendations_name(vulnerability)

        details = {}
        for child in attempt:
            if child.tag not in ['target', 'device', 'vulnerability', 'result', 'timestamp', 'commands']:
                details[child.tag] = child.text
            elif child.tag == 'commands':
                details[child.tag] = [cmd.text for cmd in child.findall('command')]

        print(f"Vulnerability Name: {vulnerability}")
        print(f"Risk Level: {risk_level}")
        print(f"CSVV Score: {cvss_score}")
        print(f"Vulnerability Details:")
        for key, value in details.items():
            if key == 'commands':
                print(f"  - {key}: {', '.join(value)}")
            else:
                print(f"  - {key}: {value}")
        print(f"Recommendations: {recommendations}")
        print("\n" + "-"*40 + "\n")


def process_smod1_data(file_path, output_file):
    """
    Processes the input SMOD-1 XML file, prints a structured report, and generates an XML report.
    """
    try:
        tree = EleTree.parse(file_path)
        root = tree.getroot()

        print_smod1_details(root)
        report_tree = generate_smod1_report(root)
        report_tree.write(output_file, encoding='utf-8', xml_declaration=True)

    except EleTree.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except Exception as e:
        print(f"Error processing the report: {e}")


# Example usage
file_path = 'B:/Work/auto-report-writer/Data/Smod-1_Data.xml'
output_file = 'B:/Work/auto-report-writer/Data/structured_smod1_report.xml'
process_smod1_data(file_path, output_file)
