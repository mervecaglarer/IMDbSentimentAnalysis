import os
import scrapy
from scrapy.crawler import CrawlerProcess

file = open("tmp/links.csv","w")
file.close()

class SearcherSpider(scrapy.Spider):
    movie_name = input("Enter your movie name: ")
    #name of the spider
    name = 'links'

    #list of allowed domains
    allowed_domains = ['www.imdb.com']

    #starting url for scraping
    reqLink = 'https://www.imdb.com/find?s=tt&q=' + movie_name + '&ref_=nv_sr_sm'
    start_urls = [reqLink]

    #setting the location of the output csv file
    custom_settings = {
        'FEED_URI' : 'tmp/links.csv'
    }
    def parse(self, response):
        global link
        print("procesing:" + response.url)
        
        #Extract article information
        links = response.xpath('//*[@class="result_text"]/a/@href').getall()
        #link="https://www.imdb.com"+str(links[0])
        link = links[0].split('/')
        link = "https://www.imdb.com/" + str(link[1]) + "/" + link[2] + "/" + "reviews?spoiler=hide"
        yield {'Link':link}

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.104'
})

process.crawl(SearcherSpider)
process.start()
process.stop()