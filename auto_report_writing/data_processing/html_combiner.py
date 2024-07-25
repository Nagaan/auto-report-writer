def html_combiner(html_files, output_file):
    """
    Combine multiple HTML files into one HTML file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write('<html><head><title>Combined Report</title></head><body>\n')

            for html_file in html_files:
                with open(html_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('<hr>\n')  # Add a separator between reports

            outfile.write('</body></html>\n')

    except Exception as e:
        print(f"Error combining HTML: {e}")
