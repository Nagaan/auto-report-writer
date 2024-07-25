<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="*">
        <html>
            <head>
                <!-- Set the title dynamically based on the root element name -->
                <title>
                    <xsl:value-of select="concat(substring-before(name(), '_report'), ' Vulnerability Report')" />
                </title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; font-size: 14px; }
                    h1 { color: #333; font-size: 20px; }
                    .host, .service, .packet, .attempt {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-left: 2px solid #000;
                    border-right: 2px solid #000;
                    background-color: #f9f9f9;
                    }
                    .subreport {
                    margin: 0;
                    border-top: 1px solid #ddd;
                    padding: 8px;
                    background-color: #fff;
                    }
                    .details {
                    margin-left: 10px;
                    border-left: 2px solid #000;
                    padding-left: 8px;
                    margin-bottom: 8px;
                    white-space: pre-wrap; /* Preserve whitespace and line breaks */
                    }
                    p {
                    margin: 5px 0;
                    font-size: 14px;
                    }
                    strong {
                    font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <!-- Set the header dynamically based on the root element name -->
                <h1>
                    <xsl:value-of select="concat(ucwords(substring-before(name(), '_report')), ' Vulnerability Report')" />
                </h1>
                <!-- Apply templates to child elements of the root -->
                <xsl:apply-templates />
            </body>
        </html>
    </xsl:template>

    <!-- Template to match each host, service, packet, or attempt -->
    <xsl:template match="host | service | packet | attempt">
        <div class="{name()}">
            <h2>
                <!-- Use dynamic text based on element type -->
                <xsl:choose>
                    <xsl:when test="name() = 'host'">Host: <xsl:value-of select="address/@addr" /></xsl:when>
                    <xsl:when test="name() = 'service'">Service: Port <xsl:value-of select="@portid"/> (<xsl:value-of select="@protocol"/>)</xsl:when>
                    <xsl:when test="name() = 'packet'">Packet ID: <xsl:value-of select="@id" /></xsl:when>
                    <xsl:when test="name() = 'attempt'">Target: <xsl:value-of select="target" /></xsl:when>
                </xsl:choose>
            </h2>
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <!-- Template to match each subreport -->
    <xsl:template match="exploit | vulnerability | details | payload | flags">
        <div class="subreport">
            <xsl:choose>
                <xsl:when test="name() = 'exploit'">
                    <p><strong>Vulnerability Name: </strong> <xsl:value-of select="name" /></p>
                    <p><strong>Risk Level: </strong> <xsl:value-of select="risk" /></p>
                    <p><strong>CVSS Score: </strong> <xsl:value-of select="cvss_score" /></p>
                    <p><strong>Details:</strong></p>
                    <div class="details">
                        <p><strong>Description: </strong> <xsl:value-of select="description" /></p>
                        <p><strong>Result: </strong> <xsl:value-of select="result" /></p>
                    </div>
                </xsl:when>
                <xsl:when test="name() = 'vulnerability'">
                    <p><strong>Vulnerability Name: </strong> <xsl:value-of select="@id" /></p>
                    <p><strong>Risk Level: </strong> <xsl:value-of select="risk_level" /></p>
                    <p><strong>CVSS Score: </strong> <xsl:value-of select="cvss_score" /></p>
                    <p><strong>Details:</strong></p>
                    <div class="details">
                        <xsl:value-of select="details" />
                    </div>
                </xsl:when>
                <xsl:when test="name() = 'details'">
                    <p><strong>Details:</strong></p>
                    <div class="details">
                        <xsl:value-of select="." />
                    </div>
                </xsl:when>
                <xsl:when test="name() = 'payload' or name() = 'flags'">
                    <p><strong><xsl:value-of select="concat(ucwords(name()), ': ')" /></strong> <xsl:value-of select="." /></p>
                </xsl:when>
            </xsl:choose>
        </div>
    </xsl:template>

    <!-- Utility template for capitalizing the first letter of each word -->
    <xsl:template name="ucwords">
        <xsl:param name="str" />
        <xsl:variable name="words" select="tokenize($str, ' ')" />
        <xsl:variable name="capitalized">
            <xsl:for-each select="$words">
                <xsl:value-of select="concat(upper-case(substring(., 1, 1)), lower-case(substring(., 2)))" />
                <xsl:if test="position() != last()"> </xsl:if>
            </xsl:for-each>
        </xsl:variable>
        <xsl:value-of select="$capitalized" />
    </xsl:template>

</xsl:stylesheet>
