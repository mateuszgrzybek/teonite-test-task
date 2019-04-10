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
    with closing(get(url, stream=True)) as response:
        if is_good_response(response):
            return response.text
        else:
            print('Invalid data.')
