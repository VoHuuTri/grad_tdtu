import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
from lxml import etree

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


class GD_DT_Spider(CrawlSpider):
    def __init__(self, my_param=None, *args, **kwargs):
        super(GD_DT_Spider, self).__init__(*args, **kwargs)
        self.my_param = my_param
        self.start_urls = [f'https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=BGD%C4%90T&area=0&match=True&type=0&status=0&signer=0&sort=1&lan=1&scan=0&org=0&fields=&page={my_param}']

    name = "gddt"
    allowed_domains = ["thuvienphapluat.vn"]
    # start_urls = ["https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=BGD%C4%90T&area=0&match=True&type=0&status=0&signer=0&sort=1&lan=1&scan=0&org=0&fields=&page=1"]
    rules = [Rule(LinkExtractor(allow = ("/van-ban/Giao-duc")), callback='parse', follow = True)]
    custom_settings = {
        'DOWNLOAD_DELAY': 3,  # Set the delay to 5 seconds between requests
    }
    titles = []

    def parse(self, response):
        if "BGDDT" in response.url:
            soup = BeautifulSoup(response.body, 'html.parser')
            title = response.css('title ::text').get()
            title = title.strip()

            content = response.xpath('//*[@id="divContentDoc"]/div[2]/div/div')
            
            soup = BeautifulSoup(content.get(), 'html.parser')
            p_tags = soup.find_all(lambda tag: tag.name == 'p' and tag.find_parent('table') is None)
            dieus = []
            tag = ""
            end_of_dieu = True
            for i in range(len(p_tags)):
                if p_tags[i].get('align') == 'center':
                    end_of_dieu = True
                if p_tags[i].get('align') == 'center':
                    tag = p_tags[i].text
                elif p_tags[i].text.startswith("Điều ") and p_tags[i].text[5].isdigit():
                    end_of_dieu = False
                    dieus.append([p_tags[i].text.replace('\r\n',' '), tag])
                elif len(dieus) > 0 and p_tags[i].get('align') != 'center' and not p_tags[i].text.startswith("Chương ") and not end_of_dieu:
                    dieus[-1][0] += " "+p_tags[i].text.replace('\r\n',' ')

            time = soup.find(lambda tag: tag.name == 'i' and tag.find_parent('table') is not None)
            time = time.text.replace("\n", "").replace("\t", "").replace("\r", "").strip()

            if dieus != None and len(dieus) > 0 and title != None and len(title) > 0 and title != " " and time != None and len(time) > 0 and time != " " and "BGDDT" in response.url and title not in self.titles:
                with open("data_gddt.jsonl", "a", encoding="utf-8") as f:
                    for i in dieus:
                        if len(i[0]) < 20000:
                            json.dump({"data":i[0], "meta_data":{"source":title, "tag":i[1], "url":response.url, "time":time}}, f, ensure_ascii=False)
                            f.write("\n")
                self.titles.append(title)



        
