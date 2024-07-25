<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/scapy_report">
        <html>
            <head>
                <title>Scapy Packet Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; font-size: 14px; }
                    h1 { color: #333; font-size: 20px; }
                    h2 { margin-left: 5px; margin-top: 0; font-size: 16px; }
                    .packet {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-left: 2px solid #000;
                    border-right: 2px solid #000;
                    background-color: #f9f9f9;
                    }
                    .details {
                    margin-left: 10px;
                    border-left: 2px solid #000;
                    padding-left: 8px;
                    margin-bottom: 8px;
                    background-color: #fff;
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
                <h1>Scapy Packet Report</h1>
                <xsl:apply-templates select="packet" />
            </body>
        </html>
    </xsl:template>

    <!-- Template to match each packet -->
    <xsl:template match="packet">
        <div class="packet">
            <h2>Packet ID: <xsl:value-of select="@id" /></h2>
            <div class="details">
                <p><strong>Timestamp: </strong> <xsl:value-of select="timestamp" /></p>
                <p><strong>Source: </strong> <xsl:value-of select="source" /></p>
                <p><strong>Destination: </strong> <xsl:value-of select="destination" /></p>
                <p><strong>Protocol: </strong> <xsl:value-of select="protocol" /></p>
                <p><strong>Length: </strong> <xsl:value-of select="length" /> bytes</p>
                <p><strong>Data: </strong> <xsl:value-of select="data" /></p>
                <p><strong>Flags: </strong> <xsl:value-of select="flags" /></p>
                <p><strong>Payload: </strong> <xsl:value-of select="payload" /></p>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>
