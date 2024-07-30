from lxml import etree
from auto_report_writer.utils.custom_logger import logger


def xml_to_html(xml_file, xsl_file, output_html):
    """
    Converts an XML file to HTML using an XSL stylesheet.

    :param xml_file: (str) Path to the input XML file.
    :param xsl_file: (str) Path to the XSL stylesheet.
    :param output_html: (str) Path where the output HTML file will be saved.
    """
    try:
        # Loading the XML and XSL files.
        xml_doc = etree.parse(xml_file)
        xsl_doc = etree.parse(xsl_file)
        transform = etree.XSLT(xsl_doc)

        # Transforming the XML to HTML.
        html_doc = transform(xml_doc)

        # Saving the HTML file.
        with open(output_html, 'wb') as f:  # 'wb' opens the file for writing in binary mode.
            f.write(etree.tostring(html_doc, pretty_print=True, encoding='UTF-8'))  # type: ignore

    except Exception as e:
        logger.error(f"Error converting XML to HTML: {e}")
