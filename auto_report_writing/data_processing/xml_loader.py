import xml.etree.ElementTree as EleTree
from auto_report_writing.utils.message_utils import *


def load_xml(file_path):
    """
    Loads an XML file and returns the tree and root elements.

    :param file_path: Path to the XML file.
    :return: A tuple (tree, root) if successful, otherwise (None, None).
    """
    try:
        tree = EleTree.parse(file_path)
        root = tree.getroot()
        return tree, root
    except EleTree.ParseError as e:
        print_error_parsing_xml(e)
        return None, None
    except FileNotFoundError:
        print_file_not_found(file_path)
        return None, None
