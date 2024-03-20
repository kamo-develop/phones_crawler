import pandas as pd
import scrapy
from scrapy import signals
from logger import base_logger

PHONES_COUNT = 100


class PhonesSpider(scrapy.Spider):
    name = "phones"
    allowed_domains = ["ozon.ru"]
    base_url = "https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?sorting=rating"
    start_urls = [base_url]

    os_versions = []                # Список с версиями ОС
    total_phones_on_pages = 0       # Суммарное количество смартфонов на страницах
    page_num = 1                    # Номер текущей страницы

    @classmethod
    def from_crawler(cls, crawler):
        spider = cls()
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse(self, response):
        """Парсинг страницы с товарами"""

        # Выборка ссылок на смартфоны на текущей странице
        # (в кратком описании товара должен быть font со словом 'Смартфон')
        phones_href = response.xpath(
            "//div[contains(@class, 'widget-search-result-container')]"
            "//div[@class='wi0' and ./div[contains(@class, 'ba9') and .//font[. = 'Смартфон']]]"
            "/a/@href"
        ).getall()

        count_requested_phones = len(phones_href)
        base_logger.info(f"{count_requested_phones} phones on page {self.page_num}")
        if self.total_phones_on_pages + count_requested_phones > PHONES_COUNT:
            # Чтобы запарсить ровно PHONES_COUNT смартфонов и не больше
            count_requested_phones = PHONES_COUNT - self.total_phones_on_pages
        self.total_phones_on_pages += count_requested_phones

        # Переход на страницы смартфонов
        for phone_href in phones_href[:count_requested_phones]:
            url = response.urljoin(phone_href)
            yield scrapy.Request(url, self.parse_phone)

        # Переход на следующую страницу товаров
        if self.total_phones_on_pages < PHONES_COUNT:
            self.page_num += 1
            url = f"{self.base_url}&page={self.page_num}"
            base_logger.info(f"Go to page {self.page_num}")
            yield scrapy.Request(url)

    def parse_phone(self, response):
        """Парсинг страницы со смартфоном"""

        # Поиск в характеристиках информации о версии ОС
        os_version = response.xpath(
            "//div[@id='section-characteristics']"
            "//dd[../dt//text() = 'Версия Android' or ../dt//text() = 'Версия iOS']//text()"
        ).get()

        # Если версия ОС не указана на странице смартфона
        if os_version is None:
            os_version = "Undefined"
        # Удаление лишнего в строке с версией (например Android 13.x)
        os_version = os_version.split('.')[0]

        self.os_versions.append(os_version)
        yield {
            "os_version": os_version,
            "url": response.url,
        }

    def spider_closed(self, spider):
        """Рассчёт распределения версий ОС и запись резултатов в файл"""

        base_logger.info(f"Spider closed. {len(self.os_versions)} phones scraped")

        result_series = pd.Series(self.os_versions).value_counts()
        with open("os_versions.out", 'w') as file:
            file.write(result_series.to_string())
