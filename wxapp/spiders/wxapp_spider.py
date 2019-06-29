# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem


class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = ( #url匹配规则
        # allow 域名
        # callback 回调函数 (如果我们只是要这个页面的url，scrapy会自动匹配，就不用写函数处理了)
        # follow 跟进（当前页面信息中还有符合这个规则的，就跟进爬取）
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='ph']/text()").get()
        author_p = response.xpath("//p[@class='authors']")
        author = author_p.xpath(".//span/text()").get()
        pub_time = author_p.xpath("./span/text()").get()
        article_content = response.xpath("//td[@id='article_content']//text()").getall()
        content = "".join(article_content).strip()
        item = WxappItem(title = title, author = author, pub_time = pub_time, content = content)
        yield item