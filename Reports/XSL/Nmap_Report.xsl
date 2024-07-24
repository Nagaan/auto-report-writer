<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/nmap_report">
        <html>
            <head>
                <title>Nmap Vulnerability Report</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    h1 { color: #333; }
                    .host { margin-bottom: 20px; }
                    .service { margin-left: 20px; }
                    .vulnerability { margin-left: 40px; border-left: 2px solid #000; padding-left: 10px; margin-bottom: 10px; }
                    h2, h3, h4, p { margin: 5px 0; }
                </style>
            </head>
            <body>
                <h1>Nmap Vulnerability Report</h1>
                <xsl:apply-templates select="host" />
            </body>
        </html>
    </xsl:template>

    <!-- Template to match each host -->
    <xsl:template match="host">
        <div class="host">
            <h2>Host: <xsl:value-of select="address/@addr" /></h2>
            <xsl:apply-templates select="service" />
        </div>
    </xsl:template>

    <!-- Template to match each service -->
    <xsl:template match="service">
        <div class="service">
            <h3>Service: Port <xsl:value-of select="@portid"/> (<xsl:value-of select="@protocol"/>)</h3>
            <p><strong>State: </strong> <xsl:value-of select="state" /></p>
            <p><strong>Product: </strong> <xsl:value-of select="product" /></p>
            <p><strong>Service Name: </strong> <xsl:value-of select="name" /></p>
            <p><strong>Vulnerabilities:</strong></p>
            <xsl:apply-templates select="vulnerability" />
        </div>
    </xsl:template>

    <!-- Template to match each vulnerability -->
    <xsl:template match="vulnerability">
        <div class="vulnerability">
            <h4>Vulnerability Name: <xsl:value-of select="@id" /></h4>
            <p><strong>Risk Level: </strong> <xsl:value-of select="risk_level" /></p>
            <p><strong>CSVV Score: </strong> <xsl:value-of select="csvv_score" /></p>
            <p><strong>Vulnerability Details:</strong></p>
            <xsl:apply-templates select="preceding-sibling::vulnerabilities[1]" />
            <p><strong>Recommendations:</strong></p>
            <p><xsl:value-of select="recommendations" /></p>
        </div>
    </xsl:template>

    <!-- Template to match each vulnerabilities element -->
    <xsl:template match="vulnerabilities">
        <p>
            <xsl:text>• </xsl:text><xsl:value-of select="substring-before(., ' URI: ')" /><br />
            <xsl:text>• URI: </xsl:text><xsl:value-of select="substring-before(substring-after(., ' URI: '), ' Payload: ')" /><br />
            <xsl:text>• Payload: </xsl:text><xsl:value-of select="substring-before(substring-after(., ' Payload: '), ' Output: ')" /><br />
            <xsl:text>• Output: </xsl:text><xsl:value-of select="substring-after(., ' Output: ')" />

        </p>
    </xsl:template>

</xsl:stylesheet>
