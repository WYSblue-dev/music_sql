import sqlite3

# This creates a new database file called bookstore.db
# If the file already exists, it connects to it
# This is creating a database(.db) file that can be thought of as a excel sheet
connection = sqlite3.connect("bookstore.db")

# A cursor is what you use to execute SQL commands
# Why do have to have a cursor?
# What is it's purpose?
cursor = connection.cursor()

print("Connected to database!")

# Create a customers table
# DO NOT LEAVE TRAILING COMMAS WHEN WRITING
cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               email TEXT UNIQUE NOT NULL
               )
               """)

connection.commit()
print("Customers table created!")

"""
CREATE TABLE IF NOT EXISTS - Make a new table, but don't crash if it already
exists
id INTEGER PRIMARY KEY AUTOINCREMENT - An integer column that automatically
assigns the next number (1,2,3...) to each new row
name TEXT NOT NULL - A text colum that cannot be left empty
email TEXT UNIQUW NOT NULL - A text column that must be unique across all rows
and cannot be empty

These rules (NOT NULL, UNIQUE) are called contraints. They're the database 
enforcing dat quality for you.
"""

cursor.execute("""
               INSERT INTO customers (name, email)
               VALUES ('James Chen', 'james@email.com')
            """)

# Inset multiple customers at once
more_customers = [
    ("Aisha Johnson", "aisha@email.com"),
    ("David Kim", "david@email.com"),
]
cursor.executemany("""
    INSERT INTO customers (name, email) VALUES (?, ?)
""", more_customers)
# Notice the ? placeholders in executemany. These are parameterized queries;
# they prevent a security vulnerability called SQL injection. Never build SQL
# strings with f-strings or string concatenation. Always use ? placeholders.
connection.commit()
print("Customers inserted!")

cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

# We get a integrity error when a unique not null
# fails. Happens if we populate the data once and try to
# run it again.
print("\nAll customers:")
for row in rows:
    print(f"    ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")

# why do we use the .close? Also we're using it on the cursor Obj right?
connection.close()
print("\nConnection closed.")

# You just created a database, defined a schema with constraints, inserted data
# safely, and queried it back. That's the foundation everything else in this 
# module builds on.

# What I think the process looks like.

"""
Create a connection to a database.....(file with the tables)
By create a connection I mean create a Connection python obj.
Then if we want to make changes we use the Cursor class obj of Connection.
For convience we will assign this to a name var cursor = connection.cursor()
Once we have the Cursor obj instance in place we can run the commands to CRUD
the schema, add data to the table and it's corresponding schema, and queried
(.get the data.) the data.
We use .execute or .executemany to make changes to the schema. We use the
.commit() to commit the changes to the database. Make sense when thinking about
django now. We could look at the django db that is popullated and think about
it more in depth now.
# what does the cursor.execute('SELECT * FROM customers)???
# I'm assume is needed to someone get the data from the corresponding table.
# The wild card * is used as a catch/get all.
Then we want to query the data we
must use the .fetchall() in a for loops of the rows var. That gives us all the
rows/instances of the table through the iteration. We can access the rows
since we have them selected and assiged to our variable rows.

# Why do we have to close? Is this something that has to be done? Data 
# corruption or for malice?
we then close the database with .close()

connection = sqlite.connect("file.db")
    cursor = connection.cursor()
        execute - initial table setup
        commit - save the table setup
        execute/executemany - insert(create) data in specified(use placeholders)
        commit - save the data insert
        rows = cursor.featchall(SELECT * FROM table)
        for row in rows:
            print(f"{row[0]}") # print the row(instance) attribute/feild/colum
connection.close()
"""