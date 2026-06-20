# Create a customers table
cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               )
               """)