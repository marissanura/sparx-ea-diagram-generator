
from use_case_csv_reader import CSVReader
from sparx_ea_xml_writer import SparxEAXMLWriter

class UseCaseGenerator:
    input_filename = "CSV-ok.csv"
    try:
        datacsv = CSVReader(input_filename)
        folder_hierarcy = ["\ASS-[0-9]{1,}\Z","\AUC-[0-9]{1,}\Z","\A\Z","\AUC-[0-9]{1,}-[0-9]{1,}\Z"]

        # xml_filename = input("Input XML filename:")
        SparxEAXMLWriter(datacsv.generate_tree(folder_hierarcy)).write("output.xml")
    except AttributeError:
        print("Please select the right file!")