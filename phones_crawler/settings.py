BOT_NAME = "phones_crawler"

SPIDER_MODULES = ["phones_crawler.spiders"]
NEWSPIDER_MODULE = "phones_crawler.spiders"

ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    "phones_crawler.middlewares.PhonesCrawlerDownloaderMiddleware": 543,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
