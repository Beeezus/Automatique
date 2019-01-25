from os.path import join, realpath
import utility
import openpyxl
import logging 


logging.basicConfig(format = '%(asctime)s %(message)s',
                            datefmt = '%m/%d/%Y %I:%M:%S %p',
                            filename = 'system.log',
                            level=logging.INFO)


class Excel():
    def __init__(self, site_name, hierarchy_name, environment_prefix, dict_meters, period, gateway_id):
        '''Set path'''
        dict_configuration_path = utility.get_configuration_path()
        self.json_templates_path = dict_configuration_path["json_templates_path"]
        self.excel_templates_path = dict_configuration_path["excel_templates_path"]
        self.json_files_path = dict_configuration_path["json_files_path"]
        self.excel_files_path = dict_configuration_path["excel_files_path"]
        self.hierarchy_file_path = dict_configuration_path["hierarchy_path"]
        self.logs_path = dict_configuration_path["logs_path"]

        '''Set Data'''
        self.site_name = site_name
        self.hierarchy_name = hierarchy_name
        self.environment_prefix = environment_prefix
        self.period = period
        self.gateway_id = gateway_id

        '''Dict'''
        self.dict_logs_file = self.getdict_logs_file()
        self.dict_from_template = self.get_template_data()
        self.dict_from_json_configuration = utility.read_json_file(join(realpath(''), "configuration", "measures_config.json"))
        self.dict_meters = self.create_dict_meter_data(dict_meters)
        self.createExcelSheet()


    def getdict_logs_file(self):
        list_logs_file = utility.create_file_list(self.logs_path, ".json")
        if(list_logs_file != []):
            for logs_file in list_logs_file:
                if(utility.get_substring(logs_file, start="-", stop=".") == self.hierarchy_name):
                    return utility.read_json_file(join(self.logs_path, logs_file))
         
            return self.gateway_id+"_"+"thing§"
        else:
             return self.gateway_id+"_"+"thing§"


    def create_dict_meter_data(self, dict_meters):    
        for meter_name, list_measures in dict_meters.items():
            for dict_measure in list_measures:
                try:
                    trend_id, period = self.dict_from_template[meter_name+"."+dict_measure["measure"]]
                    dict_measure["trend_id"] = trend_id
                    dict_measure["period"] = period
                    if(str(trend_id) in self.dict_from_json_configuration):
                        dict_measure.update(self.dict_from_json_configuration[str(trend_id)])
                except:
                    pass
        return dict_meters


    def get_template_data(self):
        list_json_file = utility.create_file_list(join(self.json_files_path, self.hierarchy_name), ".json")
        dict_measures = {}
        for _file in list_json_file:
            file_json = utility.read_json_file(join(self.json_files_path, self.hierarchy_name, _file))     
            for measure in file_json["parameters"]["filter_tag"]:
                if(measure["tag"] != "CommunicationCode"):
                    dict_measures[measure["tag"]] = [measure["id"], measure["period"]]       
        return(dict_measures)


    '''Create excel file'''    
    def createExcelSheet(self):
        excel_document = openpyxl.load_workbook(join(self.excel_templates_path, "template_leonardo.xlsx"))
        sheet = excel_document.active
        number_cell = 7  
        for meter_name, list_measures in self.dict_meters.items():
            if(type(self.dict_logs_file) == dict):
                thing_id = self.dict_logs_file[meter_name+'.json'][1]
            else:
                thing_id = self.dict_logs_file
            for dict_measure in list_measures:
                try:
                    if(dict_measure["active"] == True):
                        sheet['A'+str(number_cell)] = self.site_name
                        list_name = dict_measure["name"].replace(".", "_").split("-")
                        sheet['B'+str(number_cell)] = '{}-{}-{}\{}'.format(list_name[0], list_name[1], list_name[2], list_name[3])
                        sheet['C'+str(number_cell)] = self.environment_prefix+"_"+thing_id+"_"+str(dict_measure["trend_id"])
                        if(self.period == 0):
                            sheet['E'+str(number_cell)] = dict_measure["period"]//60 
                        else:
                            sheet['E'+str(number_cell)] = self.period//60
                        sheet['G'+str(number_cell)] = "True"
                        sheet['D'+str(number_cell)] = dict_measure["channel"]
                        sheet['F'+str(number_cell)] = dict_measure["multipler"]
                        number_cell+=1 
                except:
                    pass
        excel_document.save(join(self.excel_files_path,self.hierarchy_name+".xlsx"))