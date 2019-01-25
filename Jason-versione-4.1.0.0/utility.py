import json
from os.path import realpath, join, isfile, isdir
from os import listdir, makedirs
from validate_email import validate_email
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
import datetime


def get_configuration_path():
    return read_json_file(join(realpath(''), "configuration", "path_config.json"))


'''Function for read json files'''
def read_json_file(path):
    with open(path, 'r') as file: 
        return json.load(file)
        
        
'''Configuration path'''
dict_configuration_path = get_configuration_path()
json_templates_path = dict_configuration_path["json_templates_path"]
excel_templates_path = dict_configuration_path["excel_templates_path"]
json_files_path = dict_configuration_path["json_files_path"]
excel_files_path = dict_configuration_path["excel_files_path"]
hierarchy_path = dict_configuration_path["hierarchy_path"]
logs_path = dict_configuration_path["logs_path"]
post_files_path = dict_configuration_path["post_files_path"]


'''Function for save json files'''
def save_json_file(path_file, element):
    try:
        with open(path_file, 'w') as file:
            json.dump(element, file, indent=4)
        return True
    except:
        return False
   

'''Function for read xml files'''
def read_xml_file(path_file):
    from xml.dom import minidom
    return minidom.parse(path_file)


'''Function for create list of files'''
def create_file_list(path_file, ext):
    lis = []
    for node in listdir(path_file):
        if(node.startswith("~$") or node.startswith(".")):
            continue
        if(node.endswith(ext)):
            fullpath = join(path_file, node)
            if(isfile(fullpath)): 
                lis.append(node)
    return lis
    

'''Function for create list of directories'''
def create_directory_list(path_file):
    lis = []
    for node in listdir(path_file):
        if(node.startswith(".")):
            continue
        fullpath = join(path_file, node)
        if(isdir(fullpath)): 
            lis.append(node)
    return lis
    

'''Function return substring'''
def get_substring(string, start='', stop=''):  
    if(start != '' and stop != ''):
        return string[string.find(start)+len(start) : string.find(stop)]
        
    elif(start != '' and stop == ''):
        return string[string.find(start)+len(start) : ]
    
    elif(start == '' and stop != ''):
        return string[ : string.find(stop)]   
    else:
        return string
        

'''Refresh template configuration'''    
def refresh_template_configuration():
    list_templates = create_file_list(json_templates_path, ".json")
    add_measures_template(list_templates)
    

'''Count measures in file json template'''
def add_measures_template(list_templates):
    if(type(list_templates) == list):
        diz_templates = {}
        for template in list_templates:
            list_measures = create_model_list(json_templates_path, template)
            try:     
                diz_templates[get_substring(template, stop=".")] = {"measures_max":len(list_measures), "measures_selected":len(list_measures)}  
            except:
                pass
        save_json_file(join(realpath (''),"configuration", "template_measures_config.json"), diz_templates) 


'''Create dict model''' 
def create_model_list(path_file, model):
    file_model = read_json_file(join(path_file, model))
    list_measures = []
    try:
        for model in file_model["parameters"]["filter_tag"]:
            if(model["tag"] != "CommunicationCode"):
                list_measures.append(get_substring(model["tag"], start="."))
    except:
        pass
    return(list_measures)
    

'''Convert class bytes object into json dictionary'''
def binary_to_dict(the_binary):
   a = the_binary
   dic = json.loads(a.decode("utf-8"))
   return dic


'''RETURN: None'''
def create_logs(dict_response, hierarchy_name):
    t = datetime.datetime.utcnow()
    log_date = t.strftime('%y%m%dT%H%M')
    save_json_file(join(realpath(''), logs_path, log_date +"-"+ hierarchy_name+'.json'), dict_response)
    return send_mail(hierarchy_name, join(realpath(''), logs_path, log_date +"-"+ hierarchy_name + '.json'))


'''Toolbar function for getting thing activation information'''
def create_post_files(thing, hierarchy_name, endpoint, command_id, environment_prefix, env):
    data = {}
    data[thing] = []
    data[thing].append({
        'endpoint': endpoint,
        'command_id': command_id,
        'environment_prefix': environment_prefix,
        'env' :  env
    })
    makedirs(join(realpath(''), post_files_path, hierarchy_name), mode = 0o777, exist_ok= True)
    with open(join(realpath(''), post_files_path, hierarchy_name, thing), 'w') as outfile:
        json.dump(data, outfile, indent = 4)

'''Function for sending Email'''
def send_mail(obj, message):
    try:
        json = read_json_file(message)
        dict_email_params = read_json_file(join(realpath(''), "configuration", "email_config.json"))
        smtp_server = dict_email_params["smtp_server"]
        port = dict_email_params["port"]
        user = dict_email_params["user"]
        password = dict_email_params["password"]
        subject = dict_email_params["subject"]
        send_to = dict_email_params["send_to"]

        msg = MIMEMultipart()
        msg['From'] = subject
        msg['To'] = send_to
        msg['Subject'] = obj
        msg.attach(MIMEText(str(json)))

        server = SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.login(user,password)
        server.send_mail(
            subject,
            send_to,
            msg.as_string())
        server.close()
        return True
    except:
        return False


def change_email_send_to(send_to):
    is_valid = validate_email(send_to)
    if(is_valid == True):
        with open(join(realpath(''), "configuration", "email_config.json"), 'r') as file:
            dic = json.load(file)
        dic["send_to"] = send_to
        with open(join(realpath(''), "configuration", "email_config.json"), 'w') as file:
            json.dump(dic, file, indent=4)
        return True
    else:
        return False


def change_email_subject(subject):
    is_valid = validate_email(subject)
    if(is_valid == True):
        with open(join(realpath(''), "configuration", "email_config.json"), 'r') as file:
            dic = json.load(file)
        dic["subject"] = subject
        with open(join(realpath(''), "configuration", "email_config.json"), 'w') as file:
            json.dump(dic, file, indent=4)
        return True
    else:
        return False