from requests import get
from bs4 import BeautifulSoup

from contextlib import closing
from collections import Counter
import string

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
    """Extract the author's name from each article."""
    authors = []
    for soup in soup_pot:
        author_container = soup.find('span', class_='author-content')
        author = author_container.h4.text
        authors.append(author)

    unique_authors = list(set(authors))
    author_ids = [author.replace(' ', '').lower() for author in unique_authors]

    return dict(zip(author_ids, unique_authors))

def word_cleanup(words):
    """Clean up the extracted words, removing any unnecessary punctuation
    and unmeaningful words.
    """
    # a mapping table to create replacement pairs
    mapping_table = str.maketrans('', '', string.punctuation)
    stop_words = ['i', 'oraz', 'lub', 'w', 'z', 'a', 'and', 'but', 'or', 'the',
        'of', 'to']

    stripped = [word.translate(mapping_table) for word in words]

    for word in stripped:
        for stop_word in stop_words:
            if stop_word == word:
                stripped.remove(word)

    for word in stripped:
        if len(word) < 2:
            stripped.remove(word)
        elif word.startswith('http'):
            stripped.remove(word)

    return stripped

def get_words(authors, soup_pot):
    """Get each authors words from all the articles written by them."""
    author_names = [v for k,v in authors.items()]
    personal_words = dict.fromkeys(author_names)

    for k,v in personal_words.items():
        words_raw = []
        for soup in soup_pot:
            author_container = soup.find('span', class_='author-content')
            soup_author = author_container.h4.text
            if k == soup_author:
                # get words from header
                header = soup.find('h1', class_='post-title').text
                words_raw.append(header.replace('\n', ' ').split())
                paragraphs = soup.find('section', class_='post-content').text
                words_raw.append(paragraphs.replace('\n', ' ').split())
        words = [str(word) for sublist in words_raw for word in sublist]
        personal_words[k] = word_cleanup(words)

    return dict((k.lower().replace(' ', ''), v)
        for k, v in personal_words.items())

def words_per_author(personal_words):
    """Return a dictionary containing top 10 words for each author."""
    # an empty dict to store authors and their top words with their count
    words_per_author = dict()
    for k,v in personal_words.items():
        # create a Counter type dictionary to store the wordcount
        word_count = Counter()
        for word in v:
            word_count[word] = v.count(word)
        # use Counter's most_common() method to get the 10 most occuring words
        words_per_author[k] = word_count.most_common(10)

    for k,v in words_per_author.items():
        # this loop basically converts the lists of tuples in values to simple
        # dicts
        word_count = dict()
        for tuple in v:
            word_count[tuple[0]] = tuple[1]
        words_per_author[k] = word_count

    return words_per_author

def total_words(personal_words):
    """Return a dictionary containing top 10 words on the blog."""
    all_words = [word for k,v in personal_words.items() for word in v]

    return dict((tuple[0], tuple[1])
        for tuple in Counter(all_words).most_common(10))

soup_pot = get_soup_pot()
authors = get_authors(soup_pot)
personal_words = get_words(authors, soup_pot)
words_per_author = words_per_author(personal_words)
all_words = total_words(personal_words)
print(all_words)
# print(all_words)
