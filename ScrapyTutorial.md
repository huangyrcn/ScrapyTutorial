# Scrapy 爬虫教程

Scrapy 是一个功能强大的 Python 爬虫框架，专为大规模网页抓取而设计。它提供了完整的爬虫解决方案，包括数据提取、处理和存储。本教程将带你从零开始学习如何使用 Scrapy 构建高效的网络爬虫。

## 环境准备

首先，我们需要设置一个干净的 Python 环境来安装 Scrapy。使用 Conda 创建虚拟环境可以避免依赖冲突问题。

```bash
conda create -n spiderenv python=3.12
```

```bash
conda activate spiderenv
```

下面是我们需要的一些三方库

```bash
pip install scrapy  urljoin openpyxl ipython
```

## 创建爬虫项目

Scrapy 使用项目结构来组织代码。保证当前的路径是仓库的文件夹的根路径。通过以下命令创建一个新的爬虫项目，这将生成必要的文件和目录结构：

```bash
scrapy startproject newscraper
```


## 文件目录结构

Scrapy 项目有一个标准化的目录结构，便于代码组织和维护。下面是创建项目后的基本文件结构及各文件的作用：

`````
├── scrapy.cfg
└── infocraper
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        └── __init__.py
`````

## 创建特定爬虫

```bash
scrapy genspider newsspider http://www.ciomp.cas.cn/xwdt/zhxw/
```

按模板生成了如下代码：

```python
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

```

## 如何指定我们想要的信息

现在我们已经创建了一个特定的爬虫，接下来就需要告诉 Scrapy 如何从抓取到的网页中提取我们感兴趣的数据。
Scrapy 提供了强大的选择器机制，帮助我们精准地定位和提取 HTML 或 XML 文档中的特定内容。
其中，最常用的两种选择器是 CSS 选择器和 XPath 选择器。

### 数据提取的核心：选择器

在网络爬虫中，最关键的步骤之一就是从下载的网页源代码中提取有用的信息。
Scrapy 提供了两种强大的选择器语言，帮助我们实现这一目标：CSS 选择器 (CSS Selectors)
和 XPath 选择器 (XPath Selectors)。
它们允许我们通过不同的方式来描述我们想要选取的网页元素，从而提取出目标数据。

**CSS 选择器示例**

假设我们有如下 HTML 片段：

```html
<div id="content">
  <h2 class="news-title">最新新闻标题</h2>
  <p class="article-info">
    发布于 <span class="date">2025-03-20</span>，作者：<span class="author">张三</span>
  </p>
  <ul>
    <li class="item-1"><a href="/news/1">第一条新闻</a></li>
    <li class="item-2"><a href="/news/2">第二条新闻</a></li>
  </ul>
</div>
```
CSS 选择器可以让你通过描述 HTML 元素的特征（比如标签名、类名、ID、属性等）来精确地定位到你想要提取数据的那些元素。

以下是一些 CSS 选择器的示例及其含义：

* `div#content`: 选择 `id` 为 `content` 的 `div` 元素。 (`#` 用于选择 ID)
* `h2.news-title`: 选择 `class` 为 `news-title` 的 `h2` 元素。 (`.` 用于选择 class)
* `p.article-info span.date`: 选择 `class` 为 `article-info` 的 `p` 元素内部的 `class` 为 `date` 的 `span` 元素。 (空格表示后代选择器)
* `ul li.item-1 a`: 选择 `ul` 元素内部的 `class` 为 `item-1` 的 `li` 元素内部的 `a` 元素。
* `a[href]`: 选择所有带有 `href` 属性的 `a` 元素。 (`` 用于选择带有特定属性的元素)
* `a[href="/news/2"]`: 选择 `href` 属性值为 `/news/2` 的 `a` 元素。
* `li:first-child`: 选择 `li` 元素列表中的第一个 `li` 元素。 (`:first-child` 是一个伪类选择器)
* `li:last-child`: 选择 `li` 元素列表中的最后一个 `li` 元素。 (`:last-child` 是一个伪类选择器)

**XPath 选择器示例**

仍然使用上面的 HTML 片段：

```html
<div id="content">
  <h2 class="news-title">最新新闻标题</h2>
  <p class="article-info">
    发布于 <span class="date">2025-03-20</span>，作者：<span class="author">张三</span>
  </p>
  <ul>
    <li class="item-1"><a href="/news/1">第一条新闻</a></li>
    <li class="item-2"><a href="/news/2">第二条新闻</a></li>
  </ul>
</div>
```

