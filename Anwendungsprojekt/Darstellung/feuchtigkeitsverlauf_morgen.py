import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

API_KEY = ""
CITY = "Lemgo"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=metric&lang=de&appid={API_KEY}"

response = requests.get(URL)
data = response.json()

tomorrow = (datetime.now() + timedelta(days=1)).date()
humidity_data = []

for entry in data['list']:
    timestamp = entry['dt']
    entry_date = datetime.utcfromtimestamp(timestamp).date()

    if entry_date == tomorrow:
        time = datetime.utcfromtimestamp(timestamp).strftime('%H:%M')
        humidity = entry['main']['humidity']
        humidity_data.append((time, humidity))

times, humidity_values = zip(*humidity_data)

plt.figure(figsize=(10, 6))

plt.plot(times, humidity_values, marker='o', color='tab:blue', label='Luftfeuchtigkeit')

plt.title(f"Luftfeuchtigkeitsverlauf morgen in {CITY}", fontsize=16)
plt.xlabel("Uhrzeit", fontsize=12)
plt.ylabel("Luftfeuchtigkeit (%)", fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

plt.legend()

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().tick_params(axis='both', which='both', direction='in', top=True, right=True)

plt.show()