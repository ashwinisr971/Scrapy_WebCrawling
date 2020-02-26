import scrapy
from scrapy import FormRequest
from ..items import QuotescrapperItem
#Once the fileds are declared in items.py import the required class in the main file

class QuoteSpider(scrapy.Spider):
    #name of the spider
    name='quotes' 
    
    #Urls to crawl
    start_urls=[
        'http://quotes.toscrape.com/login'
    ]

    def parse(self,response):
        token=response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response,formdata={
            'csrf_token':token,
            'username':'ashwinisr@gmail.com',
            'password':'12345'
        },callback=self.start_scrapping) 

    def start_scrapping(self,response):
        #instance of QuotescrapperItem class
        items=QuotescrapperItem()

        #response contains the sourcecode of the url
        all_div_quotes=response.css('div.quote')

        for quotes in all_div_quotes:
            title=quotes.css('span.text::text').extract()
            author=quotes.css('.author::text').extract()
            tag=quotes.css('.tag::text').extract()
            #extract() returns a list
            #use extract_first() to avoid error when there is no element and get the first element
            #Extracted data->Temporary Containers(items)->Storing in database
            #stroring the results in the item's field
            items['title']=title
            items['author']=author
            items['tag']=tag
            
            #Use command scrapy crawl spidername -o items.json to dump the data in json file
            #for csv -o items.csv, for xml -o items.xml

            # if you want to store the data in a database then,
            #Scarppeed data-> Item Containers-> Pipeline-> SQL/Mongodb
            yield items

        next_page=response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page,callback=self.start_scrapping)