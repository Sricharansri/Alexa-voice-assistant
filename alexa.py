import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import requests

# Initialize
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)  # Female voice

# Your OpenWeatherMap API key
weather_api_key = "YOUR_API_KEY"  # Replace with your actual API key

def engine_talk(text):
    print("[Voice]:", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 404:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The current temperature in {city} is {temp}°C with {desc}."
        else:
            return f"City '{city}' not found."
    except Exception as e:
        print("Weather error:", e)
        return "Couldn't fetch weather info."

def user_commands():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = listener.listen(source)
            command = listener.recognize_google(audio)
            command = command.lower()
            print("You said:", command)

            if 'alexa' in command:
                engine_talk("You said " + command)
                return command
            else:
                engine_talk("I didn't hear Alexa in your command.")
                return ""
    except Exception as e:
        print("Speech recognition error:", e)
        engine_talk("Sorry, I couldn't understand.")
        return ""

def run_alexa():
    command = user_commands()

    if 'play' in command:
        song = command.replace('alexa', '').replace('play', '').strip()
        engine_talk("Opening YouTube for " + song)
        url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
        return url

    elif 'how are you' in command:
        engine_talk("I'm doing great, thank you!")

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        engine_talk("The current time is " + time)

    elif 'weather in' in command:
        city = command.split("weather in")[-1].strip()
        weather = get_weather(city)
        engine_talk(weather)

    elif 'who is' in command or 'what is' in command:
        query = command.replace("alexa", "").replace("who is", "").replace("what is", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            engine_talk(result)
        except:
            engine_talk("Sorry, I couldn't find anything on Wikipedia.")
    else:
        engine_talk("I could not recognize your command.")

    return None
