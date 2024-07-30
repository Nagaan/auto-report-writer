import os
import tkinter as tk
from tkinter import filedialog, messagebox
from fuzzywuzzy import process

from auto_report_writing.data_processing.html_combiner import html_combiner
from auto_report_writing.data_processing.xml_to_html import xml_to_html
from auto_report_writing.data_processing.xml_loader import load_xml
from auto_report_writing.data_processing.html_to_docx import convert_html_to_docx
from auto_report_writing.data_processing.import_directory import import_directory
from auto_report_writing.utils.graph_generator import generate_graph_from_html
from auto_report_writing.utils.summary_generator import generate_summary_from_html


def get_file_paths(prompt):
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title=prompt, filetypes=[("XML Files", "*.xml")])
    return list(file_paths)


def create_output_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def load_report_classes_from_dir(directory):
    report_classes = {}
    modules = import_directory(directory)

    for module_name, module in modules.items():
        classes = {name: obj for name, obj in module.__dict__.items() if isinstance(obj, type)}

        report_class_name = f"{module_name.replace('_report', '').capitalize()}Report"
        report_class = classes.get(report_class_name)

        if report_class:
            report_classes[report_class_name] = report_class
            print(f"Loaded report class: {report_class_name} from module {module_name}")
        else:
            print(f"No report class named {report_class_name} found in module {module_name}")

    return report_classes


def generate_file_names(report_type):
    base_name = f"{report_type.lower()}_report"
    return {
        'xml_file': f"{base_name}.xml",
        'xsl_file': f"{base_name}.xsl",
        'html_file': f"{base_name}.html"
    }


def process_report(report_type, file_path, xml_dir, xsl_dir, html_dir, report_classes, report_type_list):
    available_classes = list(report_classes.keys())
    closest_match, score = process.extractOne(report_type, available_classes)

    if closest_match and score > 50:
        report_class = report_classes.get(closest_match)
        if report_class:
            print(f"Using report class: {closest_match} with a score of {score}")
            file_names = generate_file_names(closest_match.replace('Report', ''))
            output_xml = os.path.join(xml_dir, file_names['xml_file'])
            input_xsl = os.path.join(xsl_dir, file_names['xsl_file'])
            output_html = os.path.join(html_dir, file_names['html_file'])

            print(f"Generating {closest_match} report from {file_path}...")
            report_instance = report_class(file_path, output_xml)
            report_instance.run()

            if os.path.exists(output_xml):
                xml_to_html(output_xml, input_xsl, output_html)
                print(f"XML report generated and saved as '{output_xml}'.")
                print(f"HTML report generated and saved as '{output_html}'.")

                # Append the report type to the report_type_list
                report_type_list.append(closest_match.replace('Report', ''))  # Store the report type without 'Report' suffix

                return output_html
            else:
                raise FileNotFoundError(f"Generated XML file not found: {output_xml}")
        else:
            raise ValueError(f"Class not found for report type: {closest_match}")
    else:
        raise ValueError(f"No matching report class found for report type: {report_type}")


def report_generator():
    file_paths = get_file_paths("Select one or more XML files")

    if file_paths:
        xml_dir = './reports/XML'
        xsl_dir = './reports/XSL'
        html_dir = './reports/HTML'
        create_output_dir(xml_dir)
        create_output_dir(xsl_dir)
        create_output_dir(html_dir)

        report_templates_dir = 'auto_report_writing/report_generation/report_templates'
        report_classes = load_report_classes_from_dir(report_templates_dir)

        html_files = []
        report_type_list = []  # Initialize the list to store report types

        for file_path in file_paths:
            _, root = load_xml(file_path)
            if root is not None:
                report_type = root.tag
                print(f"Detected report type: {report_type}")
                try:
                    html_file = process_report(report_type, file_path, xml_dir, xsl_dir, html_dir, report_classes, report_type_list)
                    html_files.append(html_file)
                except ValueError as e:
                    print(f"Error: {e}")
                except FileNotFoundError as e:
                    print(f"File error: {e}")
            else:
                print(f"Could not determine report type for file: {file_path}")

        if html_files:
            combined_html = './reports/combined_report.html'
            try:
                # Create the combined HTML report
                html_combiner(html_files, combined_html)
                print(f"Combined HTML report generated and saved as '{combined_html}'.")

                # Extract risk data and generate a graph
                generate_graph_from_html(combined_html)

                # Generate the project summary
                generate_summary_from_html(combined_html, report_type_list)  # Pass the report type list

                # Output docx file.
                combined_docx = './reports/combined_report.docx'
                convert_html_to_docx(combined_html, combined_docx)

            except Exception as e:
                print(f"Error combining HTML reports: {e}")
        else:
            print("No valid report types found. No reports were generated.")
            messagebox.showinfo("No Reports Generated", "No valid reports found. No combined report was generated.")
    else:
        print("No files selected. No reports will be generated.")
        messagebox.showinfo("No Files Selected", "No files selected. No reports will be generated.")
