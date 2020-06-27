import json 
import scrapy
from scrapy.crawler import CrawlerProcess

file = open("tmp/comments.csv","w")
file.close()
file = open("tmp/links.csv","r")
link = file.readline()
link = link[:-1]
link = json.loads(link)
link = link['Link']
class CommentSpider(scrapy.Spider):
    #name of the spider
    name = 'comments'

    #list of allowed domains
    allowed_domains = ['www.imdb.com']

    #starting url for scraping
    start_urls = [link]

    #setting the location of the output csv file
    custom_settings = {
        'FEED_URI' : 'tmp/comments.csv'
    }

    def parse(self, response):
        print("procesing:" + response.url)
        comments = response.xpath('//*[@id="main"]/section/div[2]/div[2]/div/div[1]/div[1]/div[3]/div[1]').getall()
        idx = 0
        for comment in comments:
            idx+=1
            comment = comment.replace('<br>', '')
            comment = comment.replace('<div class="text show-more__control">', '')
            comment = comment.replace('</div>', '')
            yield {idx : comment}


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.104'
})

process.crawl(CommentSpider)
process.start()
process.stop()