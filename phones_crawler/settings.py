BOT_NAME = "phones_crawler"

SPIDER_MODULES = ["phones_crawler.spiders"]
NEWSPIDER_MODULE = "phones_crawler.spiders"

ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    # "rotating_proxies.middlewares.RotatingProxyMiddleware": 510,
    # "rotating_proxies.middlewares.BanDetectionMiddleware": 520,
    "phones_crawler.middlewares.PhonesCrawlerDownloaderMiddleware": 543,
}

# ROTATING_PROXY_LIST = [
#     '14.99.212.242:5678',
#     '188.132.146.23:1080',
#     '43.153.64.66:443',
# ]

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
