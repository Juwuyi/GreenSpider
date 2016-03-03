# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 18:28:10 2016

@author: Ju.51
"""
from modules import Configer,Spider,SQLer
 

if __name__ == '__main__':
    
    print '打开数据库链接'    
    try:
        sqler = SQLer.SQLer(Configer.host,
                            Configer.usnm,
                            Configer.pswd,
                            Configer.dbnm)
    except Exception as ex:
        print '链接数据库失败'
        print ex.message
    
    
    print '读取配置初始化爬虫' 
    spiders = []
    for target_website in Configer.target_sites:
        try:
            website = target_website.replace('.','_')
            website_latest_link,website_latest_date = sqler.get_latest(target_website)
            spider = Spider.Spider(website,
                                   website_latest)
            spiders.append(spider)
        except Exception as ex:
            print 'Warning: Spider Initialization Failed at',target_website
            print ex.message

        
    
    