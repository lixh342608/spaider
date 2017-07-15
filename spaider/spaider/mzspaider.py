#coding=utf-8
'''
Created on 2017年7月14日

@author: Administrator
'''
import requests,json,re
from requests.exceptions import RequestException
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from multiprocessing import Pool
def get_url(url,types):
    try:
        respon=requests.get(url)
        if respon.status_code==200:
            return respon.text
        return None
    except RequestException as e:
        print("%s请求错误" % types)
        return None
def parse_do_one(url):
    one_text=get_url(url,'页面')
    data=json.loads(one_text)
    if data and 'data' in data.keys():
        for item in data.get("data"):
            yield item.get('article_url')
def parse_xqimg(html):
    soup=BeautifulSoup(html,'html.parser')
    title=soup.title.text
    req=re.compile('var gallery = (.*?);',re.S)
    result=re.search(req, html)
    if result:
        data=json.loads(result.group(1))
        sub_imgs=data.get('sub_images')
        img_urls=[item.get('url') for item in sub_imgs]
        return {
            'title':title,
            'img_urls':img_urls
            }          

def main(offset,cop='美女'):
    print("第%d页开始抓取..." % (offset/20+1))
    data={"offset":offset,
          "format":"json",
          "keyword":cop,
          "autoload":"true",
          "count":20,
          "cur_tab":3}
    
    url='http://www.toutiao.com/search_content/?'+urlencode(data)    

    for item in parse_do_one(url):
        html=get_url(item,'详情页')
        if html:
            item=parse_xqimg(html)
            if item:
                print(item)
    print("第%d页抓取完毕！" % (offset/20+1))        

if __name__=='__main__':
    pool=Pool()
    pool.map(main,[i*20 for i in range(8)])
    '''for i in range(8):
        i*=20
        main(i,"美女")'''        
        
        
    