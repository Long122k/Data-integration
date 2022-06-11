
import scrapy
from crawler.items import TGDDItem

class TGDDSpider(scrapy.Spider):
    name = 'TGDD'
    allowed_domains = ['www.thegioididong.com']
    start_urls = ['https://www.thegioididong.com/dtdd/oppo-reno7-z?code=0131491003039']

    def parse(self, response):
        phoneItem = TGDDItem()

        phoneItem['images_intro'] = response.xpath('//a[@class="slider-item "]/img/@data-src').getall()
        phoneItem['price'] = response.xpath('//p[@class="box-price-present"]/text()').get()
        phoneItem['title'] = response.xpath('//h1/text()').get()
        phoneItem['hot_line'] = '1800.1060'
        phoneItem['link_source'] = response.url
        phoneItem['rating'] = {
            'point': response.xpath('//p[@class="point"]/text()').get(),
            'rating_total': response.xpath('//a[@class="rating-total"]/text()').get(),
            'star_percent_list': response.xpath('//a[@class="number-percent"]/text()').getall(),
        },
        phoneItem['branch'] = response.xpath('//ul[@class="breadcrumb"]/li[last()]/a/text()').get()

        table_info = response.xpath('//div[@class="parameter"]/ul/li').getall(),
        table_info = table_info[0]

        def getText(s):
            s = s.split('<')[0]
            s = s.replace('"', '')
            s = s.replace("'", '')
            s = s.replace(":", '')
            return s

        phone_infors = {}
        for info in table_info:
            info = info.split('>')
            info = list(filter(lambda x: '</' in x and '\n' not in x, info))
            info = list(map(getText, info))
            title = info[0]
            detail = ', '.join(info[1:])
            phone_infors[title] = detail

        phoneItem['informations'] = phone_infors
        phoneItem['informations']['Màu sắc'] = response.xpath('//div[contains(@class,"color")]/a[contains(@class,"act")]/text()').get()
        print(phoneItem)
        yield phoneItem
