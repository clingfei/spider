from bs4 import BeautifulSoup
import requests

def get_article(url, headers):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    #print(html)
    file = open("chapter.html", 'w', encoding='utf-8')
    file.write(html)
    file.close()

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find_all("p")
    print(results[0])
    file = open("chapter.txt", "w", encoding='utf-8')
    for result in results:
        print(result)
        text = result.text
        text = text.replace("\n", "")
        text = text.replace(" ", "")
        file.write(text)
        file.write("\n")
    file.close()

if __name__ == '__main__':
    url = "https://www.zhihu.com/market/paid_column/1312485331866730496/section/1358111171007021056"
    file = open("cookies.txt", 'r', encoding='utf-8')
    cookie = file.read()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Host': 'www.zhihu.com',
        'cookie': cookie
    }
    #get_article(url, headers=headers)
    with open("chapter.html", 'r', encoding='utf-8') as f:
        html = f.read()
        parse_html(html)
