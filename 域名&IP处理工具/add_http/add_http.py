#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject 
@File    ：check_http.py
@Author  ：fang
@Date    ：2023-11-04 21:18 
@脚本说明：检测域名是不是http开头，如果不是则添加http
"""

with open('./url_http.txt', 'w'):
    pass
with open('./url.txt', 'r') as file:
    lines = file.readlines()
    stripped_lines = list(map(lambda line: line.rstrip(), lines))
    stripped_lines = list(set(stripped_lines))
    with open('./url_http.txt', 'a') as f:
        for line in stripped_lines:
            if line.startswith('http'):
                f.write(line+'\n')
            else:
                f.write(f'http://{line}\n')
