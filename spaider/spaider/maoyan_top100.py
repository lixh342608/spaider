'''
Created on 2017年7月14日

@author: Administrator
'''
import requests,re,json
from multiprocessing import Pool

def get_one_page(url):
    html=requests.get(url)
    page_text=html.text
    return page_text
def parser_one_page(html_text):
    reg='<dd>.*?index.*?>(\d+)</i>.*?title="(.*?)".*?data-src="(.*?)".*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?"integer">(.*?)</i>.*?"fraction">(\d+)</i>.*?</dd>'   
    cop=re.compile(reg,re.S)
    moves=re.findall(cop,html_text)
    for move in moves:
        yield {'index':move[0],
               'name':move[1],
               'img':move[2],
               'acter':move[3].split()[3:],
               'atime':move[4][5:],
               'fish':move[5]+move[6]
            }
def write_tofile(text):
    with open('c:/result.text','a+',encoding='utf-8') as f:
        f.write(json.dumps(text,ensure_ascii=False)+'\n')
def main(offset):
    url='http://maoyan.com/board/4?offset=%d' % (offset*10)
    html_text=get_one_page(url)
    #itms=parser_one_page(html_text)
    for itm in parser_one_page(html_text):
        print(itm)
        write_tofile(itm)
if __name__=='__main__':
    #pool=Pool()
    #pool.map(main,[i for i in range(10)])
    for i in range(10):
        main(i)
    
    