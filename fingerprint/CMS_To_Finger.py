#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject 
@File    ：CMS_To_Finger.py
@Author  ：fang
@Date    ：2023-11-08 11:45 
@脚本说明：
"""
import copy
import json
import re
from colorama import init, Fore


class CMSToFinger:

    def __init__(self):
        init(autoreset=True)
        # 读取finger.json
        self.finger_json = None
        self.readFinger()
        # with open('./finger.json', 'r', encoding='utf-8') as f:
        #     self.finger_json = json.load(f)
        self.select()

    def __del__(self):
        print(f"{Fore.RED}Success")

    # 选择
    def select(self):
        # self.cmsprint_to_finger()
        self.dismap_to_finger()
        self.goby_to_finger()
        self.ObserverWard_0x727_to_finger()
        self.FingerprintHub_to_finger()
        self.wapplayzergo_to_finger()

    # 读取finger.json
    def readFinger(self):
        with open('./finger.json', 'r', encoding='utf-8') as f:
            count = 0
            self.finger_json = json.load(f)
            for i in self.finger_json['fingerprint']:
                for j in i['keyword']:
                    count = count + 1
            print(f"Finger CMS: {count}")

    # 写入
    def execute(self, operator):
        count = 0
        self.finger_json['fingerprint'] = self.deduplication(self.finger_json['fingerprint'])
        for i in self.finger_json['fingerprint']:
            for j in i['keyword']:
                count = count + 1
        print(f"{Fore.GREEN}[+] after {operator} CMS: {count}")
        result = {
            "fingerprint": self.finger_json['fingerprint']
        }
        with open('./CMS_Result.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False))

    # 去重
    def deduplication(self, data_list):
        result1 = []
        result2 = []
        result3 = []
        check = []
        # 字典 --> json
        for d in data_list:
            d = json.dumps(d)
            result1.append(d)
        # result1 = list(set(result1))
        """
        使用字典实现去重：
            将数据进行大小写转换，作为key，原数据作为value
            {
                "data.lower()": data
            }
        """
        my_dict = {}
        for word in result1:
            my_dict[word.lower()] = word
        result1 = list(my_dict.values())

        # json列表 --> 列表字典 [{},{},{}]
        for item in result1:
            item = json.loads(item)
            result2.append(item)

        """
        不能进行合并，keyword是与匹配，不是或匹配
        """
        # 合并
        # for i in result2:
        #     tmp = copy.deepcopy(i)  # 深度拷贝
        #     del tmp['keyword']
        #     tmp = json.dumps(tmp)
        #     if tmp not in check:
        #         check.append(tmp)
        #         result3.append(i)
        #     else:
        #         tmp_list = []
        #         # print(i['cms'])
        #         # 获取重复数据的下标
        #         index = check.index(tmp)
        #         # 合并数据
        #         for data1 in i['keyword']:
        #             tmp_list.append(data1)
        #         for data2 in result3[index]['keyword']:
        #             tmp_list.append(data2)
        #         tmp_list = list(set(tmp_list))
        #         result3[index]['keyword'] = tmp_list

        return result2

    # cmsprint_to_finger
    # def cmsprint_to_finger(self):
    #     # 读取cmsprint.json
    #     with open('./cmsprint.json', 'r', encoding='utf-8') as f:
    #         data_list = json.load(f)
    #
    #     # print(data_list['RECORDS'])
    #     for item in data_list['RECORDS']:
    #         if item['keyword'] != '' and item['homeurl'] != '' and item['checksum'] == '' and not (r'.js' in item['homeurl']):
    #             self.finger_json['fingerprint'].append({
    #                 "cms": item['remark'],
    #                 "method": "keyword",
    #                 "location": "body",
    #                 "keyword": [f"{item['keyword']}"]
    #             })
    #     self.execute('cmsprint to finger')

    # dismap to finger
    def dismap_to_finger(self):
        with open('./dismap.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            stripped_lines = list(map(lambda line: line.rstrip(), lines))
            for line in stripped_lines:
                if line == '':
                    continue
                tmp = line
                line = line.split(",")

                pattern1 = r"\"(.*)\""
                match1 = re.findall(pattern1, line[1].strip())
                cms = match1[0]

                pattern2 = r"\"(.*)\""
                match2 = re.findall(pattern2, line[2].strip())
                _type = match2[0]  # body header ico body|header

                pattern3 = r"\"\((.*?)\)\""
                match3 = re.findall(pattern3, tmp)
                if match3:
                    # print(match3[0])
                    match3[0] = match3[0].replace("\\\"", "\"")
                    keyword = match3[0].split("|")
                    if _type == "body":
                        r = {
                            "cms": cms,
                            "method": "keyword",
                            "location": "body",
                            "keyword": keyword
                        }
                        self.finger_json['fingerprint'].append(r)
                    elif _type == "header":
                        r = {
                            "cms": cms,
                            "method": "keyword",
                            "location": "header",
                            "keyword": keyword
                        }
                        self.finger_json['fingerprint'].append(r)
                    # else:
                    #     print("dismap_to_finger: " + tmp + "\n  -->  Please complete it yourself")
                else:
                    # print(Fore.RED + "dismap_to_finger: " + tmp + "\n  -->  Please complete it yourself")
                    pass
        self.execute('dismap to finger')

    # goby to finger
    def goby_to_finger(self):
        with open('./goby.json', 'r', encoding='utf-8') as f:
            data_list = json.load(f)
            for d in data_list:
                if not d:
                    continue
                cms = d['product']
                tmp = json.dumps(d['rules'])
                if 'body_contains' in tmp and not ('title_contains' in tmp) and not ('header_contains' in tmp) and not (
                        'banner_contains' in tmp):
                    keyword_list = []
                    for _type_list in d['rules']:
                        for _type_dict in _type_list:
                            keyword_list.append(_type_dict['content'])
                    r = {
                        "cms": cms,
                        "method": "keyword",
                        "location": "body",
                        "keyword": keyword_list
                    }
                    self.finger_json['fingerprint'].append(r)
                # print(d['rules'])
                if 'header_contains' in tmp and not ('title_contains' in tmp) and not ('body_contains' in tmp) and not (
                        'banner_contains' in tmp):
                    header_list = []
                    for _type_list in d['rules']:
                        for _type_dict in _type_list:
                            header_list.append(_type_dict['content'])
                    r = {
                        "cms": cms,
                        "method": "keyword",
                        "location": "header",
                        "keyword": header_list
                    }
                    self.finger_json['fingerprint'].append(r)
        self.execute('goby to finger')

    # ObserverWard_0x727 to finger
    def ObserverWard_0x727_to_finger(self):
        with open('./ObserverWard_0x727.json', 'r', encoding='utf-8') as f:
            data_list = json.load(f)
            for d in data_list['/']:
                if not d:
                    continue
                cms = d['name']
                if d['headers'] != {} and d['keyword'] == []:
                    header_list = []
                    for key, value in d['headers'].items():
                        h = f"{key}: {value}"
                        header_list.append(h)
                    r = {
                        "cms": cms,
                        "method": "keyword",
                        "location": "header",
                        "keyword": header_list
                    }
                    self.finger_json['fingerprint'].append(r)

                if d['headers'] == {} and d['keyword'] != []:
                    r = {
                        "cms": cms,
                        "method": "keyword",
                        "location": "body",
                        "keyword": d['keyword']
                    }
                    self.finger_json['fingerprint'].append(r)
        self.execute('ObserverWard_0x727 to finger')

    # FingerprintHub to finger
    def FingerprintHub_to_finger(self):
        with open('FingerprintHub.json', 'r', encoding='utf-8') as f:
            data_list = json.load(f)

            for d in data_list:
                if not d:
                    continue
                cms = d['name']
                for fingerprint_dice in d['fingerprint']:
                    if fingerprint_dice['favicon_hash']:
                        continue

                    if fingerprint_dice['keyword'] != [] and fingerprint_dice['headers'] == {}:
                        # print(fingerprint_dice)
                        r = {
                            "cms": cms,
                            "method": "keyword",
                            "location": "body",
                            "keyword": fingerprint_dice['keyword']
                        }
                        self.finger_json['fingerprint'].append(r)

                    if fingerprint_dice['keyword'] == [] and fingerprint_dice['headers'] != {}:
                        header_list = []
                        for key, value in fingerprint_dice['headers'].items():
                            h = f"{key}: {value}"
                            header_list.append(h)
                        r = {
                            "cms": cms,
                            "method": "keyword",
                            "location": "header",
                            "keyword": header_list
                        }
                        self.finger_json['fingerprint'].append(r)
        self.execute('FingerprintHub to finger')

    # wapplayzergo to finger
    def wapplayzergo_to_finger(self):
        with open('wapplayzergo.json', 'r', encoding='utf-8') as f:
            data = json.load(f)['apps']
            for key, value in data.items():
                cms = key
                try:
                    s = json.dumps(value)
                    if value['headers'] and not ("cookies" in s) and not ('*' in s) and not ('?:' in s) and not (
                            r'\\d' in s) and not (r'(.+)' in s):
                        value = json.dumps(value)
                        value = value.replace('^', '')
                        value = value.replace('$', '')
                        value = json.loads(value)
                        # print(value['headers'])
                        header_list = []
                        for k, v in value['headers'].items():
                            h = f"{k}: {v}"
                            header_list.append(h)
                        r = {
                            "cms": cms,
                            "method": "keyword",
                            "location": "header",
                            "keyword": header_list
                        }
                        self.finger_json['fingerprint'].append(r)
                except:
                    pass
        self.execute('wapplayzergo to finger')


if __name__ == '__main__':
    CMSToFinger()


