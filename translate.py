# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 22:08:27 2014

@author: xueweuchen
"""
import requests
import urllib
import re

import logging
logging.basicConfig(level=logging.DEBUG)


def translate(word_ori):
    user_agent = (
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
    'Chrome/20.0.1132.57 Safari/536.11'
    )
    session = requests.session()
    session.headers['User-Agent'] = user_agent
    data = 'client=t&sl=zh-CN&tl=en&hl=zh-CN&sc=2&ie=UTF-8&oe=UTF-8&prev=btn&ssel=0&tsel=0&q=' + urllib.parse.quote(word_ori)
    resp = session.get('http://translate.google.cn/translate_a/t?' + data)
    trans_match = re.match(r'(\[)+\"[\w\-\s]+\"', resp.content.decode('utf8')).group(0)
    return re.search(r'[\w\-\s]+', trans_match).group(0) 
    
if __name__ == "__main__":
    with open('index.html', 'wb') as fout:    
        print(translate('凯文-杜兰特'))
