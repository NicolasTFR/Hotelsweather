
import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import datetime

search=os.environ["listdestination"]
now = datetime.date.today()
futur= now+datetime.timedelta(days=2)

class bookingmain(scrapy.Spider):


    name = "bookingmain"
    allowed_domains = ["booking.com"]
    start_urls = ['https://www.booking.com/index.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaE2IAQGYAQm4ARfIAQzYAQPoAQGIAgGoAgO4AteltJMGwAIB0gIkNWRiMWNlNDItZTlkNy00NTM2LThiYmMtMWNhMjY2NGE2YzVm2AIE4AIB;sid=28e22a10d86fc4b6c0b24407c1eb7e29;keep_landing=1&sb_price_type=total&']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formname='hero-banner-searchbox',
            formdata={"lang":"fr", "dest_type":"city","ssne":search,"ssne_untouched":search,"ss":search,"checkout":str(futur),"checkin":str(now)},
            callback=self.after_search
        )


    # Callback used after login
    def after_search(self, response):
        listhotels=response.xpath('//*[@id="search_results_table"]/div/div/div/div/div[6]/div')
        for hotels in listhotels:
            yield {
                 "name" : hotels.xpath('div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/div[1]/text()').get(),
                 "url" : hotels.xpath("div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/@href").get(),
                 "Rating": hotels.xpath("div[1]/div[2]/div/div[1]/div[2]/div/a/span/div/div[1]/text()").get(),
            }

           
# Name of the file where the results will be saved
filename = f"results\{search}_main.json"

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir():
    os.remove(filename)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {filename: {"format": "json"}}
})

# Start the crawling using the spider you defined above
process.crawl(bookingmain)
process.start()

