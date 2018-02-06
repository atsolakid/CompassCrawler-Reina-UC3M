# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from course_scraper.items import CourseScraperItem

class SpiderCoursesSpider(CrawlSpider):
    name = 'spider_courses'
    allowed_domains = [
        'www3.uc3m.es',
        'uc3m.es/ss',
        'uc3m.es/reina',
        'aplicaciones.uc3m.es']

    start_urls = ['https://www.uc3m.es/ss/Satellite/Grado/en/Detalle/Estudio_C/1371212562160/1371212987094/Bachelor_s_Degree_in_Computer_Science_and_Engineering#curriculum']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('[data-label="Subject"]',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        print('Processing..' + response.url)
        #self.parse_detail_page(response)
        #yield scrapy.Request(response.url, callback=self.parse_detail_page)

        #def parse_detail_page(self, response):
        year_selector = '//div [@class = "anio"]/text()'
        nameId_selector = '//div [@class = "asignatura"]/text()'
        bachelor_selector = '//div[@class="col-xs-8 col-lg-8 col-xl-8"]/center/text()'
        coordinator_selector = '//div[@class="col-xs-10 col-lg-10 col-xl-10"]/text()'
        departament_selector = '//div[@class="col-xs-12 col-lg-12 col-xl-12"]/text()'
        typeAndSemester_slector = '//div[@class="container-fluid"]/div[@class="row"]/div[1]/text()'
        credits_selector = '//div[@class="container-fluid"]/div[@class="row"]/div[2]/text()'

        year = response.xpath(year_selector).extract_first()
        name = response.xpath(nameId_selector).extract()[0]
        id = response.xpath(nameId_selector).extract()[1]
        bachelor = response.xpath(bachelor_selector).extract()[1]
        coordinator = response.xpath(coordinator_selector).extract()[1]
        departament = response.xpath(departament_selector).extract()[1]
        type = response.xpath(typeAndSemester_slector).extract()[1]
        credits = response.xpath(credits_selector).extract()[7]
        semester = response.xpath(typeAndSemester_slector).extract()[3]
       #course Problema, no soy capaz de obtenerlo

        item = CourseScraperItem()

        item['year'] = year
        item['name'] = name
        item['id'] = id
        item['bachelor'] = bachelor
        item['coordinator'] = coordinator
        item['departament'] = departament
        item['type'] = type
        item['credits'] = credits
        item['semester'] = semester
        item['url'] = response.url

        yield item