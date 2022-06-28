

import scrapy

class ClickBuy(scrapy.Spider):
  name = 'ClickBuy'
  # allowed_domain = ['https://hcm.clickbuy.com.vn']
  start_urls = ['https://hcm.clickbuy.com.vn/danh-muc/dien-thoai/']

  def parse(self, response):
    branch_urls = response.xpath('//ul[@id="menu-menu-dienthoaicu"]/li/a/@href').getall()

    for branch_url in branch_urls:
      yield scrapy.Request(branch_url, self.parse_branch, dont_filter = True)

    # yield scrapy.Request(branch_urls[0], self.parse_branch)

  def parse_branch(self, response):
    type_urls = response.xpath('//ul[@id="menu-menu-iphone"]/li/a/@href').getall()

    for type_url in type_urls:
      yield scrapy.Request(type_url, self.parse_list_phone, dont_filter = True)

    # yield scrapy.Request(type_urls[0], self.parse_list_phone)

  def parse_list_phone(self, response):
    phone_urls = response.xpath('//ul[contains(@class,"products")]/li/a/@href').getall()

    for phone_url in phone_urls:
      yield scrapy.Request(phone_url, self.parse_phone, dont_filter = True)

    # yield scrapy.Request(phone_urls[0], self.parse_phone)

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
      str = s.split('</')[0]
      str = str.split('>')[-1]
      return str


    phoneItem['images_intro'] = response.xpath('//div[@class="woocommerce-product-gallery__image"]/a/@href').get()
    phoneItem['price'] = cleanText(response.xpath('//span[@class="woocommerce-Price-amount amount"]/text()').get())
    phoneItem['title'] = cleanText(response.xpath('//h1[1]/text()').get())
    phoneItem['hot_line'] = '1900.63.39.09'
    phoneItem['link_source'] = response.url
    rating = response.xpath('//div[@class="stats"]/span/text()').get()
    phoneItem['point'] = response.xpath('//strong[@class="rating"]/text()').get()
    phoneItem['rating_total'] = response.xpath('//div[@class="ex_rating"]/a/text()').get()
    phoneItem['star_percent_list'] = response.xpath('//ul[@class="ex_saovang"]/li/span[@class="ex_sdem"]/text()').getall()
    phoneItem['branch'] = response.xpath('//nav[@class="woocommerce-breadcrumb"]/a[3]/text()').get()

    infors = response.xpath('//tr[contains(@class,"woocommerce-product-attributes-item")]/th/text()').getall()
    details = response.xpath('//tr[contains(@class,"woocommerce-product-attributes-item")]/td/p').getall()
    details = list(map(extract_detail, details))

    for index, info in enumerate(infors):
      phoneItem[info] = details[index]

    yield phoneItem

    # print(phoneItem)
    # pass
