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


def get_file_paths(prompt: str) -> list[str]:
    """
    Opens a file dialog to select multiple XML files.

    :param prompt: (str) The title of the file dialog.
    :return: (list[str]) A list of selected file paths.
    """
    root = tk.Tk()
    root.withdraw()  # Hides the root window.
    file_paths = filedialog.askopenfilenames(title=prompt, filetypes=[("XML Files", "*.xml")])
    return list(file_paths)


def create_output_dir(path: str) -> None:
    """
    Creates an output directory if it does not exist.

    :param path: (str) The path to the directory to create.
    """
    if not os.path.exists(path):
        os.makedirs(path)  # Create the directory.


def load_report_classes_from_dir(directory: str) -> dict[str, type]:
    """
    Loads report classes from Python modules in the specified directory.

    :param directory: (str) Path to the directory containing report class modules.
    :return: (dict[str, type]) A dictionary of report class names and their corresponding classes.
    """
    report_classes = {}
    modules = import_directory(directory)  # Import all modules in the directory.

    for module_name, module in modules.items():
        # Extracts classes from the module.
        classes = {name: obj for name, obj in module.__dict__.items() if isinstance(obj, type)}

        # Constructs the expected report class name.
        report_class_name = f"{module_name.replace('_report', '').capitalize()}Report"
        report_class = classes.get(report_class_name)

        if report_class:
            report_classes[report_class_name] = report_class  # Store the report class.
            logger.info(f"Loaded report class: {report_class_name} from module {module_name}")
        else:
            logger.warn(f"No report class named {report_class_name} found in module {module_name}")

    return report_classes


def generate_file_names(report_type: str) -> dict[str, str]:
    """
    Generates standardised file names for report-related files.

    :param report_type: (str) The type of report (used to create base names).
    :return: (dict[str, str]) A dictionary containing standardised file names for XML, XSL, and HTML files.
    """
    base_name = f"{report_type.lower()}_report"  # Base name for the report files.
    return {
        'xml_file': f"{base_name}.xml",
        'xsl_file': f"{base_name}.xsl",
        'html_file': f"{base_name}.html"
    }


def process_report(report_type: str, file_path: str, xml_dir: str, xsl_dir: str, html_dir: str,
                   report_classes: dict[str, type], report_type_list: list[str]) -> str:
    """
    Processes a report based on the provided type and file path.

    :param report_type: (str) The type of report to generate.
    :param file_path: (str) Path to the input XML file.
    :param xml_dir: (str) Directory to save the generated XML report.
    :param xsl_dir: (str) Directory containing the XSL templates.
    :param html_dir: (str) Directory to save the generated HTML report.
    :param report_classes: (dict[str, type]) A dictionary of report classes.
    :param report_type_list: (list[str]) A list to store the types of reports generated.
    :return: (str) Path to the generated HTML report.
    :raises ValueError: If no matching report class is found.
    :raises FileNotFoundError: If the generated XML file is not found.
    """
    available_classes = list(report_classes.keys())  # List of available report classes.
    closest_match, score = process.extractOne(report_type, available_classes)  # Fuzzy match.

    if closest_match and score > 50:  # Check for a good enough match.
        report_class = report_classes.get(closest_match)
        if report_class:
            logger.info(f"Using report class: {closest_match} with a score of {score}")
            file_names = generate_file_names(closest_match.replace('Report', ''))
            output_xml = os.path.join(xml_dir, file_names['xml_file'])
            input_xsl = os.path.join(xsl_dir, file_names['xsl_file'])
            output_html = os.path.join(html_dir, file_names['html_file'])

            logger.info(f"Generating {closest_match} report from {file_path}...")
            report_instance = report_class(file_path, output_xml)  # Instantiate the report class.
            report_instance.run()  # Run the report generation process.

            if os.path.exists(output_xml):  # Check if the XML file was generated successfully.
                xml_to_html(output_xml, input_xsl, output_html)  # Convert XML to HTML.
                logger.info(f"XML report generated and saved as '{output_xml}'.")
                logger.info(f"HTML report generated and saved as '{output_html}'.")

                report_type_list.append(closest_match.replace('Report', ''))  # Store the report type.
                return output_html  # Return the path to the generated HTML report.
            else:
                raise FileNotFoundError(logger.error(f"Generated XML file not found: {output_xml}"))
        else:
            raise ValueError(logger.error(f"Class not found for report type: {closest_match}"))
    else:
        raise ValueError(logger.error(f"No matching report class found for report type: {report_type}"))


