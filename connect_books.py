import sqlite3
import pandas as pd

# Connect to the books.db database
connection = sqlite3.connect('books.db')

# Optional: Display more columns if needed
pd.options.display.max_columns = 10

# View authors table

print("=== Authors Table ===")
df_authors = pd.read_sql('SELECT * FROM authors', connection, index_col='id')
print(df_authors)


# View titles table

print("\n=== Titles Table ===")
df_titles = pd.read_sql('SELECT * FROM titles', connection)
print(df_titles)


# View author_ISBN table (first 5 rows)

print("\n=== Author_ISBN Table (first 5 rows) ===")
df_author_isbn = pd.read_sql('SELECT * FROM author_ISBN', connection)
print(df_author_isbn.head())


# View only first and last names from authors

print("\n=== Authors (First and Last Names Only) ===")
df_author_names = pd.read_sql('SELECT first, last FROM authors', connection)
print(df_author_names)


# View books with copyright year > 2016

print("\n=== Books with Copyright After 2016 ===")
df_recent_books = pd.read_sql("""
    SELECT title, edition, copyright
    FROM titles
    WHERE copyright > '2016'
""", connection)
print(df_recent_books)


# Pattern match: Last names starting with 'D'

print("\n=== Authors Whose Last Name Starts with 'D' ===")
df_authors_d = pd.read_sql("""
    SELECT id, first, last
    FROM authors
    WHERE last LIKE 'D%'
""", connection, index_col='id')
print(df_authors_d)


# Pattern match: First names matching '_b%'

print("\n=== Authors Whose First Name Matches '_b%' Pattern ===")
df_first_match = pd.read_sql("""
    SELECT id, first, last
    FROM authors
    WHERE first LIKE '_b%'
""", connection, index_col='id')
print(df_first_match)


# Order titles by title (ascending)

print("\n=== Titles Ordered Alphabetically ===")
df_titles_sorted = pd.read_sql("""
    SELECT title
    FROM titles
    ORDER BY title ASC
""", connection)
print(df_titles_sorted)


# Order authors by last name, then first name (ascending)

print("\n=== Authors Ordered by Last, Then First Name ===")
df_authors_sorted = pd.read_sql("""
    SELECT id, first, last
    FROM authors
    ORDER BY last, first
""", connection, index_col='id')
print(df_authors_sorted)


# Order authors by last name (descending), then first name (ascending)

print("\n=== Authors Ordered by Last Name DESC, First Name ASC ===")
df_authors_sorted_desc = pd.read_sql("""
    SELECT id, first, last
    FROM authors
    ORDER BY last DESC, first ASC
""", connection, index_col='id')
print(df_authors_sorted_desc)


# Combine WHERE and ORDER BY: Titles ending with 'How to Program'

print("\n=== Books with Titles Ending in 'How to Program', Ordered by Title ===")
df_how_to_program_books = pd.read_sql("""
    SELECT isbn, title, edition, copyright
    FROM titles
    WHERE title LIKE '%How to Program'
    ORDER BY title
""", connection)
print(df_how_to_program_books)


# INNER JOIN: Authors with their book ISBNs

print("\n=== Authors and Their Book ISBNs (INNER JOIN) ===")
df_authors_isbns = pd.read_sql("""
    SELECT first, last, isbn
    FROM authors
    INNER JOIN author_ISBN
        ON authors.id = author_ISBN.id
    ORDER BY last, first
""", connection)
print(df_authors_isbns.head())


# INSERT INTO: Add Sue Red only if not already present

print("\n=== Inserting a New Author: Sue Red (if not already exists) ===")
cursor = connection.cursor()
cursor.execute("""
    INSERT INTO authors (first, last)
    SELECT 'Sue', 'Red'
    WHERE NOT EXISTS (
        SELECT 1 FROM authors WHERE first = 'Sue' AND last = 'Red'
    )
""")
connection.commit()


# UPDATE: Change Sue Red's last name to Black

print("\n=== Updating Sue Red's Last Name to Black ===")
cursor.execute("""
    UPDATE authors
    SET last = 'Black'
    WHERE first = 'Sue' AND last = 'Red'
""")
print(f"Rows updated: {cursor.rowcount}")
connection.commit()


# DELETE: Remove all entries for Sue Black

print("\n=== Deleting All Sue Black Entries from Authors ===")
cursor.execute("""
    DELETE FROM authors
    WHERE first = 'Sue' AND last = 'Black'
""")
print(f"Rows deleted: {cursor.rowcount}")
connection.commit()

# Verify the deletion
print("\n=== Updated Authors Table After Deletion ===")
df_final_authors = pd.read_sql("""
    SELECT id, first, last
    FROM authors
""", connection, index_col='id')
print(df_final_authors)

# Save output to a text file
with open("output.txt", "w") as f:
    f.write(df_final_authors.to_string())

# Close the connection
connection.close()

