
from activity_diagram_csv_reader import ADCSVReader
from activity_diagram_csv_writer import ADXMLWriter

class UseCaseGenerator:
    # input_filename = input("Inputkan nama file: ")
    datacsv = ADCSVReader("ad.csv")
    csv_tree = datacsv.generate_tree()

    xml_writer = ADXMLWriter(csv_tree)
    xml_writer.csv_tree_to_xml()

    xml_writer.write("ad_xml_output.xml")

    # folder_hierarcy = ["\AAD-[0-9]{1,}\Z"]

    # try:
    #     use_case = ADXMLWriter(datacsv.generate_tree(folder_hierarcy))
    #     print("Prose generate file " + input_filename + "\n")
    #     print("generate berhasil!\nmenuliskan file xml...\n")
    #     use_case.write(filename="output.xml")
    #     print("hasil generate sudah tersimpan pada output.xml")
    # except AttributeError as AE:
    #     print("Terdapat kesalahan pada pembacaan dan penerjemahan CSV ke XML")