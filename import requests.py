import requests

def get_cities(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()  # Assuming the response is a JSON array of city names
    else:
        raise Exception("Failed to fetch cities")

def get_weather(city, api_url):
    response = requests.get(f"{api_url}?city={city}")
    if response.status_code == 200:
        return response.json()  # Assuming the response contains weather details
    else:
        raise Exception(f"Failed to fetch weather for {city}")

def find_better_location(cities, condition, weather_api_url):
    best_city = None
    best_value = None

    for city in cities:
        weather = get_weather(city, weather_api_url)

        if condition == "hot":
            current_value = weather['temperature']
            if best_value is None or current_value > best_value:
                best_value = current_value
                best_city = city
        elif condition == "cold":
            current_value = weather['temperature']
            if best_value is None or current_value < best_value:
                best_value = current_value
                best_city = city
        elif condition == "windy":
            current_value = weather['wind_speed']
            if best_value is None or current_value > best_value:
                best_value = current_value
                best_city = city
        elif condition == "rainy":
            current_value = weather['rain_volume']
            if best_value is None or current_value > best_value:
                best_value = current_value
                best_city = city
        elif condition == "sunny":
            current_value = weather['cloud_coverage']
            if best_value is None or current_value < best_value:
                best_value = current_value
                best_city = city
        elif condition == "cloudy":
            current_value = weather['cloud_coverage']
            if best_value is None or current_value > best_value:
                best_value = current_value
                best_city = city

    return best_city

def main():
    cities_api_url = " https://quest.squadcast.tech/api/RA2111003040062/weather"
    weather_api_url = "https://quest.squadcast.tech/api/RA2111003040062/weather/get?q=city_name"
    
    condition = input("Enter the condition (hot, cold, windy, rainy, sunny, cloudy): ").strip().lower()

    try:
        cities = get_cities(cities_api_url)
        better_location = find_better_location(cities, condition, weather_api_url)
        print(f"The better location based on the condition '{condition}' is: {better_location}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()