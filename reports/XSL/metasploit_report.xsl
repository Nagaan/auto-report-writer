<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/metasploit_report">
        <html>
            <head>
                <title>Metasploit Vulnerability Report</title>
                <style>
                    .metasploit-body { font-family: Arial, sans-serif; margin: 20px; font-size: 14px; }
                    .metasploit-h2 { color: #333; font-size: 20px; }
                    .metasploit-h3 { margin-left: 5px; margin-top: 0; font-size: 16px; }
                    .metasploit-host {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-left: 2px solid #000;
                    border-right: 2px solid #000;
                    background-color: #f9f9f9;
                    }
                    .metasploit-exploit {
                    margin: -5px 0 0;
                    border-top: 1px solid #ddd;
                    padding: 8px;
                    background-color: #fff;
                    }
                    .metasploit-details {
                    margin-left: 10px;
                    border-left: 2px solid #000;
                    padding-left: 8px;
                    margin-bottom: 8px;
                    }
                    .metasploit-p {
                    margin: 5px 0;
                    font-size: 14px;
                    }
                    .metasploit-strong {
                    font-weight: bold;
                    }
                </style>
            </head>
            <body class="metasploit-body">
                <h2 class="metasploit-h2">Metasploit Vulnerability Report</h2>
                <xsl:apply-templates select="host" />
            </body>
        </html>
    </xsl:template>

    <!-- Template to match each host -->
    <xsl:template match="host">
        <div class="metasploit-host">
            <h3 class="metasploit-h3">Host: <xsl:value-of select="address/@addr" /></h3>
            <xsl:apply-templates select="exploit" />
        </div>
    </xsl:template>

    <!-- Template to match each exploit -->
    <xsl:template match="exploit">
        <div class="metasploit-exploit">
            <p class="metasploit-p"><strong class="metasploit-strong">Vulnerability Name: </strong> <xsl:value-of select="name" /></p>
            <p class="metasploit-p"><strong class="metasploit-strong">Risk Level: </strong> <xsl:value-of select="risk" /></p>
            <p class="metasploit-p"><strong class="metasploit-strong">CVSS Score: </strong> <xsl:value-of select="cvss_score" /></p>
            <p class="metasploit-p"><strong class="metasploit-strong">Vulnerability Details:</strong></p>
            <div class="metasploit-details">
                <p class="metasploit-p">• <xsl:value-of select="description" /></p>
                <p class="metasploit-p">• <xsl:value-of select="result" /></p>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>
