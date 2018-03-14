#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created by David Teng on 18-2-5
import time
import hashlib
import hmac
import re
import urllib
from urlparse import urljoin
import json

class loginUtils():
    """
        class:`loginUtils`, 为登录知乎提供一系列工具
        登录的流程：
        1. 请求验证码,从response.headers的Set-Cookie中提取 capsion_ticket
        2.
    """
    captchaUrl = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'       # 请求验证码的url
    loginUrl = "https://www.zhihu.com/api/v3/oauth/sign_in"                 # 登录请求的url
    # 用于发送验证码的请求的headers
    capsion_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
        "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",   # 这里的"authorization"是由'oauth' + client_id,  client_id是固定值
    }

    # 登录请求的cookie
    login_cookie = {

        "cap_id": "ZDAzNTJmMDFlNjk5NGRmMThhYWJiOWYyYjhhZTIyZjI=|1517790355|ecb9ce99f8f47f4f46b78440e5e9499a052203aa",
        "l_cap_id": "Y2Y5MmVmNGZmZDY1NDE5YjhhZjVkNjE0M2YyMWFlZTM=|1517790355|859dcf21317de1f9d30e524260ff0c1fe0ae918f",
        "r_cap_id": "MGY4Mjc3NjQxN2RlNDI0ZGFjMDFhODMxMTFjNDkxYTU=|1517790355|548b0d468316f5e61b95a5163487b897f6f43fc7",
        "_xsrf": "d265e4f5-f950-47cf-859b-e1cf0ba5ea95",
        "_zap": "5783a796-6691-4c2f-98b0-025da35a90c1",
        "aliyungf_tc": "AQAAANDJfAzlEQkAhi2IdVnsB0cKFeA4",
        "capsion_ticket": '',  # 需要填， getCaptchaTicket
        "d_c0": "AIAst7kYGA2PTuxnz9pvsR2yyIaYXasKUj8=|1517735393",
        "q_c1": "c17fd5b83a584d15802419cf1b49d3f9|1517735393000|1517735393000"
    }

    # 发送登录请求的data
    LOGIN_DATA = {
        'source': 'com.zhihu.web',
        'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
        'signature': '',  # 需要填， getSignature
        'timestamp': '',  # 需要填， getSignature调用getTImestamp
        'username': '你的账户名',
        'password': '你的密码',
        'captcha': '',
        'lang': 'en',
        'ref_source': 'homepage',
        'utm_source': '',
        'grant_type': 'password',
    }

    def getCaptchaTicket(self, response):
        """
            从response.headers的Set-Cookie中提取 capsion_ticket
            :param response:
            :return:
        """
        capsion_ticket_Cookie = response.headers.getlist('Set-Cookie')
        # print capsion_ticket_Cookie
        if capsion_ticket_Cookie:
            tmpStr = capsion_ticket_Cookie[1]
            matchObj = re.match(r'capsion_ticket="(.+?)"', tmpStr, re.M | re.I)
            capsion_ticket = matchObj.group(1)
            print "已获取 capsion_ticket..."
            return capsion_ticket
        else:
            print "没有获取到capsion_ticket!"
            return False
        pass

    def getTImestamp(self ):
        """
            返回当前时间的时间戳，精确到毫秒
            :return:
        """
        return str(int(round(time.time() * 1000)))

    def getSignature(self, data, secret="d1b964811afb40118a12068ff74a12f4"):

        """
            为登录请求附加签名。（该函数从根据js文件中对应函数改写的）
            :param dict data: POST 数据
            :param str|unicode secret: APP SECRET（从js函数中提取到的）
            :return: 经过签名后的 dict， 增加了 timestamp 和 signature 两项
        """
        data['timestamp'] = self.getTImestamp()

        params = ''.join([
            data['grant_type'],
            data['client_id'],
            data['source'],
            data['timestamp'],
        ])

        data['signature'] = hmac.new(
            secret.encode('utf-8'),
            params.encode('utf-8'),
            hashlib.sha1
        ).hexdigest()
        pass


