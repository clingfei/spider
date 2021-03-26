import requests
from bs4 import BeautifulSoup
import pymysql
import re
from urllib.parse import urlencode


def get_init_page(url, headers):
    html =requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    with open("zhihu_text.html",  'w', encoding="utf-8") as f:
        f.write(html)

def process_ajax():
    base_url = "https://api.zhihu.com/remix/well/1312485331866730496/catalog?"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Host': 'www.zhihu.com',
        'cookie': cookie,
        'Referer': "https://www.zhihu.com/xen/market/remix/paid_column/1312485331866730496",
        'X-Requested-With': 'XMLHttpRequest'
    }

if __name__ == '__main__':
    file = open("cookies.txt", 'r', encoding='utf-8')
    cookie = file.read()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Host': 'www.zhihu.com',
        'cookie': cookie
    }
    get_init_page("https://www.zhihu.com/xen/market/remix/paid_column/1312485331866730496", headers)


