import requests
from bs4 import BeautifulSoup
import pymysql
import re

def get_page(url, headers):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    with open("zhihu_salt.html",  'w', encoding="utf-8") as f:
        f.write(html)

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    arr = []
    titles = soup.find_all(class_="VerticalMiddle-root-g9oA5 ProductTitleTag-root-mWWpm ProductCell-titleTag-8AuZ3")
    for title in titles:
        for t in title.next_siblings:
            if(len(t.string) < 10):
                pass
            else:
                data = {
                    'title': t.string[12: -1],
                    'link': ''
                }
                arr.append(data)

    links = soup.find_all(class_="ProductCell-root-3LLcu InfiniteData-autoCell-hFmUN")
    i = -1
    for link in links:
        if i < 0:
            i += 1
        else:
            result = re.match('<a class="ProductCell-root-3LLcu InfiniteData-autoCell-hFmUN" href=".*?">', str(link))
            arr[i]['link'] = result.group()[68:-2]
            i += 1

    for s in arr:
        print(s)

if __name__ == '__main__':
    file = open("cookies.txt", 'r', encoding='utf-8')
    cookie = file.read()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Host': 'www.zhihu.com',
        'cookie': cookie
    }
    #get_page("https://www.zhihu.com/xen/market/vip/remix-album", headers)
    with open("zhihu_salt.html", 'r', encoding='utf-8') as f:
        html = f.read()
        parse_html(html)
