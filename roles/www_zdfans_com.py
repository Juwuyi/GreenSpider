# -*- coding: utf-8 -*-

"""
@author: Ju.51
"""

import requests
import bs4
import sys
import os

if os.path.abspath('../modules') not in sys.path:
    sys.path.append(os.path.abspath('../modules'))
Const = __import__('Const')

# ******************************************常量
latest_url = 'http://www.zdfans.com/page/1'     


# ******************************************函数
def page_parser(html):
    soup = bs4.BeautifulSoup(html)
    try:
        next_page_link = soup.find(lambda node: u'下一页' == node.string)['href']
    except:
        next_page_link = None
    
    ret_dic_list = []
    metas = soup.find(name='ul',class_='excerpt')
    for meta in metas.children:
        info = Const.ret_dic_tplt.copy()
        info['article_title'] = meta.h2.a.string
        info['article_link'] = meta.a['href']
        info['article_pic_link'] = meta.a.img['src']
        info['article_website'] = 'www.zdfans.com'
        info['article_note'] = meta.find(name='div',class_='note').string
        
        info['article_post_date'],\
        info['article_cnt_up'],\
        info['article_tags'],\
        info['article_download_links'],\
        info['article_content'] = subpage_parser(requests.get(info['article_link']).text)
        ret_dic_list.append(info)
        
    return next_page_link,ret_dic_list

def subpage_parser(html):
    # 进去子页面 返回日期
    soup = bs4.BeautifulSoup(html)
    article_post_date = soup.find(name='p',class_='meta-info').get_text().split()[0]    #.encode('utf-8').replace('-','')
    article_cnt_up = int(soup.find(name='span',class_='view').span.string.encode('utf-8').replace(',',''))
    article_tags = [tmp.string.encode('utf-8') for tmp in soup.find(name='p',class_='meta-info').find_all(name='a',rel='category tag')]
    article_download_links = [] 
    #以上自动抓去下载链接 以及其密码 求助攻
    article_content = soup.find(name='div',class_='entry').prettify().encode('utf-8')   #unicode.encode('utf-8')
    return article_post_date,article_cnt_up,article_tags,article_download_links,article_content


if "__main__" == __name__:
    html = requests.get("http://www.zdfans.com/page/33").text
    next_page_link,ret_dic_list = page_parser(html)
    
    
    
    