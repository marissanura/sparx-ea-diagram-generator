
from use_case_csv_reader import CSVReader
from sparx_ea_xml_writer import SparxEAXMLWriter

class UseCaseGenerator:
    # input_filename = input("Input filename:")
    datacsv = CSVReader('CSV-ok.csv')
    folder_hierarcy = ["SS-[0-9]{1,}\Z","UC-[0-9]{1,}\Z","\A\Z","UC-[0-9]{1,}-[0-9]{1,}\Z"]

    # print("CSV Tree Generation Done Successfully!")
    # xml_filename = input("Input XML filename:")
    SparxEAXMLWriter(datacsv.generate_tree(folder_hierarcy)).write("output.xml")
    