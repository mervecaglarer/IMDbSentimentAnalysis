# IMDbSentimentAnalysis
Web Mining lesson project

## Explain how my program works 
My program takes the movie name from the user and crawl it from imdb.com and takes the necessary link. 
Then it does crawl again from this link and takes the comments on the first page.
The taken comments is used to show the percentage of how many positive comments were made by using sentiment analysis.

I used this dataset for training. This dataset consist of 50.000 rows comments.
https://www.kaggle.com/lakshmi25npathi/sentiment-analysis-of-imdb-movie-reviews

## How to run?
To run main.py, you need to enter virtual environment;

![image](https://user-images.githubusercontent.com/48553941/85927414-8bf30000-b8ae-11ea-8944-8114fc13505e.png)



In nlp.py, sentiment analysis is performed with nlp libraries.

In movieLink.py, movie links are being crawl with scrapy.

In getComments.py, the comments on the link crawl from movielink are crawl with scrapy.

After running main.py, result is like that;

![image](https://user-images.githubusercontent.com/48553941/85927417-8e555a00-b8ae-11ea-8f71-15bb5d859ce7.png)

