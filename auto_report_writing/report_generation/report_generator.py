import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as EleTree

# Adding the parent directory to the system PATH.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from auto_report_writing.report_generation.report_templates.metasploit_report import metasploit_report
from auto_report_writing.report_generation.report_templates.nmap_report import nmap_report
from auto_report_writing.report_generation.report_templates.smod1_report import smod1_report
from auto_report_writing.data_processing.xml_to_html import xml_to_html
from auto_report_writing.data_processing.html_combiner import *
from auto_report_writing.utils.message_utils import *


def get_file_paths(prompt):
    """
    Open a file dialog to get one or more file paths from the user.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window.
    file_paths = filedialog.askopenfilenames(title=prompt, filetypes=[("XML Files", "*.xml")])
    return list(file_paths)


def determine_report_type(file_path):
    """
    Determine the type of report based on the XML file content.
    """
    try:
        tree = EleTree.parse(file_path)
        root = tree.getroot()

        # Identifying the report type based on the name of the root element.
        if 'metasploit' in root.tag.lower():
            return 'metasploit'
        elif 'nmap' in root.tag.lower():
            return 'nmap'
        elif 'smod-1' in root.tag.lower():
            return 'smod-1'
        else:
            print_unknown_report_type(file_path)
            return None

    except EleTree.ParseError as e:
        print_error_parsing_xml(e)
        return None


def create_output_dir(path):
    """
    Create the output directory if it doesn't exist.
    :param path: The directory to be checked and created.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    # Prompting the user for one or more XML file paths.
    file_paths = get_file_paths("Select one or more XML files")

    if file_paths:
        # Creating the output directories if they don't exist.
        xml_dir = 'Reports/XML'
        xsl_dir = 'Reports/XSL'
        html_dir = 'Reports/HTML'
        create_output_dir(xml_dir)
        create_output_dir(xsl_dir)
        create_output_dir(html_dir)

        # Tracking the generated HTML files to combine them.
        html_files = []

        for file_path in file_paths:
            # Determining the report type based on the XML root element.
            report_type = determine_report_type(file_path)

            # For handling Metasploit report data.
            if report_type == 'metasploit':
                print_generating_report(report_type, file_path)

                output_xml = os.path.join(xml_dir, 'Metasploit_Report.xml')
                input_xsl = os.path.join(xsl_dir, 'Metasploit_Report.xsl')
                output_html = os.path.join(html_dir, 'Metasploit_Report.html')

                metasploit_report(file_path, output_xml)
                xml_to_html(output_xml, input_xsl, output_html)
                html_files.append(output_html)

                print_xml_report_generated(output_xml)
                print_html_report_generated(output_html)

            # For handling Nmap report data.
            elif report_type == 'nmap':
                print_generating_report(report_type, file_path)

                output_xml = os.path.join(xml_dir, 'Nmap_Report.xml')
                input_xsl = os.path.join(xsl_dir, 'Nmap_Report.xsl')
                output_html = os.path.join(html_dir, 'Nmap_Report.html')

                nmap_report(file_path, output_xml)
                xml_to_html(output_xml, input_xsl, output_html)
                html_files.append(output_html)

                print_xml_report_generated(output_xml)
                print_html_report_generated(output_html)

            # For handling Smod-1 report data.
            elif report_type == 'smod-1':
                print_generating_report(report_type, file_path)

                output_xml = os.path.join(xml_dir, 'Smod-1_Report.xml')
                input_xsl = os.path.join(xsl_dir, 'Smod-1_Report.xsl')
                output_html = os.path.join(html_dir, 'Smod-1_Report.html')

                smod1_report(file_path, output_xml)
                xml_to_html(output_xml, input_xsl, output_html)
                html_files.append(output_html)

                print_xml_report_generated(output_xml)
                print_html_report_generated(output_html)

        if html_files:
            combined_html = 'Reports/Combined_Report.html'

            generate_combined_html_with_graph(html_files, combined_html)
            print_combined_report_generated(combined_html)

        else:
            print_no_reports_generated()
            messagebox.showinfo("No Reports Generated", "No valid reports found. No combined report was generated.")

    else:
        print_no_files_selected()
        messagebox.showinfo("No Files Selected", "No files selected. No reports will be generated.")


if __name__ == '__main__':
    main()