* `//div[@id="content"]`: 选择 `id` 属性值为 `content` 的所有 `div` 元素。 (`//` 表示在整个文档中查找，`@` 用于选择属性)
* `//h2[@class="news-title"]`: 选择 `class` 属性值为 `news-title` 的所有 `h2` 元素。
* `//p[@class="article-info"]/span[@class="date"]/text()`: 选择 `class` 为 `article-info` 的 `p` 元素内部的 `class` 为 `date` 的 `span` 元素的文本内容。 (`/` 表示子元素，`text()` 用于提取文本)
* `//ul/li[@class="item-1"]/a/@href`: 选择 `ul` 元素内部的 `class` 为 `item-1` 的 `li` 元素内部的 `a` 元素的 `href` 属性值。 (`@` 后跟属性名用于提取属性值)
* `//a`: 选择文档中的所有 `a` 元素。
* `//a[contains(@href, "/news/")]`: 选择 `href` 属性包含 `/news/` 的所有 `a` 元素。 (`contains()` 是一个函数，用于检查属性是否包含某个字符串)
* `//li[1]`: 选择 `li` 元素列表中的第一个 `li` 元素。 (索引从 1 开始)
* `//li[last()]`: 选择 `li` 元素列表中的最后一个 `li` 元素。 (`last()` 函数返回最后一个元素的索引)


### 使用 Scrapy Shell 查找 CSS 选择器、xPath选择器

Scrapy 的一大优点是它带有内置 shell，可以快速测试和调试 XPath 和 CSS 选择器。我们无需运行整个抓取程序来查看 XPath 或 CSS 选择器是否正确，而是可以直接将它们输入到终端并查看结果。

### 安装 IPython

我们使用 IPython 作为 Scrapy shell（功能更强大并提供智能自动完成和彩色输出），首先确保已安装 IPython：


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

### 使用浏览器和 scrapy shell 结合编写

在实际编写 Scrapy 爬虫时，通常会结合使用浏览器的开发者工具和 Scrapy Shell 来确定合适的 CSS 和 XPath 选择器。

#### 获取条目的信息

在 shell 中获取响应：

```python
fetch("http://www.ciomp.cas.cn/xwdt/zhxw/")
```

**选取条目和链接**

* `response.css("a.font06")`: 这个 CSS 选择器用于选取所有 `class` 属性包含 `font06` 的 `<a>` 标签元素。这通常用于定位列表中的条目链接。
* `item.css("::attr(href)")`: 如果 `item` 是一个表示 `<a>` 标签的选择器对象，这个 CSS 选择器将提取该标签的 `href` 属性值，即链接地址。`::attr(href)` 用于获取元素的属性值。

现在我们进入这具体的网页，并选择我们需要的内容：

#### 获取具体的有效信息

对于一个具体的条目，在获取了对于页面后，我们需要获取具体的信息。

在 shell 中获取响应：

```python
fetch("http://www.ciomp.cas.cn/xwdt/zhxw/202503/t20250319_7560793.html")
```

**提取标题**

* `response.css("td.bt::text").get()`: 这个 CSS 选择器首先选取所有 `class` 属性为 `bt` 的 `<td>` 标签元素，然后使用 `::text` 提取这些元素的文本内容。`.get()` 方法用于获取匹配到的第一个文本内容。

**提取发布日期**

* ```python
    response.xpath(
        '//tr[@align="right"]/td[@width="20%" and @class="hui12_sj2"]/text()'
    ).get()
    ```
    这个 XPath 选择器用于精确定位发布日期信息：
    * `//tr[@align="right"]`: 选取所有 `align` 属性为 `right` 的 `<tr>` 标签。
    * `/td[@width="20%" and @class="hui12_sj2"]`: 在上一步选取的 `<tr>` 标签的直接子元素中，选取 `width` 属性为 `"20%"` 并且 `class` 属性为 `"hui12_sj2"` 的 `<td>` 标签。
    * `/text()`: 提取该 `<td>` 标签的文本内容。
    * `.get()`: 获取匹配到的第一个文本内容。
