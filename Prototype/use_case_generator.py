
from use_case_csv_reader import CSVReader
from sparx_ea_xml_writer import SparxEAXMLWriter

class UseCaseGenerator:
    datacsv = CSVReader("CSV-ok.csv")
    SparxEAXMLWriter(datacsv.generate_tree()).write('output.xml')
    