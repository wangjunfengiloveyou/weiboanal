import importlib
import sys
import time
import random
from requests import get as requests_get
from lxml import etree
from pymysql import connect as pyconnect
from pymysql import cursors
importlib.reload(sys)

def get_url(index):

    db1 = pyconnect(host='127.0.0.1',port=3306,user='root',password='123',db='URL_database',charset='utf8mb4',cursorclass = cursors.DictCursor)
 
    cursor1 = db1.cursor()

    str_index = str(index)
    
    sql_1 = "select url from weibo_full_url where weibo_id ="+ "'" + str_index + "'" ""
 
    cursor1.execute(sql_1)
    
    result1 = cursor1.fetchall()
    
    result = result1[0]['url']
    
    db1.close()
    
    return result


def create_table(index):
    
    db3 = pyconnect(host='127.0.0.1',port=3306,user='root',password='123',db='2019_database',charset='utf8mb4',cursorclass = cursors.DictCursor)
    
    cursor3 = db3.cursor()
    
    sql_4 = "DROP TABLE IF EXISTS ID" + str(index)
    
    cursor3.execute(sql_4)
    
    sql_3 = "CREATE TABLE ID" + str(index) + "(comment_num int NOT NULL AUTO_INCREMENT,user_id  VARCHAR(60),user_level VARCHAR(600),comment VARCHAR(600),PRIMARY KEY (comment_num)) default collate = utf8mb4_unicode_ci "
 
    cursor3.execute(sql_3)

    db3.close()


def write_in_database(text1,text2,text3,text4,index):
    
    db2 = pyconnect(host='127.0.0.1',port=3306,user='root',password='123',db='2019_database',charset='utf8mb4',cursorclass = cursors.DictCursor)
 
    cursor2 = db2.cursor()
    
    sql_2 = "INSERT INTO ID" + str(index) + " (user_id,user_level,comment)" +" VALUES(%s,%s,%s)"

    cursor2.execute(sql_2,(text2,text3,text4))
    
    db2.commit()
    
    db2.close()

    
def get_url_data(base_url, pageNum, word_count, index, cookie):
    
    base_url_deal = base_url + '%d'
    
    base_url_final = str(base_url_deal)

    for page in range(1,pageNum+1):

        url = base_url_final%(page)
        lxml = requests_get(url, cookies = cookie).content

        selector = etree.HTML(lxml)

        weiboitems = selector.xpath('//div[@class="c"][@id]')

        time.sleep(random.randint(1,2))
        
        for item in weiboitems:      
            weibo_id = item.xpath('./@id')[0]
            ctt = item.xpath('./span[@class="ctt"]/text()')
            level = item.xpath('./img/@alt')
      
            text1 = str(word_count)
            text2 = str(weibo_id)
            text4 = str(ctt)
            text3 = str(level)
            
            write_in_database(text1,text2,text3,text4,index)
            
            word_count += 1

