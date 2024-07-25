<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/metasploit_report">
        <html>
            <head>
                <title>Metasploit Vulnerability Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; font-size: 14px; }
                    h1 { color: #333; font-size: 20px; }
                    h2 { margin-left: 5px; margin-top: 0; font-size: 16px; }
                    .host {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-left: 2px solid #000;
                    border-right: 2px solid #000;
                    background-color: #f9f9f9;
                    }
                    .exploit {
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
        <div class="exploit">
            <p><strong>Vulnerability Name: </strong> <xsl:value-of select="name" /></p>
            <p><strong>Risk Level: </strong> <xsl:value-of select="risk" /></p>
            <p><strong>CVSS Score: </strong> <xsl:value-of select="cvss_score" /></p>
            <p><strong>Vulnerability Details:</strong></p>
            <div class="details">
                <p>• <xsl:value-of select="description" /></p>
                <p>• <xsl:value-of select="result" /></p>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>
