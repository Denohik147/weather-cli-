import requests

def get_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"

# Параметры запроса
    params = {
        "name": city,
        "count": 1,
        "language" : "en",
        "format": "json"
    }

    try:
    # Отправляем GET-запрос серверу
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

    # Преобразуем JSON-ответ в словарь Python
        data = response.json()

        if not data.get("results"):
            return None

        return data["results"][0]

    except requests.RequestException:
        print("Ошибка подключения")
        return None


def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "Europe/Chisinau",
        "current_weather": True
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        return response.json()

    except requests.RequestException:
        print("Ошибка подключения")
        return None

weather_codes = {
    0: "☀️ Ясно",
    1: "🌤 Преимущественно ясно",
    2: "⛅ Переменная облачность",
    3: "☁️ Пасмурно",
    61: "🌧 Дождь",
    71: "🌨 Снег"
}

# Проверяем, есть ли в ответе текущая погода
def show_weather(data, city):
    if not data:
        return

    weather = data["current_weather"]
    code = weather["weathercode"]

    wind = weather["windspeed"] / 3.6

    #Выводим результат
    print(f"📍 {city}")
    print(f"🌡 {weather['temperature']}°C")
    print(f"🌤 {weather_codes.get(code, 'Неизвестно')}")
    print(f"💨 {wind:.1f} м/c")
    print(f"🕒 {weather['time']}")


city = input("Введите город: ")

location = get_coordinates(city)

if location is None:
    print("Город не найден")
else:
    lat = location.get("latitude")
    lon = location.get("longitude")

    if lat is None or lon is None:
        print("Не удалось получить координаты")
    else:
        data = get_weather(lat, lon)
        show_weather(data, city)
