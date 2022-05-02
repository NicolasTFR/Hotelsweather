
import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import json


class bookingindividual(scrapy.Spider):
    # Name of your spider
    name = "bookingindividual"
    allowed_domains = ["booking.com"]

    with open(os.environ["files"]) as json_file:
        datatest = json.load(json_file)
    listurl=[]
    for hotels in datatest:
        listurl.append(hotels["url"])

    # Starting URL
    start_urls = listurl

    # Parse function for form request
    def parse(self, response):
        descript=[]
        descriptpath=response.xpath('//*[@id="property_description_content"]/p')
        for path in descriptpath:
            descript.append(path.xpath('text()').get())

        return { "url" : response.url,
                 "description" : descript,             
                 "bbox": response.xpath('//*[@id="showMap2"]/span[1]/@data-bbox').get() ,
                 "Destination": os.environ["files"].split("_main")[0].split('\\')[-1]     
            }

           
# Name of the file where the results will be saved
filename = "resultsdetailed/{}_detailed.json".format(os.environ["files"].split("_main")[0].split('\\')[-1])


file_path = "./resultsdetailed/{}_detailed.json".format(os.environ["files"].split("_main")[0].split('\\')[-1])
if os.path.exists(file_path):
    os.remove(file_path)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {filename: {"format": "json"}}
})

# Start the crawling using the spider you defined above
process.crawl(bookingindividual)
process.start()

