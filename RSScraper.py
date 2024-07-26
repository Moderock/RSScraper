import feedparser
import newspaper

def get_rss_feed_articles(url):
    """Fetches RSS feed entries and extracts full articles."""

    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries:
        # print(entry.link)
        # Create a Newspaper article object from the entry's link
        article = newspaper.Article(entry.link)

        try:
            article.download()  # Download the article content
            article.parse()      # Parse the article structure
            parsed_article = ({
                'title': article.title,
                'text': article.text,
                'link': entry.link,
                'published': entry.published  # Optional
            })
        except newspaper.ArticleException as e:
            print(f"Error downloading or parsing article: {e}")

        print(f"Title: {parsed_article['title']}")
        print(f"Link: {parsed_article['link']}")
        print(parsed_article['text'])  # Print the full article text
        print("-" * 20)

    return articles


urls = ['https://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml']
urls = ['https://moxie.foxnews.com/google-publisher/us.xml']
for url in urls:
    print(url)
    get_rss_feed_articles(url)




