import scrapy


class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    
    start_urls = ["https://itclinical.com/it.php"] # URL inicial

    def parse(self, response):
        pass
