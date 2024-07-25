from xml.etree.ElementTree import Element, SubElement, ElementTree
import re
from auto_report_writing.data_processing.xml_loader import load_xml
from auto_report_writing.report_generation.determine_classification import cvss_from_risk_level, risk_level_from_name
from auto_report_writing.utils.message_utils import *

def generate_nmap_report(root):
    """
    Generates an XML structure with details of services for each host.
    """
    report = Element('nmap_report')

    for host in root.findall('.//host'):
        address = host.find('.//address[@addrtype="ipv4"]').get('addr')
        host_element = SubElement(report, 'host')
        SubElement(host_element, 'address', addr=address)

        services = host.findall('.//port')
        for service in services:
            port_id = service.get('portid')
            port_protocol = service.get('protocol').upper()
            state = service.find('state').get('state').capitalize()
            service_elem = service.find('service')
            product = service_elem.get('product') if service_elem is not None else 'N/A'
            service_name = service_elem.get('name').upper() if service_elem is not None else 'N/A'

            scripts = service.findall('script')
            for script in scripts:
                script_id = script.get('id').capitalize()
                script_output = script.get('output')

                # Format script output preserving important details
                formatted_script_output = re.sub(r'&lt;br/&gt;', '\n', script_output.strip())
                formatted_script_output = re.sub(r'\s{2,}', ' ', formatted_script_output)

                # Determine risk level, CVSS score.
                risk_level = risk_level_from_name(script_id)
                cvss_score = cvss_from_risk_level(risk_level)

                # Create the service element and its sub-elements
                service_element = SubElement(host_element, 'service', portid=port_id, protocol=port_protocol)
                SubElement(service_element, 'state').text = state
                SubElement(service_element, 'product').text = product
                SubElement(service_element, 'name').text = service_name
                SubElement(service_element, 'vulnerabilities').text = formatted_script_output

                # Add vulnerability details
                vulnerability_element = SubElement(service_element, 'vulnerability', id=script_id)
                SubElement(vulnerability_element, 'risk_level').text = risk_level
                SubElement(vulnerability_element, 'cvss_score').text = str(cvss_score)

    return ElementTree(report)

def count_hosts(root):
    """
    Counts the number of hosts in the given Nmap XML root.
    """
    return len(root.findall('.//host'))

def count_services_per_host(root):
    """
    Counts the number of vulnerable services (ports) for each host (IP) in the given Nmap XML root.
    """
    host_service_counts = []

    for host in root.findall('.//host'):
        host_address = host.find('.//address[@addrtype="ipv4"]').get('addr')
        services = host.findall('.//port')

        service_count = sum(1 for service in services if service.find('script') is not None)
        host_service_counts.append((host_address, service_count))

    return host_service_counts

def print_nmap_details(root):
    """
    Prints details for open services with vulnerabilities for each host.
    """
    host_count = count_hosts(root)
    services_per_host = count_services_per_host(root)
    total_services_per_host = sum(service_count for _, service_count in services_per_host)
    print_service_report_details(host_count, total_services_per_host)

    for host_address, service_count in services_per_host:
        print_service_details_for_host(host_address, service_count)

        for host in root.findall('.//host'):
            address = host.find('.//address[@addrtype="ipv4"]').get('addr')

            if address == host_address:
                services = host.findall('.//port')

                for service in services:
                    scripts = service.findall('script')
                    service_element = service.find('service')

                    for script in scripts:
                        port_id = service.get('portid')
                        port_protocol = service.get('protocol').upper()
                        state = service.find('state').get('state').capitalize()
                        product = service_element.get('product') if service_element is not None else 'N/A'
                        service_name = service_element.get('name').upper() if service_element is not None else 'N/A'

                        script_id = script.get('id').capitalize()
                        script_output = script.get('output')

                        formatted_script_output = re.sub(r'&lt;br/&gt;', '\n', script_output.strip())
                        formatted_script_output = re.sub(r'\s{2,}', ' ', formatted_script_output)

                        risk_classification = risk_level_from_name(script_id)
                        cvss_score = cvss_from_risk_level(risk_classification)

                        print_service_vulnerability_details(
                            script_id, risk_classification, cvss_score, port_id, port_protocol,
                            state, product, service_name, formatted_script_output
                        )

                break

        else:
            print_no_services_found(host_address)

def nmap_report(file_path, output_file):
    """
    Processes the input Nmap XML file and generates an Nmap report XML.
    """
    try:
        tree, root = load_xml(file_path)

        if root is not None:
            report_tree = generate_nmap_report(root)
            report_tree.write(output_file, encoding='utf-8', xml_declaration=True)

        else:
            print_failed_to_load_file()

    except Exception as e:
        print_error_processing_report(e)
