
import scrapy

class HoangHaSpider(scrapy.Spider):
  name = 'HoangHa'
  allowed_domains = ['hoanghamobile.com']
  start_urls = [
    'https://hoanghamobile.com/dien-thoai-di-dong/iphone',
    'https://hoanghamobile.com/dien-thoai-di-dong/samsung',
    'https://hoanghamobile.com/dien-thoai-di-dong/xiaomi',
    'https://hoanghamobile.com/dien-thoai-di-dong/oppo',
    'https://hoanghamobile.com/dien-thoai-di-dong/nokia',
    'https://hoanghamobile.com/dien-thoai-di-dong/realme',
    'https://hoanghamobile.com/dien-thoai-di-dong/vivo',
    'https://hoanghamobile.com/dien-thoai-di-dong/masstel',
    'https://hoanghamobile.com/dien-thoai-di-dong/xor',
    'https://hoanghamobile.com/dien-thoai-di-dong/philips',
    'https://hoanghamobile.com/dien-thoai-di-dong/bphone',
    'https://hoanghamobile.com/dien-thoai-di-dong/tecno'
  ]
  root_url = 'https://hoanghamobile.com'

  def parse(self, response):
    phone_urls = response.xpath('//div[@class="item"]/div[@class="img"]/a/@href').getall()

    phone_urls = list(map(lambda phone_url: self.root_url + phone_url, phone_urls))

    for phone_url in phone_urls:
      yield scrapy.Request(phone_url, self.parse_phone)

    # yield scrapy.Request(phone_urls[0], self.parse_option)


  def parse_option(self, response):
    option_urls = response.xpath('//div[@id="versionOption"]/div/a/@href').getall()

    if len(option_urls) > 0:
      option_urls = list(map(lambda option_url: self.root_url + option_url, option_urls))

      for option_url in option_urls:
        yield scrapy.Request(option_url, callback=self.parse_phone)
    else:
      yield scrapy.Request(response.url, callback=self.parse_phone)

    # yield scrapy.Request(option_urls[0], callback=self.parse_phone, dont_filter = True)

  def parse_phone(self, response):
    phoneItem = {}

    def cleanText(s):
      s = s.replace('"', '')
      s = s.replace("'", '')
      s = s.replace(":", '')
      s = s.replace("\n", '')
      s = s.replace("\t", '')
      s = s.replace("\r", '')
      s = s.replace("(", '')
      s = s.replace(")", '')
      s = s.strip()
      return s

    phoneItem['images_intro'] = set(response.xpath('//div[@data-u="slides"]/div/div[1]/img/@src').getall())
    phoneItem['option'] = response.xpath('//div[@id="versionOption"]/div[contains(@class,"selected")]/a/span/label/strong/text()').get()
    phoneItem['price'] = cleanText(response.xpath('//p[contains(@class,"price")]/strong/text()').get())
    phoneItem['title'] = cleanText(response.xpath('//h1[1]/text()').get())
    phoneItem['hot_line'] = '1900.2091'
    phoneItem['link_source'] = response.url
    rating = response.xpath('//div[@class="stats"]/span/text()').get()
    phoneItem['point'] = cleanText(rating.split('/')[0]),
    phoneItem['rating_total'] = cleanText(rating.split('/')[1]),
    # phoneItem['star_percent_list'] = response.xpath('//a[@class="number-percent"]/text()').getall(),
    phoneItem['branch'] = response.xpath('//ol[@class="breadcrumb"]/li[3]/a/span/text()').get()

    table_info = response.xpath('//div[@class="specs-special"]/ol/li').getall(),
    table_info = table_info[0]
    table_info = list(map(cleanText, table_info))

    for info in table_info:
      title, detail = info.split('</strong>')
      title = title.split('<strong>')[1]
      detail = detail.split('</span>')[0]
      detail = detail.split('<span>')[1]
      phoneItem[title] = detail

    phoneItem['color'] = response.xpath('//div[@id="colorOptions"]/div/span/label/strong/text()').getall()

    yield phoneItem
