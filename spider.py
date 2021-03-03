import requests
from bs4 import BeautifulSoup
import pymysql

def get_page(url, headers):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    with open("zhihu.html", 'w', encoding="utf-8") as f:
        f.write(html)

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.find_all(class_="HotItem-title")
    contents = soup.find_all(class_="HotItem-excerpt")
    links = soup.find_all(class_="HotItem-img")
    create_dic(titles, contents, links)

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

    storage(arr)

def storage(arr):
    db = pymysql.connect(host="localhost", user="root", password="root", port=3306, database="spiders")
    cursor = db.cursor()
    for data in arr:
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = "INSERT INTO zhihu ({keys}) VALUES ({values})".format(keys=keys, values=values)
        cursor.execute(sql, (data['id'], data['title'], data['content'], data['link']))
        db.commit()
    db.close()

def main():
    file = open("cookies.txt", 'r', encoding="utf-8")
    cookie = file.read()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Host': 'www.zhihu.com',
        'cookie': cookie
    }
    get_page("https://www.zhihu.com/hot", headers)
    with open("zhihu.html", 'r', encoding="utf-8") as f:
        html = f.read()
        parse_html(html)

main()
