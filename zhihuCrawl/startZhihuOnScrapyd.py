#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created by David Teng on 18-2-10
import requests
import pprint
class ZhihuSpiderControlerOnScrapyd():
    """
        爬虫在scrapyd部署的命令:
            scrapyd-deploy <target> -p <project> --version <version>
        示例（本程序的部署命令）：
        scrapyd-deploy 100 -p zhihu --version ver20180210
    """
    def getScrapydStatus(self):
        """
        获取scrapyd状态
        :return:
        """
        statusUrl = "http://127.0.0.1:6800/daemonstatus.json"
        res = requests.get(statusUrl)
        pprint.pprint(res.content)
        pass

    def getProjectsList(self):
        """
        获取项目列表
        :return:
        """
        getProjectsList = "http://127.0.0.1:6800/listprojects.json"
        res = requests.get(url=getProjectsList)
        pprint.pprint(res.content)

        pass

    def getSpiderLists(self, projName="zhihu"):
        """
        获取爬虫列表
        :param projName:
        :return:
        """
        getSpidersList = "http://127.0.0.1:6800/listspiders.json?project=%s" % projName
        res = requests.get(url=getSpidersList)
        pprint.pprint(res.content)

    def getSpidersVersionList(self, projName):
        """
        获取爬虫版本列表
        :param projName:
        :return:
        """
        url = "http://127.0.0.1:6800/listversions.json?project=%s" % projName
        res = requests.get(url=url)
        pprint.pprint(res.content)

    def getRunningSpiderStatus(self, projName="zhihu"):
        """
        获取运行中的爬虫状态
        :return:
        """
        url = "http://127.0.0.1:6800/listjobs.json?project=%s" % projName
        res = requests.get(url=url)
        pprint.pprint(res.content)

        pass

    def startSpider(self, projName="zhihu", spiderName="zhihu.com"):
        """
        启动爬虫
        :return:
        """
        startUrl = "http://127.0.0.1:6800/schedule.json"
        start_param = {
            "project": projName,
            "spider": spiderName,
        }
        res = requests.post(url=startUrl, data=start_param)
        pprint.pprint(res.content)
    pass

    def deleteSpider(self, projName, version):
        """
        删除某一版本爬虫
        :param projName:
        :return:
        """
        del_url = "http://127.0.0.1:6800/delversion.json"
        del_param = {
            "project": projName,
            "version": version,
        }
        res = requests.post(url=del_url, data=del_param)
        pprint.pprint(res.text)

    def deleteProj(self, projName):
        """
        删除某一工程，并将工程下各版本爬虫一起删除
        :return:
        """
        del_proj_url = "http://127.0.0.1:6800/delproject.json"
        del_proj_param = {
            "project": projName,
        }
        res = requests.post(url=del_proj_url, data=del_proj_param)
        pprint.pprint(res.content)

    def addProjVer(self, projName, version, projEgg=None):
        """
        给工程添加版本，如果工程不存在则创建, 类似于向github上传一个新项目或者已有项目的新版本
        :return:
        """
        add_proj_url = "http://127.0.0.1:6800/addversion.json"
        add_proj_param = {
            "project": projName,
            "version": version,
            'egg': projEgg              # 将新项目（版本）的源码打包成egg文件
        }
        res = requests.post(url=add_proj_url, data=add_proj_param)
        pprint.pprint(res.content)
        pass

    def cancelSpiderJob(self, projName, jobId):
        """
        取消一个运行的爬虫任务
        :return:
        """
        cancel_url = "http://127.0.0.1:6800/cancel.json"
        cancel_param = {
            "project": projName,
            "job": jobId
        }
        res = requests.post(url=cancel_url, data=cancel_param)
        pprint.pprint(res.content)
        pass

if __name__ == '__main__':
    tmpobj = ZhihuSpiderControlerOnScrapyd()
    # tmpobj.startSpider()
    # tmpobj.getRunningSpiderStatus("zhihu")
    # tmpobj.getProjectsList()
    # tmpobj.getScrapydStatus()
    # tmpobj.getSpiderLists("zhihu")
    # tmpobj.getSpidersVersionList("zhihu")
    # tmpobj.addProjVer("zhihu", "ver20180211")
    # tmpobj.cancelSpiderJob("zhihu", "2a4e84760e2b11e89a527c67a2537807")
    # tmpobj.deleteSpider(projName="zhihu", version="ver20180210")
    # tmpobj.deleteProj("zhihu")
    pass

