import sys, os
import psycopg2

from scrap import get_soup_pot, get_authors, get_words

db_params = {'database': os.environ.get('DB_NAME', ''),
             'host': os.environ.get('DB_HOST', ''),
             'user': os.environ.get('DB_USER', ''),
             'password': os.environ.get('DB_PASSWORD', ''),
             'port': os.environ.get('DB_PORT', ''),
            }

soup_pot = get_soup_pot()
authors = get_authors(soup_pot)

def connect(db_params, authors, soup_pot):
    words = get_words(authors, soup_pot)
    conn = None
    try:
        # connect to the database
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**db_params)

        # create a cursor
        cursor = conn.cursor()


# def initial_insert(db_params, authors, soup_pot):
#     words = get_words(authors, soup_pot)
#     conn = None
#     try:
#         # connect to the database
#         print("Connecting to the PostgreSQL database...")
#         conn = psycopg2.connect(**db_params)
#
#         # create a cursor
#         cursor = conn.cursor()
#
#         # delete records if they exist
#         cursor.execute("""CREATE TABLE all_words(
#             author_id text PRIMARY KEY,
#             word_list text NOT NULL)""")
#
#         for author_id, word_list in words.items():
#             cursor.execute(
#                 """INSERT INTO all_words (author_id, word_list)
#                 VALUES ('{}', '{}')""".format(author_id, tuple(word_list)))
#
#         conn.commit()
#         # close the connection
#         conn.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')

if __name__ == "__main__":
    initial_insert(db_params, authors, soup_pot)