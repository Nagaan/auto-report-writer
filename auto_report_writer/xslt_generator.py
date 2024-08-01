# Incomplete file. Not implemented in final product.

import re


def parse_class_file(class_file):
    """
    Parses the Python class file to extract the XML structure.
    """
    with open(class_file, 'r') as file:
        content = file.read()

    # Use regex to find all SubElement declarations
    pattern = re.compile(r'SubElement\(([^,]+), \'([^\']+)\'(, id=([^,]+))?\)')
    matches = pattern.findall(content)

    structure = {}
    current_parent = None

    for match in matches:
        parent, tag, _, _ = match
        parent = parent.strip()  # Ensure parent is stripped of whitespace

        # Update the structure based on the current parent
        if current_parent is None or parent == 'report':
            current_parent = tag
            structure[current_parent] = []
        elif current_parent:
            structure[current_parent].append(tag)

    return structure


def clean_special_char(text):
    """
    Cleans special characters from the text.
    """
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')


def load_xslt_template(template_file):
    """
    Loads the XSLT template from a file.
    """
    with open(template_file, 'r') as file:
        return file.read()


def generate_xslt(class_file, output_file):
    """
    Generates an XSLT file based on the parsed structure.
    """
    report_structure = parse_class_file(class_file)

    # Load the XSLT template from the xsl_template.xsl file
    with open('reports/XSL/xsl_template.xsl', 'r') as template_file:
        xslt_template = template_file.read()

    root = list(report_structure.keys())[0]  # Get the root element
    children = report_structure.get(root, [])  # Get the direct children of the root
    child_templates = ""

    for child in children:
        sub_elements = report_structure.get(child, [])
        sub_elements_templates = ""
        for sub_element in sub_elements:
            sub_elements_templates += f"""<p class="p"><strong class="strong">{sub_element.capitalize()}: </strong> <xsl:value-of select="{sub_element}" /></p>"""

        child_templates += f"""
    <xsl:template match="{child}">
        <div class="details">
            {sub_elements_templates}
        </div>
    </xsl:template>
"""

    xslt_content = xslt_template.format(
        root=root,
        title=f"{root.capitalize()} Vulnerability Report",
        root_child=children[0] if children else '',
        root_child_label=children[0].capitalize() if children else '',
        child=" | ".join(children),
        child_templates=child_templates
    )

    with open(output_file, 'w') as file:
        file.write(xslt_content)

    print(f"XSLT generated and saved to {output_file}")
