#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
qcc 请求头生成
"""
import hashlib
import hmac
import json
from urllib import parse


class SignTool(object):
    def __init__(self):
        self.seeds = {
            "0": "W",
            "1": "l",
            "2": "k",
            "3": "B",
            "4": "Q",
            "5": "g",
            "6": "f",
            "7": "i",
            "8": "i",
            "9": "r",
            "10": "v",
            "11": "6",
            "12": "A",
            "13": "K",
            "14": "N",
            "15": "k",
            "16": "4",
            "17": "L",
            "18": "1",
            "19": "8"
        }
        self.n = 20

    def generate_map_result(self, s):
        if not s:
            s = "/"
        s = s.lower()
        s = s + s
        k = ''
        for i in s:
            k += self.seeds[str(ord(i) % 20)]
        return k

    @staticmethod
    def sign_with_hmac(key, s):
        return hmac.new(bytes(key, encoding='utf-8'), bytes(s, encoding='utf-8'), hashlib.sha512).hexdigest()

    def get_head_key(self, s):
        s = s.lower()
        map_result = self.generate_map_result(s)
        key = self.sign_with_hmac(map_result, s)
        return key[10:10 + 20]

    def get_head_value(self, url, data=None):
        if not url:
            url = "/"
        if not data:
            data = {}
        key = url.lower()
        # JSON.stringify(data).toLowerCase()
        data_s = json.dumps(data, ensure_ascii=False).lower()
        enc_data = key + key + data_s
        enc_key = self.generate_map_result(key)
        result = self.sign_with_hmac(enc_key, enc_data)
        return result

    def get_header(self, url):
        paths = parse.urlparse(url)
        uri = paths.path + "?" + paths.query
        header_key = self.get_head_key(uri)
        header_val = self.get_head_value(uri)
        return {header_key: header_val}


sign_tool = SignTool()

if __name__ == '__main__':
    print(sign_tool.get_header('https://www.qcc.com/api/elib/getNewCompany?countyCode=&flag=&industry=&isSortAsc=false&pageSize=20&province=&sortField=startdate&startDateEnd='))
