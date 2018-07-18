
## Pipeline configuration example

Simple example of how to read RSS feed to Django model Feed.
Model:
	
	class Feed(models.Model):  
	    guid = models.CharField(max_length=100)  
	    title = models.CharField(max_length=100)  
	    link = models.CharField(max_length=100, null=True, blank=True)  
	    published = models.DateTimeField()  
	    content = models.TextField(blank=True)

Data:
	

    <item>
    	<guid>https://lenta.ru/news/2018/07/18/barca_golovin/</guid>
    	<title>«Барселона» открестилась от игрока сборной России</title>
    	<link>https://lenta.ru/news/2018/07/18/barca_golovin/</link>
    	<description>
    		<![CDATA[Испанская «Барселона» отказалась...]]>
    	</description>
    	<pubDate>Wed, 18 Jul 2018 21:58:00 +0300</pubDate>
    	<enclosure type="image/jpeg" length="117821" url="https://icdn.lenta.ru/..."/>
    	<category>Спорт</category>
    </item>

### Reader 
	reader = reader = RSSReader("https://lenta.ru/rss", chunk_size=10)

### Mapper 
	mapper = Mapper((  
      ('id', 'guid'),  
	  ('published_parsed', 'published', lambda x: datetime(*(x[0:6]))),  
	  ('summary', 'content'),  
	  ('title', lambda x: x.upper())  
	))
### Writer 
	writer = DjangoModelWriter(Feed, not_write_to=('id',))

### Pipeline
	pipeline(reader, mapper, writer)
