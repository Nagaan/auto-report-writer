<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/smod1_report">
        <html>
            <head>
                <title>Smod-1 Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; font-size: 14px; }
                    h1 { color: #333; font-size: 20px; }
                    .host {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-left: 2px solid #000;
                    border-right: 2px solid #000;
                    background-color: #f9f9f9;
                    }
                    .attempt {
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
                    h2, p {
                    margin: 5px 0;
                    font-size: 14px;
                    }
                    strong {
                    font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <h1>Smod-1 Report</h1>
                <xsl:apply-templates select="attempt" />
            </body>
        </html>
    </xsl:template>

    <!-- Template to match each attempt -->
    <xsl:template match="attempt">
        <div class="host">
            <p><strong>Host: </strong> <xsl:value-of select="target" /></p>
            <div class="attempt">
                <p><strong>Vulnerability Name: </strong> <xsl:value-of select="vulnerability" /></p>
                <p><strong>Risk Level: </strong> <xsl:value-of select="risk_level" /></p>
                <p><strong>CVSS Score: </strong> <xsl:value-of select="cvss_score" /></p>
                <div class="details">
                    <p><strong>Vulnerability Details:</strong></p>
                    <p><xsl:value-of select="vulnerability_details/details" /></p>
                    <p><xsl:value-of select="vulnerability_details/timestamp" /></p>
                </div>
                <p><strong>Recommendations: </strong> <xsl:value-of select="recommendations" /></p>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>
