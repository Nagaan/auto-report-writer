import os
import re
from bs4 import BeautifulSoup
from collections import Counter
from auto_report_writer.utils.custom_logger import logger


def calculate_average_risk_level(risk_counts):
    """
    Calculates the average risk level based on the counts of different risk levels.

    :param risk_counts: A Counter object that holds the counts of each risk level.
    :return: The average risk level as a string, one of 'Critical', 'High', 'Medium', 'Low', or 'Informational'.
    """
    risk_values = {
        'Critical': 4,
        'High': 3,
        'Medium': 2,
        'Low': 1,
        'Informational': 0
    }

    total_risk_score = 0
    total_count = 0

    for risk_level, count in risk_counts.items():
        # Slightly skew towards higher risk levels
        if risk_level in ['Critical']:
            total_risk_score += risk_values[risk_level] * count * 1.25  # 25% more weight for 'Critical'
        elif risk_level in ['High']:
            total_risk_score += risk_values[risk_level] * count * 1.1  # 10% more weight for 'High'
        else:
            total_risk_score += risk_values[risk_level] * count

        total_count += count

    # Return the risk level based on average score
    if total_count == 0:
        return 'Informational'  # Default when there are no risks

    average_score = total_risk_score / total_count

    # Determine the corresponding risk level based on average score
    if average_score >= 3.5:  # Between 3.5 and 4.0
        return 'Critical'
    elif average_score >= 2.5:  # Between 2.5 and 3.4
        return 'High'
    elif average_score >= 1.5:  # Between 1.5 and 2.4
        return 'Medium'
    elif average_score >= 0.5:  # Between 0.5 and 1.4
        return 'Low'
    else:
        return 'Informational'


def extract_highest_cvss_score(cvss_score_string):
    """
    Extracts the highest CVSS score from a string that may contain a range or a single score.

    :param cvss_score_string: A string containing the CVSS score(s).
    :return: The highest CVSS score found, or 0.0 if no valid score is found.
    """
    match = re.search(r'(\d+\.\d+)\s*-\s*(\d+\.\d+)|(\d+\.\d+)', cvss_score_string)
    if match:
        if match.group(2):  # Range matched
            return float(match.group(2))
        else:  # Single score matched
            return float(match.group(3))
    return 0.0  # Return 0 if no valid score is found


def calculate_average_cvss_score(cvss_scores):
    """
    Calculates the average CVSS score from a list of CVSS score strings.

    :param cvss_scores: A list of strings containing CVSS scores.
    :return: The average CVSS score, or 0.0 if the list is empty.
    """
    if not cvss_scores:
        return 0.0

    highest_scores = [extract_highest_cvss_score(score) for score in cvss_scores]
    return sum(highest_scores) / (len(highest_scores) / 2) if highest_scores else 0.0


def determine_highest_vulnerability(risk_counts):
    """
    Determines the highest vulnerability level from the risk counts.

    :param risk_counts: A Counter object that holds the counts of each risk level.
    :return: The highest vulnerability level, one of 'Critical', 'High', 'Medium', 'Low', or 'Informational'.
    """
    risk_levels = ['Critical', 'High', 'Medium', 'Low', 'Informational']
    for level in risk_levels:
        if risk_counts[level] > 0:
            return level
    return 'Informational'


def determine_testing_frequency(average_risk_level):
    """
    Determines the recommended testing frequency based on the average risk level.

    :param average_risk_level: The average risk level.
    :return: The recommended testing frequency as a string.
    """
    frequency_map = {
        'Critical': 'weekly',
        'High': 'fortnightly',
        'Medium': 'monthly',
        'Low': 'quarterly',
        'Informational': 'quarterly'
    }
    return frequency_map.get(average_risk_level, 'quarterly')


