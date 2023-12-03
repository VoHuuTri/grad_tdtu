import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
from lxml import html
from lxml.etree import tostring


with open("html.txt", "r", encoding="utf-8") as f:
    html_content = f.read()

tree = html.fromstring(html_content)

elements = tree.xpath('//*[@id="divContentDoc"]/div[2]/div/div')
content = ""
for element in elements:
    content  += tostring(element, encoding='unicode') + "\n"

soup = BeautifulSoup(content, 'html.parser')

p_tags = soup.find_all(lambda tag: tag.name == 'p' and tag.find_parent('table') is None)
no = 1
dieus = []
tag = ""
for i in range(len(p_tags)):
    
    if p_tags[i].text == "QUYẾT ĐỊNH:" or p_tags[i].text == "ĐIỀU LỆ":
        no = 1
        tag = p_tags[i].text
    elif p_tags[i].text.startswith("Điều "+str(no)+"."):
        if len(dieus) > 0:
            dieus[-1] = tag + " " + dieus[-1]
        dieus.append(p_tags[i].text)
        no += 1
    elif len(dieus) > 0 and p_tags[i].get('align') != 'center' and not p_tags[i].text.startswith("Chương "):
        dieus[-1] += " "+p_tags[i].text

    
time = soup.find(lambda tag: tag.name == 'i' and tag.find_parent('table') is not None)
print(time.text.replace("\n", "").replace("\t", "").replace("\r", "").strip())