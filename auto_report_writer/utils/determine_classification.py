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
    :return risk_classification: Risk level classification (critical, high, medium, low, or informational) of the vulnerability.
    """
    # Normalising the input string.
    normalised_name = vulnerability_name.lower().replace('-', ' ').replace('_', ' ')

    # Defining regex patterns for each risk classification level
    critical_patterns = [
        r"remote\s+code\s+execution|command\s+injection|deserialization|arbitrary\s+code|file\s+upload",
        r"vnc\s+authentication\s+bypass|heartbleed|apache\s+struts\s+remote\s+code\s+execution",
        r"cve\s+\d{4}-\d{4,5}|http\s+sql\s+injection",
        r"broken\s+authentication|broken\s+access\s+control|remote\s+command",
        # Added DoS related patterns
        r"denial\s+of\s+service|dos|d-o-s|distributed\s+denial\s+of\s+service|ddos",
        # Added unauthorized access patterns
        r"unauthorized\s+access|unauthorised\s+access|unauthenticated\s+access"
    ]

    high_patterns = [
        r"sql\s+injection|xss|file\s+inclusion|path\s+traversal|xxe",
        r"cross\s+site\s+scripting|http\s+pollution|smb\s+remote\s+code\s+execution",
        r"cve\s+\d{4}-\d{4,5}|ssl\s+poodle|http\s*vuln|mysql\s*vuln|modbus\s*vuln",
        r"csrf|insecure\s+direct\s+object\s+references|security\s+misconfiguration|insufficient\s+logging",
        r"missing\s+auth|unvalidated\s+redirects|server-side\s+request\s+forgery"
    ]

    medium_patterns = [
        r"directory\s+traversal|open\s+redirect|insecure\s+deserialization|session\s+fixation",
        r"insecure\s+config|unsecured\s+storage|security\s+misconfiguration|http\s+security\s+header",
        r"business\s+logic\s+vulnerability|weak\s+encryption|clickjacking",
        # Modbus related patterns
        r"modbus\s+uninitialized\s+register|cve\s+\d{4}-\d{4,5}"
    ]

    low_patterns = [
        r"outdated\s+auth|weak\s+crypto|info\s+disclosure|default\s+creds|open\s+ports",
        r"unpatched\s+software|xss\s+info|exposed\s+data|insecure\s+coding|logging",
        r"low\s+impact\s+vulnerabilities|software\s+update|information\s+disclosure|denial\s+of\s+service",
        # Other low vulnerability patterns
        r"nfs\s+ls|nfs\s+showmount|nfs\s+statfs|router\s+brute|snmp\s+info|smb\s+info"
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
    else:
        risk_level = "Informational (estimated from name)"

    return risk_level
