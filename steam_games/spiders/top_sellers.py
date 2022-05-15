import scrapy
from steam_games.items import SteamGamesItem


class TopSellersSpider(scrapy.Spider):
    name = 'top_sellers'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers']

    def get_price(self, price_selector):
        original_price = ''
        price_div = price_selector.xpath(".//div[contains(@class, 'search_price discounted')]")
        if len(price_div) > 0:
            original_price = price_div.xpath(".//span/strike/text()").get()
        else:
            original_price = price_selector.xpath("normalize-space(.//div[contains(@class, 'search_price')]/text())").get()

        return original_price

    def clean_discounted_price(self, discounted_price):
        if discounted_price:
            return discounted_price.strip()
        
        return None

    def clean_discount_rate(self, discount):
        if discount:
            return discount.lstrip("-")
        return None

    def parse(self, response):
        item = SteamGamesItem()
        games = response.xpath("//div[@id='search_resultsRows']/a")
        for game in games:
            item['image_url'] = game.xpath(".//div[contains(@class, 'search_capsule')]/img/@src").get()
            item['title'] = game.xpath(".//span[@class='title']/text()").get()
            item['release_date'] = game.xpath(".//div[contains(@class, 'search_released')]/text()").get()
            item['discount_rate'] = self.clean_discount_rate(game.xpath(".//div[contains(@class, 'search_discount')]/span/text()").get())
            item['discount_price'] = self.clean_discounted_price(game.xpath("(.//div[contains(@class, 'search_price discounted')]/text())[2]").get())
            item['original_price'] = self.get_price(game.xpath(".//div[contains(@class, 'search_price_discount_combined')]"))
            yield item

            next_page_btn = response.xpath("//a[@class='pagebtn' and text()='>']/@href").get()
            if next_page_btn:
                yield scrapy.Request(
                    url=next_page_btn,
                    callback=self.parse
                )

