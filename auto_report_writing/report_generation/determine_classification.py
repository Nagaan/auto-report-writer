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

    # Defining regex patterns for each risk classification level, including script IDs
    critical_patterns = [
        r"remote\s+code\s+execution|command\s+injection|deserialization|rce|arbitrary\s+code",
        r"file\s+upload|remote\s+command|vnc\s+authentication\s+bypass|heartbleed",
        r"apache\s+struts\s+remote\s+code\s+execution|cve\s+\d{4}-\d{4,5}",
        r"http\s+sql\s+injection|heartbleed|cve\s+\d{4}-\d{4,5}",
        r"acarsd\s+info|afp\s+path\s+vuln|cassandra\s+brute|clamav\s+exec|distcc\s+cve2004-2687",
        r"jdwp\s+exec|jdwp\s+inject|jdwp\s+info|jdwp\s+version",
        r"oracle\s+brute|oracle\s+brute\s+stealth|oracle\s+enum\s+users|oracle\s+sid\s+brute|oracle\s+tns\s+version"
    ]

    high_patterns = [
        r"sql\s+injection|sql\s+error|sql\s+query|xss|file\s+inclusion|path\s+traversal|xxe",
        r"cross\s+site\s+scripting|http\s+split|http\s+pollution|smb\s+vuln|smb\s+remote\s+code\s+execution",
        r"cve\s+\d{4}-\d{4,5}",
        r"ssl\s+poodle|http\s*vuln|mysql\s*vuln|modbus\s*vuln",
        r"afp\s+brute|ajp\s+auth|ajp\s+brute|citrix\s+brute\s+xml|cvs\s+brute",
        r"imap\s+brute|irc\s+brute|irc\s+sasl\s+brute|membase\s+brute|mongodb\s+brute|mysql\s+brute|nexpose\s+brute|nessus\s+brute|omp2\s+brute|openvas\s+otp\s+brute|radware\s+brute|smb\s+brute|xss\s+info"
    ]

    medium_patterns = [
        r"directory\s+traversal|open\s+redirect|insecure\s+deserialization|missing\s+auth",
        r"session\s+fixation|insecure\s+config|unsecured\s+storage|security\s+misconfig|http\s+security\s+header",
        r"modbus\s+uninitialized\s+register|cve\s+\d{4}-\d{4,5}",
        r"broadcast\s+dhcp\s+discover|broadcast\s+dns\s+service\s+discovery|broadcast\s+networker\s+discover|couchdb\s+databases|couchdb\s+stats",
        r"iap2\s+version|icap\s+info|iec\s+identify|ike\s+version|imap\s+capabilities|impress\s+remote\s+discover|informix\s+query|informix\s+tables|ipmi\s+cipher\s+zero|ipmi\s+version|ipv6\s+multicast\s+mld\s+list|ipv6\s+node\s+info|ipv6\s+ra\s*flood|knx\s+gateway\s+discover|knx\s+gateway\s+info|krb5\s+enum\s+users|ldap\s+novell\s+getpass|ldap\s+rootdse|ldap\s+search|llmnr\s+resolve|lltd\s+discovery|lu\s+enum|maxdb\s+info|mcafee\s+epo\s+agent|memcached\s+info|metasploit\s+info|mssql\s+info|nmap\s+info|nmap\s+scan|nmap\s+scan\s+info"
    ]

    low_patterns = [
        r"outdated\s+auth|weak\s+crypto|info\s+disclosure|dos|default\s+creds",
        r"open\s+ports|unpatched\s+software|http\s+security\s+headers|xss\s+info",
        r"clickjacking|headers|exposed\s+data|dep|insecure\s+coding|logging",
        r"bitcoin\s+getaddr|bitcoin\s+info|bittorrent\s+discovery|broadcast\s+eigrp\s+discovery|broadcast\s+pppoe\s+discover",
        r"nfs\s+ls|nfs\s+showmount|nfs\s+statfs|nje\s+node\s+brute|nje\s+pass\s+brute|ntp\s+info|ntp\s+monlist|omron\s+info|openflow\s+info|openlookup\s+info|radware\s+brute|router\s+brute|snmp\s+info|smb\s+info|system\s+info|telnet\s+info|vnc\s+info",
        r"clickjacking|headers|exposed\s+data|dep",
        r"insecure\s+coding|logging|software\s+update|cve\s+\d{4}-\d{4,5}",
        r"address\s+info|afp\s+ls|afp\s+serverinfo|afp\s+showmount|allseeingeye\s+info",
        r"icmp\s+info|iax2\s+version|iap2\s+info|info\s+info|info\s+debug|info\s+service|ntp\s+info"
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
