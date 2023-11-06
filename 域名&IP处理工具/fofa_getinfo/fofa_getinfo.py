#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject 
@File    ：fofa_getinfo.py
@Author  ：fang
@Date    ：2023-11-06 1:10 
@脚本说明：fofa批量搜索
"""

import requests, base64, os, win32api
from colorama import init, Fore
import urllib3
init(autoreset=True)


urllib3.disable_warnings()

# fofa_email = "809121932@qq.com"
# fofa_key = "69764dbc1a3937c28dddc48a77fb7e85"
fofa_email = "1412673980@qq.com"
fofa_key = "a86e1208376b14817f70bc7886384dbe"
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; PCRT00 Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.158 Safari/537.36 fanwe_app_sdk sdk_type/android sdk_version_name/4.0.1 sdk_version/2020042901 screen_width/720 screen_height/1280',
}
fofa_set = set()


def fofa(target):
    query = 'domain="%s"' % (target)  # fofa查询的语法
    query = (base64.b64encode(query.encode('utf-8'))).decode('utf-8')  # 语法需要经过base64编码
    url_api = 'https://fofa.info/api/v1/search/all?email=%s&key=%s&qbase64=%s&size=10000&fields=host,ip,port&full=true' % (
    fofa_email, fofa_key, query)
    print(Fore.RED + "[INFO]开始调用fofa api查询%s子域..." % (target))
    for i in range(1, 5):
        try:
            response = requests.get(url=url_api, headers=headers, timeout=15, verify=False,
                                    proxies={'https': 'http://127.0.0.1:7890'}).json()
            # print(response)
            if response.get('error') != False:
                print("fofa查询失败\r" + response)
                return
            print('fofa查询成功!')
            subdomain = response.get("results")  # 查询的结果保留在列表中
            # print(subdomain)
            for list in subdomain:
                host = list[0]  # 子域
                ip = list[1]  # 子域所属ip
                port = list[2]  # 开放端口
                if "https" in host:
                    url = host
                else:
                    url = "http://" + host
                print(url)
                fofa_set.add(url)
            break
        except Exception as e:
            print("请求出错，正在尝试重新请求...", e)


if __name__ == '__main__':
    # 批量读取主域名
    for domain in open("domain.txt", 'r'):
        fofa(domain.replace("\n", ""))
    print("获取去重后子域名个数为：", len(fofa_set))

    # 将结果进行保存
    if os.path.exists("fofa_subdomain.txt"):
        os.remove("fofa_subdomain.txt")
    for i in fofa_set:
        with open("fofa_subdomain.txt", "a", encoding="utf-8") as f:
            f.write(i + "\n")
    print(Fore.GREEN + "结果保存完毕！")
    # win32api.ShellExecute(0, 'open', 'fofa_subdomain.txt', '', '', 1)
