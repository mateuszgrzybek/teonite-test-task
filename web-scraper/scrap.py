from contextlib import closing
from requests import get
from bs4 import BeautifulSoup

url = 'https://teonite.com/blog/'

def is_good_response(response):
    """Check if the given url appears to be an html doctype and check the
    status code returned with the response.
    """
    return(response.status_code == 200,
           response.text.find('html'))

def get_url(url):
    """Get the page's html code."""
    # return the reponse as a block of text, and close the connection
    with closing(get(url, stream=True)) as response:
        if is_good_response(response):
            return response.text
        else:
            print('Invalid data.')

def get_articles():
    """Get urls of all articles found on the first page and all consecutive
    pages.
    """

    domain = 'https://teonite.com/blog/'
    # find all the article tags from the first page
    soup = BeautifulSoup(get_url(domain), 'html.parser')
    articles = soup.find_all('article')

    article_urls = []
    # iterate over the list of articles, extract their urls and store them in the list
    for article in articles:
        href = article.header.h2.a.get('href').replace('/blog/', '')
        article_url = ''.join([domain, href])
        article_urls.append(article_url)

    print(article_urls)

get_articles()
