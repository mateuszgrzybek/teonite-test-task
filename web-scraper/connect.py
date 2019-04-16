import sys, os
import psycopg2

from scrap import get_soup_pot, get_authors, get_words, words_per_author

# db_params = {'database': os.environ.get('DB_NAME', ''),
#              'host': os.environ.get('DB_HOST', ''),
#              'user': os.environ.get('DB_USER', ''),
#              'password': os.environ.get('DB_PASSWORD', ''),
#              'port': os.environ.get('DB_PORT', ''),
#             }
# development psql params
db_params = {'database': 'restapidevelopment',
             'host': 'localhost',
             'user': 'mateuszgrzybek',
             'password': '',
             'port': '',
            }

soup_pot = get_soup_pot()
authors = get_authors(soup_pot)

def connect(db_params, authors, soup_pot):
    words = get_words(authors, soup_pot)
    personal_words = words_per_author(words)
    total_words = total_words(words)
    conn = None
    try:
        # connect to the database
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**db_params)

        # create a cursor
        cursor = conn.cursor()

        # delete any existing records
        cursor.execute('DELETE FROM authors')
        cursor.execute('DELETE FROM personal_words')
        cursor.execute('DELETE FROM total_words')

        # insert scraped stats into the corresponding tables
        for author_id, author_name in authors.items():
            cursor.execute("""INSERT INTO authors (author_id, author_name)
                VALUES ('{}', '{}')""".format(author_id, author_name))

        for word, word_count in total_words.items():
            cursor.execute("""INSERT INTO total_words (word, word_count)
                VALUES ('{}', '{}')""".format(word, word_count)
                
        for author_id, authors_words in personal_words.items():
            for word, word_count in authors_words.items():
                cursor.execute("""INSERT INTO personal_words (author_id,
                    word, word_count) VALUES ('{}', '{}', '{}')""".format(
                    author_id, word, word_count))

        # commit the changes and close the connection
        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Connection closed.')


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
    connect(db_params, authors, soup_pot)
