import re
from xml.etree.ElementTree import ElementTree, Element, SubElement

from auto_report_writing.report_generation.determine_classification import cvss_from_risk_level, risk_level_from_name
from auto_report_writing.report_generation.report_templates.base_report import BaseReport


class NmapReport(BaseReport):
    def generate_report(self):
        report = Element('nmap_report')

        for host in self.root.findall('.//host'):
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
