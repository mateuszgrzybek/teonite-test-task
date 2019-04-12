from contextlib import closing
from requests import get
from bs4 import BeautifulSoup

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
    # iterate over the list of articles
    for article in articles:
        # extract their urls
        href = article.header.h2.a.get('href').replace('/blog/', '')
        article_url = ''.join([domain, href])
        # store them in the list
        article_urls.append(article_url)

    while True:
        # infinite loop that finds all the consecutive pages and it's articles
        try:
            href_container = soup.find('a', class_='older-posts')
            href = href_container.get('href').replace('/blog/', '')
            next_url = ''.join([domain, href])
        except AttributeError:
            break

        if next_url:
            soup = BeautifulSoup(get_url(next_url), 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                href = article.header.h2.a.get('href').replace('/blog/', '')
                article_url = ''.join([domain, href])
                article_urls.append(article_url)

    return article_urls

def get_soup_pot():
    """Create a list with the contents of each article's page."""
    article_urls = get_articles()
    soup_pot = [BeautifulSoup(get_url(url), 'html.parser')
        for url in article_urls]

    return soup_pot

def get_authors(soup_pot):
    """Extract the author's name from each article"""
    authors = []
    for soup in soup_pot:
        author_container = soup.find('span', class_='author-content')
        author = author_container.h4.text
        authors.append(author)

    unique_authors = list(set(authors))
    author_ids = [author.replace(' ', '').lower() for author in unique_authors]

    return dict(zip(author_ids, unique_authors))

def get_words(authors, soup_pot):
    author_ids = [k for k,v in authors.items()]
    author_names = [v for k,v in authors.items()]

    personal_words = dict.fromkeys(author_names)

    for k,v in personal_words.items():
        words = []
        for soup in soup_pot:
            author_container = soup.find('span', class_='author-content')
            soup_author = author_container.h4.text
            if k == soup_author:
                header = soup.find('h1', class_='post-title').text
                words.append(header)
                print(header)



soup_pot = get_soup_pot()
authors = get_authors(soup_pot)
get_words(authors, soup_pot)