class parsefollowing_follower_Data():
    """
        `parsefollowing_follower_Data1`:提供解析用户的关注和被关注的对象的工具方法
        followers与followeers的数据直接调用API获得，返回数据（response）的格式为：
         {'paging':{...}, 'data':{...}}
         其中，
         'paging'的格式:
         {
            is_end	# 当前请求的页面是否是最后一页
            totals	#　一共有多少用户（followers或followees）数据
            previous	# 当前请求页面的前一页的url
            is_start	# 当前请求的页面是否是第一页
            next　# 当前请求页面的下一页的url
         }
         'data'的格式:
         {
            is_followed	false
            avatar_url_template	https://pic3.zhimg.com/v2-1bea18837914ab5a40537d515ed3219c_{size}.jpg
            user_type	people
            answer_count	18229
            badge	[]
            is_following	false
            url	http://www.zhihu.com/api/v4/people/0970f947b898ecc0ec035f9126dd4e08
            url_token	excited-vczh
            id	0970f947b898ecc0ec035f9126dd4e08
            articles_count	91
            name	vczh
            headline	专业造轮子，拉黑抢前排。<a href="https://link.zhihu.com/?target=http%3A//gaclib.net" class=" external" target="_blank" rel="nofollow noreferrer"><span class="invisible">http://</span><span class="visible">gaclib.net</span><span class="invisible"></span></a>
            gender	1
            is_advertiser	false
            avatar_url	https://pic3.zhimg.com/v2-1bea18837914ab5a40537d515ed3219c_is.jpg
            is_org	false
            follower_count	665046
            type	people
         }
    """
    def __init__(self, response=None):
        self.res = response
        self.data = {}
        self.peopleData = []
        pass

    def getNewResponse(self, newResponse):
        """
            更新函数处理的response对象
            :param newResponse:
            :return:
        """
        self.res = newResponse
        self.__getData()
        self.__get_follwing_er_data()

    def __getData(self):
        """
            提取返回数据中所有用户的的数据（data字段）
            :return:
        """
        self.data = json.loads(self.res.text)
        pass

    def isEnd(self):
        """
            判断当前页是否是最后一页
            :return:
        """
        return False if self.data['paging']['is_end'] == 'false' else True
        pass

    def getNextpageUrl(self):
        if self.isEnd() == 'false':
            return self.data['paging']['next']

    def __get_follwing_er_data(self):
        """
        关注_被关注者数据结构：
                is_followed	            false
                avatar_url_template	    https://pic3.zhimg.com/v2-1bea18837914ab5a40537d515ed3219c_{size}.jpg
                user_type	            people
                answer_count	        18206
                is_following	        false
                headline	            专业造轮子，拉黑抢前排。<a href="https://link.zhihu.com/?target=http%3A//gaclib.net" class=" external" target="_blank" rel="nofollow noreferrer"><span class="invisible">http://</span><span class="visible">gaclib.net</span><span class="invisible"></span><i class="icon-external"></i></a>
                url_token	            excited-vczh
                id	                    0970f947b898ecc0ec035f9126dd4e08
                articles_count	        90
                type	                people
                name	                vczh
                url	                    http://www.zhihu.com/api/v4/people/0970f947b898ecc0ec035f9126dd4e08
                gender	                1
                is_advertiser	        false
                avatar_url	            https://pic3.zhimg.com/v2-1bea18837914ab5a40537d515ed3219c_is.jpg
                is_org	                false
                follower_count	        664521
                badge	                []
        :return:
        """
        self.peopleData = self.data['data']
        return self.peopleData


    def get_relations_id(self):
        """
            返回装有所有用户的url_token的列表
        """
        return [item['url_token'] for item in self.peopleData]
        pass

    def get_relations_url(self):
        """
            返回装有所有用户的主页url的列表
            :return:
        """
        basicUrl = "https://www.zhihu.com/people/"
        return [urljoin(basicUrl, item['url_token']) for item in self.peopleData]
        pass
    pass


class userInfoParse(parsefollowing_follower_Data):
    """
        用户信息解析工具函数

    """
    following_follower_headers = {

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

    # __offset = 0

    following_follower_params = {
        "include": "data[*].answer_count, articles_count, gender, follower_count, is_followed, is_following, badge[?(type = best_answerer)].topics",
        "limit": 20,
        "offset": 0
    }
    def __init__(self, response=None):
        parsefollowing_follower_Data.__init__(self, response=response)
        self.basicUrl_following_er = "https://www.zhihu.com/api/v4/members/"
        pass


    # def fresh_basicUrl_following_er(self, user_id):
    #     # self.basicUrl_following_er = urljoin(self.baseUrl, user_id)
    #     pass
    #
    # def offset_plus_one(self, limit=20):
    #     "limit的值后台已经写死为20， 请求中更改无效"
    #     # self.following_follower_params['limit'] = limit
    #     self.__offset += 1
    #     self.following_follower_params['offset'] = self.__offset
    #     pass

    # def clear_offset(self):
    #     self.__offset = 0
    #     self.following_follower_params['offset'] = self.__offset
    #     pass

    def makeUrl(self, user_id, relation_type):
        """
        按照API要求组装获取指定用户的（被）关注者数据的url（当然是抓包研究得出的啦（∩＿∩））
        :param user_id: 　用户id
        :param relation_type: 关系类型（followers　或者　followees）
        :return: 返回对应的
        """
        tmpurl = urljoin(self.basicUrl_following_er, user_id)
        return urljoin(tmpurl+'/', relation_type) + "?" + urllib.urlencode(self.following_follower_params)
        # return urljoin(self.baseurl, urllib.urlencode(self.params))
        pass


    pass

if __name__ == '__main__':
    uip = userInfoParse("https://www.zhihu.com/api/v4/members/")
    print uip.makeUrl("tombkeeper", "following")

    pass
