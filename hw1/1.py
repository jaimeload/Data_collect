import json
import requests

client_id = "__"
client_secret = "__"

endpoint = "https://api.foursquare.com/v3/places/search"

city = input("Введите город: ")
place = input("Введите место: ")

params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "near": city,
    "query": place
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}

response = requests.get(endpoint, params=params, headers=headers)

if response.status_code == 200:
    print("Success")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        print("Название:", venue["name"])
        print("Адрес:", venue["location"]["address"])
        print("Координаты:", venue["geocodes"]["main"]["latitude"], venue["geocodes"]["main"]["longitude"])
        print("\n")
else:
    print("Error")
    print(response.status_code)