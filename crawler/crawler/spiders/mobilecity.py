

import scrapy
from scrapy_splash import SplashRequest

class MobileCity(scrapy.Spider):
  name = 'MobileCity'
  start_urls = ['https://mobilecity.vn/']

  script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(4))
            assert(splash:runjs("$('.more')[0].click();"))
            assert(splash:wait(2))
            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """

  script_phone = """
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

  def parse(self, response):
    branch_urls = response.xpath('//li[@class="v2-item-menu"][1]//div[@class="left-menu"]/div/ul/li/a/@href').getall()
    branch_urls = branch_urls[1:]

    for url in branch_urls:
      yield SplashRequest(
        url,
        callback=self.parse_list,
        meta={
          "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
        },
      )

  def parse_list(self, response):
    list_urls = response.xpath('//p[@class="name"]/a/@href').getall()

    for url in list_urls:

      yield SplashRequest(
        url=url,
        callback=self.parse_phone,
        meta={
          "splash": {"endpoint": "render.html", "args": {"lua_source": self.script_phone}}
        },
      )



  def parse_phone(self, response):
      phoneItem = {}

      def cleanText(s):
        s = s.replace('"', '')
        s = s.replace("'", '')
        s = s.replace(":", '')
        s = s.replace("\n", '')
        s = s.replace("\t", '')
        s = s.replace("\r", '')
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


      phoneItem['images_intro'] = response.xpath('//div[@class="product_image v2-product-image"]/li[@class="active"]/img/@data-original').get()
      phoneItem['price'] = response.xpath('//p[@class="product-summary-price"]/text()').get()
      phoneItem['title'] = response.xpath('//p[@class="product-summary-title"]/text()').get()
      phoneItem['hot_line'] = '0969.120.120'
      phoneItem['link_source'] = response.url
      phoneItem['rating_total'] = response.xpath('//div[@class="comment-vote__star-total"]/p/text()').get()
      phoneItem['branch'] = response.xpath('//div[@class="breadcrumb"]/ul/li[2]/a/span/text()').get()
      #
      infors = response.xpath('//div[@class="product-info-content"]/table/tbody/tr/td[1]/text()').getall()
      infors = list(map(cleanText, infors))
      # print(infors)
      details = response.xpath('//div[@class="product-info-content"]/table/tbody/tr/td[2]/text()').getall()
      details = list(map(cleanText, details))
      # print(details)
      # #
      for index, info in enumerate(infors):
        phoneItem[info] = details[index]
      # #
      yield phoneItem

      # print(phoneItem)
      # pass
