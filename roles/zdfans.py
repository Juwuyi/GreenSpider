# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:46:24 2016

@author: 4473
"""

import requests
import bs4
import sys
sys.path.append('..')
import ConfigRPG

# ******************************************常量

latest_url = 'http://www.zdfans.com/page/1'     
allowed_domain = 'www.zdfans.com'
time_out = 3
            

# ******************************************函数


def page_parser(html):
    soup = bs4.BeautifulSoup(html)
    try:
        next_page_link = soup.find(lambda node: u'下一页' == node.string)['href']
    except Exception as ex:
        print 'warning at',allowed_domain,'finished or aborted'
        print ex.message
        next_page_link = None
    metas = soup.find(name='ul',class_='excerpt')
    infos = []
    for li in metas.children:
        info = ConfigRPG.article_Tplt.copy()
        info['article_link'] = li.a['href']
        info['article_title'] = li.h2.a.string
        info['content'] = li.find(name='div',class_='note').string
        info['pic_link'] = li.a.img['src']
        info['website'] = allowed_domain
        infos.append(info)
    return next_page_link,infos



if "__main__" == __name__:
    html = requests.get("http://www.zdfans.com/page/33").text
    next_page_link,infos = page_parser(html)
    #nextPage,metas = find_linker_from_html(html)
    
    
    
    