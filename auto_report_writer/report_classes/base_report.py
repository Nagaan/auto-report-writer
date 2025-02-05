from auto_report_writer.utils.xml_loader import load_xml
from auto_report_writer.utils.custom_logger import logger


class BaseReport:
    """
    BaseReport is an abstract base class for generating reformatted XML reports from input XML data.

    This class provides the basic structure and methods for loading input XML files,
    generating reports, and saving the output. Subclasses should implement the
    generate_report method to define how the report is created.

    Subclass .py files should be named [root-element]_report.py.
    Subclasses should be named [RootElement]Report(BaseReport).

    In most cases, the root element of an XML file output by a penetration testing
    tool will be the name of the penetration testing tool, 'metasploit', for example,
    would be 'metasploit_report.py', as its root element should be <metasploit>.

    Example:
        class [RootElement]Report(BaseReport):
            def generate_report(self):
                report = Element('root-element_report')
                # Implement report formatting logic here.
                return ElementTree(report)

    The following template should be followed when formatting the XML:
        Vulnerability Name: [Name of the vulnerability/exploit]
            Risk Level: [If not already in the report to extract, use determine_classification.py: risk_level_from_name]
            CVSS Score: [If not already in the report to extract, use determine_classification.py: cvss_from_risk_level]
            Vulnerability Details: [All other relevant elements of the vulnerability/exploit and their details/information listed below]
                • {Element Name}: [Information extracted from related element name]

    :param file_path: (str) Path to the input XML file.
    :param output_file: (str) Path where the output XML file will be saved.
    """

    def __init__(self, file_path, output_file):
        """
        Initialises the BaseReport class instance with the given file path and output file path.

        :param file_path: (str) Path to the input XML file.
        :param output_file: (str) Path where the output XML file will be saved.
        """
        self.file_path = file_path  # Assigning the file path to the instance attribute.
        self.output_file = output_file  # Assigning the output path to the instance attribute.
        self.tree, self.root = load_xml(file_path)  # Loading the input XML file and setting the tree and root instance attributes.

    def generate_report(self):
        """
        Generates the class report. This method should be implemented by subclasses.

        :return: Should return an ElementTree representing the report.
        :raises NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement generate_report method.")

    def save_report(self, report_tree):
        """
        Saves the generated class report to the specified output file.

        :param report_tree: An ElementTree representing the class report.
        """
        try:
            report_tree.write(self.output_file, encoding='utf-8', xml_declaration=True)
        except Exception as e:
            logger.error(f"Error processing report class: {e}")

    def run(self):
        """
        Runs the class report generation process.
        """
        if self.root is not None:
            report_tree = self.generate_report()
            self.save_report(report_tree)
        else:
            logger.warn("Failed to load the XML file. No class report generated.")