* `publish_date_elem.strip() if publish_date_elem else None`: 这段 Python 代码用于对提取到的发布日期文本进行处理。如果 `publish_date_elem` 不为空，则使用 `.strip()` 方法去除文本两端的空白字符；如果为空，则返回 `None`。

**提取作者/来源**

* ```python
    response.xpath(
        '//tr[@align="right"]/td[@align="center" and @width="22%"]/text()'
    ).get()
    ```
    这个 XPath 选择器用于精确定位作者/来源信息，结构与提取发布日期的 XPath 类似：
    * `//tr[@align="right"]`: 选取所有 `align` 属性为 `right` 的 `<tr>` 标签。
    * `/td[@align="center" and @width="22%"]`: 在上一步选取的 `<tr>` 标签的直接子元素中，选取 `align` 属性为 `"center"` 并且 `width` 属性为 `"22%"` 的 `<td>` 标签。
    * `/text()`: 提取该 `<td>` 标签的文本内容。
    * `.get()`: 获取匹配到的第一个文本内容。

这些示例展示了如何使用 CSS 和 XPath 选择器从网页中提取特定的数据，以及如何结合 Scrapy Shell 进行测试和完善。在实际操作中，你需要检查目标网页的 HTML 结构，并根据需要调整选择器。

## 处理 JavaScript 生成的内容

我们发现，这个网页的代码在禁用了 JavaScript 后，没有页码。而正常情况下 Scrapy 不能处理这些数据。下面我们演示两种可行的方法。

### 方案一、预渲染

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

### 方案二、寻找规律

start_urls = ["http://www.ciomp.cas.cn/xwdt/zhxw/"] + [
  
    f"http://www.ciomp.cas.cn/xwdt/zhxw/index_{i}.html" for i in range(1, 38)
  
]

<!-- 说明 -->

此方案通过观察目标网站分页 URL 的固定规律实现自动构造各分页 URL。由于网页在禁用 JavaScript 后还保留分页链接，因此可以根据已知 URL 模板，利用页码递增来生成所有页面的完整 URL。这种方法简单高效，适用于页面 URL 格式一致、无需浏览器渲染的场景。


## 第一阶段的成果
下面，的代码是我们第一阶段的成果：

```python

import scrapy
import json
from urllib.parse import urljoin


class NewsspiderSpider(scrapy.Spider):
    name = "newsspider"
    allowed_domains = ["www.ciomp.cas.cn"]
    start_urls = ["http://www.ciomp.cas.cn/xwdt/zhxw/"] + [
        f"http://www.ciomp.cas.cn/xwdt/zhxw/index_{i}.html" for i in range(1, 38)
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_list = []  # 用于存储所有数据

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # 处理所有目标项
        for item in response.css("a.font06"):
            link = item.css("::attr(href)").get()
            # 如果 link 是完整的 URL，则直接使用，否则拼接为完整 URL
            if link:
                detail_url = (
                    link if link.startswith("http") else urljoin(response.url, link)
                )

                yield scrapy.Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        """解析每个新闻详情页的内容"""
        # 提取标题 - 从td.bt中提取文本内容
        title = response.css("td.bt::text").get()

        # 提取发布日期 - 精确定位到width="20%"的hui12_sj2元素
        publish_date_elem = response.xpath(
            '//tr[@align="right"]/td[@width="20%" and @class="hui12_sj2"]/text()'
        ).get()
        publish_date = publish_date_elem.strip() if publish_date_elem else None

        # 作者/来源 - 精确定位到width="22%"的td元素
        author_elem = response.xpath(
            '//tr[@align="right"]/td[@align="center" and @width="22%"]/text()'
        ).get()
        author = author_elem.strip() if author_elem else None

        data = {
            "title": title,
            "publish_date": publish_date,
            "author": author,
            "url": response.url,
        }
        self.data_list.append(data)  # 将数据添加到列表中
        yield data

    def closed(self, reason):
        # 在爬虫结束时将所有数据写入文件
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(self.data_list, f, ensure_ascii=False, indent=4)


```

将上述代码粘贴到前面生成的 newsspider.py文件中，然后使用如下命令即可运行爬虫。

确保路径如下：
在 项目的文件夹下运行：

```bash
scrapy crawl newsspider
```

### 结构化数据处理

