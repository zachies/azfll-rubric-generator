from models.DataContext import DataContext
from controllers.csv_handler import CSVHandler
import pdfrw
import re
import os
from sheet_importer import SheetIO

class Generator:
    def __init__(self, data_context: DataContext) -> None:
        self.data_context = data_context
        self.start()

    def encode_string(self, value, type):
            if type == 'string':
                if value:
                    return pdfrw.objects.pdfstring.PdfString.encode(value)
                else:
                    return pdfrw.objects.pdfstring.PdfString.encode('')
            
            elif type == 'checkbox':
                if value == 'True' or value == True:
                    return pdfrw.objects.pdfname.BasePdfName('Yes')
                else: 
                    return pdfrw.objects.pdfname.BasePdfName('No')
            
            return ''

    # returns tuple of form (data, type)
    def translate_key(self, input: str, dict_data: dict):
        if('JudgingRoom' in input):
            return dict_data['Judging Panel'], 'string'
        if('TeamNumber' in input):
            return dict_data['Team Number'], 'string'
        if('TeamName' in input):
            return dict_data['Team Name'], 'string'

        '''
        CORE VALUES
        '''

        # if('Breakthrough' in input):
        #     return ('Breakthrough Award' in dict_data['Core Values Awards'].split(', ')), 'checkbox'
        # if('RisingAllStar' in input):
        #     return ('Rising All-Star' in dict_data['Core Values Awards'].split(', ')), 'checkbox'
        # if('Motivate' in input):
        #     return ('Motivate' in dict_data['Core Values Awards'].split(', ')), 'checkbox'

        if('CVDiscovery' in input):
            match = 'CVDiscovery'
            number = input.replace(match, '')[0]
            if(dict_data['DISCOVERY - Team explored new skills and ideas.'] == number):
                return True, 'checkbox'
        if('CVDiscoveryExceeds' in input):
            return dict_data['If you scored the team with a 4 in the \'DISCOVERY\' category, add a brief description on how they exceeded.'], 'string'

        if('CVInnovation' in input):
            match = 'CVInnovation'
            number = input.replace(match, '')[0]
            if(dict_data['INNOVATION - Team used creativity and persistence to solve problems.'] == number):
                return True, 'checkbox'
        if('CVInnovationExceeds' in input):
            return dict_data['If you scored the team with a 4 in the \'INNOVATION\' category, add a brief description on how they exceeded.'], 'string'

        if('CVImpact' in input):
            match = 'CVImpact'
            number = input.replace(match, '')[0]
            if(dict_data['IMPACT - Team applied what they learned to improve their world.'] == number):
                return True, 'checkbox'
        if('CVImpactExceeds' in input):
            return dict_data['If you scored the team with a 4 in the \'IMPACT\' category, add a brief description on how they exceeded.'], 'string'

        if('CVInclusion' in input):
            match = 'CVInclusion'
            number = input.replace(match, '')[0]
            if(dict_data['INCLUSION - Team demonstrated respect and embraced their differences.'] == number):
                return True, 'checkbox'
        if('CVInclusionExceeds' in input):
            return dict_data['If you scored the team with a 4 in the \'INCLUSION\' category, add a brief description on how they exceeded.'], 'string'

        if('CVTeamwork' in input):
            match = 'CVTeamwork'
            number = input.replace(match, '')[0]
            if(dict_data['TEAMWORK - Team clearly showed they had worked as a team throughout their journey.'] == number):
                return True, 'checkbox'
        if('CVTeamworkExceeds' in input):
            return dict_data['If you scored the team with a 4 in the \'TEAMWORK\' category, add a brief description on how they exceeded.'], 'string'

        if('CVFun' in input):
            match = 'CVFun'
            number = input.replace(match, '')[0]
            if(dict_data['FUN - Teams clearly had fun and celebrated what they have achieved.'] == number):
                return True, 'checkbox'
        if('CVFunExceeds' in input):
            return dict_data['If you scored the team with a 4 in the \'FUN\' category, add a brief description on how they exceeded.'], 'string'

        if('CVFeedbackGreat' in input):
            return dict_data['(CV) Feedback Comments: Great Job!'], 'string'

        if('CVFeedbackThink' in input):
            return dict_data['(CV) Feedback Comments: Think About...'], 'string'

        '''
        INNOVATION PROJECT
        '''

        if('IPIdentifyA' in input):
            match = 'IPIdentifyA'
            number = input.replace(match, '')[0]
            if(dict_data['IDENTIFY - Problem Definition'] == number):
                return True, 'checkbox'
        if('IPIdentifyB' in input):
            match = 'IPIdentifyB'
            number = input.replace(match, '')[0]
            if(dict_data['IDENTIFY - Research'] == number):
                return True, 'checkbox'
        if('IPIdentifyExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'IDENTIFY - Problem Definition\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'IDENTIFY - Research\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('IPDesignA' in input):
            match = 'IPDesignA'
            number = input.replace(match, '')[0]
            if(dict_data['DESIGN - Idea Generation'] == number):
                return True, 'checkbox'
        if('IPDesignB' in input):
            match = 'IPDesignB'
            number = input.replace(match, '')[0]
            if(dict_data['DESIGN - Planning Phase'] == number):
                return True, 'checkbox'
        if('IPDesignExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'DESIGN - Idea Generation\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'DESIGN - Planning Phase\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('IPCreateA' in input):
            match = 'IPCreateA'
            number = input.replace(match, '')[0]
            if(dict_data['CREATE - Solution Development'] == number):
                return True, 'checkbox'
        if('IPCreateB' in input):
            match = 'IPCreateB'
            number = input.replace(match, '')[0]
            if(dict_data['CREATE - Solution Model'] == number):
                return True, 'checkbox'
        if('IPCreateExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'CREATE - Solution Development\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'CREATE - Solution Model\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('IPIterateA' in input):
            match = 'IPIterateA'
            number = input.replace(match, '')[0]
            if(dict_data['ITERATE - Solution Sharing'] == number):
                return True, 'checkbox'
        if('IPIterateB' in input):
            match = 'IPIterateB'
            number = input.replace(match, '')[0]
            if(dict_data['ITERATE - Solution Improvement'] == number):
                return True, 'checkbox'
        if('IPIterateExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'ITERATE - Solution Sharing\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'ITERATE - Solution Improvement\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('IPCommunicateA' in input):
            match = 'IPCommunicateA'
            number = input.replace(match, '')[0]
            if(dict_data['COMMUNICATE - Presentation Engagement'] == number):
                return True, 'checkbox'
        if('IPCommunicateB' in input):
            match = 'IPCommunicateB'
            number = input.replace(match, '')[0]
            if(dict_data['COMMUNICATE - Solution Impact'] == number):
                return True, 'checkbox'
        if('IPCommunicateExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'COMMUNICATE - Presentation Engagement\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'COMMUNICATE - Solution Impact\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('IPFeedbackGreat' in input):
            return dict_data['(IP) Feedback Comments: Great Job!'], 'string'

        if('IPFeedbackThink' in input):
            return dict_data['(IP) Feedback Comments: Think About...'], 'string'

        
        '''
        ROBOT DESIGN
        '''

        if('RDIdentifyA' in input):
            match = 'RDIdentifyA'
            number = input.replace(match, '')[0]
            if(dict_data['IDENTIFY - Mission Strategy'] == number):
                return True, 'checkbox'
        if('RDIdentifyB' in input):
            match = 'RDIdentifyB'
            number = input.replace(match, '')[0]
            if(dict_data['IDENTIFY - Learning'] == number):
                return True, 'checkbox'
        if('RDIdentifyExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'IDENTIFY - Mission Strategy\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'IDENTIFY - Learning\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('RDDesignA' in input):
            match = 'RDDesignA'
            number = input.replace(match, '')[0]
            if(dict_data['DESIGN - Evidence of Workplan'] == number):
                return True, 'checkbox'
        if('RDDesignB' in input):
            match = 'RDDesignB'
            number = input.replace(match, '')[0]
            if(dict_data['DESIGN - Explanation of Features'] == number):
                return True, 'checkbox'
        if('RDDesignExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'DESIGN - Evidence of Workplan\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'DESIGN - Explanation of Features\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('RDCreateA' in input):
            match = 'RDCreateA'
            number = input.replace(match, '')[0]
            if(dict_data['CREATE - Added Functionality'] == number):
                return True, 'checkbox'
        if('RDCreateB' in input):
            match = 'RDCreateB'
            number = input.replace(match, '')[0]
            if(dict_data['CREATE - Explanation of Code'] == number):
                return True, 'checkbox'
        if('RDCreateExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'CREATE - Added Functionality\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'CREATE - Explanation of Code\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('RDIterateA' in input):
            match = 'RDIterateA'
            number = input.replace(match, '')[0]
            if(dict_data['ITERATE - Testing'] == number):
                return True, 'checkbox'
        if('RDIterateB' in input):
            match = 'RDIterateB'
            number = input.replace(match, '')[0]
            if(dict_data['ITERATE - Improvement'] == number):
                return True, 'checkbox'
        if('RDIterateExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'ITERATE - Testing\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'ITERATE - Improvement\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('RDCommunicateA' in input):
            match = 'RDCommunicateA'
            number = input.replace(match, '')[0]
            if(dict_data['COMMUNICATE - Design Explanation'] == number):
                return True, 'checkbox'
        if('RDCommunicateB' in input):
            match = 'RDCommunicateB'
            number = input.replace(match, '')[0]
            if(dict_data['COMMUNICATE - Team Member Involvement'] == number):
                return True, 'checkbox'
        if('RDCommunicateExceeds' in input):
            output = dict_data['If you scored the team with a 4 in the \'COMMUNICATE - Design Explanation\' category, add a brief description on how they exceeded.']
            output = output + ' '
            output = output + dict_data['If you scored the team with a 4 in the \'COMMUNICATE - Team Member Involvement\' category, add a brief description on how they exceeded.']
            return output, 'string'

        if('RDFeedbackGreat' in input):
            return dict_data['(RD) Feedback Comments: Great Job!'], 'string'

        if('RDFeedbackThink' in input):
            return dict_data['(RD) Feedback Comments: Think About...'], 'string'

    def add_data(self, pdf_template: str, output_dir: str, team_number: int, dict_data: dict) -> bool:
        print('Adding data to the pdf file.')
        pdf = pdfrw.PdfReader(pdf_template)

        for page in pdf.pages:
            annotations = page['/Annots']

            if annotations is None:
                continue

            for annotation in annotations:
                if annotation['/Subtype'] == '/Widget':
                    if annotation['/T']:
                        key = annotation['/T'][1:-1]
                        result = self.translate_key(key, dict_data)
                        if result:
                            annotation.update(pdfrw.PdfDict())
                            if result[1] == 'checkbox' and result[0] == True:
                                annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('On'), V=pdfrw.PdfName('Yes')))
                            else:
                                annotation.update(pdfrw.PdfDict(AS=self.encode_string(result[0], result[1]), V=self.encode_string(result[0], result[1])))
                        annotation.update(pdfrw.PdfDict())

        pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write(output_dir + '/' + team_number + '.pdf', pdf)
        print('PDF saved for ' + team_number)

    def start(self) -> None:
        # we don't ACTUALLY know which path is which, but it doesn't really matter
        rd_csv = self.data_context.data_sheet_paths[0]
        ip_csv = self.data_context.data_sheet_paths[1]
        cv_csv = self.data_context.data_sheet_paths[2]
        pdf_template = self.data_context.pdf_template_path
        output_dir = self.data_context.output_dir_path
        csv_data = SheetIO().combine_files_as_dict(rd_csv, cv_csv, ip_csv, delimiter='\t')

        for data in csv_data:
            self.add_data(pdf_template, output_dir, data, csv_data[data])
        
        self.result = len(csv_data.keys())

    def get_dict(self) -> None:
        self.csv_handler = CSVHandler(self.data_context.data_sheet_paths)
        self.data = self.csv_handler.combine_files_as_dict()