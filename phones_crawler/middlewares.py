from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
# import undetected_chromedriver as uc
from selenium import webdriver

class PhonesCrawlerDownloaderMiddleware:
    """Совершает запросы через специальный драйвер, который обходит блокировку"""

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    @classmethod
    def from_crawler(cls, crawler):
        spider = cls()
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def process_request(self, request, spider):
        self.driver.get(request.url)

        # Необходимо дождаться загрузки всей страницы
        WebDriverWait(self.driver, 300).until(
            expected_conditions.presence_of_element_located((By.ID, "ozonTagManagerApp"))
        )

        return HtmlResponse(
            self.driver.current_url,
            body=str.encode(self.driver.page_source),
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        self.driver.close()
        self.driver.quit()
