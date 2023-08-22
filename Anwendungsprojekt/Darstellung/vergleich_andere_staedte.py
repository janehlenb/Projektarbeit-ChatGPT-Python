import requests
import matplotlib.pyplot as plt

API_KEY = ""
CITIES = ["Bielefeld", "Lemgo", "Blomberg"]
URL_BASE = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=de&appid={}"

temperatures = []
humidities = []

for city in CITIES:
    url = URL_BASE.format(city, API_KEY)
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    humidity = data['main']['humidity']

    temperatures.append(temperature)
    humidities.append(humidity)

plt.figure(figsize=(10, 6))

plt.bar(CITIES, temperatures, label='Temperatur (°C)')
plt.plot(CITIES, humidities, marker='o', color='r', label='Luftfeuchtigkeit (%)')

plt.title("Vergleich von Temperatur und Luftfeuchtigkeit")
plt.xlabel("Städte")
plt.ylabel("Werte")
plt.legend()
plt.grid()
plt.show()