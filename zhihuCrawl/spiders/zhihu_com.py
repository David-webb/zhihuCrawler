# -*- coding: utf-8 -*-
import json
import os
import re

from urllib import urlencode

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from zhihuCrawl.items import UserInfoItem, RelationItem
from scrapy.http import Request, FormRequest
from zhihuCrawl.zhihu_utils import loginUtils
from zhihuCrawl.zhihu_utils import userInfoParse

class ZhihuComSpider(CrawlSpider):
    name = 'zhihu.com'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/people/tombkeeper']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    def __init__(self, *args, **kwargs):
        super(ZhihuComSpider, self).__init__(*args, **kwargs)
        # self.xsrf = ''
        self.cookies = ''
        self.loginUtils = loginUtils()
        self.usrParsetool = userInfoParse()

# if os.path.exists('session.txt'):
#         with open('session.txt','rb') as f:
#             import pickle
#             self.cookies = pickle.load(f)
#             self.xsrf = self.cookies['_xsrf']
#             return [Request(
#             self.start_urls[0],
#             cookies=self.cookies,
#             meta={'cookiejar': 1},
#             callback=self.parse_user_info,
#             errback=self.parse_err,
#         )]

    def start_requests(self):
        """
        重写CrawlSpider的start_requests函数，发送验证码请求（为了获取capsion_ticket）
        :return:
        """
        #首先请求验证码（为了获取captcha_ticket, 登录要用）
        return [Request(self.loginUtils.captchaUrl,
                        headers=self.loginUtils.capsion_headers, callback=self.start_login)
                ]

    def start_login(self, response):
        """
        处理验证码请求返回的数据，并提取
        :param response:
        :return:
        """
        # 解析response的Cookie， 提取capsion_ticket
        capsion_ticket = self.loginUtils.getCaptchaTicket(response)

        # 开始登录
        if capsion_ticket:
            self.loginUtils.login_cookie['capsion_ticket'] = capsion_ticket     # 将获得的capsion_ticket放到登录请求的cookies中
            self.loginUtils.getSignature(self.loginUtils.LOGIN_DATA)            # 根据已知LOGIN_DATA字段计算Signature并添加到LOGIN_DATA中
            return [FormRequest(
                url=self.loginUtils.loginUrl,
                method='POST',
                cookies=self.loginUtils.login_cookie,
                meta={'cookiejar': 1},
                formdata=self.loginUtils.LOGIN_DATA,
                callback=self.after_login
            )]


    def saveCookies_accessToken(self, response):
        """
        保存登录后的cookies、以及成功登录后返回的access_token（参考oauth2协议：
                    http://www.barretlee.com/blog/2016/01/10/oauth2-introduce/）等信息
        :param response:
        :return:
        """
        if not os.path.exists('session.txt'):
            with open('session.txt', 'wb') as f:
                import pickle
                cookies = response.request.headers['cookie']
                cookieDict = {}
                for cookie in cookies.split(';'):
                    key, value = cookie[0:cookie.find('=')], cookie[cookie.find('=') + 1:]
                    cookieDict[key] = value
                pickle.dump(cookieDict, f)
        if not os.path.exists('access_token.txt'):
            with open('access_token.txt', 'wb') as f:
                import pickle
                cookies = response.body
                cookieDict = {}
                for cookie in cookies.split(';'):
                    key, value = cookie[0:cookie.find('=')], cookie[cookie.find('=') + 1:]
                    cookieDict[key] = value
                pickle.dump(cookieDict, f)


    def after_login(self, response):
        """
        判断登录是否成功，成功就保存cookie等信息并开始请求初始解析页面，失败就报错退出
        :param response:
        :return:
        """

        if "access_token" in response.body:
            print response.body
            tmpbody = json.loads(response.body)
            self.logger.info("登录成功！")
            self.saveCookies_accessToken(response)
            return [Request(
                self.start_urls[0],
                meta={'cookiejar': response.meta['cookiejar'],
                      'user_id': tmpbody['user_id'],
                      },
                callback=self.parse_user_info,
                errback=self.parse_err,)]

        else:
            self.logger.error('登录失败！')
            return


