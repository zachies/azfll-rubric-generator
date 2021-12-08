import os
import openpyxl

from models.sheet import SheetSource, Sheet

'''
Wrapper for manipulating CSV files.
'''
class CSVHandler():
    '''
    Creates a new instance of CSVHandler() with the specified file paths.
    '''
    def __init__(self, *sheet_paths: str) -> None:
        self.sheet_sources = list()
        self.add_file_to_sources(sheet_paths)

    '''
    Adds the given file paths to the list of sources that this instance of 
    CSVHandler has.
    '''
    def add_file_to_sources(self, *sheet_paths: str) -> None:
        for sheet_path in sheet_paths:
            base = os.path.basename(sheet_path)
            base = os.path.splitext(base)

            sheet_source = SheetSource(sheet_path, base[0], base[1])
            
            self.sheet_sources.append(sheet_source)

    '''
    Parses each of the files into a single dictionary. 
    Excel files will not use the delimiter parameter.
    '''
    def combine_files_as_dict(self, delimiter: str = ',') -> Sheet:
        sheet_dicts = list()
        
        for sheet in self.sheet_sources:
            sheet_dicts.append(self.get_dict_from_file(sheet))

        output = Sheet(headers=list(), data=dict())
        for entry in sheet_dicts:
            output.headers.extend(entry.headers)
            output.data.update(entry.data)

        return output

    '''
    Gets the sheet file from a file. Implements logic to choose best parser based on
    file extension.
    '''
    def get_dict_from_file(self, sheet_source: SheetSource, delimiter: str = ',') -> Sheet:
        if(sheet_source.extension == '.csv'):
            return self.__parse_csv_to_dict__(self, sheet_source, delimiter)
        elif(sheet_source.extension == '.tsv'):
            return self.__parse_csv_to_dict__(self, sheet_source, '\t')
        elif(sheet_source.extension == '.xlsx'):
            return self.__parse_xlsx_to_dict__(self, sheet_source)
        

    '''
    Parses a CSV file to an instance of a sheet.
    '''
    def __parse_csv_to_dict__(self, sheet_source: SheetSource, delimiter: str = ',') -> Sheet:
        sheet = Sheet()

        with open(sheet_source.filename, 'r') as file:
            line_count = 0
            sheet.headers = list()
            sheet.data = dict()

            for line in file:
                line_data = line.split(delimiter)

                if line_count == 0:
                    for i in line_data:
                        sheet.headers.append(i)

                    line_count += 1
                    continue
            
            team_entry = dict()
            for i in range(len(line_data)):
                team_entry[sheet.headers[i]] = line_data[i]

            sheet.data[line_data[3]] = team_entry
            line_count += 1
        
        return sheet


    '''
    Parses an Excel file to an instance of a sheet.
    '''
    def __parse_xlsx_to_dict__(self, sheet_source: SheetSource) -> list:
        workbook = openpyxl.load_workbook(sheet_source.path)