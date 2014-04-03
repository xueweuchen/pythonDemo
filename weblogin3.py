# -*- coding: utf-8 -*-
import re
import json
import urllib
import base64
import binascii
import os

import rsa
import requests

import logging
logging.basicConfig(level=logging.DEBUG)

UID = '1662068793'
IMGPATH = 'picture'+ UID +'\\'
os.mkdir(IMGPATH)

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
    print(wblogin('19920314wei@sina.com', '65674663'))        
    # Get the album_id list
    response = session.get('http://photo.weibo.com/albums/get_all?uid=' + UID + '&page=1&count=5')
    album_id_json = response.content.decode('utf8')
    album_id_list = re.findall(r'\"album_id\":\"\d+\"',album_id_json)
    
    for album_id in album_id_list:
        # Get the pic_name list and timestamp
        album_id = re.search(r'\d+',album_id).group(0)
        response = session.get('http://photo.weibo.com/photos/get_all?uid=' + UID + '&album_id=' + album_id + '&count=100&page=1&type=3&__rnd=1396355396834')
        pic_name_json = response.content.decode('utf8')    
        pic_name_list = re.findall(r'\"pic_name\":\"[\w|\.]+\"', pic_name_json)
        for pic_name in pic_name_list:    
            # Download the photo
            pic_name = re.search(r'\"\w+.jpg', pic_name).group(0)[1:]
            response = session.get('http://ww4.sinaimg.cn/mw690/' + pic_name)
            with open(IMGPATH + pic_name, mode = 'wb') as fileout:  
                fileout.write(response.content)
        

