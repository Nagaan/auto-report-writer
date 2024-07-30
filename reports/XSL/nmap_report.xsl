<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/nmap_report">
        <html>
            <head>
                <title>Nmap Vulnerability Report</title>
                <style>
                    .nmap-body { font-family: Arial, sans-serif; margin: 20px; font-size: 14px; }
                    .nmap-h2 { color: #333; font-size: 20px; }
                    .nmap-h3 { margin-left: 5px; margin-top: 0; font-size: 16px; }
                    .nmap-host {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-left: 2px solid #000;
                    border-right: 2px solid #000;
                    background-color: #f9f9f9;
                    }
                    .nmap-service {
                    margin: -5px 0 0;
                    border-top: 1px solid #ddd;
                    padding: 8px;
                    background-color: #fff;
                    }
                    .nmap-vulnerability {
                    margin-left: 10px;
                    border-left: 2px solid #000;
                    padding-left: 8px;
                    margin-bottom: 8px;
                    }
                    .nmap-details {
                    margin-left: 10px;
                    border-left: 2px solid #000;
                    padding-left: 8px;
                    margin-bottom: 8px;
                    white-space: pre-wrap; /* Preserve whitespace and line breaks */
                    }
                    .nmap-p {
                    margin: 5px 0;
                    font-size: 14px;
                    }
                    .nmap-strong {
                    font-weight: bold;
                    }
                </style>
            </head>
            <body class="nmap-body">
                <h2 class="nmap-h2">Nmap Vulnerability Report</h2>
                <xsl:apply-templates select="host" />
            </body>
        </html>
    </xsl:template>

    <!-- Template to match each host -->
    <xsl:template match="host">
        <div class="nmap-host">
            <h3 class="nmap-h3">Host: <xsl:value-of select="address/@addr" /></h3>
            <xsl:apply-templates select="service" />
        </div>
    </xsl:template>

    <!-- Template to match each service -->
    <xsl:template match="service">
        <div class="nmap-service">
            <p class="nmap-p"><strong class="nmap-strong">Service: </strong> Port <xsl:value-of select="@portid"/> (<xsl:value-of select="@protocol"/>)</p>
            <p class="nmap-p"><strong class="nmap-strong">State: </strong> <xsl:value-of select="state" /></p>
            <p class="nmap-p"><strong class="nmap-strong">Product: </strong> <xsl:value-of select="product" /></p>
            <p class="nmap-p"><strong class="nmap-strong">Service Name: </strong> <xsl:value-of select="name" /></p>
            <xsl:apply-templates select="vulnerability" />
        </div>
    </xsl:template>

    <!-- Template to match each vulnerability -->
    <xsl:template match="vulnerability">
        <div class="nmap-vulnerability">
            <p class="nmap-p"><strong class="nmap-strong">Vulnerability Name: </strong> <xsl:value-of select="@id" /></p>
            <p class="nmap-p"><strong class="nmap-strong">Risk Level: </strong> <xsl:value-of select="risk_level" /></p>
            <p class="nmap-p"><strong class="nmap-strong">CVSS Score: </strong> <xsl:value-of select="cvss_score" /></p>
            <p class="nmap-p"><strong class="nmap-strong">Vulnerability Details:</strong></p>
            <div class="nmap-details">
                <xsl:value-of select="../vulnerabilities" />
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>
