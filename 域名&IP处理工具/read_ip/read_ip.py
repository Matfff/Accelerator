#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject 
@File    ：read_ip.py
@Author  ：fang
@Date    ：2023-11-01 12:49 
@脚本说明：读取IP
"""
import re


def read_hostname():
    hostname_list = []
    with open('./url.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        stripped_lines = list(map(lambda line: line.rstrip(), lines))
        for line in stripped_lines:
            # match = re.findall('://(.*)$', line)
            pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            match = re.findall(pattern, line)
            if match:
                hostname = match[0]
                # print(hostname)
                hostname_list.append(hostname)
    # 去重
    hostname_list = set(hostname_list)
    for i in hostname_list:
        print(i)
    print(f"hostname count: {len(hostname_list)}")



def read_ip():
    ip_list = []
    with open('./url.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        stripped_lines = list(map(lambda line: line.rstrip(), lines))
        for line in stripped_lines:
            # match = re.findall('://(.*)$', line)
            pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            match = re.findall(pattern, line)
            if match:
                ip = match[0]
                # print(ip)
                ip_list.append(ip)

    # 去重
    ip_list = set(ip_list)
    for i in ip_list:
        print(i)
    print(f"ip count: {len(ip_list)}")


read_hostname()
# read_ip()
