#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Chufuyuan
# Mail: chufuyuan01@chinatopcredit.com
# Date: 15/11/6

import random
from multiprocessing import Process, Queue
import requests
from pyquery import PyQuery


class SimpleSpider(Process):
    def __init__(self, keyword):
        super(SimpleSpider, self).__init__()
        self._keyword = keyword
        self._chrome_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) " + \
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
        self._firefox_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0"
        self._safari_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) " \
                          "Version/9.0 Safari/601.1.56"
        self._ua = [self._chrome_ua, self._firefox_ua, self._safari_ua]
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
        self._headers = {"User-Agent": self._ua[random.randint(0, 2)],
                         "Accept-Language": self._accept_language,
                         "Cookie": self._cookie
                         }
        self.promotes = []
        self.fetch_urls()

    @property
    def page(self):
        resp = requests.get(self._url, headers=self._headers)
        # resp = requests.Session().get(self._url, headers=self._headers)
        for i in resp.cookies.values():
            print i
        if resp.status_code == 200:
            return resp.text
        return None

    def fetch_urls(self):
        # with open("/Users/Eason/Desktop/index.html", "w") as f:
        #     f.write(self.page.encode(encoding="utf8", errors="ignore"))
        if self.page:
            ids = ["#3001", "#3002", "#3003", "#4001", "#4002", "#4003", "#5001", "#5002", "#5003"]
            for promote_div in [PyQuery(PyQuery(self.page)("div").html())("%s" % tag_id).html() for tag_id in ids]:
                if promote_div:
                    promote_url = PyQuery(PyQuery(promote_div).find("a")).eq(0).attr("href")
                    promote_title = PyQuery(PyQuery(promote_div).find("a")).eq(0).text()
                    promote_domain = PyQuery(PyQuery(promote_div).find("span")).eq(0).text()
                    self.promotes.append({"promote_url": promote_url,
                                          "promote_title": promote_title,
                                          "promote_domain": promote_domain})
            # if not self.promotes:
            #     print "No Promote Div found!"


class SmartMouse(Process):
    def __init__(self, promote):
        super(SmartMouse, self).__init__()
        self.chrome_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) " + \
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
        self.firefox_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0"
        self.safari_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) " \
                         "Version/9.0 Safari/601.1.56"
        self.ua = [self.chrome_ua, self.firefox_ua, self.safari_ua]
        self.accept_language = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
        # self.proxy = {"http": "http://user:pass@1.2.3.4:5678"}
        self.headers = {"User-Agent": self.ua[random.randint(0, 2)],
                        "Accept-Language": self.accept_language
                        }
        self.promote = promote

    def run(self):
        try:
            # click = requests.get(url=promote["promote_url"], headers=headers, proxies=proxy)
            print "推广: ", self.promote["promote_domain"], self.promote["promote_title"]
            do_click = requests.get(url=self.promote["promote_url"], headers=self.headers)
            print "点击: ", do_click.status_code, PyQuery(do_click.text).find("title").text(), do_click.url
        except Exception as e:
            print e.message

if __name__ == '__main__':
    q = Queue(20)
    proxy = {"http": "http://user:pass@1.2.3.4:5678"}
    ss = SimpleSpider("麻袋理财")
    # ss = SimpleSpider("中腾信")
    for promote in ss.promotes:
        sm = SmartMouse(promote)
        sm.run()
