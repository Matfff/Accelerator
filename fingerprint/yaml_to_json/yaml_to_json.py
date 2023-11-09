#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：POC 
@File    ：yaml_to_json.py
@Author  ：fang
@Date    ：2023-11-09 14:26 
@脚本说明：
"""

import yaml
import json
import os

# 遍历yaml目录下的文件
def traverse_directory(path):
    yaml_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            # print(os.path.join(root, file))
            yaml_files.append(os.path.join(root, file))
    return yaml_files


# 将yaml转为json
def yaml_to_json(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)

    json_data = json.dumps(yaml_data)

    return json_data


yamls = traverse_directory('yaml')
result = []
for i in yamls:
    yaml_dict = json.loads(yaml_to_json(i))
    # print(yaml_dict)
    result.append(yaml_dict)

with open('./result.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False))