def extract_data_from_html(html_file):
    """
    Extracts CVSS scores, risk counts, and vulnerabilities from an HTML file.

    :param html_file: The path to the HTML file.
    :return: A tuple containing:
             - A list of CVSS scores,
             - A Counter object of risk counts,
             - A list of tuples containing vulnerabilities and their risk levels.
    """
    if not os.path.isfile(html_file):
        logger.error(f"Error: The file {html_file} does not exist.")
        return [], Counter(), []

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        logger.error(f"Error reading HTML file {html_file}: {e}")
        return [], Counter(), []

    risk_levels = ['Critical', 'High', 'Medium', 'Low', 'Informational']
    risk_count = Counter()
    cvss_scores = []
    vulnerabilities = []

    # Initialize risk_level variable
    risk_level = None

    # Iterate over all elements in the document
    for element in soup.find_all(True):  # True means it finds all tags
        text = element.get_text()  # Get the text content of the element

        # Check for Risk Level
        if 'Risk Level:' in text:
            # Safely extract the risk level
            try:
                risk_level = text.split('Risk Level:')[-1].strip().split()[0]  # Get the first word after "Risk Level:"
                if risk_level in risk_levels:
                    risk_count[risk_level] += 1
            except IndexError:
                error = 1

        # Check for CVSS Score
        elif 'CVSS Score:' in text:
            # Safely extract the CVSS score
            try:
                score_range = text.split('CVSS Score:')[-1].strip()
                cvss_scores.append(score_range)  # Append the raw score string
            except IndexError:
                logger.warn("CVSS Score format unexpected.")

        # Check for Vulnerability Name
        elif 'Vulnerability Name:' in text:
            # Safely extract the vulnerability name
            try:
                vulnerability_name = text.split('Vulnerability Name:')[-1].strip()
                # Append only if the vulnerability name is valid and not empty
                if vulnerability_name and risk_level in risk_levels:
                    vulnerabilities.append((vulnerability_name, risk_level))  # Store vulnerability with its risk level
            except IndexError:
                logger.warn("Vulnerability Name format unexpected.")

    return cvss_scores, risk_count, vulnerabilities


def generate_project_summary(average_risk_level, average_cvss_score, highest_vulnerability, highest_level_vulnerabilities_list, testing_frequency):
    """
    Generates a project summary HTML based on the provided metrics.

    :param average_risk_level: The average risk level.
    :param average_cvss_score: The average CVSS score.
    :param highest_vulnerability: The highest vulnerability level.
    :param highest_level_vulnerabilities_list: List of vulnerabilities at the highest risk level.
    :param testing_frequency: Recommended frequency for testing.
    :return: The HTML string of the generated project summary.
    """
    template_path = './auto_report_writer/resources/summary_template.html'
    if not os.path.isfile(template_path):
        logger.error(f"The template file {template_path} does not exist.")
        return ""

    try:
        with open(template_path, 'r', encoding='utf-8') as template_file:
            summary_html = template_file.read()

        # Create a vulnerability items list based on the highest level found
        vulnerability_items = ''.join(f'<li>{vuln[0]}</li>' for vuln in highest_level_vulnerabilities_list)

        if not vulnerability_items:  # If no vulnerabilities found
            vulnerability_items = '<li>No vulnerabilities found.</li>'

        summary_html = (
            summary_html.replace('{weighted_risk_level}', average_risk_level)
            .replace('{average_cvss_score}', f"{average_cvss_score:.2f}")
            .replace('{highest_vulnerability}', highest_vulnerability)
            .replace('{vulnerability_list}', vulnerability_items)
            .replace('{testing_frequency}', testing_frequency)
        )

        return summary_html

    except Exception as e:
        logger.error(f"Error reading template file {template_path}: {e}")
        return ""


def append_summary_to_html(html_file, project_summary):
    """
    Appends the project summary HTML to the end of an existing HTML file.

    :param html_file: The path to the HTML file to update.
    :param project_summary: The HTML string to append.
    """
    if not os.path.isfile(html_file):
        logger.error(f"Error: The file {html_file} does not exist.")
        return

    try:
        with open(html_file, 'r+', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            body = soup.find('body')

            if body:
                body.insert(0, BeautifulSoup(project_summary, 'html.parser'))

            f.seek(0)
            f.write(str(soup.prettify()))
            f.truncate()

    except Exception as e:
        logger.error(f"Error updating HTML file {html_file}: {e}")


def generate_summary_from_html(html_file, report_type_list):
    """
    Generates a summary from the data extracted from an HTML file and appends it to the file.

    :param html_file: The path to the HTML file from which to extract data.
    :param report_type_list: A list of report types to include in the summary.
    """
    cvss_scores, risk_counts, vulnerabilities = extract_data_from_html(html_file)

    average_risk_level = calculate_average_risk_level(risk_counts)
    average_cvss_score = calculate_average_cvss_score(cvss_scores)
    highest_vulnerability = determine_highest_vulnerability(risk_counts)
    testing_frequency = determine_testing_frequency(average_risk_level)

    # Create the list of vulnerabilities based on the highest risk level
    highest_level_vulnerabilities_list = [
        vuln for vuln in vulnerabilities if vuln[1] == highest_vulnerability
    ]

    # Prepare the report type list as a string for the HTML
    report_type_list_str = '<li>' + '</li><li>'.join(report_type_list) + '</li>'

    project_summary = generate_project_summary(
        average_risk_level, average_cvss_score, highest_vulnerability, highest_level_vulnerabilities_list, testing_frequency
    )

    if project_summary:
        # Insert the report type list into the summary
        project_summary = project_summary.replace('{report_type_list}', report_type_list_str)
        append_summary_to_html(html_file, project_summary)
