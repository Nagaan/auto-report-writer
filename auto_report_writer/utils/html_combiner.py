from auto_report_writer.utils.custom_logger import logger


def html_combiner(html_files: list[str], output_file: str) -> None:
    """
    Combines multiple HTML files into one HTML file.

    :param html_files: (list[str]) List of paths to the HTML files to be combined.
    :param output_file: (str) Path to the output HTML file.
    """
    try:
        # Reads the template file in read-only mode.
        with open('auto_report_writer/resources/combined_template.html', 'r', encoding='utf-8') as template_file:
            template = template_file.read()

        combined_content = ''  # Creating a blank string object to store content from each HTML file.

        for html_file in html_files:  # Loops through the html_files list.
            try:
                # Opens the file in read-only mode.
                with open(html_file, 'r', encoding='utf-8') as infile:
                    combined_content += infile.read()  # Reads the content of each file and concatenates it.
                    combined_content += '<hr>\n'  # Adds a separator between reports.

            except Exception as e:
                logger.error(f"Error reading {html_file}: {e}")

        # Replaces the placeholder in the template with the combined content.
        final_html = template.replace('{content}', combined_content)

        # Writes the final HTML to the output file.
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(final_html)

    except Exception as e:
        logger.error(f"Error processing files: {e}")
