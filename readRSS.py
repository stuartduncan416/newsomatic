from configparser import ConfigParser
from datetime import datetime
from dateutil import parser
import os

import dbConnect
import feedparser
import pytz
from newspaper import Article

def readFeed(rssUrl, section, dbCursor,dbConnection):
    newsFeed = feedparser.parse(rssUrl)
    tz = pytz.timezone('Canada/Eastern')
    now = datetime.now(tz)

    sql = "SELECT url FROM articles"
    dbCursor.execute(sql)
    articles = dbCursor.fetchall()

    # CHECK TO SEE IF THESE ENTRIES ARE ALREADY IN DB
    urlsInDb = []

    for article in articles:
        urlsInDb.append(article[0])

    urlsFromFeed = []

    for article in newsFeed.entries:
        cleanUrl = article.link.split("?")[0]
        urlsFromFeed.append(cleanUrl)

    remainingUrls = list(set(urlsFromFeed) - set(urlsInDb))

    count = 0

    for article in newsFeed.entries:

        # remove any html and leading spaces from description

        print("The title is : {}".format(article.title))
        print("The url is : {}".format(article.link))

        cleanUrl = article.link.split("?")[0]

        if(cleanUrl in remainingUrls):

            print("INSERTING INTO DATABASE")

            body = readBody(article.link)

            sql = "INSERT INTO articles(title, body, section, pubdate, url) VALUES (%s, %s, %s, %s,%s)"
            values = (article.title, body, section, makeDatetime(article.published), cleanUrl)

            try:
                dbCursor.execute(sql, values)
                dbConnection.commit()
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)

        else:
            print("ALREADY IN DATABASE")


def readBody(url):

    body = "ERROR"

    try:
        article = Article(url,keep_article_html=True)
        article.download()
        article.parse()
        article.nlp()
        body = article.text
    except Exception as error:
        print (error)
        body = ""

    return(body)

def makeDatetime(timeString):
    #stripping the timezone out
    dateTimePython = parser.parse(timeString[:-4])
    dateTimeSQL = dateTimePython.strftime("%Y-%m-%d %H:%M:%S")
    return(dateTimeSQL)

def main():
    config = ConfigParser()

    configFile = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(configFile)
    dbCursor, dbConnection = dbConnect.getDbConnection(config["database"])

    # read all the rss feeds from the config.ini file

    for x in range(1, int(config["config"]["feedCount"]) + 1):
        feedString = "feed" + str(x)
        readFeed(config[feedString]["url"],config[feedString]["section"],dbCursor, dbConnection)

if __name__ == "__main__":
    main()
