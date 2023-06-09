import scrapy

class AllArtistSpider(scrapy.Spider):
    name =  "letras-all-artists"
    allowed_domains=["letras.com"]

    def start_requests(self):
        start_urls = ["https://www.letras.com/"]
        for url in start_urls:
            yield scrapy.Request(url, meta={'playwright' : True})

    def parse(self, response):
        alphabet =  response.xpath("//body/footer[@class='footer']//li[@class='footer-alphabet-item']/a/@href").getall()
        for letter_link in alphabet:
            yield response.follow(f"https://www.letras.com{letter_link}", callback=self.parse_artists_by_letter_page)

    def parse_artists_by_letter_page(self, response):
        # artists_by_letter = response.xpath("//wrapper/div[@id='all']/div[@id='cnt-top']//div[@class='artistas-a']/ul/li/a/span/text()").getall()
        artists_by_letter = response.xpath("//body/div[@class='wrapper']/div[@id='all']/div[@id='cnt_top']/div[@class='g-mb']/div[2]/div[1]/ul/li/a/@href").getall()
        for item in artists_by_letter:
            print(item, sep="|", end=" ")