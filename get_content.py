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
    parse_html(html)

"""得到已更新的章节数"""
def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    totals = soup.find(class_="CatalogModule-updateText-upu4E")
    if re.search("已完结", totals.string):
        result = re.search("共 .*? 节", totals.string)
    else:
        result = re.search("第 .*? 节", totals.string)
    sum = int(result.group()[2: -2])
    print(sum)
    process_ajax(sum)

def process_ajax(total):
    base_url = "https://api.zhihu.com/remix/well/1312485331866730496/catalog?"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Referer': "https://www.zhihu.com/xen/market/remix/paid_column/1312485331866730496",
        'origin': 'https: // www.zhihu.com',
        'X-Requested-With': 'Fetch',
    }
    params = {
        'offset': 10,
        'limit': 13,
        'order_by': 'global_idx',
        'is_new_column': 'true'
    }
    while((params['offset'] + params['limit'])<total):
        params['offset'] += 13
    url = base_url + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            parse_json(response.json(), re.search('/[0-9]+?/', base_url).group()[1: -1])
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_json(json, article_no):
    base_url = "https://www.zhihu.com/market/paid_column/"
    for i in range(len(json["data"])):
        url = base_url + str(article_no) + "/section/" + json["data"][i]["id"]
        print(url)

if __name__ == '__main__':
    file = open("cookies.txt", 'r', encoding='utf-8')
    cookie = file.read()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Host': 'www.zhihu.com',
        'cookie': cookie
    }
    #get_init_page("https://www.zhihu.com/xen/market/remix/paid_column/1312485331866730496", headers)
    with open("zhihu_text.html", 'r', encoding='utf-8') as f:
        html = f.read()
        parse_html(html)


