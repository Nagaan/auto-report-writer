import os
import sys
import xml.etree.ElementTree as EleTree
import tkinter as tk
from tkinter import filedialog, messagebox
from fuzzywuzzy import process

# Adding the parent directory to the system PATH.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from auto_report_writing.data_processing.html_combiner import html_combiner
from auto_report_writing.data_processing.graph_generator import generate_graph_from_html
from auto_report_writing.data_processing.xml_to_html import xml_to_html
from auto_report_writing.data_processing.xml_loader import load_xml
from auto_report_writing.utils.message_utils import *
from auto_report_writing.data_processing.import_directory import import_directory


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
        return root
    except EleTree.ParseError as e:
        print_error_parsing_xml(e)
        return None


def create_output_dir(path):
    """
    Create the output directory if it doesn't exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def load_report_functions_from_dir(directory):
    """
    Load and register report functions from the specified directory.
    """
    report_functions = {}
    modules = import_directory(directory)

    for module_name, module in modules.items():
        # Functions available in the module. Print for debugging.
        functions = {name: obj for name, obj in module.__dict__.items() if callable(obj)}

        # Determine the function name to use
        report_func_name = f"{module_name}"  # Matches the exact name in modules
        report_func = functions.get(report_func_name)

        if report_func:
            report_functions[report_func_name] = report_func
            print(f"Loaded report function: {report_func_name} from module {module_name}")
        else:
            print(f"No report function named {report_func_name} found in module {module_name}")

    return report_functions


def generate_file_names(report_type):
    """
    Generate file names dynamically based on the report type.
    """
    base_name = f"{report_type}_report"
    return {
        'xml_file': f"{base_name}.xml",
        'xsl_file': f"{base_name}.xsl",
        'html_file': f"{base_name}.html"
    }


def process_report(report_type, file_path, xml_dir, xsl_dir, html_dir, report_functions):
    """
    Process a report by generating XML and HTML files based on the report type.
    """
    # Use fuzzy matching to find the closest matching report function
    available_functions = list(report_functions.keys())
    closest_match, score = process.extractOne(report_type, available_functions)

    if closest_match and score > 50:  # Threshold can be adjusted
        report_func = report_functions.get(closest_match)
        if report_func:
            print(f"Using report function: {closest_match} with a score of {score}")
            file_names = generate_file_names(closest_match.replace('_report', ''))
            output_xml = os.path.join(xml_dir, file_names['xml_file'])
            input_xsl = os.path.join(xsl_dir, file_names['xsl_file'])
            output_html = os.path.join(html_dir, file_names['html_file'])

            print_generating_report(closest_match, file_path)
            try:
                report_func(file_path, output_xml)

                if os.path.exists(output_xml):
                    xml_to_html(output_xml, input_xsl, output_html)
                    print_xml_report_generated(output_xml)
                    print_html_report_generated(output_html)
                    return output_html
                else:
                    raise FileNotFoundError(f"Generated XML file not found: {output_xml}")
            except Exception as e:
                print(f"Error processing report function: {e}")
                raise
        else:
            raise ValueError(f"Function not found for report type: {closest_match}")
    else:
        raise ValueError(f"No matching report function found for report type: {report_type}")


def main():
    file_paths = get_file_paths("Select one or more XML files")

    if file_paths:
        xml_dir = '../../auto_report_writing/report_generation/reports/XML'
        xsl_dir = '../../auto_report_writing/report_generation/reports/XSL'
        html_dir = '../../auto_report_writing/report_generation/reports/HTML'
        create_output_dir(xml_dir)
        create_output_dir(xsl_dir)
        create_output_dir(html_dir)

        # Load report functions dynamically from the report_templates directory
        report_templates_dir = 'auto_report_writing/report_generation/report_templates'
        report_functions = load_report_functions_from_dir(report_templates_dir)

        html_files = []

        for file_path in file_paths:
            _, root = load_xml(file_path)
            if root is not None:
                report_type = root.tag
                print(f"Detected report type: {report_type}")  # Debug print statement
                try:
                    html_file = process_report(report_type, file_path, xml_dir, xsl_dir, html_dir, report_functions)
                    html_files.append(html_file)
                except ValueError as e:
                    print(f"Error: {e}")
                except FileNotFoundError as e:
                    print(f"File error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
            else:
                print(f"Could not determine report type for file: {file_path}")

        if html_files:
            combined_html = 'reports/combined_report.html'
            try:
                html_combiner(html_files, combined_html)
                print_combined_report_generated(combined_html)
                try:
                    generate_graph_from_html(combined_html)
                except Exception as e:
                    print_error_generating_graph(e)
            except Exception as e:
                print_error_combining_html(e)
        else:
            print_no_reports_generated()
            messagebox.showinfo("No Reports Generated", "No valid reports found. No combined report was generated.")
    else:
        print_no_files_selected()
        messagebox.showinfo("No Files Selected", "No files selected. No reports will be generated.")


if __name__ == '__main__':
    main()
