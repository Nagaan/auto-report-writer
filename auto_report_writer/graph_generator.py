import os
import json
from collections import defaultdict
from bs4 import BeautifulSoup

from auto_report_writer.utils.custom_logger import logger


def extract_risk_levels_from_html(html_file: str) -> dict:
    """
    Extracts and counts the occurrences of risk levels from the combined HTML file.
    Instances of 'defaultdict' sets any key without a value to 0. Important when errors are returned.

    :param html_file: (str) Path to the HTML file.
    :return: (dict) A dictionary with risk levels as keys and their counts as values.
    """

    # Defining a constant for risk levels.
    risk_levels = ['Critical', 'High', 'Medium', 'Low', 'Informational']

    try:
        # Checking if the HTML file exists.
        if not os.path.isfile(html_file):
            logger.error(f"Error: The file '{html_file}' does not exist.")
            return defaultdict(int)

        # Opens the HTML file in read-only mode and parses it.
        with open(html_file, 'r', encoding='utf-8') as f:
            # Creates a BeautifulSoup object to parse and navigate the HTML.
            soup = BeautifulSoup(f, 'html.parser')

    except Exception as e:
        print(f"Error reading HTML file '{html_file}': {e}")
        return defaultdict(int)

    # Initialises a default dictionary for counting risk levels.
    risk_count = defaultdict(int)

    # Iterates through all the text in the 'soup' object.
    for text in soup.stripped_strings:
        # For each 'level' (item) in the risk_levels list, iterate through the text.
        for level in risk_levels:
            # If the 'level' (item) matches a word in the text, increment the count.
            if level in text:
                risk_count[level] += 1

    # Ensures all risk levels are included in the count, even if zero, and returns the result.
    return {level: risk_count[level] for level in risk_levels}


def append_graph_to_html(html_file: str, risk_data: dict) -> None:
    """
    Appends a pie chart to the top of the HTML file based on the risk data.

    :param html_file: (str) Path to the HTML file.
    :param risk_data: (dict) A dictionary with risk levels and their counts.
    """
    json_data = json.dumps(risk_data)
    template_path = './auto_report_writer/resources/graph_template.html'

    try:
        # Checks if the template file exists.
        if not os.path.isfile(template_path):
            print(f"Error: The template file {template_path} does not exist.")
            return

        # Reads the template file and replaces the placeholder text in it with actual data.
        with open(template_path, 'r', encoding='utf-8') as template_file:
            graph_html = template_file.read().replace('{json_data}', json_data)

    except Exception as e:
        print(f"Error reading template file {template_path}: {e}")
        return

    try:
        # Checks if the HTML file exists.
        if not os.path.isfile(html_file):
            print(f"Error: The file {html_file} does not exist.")
            return

        # Opens the HTML file in read and write mode.
        with open(html_file, 'r+', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')  # Creates a BeautifulSoup object to parse and navigate the HTML.
            body = soup.find('body')  # Searches for the <body> tag in the parsed text.

            if body:  # If the <body> tag is found:
                # Creates a BeautifulSoup object to isolate the graph HTML.
                graph_soup = BeautifulSoup(graph_html, 'html.parser')
                # Inserts the graph HTML at the beginning of the body.
                body.insert(0, graph_soup)

            # Writes the modified HTML back to the file.
            f.seek(0)  # Resets the file pointer back to the beginning of the file.
            f.write(str(soup.prettify()))  # Writes the BeautifulSoup object back into the file.
            f.truncate()  # Cuts off any remaining content in the file, ensuring old content is removed.

    except Exception as e:
        print(f"Error updating HTML file {html_file}: {e}")


def generate_graph_from_html(html_file: str) -> None:
    """
    Extracts risk data from the HTML file and appends a pie chart to it.

    :param html_file: (str) Path to the HTML file.
    """
    try:
        risk_data = extract_risk_levels_from_html(html_file)

        if risk_data:  # If risk_data was extracted...
            append_graph_to_html(html_file, risk_data)
        else:
            print("No risk data found to append the graph.")

    except Exception as e:
        print(f"Error in {__file__}: An error occurred while generating the graph: {e}")
