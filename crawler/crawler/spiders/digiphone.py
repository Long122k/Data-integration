

import scrapy
from scrapy_splash import SplashRequest

class DigiPhone(scrapy.Spider):
  name = 'DigiPhone'
  start_urls = ['https://digiphone.vn/']
  root_url = 'https://digiphone.vn'

  def parse(self, response):
     yield SplashRequest(
       'https://digiphone.vn/collections/dien-thoai',
       self.parse_branch,
       args={
         'wait': 3
       }
     )

  def parse_branch(self, response):
    branch_urls = response.xpath('//div[@class="new-collection-brand-item"]/a/@href').getall()

    for branch_url in branch_urls:
      yield scrapy.Request(
        branch_url,
        self.parse_page
      )

  def parse_page(self, response):
    pages = response.xpath('//ul[@id="new-product-pagination"]/li/a/text()').getall()
    # print(f'day laf pages: {pages}')
    if len(pages) > 0:
      max_page = pages[-1]
      link_page =response.xpath('//ul[@id="new-product-pagination"]/li[last()]/a/@href').get()
      link_page = self.root_url + link_page[:-1]

      for page_num in range(1, int(max_page) + 1):
        page = link_page + str(page_num)
        yield scrapy.Request(
          page,
          self.parse_list
        )
    else:
      yield scrapy.Request(
        response.url,
        self.parse_list
      )

  def parse_list(self, response):
    list_phone = response.xpath('//div[@class="new-product-item-img"]/a/@href').getall()
    list_phone = list(map(lambda x: self.root_url + x, list_phone))

    for phone_url in list_phone:
      yield scrapy.Request(
        phone_url,
        self.parse_phone
      )
    #
    # yield scrapy.Request(
    #   list_phone[0],
    #   self.parse_phone
    # )

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

    phoneItem['images_intro'] = 'https:' + response.xpath('//div[@id="ProductPhoto"]/img[last()]/@src').get()
    phoneItem['price'] = cleanText(response.xpath('//span[@class="current-price ProductPrice"]/text()').get())
    phoneItem['title'] = cleanText(response.xpath('//h1[1]/text()').get())
    phoneItem['hot_line'] = '0905988900'
    phoneItem['link_source'] = response.url
    phoneItem['rating_total'] = response.xpath('//div[@class="haravan-product-reviews-badge"]/div/div/div/span/text()').get()
    phoneItem['branch'] = response.xpath('//div[@class="pro-brand"]/a/text()').get()


    phoneItem['Kích thước'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[2]/td[2]/text()').get()
    phoneItem['SIM'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[4]/td[2]/text()').get()
    phoneItem['Khối lượng'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[3]/td[2]/text()').get()
    phoneItem['Màn hình'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[6]/td[2]/text()').get()
    phoneItem['Hệ điều hành'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[11]/td[2]/text()').get()
    phoneItem['RAM'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[16]/td[2]/text()').get()
    phoneItem['Bộ nhớ trong'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[17]/td[2]/text()').get()
    phoneItem['Thẻ nhớ ngoài'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[18]/td[2]/text()').get()
    phoneItem['Camera sau'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[20]/td[2]/text()').get()
    phoneItem['Camera trước'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[24]/td[2]/text()').get()
    phoneItem['Pin'] = response.xpath('//div[@class="content hFirst"]/table/tbody/tr[28]/td[2]/text()').get()

    phoneItem['color'] = response.xpath('//div[@class="select-swap"]/div/label/span/text()').getall()

    yield phoneItem

    # print(phoneItem)
    # pass
