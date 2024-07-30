import os
import sys
from auto_report_writer.report_generator import report_generator


def set_python_path():
    """
    Adds the auto_report_writer directory to the Python path.
    """
    # Append the absolute path of the auto_report_writer directory to the Python path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'auto_report_writer')))


def main():
    """
    Main entry point for the Auto Report Writer.
    This function executes the report generator.
    """
    set_python_path()  # Set the Python path for imports
    report_generator()  # Call the report generator


if __name__ == "__main__":
    main()  # Execute the main function when the script is run directly
