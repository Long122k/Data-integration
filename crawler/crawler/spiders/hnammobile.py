

import scrapy
import re
import pandas as pd

class HNamMobile(scrapy.Spider):
  name = 'HNam'
  start_urls = ['https://www.hnammobile.com/dien-thoai']

  def parse(self, response):
    branch_urls = response.xpath('//div[@class="list-brands"]/a/@href').getall()

    for branch_url in branch_urls:
      yield scrapy.Request(branch_url, self.parse_list)

    # yield scrapy.Request(branch_urls[1], self.parse_list)


  def parse_list(self, response):
    list_urls = response.xpath('//div[@class="product-image"]/figure/a/@href').getall()
    list_urls = [list_url for list_url in list_urls if "https" in list_url]

    for list_url in list_urls:
      yield scrapy.Request(list_url, self.parse_phone)

    # yield scrapy.Request(list_urls[0], self.parse_phone)


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

    def extract_detail(s):
      str = ''.join(s.split('<br>'))
      str = ''.join(str.split('<td>'))
      str = ''.join(str.split('</td>'))
      str = str.split('</a>')
      str = list(map(lambda st: st.split('<a')[0], str))
      str = ','.join(str)
      return str


    phoneItem['images_intro'] = response.xpath('//div[@class="lead-image-item"]//source[1]/@data-srcset').get()
    phoneItem['option'] = response.xpath('//a[@class="option active"]/text()').get()
    phoneItem['price'] = response.xpath('//div[@id="product-item-price"]/span[@class="price"]/b/text()').get()
    phoneItem['title'] = response.xpath('//h1/text()').get()
    phoneItem['hot_line'] = '1800.6878'
    phoneItem['link_source'] = response.url
    phoneItem['point'] = response.xpath('//div[@class="rating-header"]/div[@class="point"]/text()').get()
    phoneItem['rating_total'] = response.xpath('//div[@class="rating-header"]/div[@class="rating-times"]/p/text()').get()
    phoneItem['star_percent_list'] = response.xpath('//div[@class="rating-bar"]/div[@class="percentage-num"]/text()').getall()
    phoneItem['branch'] = response.xpath('//div[@class="list-breadcrumb"]/a[3]/text()').get()

    infors = response.xpath('//table[@id="tableThongso"]/tr/th[not(@class)]/text()').getall()
    infors = list(map(cleanText, infors))
    details = response.xpath('//table[@id="tableThongso"]/tr/td').getall()
    details = list(map(extract_detail, details))
    #
    for index, info in enumerate(infors):
      phoneItem[info] = details[index]
    #
    yield phoneItem

    # print(phoneItem)
    # pass
