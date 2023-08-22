import requests
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = ""
CITY = "Lemgo"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=metric&lang=de&appid={API_KEY}"

response = requests.get(URL)
data = response.json()

timestamps = []
temperatures = []

for entry in data['list']:
    timestamp = entry['dt']
    date_time = datetime.utcfromtimestamp(timestamp)
    temperature = entry['main']['temp']

    timestamps.append(timestamp)
    temperatures.append(temperature)

plt.figure(figsize=(10, 6))  # Vergrößere die Abbildung

# Plot der Daten mit Linie und Markern
plt.plot(timestamps, temperatures, marker='o', linestyle='-', color='tab:red', label='Temperatur')

plt.title(f"5-Tage-Temperaturvorhersage in {CITY}")
plt.xlabel("Datum und Uhrzeit")
plt.ylabel("Temperatur (°C)")

# Formatieren der x-Achsenbeschriftungen nach deutschem Datum und Uhrzeitformat
formatted_labels = [datetime.utcfromtimestamp(ts).strftime('%d.%m.%y %H:%M') for ts in timestamps]
# plt.xticks(timestamps, formatted_labels, rotation=45, ha='right', fontsize=8)
plt.xticks(timestamps, formatted_labels, rotation=90, ha='right')

plt.grid(True, linestyle='--', alpha=0.7)  # Hinzufügen von gestrichelten Gitterlinien
plt.tight_layout()

# Hinzufügen von Legende
plt.legend()

# Stilisierung der Achsen
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().tick_params(axis='both', which='both', direction='in', top=True, right=True)

plt.show()
