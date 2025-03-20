import scrapy
import urljoin


class InfospiderSpider(scrapy.Spider):
    name = "infospider"
    allowed_domains = ["www.ciomp.cas.cn"]
    start_urls = ["http://www.ciomp.cas.cn/xwdt/zhxw/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # 处理所有目标项
        for item in response.css("a.font06"):
            link = item.css("::attr(href)").get()
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

        yield {
            "title": title,
            "publish_date": publish_date,
            "author": author,
            "url": response.url,
        }
