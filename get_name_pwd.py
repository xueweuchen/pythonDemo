# -*- coding: utf-8 -*-
import json

def get_name_pwd():
    username = ''
    password = ''
    with open('conf.json', mode = 'r') as fin:
        conf = fin.read()
        conf = json.loads(conf)
        username = conf['username']
        password = conf['password']
    
    return username, password


def get_uid_list():
    uid_list = list()
    with open('conf.json', mode = 'r') as fin:
        conf = fin.read()
        conf = json.loads(conf)
        uid_list = conf['uid_list']
        
    return uid_list

