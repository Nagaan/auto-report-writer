def html_combiner(html_files, output_file):
    """
    Combine multiple HTML files into one HTML file.

    :param html_files: (list) List of paths to the HTML files to be combined.
    :param output_file: (str) Path to the output HTML file.
    """
    try:
        # Opens the file in write mode.
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Appends the HTML opening tags to the top of the file.
            outfile.write('<html><head><title>Combined Report</title></head><body>\n')

            for html_file in html_files:  # Loops through the html_files list.
                try:
                    # Opens the file in read mode.
                    with open(html_file, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())  # Reads the content of the file and outputs it to the output file.
                        outfile.write('<hr>\n')  # Adding a separator between reports.

                except Exception as e:
                    print(f"Error reading {html_file}: {e}")

            # Appends the HTML closing tags to the bottom of the file.
            outfile.write('</body></html>\n')

    except Exception as e:
        print(f"Error writing to {output_file}: {e}")
