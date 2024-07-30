<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/smod1_report">
        <html>
            <head>
                <title>Smod-1 Report</title>
                <style>
                    .smod1-body { font-family: Arial, sans-serif; margin: 20px; font-size: 14px; }
                    .smod1-h2 { color: #333; font-size: 20px; }
                    .smod1-h3 { margin-left: 5px; margin-top: 0; font-size: 16px; }
                    .smod1-host {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-left: 2px solid #000;
                    border-right: 2px solid #000;
                    background-color: #f9f9f9;
                    }
                    .smod1-attempt {
                    margin: -5px 0 0;
                    border-top: 1px solid #ddd;
                    padding: 8px;
                    background-color: #fff;
                    }
                    .smod1-details {
                    margin-left: 10px;
                    border-left: 2px solid #000;
                    padding-left: 8px;
                    margin-bottom: 8px;
                    }
                    .smod1-p, .smod1-strong {
                    margin: 5px 0;
                    font-size: 14px;
                    }
                    .smod1-strong {
                    font-weight: bold;
                    }
                </style>
            </head>
            <body class="smod1-body">
                <h2 class="smod1-h2">Smod-1 Report</h2>
                <xsl:apply-templates select="attempt" />
            </body>
        </html>
    </xsl:template>

    <!-- Template to match each attempt -->
    <xsl:template match="attempt">
        <div class="smod1-host">
            <h3 class="smod1-h3">Host: <xsl:value-of select="target" /></h3>
            <div class="smod1-attempt">
                <p class="smod1-p"><strong class="smod1-strong">Vulnerability Name: </strong> <xsl:value-of select="vulnerability" /></p>
                <p class="smod1-p"><strong class="smod1-strong">Risk Level: </strong> <xsl:value-of select="risk_level" /></p>
                <p class="smod1-p"><strong class="smod1-strong">CVSS Score: </strong> <xsl:value-of select="cvss_score" /></p>
                <p class="smod1-p"><strong class="smod1-strong">Vulnerability Details:</strong></p>
                <div class="smod1-details">
                    <p class="smod1-p">• <xsl:value-of select="vulnerability_details/details" /></p>
                    <p class="smod1-p">• <xsl:value-of select="vulnerability_details/timestamp" /></p>
                </div>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>
