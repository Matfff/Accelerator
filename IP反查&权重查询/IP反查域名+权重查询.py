#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject 
@File    ：IP反查域名+权重查询.py
@Author  ：
@Date    ：2023-11-01 14:40 
@脚本说明：
"""

import json
import re, time
import requests
from fake_useragent import UserAgent
from tqdm import tqdm
from lxml import etree


class IPToDomain:

    def __init__(self, path, rank=False):
        # 清空文件
        with open('查询结果.json', 'w'):
            pass
        with open('./反查失败列表.txt', 'w'):
            pass
        with open('./tmp.txt', 'w'):
            pass
        with open('./权重不小于1的HOST.txt', 'w'):
            pass
        with open('./反查域名列表.txt', 'w'):
            pass
        self.used_ip_list = []  # 反查过的IP，用于host去重
        self.path = path
        self.result_json = {}
        self.ip_list = []
        self.hostname_list = []
        # self.read_ip()
        self.hostname()
        self.is_rank = rank

    # 读取IP
    def read_ip(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            stripped_lines = list(map(lambda line: line.rstrip(), lines))
            for line in stripped_lines:
                pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
                match = re.findall(pattern, line)
                if match:
                    ip = match[0]
                    # print(ip)
                    self.ip_list.append(ip)

        # 去重
        self.ip_list = set(self.ip_list)

    # 读取host
    def hostname(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            stripped_lines = list(map(lambda line: line.rstrip(), lines))
            for line in stripped_lines:
                pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
                # 提取域名
                pattern2 = r"://([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?:\d{1,5})|://([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?)"
                match = re.findall(pattern, line)
                match2 = re.findall(pattern2, line)
                if match:
                    hostname = match[0]
                    # print(ip)
                    self.hostname_list.append(hostname)
                elif match2:
                    if match2[0][0]:
                        hostname = match2[0][0]
                        self.hostname_list.append(hostname)
                    elif match2[0][2]:
                        hostname = match2[0][2]
                        self.hostname_list.append(hostname)
                else:
                    pass

        # 去重
        self.hostname_list = set(self.hostname_list)
        # print(self.hostname_list)

    # 查询权重
    def rank(self, domain):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,vi;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://www.aizhan.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'linux',
        }
        # 爱站的网站url
        aizhanurl = 'https://www.aizhan.com/cha/'
        # 获取查询的网站的url
        chaxunurl = domain
        # print("[+] 正在查询：" + chaxunurl)
        url = aizhanurl + chaxunurl
        # time.sleep(1)  # 延迟1s
        res = requests.get(url, headers=headers)
        # print("[-] 请求url：" + url)
        html = res.text.encode(res.encoding).decode('utf-8')
        tree = etree.HTML(html)
        br = tree.xpath('//a[@id="baidurank_br"]//img//@alt')  # 百度权重
        mbr = tree.xpath('//a[@id="baidurank_mbr"]//img//@alt')  # 移动权重
        pr = tree.xpath('//a[@id="360_pr"]//img//@alt')  # 360权重
        sm_pr = tree.xpath('//a[@id="sm_pr"]//img//@alt')  # 神马权重
        sogou_pr = tree.xpath('//a[@id="sogou_pr"]//img//@alt')  # 搜狗权重
        google_pr = tree.xpath('//a[@id="google_pr"]//img//@alt')  # 谷歌权重
        result = {
            f"{chaxunurl}": [f"百度权重: Rank{br[0]}", f"移动权重: Rank{mbr[0]}", f"360权重: Rank{pr[0]}",
                             f"神马权重: Rank{sm_pr[0]}", f"搜狗权重: Rank{sogou_pr[0]}",
                             f"谷歌权重: Rank{google_pr[0]}"]
        }
        return result

    # ip138
    def ip138_chaxun(self, ip, ua):
        ip138_headers = {
            'Host': 'site.ip138.com',
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://site.ip138.com/'}
        ip138_url = 'https://site.ip138.com/' + str(ip) + '/'
        try:
            ip138_res = requests.get(url=ip138_url, headers=ip138_headers, timeout=2).text
            if '<li>暂无结果</li>' not in ip138_res:
                result_site = re.findall(r"""</span><a href="/(.*?)/" target="_blank">""", ip138_res)
                return result_site
        except:
            pass

    # 爱站
    def aizhan_chaxun(self, ip, ua):
        aizhan_headers = {
            'Host': 'dns.aizhan.com',
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://dns.aizhan.com/'}
        aizhan_url = 'https://dns.aizhan.com/' + str(ip) + '/'
        try:
            aizhan_r = requests.get(url=aizhan_url, headers=aizhan_headers, timeout=2).text
            aizhan_nums = re.findall(r'''<span class="red">(.*?)</span>''', aizhan_r)
            if int(aizhan_nums[0]) > 0:
                aizhan_domains = re.findall(r'''rel="nofollow" target="_blank">(.*?)</a>''', aizhan_r)
                return aizhan_domains
        except:
            pass

    # scan
    def catch_result(self, host):
        rank_list = []
        domain_list = []
        ua_header = UserAgent()
        pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        match = re.findall(pattern, host)
        try:
            # 将host中的ip筛选出来，进行IP反查
            if match:
                ip = match[0]
                if not (ip in self.used_ip_list):
                    self.used_ip_list.append(ip)
                    ip138_result = self.ip138_chaxun(ip, ua_header)
                    aizhan_result = self.aizhan_chaxun(ip, ua_header)
                    time.sleep(1)
                    if ((ip138_result != None and ip138_result != []) or (aizhan_result != None and aizhan_result != [])):
                        ############################################
                        # 合并结果
                        #
                        if ip138_result:
                            for i in ip138_result:
                                domain_list.append(i)
                        if aizhan_result:
                            for i in aizhan_result:
                                domain_list.append(i)
                        domain_list = list(set(domain_list))
                        # 反查域名列表
                        with open('./反查域名列表.txt', 'a', encoding='utf-8') as file:
                            if domain_list:
                                for domain in domain_list:
                                    file.write(f"{domain}\n")
                else:
                    with open("反查失败列表.txt", 'a', encoding='utf-8') as file:
                        file.write(ip + "\n")
            else:
                domain_list.append(host)
            ############################################
            #
            ############################################
            # 权重查询
            if self.is_rank:
                if domain_list:
                    for url in domain_list:
                        rank_resule = self.rank(url)
                        rank_list.append(rank_resule)
                    domain_list = rank_list
                # 记录权重不小于1的HOST
                with open('权重不小于1的HOST.txt', 'a', encoding='utf-8') as f:
                    for i in range(1, 11):
                        if f'Rank{i}' in json.dumps(domain_list, ensure_ascii=False):
                            f.write(host + "\n")
                            break
            ############################################
            #
            if domain_list:
                self.result_json[f'{host}'] = domain_list
                result = {f"{host}": self.result_json[f'{host}']}
                with open('./tmp.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")
                print(result)
        except:
            pass



if __name__ == '__main__':
    ###############################################
    # 参数1: IP文本路径
    # 参数2: 是否开启权重查询
    scan = IPToDomain(path='./url_list.txt', rank=True)
    #
    #
    print('================================================================')
    print(r'[-]  本脚本会自动提取 :\\开头的 IP、域名、去重')
    print('[-]  最终保存结果为json文件')
    print(f'[+]  host count: {len(scan.hostname_list)}')
    print('================================================================')
    print()
    #
    #
    ###############################################
    #
    for hostname in tqdm(scan.hostname_list):
        # print(i)
        scan.catch_result(hostname)
    with open("./查询结果.json", 'a', encoding='utf-8') as f:
        f.write(json.dumps(scan.result_json, ensure_ascii=False))

