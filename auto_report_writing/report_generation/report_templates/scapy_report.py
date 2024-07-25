from xml.etree.ElementTree import Element, SubElement, ElementTree
from auto_report_writing.data_processing.xml_loader import load_xml
from auto_report_writing.utils.message_utils import *


def generate_scapy_report(root):
    """
    Generates an XML structure with details of packets from the Scapy data.
    """
    report = Element('scapy_report')

    for packet in root.findall('.//packet'):
        packet_id = packet.get('id')
        timestamp = packet.find('timestamp').text
        source = packet.find('source').text
        destination = packet.find('destination').text
        protocol = packet.find('protocol').text
        length = packet.find('length').text
        data = packet.find('data').text
        flags = packet.find('flags').text
        payload = packet.find('payload').text

        packet_element = SubElement(report, 'packet', id=packet_id)
        SubElement(packet_element, 'timestamp').text = timestamp
        SubElement(packet_element, 'source').text = source
        SubElement(packet_element, 'destination').text = destination
        SubElement(packet_element, 'protocol').text = protocol
        SubElement(packet_element, 'length').text = length
        SubElement(packet_element, 'data').text = data
        SubElement(packet_element, 'flags').text = flags
        SubElement(packet_element, 'payload').text = payload

    return ElementTree(report)


def count_packets(root):
    """
    Counts the number of packets in the given Scapy XML root.
    """
    return len(root.findall('.//packet'))


def print_packet_details(root):
    """
    Prints details for each packet in the given Scapy XML root.
    """
    packet_count = count_packets(root)
    print(f"Total packets: {packet_count}")

    for packet in root.findall('.//packet'):
        packet_id = packet.get('id')
        timestamp = packet.find('timestamp').text
        source = packet.find('source').text
        destination = packet.find('destination').text
        protocol = packet.find('protocol').text
        length = packet.find('length').text
        data = packet.find('data').text
        flags = packet.find('flags').text
        payload = packet.find('payload').text

        print(f"Packet ID: {packet_id}")
        print(f"Timestamp: {timestamp}")
        print(f"Source: {source}")
        print(f"Destination: {destination}")
        print(f"Protocol: {protocol}")
        print(f"Length: {length}")
        print(f"Data: {data}")
        print(f"Flags: {flags}")
        print(f"Payload: {payload}")
        print("")


def scapy_report(file_path, output_file):
    """
    Processes the input Scapy XML file and generates a Scapy report XML.
    """
    try:
        tree, root = load_xml(file_path)

        if root is not None:
            report_tree = generate_scapy_report(root)
            report_tree.write(output_file, encoding='utf-8', xml_declaration=True)
            print(f"Report successfully generated and saved to {output_file}")

            # Print details for verification
            print_packet_details(root)

        else:
            print_failed_to_load_file()

    except Exception as e:
        print_error_processing_report(e)
