# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:21:42 2016

@author: Ju.51
"""

import MySQLdb

class SQLer():
    def __init__(self,host,user,pswd,dbnm=None):
        self.db = MySQLdb.connect(host=host,
                                          user=user,
                                          passwd=pswd,
                                          db=dbnm,
                                          charset='utf8')
    
    def get_latest(self,website):
        # website : www.example.com
        # 返回该网站在数据库中已有的、最新的文章链接 以及该文章的发布时间
        # 返回日期防止该文章被删除
        # 如果没有则返回None
        try:
            cs = self.db.cursor()
            cmd = 'SELECT * FROM articles WHERE article_website="%s" ORDER BY article_post_date DESC LIMIT 1;' % (website)
            cs.execute(cmd)
            data = cs.fetchone()
        except Exception as ex:
            print type(ex),ex
            data = None
        finally:
            return data[2],data[5]
            
    def insert(self,infos):
        cursor = self.connection.cursor()
        for info in infos:
            try:
                fields = [key for key in info.keys() if info[key] is not None]
                values = [info[key] for key in fields]
                f_str = '('+','.join(fields)+')'   
                v_str = '('+','.join(['"'+item+'"' for item in values])+')'
                cmd = """INSERT INTO infos %s VALUES %s ;""" % (f_str,v_str)
                cursor.execute(cmd)            
                self.connection.commit()
                #print 'Success entry AT ' + info['article_link']
            except Exception as ex:
                if 1062 == ex[0]:
                    pass
                    #print 'Duplicate entry AT ' + info['article_link']
                else:
                    raise Exception
        cursor.close()
        return 


if '__main__' == __name__:
    import Configer
    sqler = SQLer(Configer.host,Configer.usnm,Configer.pswd,Configer.dbnm)
    for website in Configer.target_sites:
        break
        website_latest = sqler.get_latest(website)
        print website_latest
    
    
    
    

    
































