import requests
import datetime

# Deinen OpenWeatherMap API-Schlüssel hier eintragen
api_key = "8458a13ebaeba1acef15ef61c32b8d4e"

# Die gewünschte Stadt und Ländercode (z.B. "Berlin,de")
city = "Berlin"

# Die Basis-URL für die OpenWeatherMap API
forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=de"

# Listen für die einzelnen Daten
timestamps = []
temperatures = []
temp_mins = []
temp_maxs = []
wind_speeds = []
wind_gusts = []
min_temps_per_day = []
max_temps_per_day = []
icon_urls_per_day = []



# Heutiges Datum
today = datetime.datetime.now()

# API-Anfrage senden
response = requests.get(forecast_url)
data = response.json()

# Daten verarbeiten
current_day = None
min_temp_day = float('inf')
max_temp_day = float('-inf')

for entry in data['list']:
    # Zeitpunkt des Datensatzes
    timestamp = datetime.datetime.fromtimestamp(entry['dt'])
    
    # Nur Daten für die nächsten 5 Tage berücksichtigen
    if today.date() <= timestamp.date() <= today.date() + datetime.timedelta(days=4):
        if current_day is None:
            current_day = timestamp.date()
        elif current_day != timestamp.date():
            min_temps_per_day.append(min_temp_day)
            max_temps_per_day.append(max_temp_day)
            min_temp_day = float('inf')
            max_temp_day = float('-inf')
            current_day = timestamp.date()
        
        temperature = entry['main']['temp']
        temp_min = entry['main']['temp_min']
        temp_max = entry['main']['temp_max']
        wind_speed = entry['wind']['speed']
        wind_gust = entry['wind'].get('gust', 0)  # gust ist nicht immer vorhanden
        weather_icon = entry['weather'][0]['icon']
        
        timestamps.append(timestamp)
        temperatures.append(temperature)
        temp_mins.append(temp_min)
        temp_maxs.append(temp_max)
        wind_speeds.append(wind_speed)
        wind_gusts.append(wind_gust)
        
        min_temp_day = min(min_temp_day, temp_min)
        max_temp_day = max(max_temp_day, temp_max)

# Füge die Temperaturen des letzten Tages hinzu
min_temps_per_day.append(min_temp_day)
max_temps_per_day.append(max_temp_day)

base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=de"

# API-Anfrage senden
response = requests.get(base_url)
data = response.json()

# Wetterdaten aus API-Daten extrahieren
temperature = data['main']['temp']
humidity = data['main']['humidity']
wind_speed = data['wind']['speed']
weather_icon = data['weather'][0]['icon']
icon_url = f"http://openweathermap.org/img/w/{weather_icon}.png"
summary = data['weather'][0]['description']

# Ergebnisse in Variablen speichern
current_temperature = temperature
current_humidity = humidity
current_wind_speed = wind_speed
current_icon_url = icon_url
current_summary = summary

# Ergebnisse ausgeben
for i in range(len(timestamps)):
    print(f"Datum/Uhrzeit: {timestamps[i]}")
    print(f"Temperatur: {temperatures[i]}°C")
    print(f"Min. Temperatur: {temp_mins[i]}°C")
    print(f"Max. Temperatur: {temp_maxs[i]}°C")
    print(f"Windgeschwindigkeit: {wind_speeds[i]} m/s")
    print(f"Böengeschwindigkeit: {wind_gusts[i]} m/s")
    print("-------------------------------")

for i in range(len(min_temps_per_day)):
    print(f"Tag {i + 1}: Min. Temperatur: {min_temps_per_day[i]}°C, Max. Temperatur: {max_temps_per_day[i]}°C")

print(f"Aktuelle Temperatur: {current_temperature}°C")
print(f"Luftfeuchtigkeit: {current_humidity}%")
print(f"Windgeschwindigkeit: {current_wind_speed} m/s")
print(f"Wetter-Icon URL: {current_icon_url}")
print(f"Zusammenfassung: {current_summary}")
