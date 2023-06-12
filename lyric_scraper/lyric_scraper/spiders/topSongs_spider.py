from ..items import TopSongItem
from pathlib import Path
import scrapy
import csv

class TopSongsSpider(scrapy.Spider):
    name = "letras-top-songs"

    def start_requests(self):
        url = "https://www.letras.com/mais-acessadas"
        yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        contador = 1
        songs = []

        content = response.css(".g-2-3 li")

        for item in content:
            position = content.index(item) + 1
            topSongItem = TopSongItem()

            topSongItem["position"] = position
            topSongItem["song"] = item.css("b::text").get()
            topSongItem["artist"] = item.css("span::text").get()

            songs.append(topSongItem)

        with open("top_songs.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=" ")
            for song in songs:
                writer.writerow(str(song["position"]) + song["song"] + song["artist"])