def ask_user_conversion_options() -> str | None:
    """
    Custom dialog to ask the user what conversion to perform (DOCX, PDF, or both).

    :return: (str | None) The user's choice of conversion, or None if the dialog is closed.
    """
    def on_button_click(choice: str):
        nonlocal user_choice
        user_choice = choice  # Set the user's choice.
        dialog.quit()  # Close the dialog.

    # Create a new Tkinter window for the dialog.
    dialog = tk.Tk()
    dialog.title("Convert Report")

    # Center the dialog on the screen.
    dialog_width = 400
    dialog_height = 100
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width // 2) - (dialog_width // 2)
    y = (screen_height // 2) - (dialog_height // 2)
    dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')

    user_choice = None  # Variable to store user choice.

    # Create a label above the buttons.
    label = tk.Label(dialog, text="The report has been generated as HTML.\nAlso generate the report as...", wraplength=300)
    label.pack(pady=10)

    # Frame for buttons.
    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    # Create buttons for each conversion option.
    pdf_button = tk.Button(button_frame, text="PDF", command=lambda: on_button_click('pdf'), width=10)
    pdf_button.pack(side=tk.LEFT, padx=5)

    docx_button = tk.Button(button_frame, text="DOCX", command=lambda: on_button_click('docx'), width=10)
    docx_button.pack(side=tk.LEFT, padx=5)

    both_button = tk.Button(button_frame, text="Both", command=lambda: on_button_click('both'), width=10)
    both_button.pack(side=tk.LEFT, padx=5)

    dialog.protocol("WM_DELETE_WINDOW", dialog.quit)  # Handle window close.

    # Start the Tkinter main loop.
    dialog.mainloop()

    return user_choice  # Return the user's choice.


def report_generator() -> None:
    """
    Main function to generate reports based on selected XML files.

    This function orchestrates the loading of report classes, processing of each XML file,
    and conversion of the generated HTML report into desired formats (DOCX, PDF).
    """
    file_paths = get_file_paths("Select one or more XML files")

    if file_paths:
        # Define directories for storing generated reports.
        xml_dir = './reports/XML'
        xsl_dir = './reports/XSL'
        html_dir = './reports/HTML'
        create_output_dir(xml_dir)  # Create XML output directory.
        create_output_dir(xsl_dir)   # Create XSL output directory.
        create_output_dir(html_dir)   # Create HTML output directory.

        report_classes_dir = './auto_report_writer/report_classes'
        report_classes = load_report_classes_from_dir(report_classes_dir)  # Load report classes.

        html_files = []  # List to store paths of generated HTML files.
        report_type_list = []  # Initialise the list to store report types.

        for file_path in file_paths:
            _, root = load_xml(file_path)  # Load XML file and get the root element.
            if root is not None:
                report_type = root.tag  # Extract report type from the root element.
                logger.info(f"Detected report type: {report_type}")
                try:
                    # Process the report and generate the corresponding HTML file.
                    html_file = process_report(report_type, file_path, xml_dir, xsl_dir, html_dir, report_classes, report_type_list)
                    html_files.append(html_file)  # Store the generated HTML file.
                except ValueError as e:
                    logger.error(f"Error: {e}")
                except FileNotFoundError as e:
                    logger.error(f"File not found: {e}")
            else:
                logger.warn(f"Could not determine report type for file: {file_path}")

        if html_files:
            combined_html = './reports/combined_report.html'  # Path for the combined HTML report.
            try:
                # Create the combined HTML report.
                html_combiner(html_files, combined_html)
                logger.info(f"Combined HTML report generated and saved as '{combined_html}'.")

                # Extract risk data and generate a graph.
                generate_graph_from_html(combined_html)

                # Generate the project summary based on the combined HTML.
                generate_summary_from_html(combined_html, report_type_list)

                # Ask the user how they want to convert the HTML report.
                conversion_choice = ask_user_conversion_options()

                # Only perform conversions if the user made a choice.
                if conversion_choice is not None:
                    # Define output file paths for conversions.
                    combined_docx = './reports/combined_report.docx'
                    combined_pdf = './reports/combined_report.pdf'

                    # Perform conversions based on user's choice.
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
            logger.warn("No valid report types found. No reports were generated.")
            messagebox.showinfo("No Reports Generated", "No valid reports found. No combined report was generated.")

    else:
        logger.warn("No files selected. No reports will be generated.")
        messagebox.showinfo("No Files Selected", "No files selected. No reports will be generated.")
