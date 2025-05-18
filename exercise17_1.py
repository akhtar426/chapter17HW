'''
Author: Anuss Akhtar
Date: 5/18/2025
Question 3 of the assignment (exercise 17.1)
'''

import sqlite3
import pandas as pd

# Connect to the database
connection = sqlite3.connect('books.db')
cursor = connection.cursor()

pd.options.display.max_columns = 10

# 1. Select all authors’ last names in descending order
print("=== 1. Authors’ Last Names (Descending) ===")
df1 = pd.read_sql("SELECT last FROM authors ORDER BY last DESC", connection)
print(df1)

# 2. Select all book titles in ascending order
print("\n=== 2. Book Titles (Ascending) ===")
df2 = pd.read_sql("SELECT title FROM titles ORDER BY title ASC", connection)
print(df2)

# 3. INNER JOIN: All books for a specific author (Paul Deitel)
print("\n=== 3. Books by Paul Deitel ===")
df3 = pd.read_sql("""
    SELECT titles.title, titles.copyright, titles.isbn
    FROM authors
    INNER JOIN author_ISBN ON authors.id = author_ISBN.id
    INNER JOIN titles ON author_ISBN.isbn = titles.isbn
    WHERE authors.first = 'Paul' AND authors.last = 'Deitel'
    ORDER BY titles.title
""", connection)
print(df3)

# 4. Insert a new author
print("\n=== 4. Inserting New Author: Lena Gray ===")
cursor.execute("""
    INSERT INTO authors (first, last)
    SELECT 'Lena', 'Gray'
    WHERE NOT EXISTS (
        SELECT 1 FROM authors WHERE first = 'Lena' AND last = 'Gray'
    )
""")
connection.commit()

# Get Lena's author ID
author_id = pd.read_sql("SELECT id FROM authors WHERE first = 'Lena' AND last = 'Gray'", connection).iloc[0, 0]
print(f"Inserted/Found Lena Gray with ID = {author_id}")

# 5. Insert new title and associate with Lena Gray
print("\n=== 5. Inserting New Book: Python Mastery ===")
cursor.execute("""
    INSERT OR IGNORE INTO titles (isbn, title, edition, copyright)
    VALUES ('9999999999', 'Python Mastery', 1, '2025')
""")
cursor.execute("""
    INSERT OR IGNORE INTO author_ISBN (id, isbn)
    VALUES (?, '9999999999')
""", (author_id,))
connection.commit()

# Confirm new book
print("\n=== Confirm Lena Gray’s Book ===")
df5 = pd.read_sql("""
    SELECT titles.title, titles.copyright, titles.isbn
    FROM titles
    INNER JOIN author_ISBN ON titles.isbn = author_ISBN.isbn
    INNER JOIN authors ON authors.id = author_ISBN.id
    WHERE authors.first = 'Lena' AND authors.last = 'Gray'
""", connection)
print(df5)

# Save full output to text file
with open("exercise17_1_output.txt", "w") as f:
    f.write("=== 1. Authors’ Last Names (Descending) ===\n")
    f.write(df1.to_string())
    f.write("\n\n=== 2. Book Titles (Ascending) ===\n")
    f.write(df2.to_string())
    f.write("\n\n=== 3. Books by Paul Deitel ===\n")
    f.write(df3.to_string())
    f.write(f"\n\n=== 4. Inserted/Found Lena Gray with ID = {author_id} ===\n")
    f.write("\n\n=== 5. Lena Gray’s Book ===\n")
    f.write(df5.to_string())

# Close the connection
connection.close()
