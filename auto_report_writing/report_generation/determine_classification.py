import re


def cvss_from_risk_level(risk_level):
    """
    Determines the CVSS score of the vulnerability based on its risk level classification.

    :param risk_level: Risk level classification of the vulnerability.
    :return string: Estimated CVSS score of the vulnerability.
    """
    risk_level_string = str(risk_level).lower()

    if 'critical' in risk_level_string:
        return "9.0 - 10.0 (estimated from risk level)"
    if 'high' in risk_level_string:
        return "7.0 - 8.9 (estimated from risk level)"
    if 'medium' in risk_level_string:
        return "4.0 - 6.9 (estimated from risk level)"
    if 'low' in risk_level_string:
        return "0.1 - 3.9 (estimated from risk level)"
    else:
        return "0.0 (estimated from risk level)"


def risk_level_from_name(vulnerability_name):
    """
    Determines the risk level classification of the vulnerability based on its name, specifically for Nmap results.

    :param vulnerability_name: Name of the vulnerability.
    :return risk_classification: Risk level classification (critical, high, medium, low, or none) of the vulnerability.
    """
    # Normalising the input string.
    normalised_name = vulnerability_name.lower().replace('-', ' ').replace('_', ' ')

    # Defining regex patterns for each risk classification level.
    critical_patterns = [
        r"remote\s+code\s+execution|command\s+injection|deserialization|rce|arbitrary\s+code",
        r"file\s+upload|remote\s+command"
    ]

    high_patterns = [
        r"sql\s+injection|sql\s+error|sql\s+query|xss|file\s+inclusion|path\s+traversal|xxe",
        r"cross\s+site\s+scripting|http\s+split|http\s+pollution"
    ]

    medium_patterns = [
        r"directory\s+traversal|open\s+redirect|insecure\s+deserialization|missing\s+auth",
        r"session\s+fixation|insecure\s+config|unsecured\s+storage|security\s+misconfig"
    ]

    low_patterns = [
        r"outdated\s+auth|weak\s+crypto|info\s+disclosure|dos|default\s+creds",
        r"open\s+ports|unpatched\s+software|http\s+security\s+headers"
    ]

    none_patterns = [
        r"clickjacking|headers|exposed\s+data|dep",
        r"insecure\s+coding|logging"
    ]

    # Sub-function checking if any of the regex patterns match the normalised vulnerability name.
    def matches_any_pattern(patterns):
        return any(re.search(pattern, normalised_name) for pattern in patterns)

    # Classifying vulnerability names based on pattern matching.
    if matches_any_pattern(critical_patterns):
        risk_level = "Critical (estimated from name)"
    elif matches_any_pattern(high_patterns):
        risk_level = "High (estimated from name)"
    elif matches_any_pattern(medium_patterns):
        risk_level = "Medium (estimated from name)"
    elif matches_any_pattern(low_patterns):
        risk_level = "Low (estimated from name)"
    elif matches_any_pattern(none_patterns):
        risk_level = "None (estimated from name)"
    else:
        risk_level = "Unknown (estimated from name)"

    return risk_level


def risk_level_from_cvss(cvss):
    """
    Determines the risk level classification of the vulnerability based on its CVSS score.

    :param cvss: CVSS score of the vulnerability.
    :return string: Risk level classification (critical, high, medium, low, or none) of the vulnerability.
    """
    cvss_float = float(cvss)

    # If CVSS is between x and y ...
    if 9.0 <= cvss_float <= 10.0:
        return "Critical (estimated from CVSS)"
    elif 7.0 <= cvss_float <= 8.9:
        return "High (estimated from CVSS)"
    elif 4.0 <= cvss_float <= 6.9:
        return "Medium (estimated from CVSS)"
    elif 0.1 <= cvss_float <= 3.9:
        return "Low (estimated from CVSS)"
    else:
        return "None (estimated from CVSS)"
