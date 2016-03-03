# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:48:29 2016

@author: Juwuyi
"""

import os,sys
import ConfigRPG
import SQLer
import requests
import time


class Spider():
    def __init__(self,website_name):
        try:
            roles_dir = os.path.abspath('./roles/')
            if roles_dir not in sys.path:
                sys.path.append(roles_dir)
            website_role = __import__(website_name)  
        except Exception as ex:
            print '*'*50
            print ex.message
            print '*'*50
        
        # 关于爬虫爬取目标网站的配置
        self.latest_url = website_role.latest_url
        self.time_out = website_role.time_out
        self.allowed_domain = website_role.allowed_domain
        self.page_parser = website_role.page_parser
        
        # 存储数据
        
        
        # 数据库链接信息
        self.sql_host = ConfigRPG.sql_host
        self.sql_user = ConfigRPG.sql_user
        self.sql_pass = ConfigRPG.sql_pass
        self.sql_dbnm = ConfigRPG.sql_dbnm
        self.SQLer = SQLer.SQLer(self.sql_host,
                                 self.sql_user,
                                 self.sql_pass,
                                 self.sql_dbnm)
        
    def get_latest_article_link(self):
        # 这里有个小BUF 比如第一次读取1-27页面  会吧27页面的infos当作最新
        #直到新的文章更新，不影响
        print self.allowed_domain
        article_link = self.SQLer.get_latest_link(self.allowed_domain)
        return article_link
        
    def go_crawling(self):
        latest_article_link = self.get_latest_article_link()
        next_page_link = self.latest_url
        while next_page_link:
            time.sleep(1)
            try:
                r = requests.get(next_page_link,timeout=self.time_out)
            except Exception as ex:
                print ex
                next_page_link = None
                break
                
            if r.ok:
                print 'parsing:',next_page_link,
                next_page_link,infos = self.page_parser(r.text)
                print 'successfully'
            else:
                print 'something wrong during parsing'
                raise Exception
            if latest_article_link in [info['article_link'] for info in infos]:
                print 'meet old friend %s then stop before %s' % (latest_article_link,next_page_link)
                next_page_link = None
            try:
                self.SQLer.insert(infos)
            except:
                print 'sth wrong when insert to database',next_page_link
        return






if '__main__' == __name__:
    running = True
    spiders = [Spider(name) for name in ['zdfans']]
    while running:
        for spider in spiders:
            spider.go_crawling()
            print 'a spider fall asleep'
        time.sleep(10)

    