# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class NewsItem(scrapy.Item):
    """定义新闻文章的数据结构"""
    title = scrapy.Field()          # 新闻标题
    publish_date = scrapy.Field()   # 发布日期
    author = scrapy.Field()         # 作者/来源
    url = scrapy.Field()            # 文章URL
    created_at = scrapy.Field()     # 爬取时间
    response = scrapy.Field()       # 响应对象
    html_saved_path = scrapy.Field()  # 保存HTML文件路径