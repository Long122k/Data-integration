

import scrapy

class Store24H(scrapy.Spider):
  name = '24hStore'
  allowed_domains = ['24hstore.vn']
  start_urls = ['https://24hstore.vn/dien-thoai']

  def _parse(self, response):
    branch_urls = response.xpath('//a[@class="cat_child "]/@href').getall()

    for branch_url in branch_urls:
      yield scrapy.Request(branch_url, self.parse_branch, dont_filter = True)

    # yield scrapy.Request(branch_urls[0], self.parse_branch)


  def parse_branch(self, response):
    phone_urls = response.xpath('//div[contains(@class,"product")]/div/a/@href').getall()
    phone_urls = phone_urls[:-2]

    for phone_url in phone_urls:
      yield scrapy.Request(phone_url, self.parse_type, dont_filter = True)

    # yield scrapy.Request(phone_urls[0], self.parse_type)


  def parse_type(self, response):
    type_urls = response.xpath('//div[@class="list_same"]/a/@href').getall()

    if len(type_urls) > 0:
      for type_url in type_urls:
        yield scrapy.Request(type_url, callback=self.parse_phone, dont_filter = True)
    else:
      yield scrapy.Request(response.url, callback=self.parse_phone, dont_filter = True)

    # yield scrapy.Request(type_urls[0], self.parse_phone)
    # yield scrapy.Request('https://24hstore.vn/dien-thoai-xiaomi/xiaomi-redmi-note-10-pro-hang-cong-ty-p5787', self.parse_phone)


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

    phoneItem['images_intro'] = set(response.xpath('//ul[@id="imageGallery"]/li/@data-src').getall())
    phoneItem['option'] = response.xpath('//a[@class="item_same active"]/span[@class="nick_name"]/span/text()').get()
    phoneItem['price'] = cleanText(response.xpath('//div[@class="price_ins"]/p/span[@class="_price"]/text()').get())
    phoneItem['title'] = cleanText(response.xpath('//h1[1]/text()').get())
    phoneItem['hot_line'] = '1900.0351'
    phoneItem['link_source'] = response.url
    rating = response.xpath('//div[@class="stats"]/span/text()').get()
    phoneItem['point'] = response.xpath('//div[@class="star-detail"][1]/@data-rating').get()
    phoneItem['rating_total'] = response.xpath('//div[@class="total_rate"]/span/text()').get()
    # phoneItem['star_percent_list'] = response.xpath('//a[@class="number-percent"]/text()').getall(),
    phoneItem['branch'] = response.xpath('//div[contains(@class,"fl-left")][3]/a/span/text()').get()

    infors = response.xpath('//td[@class="title_charactestic"]/text()').getall()
    details = response.xpath('//td[@class="content_charactestic"]/text()').getall()
    infors = list(map(cleanText, infors))
    details = list(map(cleanText, details))

    for index, info in enumerate(infors):
      phoneItem[info] = details[index]

    phoneItem['color'] = response.xpath('//div[contains(@class,"color_item")]/span/span/text()').getall()

    yield phoneItem

