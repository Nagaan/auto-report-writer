import shutil
import pypandoc
import tkinter as tk
from tkinter import messagebox
from auto_report_writer.utils.custom_logger import logger


def is_pandoc_installed() -> bool:
    """
    Checks if Pandoc is installed and available in the system PATH.

    :return: True if Pandoc is installed, False otherwise.
    """
    return shutil.which("pandoc") is not None


def ask_user_to_install_pandoc() -> bool:
    """
    Prompts the user with a message box asking if they want to install Pandoc.

    :return: True if the user wants to install, False otherwise.
    """
    root = tk.Tk()
    root.withdraw()  # Hides the root window.
    response = messagebox.askyesno(
        "Install Pandoc",
        "Pandoc is required to convert the file to DOCX.\n"
        "Pandoc is not installed.\n"
        "Do you want to install Pandoc?",
    )
    root.destroy()  # Closes the tkinter root window.
    return response


def download_pandoc() -> None:
    """
    Downloads Pandoc using pypandoc's built-in downloader.
    """
    try:
        pypandoc.download_pandoc()
        logger.info("Pandoc has been successfully installed.")
        messagebox.showinfo("Pandoc Installed", "Pandoc has been successfully installed.")

    except Exception as e:
        logger.error(f"Error downloading Pandoc: {e}")
        messagebox.showerror("Download Failed", "Failed to download Pandoc. Please install it manually.")


def convert_html_to_docx(input_file: str, output_file: str) -> None:
    """
    Converts an HTML file to a DOCX file using Pandoc.

    :param input_file: (str) Path to the input HTML file.
    :param output_file: (str) Path to the output DOCX file.
    """
    try:
        # Checking if Pandoc is not available.
        if not is_pandoc_installed():
            logger.info("Pandoc not found.")

            # Prompts the user to install Pandoc.
            if ask_user_to_install_pandoc():
                logger.info("Downloading Pandoc...")
                download_pandoc()

            else:  # If the user has chosen not to install Pandoc...
                logger.warning("User chose not to install Pandoc. Exiting conversion.")
                return

        # Converts the HTML file to DOCX format.
        pypandoc.convert_file(input_file, 'docx', outputfile=output_file)
        logger.info(f"Successfully converted {input_file} to {output_file}")

    except Exception as e:
        logger.error(f"Unexpected error converting {input_file} to DOCX: {e}")
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
