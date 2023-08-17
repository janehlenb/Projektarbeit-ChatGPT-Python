import requests

API_KEY = '8458a13ebaeba1acef15ef61c32b8d4e'
city_name = 'London'  # Replace with the city name for which you want weather forecast

url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric'

try:
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        forecast_list = data['list']

        min_temps = []
        max_temps = []

        for forecast in forecast_list[:5]:  # Extract temperatures for the next 5 days
            min_temp = forecast['main']['temp_min']
            max_temp = forecast['main']['temp_max']

            min_temps.append(min_temp)
            max_temps.append(max_temp)

        print(f"Min Temperatures: {min_temps}")
        print(f"Max Temperatures: {max_temps}")

    else:
        print(f"Error: {data['message']}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
