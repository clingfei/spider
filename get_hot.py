import datetime
import requests
from bs4 import BeautifulSoup
import pymysql

"""获取热榜页面"""
def get_page(url, headers):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    return html

"""处理html页面，生成每一条数据的标题、链接和简介"""
def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.find_all(class_="HotItem-title")
    contents = soup.find_all(class_="HotItem-excerpt")
    links = soup.find_all(class_="HotItem-img")
    create_dic(titles, contents, links)

"""
接收来自paese_html传递的参数，将其合并入字典,并传入store_intext函数中用以生成文件
实际上，如果将store_intext函数更换为store_indb, 可以存入本地的mysql数据库中
"""
def create_dic(titles, contents, links):
    arr = []
    for i in range(0, 50):
        len_t = len(titles[i].text) - 18
        data = {
            "id": i + 1,
            "title": titles[i].text[18: len_t + 1],
            "content": None,
            "link": None
        }
        arr.append(data)

    i = 0
    for content in contents:
        len_c = len(content.text) - 18
        arr[i]['content'] = content.text[18: len_c + 1]
        i += 1

    i = 0
    for link in links:
        arr[i]['link'] = link.attrs['href']
        i += 1
    store_intext(arr)

"""将字典存入文件"""
def store_intext(arr):
    time = datetime.date.today()
    docName = "hot_" + str(time) + ".txt"
    file = open(docName, "a+", encoding="utf-8")
    for data in arr:
        if (data['content']==None):
            data['content'] = "暂无详细内容"
        file.write(str(data['id']) + " " + "title: " + str(data['title']) + "\ncontent: " + str(data['content']) + "\nlink: " + str(data['link']))
        file.write("\n\n")
    file.close()

"""将字典存入数据库"""
def store_indb(arr):
    db = pymysql.connect(host="localhost", user="root", password="root", port=3306, database="spiders")
    cursor = db.cursor()
    for data in arr:
        if (data['content']==None):
            data['content'] = "暂无详细内容"
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = "INSERT INTO zhihu ({keys}) VALUES ({values})".format(keys=keys, values=values)
        cursor.execute(sql, (data['id'], data['title'], data['content'], data['link']))
        db.commit()
    db.close()

if __name__ == '__main__':
    file = open("cookies.txt", 'r', encoding="utf-8")
    cookie = file.read()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Host': 'www.zhihu.com',
        'cookie': cookie
    }
    file.close()
    url = "https://www.zhihu.com/hot"
    html = get_page(url, headers)
    parse_html(html)