scrapy 提供了一种机制让我们不必把所有操作都放在爬虫中，而是可以把任务分散到管道中。这需要通过定义 Scrapy Items 实现。

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
```

下面是我们完整的 newsspider.py

```python
import scrapy
from newscraper.items import NewsItem
from urllib.parse import urljoin


class newsspider(scrapy.Spider):
    name = "newsspider"
    allowed_domains = ["cas.cn"]
    start_urls = ["http://www.ciomp.cas.cn/xwdt/zhxw/"] + [
        f"http://www.ciomp.cas.cn/xwdt/zhxw/index_{i}.html" for i in range(1, 38)
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """解析新闻列表页"""
        # 处理所有新闻条目
        for item in response.css("a.font06"):
            link = item.css("::attr(href)").get()

            # 如果 link 是完整的 URL，则直接使用，否则拼接为完整 URL
            if link:
                detail_url = (
                    link if link.startswith("http") else urljoin(response.url, link)
                )

                yield scrapy.Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        """解析每个新闻详情页，仅提取原始数据，不进行处理"""
        # 创建NewsItem对象
        news_item = NewsItem()

        # 提取原始数据，不做任何清洗处理
        news_item["title"] = response.css("title::text").get()
        news_item["publish_date"] = response.xpath(
            '//tr[@align="right"]/td[@width="20%" and @class="hui12_sj2"]/text()'
        ).get()
        news_item["author"] = response.xpath(
            '//tr[@align="right"]/td[@align="center" and @width="22%"]/text()'
        ).get()
        news_item["url"] = response.url

        # 保存响应对象，以便在 pipeline 中使用
        news_item["response"] = response

        # 直接yield原始数据，让pipeline处理清洗和存储
        yield news_item

```

## 使用管道处理

Scrapy的管道系统是基于生成器(generator)设计的，每个管道组件接收 item 对象并返回处理后的结果或产生新的 item。这种设计使数据能够逐步流经多个处理阶段，实现数据清洗、验证、存储等功能。


### 数据清洗管道

NewsPipeline 负责清洗原始数据，去除多余空格、标准化日期格式，并添加爬取时间戳，确保数据质量和一致性。

```python
# 数据清洗管道示例 (pipelines.py)
class NewsPipeline:
    def process_item(self, item, spider):
        """处理每个抓取的新闻项"""
        adapter = ItemAdapter(item)

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
        adapter["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return item
```

### 数据持久化管道

#### SQLite 数据库存储

SQLitePipeline 实现数据的持久化存储，使用 open_spider() 在爬虫启动时初始化数据库连接，close_spider() 在爬虫结束时关闭连接，保证资源的正确释放。数据表使用 `url` 字段的 UNIQUE 约束防止重复插入。

```python
# SQLite 存储管道示例 (pipelines.py)
class SQLitePipeline:
    def __init__(self):
        # 数据库连接和游标
        self.conn = None
        self.cur = None
        
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
                adapter.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ),
        )
        self.conn.commit()

        return item
```

#### Excel 文件导出

ExcelPipeline 使用 openpyxl 库将抓取数据写入 Excel 表格，便于用户直接查看分析。`open_spider()` 方法创建工作簿和表头，`process_item()` 逐行添加数据，`close_spider()` 在爬虫结束时保存文件。

```python
# Excel 导出管道示例 (pipelines.py)
class ExcelPipeline:
    def __init__(self):
        self.workbook = None
        self.sheet = None
        self.file_name = "news.xlsx"
        self.current_row = 1  # Start from row 2 (after header)
        print("ExcelPipeline init")
        
    def open_spider(self, spider):
        """当爬虫启动时创建Excel文件"""
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "新闻数据"

        # 设置表头
        headers = ["标题", "发布日期", "作者/来源", "URL", "爬取时间"]
        for col_num, header in enumerate(headers, 1):
            self.sheet.cell(row=1, column=col_num).value = header
        
    def close_spider(self, spider):
        self.workbook.save(self.file_name)
        
    def process_item(self, item, spider):
        """将数据项添加到Excel文件"""
        adapter = ItemAdapter(item)
        self.current_row += 1

        # 添加数据到对应的列
        self.sheet.cell(row=self.current_row, column=1).value = adapter.get("title", "")
        self.sheet.cell(row=self.current_row, column=2).value = adapter.get(
            "publish_date", ""
        )
        self.sheet.cell(row=self.current_row, column=3).value = adapter.get(
            "author", ""
        )
        self.sheet.cell(row=self.current_row, column=4).value = adapter.get("url", "")
        self.sheet.cell(row=self.current_row, column=5).value = adapter.get(
            "created_at", ""
        )

        return item
