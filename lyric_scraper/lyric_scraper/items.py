
from scrapy import Item, Field

class TopSongItem(Item):
    position  = Field()
    song = Field()
    artist = Field()

class TopArtistItem(Item):
    position = Field()
    artist = Field()

class SongItem(Item):
    name = Field()
    artist = Field()
    lyric = Field()
    composedBy = Field()

class ArtistItem(Item):
    name = Field()
    songs = Field()
    


    
