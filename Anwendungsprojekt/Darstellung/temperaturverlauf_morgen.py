import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

API_KEY = ""
CITY = "Lemgo"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=metric&lang=de&cnt=8&appid={API_KEY}"

response = requests.get(URL)
data = response.json()

tomorrow = (datetime.now() + timedelta(days=1)).date()
tomorrow_temperatures = []

for entry in data['list']:
    timestamp = entry['dt']
    entry_date = datetime.utcfromtimestamp(timestamp).date()

    if entry_date == tomorrow:
        time = datetime.utcfromtimestamp(timestamp).strftime('%H:%M')
        temperature = entry['main']['temp']
        tomorrow_temperatures.append((time, temperature))

times, temperatures = zip(*tomorrow_temperatures)

plt.figure(figsize=(10, 6))  # Vergrößere die Abbildung

# Plot der Daten mit Linie und Markern
plt.plot(times, temperatures, marker='o', color='tab:red', label='Temperatur')

plt.title(f"Temperaturverlauf morgen in {CITY}", fontsize=16)
plt.xlabel("Uhrzeit", fontsize=12)
plt.ylabel("Temperatur (°C)", fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

plt.grid(True, linestyle='--', alpha=0.7)  # Hinzufügen von gestrichelten Gitterlinien
plt.tight_layout()

# Hinzufügen von Legende
plt.legend()

# Stilisierung der Achsen
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().tick_params(axis='both', which='both', direction='in', top=True, right=True)

plt.show()
