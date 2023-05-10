
from activity_diagram_csv_reader import ADCSVReader
from activity_diagram_csv_writer import ADXMLWriter

class UseCaseGenerator:
    # input_filename = input("Inputkan nama file: ")
    datacsv = ADCSVReader("ad.csv")
    csv_tree = datacsv.generate_tree()

    xml_writer = ADXMLWriter(csv_tree)
    xml_writer.csv_tree_to_xml()

    xml_writer.write("ad_xml_output.xml")