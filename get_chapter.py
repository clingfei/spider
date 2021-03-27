from bs4 import BeautifulSoup
import requests
import get_catalog

"""获取小说页面"""
def get_article(url, headers):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    return html

"""将标题写入文件"""
def parse_html(html, title, chapter):
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find_all("p")
    path = title + "/" + chapter + ".txt"
    file = open(path, "w", encoding='utf-8')
    for result in results:
        text = result.text
        text = text.replace("\n", "")
        text = text.replace(" ", "")
        file.write(text)
        file.write("\n")
    file.close()
    print("写入完成")

"""获得小说每一章的标题及其链接，以及小说标题"""
def getArr(arr, title):
    headers = get_catalog.get_headers()
    for params in arr:
        url = params["url"]
        chapter = params["serial_number_txt"]
        html = get_article(url, headers=headers)
        parse_html(html, title, chapter)
