

import scrapy
from scrapy_splash import SplashRequest

class ViettelStore(scrapy.Spider):
  name = 'Viettel'
  start_urls = ['https://viettelstore.vn/dien-thoai']
  root_url = 'https://viettelstore.vn'

  script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(4))
            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """

  def parse(self, response ):
    branch_urls = response. xpath('//div[@id="manulist"]/div/a/@href').getall()
    branch_urls = list(map(lambda x: self.root_url + x, branch_urls))

    for url in branch_urls:
      yield SplashRequest(
        url,
        self.parse_list,
        endpoint='render.html',
        args={
          'wait': 3
        }
      )
    #
    # yield SplashRequest(
    #   branch_urls[0],
    #   self.parse_list,
    #   endpoint='render.html',
    #   args={
    #     'wait': 3,
    #     'lua_source': self.script
    #   }
    # )


  def parse_list(self, response):
    phone_urls = response.xpath('//div[contains(@class,"ProductList3Col_item")]/a/@href').getall()
    # lisst = response.xpath('//div[@id="div_Danh_Sach_San_Pham_loadMore_btn"]').get()
    phone_urls = list(map(lambda x: self.root_url + x, phone_urls))

    for url in phone_urls:
      yield SplashRequest(
        url,
        self.parse_phone,
        endpoint='render.html',
        args={
          'wait': 5
        }
      )

    # yield SplashRequest(
    #   phone_urls[0],
    #   self.parse_phone,
    #   endpoint='render.html',
    #   args={
    #     'wait': 5,
    #     'lua_source': self.script
    #   }
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

    def extract_detail(s):
      str = ''.join(s.split('<br>'))
      str = ''.join(str.split('<td>'))
      str = ''.join(str.split('</td>'))
      str = str.split('</a>')
      str = list(map(lambda st: st.split('<a')[0], str))
      str = ','.join(str)
      return str


    phoneItem['images_intro'] = response.xpath('//div[@class="item"][1]/img/@src').get()
    phoneItem['price'] = response.xpath('//span[@id="_price_new436"]/text()').get()
    phoneItem['title'] = cleanText(response.xpath('//h1[@class="txt-24"]/text()').get())
    phoneItem['hot_line'] = '1800.8123'
    phoneItem['link_source'] = response.url
    #
    infors = response.xpath('//div[@class="digital "]/table/tbody/tr/td[1]/text()').getall()
    infors = list(map(cleanText, infors))
    # print(infors)
    details = response.xpath('//div[@class="digital "]/table/tbody/tr/td[2]/text()').getall()
    # details = list(map(cleanText, details))
    # print(details)
    # #
    for index, info in enumerate(infors):
      phoneItem[info] = details[index]
    #
    yield phoneItem

    # print(phoneItem)
    # pass
