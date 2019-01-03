import os
import json
import requests
from urllib import parse
import sys
import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import time
from tqdm import tqdm

def get_play_list(url):
    # <a.+?href=\"(.+?)\".*>(.+)</a>
    # site-piclist_pic_link
    r = requests.get(url)
    p = re.compile('<a.+?href=\"(.+?)\".*>(.+)</a>')
    html = r.content.decode('utf-8')
    m = p.findall(html)
    _tmp = []
    _chk = False
    for s in m:
        if s[1] == '查看全部剧集详情':
            _chk = True
            continue
        if s[1] == '收起':
            break
        if _chk:
            _tmp.append(s)
    return _tmp


def agent(url, id=0):
    os.system('rm -rf ' + str(id) + '.json')
    try:
        os.system('you-get --json ' + url + ' >> ' + str(id) + '.json')
        _f = open(str(id) + '.json', 'r', encoding='utf8')
        _json = json.load(_f)
        _title = _json['title']
        _url = _json['url']
        _streams = _json['streams']
        os.system('mkdir ' + _title)
        for p in _streams:
            _type = p
            _value = _streams[p]
            _m3u8_url = _value['m3u8_url']
            os.system('curl -s \"' + _m3u8_url + '\" -o ' +
                    _title + '/' + _type + '.m3u8')
            _file = open(_title + '/' + _type + '.m3u8', 'r')
            _writer = open(_title + '/' + _type, 'w')
            for _lines in _file:
                try:
                    o = dict(parse.parse_qsl(parse.urlsplit(_lines).query))
                    length = o['contentlength']
                    _writer.write(str(length) + '\n')
                except:
                    pass
            _writer.close()
            _file.close()
            os.system('rm -f ' + _title + '/' + _type + '.m3u8')
        _f.close()
        os.system('mv ' + str(id) + '.json ' + _title + '/' + 'index.json')
        return True
    except:
        _f.close()
        os.system('rm -f ' + str(id) + '.json')
        return False

RETRY = 10
for (p, q) in tqdm(get_play_list(sys.argv[1])):
    for r in range(RETRY):
        if agent('http:' + p):
            break
# agent(sys.argv[1])
