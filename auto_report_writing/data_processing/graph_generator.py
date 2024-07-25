import json
from bs4 import BeautifulSoup
from collections import Counter


def extract_risk_levels_from_html(html_file):
    """
    Extracts and counts the occurrences of risk levels from the combined HTML file.
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

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
    """
    json_data = json.dumps(risk_data)

    graph_html = f"""
    <div style="width: 50%; margin: auto;">
        <canvas id="riskLevelPieChart" width="400" height="400"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {{
            var ctx = document.getElementById('riskLevelPieChart').getContext('2d');
            var riskLevelData = {json_data};
            new Chart(ctx, {{
                type: 'pie',
                data: {{
                    labels: Object.keys(riskLevelData),
                    datasets: [{{
                        label: 'Proportion of Vulnerabilities',
                        data: Object.values(riskLevelData),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',  // Critical
                            'rgba(255, 155, 86, 0.2)',  // High
                            'rgba(255, 230, 86, 0.2)',  // Medium
                            'rgba(75, 192, 192, 0.2)',   // Low
                            'rgba(54, 162, 235, 0.2)'   // Informational
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',  // Critical
                            'rgba(255, 155, 86, 1)',  // High
                            'rgba(255, 230, 86, 1)',  // Medium
                            'rgba(75, 192, 192, 1)',   // Low
                            'rgba(54, 162, 235, 1)'   // Informational
                        ],
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'top',
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(tooltipItem) {{
                                    var label = tooltipItem.label;
                                    var value = tooltipItem.raw;
                                    return label + ': ' + value;
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }});
    </script>
    """

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


def generate_graph_from_html(html_file):
    """
    Extract risk data from the HTML file and append a pie chart to it.
    """
    risk_data = extract_risk_levels_from_html(html_file)
    append_graph_to_html(html_file, risk_data)
