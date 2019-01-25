import utility
from os.path import join, realpath, exists, basename, isfile, isdir
from os import mkdir, remove
from shutil import copy 


'''CONFIGURATION PATH'''
dict_configuration_path = utility.get_configuration_path()
json_templates_path = dict_configuration_path["json_templates_path"]
excel_templates_path = dict_configuration_path["excel_templates_path"]
json_files_path = dict_configuration_path["json_files_path"]
excel_files_path = dict_configuration_path["excel_files_path"]
hierarchy_path = dict_configuration_path["hierarchy_path"]
excel_final_path = dict_configuration_path["excel_final_path"]
logs_path = dict_configuration_path["logs_path"]
post_files_path = dict_configuration_path["post_files_path"]


'''PATH FOR JSON FILE GENERATED'''
def change_json_path(path_file):
    if(exists(join(path_file,"json_files")) == False):
        mkdir(join(path_file,"json_files"))
    dict_configuration_path["json_files_path"] = join(path_file, "json_files")
    utility.save_json_file(join(realpath(''), "configuration", "path_config.json"), dict_configuration_path) 
    return True
    

'''PATH FOR HIERARCHY FILE'''
def change_hierarchy_path(path_file):
    if(exists(join(path_file,"hierarchy")) == False):
        mkdir(join(path_file,"hierarchy"))
    dict_configuration_path["hierarchy_path"] = join(path_file, "hierarchy")
    utility.save_json_file(join(realpath(''), "configuration", "path_config.json"), dict_configuration_path)
    return True


'''PATH FOR TEMPLATE FILE'''
def change_template_path(path_file):
    if(exists(join(path_file,"json_templates")) == False):
        mkdir(join(path_file,"json_templates"))
    dict_configuration_path["json_templates_path"] = join(path_file, "json_templates")
    utility.save_json_file(join(realpath(''), "configuration", "path_config.json"), dict_configuration_path)
    return True
    

'''PATH FOR EXCEL FILE GENERATED'''   
def change_excel_path(path_file):
    if(exists(join(path_file,"excel_files")) == False):
        mkdir(join(path_file,"excel_files"))
    dict_configuration_path["excel_files_path"] = join(path_file, "excel_files")
    utility.save_json_file(join(realpath(''), "configuration", "path_config.json"), dict_configuration_path)
    return True


'''PATH FOR EXCEL TEMPLATES'''   
def change_excel_templates_path(path_file):
    if(exists(join(path_file,"excel_templates")) == False):
        mkdir(join(path_file,"excel_templates"))
    dict_configuration_path["excel_templates_path"] = join(path_file, "excel_templates")
    utility.save_json_file(join(realpath(''), "configuration", "path_config.json"), dict_configuration_path)
    return True


'''PATH FOR EXCEL APPEND FILE GENERATED'''   
def change_excel_final_path(path_file):
    if(exists(join(path_file,"excel_final")) == False):
        mkdir(join(path_file,"excel_final"))
    dict_configuration_path["excel_final_path"] = join(path_file, "excel_final")
    utility.save_json_file(join(realpath(''), "configuration", "path_config.json"), dict_configuration_path)
    return True
    

'''PATH FOR LOG'''   
def change_logs_file_path(path_file):
    if(exists(join(path_file,"logs")) == False):
        mkdir(join(path_file,"logs"))
    dict_configuration_path["logs_path"] = join(path_file, "logs")
    utility.save_json_file(join(realpath(''), "configuration", "path_config.json"), dict_configuration_path)
    return True


'''PATH POST FILES'''   
def change_post_files_path(path_file):
    if(exists(join(path_file,"post_files")) == False):
        mkdir(join(path_file,"post_files"))
    dict_configuration_path["post_files_path"] = join(path_file, "post_files")
    utility.save_json_file(join(realpath(''), "configuration", "path_config.json"), dict_configuration_path)
    return True
    