# if not os.path.exists('session.txt'):
#     with open('session.txt','wb') as f:
#         import pickle
#         cookies = response.request.headers['cookie']
#         cookieDict={}
#         for cookie in cookies.split(';'):
#             key,value = cookie[0:cookie.find('=')], cookie[cookie.find('=')+1:]
#             cookieDict[key]=value
#         pickle.dump(cookieDict,f)

    def parse_user_info(self, response):
        '''
        解析用户信息
        :param response:
        :return:
        '''


        user_id = os.path.split(response.url)[-1]
        # user_id = response.meta['user_id']
        user_image_url = response.xpath("//img[@class='Avatar Avatar--large UserAvatar-inner']/@src").extract_first()
        # name = response.xpath("//*[@class='ProfileHeader-title']/span[@class='ProfileHeader-name']/text() | //*[@class='title-section']/a/text()").extract_first()
        name = response.xpath("//*[@class='ProfileHeader-title']/span[@class='ProfileHeader-name']/text()").extract_first()
        location = response.xpath("//*[@class='location item']/@title").extract_first()
        business = response.xpath("//*[@class='business item']/@title").extract_first()
        gender = response.xpath("//svg[@class='Icon Icon--male']/@class | //svg[@class='Icon Icon--female']/@class").extract_first()
        if gender and u"female" in gender:
            gender = u"female"
        else:
            gender = u"male"
        employment = response.xpath("//*[@class='employment item']/@title").extract_first()
        position = response.xpath("//*[@class='position item']/@title").extract_first()
        education = response.xpath("//*[@class='education item']/@title").extract_first()
        # //div[@class='Profile-followStatusValue']
        try:
            following_num, followers_num = tuple(response.xpath("//div[@class='NumberBoard FollowshipCard-counts NumberBoard--divider']/a[@class='Button NumberBoard-item Button--plain']/div/strong/text()").extract())
            relations_url = response.xpath("//a[@class='Button NumberBoard-item Button--plain']/@href").extract()
        except Exception,e:  # 这里目前还不知道会出现什么异常
            following_num, followers_num = tuple(response.xpath("//div[@class='Profile-followStatusValue']/text()").extract())
            relations_url =response.xpath("//a[@class='Profile-followStatus']/@href").extract()
        followers_num = followers_num.replace(',', '')
        following_num = following_num.replace(',', '')
        # print following_num, followers_num
        user_info_item = UserInfoItem(user_id=user_id, user_image_url=user_image_url,
                                      name=name, location=location, business=business,
                                      gender=gender, employment=employment, position=position,
                                      education=education, followees_num=int(following_num),
                                      followers_num=int(followers_num))
        # self.logger.info(user_info_item)
        yield user_info_item
       # 关注我和我关注的人的列表的链接

        for url in relations_url:
            if u"following" in url:
                relation_type = u"followees"
            else:
                relation_type = u"followers"

            # self.usrParsetool.clear_offset()  # offset 清0
            # print self.usrParsetool.makeUrl(user_id, relation_type)
            yield Request(url=self.usrParsetool.makeUrl(user_id, relation_type),
                          headers=self.usrParsetool.following_follower_headers,
                          meta={
                              'user_id': user_id,
                              'relation_type': relation_type,
                              'cookiejar': response.meta['cookiejar'],
                              'dont_merge_cookies': True,

                            },
                          errback=self.parse_err,
                          callback=self.parse_relation
                          )


    def parse_relation(self, response):
        '''
        解析和我有关系的人,这个只处理前20
        :param response:
        :return:
        '''
        user_id = response.meta['user_id']
        relation_type = response.meta['relation_type']
        self.usrParsetool.getNewResponse(response)  # 更新解析工具的response


        relations_url = self.usrParsetool.get_relations_url()
        relations_id = self.usrParsetool.get_relations_id()

        yield RelationItem(
                           user_id=user_id,
                           relation_type=relation_type,
                           relations_id=relations_id
                           )

        # 如果还没有解析到最后一页
        if not self.usrParsetool.isEnd():
            # self.usrParsetool.offset_plus_one()
            yield Request(
                url=self.usrParsetool.getNextpageUrl(),
                headers=self.usrParsetool.following_follower_headers,
                meta={
                    'user_id': user_id,
                    'relation_type': relation_type,
                    'cookiejar': response.meta['cookiejar'],
                    'dont_merge_cookies': True,
                    # 'peopleNum': peopleNum
                },
                errback=self.parse_err,
                callback=self.parse_relation
            )
            pass

        # except Exception,e:
        #     self.logger.warning('no second post--'+str(data_init)+'--'+str(e))


        for url in relations_url:
            yield Request(url=url,
                          meta={'cookiejar': response.meta['cookiejar']},
                          callback=self.parse_user_info,
                          errback=self.parse_err)


    def parse_err(self,response):
        """
        报错函数
        :param response:
        :return:
        """
        self.logger.error('crawl %s fail' % response.request.url)




from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('zhihu.com')
    process.start()
    pass
