import shutil
import pypandoc


def is_pandoc_installed():
    """
    Check if Pandoc is installed and available in the system PATH.

    :return: True if Pandoc is installed, False otherwise.
    """
    return shutil.which("pandoc") is not None


def download_pandoc():
    """
    Download Pandoc using pypandoc's built-in downloader.
    """
    pypandoc.download_pandoc()


def convert_html_to_docx(input_file, output_file):
    """
    Convert an HTML file to a DOCX file using Pandoc.

    :param input_file: Path to the input HTML file.
    :param output_file: Path to the output DOCX file.
    """
    try:
        # Check if pandoc is available, if not download it
        if not is_pandoc_installed():
            print("Pandoc not found. Downloading...")
            download_pandoc()

        pypandoc.convert_file(input_file, 'docx', outputfile=output_file)
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error converting {input_file} to DOCX: {e}")
