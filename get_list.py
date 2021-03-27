import requests
from bs4 import BeautifulSoup
import re
import get_catalog

"""获得盐选小说排行榜页面"""
def get_page(url, headers):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    #with open("zhihu_salt.html",  'w', encoding="utf-8") as f:
    #    f.write(html)
    return html

"""处理小说排行榜, 并将每部小说标题及其链接传入get_catalog作进一步处理"""
def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    arr = []
    titles = soup.find_all(class_="VerticalMiddle-root-g9oA5 ProductTitleTag-root-mWWpm ProductCell-titleTag-8AuZ3")
    for title in titles:
        for t in title.next_siblings:
            if(len(t.string) < 10):
                pass
            else:
                title = t.string[13: -12]
                title.replace(" ", "")
                title.replace("\n", "")
                data = {
                    'title': title,
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

    get_catalog.get_catalog(arr)


if __name__ == '__main__':
    headers = get_catalog.get_headers()
    html = get_page("https://www.zhihu.com/xen/market/vip/remix-album", headers)
    #with open("zhihu_salt.html", 'r', encoding='utf-8') as f:
    #html = f.read()
    parse_html(html)
