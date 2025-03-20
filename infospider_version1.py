import scrapy


class InfospiderSpider(scrapy.Spider):
    name = "infospider"
    allowed_domains = ["www.ciomp.cas.cn"]
    start_urls = ["http://www.ciomp.cas.cn/xwdt/zhxw/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        print("Request URL:", response.url)
        # 处理所有目标项
        for item in response.css("a.font06"):
            link = item.css("::attr(href)").get()
            print(link)
            yield {"link": link}
        # 拼接并请求下一页
        # 通过 XPath 提取文本为“下一页”的链接地址
        next_page = response.xpath('//a[text()="下一页"]/@href').get()
        # 如果存在，将基地址与提取的 href 拼接成完整 URL
        print("下一页Next page:", next_page)
        if next_page:
            next_page_url = "http://www.ciomp.cas.cn/xwdt/zhxw/" + next_page
            print("Next page URL:", next_page_url)
