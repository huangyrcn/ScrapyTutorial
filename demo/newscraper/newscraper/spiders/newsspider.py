
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