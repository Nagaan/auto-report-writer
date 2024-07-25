<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/nmap_report">
        <html>
            <head>
                <title>Nmap Vulnerability Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; font-size: 14px; }
                    h1 { color: #333; font-size: 16px; }
                    h2 { margin-left: 5px; margin-top: 0; font-size: 16px; }
                    .host {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-left: 2px solid #000;
                    border-right: 2px solid #000;
                    background-color: #f9f9f9;
                    }
                    .service {
                    margin: 0;
                    border-top: 1px solid #ddd;
                    padding: 8px;
                    background-color: #fff;
                    }
                    .vulnerability {
                    margin-left: 10px;
                    border-left: 2px solid #000;
                    padding-left: 8px;
                    margin-bottom: 8px;
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
            <p><strong>Service: </strong> Port <xsl:value-of select="@portid"/> (<xsl:value-of select="@protocol"/>)</p>
            <p><strong>State: </strong> <xsl:value-of select="state" /></p>
            <p><strong>Product: </strong> <xsl:value-of select="product" /></p>
            <p><strong>Service Name: </strong> <xsl:value-of select="name" /></p>
            <xsl:apply-templates select="vulnerability" />
        </div>
    </xsl:template>

    <!-- Template to match each vulnerability -->
    <xsl:template match="vulnerability">
        <div class="service">
            <p><strong>Vulnerability Name: </strong> <xsl:value-of select="@id" /></p>
            <p><strong>Risk Level: </strong> <xsl:value-of select="risk_level" /></p>
            <p><strong>CVSS Score: </strong> <xsl:value-of select="cvss_score" /></p>
            <p><strong>Vulnerability Details:</strong></p>
            <div class="details">
                <xsl:apply-templates select="service" />
                <xsl:apply-templates select="parent::service/vulnerabilities" />
            </div>
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
