from openai import OpenAI
import re


def generate_recommendations_name(vulnerability_name):
    vulnerability_name_string = vulnerability_name.lower()

    if vulnerability_name_string == "sql-injection":
        recommendations = f"[Generalised Recommendations for {vulnerability_name}] \
To effectively address SQL injection vulnerabilities, employ the following strategies: \
Use prepared statements and parameterized queries to separate SQL code from data, \
ensuring malicious input cannot alter queries. Implement stored procedures, which \
encapsulate SQL logic within the database to minimize exposure to injection. Validate \
and sanitize all user inputs to adhere to expected formats, thereby rejecting potentially \
harmful data. Utilize ORM (Object-Relational Mapping) libraries to abstract SQL operations, \
reducing direct interaction with raw SQL. Restrict database user privileges to the minimum \
necessary for application functionality. Properly handle errors by avoiding the exposure of \
detailed SQL error messages to users; instead, log them securely. Regularly conduct security \
testing to identify and address vulnerabilities, and consider using web application firewalls \
(WAFs) to filter out malicious SQL attempts. Finally, keep all systems and libraries up to \
date with the latest security patches and updates to mitigate emerging threats."
        return recommendations

    # Any string starting with 'MS' will receive the below recommendation.
    elif re.match(r'^ms', vulnerability_name_string):
        recommendations = f"Check the appropriate Microsoft Security Bulletin for recommendations: " \
                          f"https://learn.microsoft.com/en-us/security-updates/securitybulletins/securitybulletins"
        return recommendations

    else:
        return "No recommendations."


def generate_recommendations_openai(vulnerability_details):

    client = OpenAI(api_key="[API Key removed due to public nature of repository.]")

    recommendations = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a straight-to-the-point deadpan assistant."},
            {"role": "user", "content": f"Using a 200 word paragraph, detail some recommendations and solutions for: {vulnerability_details}"},
        ],
    )

    return recommendations.choices[0].text.strip()
