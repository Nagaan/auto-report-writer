# Auto Report Writer

Auto Report Writer is a Python-based project designed to automate the generation of comprehensive reports from various data sources. This tool is especially useful for summarising and presenting data in multiple formats such as PDF, HTML, and DOCX.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- Automatic report generation from XML data.
- Supports multiple output formats: PDF, HTML, DOCX.
- Customisable templates for report generation.
- Integrated logging for debugging and monitoring.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Nagaan/auto-report-writer.git
    cd auto-report-writer
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Prepare your data files in the `data` directory.
2. Run the main script to initialise file selection:
    ```bash
    python auto_report_writer.py
    ```
3. Select your data files (single or multiple).
4. The generated reports will be available in the `reports` directory.

## Project Structure
- `auto_report_writer/`: Contains the core modules for report generation.
    - `graph_generator.py`: Module for generating graphs.
    - `report_generator.py`: Module for generating reports.
    - `summary_generator.py`: Module for generating summaries.
    - `template_generator.py`: Module for generating templates.
    - `xslt_generator.py`: Module for XSLT transformations.
- `data/`: Directory for input data files.
- `docs/`: Documentation and design notes.
- `reports/`: Generated reports and related resources.
- `requirements.txt`: List of dependencies.

## Contributing
Contributions are welcome! Keep in mind the project is in active development.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
