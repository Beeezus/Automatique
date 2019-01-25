from xml.dom import minidom
from os.path import  basename, join, realpath
from os import mkdir, listdir
import utility
import logging
import uuid

class Jasonx():
    logging.basicConfig(format = '%(asctime)s %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p',
                    filename = 'system.log',
                    level=logging.INFO)

    def __init__(self, username, password, gateway_id, env_dict, hierarchy, boolean_save_json_file):
        dict_configuration_path = utility.get_configuration_path()
        self.json_templates_path = dict_configuration_path["json_templates_path"]
        self.excel_templates_path = dict_configuration_path["excel_templates_path"]
        self.json_files_path = dict_configuration_path["json_files_path"]
        self.excel_files_path = dict_configuration_path["excel_files_path"]
        self.hierarchy_file_path = dict_configuration_path["hierarchy_path"]

        '''SET DATA'''
        self.dict_configuration_path = utility.get_configuration_path
        self.username = username
        self.password = password
        self.hierarchy_name = utility.get_substring(basename(hierarchy), stop=".")
        self.hierarchy_path = join(self.hierarchy_file_path, self.hierarchy_name+".xml")
        self.serial_number, self.match_group_value, self.dict_meters = self.get_data_from_hierarchy()
        self.gateway_id = gateway_id
        self.environment_prefix = env_dict[gateway_id]["environment_prefix"]
        self.match_group_value = self.hierarchy_name.split("_")[1]+"_"+self.match_group_value
        self.dict_meter_template, self.dict_meters_not_found = self.create_dict_meter_template()

    '''Search serial_number, match_group_value and create dict_meter -> {"meter_name" : [{"name_measure" : "val", "tag_measure : "val"} , {...}, ...]'''
    def get_data_from_hierarchy(self):
        try:
            logging.info("getting data from the Hierarchy")
            file_hierarchy = minidom.parse(self.hierarchy_path) 
            dict_meters = {}    
            local_id = file_hierarchy.getElementsByTagName("LocalId")   
            name = file_hierarchy.getElementsByTagName("Name")  
            description = file_hierarchy.getElementsByTagName("Description")[0].firstChild.nodeValue
            serial_number = description[description.find("SerialNumber=")+13:description.find("\n")]
            match_group_value = name[0].firstChild.nodeValue
            if(len(match_group_value) > 15):
                match_group_value = match_group_value[0:15]
            for i in range(0, len(local_id)): 
                if(local_id[i].parentNode.nodeName == "Meter"):
                    meter_name, measure = local_id[i].firstChild.nodeValue.split(".")   
                    measure_eff = name[i].firstChild.nodeValue  
                    if(meter_name not in dict_meters):
                        dict_meters[meter_name] = [{"measure" : measure, "name" : measure_eff}] 
                    else:
                        dict_meters[meter_name].append({"measure" : measure, "name" : measure_eff})
            return serial_number, match_group_value, dict_meters
        except Exception as e:
            logging.error(e, exc_info=True)

    '''Create dict -> {meter_name : template_name / not found, ...}'''
    def create_dict_meter_template(self):
        try:
            logging.info("creating Dictionary Meter")
            dict_meters_template = {}
            dict_meters_not_found = {}
            for meter_name, list_measures in self.dict_meters.items():
                list_meter_measures = []
                for measure in list_measures:
                    list_meter_measures.append(measure["measure"])
                response = self.search_template(list_meter_measures) 
                if(response != False):
                    dict_meters_template[meter_name] = response
                else:
                    dict_meters_template[meter_name] = "Not Found"
                    dict_meters_not_found[meter_name] = list_measures
            return dict_meters_template, dict_meters_not_found
        except Exception as e:
            logging.error(e, exc_info=True)

    '''Match number measures-> template - meter'''
    def search_template(self, list_meter_measures):
        try:
            dict_meters_config = utility.read_json_file(join(realpath(''), "configuration", "template_measures_config.json"))
            for model_meter, diz_value in dict_meters_config.items():
                for key, value in diz_value.items():
                   if(key == "measures_selected" and value==len(list_meter_measures)):
                        response = self.control_template(model_meter+".json", list_meter_measures)               
                        if(response != False):
                            logging.info('found corespondence with Template' +response)
                            return response
            return False
        except Exception as e:
            logging.error(e, exc_info=True)
            
    '''Match tag measures -> template - meter'''
    def control_template(self, template, list_meter_measures):
        try:
            logging.info("controlling Template")
            count = 0
            list_measures_template = self.create_template_list(template)
            for measure in list_meter_measures:
                if(measure not in list_measures_template):
                    break
                else:
                    if(count+1 == len(list_meter_measures)):
                        return template
                    else:
                        count+=1
            return False        
        except Exception as e:
            logging.error(e, exc_info=True)

    '''Create list tag measures template'''
    def create_template_list(self, template):
        try:
            logging.info("creating Template list")
            file_template = utility.read_json_file(join(self.json_templates_path, template))
            list_measures = []
            for model in file_template["parameters"]["filter_tag"]:
                if(model["tag"] != "CommunicationCode"):
                    list_measures.append(utility.get_substring(model["tag"], start="."))           
            return(list_measures)
        except Exception as e:
            logging.error(e, exc_info=True)

    '''Create file json'''
    def create_json(self):
        try:
            if(self.hierarchy_name not in listdir(join(self.json_files_path))):
                mkdir(join(self.json_files_path, self.hierarchy_name))
            for meter_name, template in self.dict_meter_template.items():
                if(template != "Not Found"):
                    file_template = utility.read_json_file(join(self.json_templates_path, template))
                    file_template["gateway_id"] = self.gateway_id
                    file_template["parameters"]["environment_prefix"] = self.environment_prefix
                    file_template["parameters"]["serial_number"] = self.serial_number
                    file_template["parameters"]["model"] = template[:template.find(".")]
                    file_template["parameters"]["user_name"] = self.username
                    file_template["parameters"]["password"] = self.password
                    key = file_template["parameters"]["file_name_filter"]
                    key["match_group_value"] = self.match_group_value
                    file_template["parameters"]["meter_name"] = meter_name
                    file_template["parameters"]["maker"] = meter_name
                    for measure_meter in file_template["parameters"]["filter_tag"]:
                        if(measure_meter["tag"]!="CommunicationCode"):
                            measure_meter["tag"] = measure_meter["tag"].replace(measure_meter["tag"][:measure_meter["tag"].find(".")], meter_name)                
                    utility.save_json_file(join(self.json_files_path, self.hierarchy_name, meter_name+".json"), file_template)
        except Exception as e:
            logging.error(e, exc_info=True)


    def create_template(self):
        master_list_trend_id = utility.read_json_file(join(realpath(''), "configuration", "measures_config.json"))
        list_measures_for_template = self.create_list_measures()
        list_trend_id_not_found = []
        self.dict_meters_not_found = {}
        for list_measures in list_measures_for_template:
            control = True
            new_template = utility.read_json_file(join(realpath(''), "configuration", "empty_template.json"))
            for measure in list_measures:
                if(measure in master_list_trend_id):
                    new_template['parameters']['filter_tag'].append({"id":master_list_trend_id[measure]['TrendID'], "period":900, "tag":"resource."+measure})
                else:
                    list_trend_id_not_found.append(measure)
                    control = False
                    break
            if(control == True):   
                uuid_string = str(uuid.uuid1()) 
                utility.save_json_file(join(self.json_templates_path, "custom_template_"+uuid_string+".json"), new_template)
        utility.refresh_template_configuration()
        return list_trend_id_not_found
    
    def create_list_measures(self):
        list_measures_for_template = [] 
        for dict_values in self.dict_meters_not_found.values():  
            _list = []
            for key_value in dict_values:
                _list.append(key_value['measure'])
            _list.sort()
            if(_list not in list_measures_for_template):
                list_measures_for_template.append(_list)
        return list_measures_for_template