from dotenv import load_dotenv
import anthropic
import requests
import os

load_dotenv() 
def get_weather_forecast(city: str) ->list:
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial&cnt=7"
    response = requests.get(url)
    data = response.json()
    return data["list"]

def analyze_schedule(forecast: list) -> str:
    forecast_text = ""
    for day in forecast:
        temp = day["main"]["temp"]
        weather = day["weather"][0]["description"]
        date = day["dt_txt"]
        forecast_text += f"{date}: {temp}°F, {weather}\n"

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"You are an HVAC scheduling assistant. Based on this weather forecast, recommend the best days to send maintenance crews. Avoid extreme heat above 95°F and bad weather. Be specific and brief.\n\nForecast:\n{forecast_text}"
            }
        ]
    )
    return message.content[0].text

city = "Austin, Texas"
forecast = get_weather_forecast(city)
recommendation = analyze_schedule(forecast)

print(f"HVAC Scheduling Recommendation for {city}:")
print(recommendation)