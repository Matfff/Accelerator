#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject 
@File    ：get_root_domain.py
@Author  ：fang
@Date    ：2023-11-06 0:45 
@脚本说明：获取根域名
"""
import re

url_list = []
with open('./result.txt', 'w'):
    pass

with open('./url.txt', 'r') as file:
    lines = file.readlines()
    stripped_lines = list(map(lambda line: line.rstrip(), lines))
    stripped_lines = list(set(stripped_lines))
    with open('./result.txt', 'a') as f:
        for line in stripped_lines:
            pattern = r"(?:[a-z]+\:\/\/)?(?:[\w]+\.)?([\w\-]+\.[a-zA-Z]{2,4})\/?(?:[^\s]*)?"
            match = re.match(pattern, line)
            if match:
                # print(match.group(1))
                f.write(match.group(1) + '\n')
                # if line.startswith('http://www.'):
            #     url_list.append(f"{line.replace('http://www.', '')}")
            # elif line.startswith('http://'):
            #     url_list.append(f"{line.replace('http://', '')}")
            # else:
            #     url_list.append(line)
