
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
        <guid>https://lenta.ru/news/2018/07/19/dobro_propadaet/</guid>
        <title>В Кемерово жители ...</title>
        <link>https://lenta.ru/news/2018/07/19/dobro_propadaet/</link>
        <description>
            <![CDATA[В Кемерово шесть местных жителей открыли ...]]>
        </description>
        <pubDate>Thu, 19 Jul 2018 00:31:43 +0300</pubDate>
        <enclosure url="https://icdn.lenta.ru/..."/>
        <category>Силовые структуры</category>
    </item>

Data after feedparser:


    id : https://lenta.ru/news/2018/07/19/dobro_propadaet/
    guidislink : True
    link : https://lenta.ru/news/2018/07/19/dobro_propadaet/
    title : В Кемерово жители ...
    title_detail : {'type': 'text/plain', 'language': None, 'base': 'https://lenta.ru/rss', ...'}
    links : [{'rel': 'alternate', 'type': 'text/html', ...}]
    summary : В Кемерово шесть местных жителей ...
    summary_detail : {'type': 'text/html', 'language': None, 'base': 'https://lenta.ru/rss', ...}
    published : Thu, 19 Jul 2018 00:31:43 +0300
    published_parsed : time.struct_time(tm_year=2018, tm_mon=7, tm_mday=18, tm_hour=21, tm_min=31, tm_sec=43, tm_wday=2, tm_yday=199, tm_isdst=0)
    tags : [{'term': 'Силовые структуры', 'scheme': None, 'label': None}]

### Reader 
	reader = reader = RSSReader("https://lenta.ru/rss", chunk_size=10)

### Mapper 
	mapper = Mapper((  
      ('id', 'guid'),  
	  ('published_parsed', 'published', lambda x: datetime(*(x[:6]))),  
	  ('summary', 'content'),  
	  ('title', lambda x: x.upper())  
	))
### Writer 
	writer = DjangoModelWriter(Feed, not_write_to=('id',))

### Pipeline
	pipeline(reader, mapper, writer)
