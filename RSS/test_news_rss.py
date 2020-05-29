
import feedparser  # Usefull to parse RSS feeds
from RSS.news_rss import RssUrl


class TestRssUrl(RssUrl):
    def test_url_feed(self, news_source):
        """
        See if can get a positive response
        :return:
        """
        url_list = self.get_url_feed(news_source)  # This provides a list with URLs...
        label_name = self.url_dict[news_source]['name']  # This is the label name of the news category
        assert len(url_list) == len(label_name)  # These two should be of equal length

        status_dict = {}
        for i_name, i_url in zip(label_name, url_list):
            url_content = feedparser.parse(i_url)
            if url_content.status == 200:
                temp_dict = {i_name: 'pass'}
            elif url_content.status == 301:
                temp_dict = {i_name: 'moved'}
            else:
                temp_dict = {i_name: url_content.status}

            status_dict.update(temp_dict)
        return {news_source: status_dict}


if __name__ == "__main__":
    a = TestRssUrl()
    print('status NOS feed: ', a.test_url_feed('nos'))
    print('status NU feed: ', a.test_url_feed('nu'))
    print('status RTL feed: ', a.test_url_feed('rtl'))