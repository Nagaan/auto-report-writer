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


def print_unknown_report_type(file_path):
    print(f"Unknown XML format or root element in file: {file_path}")


# Metasploit Report Details
def print_exploit_report_details(host_count, total_exploits_per_host):
    print(f"Metasploit has detected {host_count} hosts with a total of {total_exploits_per_host} exploits.")


def print_exploit_details_for_host(host_address, exploit_count):
    print(f"\n[{host_address}] has {exploit_count} vulnerabilities:")


def print_vulnerability_details(name, risk, csvv, description, result, recommendations):
    print(f"Vulnerability Name: {name}")
    print(f"Risk Level: {risk}")
    print(f"CSVV Score: {csvv} (estimated from risk level)")
    print(f"Vulnerability Details: ")
    print(f"\t Description: {description}")
    print(f"\t Result: {result}.")
    print(f"Recommendations: {recommendations}")
    print("")


def print_no_exploits_found(host_address):
    print(f"No exploits found for host: {host_address}.")


# Nmap Report Details
def print_service_report_details(host_count, total_services_per_host):
    print(f"Nmap has detected {host_count} hosts with a total of {total_services_per_host} vulnerable services.")


def print_service_details_for_host(host_address, service_count):
    print(f"\n[{host_address}] has {service_count} vulnerable services:")


def print_service_vulnerability_details(script_id, risk_classification, csvv_score, port_id, port_protocol, state, product, service_name, script_output_formatted, recommendations):
    print(f"Vulnerability Name: {script_id}")
    print(f"Risk Level: {risk_classification}")
    print(f"CSVV Score: {csvv_score}")
    print(f"Vulnerability Details: ")
    print(f"\t Port: {port_id} ({port_protocol})")
    print(f"\t State: {state}")
    print(f"\t Product: {product}")
    print(f"\t Service: {service_name}")
    print(f"\t Vulnerabilities: \n\t\t• {script_output_formatted}.")
    print(f"Recommendations: {recommendations}")
    print("")


def print_no_services_found(host_address):
    print(f"No vulnerable services found for host: {host_address}.")
