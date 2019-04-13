import os
import psycopg2

from ../web-scraper/scrap import get_soup_pot, get_authors, get_words

db_params = {'database': os.environ.get('DB_NAME', ''),
             'host': os.environ.get('DB_HOST', ''),
             'user': os.environ.get('DB_USER', ''),
             'password': os.environ.get('DB_PASSWORD', ''),
             'port': os.environ.get('DB_PORT', ''),
            }

soup_pot = get_soup_pot()
authors = get_authors(soup_pot)

def initial_insert(db_params):

    
