

import scrapy
import re

class DiDongViet(scrapy.Spider):
  name = 'DiDongViet'
  start_urls = ['https://didongviet.vn/dien-thoai']

  def parse(self, response):
    branch_urls = response.xpath('//div[@class="list-child-scroll"]/a/@href').getall()

    for branch_url in branch_urls:
      yield scrapy.Request(branch_url, self.parse_type)

    # yield scrapy.Request(branch_urls[0], self.parse_type)


  def parse_type(self, response):
    type_urls = response.xpath('//span[@class="list-cat-child-category"]/a/@href').getall()

    for type_url in type_urls:
      yield scrapy.Request(type_url, self.parse_list)
    # yield scrapy.Request(type_urls[0], self.parse_list)

  def parse_list(self, response):
    list_urls = response.xpath('//a[@class="product-item-link"]/@href').getall()

    for list_url in list_urls:
      yield scrapy.Request(list_url, self.parse_phone)
    # yield scrapy.Request(list_urls[1], self.parse_phone)

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
      s = re.sub("[^0123456789\.\₫]", '', s)
      s = s.strip()
      return s

    def extract_detail(s):
      str = s.split('</')[0]
      str = str.split('>')[-1]
      return str


    phoneItem['images_intro'] = response.xpath('//img[@class="gallery-placeholder__image"]/@src').get()
    phoneItem['price'] = cleanText(response.xpath('//span[@class="price"][1]/text()').get())
    phoneItem['title'] = response.xpath('//h1/text()').get()
    phoneItem['hot_line'] = '1800.6018'
    phoneItem['link_source'] = response.url
    rating = response.xpath('//div[@class="stats"]/span/text()').get()
    phoneItem['point'] = response.xpath('//meta[@itemprop="ratingValue"]/@content').get()
    phoneItem['rating_total'] = response.xpath('//div[@class="ex_rating"]/a/text()').get()
    phoneItem['star_percent_list'] = response.xpath('//ul[@class="ex_saovang"]/li/span[@class="ex_sdem"]/text()').getall()
    phoneItem['branch'] = response.xpath('//ul[@class="items"]/li[3]/a/text()').get()

    infors = response.xpath('//ul[@class="display"]/li/p/text()').getall()
    details = response.xpath('//ul[@class="display"]/li/div/span').getall()
    details = list(map(extract_detail, details))

    for index, info in enumerate(infors):
      phoneItem[info] = details[index]

    yield phoneItem

    # print(phoneItem)
    # pass
