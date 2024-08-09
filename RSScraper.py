import feedparser
import newspaper
import mysql.connector
import html
import openai

openai.api_key = "AIzaSyChIGZjz5MKsVEKEZ7PaQBIRuGezMrmUAc"

response = openai.ChatCompletion.create(
    model="gpt-4",  # or the specific model you've been granted access to
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message['content'])
sql_config = {
    'user': 'scraper',
    'password': 'Scraper2024!"£',
    'host': '127.0.0.1',
    'database': 'RSS'
}

def insert_if_not_exists(data_to_insert):
    try:
        # Establish a connection to the database
        cnx = mysql.connector.connect(**sql_config)
        cursor = cnx.cursor()

        title = data_to_insert['title']
        text = data_to_insert['text']
        link = data_to_insert['link']
        published = data_to_insert['published']
        url = data_to_insert['url']

        query = "INSERT INTO rss.articles (url, title, article_text, link, published) " \
                "VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (url, html.escape(title), text, link, published))
        cnx.commit()
        print("Data inserted successfully.")

    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def get_rss_feed_articles(url):
    feed = feedparser.parse(url)
    cnx = mysql.connector.connect(**sql_config)
    cursor = cnx.cursor()
    for entry in feed.entries:
        link = entry.link
        query = f"SELECT 1 FROM rss.articles WHERE link = '{link}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            print("Field value already exists. No data inserted.")
            continue

        article = newspaper.Article(entry.link)
        try:
            article.download()
            article.parse()
            parsed_article = ({
                'title': article.title,
                'text': article.text,
                'link': entry.link,
                'url': url,
                'published': entry.published
            })
            insert_if_not_exists(parsed_article)
        except newspaper.ArticleException as e:
            print(f"Error downloading or parsing article: {e}")


cn = mysql.connector.connect(**sql_config)
cr = cn.cursor()
sql = f"SELECT url FROM rss.urls"
cr.execute(sql)
urls = cr.fetchall()
if cr:
    cr.close()
if cn:
    cn.close()

for url in urls:
    print(url[0])
    get_rss_feed_articles(url[0])
