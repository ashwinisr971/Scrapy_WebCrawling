# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazoncrawlerItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = ['https://www.amazon.in/s?k=books&ref=nb_sb_noss']

    def parse(self, response):
        
        items=AmazoncrawlerItem()

        product_name=response.css('.a-size-medium').css('::text').extract()
        product_author=response.css('.a-color-secondary .a-link-normal').css('::text').extract()
        product_price=response.css('.a-spacing-top-small .a-price-whole , .index\=1 .a-color-secondary .a-link-normal').css('::text').extract()
        product_imagelink=response.css('.s-image , .index\=1 .a-color-secondary .a-link-normal').css('::attr(src)').extract()

        items['product_name']=product_name
        items['product_author']=product_author
        items['product_price']=product_price
        items['product_imagelink']=product_imagelink
        yield items


        
