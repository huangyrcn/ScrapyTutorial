# Scrapy 爬虫教程

Scrapy 是一个功能强大的 Python 爬虫框架，专为大规模网页抓取而设计。它提供了完整的爬虫解决方案，包括数据提取、处理和存储。本教程将带你从零开始学习如何使用 Scrapy 构建高效的网络爬虫。

## 环境准备

首先，我们需要设置一个干净的 Python 环境来安装 Scrapy。使用 Conda 创建虚拟环境可以避免依赖冲突问题。

```bash
conda create -n spiderenv
conda activate spiderenv
pip install scrapy
pip install scrapy  urljoin
```

## 创建爬虫项目

Scrapy 使用项目结构来组织代码。通过以下命令创建一个新的爬虫项目，这将生成必要的文件和目录结构：

```bash
cd xxxx  # 到一个合适的文件夹
scrapy startproject newscraper
```

## 创建爬虫

项目创建后，我们需要在项目内部创建具体的爬虫。下面的命令将创建一个名为 bookspider 的爬虫，目标网站是 books.toscrape.com：

```bash
scrapy genspider newspider 
```

## 文件目录结构

Scrapy 项目有一个标准化的目录结构，便于代码组织和维护。下面是创建项目后的基本文件结构及各文件的作用：

````
├── scrapy.cfg
└── infocraper
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        └── __init__.py
````

## 创建特定爬虫

```bash
scrapy genspider infospider http://www.ciomp.cas.cn/xwdt/zhxw/
```

## 使用 Scrapy Shell 查找 CSS 选择器、xPath选择器

Scrapy 的一大优点是它带有内置 shell，可以快速测试和调试 XPath 和 CSS 选择器。我们无需运行整个抓取程序来查看 XPath 或 CSS 选择器是否正确，而是可以直接将它们输入到终端并查看结果。

### 安装 IPython

我们使用 IPython 作为 Scrapy shell（功能更强大并提供智能自动完成和彩色输出），首先确保已安装 IPython：

```bash
pip install ipython
```

然后需要编辑 scrapy.cfg 的设置如下：

```ini
# scrapy.cfg
[settings]
default = tutorial.settings
shell = ipython
```

要打开 Scrapy shell，请使用以下命令：

```bash
scrapy shell
```

**CSS 选择器是 Scrapy 支持的一种选择器语言。** 它可以让你通过描述 HTML 元素的特征（比如标签名、类名、ID、属性等）来精确地定位到你想要提取数据的那些元素。

## 处理 JavaScript 生成的内容

我们发现，这个网页的代码在禁用了 JavaScript 后，没有页码。而正常情况下 Scrapy 不能处理这些数据。下面我们演示两种可行的方法。

### 方案一，预渲染

#### 使用 scrapy-playwright 渲染页面以获得通过 JavaScript 生成的网页内容

1. 安装 scrapy-playwright 及浏览器：

   ```bash
   pip install scrapy-playwright
   playwright install chromium  # 安装必要的浏览器
   ```

2. 配置 settings.py：

   ```python
   # 启用 playwright 下载处理器
   DOWNLOAD_HANDLERS = {
       "http": "scrapy_playwright.handler.PlaywrightDownloadHandler",
       "https": "scrapy_playwright.handler.PlaywrightDownloadHandler",
   }
   ```


#### 在 scrapy shell 中启用 playwright

下面是一个例子：

```python
fetch("http://www.ciomp.cas.cn/xwdt/zhxw/", meta={"playwright": True})
```

### 处理 JavaScript 生成的内容，方案二，寻找规律

start_urls = ["[http://www.ciomp.cas.cn/xwdt/zhxw/](http://www.ciomp.cas.cn/xwdt/zhxw/)"] + [
  
f"[http://www.ciomp.cas.cn/xwdt/zhxw/index_{i}.html](http://www.ciomp.cas.cn/xwdt/zhxw/index_%7Bi%7D.html)" for i in range(1, 38)
  
]

## 结构化数据处理

### 编写 items

Scrapy Items 是一种预定义的数据结构，用于保存数据。
  
我们可以预先在 items.py 文件中定义一个 Item 模式，并在抓取数据时使用该模式，而不要以字典的形式生成抓取的数据，以保证数据的结构化。

下面是我们定义的 items 和修改后的 parse_detail：

```python
class NewsItem(scrapy.Item):
    """定义新闻文章的数据结构"""
    title = scrapy.Field()          # 新闻标题
    publish_date = scrapy.Field()   # 发布日期
    author = scrapy.Field()         # 作者/来源
    url = scrapy.Field()            # 文章URL
    created_at = scrapy.Field()     # 爬取时间

def parse_detail(self, response):
    """解析每个新闻详情页，仅提取原始数据，不进行处理"""
    # 创建NewsItem对象
    news_item = NewsItem()
    
    # 提取原始数据，不做任何清洗处理
    news_item['title'] = response.css("td.bt::text").get()
    news_item['publish_date'] = response.xpath(
        '//tr[@align="right"]/td[@width="20%" and @class="hui12_sj2"]/text()'
    ).get()
    news_item['author'] = response.xpath(
        '//tr[@align="right"]/td[@align="center" and @width="22%"]/text()'
    ).get()
    news_item['url'] = response.url
    
    # 直接yield原始数据，让pipeline处理清洗和存储
    yield news_item
```

## 使用管道处理

Scrapy的管道系统是基于生成器(generator)设计的，每个管道通过yield返回处理后的item 这种设计使数据能够逐步流经多个处理阶段，而不需要一次性将所有数据加载到内存中

### 数据清洗

class NewsPipeline:
  
def process_item(self, item, spider):
  
"""处理每个抓取的新闻项"""
  
adapter = ItemAdapter(item)

````
    # 清洗数据
    # 1. 标题清洗：删除多余空格
    if adapter.get("title"):
        adapter["title"] = adapter["title"].strip()

    # 2. 发布日期清洗与格式化
    if adapter.get("publish_date"):
        adapter["publish_date"] = adapter["publish_date"].strip()
        # 可以添加日期格式化逻辑，例如将 "2025-03-18" 转为标准日期格式

    # 3. 作者/来源清洗
    if adapter.get("author"):
        adapter["author"] = adapter["author"].strip()

    # 添加爬取时间
    adapter["created_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return item
````

### 把结构化数据保存到数据库中

class SQLitePipeline:
  
def **init**(self):
  
# 数据库连接和游标
  
self.conn = None
  
self.cur = None

````
def open_spider(self, spider):
    """当爬虫启动时创建数据库连接"""
    self.conn = sqlite3.connect("news.db")
    self.cur = self.conn.cursor()

    # 创建表（如果不存在）
    self.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            publish_date TEXT,
            author TEXT,
            url TEXT UNIQUE,
            created_at TEXT
        )
    """
    )
    self.conn.commit()

def close_spider(self, spider):
    """当爬虫关闭时关闭数据库连接"""
    self.conn.close()

def process_item(self, item, spider):
    """将数据项插入数据库"""
    adapter = ItemAdapter(item)

    # 准备SQL语句和参数
    self.cur.execute(
        "INSERT OR IGNORE INTO news (title, publish_date, author, url, created_at) VALUES (?, ?, ?, ?, ?)",
        (
            adapter.get("title", ""),
            adapter.get("publish_date", ""),
            adapter.get("author", ""),
            adapter.get("url", ""),
            adapter.get(
                "created_at", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
        ),
    )
    self.conn.commit()

    return item
````

### 保存html文件