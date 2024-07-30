import json
from bs4 import BeautifulSoup
from collections import Counter
import os


def extract_risk_levels_from_html(html_file):
    """
    Extracts and counts the occurrences of risk levels from the combined HTML file.

    :param html_file: (str) Path to the HTML file.
    :return: (dict) A dictionary with risk levels as keys and their counts as values.
    """
    if not os.path.isfile(html_file):
        print(f"Error: The file {html_file} does not exist.")
        return {level: 0 for level in ['Critical', 'High', 'Medium', 'Low', 'Informational']}

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"Error reading HTML file {html_file}: {e}")
        return {level: 0 for level in ['Critical', 'High', 'Medium', 'Low', 'Informational']}

    risk_levels = ['Critical', 'High', 'Medium', 'Low', 'Informational']
    risk_count = Counter()

    # Iterate over all text in the HTML to find risk levels.
    for text in soup.stripped_strings:
        for level in risk_levels:
            if level in text:
                risk_count[level] += 1

    # Ensure all risk levels are included in the count, even if zero
    for level in risk_levels:
        if level not in risk_count:
            risk_count[level] = 0

    return {level: risk_count[level] for level in risk_levels}  # Maintain order


def append_graph_to_html(html_file, risk_data):
    """
    Appends a pie chart to the top of the HTML file based on the risk data.

    :param html_file: (str) Path to the HTML file.
    :param risk_data: (dict) A dictionary with risk levels and their counts.
    """
    json_data = json.dumps(risk_data)

    template_path = './auto_report_writer/resources/graph_template.html'
    if not os.path.isfile(template_path):
        print(f"Error: The template file {template_path} does not exist.")
        return

    try:
        # Read the template file
        with open(template_path, 'r', encoding='utf-8') as template_file:
            graph_html = template_file.read().replace('{json_data}', json_data)

    except Exception as e:
        print(f"Error reading template file {template_path}: {e}")
        return

    if not os.path.isfile(html_file):
        print(f"Error: The file {html_file} does not exist.")
        return

    try:
        with open(html_file, 'r+', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            body = soup.find('body')

            if body:
                # Insert the graph HTML at the beginning of the body
                body.insert(0, BeautifulSoup(graph_html, 'html.parser'))

            # Write the modified HTML back to the file
            f.seek(0)
            f.write(str(soup.prettify()))
            f.truncate()

    except Exception as e:
        print(f"Error updating HTML file {html_file}: {e}")


def generate_graph_from_html(html_file):
    """
    Extracts risk data from the HTML file and appends a pie chart to it.

    :param html_file: (str) Path to the HTML file.
    """
    risk_data = extract_risk_levels_from_html(html_file)
    if risk_data:  # Only append graph if risk_data was successfully extracted
        append_graph_to_html(html_file, risk_data)
