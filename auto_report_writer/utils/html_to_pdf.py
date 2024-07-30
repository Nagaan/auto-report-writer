import shutil
import pdfkit
from auto_report_writer.utils.custom_logger import logger


def is_wkhtmltopdf_installed():
    """
    Check if wkhtmltopdf is installed and available in the system PATH.

    :return: True if wkhtmltopdf is installed, False otherwise.
    """
    return shutil.which("wkhtmltopdf") is not None


def convert_html_to_pdf(input_file, output_file):
    """
    Convert an HTML file to a PDF file using pdfkit.

    :param input_file: Path to the input HTML file.
    :param output_file: Path to the output PDF file.
    """
    try:
        # Check if wkhtmltopdf is available
        if not is_wkhtmltopdf_installed():
            logger.warn("wkhtmltopdf not found. Please install it.")
            return

        # Convert HTML to PDF
        pdfkit.from_file(input_file, output_file)
        logger.info(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        logger.error(f"Error converting {input_file} to PDF: {e}")
