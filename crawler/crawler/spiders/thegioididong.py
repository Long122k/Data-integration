
import scrapy
from crawler.items import TGDDItem

class TGDDSpider(scrapy.Spider):
    name = 'TGDD'
    allowed_domains = ['www.thegioididong.com']
    start_urls = ['https://www.thegioididong.com/dtdd']
    root_url = 'https://www.thegioididong.com'

    def parse(self, response):
        branchs = response.xpath('//div[@class="lst-quickfilter q-manu "]/a/@href').getall()

        branchs_url = []
        for branch in branchs:
            branchs_url.append(self.root_url + '/' + branch)

        for branch_url in branchs_url:
            yield scrapy.Request(branch_url, callback=self.parse_branch)
        # yield scrapy.Request('https://www.thegioididong.com/dtdd-itel', callback=self.parse_branch)

    def parse_branch(self, response):
        print(response.url)
        list_phones = response.xpath('//ul[@class="listproduct"]/li/a[1]/@href').getall()

        list_phones = list(map(lambda phone_url: self.root_url + phone_url, list_phones))

        for phone_url in list_phones:
            yield scrapy.Request(phone_url, callback=self.parse_type)

        # yield scrapy.Request('https://www.thegioididong.com/dtdd/itel-l6502?src=osp', callback=self.parse_type)

    def parse_type(self, response):
        types_url = response.xpath('//div[@class="box03 group desk"]/a/@href').getall()
        print(types_url)
        if len(types_url) > 0:
            types_url = list(map(lambda type_url: self.root_url + type_url, types_url))
            for type_url in types_url:
                yield scrapy.Request(type_url, callback=self.parse_phone, dont_filter = True)
        else:
            yield scrapy.Request(response.url, callback=self.parse_phone, dont_filter = True)

        # yield scrapy.Request('https://www.thegioididong.com/dtdd/itel-l6502?src=osp', callback=self.parse_phone, dont_filter = True)

    def parse_phone(self, response):
        phoneItem = {}

        phoneItem['images_intro'] = response.xpath('//a[@class="slider-item "]/img/@data-src').getall()
        phoneItem['type'] = response.xpath('//div[contains(@class,"box03")][1]/a[contains(@class,"act")]/text()').get()
        phoneItem['price'] = response.xpath('//p[@class="box-price-present"]/text()').get()
        phoneItem['title'] = response.xpath('//h1/text()').get()
        phoneItem['hot_line'] = '1800.1060'
        phoneItem['link_source'] = response.url
        phoneItem['point'] = response.xpath('//p[@class="point"]/text()').get(),
        phoneItem['rating_total'] = response.xpath('//a[@class="rating-total"]/text()').get(),
        phoneItem['star_percent_list'] = response.xpath('//a[@class="number-percent"]/text()').getall(),
        phoneItem['branch'] = response.xpath('//ul[@class="breadcrumb"]/li[last()]/a/text()').get()

        table_info = response.xpath('//div[@class="parameter"]/ul/li').getall(),
        table_info = table_info[0]

        def getText(s):
            s = s.split('<')[0]
            s = s.replace('"', '')
            s = s.replace("'", '')
            s = s.replace(":", '')
            return s

        for info in table_info:
            info = info.split('>')
            info = list(filter(lambda x: '</' in x and '\n' not in x, info))
            info = list(map(getText, info))
            title = info[0]
            detail = ', '.join(info[1:])
            phoneItem[title] = detail

        phoneItem['Màu sắc'] = response.xpath('//div[contains(@class,"color")]/a/text()').getall()
        print(phoneItem)

        yield phoneItem
