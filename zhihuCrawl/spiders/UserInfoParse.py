#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created by David Teng on 18-2-6

"""
这个文件暂时用作测试文件
"""

class userInfoParse():


    def __init__(self, response=None):
        self.response = response
        pass


    def saveLoginSucBody(self):
        pass


    pass

if __name__ == '__main__':

    # with open("follower_Doc.txt", "r")as rd:
    #     res = rd.read()
    # import scrapy
    # sel = scrapy.Selector(text=res)
    # relations_url = sel.xpath("//div[@class='List-item']//div[@class='ContentItem-image']//a/@href").extract()
    # print relations_url

    cookies = {
        "_xsrf": "fe7f3538-cef0-4d95-bd09-e99af2fa8452",
        "_zap": "cb60cde1-ceb0-48b3-a1aa-00607d84e315",
        "aliyungf_tc": "AQAAAKTvhj3Y7goAQnRBMQOee1gx7S9V",
        # "capsion_ticket": "2|1:0|10:1517995128|14:capsion_ticket|44:MzE4MDA1M2NhY2NiNDNhMDg1YTI0NGVmNDBkZGQzNDI=|b97fd02eeb1be3762f694a69d6684f194c6fd0e5699ae006ee9e6e9a95a25cbc",
        "d_c0": "AICrab_1Gw2PTli-ADwIYW3qRNXmaMBTPTw=|1517994660",
        "q_c1": "a54c02afce4f4d73baa5cbdcf517a460|1517994660000|1517994660000",
    }
    headers = {

        # "Accept": "application/json, text/plain, */*:",
        # "Accept-Encoding": "gzip, deflate",
        # "Accept-Language": 	"en-US,en;q=0.5",
        "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
        # "Cache-Control": "no-cache",
        # "Connection": "keep-alive",
        # "Cookie": cookies,
        # "Host":	"www.zhihu.com",
        # "origin": "https://www.zhihu.com",
        # "Pragma": "no-cache",
        # "Referer": "https://www.zhihu.com/people/tombkeeper/followers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
        # "x-udid":	"AABse1vgHA2PTkZLcMgyYsF675NWcXGJAgI=",
    }

    params = {
        "include": "data[*].answer_count, articles_count, gender, follower_count, is_followed, is_following, badge[?(type = best_answerer)].topics",
        "limit": 20,
        "offset": 0
    }

    # url = "https://www.zhihu.com/people/tombkeeper/followers"
    # url = """https://www.zhihu.com/api/v4/members/tombkeeper/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=100"""
    # url = """https://www.zhihu.com/api/v4/members/tombkeeper/followers?include=data%5B%2A%5D.answer_count%2C+articles_count%2C+gender%2C+follower_count%2C+is_followed%2C+is_following%2C+badge%5B%3F%28type+%3D+best_answerer%29%5D.topics&limit=20&offset=0"""
    url = """http://www.zhihu.com/api/v4/members/tombkeeper/following?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&offset=0"""
    import requests
    res = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
    print res.headers
    with open('tmp.html', 'w')as wr:
        wr.write(res.content)

    pass
