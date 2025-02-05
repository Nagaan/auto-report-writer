import xml.etree.ElementTree as EleTree
from xml.etree.ElementTree import ElementTree, Element
from auto_report_writer.utils.custom_logger import logger


def load_xml(file_path: str) -> tuple[ElementTree, Element] | tuple[None, None]:
    """
    Loads an XML file and returns the tree and root elements.

    :param file_path: (str) Path to the XML file.
    :return: (tuple[ElementTree, Element] | tuple[None, None]) A tuple (tree, root) if successful, otherwise a tuple (None, None).
    """
    try:
        tree = EleTree.parse(file_path)
        root = tree.getroot()
        return tree, root

    except EleTree.ParseError as e:
        logger.error(f"Error parsing XML: {e}")
        return None, None

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None, None
