import requests

url = 'https://v2.jokeapi.dev/joke/Any?type=single'  # JokeAPI endpoint for one-liners

try:
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        joke = data['joke']
        print(joke)
    else:
        print("Failed to fetch a joke.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
