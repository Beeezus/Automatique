import time
from utility import binary_to_dict, create_post_files, read_json_file, get_configuration_path
from PyQt5 import QtCore
import httpReq
from os.path import join, realpath
from json import dumps
from time import sleep


def read_credentials(account):
    dict_cred = {}
    pathcredentials = QtCore.QDir.homePath() + '/.aws/credentials'
    with open( pathcredentials , 'r') as fin:
        credentials = fin.read()
    list_credentials = credentials.split("[")
    for lis in list_credentials:
        if( account in lis):
            for attr in lis.split("\n"):
                if("region" in attr or "aws_access_key_id" in attr or "aws_secret_access_key" in attr or "aws_session_token" in attr or "aws_security_token" in attr):
                        key, val =attr.split(" = ")
                        dict_cred[key] = val                    
    return dict_cred


def readfilejson(path):
    with open(path, 'r') as json_file: 
        return json_file.read()


def initialize_activations(hierarchy_name, list_json_file, gateway_id, env_dict):

    account = env_dict[gateway_id]["account"]
    env = env_dict[gateway_id]["environment"]

    dict_credentials = read_credentials(account)
    dict_credentials["account"] = account

    if(env == 'dev_ap11531'):
        dict_cred_g = read_credentials("saml-GG-SH-AWS-IOT-E-Solution-DevQa-esol-ap11531-dev")
    elif(env == 'qa_ap11531'):
        dict_cred_g = read_credentials("saml-GG-SH-AWS-IOT-E-Solution-DevQa-esol-ap11531-qa")
    elif(env == 'prod_ap11531'):
        dict_cred_g = read_credentials("saml-GG-SH-AWS-IOT-E-Solution-Prod-esol-ap11531-prod")

    dict_response = {}    
    if(list_json_file != []):
        for file in list_json_file:
            print("\n<<<Activate "+file+" in progress..")
            response = activate_thing(hierarchy_name, file, dict_credentials, dict_cred_g, api_id, api_id_g, stage, env, env_prefix, gateway_id )
            dict_response[file] = "STATUS:" + str(response[0]) + ";" + "MESSAGE:" + str(response[1]) 
            print(">>>"+file+"\t\t||"+str(response[0])+"\t\t||"+str(response[1]))
    return dict_response


def activate_thing(hierarchy_name, file, dict_credentials, dict_cred_g, api_id, api_id_g, stage, env, env_prefix, gateway_id):
    payload = readfilejson(join(realpath(''),'json_files', hierarchy_name, file))
    endpoint = 'https://' + api_id + '.execute-api.eu-central-1.amazonaws.com/' + stage + '/v1/gateways/' + gateway_id +'/command'
    print("GATEWAY-ID_A:", gateway_id)
    print("API_ID:_A:", api_id)
    print("STAGE_A:", stage)
    print("ENVIRONMENT PREFIX_A:", env_prefix)
    post_response = httpReq.post(dict_credentials, endpoint, stage, payload)
    if(post_response[0] == 200):
        endpoint = 'https://' + api_id_g + '.execute-api.eu-central-1.amazonaws.com/' + env + '/v1/jobs/'
        create_post_files(file, hierarchy_name, endpoint, binary_to_dict(post_response[1])["command_id"], env_prefix, env)
        time.sleep(25)
        response = httpReq.get(dict_cred_g,
            endpoint, 
            binary_to_dict(post_response[1])["command_id"],
            env_prefix,
            env
            )
        return response
    elif(post_response[0] == 403):
        status = post_response[0]
        message = "The security token include in the request is expired"
        response = (status, message)
        return response
    else:
        status = post_response[0]
        message = binary_to_dict(post_response[1])["errors"][0]["error_message"]
        response = (status,message)
        return response


def refresh_get(post_file, hierarchy_name, env):
    file_path = join(realpath(''), get_configuration_path()["post_files_path"], hierarchy_name, post_file)

    if(env == 'dev_ap11531'):
        credentials_g = read_credentials("saml-GG-SH-AWS-IOT-E-Solution-DevQa-esol-ap11531-dev")
    elif(env == 'qa_ap11531'):
        credentials_g = read_credentials("saml-GG-SH-AWS-IOT-E-Solution-DevQa-esol-ap11531-qa")
    elif(env == 'prod_ap11531'):
        credentials_g = read_credentials("saml-GG-SH-AWS-IOT-E-Solution-Prod-esol-ap11531-prod")
        
    thing = read_json_file(file_path)
    endpoint = thing[post_file][0]["endpoint"]
    commandId = thing[post_file][0]["commandId"]
    env_prefix = thing[post_file][0]["environmentPrefix"]

    response = httpReq.get(credentials_g, endpoint, commandId, env_prefix, env)
    return response


