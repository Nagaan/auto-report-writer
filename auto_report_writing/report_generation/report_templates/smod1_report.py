from auto_report_writing.data_processing.xml_loader import load_xml
from auto_report_writing.report_generation.determine_classification import cvss_from_risk_level, risk_level_from_name
from auto_report_writing.report_generation.generate_recommendations import generate_recommendations_name
from auto_report_writing.utils.message_utils import *

from xml.etree.ElementTree import Element, SubElement, ElementTree


def generate_smod1_report(root):
    """
    Generates an XML structure with details of exploitation attempts where the result is not 'Failed'.
    """
    report = Element('smod1_report')

    for attempt in root.findall('.//attempt'):
        result = attempt.find('result').text
        if result != 'Failed':
            target = attempt.find('target').text
            vulnerability_name = attempt.find('vulnerability').text
            timestamp = attempt.find('timestamp').text
            details = attempt.find('details').text
            commands = attempt.findall('commands/command')

            # Generate Risk Level and CVSS Score using functions
            risk_level = risk_level_from_name(vulnerability_name)  # Replace with your actual function
            cvss_score = cvss_from_risk_level(risk_level)
            recommendations = generate_recommendations_name(vulnerability_name)

            attempt_element = SubElement(report, 'attempt', id=attempt.get('id'))
            SubElement(attempt_element, 'target').text = target
            SubElement(attempt_element, 'vulnerability').text = vulnerability_name
            SubElement(attempt_element, 'risk_level').text = risk_level
            SubElement(attempt_element, 'cvss_score').text = f"{cvss_score}"

            # Add vulnerability details
            details_element = SubElement(attempt_element, 'vulnerability_details')
            SubElement(details_element, 'details').text = details
            SubElement(details_element, 'timestamp').text = f"Timestamp: {timestamp}"

            # Adding commands
            commands_element = SubElement(attempt_element, 'commands')
            for command in commands:
                SubElement(commands_element, 'command').text = command.text

            # Adding recommendations
            SubElement(attempt_element, 'recommendations').text = recommendations

    return ElementTree(report)


def count_attempts(root):
    """
    Counts the number of exploitation attempts where the result is not 'Failed' in the given Smod-1 XML root.
    """
    return len(root.findall('.//attempt[result!="Failed"]'))


def print_exploit_details_smod1(root):
    """
    Prints details for each exploitation attempt where the result is not 'Failed' in the given Smod-1 XML root.
    """
    attempts_count = count_attempts(root)
    print(f"Number of exploitation attempts (excluding failures): {attempts_count}")

    for attempt in root.findall('.//attempt'):
        result = attempt.find('result').text
        if result != 'Failed':
            target = attempt.find('target').text
            vulnerability_name = attempt.find('vulnerability').text
            timestamp = attempt.find('timestamp').text
            details = attempt.find('details').text
            commands = [cmd.text for cmd in attempt.findall('commands/command')]

            risk_level = risk_level_from_name(vulnerability_name)  # Replace with your actual function
            cvss_score = cvss_from_risk_level(risk_level)
            recommendations = generate_recommendations_name(vulnerability_name)

            print(f"Host: {target}")
            print(f"Vulnerability Name: {vulnerability_name}")
            print(f"Risk Level: {risk_level}")
            print(f"CVSS Score: {cvss_score}")
            print(f"Details: {details}")
            print(f"Timestamp: {timestamp}")
            print(f"Commands: {', '.join(commands)}")
            print(f"Recommendations: {recommendations}")
            print("")


def smod1_report(file_path, output_file):
    """
    Processes the input Smod-1 XML file and generates an Smod-1 report XML.
    """
    try:
        tree, root = load_xml(file_path)

        if root is not None:
            report_tree = generate_smod1_report(root)
            report_tree.write(output_file, encoding='utf-8', xml_declaration=True)
            print(f"Report generated successfully and saved to {output_file}")

        else:
            print_failed_to_load_file()

    except Exception as e:
        print_error_processing_report(e)
