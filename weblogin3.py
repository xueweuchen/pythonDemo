# -*- coding: utf-8 -*-
import re
import json
import urllib
import base64
import binascii
import os

import rsa
import requests
from get_name_pwd import get_name_pwd
from get_name_pwd import get_uid_list

import logging
logging.basicConfig(level=logging.DEBUG)

WBCLIENT = 'ssologin.js(v1.4.5)'
user_agent = (
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
    'Chrome/20.0.1132.57 Safari/536.11'
)
session = requests.session()
session.headers['User-Agent'] = user_agent


def encrypt_passwd(passwd, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
    passwd = rsa.encrypt(message.encode('ascii'), key)
    return binascii.b2a_hex(passwd)


def wblogin(username, password):
    resp = session.get(
        'http://login.sina.com.cn/sso/prelogin.php?'
        'entry=sso&callback=sinaSSOController.preloginCallBack&'
        'su=%s&rsakt=mod&client=%s' %
        (base64.b64encode(username.encode('ascii')), WBCLIENT)
    )

    pre_login_str = re.match(r'[^{]+({.+?})', resp.content.decode('ascii')).group(1)
    pre_login = json.loads(pre_login_str)

    pre_login = json.loads(pre_login_str)
    data = {
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'userticket': 1,
        'ssosimplelogin': 1,
        'su': base64.b64encode(urllib.parse.quote(username).encode('ascii')),
        'service': 'miniblog',
        'servertime': pre_login['servertime'],
        'nonce': pre_login['nonce'],
        'vsnf': 1,
        'vsnval': '',
        'pwencode': 'rsa2',
        'sp': encrypt_passwd(password, pre_login['pubkey'],
                             pre_login['servertime'], pre_login['nonce']),
        'rsakv' : pre_login['rsakv'],
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
               'naSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    resp = session.post(
        'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
        data=data
    )

    login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',
                          resp.content.decode('gbk')).group(1)
    resp = session.get(login_url)
    login_str = re.match(r'[^{]+({.+?}})', resp.content.decode('gbk')).group(1)
    return json.loads(login_str)


if __name__ == '__main__':
    # Load the username and password from the configure file
    username, password = get_name_pwd()
    print(wblogin(username, password))     
    # Load the uid list from the configure file
    uid_list = get_uid_list()
    for uid in uid_list:
        IMGPATH = 'picture' + uid + '\\'
        # Create the directary for store the images
        if not os.path.exists(IMGPATH):
            os.mkdir(IMGPATH)
        # Get the album_id list
        response = session.get('http://photo.weibo.com/albums/get_all?uid=' + uid + '&page=1&count=5')
        album_id_json = response.content.decode('utf8')
        # album_id_list = re.findall(r'\"album_id\":\"\d+\"',album_id_json)
        album_id_list_ori = json.loads(album_id_json)['data']['album_list']
        album_id_list = list()
        for album_item in album_id_list_ori:
            id = album_item['album_id']
            count = album_item['count']['photos']
            album_id_list.append((id, count))
        
        for album_id in album_id_list:
            # Get the pic_name list and timestamp
            response = session.get('http://photo.weibo.com/photos/get_all?uid=' + uid + '&album_id=' + album_id[0] + '&count=' + str(album_id[1]) + '&page=1&type=3&__rnd=1396355396834')
            pic_name_json = response.content.decode('utf8')    
            pic_name_list = re.findall(r'\"pic_name\":\"[\w|\.]+\"', pic_name_json)
            for pic_name in pic_name_list:    
                # Download the photo
                pic_name = re.search(r'\"\w+.(jpg|gif)', pic_name).group(0)[1:]
                response = session.get('http://ww4.sinaimg.cn/mw690/' + pic_name)
                with open(IMGPATH + pic_name, mode = 'wb') as fileout:  
                    fileout.write(response.content)
        

