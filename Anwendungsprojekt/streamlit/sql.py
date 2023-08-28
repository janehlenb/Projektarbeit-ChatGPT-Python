import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('weather.db')
cursor = conn.cursor()

# Tabelle erstellen (falls noch nicht vorhanden)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')
conn.commit()

# Daten speichern
def save_to_db(city):
    cursor.execute('INSERT INTO cities (name) VALUES (?)', (city,))
    conn.commit()

# Am häufigsten gesuchte Städte anzeigen
def most_searched_cities_db():
    cursor.execute('''
        SELECT name, COUNT(*) as count
        FROM cities
        GROUP BY name
        ORDER BY count DESC
        LIMIT 3
    ''')
    rows = cursor.fetchall()
    return [row[0] for row in rows]