```

### HTML 内容保存与处理

HtmlSavePipeline 不仅保存原始 HTML 内容，还会处理页面中的相对路径链接问题。通过 lxml 库解析 HTML 结构，将 img、a、link、script 等标签的相对路径转换为绝对路径，确保离线浏览时资源引用正确。同时实现了智能文件命名和异常处理。

```python
# HTML 内容保存管道示例 (pipelines.py)
class HtmlSavePipeline:
    def __init__(self):
        # 创建保存目录
        self.output_dir = "html_files"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def process_item(self, item, spider):
        """保存 HTML 并将相对路径转换为绝对路径"""
        adapter = ItemAdapter(item)
            
        response = adapter["response"]
        url = response.url
        
        try:
            # 解析 HTML
            doc = lxml.html.fromstring(response.text)
            
            # 转换 img 标签的 src
            for img in doc.xpath('//img'):
                src = img.get('src')
                if src and not src.startswith(('http://', 'https://', '//')):
                    img.set('src', urljoin(url, src))
            
            # 转换 a 标签的 href
            for a in doc.xpath('//a'):
                href = a.get('href')
                if href and not href.startswith(('http://', 'https://', '//', '#', 'javascript:')):
                    a.set('href', urljoin(url, href))
            
            # 转换 link 标签的 href
            for link in doc.xpath('//link'):
                href = link.get('href')
                if href and not href.startswith(('http://', 'https://', '//')):
                    link.set('href', urljoin(url, href))
            
            # 转换 script 标签的 src
            for script in doc.xpath('//script'):
                src = script.get('src')
                if src and not src.startswith(('http://', 'https://', '//')):
                    script.set('src', urljoin(url, src))
            
            # 获取修改后的 HTML
            html_content = lxml.html.tostring(doc, encoding='unicode', method='html')
            
            # 生成文件名 (使用标题或 URL 中的一部分)
            title = adapter.get('title', '')
            if not title:
                # 从 URL 创建文件名
                title = url.split('/')[-1].split('.')[0]
            
            # 清理文件名中的非法字符
            filename = re.sub(r'[\\/*?:"<>|]', "_", title)
            filename = filename[:100]  # 限制文件名长度
            
            # 保存 HTML 文件
            file_path = os.path.join(self.output_dir, f"{filename}.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 将保存路径添加到 item 中
            adapter['html_saved_path'] = file_path
            
        except Exception as e:
            spider.logger.error(f"保存 HTML 时发生错误: {e}")
            
        return item
```

### 管道运行流程说明

当 Scrapy 爬虫运行时，每个提取的 Item 会依次通过所有启用的管道：

1. 首先通过 NewsPipeline 进行数据清洗
2. 然后经由 SQLitePipeline 保存到数据库
3. 接着被 ExcelPipeline 写入 Excel 文件
4. 最后由 HtmlSavePipeline 保存 HTML 内容

这种链式处理方式实现了数据抓取、清洗和存储的完整流程，每个管道专注于特定任务，实现了关注点分离和代码复用。

### 管道配置详解

在 Scrapy 中，管道的配置主要通过 `settings.py` 文件中的 `ITEM_PIPELINES` 字典实现。这个字典指定了哪些管道会被启用，以及它们的处理顺序。

```python
# settings.py 中的管道配置示例
ITEM_PIPELINES = {
   'tutorial.pipelines.NewsPipeline': 300,      # 数据清洗管道
   'tutorial.pipelines.HtmlSavePipeline': 10,   # HTML保存管道
   'tutorial.pipelines.ExcelPipeline': 500,     # Excel导出管道
   'tutorial.pipelines.SQLitePipeline': 800,    # 数据库存储管道
}
```

#### 配置说明：

1. **字典键**：是管道类的完整 Python 路径（模块.类名）
2. **字典值**：是一个整数，表示处理优先级
   - 数值越小，优先级越高，管道越先执行
   - 数值范围通常在 0-1000 之间

#### 管道执行顺序

根据上面的配置，管道处理顺序如下：
1. `HtmlSavePipeline` (10) - 最优先执行，保存原始 HTML
2. `NewsPipeline` (300) - 其次执行，对数据进行清洗
3. `ExcelPipeline` (500) - 然后执行，将数据导出到 Excel
4. `SQLitePipeline` (800) - 最后执行，将数据存入数据库

## 第二阶段的成果

```python
from itemadapter import ItemAdapter

import sqlite3
from datetime import datetime
from openpyxl import Workbook
import lxml.html
from urllib.parse import urljoin
import re
import os

class NewsPipeline:
    def process_item(self, item, spider):
        """处理每个抓取的新闻项"""
        adapter = ItemAdapter(item)

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
        adapter["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return item


class SQLitePipeline:
    def __init__(self):
        # 数据库连接和游标
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        """当爬虫启动时创建数据库连接"""
        self.conn = sqlite3.connect("news.db")
        self.cur = self.conn.cursor()

        # 创建表（如果不存在）·
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
                adapter.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ),
        )
        self.conn.commit()

        return item


