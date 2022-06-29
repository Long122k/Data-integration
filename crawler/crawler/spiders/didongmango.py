

import scrapy

class DiDongMango(scrapy.Spider):
  name = 'Mango'
  # start_urls = ['https://didongmango.com/iphone-pc49.html']
  start_urls = ['https://didongmango.com/iphone-pc49.html',
                'https://didongmango.com/sony-pc53.html',
                'https://didongmango.com/samsung-pc51.html',
                'https://didongmango.com/lg-pc709.html',
                'https://didongmango.com/google-pixel-pc889.html']


  def parse(self, response):
    type_urls = response.xpath('//div[@class="body_block_product_cate"]/a/@href').getall()

    for type_url in type_urls:
      yield scrapy.Request(type_url, self.parse_list)

    # yield scrapy.Request(type_urls[0], self.parse_list)


  def parse_list(self, response):
    list_urls = response.xpath('//figure[@class="product_image "]/a/@href').getall()

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


    phoneItem['images_intro'] = response.xpath('//div[@class="item hide"]/a/@href').getall()
    if len(phoneItem['images_intro']) == 0:
      phoneItem['images_intro'] = response.xpath('//img[@id="img-root-styling"]/@src').get()

      if phoneItem['images_intro'] is None:
        phoneItem['images_intro'] = response.xpath('//div[@id="products_slideshow_hightlight"]/div/img/@src').getall()

    option = response.xpath('//a[@class="Selector active"]/text()').get()
    if option is not None:
      phoneItem['option'] = cleanText(option)
    phoneItem['price'] = cleanText(response.xpath('//div[@id="price"]/text()').get())
    phoneItem['title'] = response.xpath('//div[@class="product_name"]/h1/text()').get()
    phoneItem['hot_line'] = '0982351080'
    phoneItem['link_source'] = response.url
    phoneItem['point'] = response.xpath('//span[@class="point"]/text()').get()
    phoneItem['rating_total'] = response.xpath('//span[@itemprop="ratingCount"]/text()').get()
    phoneItem['branch'] = response.xpath('//ul[@class="breadcrumb"]/li[3]/a/span/text()').get()
    phoneItem['color'] = response.xpath('//span[@class="color_name"]/text()').getall()

    infors = response.xpath('//table[@class="compare_table"]//td[@class="title_charactestic"]/text()').getall()
    infors = list(map(cleanText, infors))

    details = response.xpath('//table[@class="compare_table"]//td[@class="content_charactestic"]/text()').getall()
    details = list(map(cleanText, details))

    for index, info in enumerate(infors):
      phoneItem[info] = details[index]

    yield phoneItem

    # print(phoneItem)
    # pass
