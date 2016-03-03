# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:21:42 2016

@author: 4473
"""

import MySQLdb
import ConfigRPG
import sys
import _mysql



class SQLer():
    def __init__(self,host,user,pswd,dbnm=None):
        self.connection = MySQLdb.connect(host=host,user=user,passwd=pswd,db=dbnm,charset='utf8')
        self.cc = _mysql.connect(host,user,pswd,dbnm)
    
    def get_latest_link(self,website):
        try:
            cmd = 'SELECT article_link FROM infos WHERE website="%s" ORDER BY post_time DESC LIMIT 1;' % (website)
            self.cc.query(cmd)
            r = self.cc.use_result()
            link = r.fetch_row()[0][0]
        except Exception as ex:
            print ex
            link = None
        finally:
            return link
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
    host = ConfigRPG.sql_host
    user = ConfigRPG.sql_user
    pswd = ConfigRPG.sql_pass
    dbnm = ConfigRPG.sql_dbnm
    
    
    db = MySQLdb.connect(host=host,user=user,passwd=pswd,db=dbnm,charset='utf8')
    
    from roles import zdfans
    html = zdfans.requests.get(zdfans.latest_url).text
    next_page_link,infos = zdfans.page_parser(html)
    
    sqler =SQLer(host,user,pswd,dbnm)
    print  sqler.get_latest_link('www.zdfans.com') 
    
    
    

    
































