import re


def csvv_from_classification(risk_classification):
    """
    Determines the CSVV score of the vulnerability based on its risk level classification.

    :param risk_classification: Risk level classification of the vulnerability.
    :return string: Estimated CSVV score of the vulnerability.
    """
    risk_classification_string = str(risk_classification).lower()

    if 'critical' in risk_classification_string:
        return "9.0 - 10.0 (estimated from risk level)"
    if 'high' in risk_classification_string:
        return "7.0 - 8.9 (estimated from risk level)"
    if 'medium' in risk_classification_string:
        return "4.0 - 6.9 (estimated from risk level)"
    if 'low' in risk_classification_string:
        return "0.1 - 3.9 (estimated from risk level)"
    else:
        return "0.0 (estimated from risk level)"


def classification_from_name(vulnerability_name):
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
        risk_classification = "Critical (estimated from name)"
    elif matches_any_pattern(high_patterns):
        risk_classification = "High (estimated from name)"
    elif matches_any_pattern(medium_patterns):
        risk_classification = "Medium (estimated from name)"
    elif matches_any_pattern(low_patterns):
        risk_classification = "Low (estimated from name)"
    elif matches_any_pattern(none_patterns):
        risk_classification = "None (estimated from name)"
    else:
        risk_classification = "Unknown (estimated from name)"

    return risk_classification


def classification_from_csvv(csvv):
    """
    Determines the risk level classification of the vulnerability based on its CSVV score.

    :param csvv: CSVV score of the vulnerability.
    :return string: Risk level classification (critical, high, medium, low, or none) of the vulnerability.
    """
    csvv_classification_float = float(csvv)

    # If CSVV is between x and y ...
    if 9.0 <= csvv_classification_float <= 10.0:
        return "Critical (estimated from CSVV)"
    elif 7.0 <= csvv_classification_float <= 8.9:
        return "High (estimated from CSVV)"
    elif 4.0 <= csvv_classification_float <= 6.9:
        return "Medium (estimated from CSVV)"
    elif 0.1 <= csvv_classification_float <= 3.9:
        return "Low (estimated from CSVV)"
    else:
        return "None (estimated from CSVV)"
