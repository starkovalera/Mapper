import feedparser


class RSSReader:
    """Holds logic of reading RSS feed."""

    def __init__(self, source, batch_size=None):
        """
        :param source: URL, filename, or string.
        :param batch_size (int): batch size returned on each iteration.
        """
        self._source = source
        self._batch_size = batch_size
        self._etag = None
        self._last_item_published = None  #: Last loaded feed published date as 9-tuple

    def read(self):
        feedset = self._get_feedset()
        feed_items = self._get_feed_items(feedset.entries)
        if self._batch_size is None:
            return feed_items
        for index in range(0, len(feed_items), self._batch_size):
            yield feed_items[index:index + self._batch_size]

    def _get_feed_items(self, entries):
        feed_items = ([item for item in entries if item.published_parsed > self._last_item_published]
                      if self._last_item_published is not None
                      else entries)
        if feed_items:
            self._last_item_published = feed_items[0].published_parsed
        return feed_items

    def _get_feedset(self):
        headers = {}
        if self._etag is not None:
            headers['etag'] = self._etag
        feedset = feedparser.parse(self._source, **headers)
        self._etag = feedset.get('etag', None)
        return feedset
