import os
import sys
from auto_report_writing.report_generation.report_generator import report_generator


def set_python_path():
    """
    Adds the auto_report_writing directory to the Python path.
    """
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'auto_report_writing')))


def main():
    """
    Main entry point for the Auto Report Writer.
    This function executes the report generator.
    """
    set_python_path()
    report_generator()


if __name__ == "__main__":
    main()
