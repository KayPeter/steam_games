import scrapy


class TopSellersSpider(scrapy.Spider):
    name = 'top_sellers'
    allowed_domains = ['www.store.steampowered.com']
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
        games = response.xpath("//div[@id='search_resultsRows']/a")
        for game in games:
            image_url = game.xpath(".//div[contains(@class, 'search_capsule')]/img/@src").get()
            title = game.xpath(".//span[@class='title']/text()").get()
            release_date = game.xpath(".//div[contains(@class, 'search_released')]/text()").get()
            discount_rate = self.clean_discount_rate(game.xpath(".//div[contains(@class, 'search_discount')]/span/text()").get())
            discount_price = self.clean_discounted_price(game.xpath("(.//div[contains(@class, 'search_price discounted')]/text())[2]").get())
            original_price = self.get_price(game.xpath(".//div[contains(@class, 'search_price_discount_combined')]"))

            yield {
                'image_url': image_url,
                'title': title,
                'release_date': release_date,
                'discount_rate': discount_rate,
                'discount_price': discount_price,
                'original_price': original_price
            }

