#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject 
@File    ：cut_out.py
@Author  ：fang
@Date    ：2023-11-06 9:59 
@脚本说明：文本截取截取
"""

with open('./result.txt', 'w'):
    pass

with open('./file.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    stripped_lines = list(map(lambda line: line.rstrip(), lines))
    with open('./result.txt', 'a') as f:
        for line in range(140000, 200000):
            f.write(stripped_lines[line] + '\n')
