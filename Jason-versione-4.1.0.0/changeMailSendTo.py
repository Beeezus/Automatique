from validate_email import validate_email
from os.path import join, realpath
import json


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
