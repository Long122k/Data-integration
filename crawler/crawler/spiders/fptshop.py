
import scrapy


class TGDDSpider(scrapy.Spider):
  name = 'TGDD'
  allowed_domains = ['https://fptshop.com.vn']
  start_urls = ['https://fptshop.com.vn/dien-thoai']
  root_url = 'https://fptshop.com.vn'

  def parse(self, response):
    list_branchs_url = response.xpath('//div[contains(@class,"swiper-slide")]/a/@href').getall()

    list_branchs_url = list(map(lambda branch_url: self.root_url + branch_url, list_branchs_url))

    # for branch_url in list_branchs_url:
    #   yield scrapy.Request(branch_url, self.parse_branch)

    yield scrapy.Request(list_branchs_url[0], self.parse_branch)


  def parse_branch(self, response):
    list_phone_urls = response.xpath('//div[@class="cdt-product__img"]/a/@href').getall()

    list_phone_urls = list(map(lambda branch_url: self.root_url + branch_url, list_phone_urls))

    yield scrapy.Request(list_phone_urls[0], self)
    pass

