<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/metasploit_report">
        <html>
            <head>
                <title>Metasploit Vulnerability Report</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    h1 { color: #333; }
                    .host { margin-bottom: 20px; }
                    .vulnerability { margin-left: 20px; border-left: 2px solid #000; padding-left: 10px; margin-bottom: 10px; }
                    h2, h3, p { margin: 5px 0; }
                </style>
            </head>
            <body>
                <h1>Metasploit Vulnerability Report</h1>
                <xsl:apply-templates select="host" />
            </body>
        </html>
    </xsl:template>

    <!-- Template to match each host -->
    <xsl:template match="host">
        <div class="host">
            <h2>Host: <xsl:value-of select="address/@addr" /></h2>
            <xsl:apply-templates select="exploit" />
        </div>
    </xsl:template>

    <!-- Template to match each exploit -->
    <xsl:template match="exploit">
        <div class="vulnerability">
            <p><strong>Vulnerability Name: </strong> <xsl:value-of select="name" /></p>
            <p><strong>Risk Level: </strong> <xsl:value-of select="risk" /></p>
            <p><strong>CSVV Score: </strong> <xsl:value-of select="csvv_score" /></p>
            <p><strong>Vulnerability Details: </strong></p>
            <p>• <xsl:value-of select="description" /></p>
            <p>• <xsl:value-of select="result" /></p>
            <p><strong>Recommendations: </strong> <xsl:value-of select="recommendations" /></p>
        </div>
    </xsl:template>

</xsl:stylesheet>
