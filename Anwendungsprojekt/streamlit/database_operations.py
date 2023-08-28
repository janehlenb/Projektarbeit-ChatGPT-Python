import sqlite3

# Verbindung zur Datenbank herstellen
def connect_to_database():
    conn = sqlite3.connect('weather.db')
    return conn

# Daten speichern
def save_to_db(city):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO cities (name) VALUES (?)', (city,))
    conn.commit()
    conn.close()

# Am häufigsten gesuchte Städte abrufen
def most_searched_cities_db(limit=3):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, COUNT(*) as count
        FROM cities
        GROUP BY name
        ORDER BY count DESC
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [row[0] for row in rows]