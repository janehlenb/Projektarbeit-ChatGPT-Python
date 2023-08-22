import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

API_KEY = ""
CITY = "Lemgo"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=metric&lang=de&cnt=8&appid={API_KEY}"

response = requests.get(URL)
data = response.json()

tomorrow = (datetime.now() + timedelta(days=1)).date()
weather_counts = {}

for entry in data['list']:
    timestamp = entry['dt']
    entry_date = datetime.utcfromtimestamp(timestamp).date()

    if entry_date == tomorrow:
        weather = entry['weather'][0]['description']

        if weather not in weather_counts:
            weather_counts[weather] = 1
        else:
            weather_counts[weather] += 1

labels = list(weather_counts.keys())
values = list(weather_counts.values())

plt.figure(figsize=(10, 6))  # Vergrößere die Abbildung

# Explode, um den Hervorhebungseffekt zu erzeugen
explode = [0.1] * len(values)

# Farbpalette für die Sektoren
colors = plt.cm.Paired.colors

# Plot des Kreisdiagramms mit verbesserter Darstellung
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140,
        colors=colors, explode=explode, shadow=True, textprops={'fontsize': 10})

plt.title(f"Verteilung der Wetterzustände morgen in {CITY}", fontsize=16)
plt.axis('equal')  # Sorgt dafür, dass das Diagramm rund ist
plt.tight_layout()

plt.show()
