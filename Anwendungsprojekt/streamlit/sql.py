import sqlite3

# Verbindung zur Datenbank herstellen
def create_connection():
    conn = sqlite3.connect('weather.db')
    return conn

# Tabelle erstellen (falls noch nicht vorhanden)
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Daten speichern
def save_to_db(city):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cities (name) VALUES (?)', (city,))
    conn.commit()
    conn.close()

# Am häufigsten gesuchte Städte anzeigen
def most_searched_cities_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, COUNT(*) as count
        FROM cities
        GROUP BY name
        ORDER BY count DESC
        LIMIT 3
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
