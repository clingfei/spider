import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlencode
import os
import get_chapter

"""得到一部小说的主页面"""
def get_init_page(url, headers, title):
    html =requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    try:
        os.makedirs(title)
    except:
        return
    sum = get_total(html)
    parse_html(url, html, title)
    process_ajax(sum, title, url)

"""处理小说初始页面的章节目录"""
def parse_html(url, html, title):
    soup = BeautifulSoup(html, 'lxml')
    res_chapters = soup.find_all(class_="CatalogModule-chapterCommonTitle-cbpkp")

    chapter = []
    for res_chapter in res_chapters:
        chapter.append(res_chapter.text[11:-10])

    sections = []
    results = soup.find_all(class_="Image-imageWrapper-7zqcD ChapterItem-vipTag-vJ2vM")
    for result in results:
        for res_section in result.next_siblings:
            tmp = res_section.string
            tmp = tmp.replace('\n', "")
            if len(tmp) > 2:
                sections.append(tmp[12:-11])

    arr = []
    base_url = "https://www.zhihu.com/market/paid_column/" + url[-19:]

    textarea = soup.find(name="textarea").text
    id = re.findall("track_id=[0-9]{19}", textarea)

    i, j = -1, -1
    print(chapter)
    print(url)
    for section in sections:
        params = {
            "url": "",
            "serial_number_txt": ""
        }
        if len(chapter) > 0:
            if re.search("第 1 节", section):
                j += 1
            params["serial_number_txt"] = chapter[j] + section[0:6]
        else:
            params["serial_number_txt"] = section[0:6]
        i += 1
        params["url"] = base_url  + "/section/" + id[i][9:]
        arr.append(params)

    get_chapter.getArr(arr, title)

"""得到已更新的章节数"""
def get_total(html):
    soup = BeautifulSoup(html, 'lxml')
    totals = soup.find(class_="CatalogModule-updateText-upu4E")
    if re.search("已完结", totals.string):
        result = re.search("共 .*? 节", totals.string)
    else:
        result = re.search("第 .*? 节", totals.string)
    sum = int(result.group()[2: -2])
    return sum

"""
    处理ajax请求，获取一部小说的全部目录,获得每一次展开的目录的json格式的响应
    由于分批显示所有目录，因此可依次爬取每个目录中的小说文本
"""
def process_ajax(total, title, url):
    base_url = "https://api.zhihu.com/remix/well/" + url[-19:] + "/catalog?"   #这里的Url应该换成通用的
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Referer': "https://www.zhihu.com/xen/market/remix/paid_column/" + url[-19:],
        'origin': 'https: // www.zhihu.com',
        'X-Requested-With': 'Fetch',
    }
    params = {
        'offset': 10,
        'limit': 13,
        'order_by': 'global_idx',
        'is_new_column': 'true'
    }
    while((params['offset'] + params['limit']) < total):
        params['offset'] += 13
        url = base_url + urlencode(params)
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                parse_json(response.json(), re.search('/[0-9]+?/', base_url).group()[1: -1], title)
        except requests.ConnectionError as e:
            print('Error', e.args)

"""
    获取ajax传送的json数据，并依次提取其章节名，章节url
    arr中的数据包括url和章节名两部分
"""
def parse_json(json, article_no, title):
    base_url = "https://www.zhihu.com/market/paid_column/"
    arr = []
    for i in range(len(json["data"])):
        params = {
            "url": "",
            "serial_number_txt": ""
        }
        url = base_url + str(article_no) + "/section/" + json["data"][i]["id"]
        params["url"] = url
        serial_number_txt = json["data"][i]["chapter"]["serial_number_txt"] + json['data'][i]["index"]["serial_number_txt"]
        params["serial_number_txt"] = serial_number_txt
        arr.append(params)

    get_chapter.getArr(arr, title)

def get_headers():
    file = open("cookies.txt", 'r', encoding='utf-8')
    cookie = file.read()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Host': 'www.zhihu.com',
        'cookie': cookie
    }
    file.close()
    return headers

def get_catalog(arr):
    for params in arr:
        title = params['title']
        url = params['link']
        headers = get_headers()
        get_init_page(url, headers, title)


