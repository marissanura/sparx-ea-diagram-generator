
from use_case_csv_reader import UCCSVReader
from sparx_ea_xml_writer import SparxEAXMLWriter

class UseCaseGenerator:
    input_filename = input("Inputkan nama file: ")
    datacsv = UCCSVReader(input_filename)
    folder_hierarcy = ["\ASS-[0-9]{1,}\Z","\AUC-[0-9]{1,}\Z","\A\Z","\AUC-[0-9]{1,}-[0-9]{1,}\Z"]

    try:
        use_case = SparxEAXMLWriter(datacsv.generate_tree(folder_hierarcy))
        print("Prose generate file " + input_filename + "\n")
        print("generate berhasil!\nmenuliskan file xml...\n")
        use_case.write(filename="output.xml")
        print("hasil generate sudah tersimpan pada output.xml")
    except AttributeError as AE:
        print("Terdapat kesalahan pada pembacaan dan penerjemahan CSV ke XML")