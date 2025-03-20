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

start_urls = ["http://www.ciomp.cas.cn/xwdt/zhxw/"] + [
  
    f"http://www.ciomp.cas.cn/xwdt/zhxw/index_{i}.html" for i in range(1, 38)
  
]

<!-- 说明 -->
此方案通过观察目标网站分页 URL 的固定规律实现自动构造各分页 URL。由于网页在禁用 JavaScript 后还保留分页链接，因此可以根据已知 URL 模板，利用页码递增来生成所有页面的完整 URL。这种方法简单高效，适用于页面 URL 格式一致、无需浏览器渲染的场景。

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

Scrapy的管道系统是基于生成器(generator)设计的，每个管道组件接收 item 对象并返回处理后的结果或产生新的 item。这种设计使数据能够逐步流经多个处理阶段，实现数据清洗、验证、存储等功能。

在 settings.py 中通过 `ITEM_PIPELINES` 配置管道处理顺序，数字越小优先级越高：

```python
ITEM_PIPELINES = {
    'tutorial.pipelines.NewsPipeline': 300,
    'tutorial.pipelines.SQLitePipeline': 400,
    'tutorial.pipelines.ExcelPipeline': 500,
    'tutorial.pipelines.HtmlSavePipeline': 600,
}
```

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

#### 配置最佳实践

* **考虑数据依赖关系**：某些管道可能依赖其他管道的处理结果，应确保它们按正确顺序执行
* **资源高效利用**：需要打开/关闭外部资源（如文件、数据库连接）的管道应合理安排顺序
* **错误处理考虑**：可能引发错误的管道（如网络请求、文件操作）应考虑在何处执行更合适

#### 动态启用和禁用管道

可以在爬虫运行时通过命令行参数动态控制管道配置：

```bash
# 禁用某个管道
scrapy crawl newspider -s ITEM_PIPELINES='{"tutorial.pipelines.SQLitePipeline": None}'

# 临时启用某个管道或修改优先级
scrapy crawl newspider -s ITEM_PIPELINES='{"tutorial.pipelines.CustomPipeline": 100}'
```

这种灵活的配置机制使 Scrapy 能够适应不同的数据处理需求，实现可插拔的数据处理流程。