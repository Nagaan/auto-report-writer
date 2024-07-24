from lxml import etree
from auto_report_writing.utils.message_utils import *


def xml_to_html(xml_file, xsl_file, output_html):
    """
    Convert XML file to HTML using an XSL stylesheet.
    """
    try:
        # Load XML and XSL files
        xml_doc = etree.parse(xml_file)
        xsl_doc = etree.parse(xsl_file)
        transform = etree.XSLT(xsl_doc)

        # Transform XML to HTML
        html_doc = transform(xml_doc)

        # Save HTML file
        with open(output_html, 'wb') as f:
            f.write(etree.tostring(html_doc, pretty_print=True, encoding='UTF-8'))

    except Exception as e:
        print_error_converting_xml_to_html(e)
