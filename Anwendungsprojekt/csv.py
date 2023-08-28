import csv
import yaml

# Daten speichern
def save_to_csv(city):
    with open('cities.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([city])

def save_to_yaml(city):
    cities = []
    try:
        with open('cities.yaml', 'r') as file:
            cities = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        pass

    cities.append(city)
    with open('cities.yaml', 'w') as file:
        yaml.dump(cities, file)

# Am häufigsten gesuchte Städte anzeigen
def most_searched_cities_csv():
    cities = {}
    with open('cities.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            city = row[0]
            cities[city] = cities.get(city, 0) + 1

    return sorted(cities, key=cities.get, reverse=True)[:3]

def most_searched_cities_yaml():
    cities = {}
    try:
        with open('cities.yaml', 'r') as file:
            cities = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        pass
    
    city_count = {}
    for city in cities:
        city_count[city] = city_count.get(city, 0) + 1
    
    return sorted(city_count, key=city_count.get, reverse=True)[:3]
