import sqlite3

connection = sqlite3.connect("musicians.db")

# create 2 artists(id, name(text, not null), genre)

cursor = connection.cursor()
# sqlite3 doesn't auto accept foreign_keys
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS artist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                genre TEXT NOT NULL
               )
               """)

connection.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS album (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               year INTEGER,
               artist_id INTEGER NOT NULL,
               FOREIGN KEY (artist_id) REFERENCES artist(id)
               )
""")

connection.commit()

# add 3 artist here with insert
cursor.execute("""
    INSERT INTO artist (name, genre)
    VALUES ('Tyler Childers', 'Appalachian Country')
"""
)
more_artists = ('Stevie Ray Vaughan', 'Texas Blues'), ('B.B. King', 'Electric Blues')
cursor.executemany("""
    INSERT INTO artist (name, genre) VALUES (?, ?)
""", more_artists)
# commit the artist that we have inserted into the table
connection.commit()

albums = [
    ("Purgatory", 2017, "Tyler Childers"),
    ("Country Squire", 2019, "Tyler Childers"),
    ("Long Violent History", 2020, "Tyler Childers"),
    ("Can I Take My Hounds to Heaven?", 2022, "Tyler Childers"),
    ("Rustin' in the Rain", 2023, "Tyler Childers"),
    ("Texas Flood", 1983, "Stevie Ray Vaughan"),
    ("Couldn't Stand the Weather", 1984, "Stevie Ray Vaughan"),
    ("In Step", 1989, "Stevie Ray Vaughan"),
    ("Live at the Regal", 1965, "B.B. King"),
    ("Completely Well", 1969, "B.B. King"),
    ("Indianola Mississippi Seeds", 1970, "B.B. King"),
]
cursor.executemany("""
    INSERT INTO album (title, year, artist_id)
    VALUES (
            ?,
            ?,
            (SELECT id FROM artist WHERE name = ?)
        )
""", albums)

connection.commit()
cursor.execute("SELECT * FROM artist")
artists = cursor.fetchall()
cursor.execute("SELECT * FROM album")
albums = cursor.fetchall()
for artist in artists:
    print(f"Name - {artist[1]}\nGenre - {artist[2]}\n{'Albums':^60}")
    for album in albums:
        if album[3] == artist[0]:
            print(f"{album[1]:^60}")

# close the database connection. Make me think of correctly closing a file.
connection.close()

# albums(id(primarykey, autoincrement) title(text, not null), year(integer),
# artist_id(integer, foreign key refrencing(artist.id)))

# add 3 artist by execute(instert); then commit() to the database
# (makemigrations)
# query the data by using the cursor select * from table inside the fetchall()
# and interation with a f string through the rows of the selected
# close the connection.

# To create a foreign key in SQLite, add FOREIGN KEY (artist_id) REFERENCES
# artists(id) at the end of your CREATE TABLE statement for albums. Also, make
# sure to enable foreign key enforcement by running
# cursor.execute("PRAGMA foreign_keys = ON") right after connecting — SQLite
# doesn't enforce foreign keys by default.

# When working with this and thiking about it I thought a lot of the sqlite3 
# database that django creates. I didn't relize that djanogo was handling this
# database on the backend the way it does. Means the commands are just working
# with a python standard library package and its classes/methods.