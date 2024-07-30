from xml.etree.ElementTree import Element, SubElement, ElementTree

from auto_report_writer.report_classes.base_report import BaseReport
from auto_report_writer.utils.determine_classification import cvss_from_risk_level, risk_level_from_name


class Smod1Report(BaseReport):
    def generate_report(self):
        """
        Generates an XML structure with details of exploitation attempts where the result is not 'Failed'.
        """
        report = Element('smod1_report')

        for attempt in self.root.findall('.//attempt'):
            result = attempt.find('result').text
            if result != 'Failed':
                target = attempt.find('target').text
                vulnerability_name = attempt.find('vulnerability').text
                timestamp = attempt.find('timestamp').text
                details = attempt.find('details').text
                commands = attempt.findall('commands/command')

                risk_level = risk_level_from_name(vulnerability_name)
                cvss_score = cvss_from_risk_level(risk_level)

                attempt_element = SubElement(report, 'attempt', id=attempt.get('id'))
                SubElement(attempt_element, 'target').text = target
                SubElement(attempt_element, 'vulnerability').text = vulnerability_name
                SubElement(attempt_element, 'risk_level').text = risk_level
                SubElement(attempt_element, 'cvss_score').text = f"{cvss_score}"

                details_element = SubElement(attempt_element, 'vulnerability_details')
                SubElement(details_element, 'details').text = details
                SubElement(details_element, 'timestamp').text = f"Timestamp: {timestamp}"

                commands_element = SubElement(attempt_element, 'commands')
                for command in commands:
                    SubElement(commands_element, 'command').text = command.text

        return ElementTree(report)
