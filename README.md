# zhihu-spider
针对知乎热榜和知乎盐选开发了爬虫功能

## 项目依赖

​			使用Python 3.8.3编写，调用了requests, bs4, re, urllib, os等库辅助开发

​			在Windows10平台上测试通过

## 项目结构
* get_hot.py文件是针对知乎热榜的爬虫，
* get_list.py, get_catalog.py, get_chapter.py组成了针对知乎盐选的爬虫

### 爬取知乎热榜
1. 反爬

   由于知乎具有反爬虫机制，因此必须在请求数据时加入真实的请求头，具体定义在headers中，包括User-Agent, host, cookie三个部分

   加入cookie是为了绕过知乎的login页面，我将其写入cookies.txt文件中，在生成请求头时读取, 由于隐私原因，在项目文件中将其隐去

2. 提取信息

   主要使用了BeautifulSoup这一用于解析Html文档的强大的库，在其中使用lxml解析器

   提取到信息后按顺序将其依次排列，主要包括序号、问题、链接、简介等几部分内容

3. 数据存储

   提供了两种存储方式，一种是直接写入txt文件，另一种是存入mysql数据库中。

   Mysql默认使用3306端口，并且需要提前建立数据库表格

### 爬取盐选专栏
* get_list.py

    **该文件用于获取盐选专栏中的小说列表及其链接**
    1. 获取页面
    
        该部分与爬取热榜部分几乎完全一致，不再赘述
       
    2. 提取信息
       
        提取小说列表使用了find_all函数获得所有相邻节点，并提取每个节点的兄弟节点的文本值即可完成操作
       
        但对于每个小说链接的提取颇费功夫。由于href写在class中，而我并不清楚有无简便办法能完成提取功能，因此这部分采用了正则表达式完成提取，代码如下
       ```
       result = re.match('<a class="ProductCell-root-3LLcu InfiniteData-autoCell-hFmUN" href=".*?">', str(link))
       arr[i]['link'] = result.group()[68:-2]
       ```
    2. 数据的标准化
       
        find_all函数所提取到的数据包含大量空格和回车，其对于后面的使用会带来极大的不确定性，因此需要将数据转化为标准的格式，我使用了replace函数完成了替换工作
       
        
    
* get_catalog.py
  
    **该文件用于获取每部小说中的章节列表及其链接**
    1. 模拟ajax请求
       
        小说默认只显示前十章目录，而后面的章节需要人手动点击查看更多才会不断显示
       
        因此需要使用爬虫模拟ajax请求，经过分析，得到ajax请求头格式如下：
         ```
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
            'Referer': "https://www.zhihu.com/xen/market/remix/paid_column/" + url[-19:],
            'origin': 'https: // www.zhihu.com',
            'X-Requested-With': 'Fetch',
        }
         ```
    
        并且在请求url中使用offset来表示当前显示的章节数，limit表示每次请求的章节数，且固定为13，使用urlencode函数将参数拼接成标准的urL请求参数，请求到的信息为json格式
    2. 解析json
    
        这部分使用了在线json解析器来帮助分析数据，并将需要的数据写入Params字典中
    
    3. 处理初始目录页面
       
        小说前十章章节列表是直接显示在页面上的，章节名称可以直接通过findall提取
    
        但每一章的url在html页面中并没有直接显示，而是存放在\<textarea>这样一个隐藏数据块中, 这部分数据无法直接提取，因此使用了正则表达式将所需数据匹配出来
    4. 存储
       
        采取的存储策略是对于每部小说新建一个文件夹，在其中写入txt文件存放每一章内容，由于重复的文件名会报错，因此引入错误处理，若已存在则继续在文件夹中追加章节，否则新建
    
* get_chapter.py

    **该文件用于获取每一章的具体内容并写入指定的文件**
    
    这部分是向指定路径写入文本，并且去掉冗余的空格和回车
## 开发历程
Github仓库地址 <https://github.com/clingfei/spider>

其中main分支是项目的主分支，get_all分支是下载指定小说的代码，get_chapter是下载指定小说章节的代码

