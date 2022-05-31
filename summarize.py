from transformers import pipeline
from configparser import ConfigParser
import os

import dbConnect

def summarize(dbCursor,dbConnection):

        summarizer = pipeline("summarization")

        # find articles that don't have a summary
        sql = "SELECT id,body FROM articles WHERE summary = ''"
        dbCursor.execute(sql)
        articles = dbCursor.fetchall()

        # add a summary for each article
        for article in articles:
            print("Summarizing article id {}".format(article[0]))
            summary = summarizer(article[1][:1000], max_length=130, min_length=30, do_sample=False)
            sql = "UPDATE articles SET summary = %s WHERE id = %s"
            values = (summary[0]["summary_text"], article[0])
            dbCursor.execute(sql, values)
            dbConnection.commit()


def main():
    config = ConfigParser()
    configFile = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(configFile)
    dbCursor, dbConnection = dbConnect.getDbConnection(config["database"])
    summarize(dbCursor, dbConnection)

if __name__ == "__main__":
    main()
