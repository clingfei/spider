from bs4 import BeautifulSoup
import requests
#import get_catalog

def get_article(url, headers):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    return html

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find_all("p")
    file = open("chapter.txt", "w", encoding='utf-8')
    print(results)
    for result in results:
        text = result.text
        text = text.replace("\n", "")
        text = text.replace(" ", "")
        file.write(text)
        file.write("\n")
    file.close()
    print("写入完成")

if __name__ == "__main__":
    url = "https://www.zhihu.com/market/paid_column/1238803218659819520/section/1238882552661647360"
    file = open("cookies.txt", 'r', encoding='utf-8')
    cookie = file.read()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Host': 'www.zhihu.com',
        'cookie': cookie
    }
    file.close()
    html = get_article(url, headers)
    parse_html(html)