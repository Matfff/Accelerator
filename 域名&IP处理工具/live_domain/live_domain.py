#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject 
@File    ：live_domain.py
@Author  ：fang
@Date    ：2023-11-06 14:26 
@脚本说明：检测存活域名
"""
import time
import requests
import urllib3
import threading


class LiveDomain:

    def __init__(self, thread_count=1):
        self.threadLock = threading.Lock()  # 同步锁
        with open('./result.txt', 'w'):
            pass
        # self.f = open('./result.txt', 'a')
        urllib3.disable_warnings()  # 忽略https证书告警
        self.finish = 0
        self.thread_flag = False
        self.url_list = []
        self.thread_count = thread_count
        self.read_url()
        self.creat_thread()
        threading.Thread(target=self.listen_end, daemon=True).start()

    # 监听线程是否结束
    def listen_end(self):
        time.sleep(3)
        flag = 'live_scan_t'
        current_thread = str(threading.enumerate())
        if flag in current_thread:
            print(f"当前进度： [{self.finish}/{len(self.url_list)}]")
            self.listen_end()
        else:
            self.thread_flag = True

    # 读url
    def read_url(self):
        with open('./url.txt', 'r') as f:
            lines = f.readlines()
            stripped_lines = list(map(lambda line: line.rstrip(), lines))
            self.url_list = list(set(stripped_lines))
        print(f"url count: {len(self.url_list)}")

    # 创建线程
    def creat_thread(self):
        url_count = len(self.url_list)
        try:
            step = url_count // self.thread_count
            if step < 1:
                step = 1
            for start in range(0, url_count, step):
                if self.thread_flag:
                    break
                stop = start + step
                if stop > url_count:
                    stop = url_count
                threading.Thread(name='live_scan_t', target=self.live_scan, args=(start, stop), daemon=True).start()
        except:
            pass

    # scan
    def live_scan(self, start, stop):
        for i in range(start, stop):
            self.finish = self.finish + 1
            if self.thread_flag:
                break
            url = self.url_list[i]
            try:
                res = requests.get(url, verify=False, allow_redirects=False, timeout=3)
                if 200 <= res.status_code < 400:
                    self.write_url(url)
                    # print(url)
            except:
                pass

    # 写入文本
    def write_url(self, url, path="result.txt"):
        # self.threadLock.acquire()  # 同步锁
        with open(path, 'a') as f:
            f.write(url + "\n")
        # self.threadLock.release()


if __name__ == '__main__':
    scan = LiveDomain(thread_count=100)
    while True:
        if scan.thread_flag:
            print("############### 扫描完成 ###############")
            break
        else:
            time.sleep(3)

