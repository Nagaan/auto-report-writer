# Report Generation Messages


def print_combined_report_generated(path):
    print(f"Combined HTML report generated and saved as '{path}'.")


def print_xml_report_generated(output_xml):
    print(f"XML report generated and saved as '{output_xml}'.")


def print_html_report_generated(output_html):
    print(f"HTML report generated and saved as '{output_html}'.")


def print_generating_report(report_type, file_path):
    print(f"Generating {report_type.capitalize()} report from {file_path}...")


# Error Handling Messages
def print_error_converting_xml_to_html(error_message):
    print(f"Error converting XML to HTML: {error_message}")


def print_error_parsing_xml(error_message):
    print(f"Error parsing XML file: {error_message}")


def print_error_combining_html(error_message):
    print(f"Error combining HTML reports: {error_message}")


def print_error_processing_report(error_message):
    print(f"Error processing report: {error_message}")


def print_failed_to_load_file():
    print("Failed to load the XML file.")


# File Status Messages
def print_no_files_selected():
    print("No files selected. No reports will be generated.")


def print_file_not_found(file_path):
    print(f"File not found: {file_path}")


def print_no_reports_generated():
    print("No valid report types found. No reports were generated.")


def print_error_generating_graph(error):
    print(error)


def print_unknown_report_type(file_path):
    print(f"Unknown XML format or root element in file: {file_path}")
