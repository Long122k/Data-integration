
import scrapy

class HoangHaSpider(scrapy.Spider):
  name = 'HoangHa'
  allowed_domains = ['hoanghamobile.com']
  start_urls = [
    'https://hoanghamobile.com/dien-thoai-di-dong/iphone',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/samsung',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/xiaomi',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/oppo',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/nokia',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/realme',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/vivo',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/masstel',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/xor',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/philips',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/bphone',
    # 'https://hoanghamobile.com/dien-thoai-di-dong/tecno'
  ]
  root_url = 'https://hoanghamobile.com'

  def parse(self, response):
    phone_urls = response.xpath('//div[@class="item"]/div[@class="img"]/a/@href').getall()

    phone_urls = list(map(lambda phone_url: self.root_url + phone_url, phone_urls))

    # for phone_url in phone_urls:
    #   yield scrapy.Request(phone_url, self.parse_phone)

    yield scrapy.Request(phone_urls[0], self.parse_option)


  def parse_option(self, response):


    pass

  def parse_phone(self, response):
    phoneItem = {}

    phoneItem['images_intro'] = set(response.xpath('//div[@data-u="slides"]/div/div[1]/img/@src').getall())
    phoneItem['type'] = response.xpath('//div[contains(@class,"box03")][1]/a[contains(@class,"act")]/text()').get()
    # phoneItem['price'] = response.xpath('//p[@class="box-price-present"]/text()').get()
    # phoneItem['title'] = response.xpath('//h1/text()').get()
    # phoneItem['hot_line'] = '1800.1060'
    # phoneItem['link_source'] = response.url
    # phoneItem['point'] = response.xpath('//p[@class="point"]/text()').get(),
    # phoneItem['rating_total'] = response.xpath('//a[@class="rating-total"]/text()').get(),
    # phoneItem['star_percent_list'] = response.xpath('//a[@class="number-percent"]/text()').getall(),
    # phoneItem['branch'] = response.xpath('//ul[@class="breadcrumb"]/li[last()]/a/text()').get()
    #
    # table_info = response.xpath('//div[@class="parameter"]/ul/li').getall(),
    # table_info = table_info[0]
    #
    # def getText(s):
    #   s = s.split('<')[0]
    #   s = s.replace('"', '')
    #   s = s.replace("'", '')
    #   s = s.replace(":", '')
    #   return s
    #
    # for info in table_info:
    #   info = info.split('>')
    #   info = list(filter(lambda x: '</' in x and '\n' not in x, info))
    #   info = list(map(getText, info))
    #   title = info[0]
    #   detail = ', '.join(info[1:])
    #   phoneItem[title] = detail
    #
    # phoneItem['Màu sắc'] = response.xpath('//div[contains(@class,"color")]/a/text()').getall()
    print(phoneItem)

    pass
