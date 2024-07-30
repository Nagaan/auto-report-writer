import os
import tkinter as tk
from tkinter import filedialog, messagebox
from fuzzywuzzy import process

from auto_report_writer.utils.custom_logger import logger
from auto_report_writer.utils.html_combiner import html_combiner
from auto_report_writer.utils.xml_to_html import xml_to_html
from auto_report_writer.utils.xml_loader import load_xml
from auto_report_writer.utils.html_to_docx import convert_html_to_docx
from auto_report_writer.utils.html_to_pdf import convert_html_to_pdf
from auto_report_writer.utils.import_directory import import_directory
from auto_report_writer.graph_generator import generate_graph_from_html
from auto_report_writer.summary_generator import generate_summary_from_html


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


def ask_user_conversion_options():
    """
    Custom dialog with buttons to ask the user what conversion to perform.
    Returns 'docx', 'pdf', or 'both' based on user selection.
    If the dialog is closed, it returns None.
    """
    def on_button_click(choice):
        nonlocal user_choice
        user_choice = choice  # Set the user's choice
        dialog.quit()  # Close the dialog

    # Create a new Tkinter window
    dialog = tk.Tk()
    dialog.title("Convert Report")

    # Center the dialog on the screen
    dialog_width = 400
    dialog_height = 100
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width // 2) - (dialog_width // 2)
    y = (screen_height // 2) - (dialog_height // 2)
    dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')

    user_choice = None  # Variable to store user choice

    # Create a label above the buttons
    label = tk.Label(dialog, text="The report has been generated as HTML.\nAlso generate the report as...", wraplength=300)
    label.pack(pady=10)

    # Frame for buttons
    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    # Create buttons for each conversion option and place them side by side
    pdf_button = tk.Button(button_frame, text="PDF", command=lambda: on_button_click('pdf'), width=10)
    pdf_button.pack(side=tk.LEFT, padx=5)

    docx_button = tk.Button(button_frame, text="DOCX", command=lambda: on_button_click('docx'), width=10)
    docx_button.pack(side=tk.LEFT, padx=5)

    both_button = tk.Button(button_frame, text="Both", command=lambda: on_button_click('both'), width=10)
    both_button.pack(side=tk.LEFT, padx=5)

    dialog.protocol("WM_DELETE_WINDOW", dialog.quit)  # Handle window close

    # Start the Tkinter main loop
    dialog.mainloop()

    return user_choice  # Return None if no choice is made (dialog closed)


def report_generator():
    file_paths = get_file_paths("Select one or more XML files")

    if file_paths:
        xml_dir = './reports/XML'
        xsl_dir = './reports/XSL'
        html_dir = './reports/HTML'
        create_output_dir(xml_dir)
        create_output_dir(xsl_dir)
        create_output_dir(html_dir)

        report_classes_dir = './auto_report_writer/report_classes'
        report_classes = load_report_classes_from_dir(report_classes_dir)

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
                generate_graph_from_html(combined_htmls)

                # Generate the project summary
                generate_summary_from_html(combined_html, report_type_list)

                # Ask the user how they want to convert the HTML
                conversion_choice = ask_user_conversion_options()  # noqa: "doesn't return anything" error.

                # Only perform conversions if the user made a choice
                if conversion_choice is not None:
                    # Define output file paths
                    combined_docx = './reports/combined_report.docx'
                    combined_pdf = './reports/combined_report.pdf'

                    # Perform conversions based on user's choice
                    if conversion_choice == "docx":
                        convert_html_to_docx(combined_html, combined_docx)
                    elif conversion_choice == "pdf":
                        convert_html_to_pdf(combined_html, combined_pdf)
                    elif conversion_choice == "both":
                        convert_html_to_docx(combined_html, combined_docx)
                        convert_html_to_pdf(combined_html, combined_pdf)

            except Exception as e:
                logger.error(f"Error combining HTML reports: {e}")
        else:
            print("No valid report types found. No reports were generated.")
            messagebox.showinfo("No Reports Generated", "No valid reports found. No combined report was generated.")
    else:
        print("No files selected. No reports will be generated.")
        messagebox.showinfo("No Files Selected", "No files selected. No reports will be generated.")
