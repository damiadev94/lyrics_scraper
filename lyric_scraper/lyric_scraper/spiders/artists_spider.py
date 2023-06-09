import scrapy
from scrapy_playwright.page import PageMethod


class ArtistSpider(scrapy.Spider):
    name = "letras-artists"
    allowed_domains = ["letras.com"]

    async def start_requests(self):
        start_urls = ["https://www.letras.com/"]
        for url in start_urls:
            yield scrapy.Request(
                url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_load_state", "domcontentloaded")
                    ],
                    errback = self.errback
                )
            )

    async def parse(self, response):
        page = response.meta['playwright_page']
        alphabet = response.xpath(
            "//body/footer[@class='footer']//li[@class='footer-alphabet-item']/a/@href"
        ).getall()
        for letter_link in alphabet:
            yield scrapy.Request(
                f"https://www.letras.com{letter_link}artistas.html",
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_load_state", "domcontentloaded")
                    ],
                    errback = self.errback
                ),
                callback=self.parse_artists_by_letter_page,
            )

    async def parse_artists_by_letter_page(self, response):
        # artists_by_letter = response.xpath("//wrapper/div[@id='all']/div[@id='cnt-top']//div[@class='artistas-a']/ul/li/a/span/text()").getall()
        artists_by_letter_first_list = response.xpath(
            "//body/div[@class='wrapper']/div[@id='all']/div[@id='cnt_top']/div[@class='g-mb']/div[2]/div[1]/ul[1]/li/a/@href"
        ).getall()
        artists_by_letter_full_list = response.xpath(
            "//body/div[@class='wrapper']/div[@id='all']/div[@id='cnt_top']/div[@class='g-mb']/div[2]/div[1]/ul[2]/li/a/@href"
        ).getall()
        
        for item in artists_by_letter_first_list:
            print(item, sep="|", end=" ")

        for item in artists_by_letter_full_list:
            print(item, sep="|", end=" ")

    async def errback(self, err):
        page =  err.request.meta["playwright_page"]
        await page.close()