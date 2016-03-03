# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:48:29 2016

@author: Juwuyi
"""

import os,sys
import requests
import time


class Spider():
    def __init__(self,website_name,website_latest):
        #爬虫初始化
        try:
            roles_dir = os.path.abspath('./roles/')
            if roles_dir not in sys.path:
                sys.path.append(roles_dir)
            website_Configer = __import__(website_name)  
        except Exception as ex:
            print ex.message
        # 关于起始页面和html解析函数
        self.latest_url = website_Configer.latest_url
        self.page_parser = website_Configer.page_parser
        self.latest = website_latest
        self.ret_list = []
        
        
    
        
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

    