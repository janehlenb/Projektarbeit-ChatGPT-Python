import requests

API_KEY = '8458a13ebaeba1acef15ef61c32b8d4e'
city_name = 'London'  # Replace with the city name for which you want weather information

url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'

try:
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        current_temp = data['main']['temp']
        max_temp = data['main']['temp_max']
        min_temp = data['main']['temp_min']

        current_wind_speed = data['wind']['speed']  # Extract wind speed
        current_humidity = data['main']['humidity']  # Extract humidity
        weather_description = data['weather'][0]['description']  # Extract weather description
        weather_icon = data['weather'][0]['icon']  # Extract weather icon code

        print(f"Current Temperature in {city_name}: {current_temp}°C")
        print(f"Max Temperature in {city_name}: {max_temp}°C")
        print(f"Min Temperature in {city_name}: {min_temp}°C")
        print(f"Current Wind Speed in {city_name}: {current_wind_speed} m/s")
        print(f"Current Humidity in {city_name}: {current_humidity}%")
        print(f"Weather Description in {city_name}: {weather_description}")

Using the weather icon code to construct the icon URL
        icon_url = f"http://openweathermap.org/img/w/%7Bweather_icon%7D.png"
        print(f"Weather Icon URL: {icon_url}")

    else:
        print(f"Error: {data['message']}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