'''RESET DEFAULT PATH'''
def reset_path(): 
    path_file = realpath('')
    if(exists(join(path_file,"json_files")) == False):
        mkdir(join(path_file,"json_files"))  
        
    if(exists(join(path_file,"hierarchy")) == False):
        mkdir(join(path_file,"hierarchy"))        
        
    if(exists(join(path_file,"excel_files")) == False):
        mkdir(join(path_file,"excel_files"))
    
    if(exists(join(path_file,"excel_templates")) == False):
        mkdir(join(path_file,"excel_templates"))

    if(exists(join(path_file,"json_templates")) == False):
        mkdir(join(path_file,"json_templates"))

    if(exists(join(path_file,"excel_final")) == False):
        mkdir(join(path_file,"excel_final"))

    if(exists(join(path_file,"logs")) == False):
        mkdir(join(path_file,"logs"))

    if(exists(join(path_file,"post_files")) == False):
        mkdir(join(path_file,"post_files"))

    dict_configuration_path["json_files_path"] = join(path_file, "json_files")
    dict_configuration_path["hierarchy_path"] = join(path_file, "hierarchy")
    dict_configuration_path["excel_files_path"] = join(path_file, "excel_files")    
    dict_configuration_path["excel_templates_path"] = join(path_file, "excel_templates")    
    dict_configuration_path["json_templates_path"] = join(path_file, "json_templates")  
    dict_configuration_path["excel_final_path"] = join(path_file, "excel_final")
    dict_configuration_path["logs_path"] = join(path_file, "logs")
    dict_configuration_path["post_files_path"] = join(path_file, "post_files")
    utility.save_json_file(join(path_file, "configuration", "path_config.json"), dict_configuration_path)


'''Change email'''
def change_email(string):
    try:
        path_file = join(realpath (''), "configuration", "email_config.json")
        file_config = utility.read_json_file(path_file)
        file_config["send_to"] = string
        utility.save_json_file(path_file, file_config)  
        return True
    except:
        return False
       

'''CONTROL PATH EXIST'''
def control_paths():
    if(exists(json_files_path) == False):
        mkdir(json_files_path)
    
    if(exists(hierarchy_path) == False):  
        mkdir(join(hierarchy_path))

    if(exists(excel_files_path) == False):
        mkdir(join(excel_files_path))

    if(exists(excel_templates_path) == False):
        mkdir(join(excel_templates_path))

    if(exists(excel_final_path) == False):
        mkdir(join(excel_final_path))

    if(exists(json_templates_path) == False):
        mkdir(join(json_templates_path)) 

    if(exists(logs_path) == False):
        mkdir(join(logs_path))        

    if(exists(post_files_path) == False):
        mkdir(join(post_files_path))          


'''ADD NEW TEMPLATE JSON'''    
def add_json_template(path_file):
    file_path = basename(path_file)  
    if(isfile(path_file) and utility.get_substring(file_path, start=".") == "json"):
        copy(path_file, join(json_templates_path))
        utility.refresh_template_configuration()
        return True
    elif(isdir(path_file)):
        list_files = utility.create_file_list(path_file, ".json")
        for file in list_files:
            copy(join(path_file, file), join(json_templates_path))
        utility.add_measures_template(list_files)
        return True
    else: 
        return False
    

'''ADD NEW HIERARCHY'''
def add_file_hierarchy(path_file):  
    file_path = basename(path_file)   
    if(isfile(path_file) and utility.get_substring(file_path, start=".") == "xml"):
        copy(path_file, hierarchy_path)  
        return True
    elif(isdir(path_file)):
        list_files = utility.create_file_list(path_file, ".xml")
        for file_hierarchy in list_files:
            copy(join(path_file, file_hierarchy), hierarchy_path)
        return True
    else:	
        return False


'''DELETE JSON TEMPLATE'''
def delete_json_templates(list_templates):
    try:
        for template in list_templates:
            remove(join(json_templates_path, template))
            utility.refresh_template_configuration()
        return True
    except:
        return False


'''DELETE HIERARCHIES'''
def delete_hierarchies(list_hierarchies):
    try:
        for hierarchy in list_hierarchies:
            remove(join(hierarchy_path, hierarchy))
        return True
    except:
        return False

