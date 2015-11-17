#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Chufuyuan
# Mail: chufuyuan01@chinatopcredit.com
# Date: 15/11/6

import random
from multiprocessing import Queue
from threading import Thread
import time
import requests
from pyquery import PyQuery


class SimpleSpider(Thread):
    def __init__(self, keyword, queue):
        super(SimpleSpider, self).__init__()
        self._keyword = keyword
        self._chrome_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) " + \
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
        self._firefox_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0"
        self._ua = [self._chrome_ua, self._firefox_ua]
        self._accept_language = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
        self._url = "http://www.baidu.com/s?ie=UTF-8&wd=%s" % self._keyword
        self._cookie = "PSTM=1443951712; BIDUPSID=9ABF661BF402763910B4E6857AEEB283; " \
                       "BAIDUID=00CF36CC3258FEC97E1B28A2336BB89F:FG=1; ispeed_lsm=0; " \
                       "BDUSS=BWOGFUMUNIZVhCMy0ySkhjVm9sNFZXT0FOSFk0UmEwSXN3YWFwRVFvbVIyMTVXQVFBQUFBJCQAA" \
                       "AAAAAAAAAEAAAANMNRUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
                       "AAAAAAAAAAAAAAAAAAAAAAAJFON1aRTjdWM3; H_WISE_SIDS=100039_100291; BDSFRCVID=M2PsJe" \
                       "C62wwq3ir4hhsQ2Q3ErEjoDGbTH6aIYg2YCfKe7MoD4XGkEG0PJ3lQpYD-TkKZogKK0eOTHkOP; " \
                       "H_BDCLCKID_SF=Jb4D_IKhfIvbfP0kh4n_hPD_hx4X5-RLfavdM-OF5lOTJh0R2lnfXT3X2HO93fvKfR6t" \
                       "Wh7hy45bHp3jW6bke6oLDHAftT-qf57EsJnH-bnEebjYq4bohjP43tjeBtQmJJrfL-Db24_Mjh6yQ55GDU" \
                       "LXQf6y0UbaQg-q3lTw5KoZEnQobjJYhU33W-JW0x-jLgLeWUjMyl-VSbvoW4nJyUnQbtnnBPn9LnLDoCDy" \
                       "JK-bMCvR2CTsbJtJMfOKaC62aKDs2qoa-hcqEIL45nJaDPFXjM73WhIHLR74Qq5_ahbnHxbSj4QzWtbXWt" \
                       "bhB-LfBCOR_UnT2h5nhMJ_DPvGKhFvqJOWBhTy523ion5vQpnO8UtuDjLae5b3jNDsbbIX2ITeBnTeKRI_" \
                       "Hn7zeUFK0btpbt-qJJbf-R70QDbS2POGhxDRQJ5pM44vQU5nBT5KWG5MofTn5qvqMp6vQ5OiQPPkQN3TBj" \
                       "JQL6RkKT6m2hvADn3oyT3qXp0nMPnTqtJHKbDH_KtytUK; shifen[28507946690_84614]=1447038629; " \
                       "BCLID=12112589048866824416; BD_HOME=1; BD_UPN=123253; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; " \
                       "BD_CK_SAM=1; " \
                       "H_PS_PSSID=17519_17746_1453_17620_17901_12826_17783_17501_17001_17073_15594_12165_10634; " \
                       "__bsi=3137023652248049585_00_0_I_R_121_0303_C02F_N_I_I_0; " \
                       "H_PS_645EC=83d1tHnpHoljaSTbDy3JEisl4VLsrf20H2NFYdPuYWHMzgAzl%2F2zdb%2BwdIAa6C4CDkaX; " \
                       "WWW_ST=1447047984362"
        self.queue = queue

    def fetch_urls(self):
        _headers = {"User-Agent": self._ua[random.randint(0, 1)],
                    "Accept-Language": self._accept_language,
                    "Cookie": self._cookie
                    }
        print("Query [%s]" % self._url)
        resp = requests.get(self._url, headers=_headers)
        promotes = []
        if resp.status_code == 200:
            page = resp.text
        if page:
            ids = ["#3001", "#3002", "#3003", "#4001", "#4002", "#4003", "#5001", "#5002", "#5003"]
            for promote_div in [PyQuery(PyQuery(page)("div").html())("%s" % tag_id).html() for tag_id in ids]:
                if promote_div:
                    promote_url = PyQuery(PyQuery(promote_div).find("a")).eq(0).attr("href")
                    promote_title = PyQuery(PyQuery(promote_div).find("a")).eq(0).text()
                    promote_domain = PyQuery(PyQuery(promote_div).find("span")).eq(0).text()
                    promotes.append([promote_url, promote_domain, promote_title])
        print("[%d] promotes found" % len(promotes))
        return promotes

    def put_into_queue(self):
        promotes = self.fetch_urls()
        for promote in promotes:
            if self.queue.full():
                print("Queue is full, waiting...")
                time.sleep(20)
            if promote:
                print("Put into Queue [%s]" % self._keyword)
                self.queue.put({"promote_url": promote[0],
                                "promote_domain": promote[1],
                                "promote_title": promote[2]})

    def run(self):
        while True:
            if self.queue.qsize() >= 150:
                print("Queue size [%d], waiting..." % self.queue.qsize())
                time.sleep(20)
            # print("Put promotes into Queue...")
            self.put_into_queue()
            time.sleep(random.randint(5, 20))


class SmartMouse(Thread):
    def __init__(self, queue):
        super(SmartMouse, self).__init__()
        self._chrome_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) " + \
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
        self._firefox_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0"
        self._ua = [self._chrome_ua, self._firefox_ua]
        self._accept_language = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
        # self.proxy = {"http": "http://user:pass@1.2.3.4:5678"}
        self.headers = {"User-Agent": self._ua[random.randint(0, 1)],
                        "Accept-Language": self._accept_language
                        }
        self.retry = 10
        self.queue = queue
        self.promote_domain = ["www.qianmama.com", "jimubox.com", "www.jinlianchu.com"]

    def click(self, promote):
        seconds = random.randint(1, 10)
        # click = requests.get(url=promote["promote_url"], headers=headers, proxies=proxy)
        if promote["promote_domain"] not in self.promote_domain:
            return False
        print "推广: ", promote["promote_domain"], promote["promote_title"]
        print("等待点击(%ss)..." % seconds)
        print("Queue size [%d]" % self.queue.qsize())
        time.sleep(seconds)
        try:
            do_click = requests.get(url=promote["promote_url"], headers=self.headers)
            print "点击: ", do_click.status_code, PyQuery(do_click.text).find("title").text(), do_click.url
        except Exception as e:
            print e.message

    def run(self):
        # while not self.queue.empty():
        try_num = 0
        while True:
            print("Read Queue")
            if self.queue.empty():
                print("Queue Empty, waiting...")
                try_num += 1
                if try_num >= self.retry:
                    print("Tried %d times. Abort..." % try_num)
                    break
                time.sleep(5)
                continue
            # reset try num
            try_num = 0
            promote = self.queue.get()
            self.click(promote)

if __name__ == '__main__':
    q = Queue(200)
    # proxy = {"http": "http://user:pass@1.2.3.4:5678"}
    ss = SimpleSpider("麻袋理财", q)
    sss = SimpleSpider("麻袋理财官网", q)
    sm = SmartMouse(q)
    ss.start()
    sss.start()
    sm.start()
    ss.join()
    sss.join()
    sm.join()