def activate_dummy(user_name, password, gateway_id, env_dict):
    credentials = read_credentials(env_dict[gateway_id]["account"])
    credentials["account"] = env_dict[gateway_id]["account"]

    stage = env_dict[gateway_id]["stage"]
    api_id = env_dict[gateway_id]["api_post"]
    api_id_g = env_dict[gateway_id]["api_get"]
    env = env_dict[gateway_id]["environment"]
    env_prefix = env_dict[gateway_id]["environment_prefix"]

    if env == 'dev_ap11531':
        dict_cred_g = read_credentials("saml-GG-SH-AWS-IOT-E-Solution-DevQa-esol-ap11531-dev")
    elif env == 'qa_ap11531':
        dict_cred_g = read_credentials("saml-GG-SH-AWS-IOT-E-Solution-DevQa-esol-ap11531-qa")
    elif env == 'prod_ap11531':
        dict_cred_g = read_credentials("saml-GG-SH-AWS-IOT-E-Solution-Prod-esol-ap11531-prod")

    endpoint = 'https://' + api_id + '.execute-api.eu-central-1.amazonaws.com/' + stage + '/v1/gateways/' + gateway_id +'/command'
   
    data = {
            "version": "1.0",
            "gateway_id": gateway_id,
            "command": "activate-thing",
            "parameters": {
                "interaction_mode": "gateway",
                "outbound_communication_modes": [
                    "topic"
                ],
                "environment_prefix": env_prefix,
                "radio_type": "Eth",
                "filter_tag": [
                    {
                        "id": 1,
                        "period": 1,
                        "tag": "METER_00000000000000_Resource-0.Dummy"
                    }
                ],
                "isHierarchy": True,
                "meter_name": "METER_00000000000000_Resource-0",
                "device_type": "fhttps",
                "serial_number": "DN00000SE000000",
                "model": "Dummy",
                "user_name": user_name,
                "password": password,
                "file_format": {
                    "type": "xml",
                    "root_element": "XML",
                    "data_element": "action/MeterData",
                    "value_element": "Value",
                    "tag_element": "MeterLocalId",
                    "timestamp_element": "AcquisitionDateTime",
                    "timestamp_format": "yyyy-MM-DDTHH:mm:ss.SSS"
                },
                "row_filter": {
                    "column_name": "",
                    "value": ""
                },
                "file_name_filter": {
                    "regex_pattern": "([a-zA-Z0-9_]*)_\\d{14}_\\d{14}",
                    "match_group_value": "Hierarchy_" + user_name
                },
                "maker": "METER_00000000000000_Resource-0"
            }
        }
    payload = dumps(data, indent=4)

    hierarchy_name = "Hierarchy_" + user_name
    endpoint = 'https://' + api_id + '.execute-api.eu-central-1.amazonaws.com/' + stage + '/v1/gateways/' + gateway_id +'/command'
    post_response = httpReq.post(credentials, endpoint, stage, payload)

    if post_response[0] == 200:
        endpoint = 'https://' + api_id_g + '.execute-api.eu-central-1.amazonaws.com/' + env + '/v1/jobs/'
        create_post_files("Dummy", hierarchy_name, endpoint, binary_to_dict(post_response[1])["command_id"], env_prefix, env)
        sleep(25)
        dict_response = httpReq.get(dict_cred_g,
            endpoint, 
            binary_to_dict(post_response[1])["command_id"],
            env_prefix,
            env
            )     
        return dict_response

    elif post_response[0] == 403:
        status = post_response[0]
        message = "The security token include in the request is expired"
        dict_response = (status, message)
        return dict_response
        
    else:
        status = post_response[0]
        message = binary_to_dict(post_response[1])["errors"][0]["error_message"]
        dict_response = (status,message)
        return dict_response