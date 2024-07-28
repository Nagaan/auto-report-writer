import xml.etree.ElementTree as EleTree


def load_xml(file_path):
    """
    Loads an XML file and returns the tree and root elements.

    :param file_path: (str) Path to the XML file.
    :return: (tuple) A tuple (tree, root) if successful, otherwise (None, None).
    """
    try:
        tree = EleTree.parse(file_path)
        root = tree.getroot()
        return tree, root

    except EleTree.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None, None

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None, None
