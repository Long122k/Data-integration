


import scrapy
from scrapy_splash import SplashRequest

class MediaMart(scrapy.Spider):
  name = 'MediaMart'
  start_urls = ['https://mediamart.vn/smartphones']
  root_url = 'https://mediamart.vn'

  script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(4))
            local seemore = splash:select('.seemoreproducts')[0]
            if (seemore != nil or seemore != '') then
              seemore:mouse_click()
              assert(splash:wait(2))
            end
            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """

  def parse(self, response):
    branch_urls = response.xpath('//div[@id="collapseBrand"]/div[@class="card-body"]/ul[@class="list-unstyled"]/li/a/@href').getall()
    branch_urls = list(map(lambda x: self.root_url + '/' + x, branch_urls))

    for url in branch_urls:
      yield SplashRequest(
        url,
        callback=self.parse_list,
        meta={
          "splash": {"endpoint": "render.html", "args": {"lua_source": self.script}}
        },
      )

  def parse_list(self, response):
    phone_urls = set(response.xpath('//div[@class="card mb-4"]/a/@href').getall())
    phone_urls = list(map(lambda x: self.root_url + x, phone_urls))

    for phone_url in phone_urls:
      yield SplashRequest(
        phone_url,
        self.parse_phone,
        args={
          'wait': 2
        }
      )

    # yield SplashRequest(
    #   phone_urls[0],
    #   self.parse_phone,
    #   args={
    #     'wait': 2
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

    phoneItem['images_intro'] = response.xpath('//div[@class="owl-item active"]/a[1]//img/@src').get()
    phoneItem['price'] = response.xpath('//div[@class="pdetail-price-box"]/h3/text()').get()
    phoneItem['title'] = response.xpath('//div[@class="pdetail-name"]/h1/text()').get()
    phoneItem['hot_line'] = '1900.6788'
    phoneItem['link_source'] = response.url
    phoneItem['rating_total'] = response.xpath('//li[@class="product-review-list"]/span/text()').get()
    phoneItem['branch'] = response.xpath('//table[@class="table table-striped"]/tbody/tr[1]/td[2]/span/text()').get()
    # #
    infors = response.xpath('//div[@class="pdetail-attrfeatured-row"][1]/div/span/text()').getall()
    print(infors)
    details = response.xpath('//div[@class="pdetail-attrfeatured-row"][2]/div/b/text()').getall()
    details = list(map(cleanText, details))
    print(details)
    # #
    for index, info in enumerate(infors):
      phoneItem[info] = details[index]
    #
    phoneItem['Màu sắc'] = response.xpath('//div[contains(@class,"pdetail-options")]/a/text()').getall()

    yield phoneItem

    # print(phoneItem)
    # pass
