import requests
from bs4 import BeautifulSoup
import pymysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
    'Host': 'www.zhihu.com',
    'cookie': '_zap=77da30fd-21a0-4768-a388-3f9aba501a88; d_c0="ANDYY67F1RCPTumDleF-m85vXCcFBAAti1M=|1582003915"; _ga=GA1.2.1481100015.1582362017; _xsrf=sLZnNY1N291A0Eyt7rXDrrMMgqNJGOqe; __gads=ID=30e43948c1587368:T=1561982828:S=ALNI_MaKixacoDHA-VfflUUbMGNjvMZCFA; tshl=; __utmv=51854390.100--|2=registration_date=20191120=1^3=entry_date=20191120=1; __utma=51854390.1481100015.1582362017.1606704403.1606830558.12; __utmz=51854390.1606830558.12.4.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/432775510; q_c1=22708782701e4ae5858bac68041143f8|1612748001000|1582102080000; captcha_ticket_v2="2|1:0|10:1614431887|17:captcha_ticket_v2|312:eyJhcHBpZCI6IjIwMTIwMzEzMTQiLCJyZXQiOjAsInRpY2tldCI6InQwM2d1c2VwSFZxYkItR2lHbnFJWEY1N19CaHlWdTFfdGo5TWNsZFdkaEQ5NjRoQWZSTmVnRFA4SU43ckg1RGFCQlB0a0pOY1pweHg0RzQwUHBvTWtfQnZranhMN2Y2U3MtOUVuakdLTlR1SkItazRWTThmck9iM2loLXdrNENPSFpkMXpXRHljRk9qeW1vN1IzY3dvUmZYWFFwT2RlcHJlY3cweVEweFdMVnRHayoiLCJyYW5kc3RyIjoiQGRveCJ9|971a6512e9bfb06945e9617c9fb3a9bfd16b075ba0c0e749b22be7b1c9a5dcbd"; z_c0="2|1:0|10:1614431888|4:z_c0|92:Mi4xbGFmSEdnQUFBQUFBME5oanJzWFZFQ1lBQUFCZ0FsVk5qNVFuWVFBTWRBZmdMYTJYUmVTVWZPVV96N2Via01SSkVB|a1a5a8a9dae47eee957c36dcfb41796946886a5b39fad7de4c1a9fb985ccaa87"; captcha_session_v2="2|1:0|10:1614431889|18:captcha_session_v2|88:bHExWkxmVm1VMjVlU2NhcXRFKzBNTTJiWEhxSnRxM2ttTE1HZzBLdStYN1ZnUkFLN3pvV1Y0Y3djOStHY1pkYw==|90aac5946d28d894935e773d261012a2f10748c2ae60396f9592d2c91b5d6662"; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1614684147,1614686582,1614699662,1614700147; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1614700147; SESSIONID=1ghqkdaaP14PJqvEfuAs25swGK897vao91BeQdMiDQT; JOID=Vl8TBUmzP3yOTwGdKLHqq9Fdvs47gVkU-yJm_UnlDUneAXbobMVgRuxKA5wsdJ9ZfYLnaKFG0Q7-36seVHZkLr0=; osd=W1kXAUi-OXiKTgybLLXrptdZus82h10Q-i9g-U3kAE_aBXflasFkR-FMB5gteZldeYPqbqVC0AP4268fWXBgKrw=; KLBRSID=81978cf28cf03c58e07f705c156aa833|1614700170|1614699662'
}



def get_page(url):
    html = requests.get("https://www.zhihu.com/hot", headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()
    with open("zhihu.html", 'w', encoding="utf-8") as f:
        f.write(html)

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.find_all(class_="HotItem-title")
    contents = soup.find_all(class_="HotItem-excerpt")
    links = soup.find_all(class_="HotItem-img")
    print(links['href'])
    print(contents[0].text)
    print(len(contents))
    #for title in titles:
     #   print(title.text)
        #print(content.text)

def main():
    with open("zhihu.html", 'r', encoding="utf-8") as f:
        html = f.read()
        parse_html(html)

main()
