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
weather_icon_codes = []

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
        weather_icon_code = entry['weather'][0]['icon']

        timestamps.append(timestamp)
        temperatures.append(temperature)
        temp_mins.append(temp_min)
        temp_maxs.append(temp_max)
        wind_speeds.append(wind_speed)
        wind_gusts.append(wind_gust)
        weather_icon_codes.append(weather_icon_code)

        icon_base_url = "http://openweathermap.org/img/w/"

        weather_icons = {
                    '01d': f"{icon_base_url}01d.png",  # clear sky (day)
                    '01n': f"{icon_base_url}01n.png",  # clear sky (night)
                    '02d': f"{icon_base_url}02d.png",  # few clouds (day)
                    '02n': f"{icon_base_url}02n.png",  # few clouds (night)
                    '03d': f"{icon_base_url}03d.png",  # scattered clouds
                    '03n': f"{icon_base_url}03n.png",  # scattered clouds
                    '04d': f"{icon_base_url}04d.png",  # broken clouds
                    '04n': f"{icon_base_url}04n.png",  # broken clouds
                    '09d': f"{icon_base_url}09d.png",  # shower rain
                    '09n': f"{icon_base_url}09n.png",  # shower rain
                    '10d': f"{icon_base_url}10d.png",  # rain
                    '10n': f"{icon_base_url}10n.png",  # rain
                    '11d': f"{icon_base_url}11d.png",  # thunderstorm
                    '11n': f"{icon_base_url}11n.png",  # thunderstorm
                    '13d': f"{icon_base_url}13d.png",  # snow
                    '13n': f"{icon_base_url}13n.png",  # snow
                    '50d': f"{icon_base_url}50d.png",  # mist
                    '50n': f"{icon_base_url}50n.png"   # mist
                }
# Ergebnisse ausgeben
for i in range(len(timestamps)):
    print(f"Datum/Uhrzeit: {timestamps[i]}")
    print(f"Temperatur: {temperatures[i]}°C")
    print(f"Min. Temperatur: {temp_mins[i]}°C")
    print(f"Max. Temperatur: {temp_maxs[i]}°C")
    print(f"Windgeschwindigkeit: {wind_speeds[i]} m/s")
    print(f"Böengeschwindigkeit: {wind_gusts[i]} m/s")
    print(f"Wetter-Icon: {weather_icon_codes[i]}")
    print(f"Weather Icon URL: {weather_icons[weather_icon_codes[i]]}")
    print("-------------------------------")
