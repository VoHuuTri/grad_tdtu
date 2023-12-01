import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json

class GradSpider(CrawlSpider):
    name = "grad"
    allowed_domains = ["grad.tdtu.edu.vn"]
    start_urls = ["https://grad.tdtu.edu.vn/"]
    rules = [Rule(LinkExtractor(allow='grad.tdtu.edu.vn', deny = '/en'), callback='parse', follow = True)]

    def parse(self, response):
        #  get title content in h1 tag with class = "post-title"
        # title = soup.select_one("h1.post-title")
        # soup = BeautifulSoup(response.body, 'html.parser')
        title = response.xpath('//*[@id="block-gavias-edubiz-content"]/div/article/div/div[2]')
        title = title.css('h1.post-title ::text').get()

        content = response.xpath('//*[@id="block-gavias-edubiz-content"]/div/article/div/div[2]/div[2]/div[2]')
        content = content.css('p ::text').getall()
        content = " ".join(content)

        time = response.xpath('//*[@id="block-gavias-edubiz-content"]/div/article/div/div[2]/div[1]')
        time = time.css('span.post-created ::text').get()
        if(title != None and len(title) > 0 and title != " " and content != None and len(content) > 0 and content != " " and time != None and len(time) > 0 and time != " "):

            
            with open("data.jsonl", "a", encoding="utf-8") as f:
                json.dump({"data":{"title": title, "url":response.url, "content": content}, "meta_data":{"school":time[:4], "time":time[6:]}}, f, ensure_ascii=False)
                f.write("\n")

