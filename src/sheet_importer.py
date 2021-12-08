import json

class SheetIO:
    def __init__(self) -> None:
        pass

    # combine the three CSV files into a single dictionary; keys are the team number
    def combine_files_as_dict(self, robot_design_csv: str, core_values_csv: str, innovation_project_csv: str, delimiter=',') -> dict:
        # get dictionaries from csv files
        rd_dict = self.get_dict_from_csv(robot_design_csv, delimiter)
        cv_dict = self.get_dict_from_csv(core_values_csv, delimiter)
        ip_dict = self.get_dict_from_csv(innovation_project_csv, delimiter)

        output = dict()

        # merge dictionaries together into single dictionary entry
        # timestamp, entry, judging panel, and notes will all take the value present
        # in the innovation project dictionary
        for key in rd_dict:
            output[key] = rd_dict[key].copy()
            output[key].update(cv_dict[key])
            output[key].update(ip_dict[key])

        return output

    # get a dictionary representation from a single csv
    def get_dict_from_csv(self, file_csv: str, delimiter: str) -> dict:
        output = dict()

        with open(file_csv, 'r') as file:
            line_count = 0
            headers = list()

            for line in file:
                # split the line into a string list
                line_list = line.split(delimiter)

                # populate headers list (first line of spreadsheet)
                if line_count == 0:
                    for i in line_list:
                        headers.append(i.replace('\n', ''))

                    line_count += 1
                    continue
                
                # construct a new dictionary entry with the team's info
                team_entry = dict()
                for i in range(len(line_list)):
                    team_entry[headers[i]] = line_list[i]
                    
                # hard code the dictionary entry as the team number
                output[line_list[3]] = team_entry
                line_count += 1
        
        return output

    def get_headers_from_csv(self, delimiter:str, *files: str) -> list:
        headers = list()

        for f in files:
            with open(f, 'r') as file:
                line_list = file.readline().split(delimiter)
                for i in line_list:
                        headers.append(i.replace('\n', ''))

        return headers

    # writes a list to a file, each entry is on a new line
    def write_list_to_file(self, input: list, output: str) -> None:
        with open(output, 'w+') as file:
            for item in input:
                file.write(item + "\n")


    # writes a dictionary object to a file, serialized as JSON
    def write_dict_to_file(self, input: dict, output: str) -> None:
        with open(output, 'w+') as file:
            file.write(json.dumps(input))