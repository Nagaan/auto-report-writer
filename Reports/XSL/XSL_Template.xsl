<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="*">
        <html>
            <head>
                <!-- Set the title dynamically based on the root element name -->
                <title>
                    <xsl:value-of select="concat(name(), ' Vulnerability Report')" />
                </title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; font-size: 14px; }
                    h1 { color: #333; font-size: 20px; }
                    .repeating_root {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-left: 2px solid #000;
                    border-right: 2px solid #000;
                    background-color: #f9f9f9;
                    }
                    .repeating_subroot {
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
                <!-- Set the header dynamically based on the root element name -->
                <h1>
                    <xsl:value-of select="concat(name(), ' Vulnerability Report')" />
                </h1>
                <!-- Apply templates to child elements of the root -->
                <xsl:apply-templates />
            </body>
        </html>
    </xsl:template>

    <!-- Template to match each repeating_root -->
    <xsl:template match="repeating_root">
        <div class="repeating_root">
            <h2>Host: <xsl:value-of select="." /></h2>
            <xsl:apply-templates select="repeating_subroot" />
        </div>
    </xsl:template>

    <!-- Template to match each repeating_subroot -->
    <xsl:template match="repeating_subroot">
        <div class="repeating_subroot">
            <p><strong>Vulnerability Name: </strong> <xsl:value-of select="name" /></p>
            <p><strong>Risk Level: </strong> <xsl:value-of select="risk" /></p>
            <p><strong>CVSS Score: </strong> <xsl:value-of select="cvss_score" /></p>
            <div class="details">
                <p><strong>Vulnerability Details:</strong></p>
                <p><xsl:value-of select="details" /></p>
            </div>
            <p><strong>Recommendations: </strong> <xsl:value-of select="recommendations" /></p>
        </div>
    </xsl:template>

</xsl:stylesheet>
