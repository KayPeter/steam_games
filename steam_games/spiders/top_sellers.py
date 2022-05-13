import scrapy


class TopSellersSpider(scrapy.Spider):
    name = 'top_sellers'
    allowed_domains = ['www.store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers']

    def parse(self, response):
        games = response.xpath("//div[@id='search_resultsRows']/a")
        for game in games:
            image_url = game.xpath(".//div[contains(@class, 'search_capsule')]/img/@src").get()
            title = game.xpath(".//span[@class='title']/text()").get()
            release_date = game.xpath(".//div[contains(@class, 'search_released')]/text()").get()
            discount = game.xpath(".//div[contains(@class, 'search_discount')]/span/text()").get()
            price = game.xpath(".//div[contains(@class, 'search_price')]/text()").get()

            yield {
                'image_url': image_url,
                'title': title,
                'release_date': release_date,
                'discount': discount
            }