class ExcelPipeline:
    def __init__(self):
        self.workbook = None
        self.sheet = None
        self.file_name = "news.xlsx"
        self.current_row = 1  # Start from row 2 (after header)
        print("ExcelPipeline init")

    def open_spider(self, spider):
        """当爬虫启动时创建Excel文件"""
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "新闻数据"

        # 设置表头
        headers = ["标题", "发布日期", "作者/来源", "URL", "爬取时间"]
        for col_num, header in enumerate(headers, 1):
            self.sheet.cell(row=1, column=col_num).value = header

    def close_spider(self, spider):
        self.workbook.save(self.file_name)

    def process_item(self, item, spider):
        """将数据项添加到Excel文件"""
        adapter = ItemAdapter(item)
        self.current_row += 1

        # 添加数据到对应的列
        self.sheet.cell(row=self.current_row, column=1).value = adapter.get("title", "")
        self.sheet.cell(row=self.current_row, column=2).value = adapter.get(
            "publish_date", ""
        )
        self.sheet.cell(row=self.current_row, column=3).value = adapter.get(
            "author", ""
        )
        self.sheet.cell(row=self.current_row, column=4).value = adapter.get("url", "")
        self.sheet.cell(row=self.current_row, column=5).value = adapter.get(
            "created_at", ""
        )

        return item



class HtmlSavePipeline:
    def __init__(self):
        # 创建保存目录
        self.output_dir = "html_files"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def process_item(self, item, spider):
        """保存 HTML 并将相对路径转换为绝对路径"""
        adapter = ItemAdapter(item)
            
        response = adapter["response"]
        url = response.url
        
        try:
            # 解析 HTML
            doc = lxml.html.fromstring(response.text)
            
            # 转换 img 标签的 src
            for img in doc.xpath('//img'):
                src = img.get('src')
                if src and not src.startswith(('http://', 'https://', '//')):
                    img.set('src', urljoin(url, src))
            
            # 转换 a 标签的 href
            for a in doc.xpath('//a'):
                href = a.get('href')
                if href and not href.startswith(('http://', 'https://', '//', '#', 'javascript:')):
                    a.set('href', urljoin(url, href))
            
            # 转换 link 标签的 href
            for link in doc.xpath('//link'):
                href = link.get('href')
                if href and not href.startswith(('http://', 'https://', '//')):
                    link.set('href', urljoin(url, href))
            
            # 转换 script 标签的 src
            for script in doc.xpath('//script'):
                src = script.get('src')
                if src and not src.startswith(('http://', 'https://', '//')):
                    script.set('src', urljoin(url, src))
            
            # 获取修改后的 HTML
            html_content = lxml.html.tostring(doc, encoding='unicode', method='html')
            
            # 生成文件名 (使用标题或 URL 中的一部分)
            title = adapter.get('title', '')
            if not title:
                # 从 URL 创建文件名
                title = url.split('/')[-1].split('.')[0]
            
            # 清理文件名中的非法字符
            filename = re.sub(r'[\\/*?:"<>|]', "_", title)
            filename = filename[:100]  # 限制文件名长度
            
            # 保存 HTML 文件
            file_path = os.path.join(self.output_dir, f"{filename}.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 将保存路径添加到 item 中
            adapter['html_saved_path'] = file_path
            
        except Exception as e:
            spider.logger.error(f"保存 HTML 时发生错误: {e}")
            
        return item
```


