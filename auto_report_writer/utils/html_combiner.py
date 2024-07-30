def html_combiner(html_files, output_file):
    """
    Combine multiple HTML files into one HTML file.

    :param html_files: (list) List of paths to the HTML files to be combined.
    :param output_file: (str) Path to the output HTML file.
    """
    try:
        # Read the template file
        with open('auto_report_writer/resources/combined_template.html', 'r', encoding='utf-8') as template_file:
            template = template_file.read()

        combined_content = ''

        for html_file in html_files:  # Loops through the html_files list.
            try:
                # Opens the file in read mode.
                with open(html_file, 'r', encoding='utf-8') as infile:
                    combined_content += infile.read()  # Read content of each file and concatenate it.
                    combined_content += '<hr>\n'  # Adding a separator between reports.

            except Exception as e:
                print(f"Error reading {html_file}: {e}")

        # Replace the placeholder in the template with the combined content
        final_html = template.replace('{content}', combined_content)

        # Write the final HTML to the output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(final_html)

    except Exception as e:
        print(f"Error processing files: {e}")
