import os
from bs4 import BeautifulSoup
from collections import Counter
import re


def calculate_weighted_risk_level(risk_counts):
    total_risks = sum(risk_counts.values())
    if total_risks == 0:
        return 'Informational'  # Default when there are no risks

    risk_levels = ['Critical', 'High', 'Medium', 'Low', 'Informational']
    risk_weights = {'Critical': 2, 'High': 1.5, 'Medium': 1, 'Low': 0.5, 'Informational': 0}

    weighted_sum = sum(risk_counts[level] * risk_weights[level] for level in risk_levels)
    max_weighted_sum = sum(risk_weights[level] * risk_counts[level] for level in risk_levels if risk_counts[level] > 0)

    if max_weighted_sum == 0:
        return 'Informational'

    normalised_weight = weighted_sum / max_weighted_sum

    if normalised_weight >= 0.75:  # Skewing towards 'Critical'
        return 'Critical'
    elif normalised_weight >= 0.5:  # Skewing towards 'High'
        return 'High'
    elif normalised_weight >= 0.25:  # Skewing towards 'Medium'
        return 'Medium'
    else:  # Skewing towards 'Low' or 'Informational'
        return 'Low'


def extract_highest_cvss_score(cvss_score_string):
    match = re.search(r'(\d+\.\d+)\s*-\s*(\d+\.\d+)|(\d+\.\d+)', cvss_score_string)
    if match:
        if match.group(2):  # Range matched
            return float(match.group(2))
        else:  # Single score matched
            return float(match.group(3))
    return 0.0  # Return 0 if no valid score is found


def calculate_average_cvss_score(cvss_scores):
    if not cvss_scores:
        return 0.0

    highest_scores = [extract_highest_cvss_score(score) for score in cvss_scores]
    return sum(highest_scores) / len(highest_scores) if highest_scores else 0.0


def determine_highest_vulnerability(risk_counts):
    risk_levels = ['Critical', 'High', 'Medium', 'Low', 'Informational']
    for level in risk_levels:
        if risk_counts[level] > 0:
            return level
    return 'Informational'


def determine_testing_frequency(weighted_risk_level):
    frequency_map = {
        'Critical': 'weekly',
        'High': 'fortnightly',
        'Medium': 'monthly',
        'Low': 'quarterly',
        'Informational': 'quarterly'
    }
    return frequency_map.get(weighted_risk_level, 'quarterly')


def extract_data_from_html(html_file):
    if not os.path.isfile(html_file):
        print(f"Error: The file {html_file} does not exist.")
        return [], Counter(), []

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"Error reading HTML file {html_file}: {e}")
        return [], Counter(), []

    risk_levels = ['Critical', 'High', 'Medium', 'Low', 'Informational']
    risk_count = Counter()
    cvss_scores = []
    vulnerabilities = []

    # Iterate over all elements in the document
    for element in soup.find_all(True):  # True means it finds all tags
        text = element.get_text()  # Get the text content of the element

        # Check for Risk Level
        if 'Risk Level:' in text:
            risk_level = text.split('Risk Level:')[-1].strip()
            if risk_level in risk_levels:
                risk_count[risk_level] += 1

        # Check for CVSS Score
        elif 'CVSS Score:' in text:
            score_range = text.split('CVSS Score:')[-1].strip()
            cvss_scores.append(score_range)  # Append the raw score string

        # Check for Vulnerability Name
        elif 'Vulnerability Name:' in text:
            vulnerability_name = text.split('Vulnerability Name:')[-1].strip()
            # Assign the last recorded risk level to the vulnerability
            if risk_level in risk_levels:
                vulnerabilities.append((vulnerability_name, risk_level))  # Store vulnerability with its risk level

    return cvss_scores, risk_count, vulnerabilities


def generate_project_summary(weighted_risk_level, average_cvss_score, highest_vulnerability, highest_level_vulnerabilities_list, testing_frequency):
    template_path = 'auto_report_writing/data_processing/resources/summary_template.html'
    if not os.path.isfile(template_path):
        print(f"Error: The template file {template_path} does not exist.")
        return ""

    try:
        with open(template_path, 'r', encoding='utf-8') as template_file:
            summary_html = template_file.read()

        # Create a vulnerability items list based on the highest level found
        vulnerability_items = ''.join(f'<li>{vuln[0]}</li>' for vuln in highest_level_vulnerabilities_list)

        if not vulnerability_items:  # If no vulnerabilities found
            vulnerability_items = '<li>No vulnerabilities found.</li>'

        summary_html = (
            summary_html.replace('{weighted_risk_level}', weighted_risk_level)
            .replace('{average_cvss_score}', f"{average_cvss_score:.2f}")
            .replace('{highest_vulnerability}', highest_vulnerability)
            .replace('{vulnerability_list}', vulnerability_items)
            .replace('{testing_frequency}', testing_frequency)
        )

        return summary_html

    except Exception as e:
        print(f"Error reading template file {template_path}: {e}")
        return ""


def append_summary_to_html(html_file, project_summary):
    if not os.path.isfile(html_file):
        print(f"Error: The file {html_file} does not exist.")
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
        print(f"Error updating HTML file {html_file}: {e}")


def generate_summary_from_html(html_file):
    cvss_scores, risk_counts, vulnerabilities = extract_data_from_html(html_file)

    weighted_risk_level = calculate_weighted_risk_level(risk_counts)
    average_cvss_score = calculate_average_cvss_score(cvss_scores)
    highest_vulnerability = determine_highest_vulnerability(risk_counts)
    testing_frequency = determine_testing_frequency(weighted_risk_level)

    # Create the list of vulnerabilities based on the highest risk level
    highest_level_vulnerabilities_list = [
        vuln for vuln in vulnerabilities if vuln[1] == highest_vulnerability
    ]

    project_summary = generate_project_summary(
        weighted_risk_level, average_cvss_score, highest_vulnerability, highest_level_vulnerabilities_list, testing_frequency
    )

    if project_summary:
        append_summary_to_html(html_file, project_summary)