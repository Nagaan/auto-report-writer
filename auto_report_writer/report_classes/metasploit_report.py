from xml.etree.ElementTree import ElementTree, Element, SubElement

from auto_report_writer.utils.determine_classification import cvss_from_risk_level
from auto_report_writer.report_classes.base_report import BaseReport


class MetasploitReport(BaseReport):
    def generate_report(self):
        report = Element('metasploit_report')

        for host in self.root.findall('.//host'):
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
