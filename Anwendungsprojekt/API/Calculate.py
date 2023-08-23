import requests
import datetime

# Deinen OpenWeatherMap API-Schlüssel hier eintragen
api_key = "8458a13ebaeba1acef15ef61c32b8d4e"

# Die gewünschte Stadt und Ländercode (z.B. "Berlin,de")
city = "Berlin,de"

# Die Basis-URL für die OpenWeatherMap API
base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

# Listen für die einzelnen Daten
timestamps = []
temperatures = []
temp_mins = []
temp_maxs = []
wind_speeds = []
wind_gusts = []

# Heutiges Datum
today = datetime.datetime.now()

# API-Anfrage senden
response = requests.get(base_url)
data = response.json()

# Daten verarbeiten
for entry in data['list']:
    # Zeitpunkt des Datensatzes
    timestamp = datetime.datetime.fromtimestamp(entry['dt'])
    
    # Nur Daten für die nächsten 5 Tage berücksichtigen
    if today.date() <= timestamp.date() <= today.date() + datetime.timedelta(days=4):
        temperature = entry['main']['temp']
        temp_min = entry['main']['temp_min']
        temp_max = entry['main']['temp_max']
        wind_speed = entry['wind']['speed']
        wind_gust = entry['wind'].get('gust', 0)  # gust ist nicht immer vorhanden
        
        timestamps.append(timestamp)
        temperatures.append(temperature)
        temp_mins.append(temp_min)
        temp_maxs.append(temp_max)
        wind_speeds.append(wind_speed)
        wind_gusts.append(wind_gust)

# Ergebnisse ausgeben
for i in range(len(timestamps)):
    print(f"Datum/Uhrzeit: {timestamps[i]}")
    print(f"Temperatur: {temperatures[i]}°C")
    print(f"Min. Temperatur: {temp_mins[i]}°C")
    print(f"Max. Temperatur: {temp_maxs[i]}°C")
    print(f"Windgeschwindigkeit: {wind_speeds[i]} m/s")
    print(f"Böengeschwindigkeit: {wind_gusts[i]} m/s")
    print("-------------------------------")
