import tkinter as tk
from tkinter import ttk
import time
import random
import threading
import speech_recognition as sr
from gtts import gTTS
import io
import pygame
import webbrowser
import pywhatkit
import pyjokes
import requests
from googlesearch import search
import pyautogui
import subprocess
import os
import pyautogui         
import psutil            
import winshell          
import subprocess        
import randomfacts
import math


# === Init GUI ===
root = tk.Tk()
root.title("Phoenix AI Interface")
root.attributes('-fullscreen', True)
root.configure(bg="#000000")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="#000000", highlightthickness=0)
canvas.pack(fill="both", expand=True)

center_x = screen_width // 2
center_y = screen_height // 2 - 40
circle_radius = 160
max_ripple_radius = 240

# === Grid Background ===
for i in range(0, screen_width, 80):
    canvas.create_line(i, 0, i, screen_height, fill="#002200")
for j in range(0, screen_height, 80):
    canvas.create_line(0, j, screen_width, j, fill="#002200")

# === Falling Dots ===
dots = []
for _ in range(200):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    speed = random.uniform(0.2, 0.8)
    dot = canvas.create_oval(x, y, x + 2, y + 2, fill="#00ff66", outline="")
    dots.append((dot, speed))

def animate_dots():
    for i in range(len(dots)):
        dot, speed = dots[i]
        x1, y1, x2, y2 = canvas.coords(dot)
        y1 += speed
        y2 += speed
        if y1 > screen_height:
            y1 = -2
            y2 = 0
        canvas.coords(dot, x1, y1, x2, y2)
    root.after(30, animate_dots)

animate_dots()

# === Ripple Animation ===
circle = canvas.create_oval(center_x - circle_radius,
                            center_y - circle_radius,
                            center_x + circle_radius,
                            center_y + circle_radius,
                            outline="#00ff66", width=3)

ripple_circles = []
ripple_count = 4
for i in range(ripple_count):
    ripple = canvas.create_oval(center_x - circle_radius,
                                 center_y - circle_radius,
                                 center_x + circle_radius,
                                 center_y + circle_radius,
                                 outline="#007744", width=1)
    ripple_circles.append(ripple)

def animate_ripples():
    current_time = time.time()
    for i, ripple in enumerate(ripple_circles):
        r = circle_radius + (current_time * 50 + i * 50) % (max_ripple_radius - circle_radius)
        alpha = int(255 - (r - circle_radius) / (max_ripple_radius - circle_radius) * 255)
        color = f'#00{int(alpha):02x}{88:02x}'
        canvas.coords(ripple, center_x - r, center_y - r, center_x + r, center_y + r)
        canvas.itemconfig(ripple, outline=color)
    root.after(30, animate_ripples)

animate_ripples()

canvas.create_text(center_x, center_y + circle_radius + 140,
                   text="P H E O N I X", font=("Orbitron", 38, "bold"), fill="#00ff66")

# === Clock and Date ===
time_label = tk.Label(root, font=("Consolas", 24, "bold"), bg="#000000", fg="#00ff99")
time_label.place(relx=0.92, rely=0.08, anchor="center")

date_label = tk.Label(root, font=("Consolas", 24, "bold"), bg="#000000", fg="#00ff99")
date_label.place(relx=0.08, rely=0.08, anchor="center")

def update_time():
    time_label.config(text=time.strftime("%H:%M:%S"))
    date_label.config(text=time.strftime("%d %B %Y"))
    root.after(1000, update_time)

update_time()

# === Log Box ===
style = ttk.Style()
style.theme_use('clam')
style.configure("Vertical.TScrollbar", troughcolor="#002200", background="#00ff66",
                bordercolor="#001100", arrowcolor="#00ff66", relief="flat", width=12)

log_frame = tk.Frame(root, bg="#001100")
log_frame.place(relx=0.82, rely=0.5, anchor="center", relwidth=0.3, relheight=0.6)

text_scroll_frame = tk.Frame(log_frame, bg="#001100")
text_scroll_frame.pack(expand=True, fill='both', padx=10, pady=10)

log_box = tk.Text(text_scroll_frame, font=("Consolas", 12), bg="#000000", fg="#00ff99",
                  insertbackground="#00ff99", wrap=tk.WORD, state='disabled', relief="flat")
log_box.pack(side=tk.LEFT, expand=True, fill='both')

scrollbar = ttk.Scrollbar(text_scroll_frame, style="Vertical.TScrollbar", orient="vertical", command=log_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_box.config(yscrollcommand=scrollbar.set)

def log_message(sender, message):
    log_box.config(state='normal')
    log_box.insert(tk.END, f"{sender}: {message}\n")
    log_box.config(state='disabled')
    log_box.see(tk.END)

# === Escape Key to Exit Fullscreen ===
def exit_fullscreen(event):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

# === Voice Recognition and Audio Init ===
Recognizer = sr.Recognizer()
Mic = sr.Microphone()

pygame.mixer.init()

def speak(text):
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang='en')
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    except Exception as e:
        log_message("Phoenix", f"Speech Error: {str(e)}")

# === Greeting ===
hour = int(time.strftime("%H"))
if 6 <= hour < 12:
    greetings = "Good Morning"
elif 12 <= hour < 17:
    greetings = "Good Afternoon"
elif 17 <= hour < 22:
    greetings = "Good Evening"
else:
    greetings = "Hello"

#TIME

def Time():
    hour = int(time.strftime("%H"))
    if 0 <= hour < 12:
        AMPM = "A-M"
    else:
        AMPM = "P-M"
    Time = f"{time.strftime("%H:%M")} {AMPM}"
    log_message("Pheonix",Time)
    speak(Time)
 
#Jokes

def Joke():
    Joke = pyjokes.get_joke()
    log_message("Pheonix",Joke)
    speak(Joke)

#Height of projectile

def Height_projectile():
    Mic = sr.Microphone()

    with Mic as source:
        try:
            speak("To calculate the projectile height please speak the following details")
            log_message("Phoenix", "To calculate the projectile height please speak the following details")

            # --- Velocity ---
            speak("Please speak the velocity of projectile")
            log_message("Phoenix", "Please speak the velocity of projectile")
            Recognizer.adjust_for_ambient_noise(source)
            v = Recognizer.listen(source)
            v_text = Recognizer.recognize_google(v)
            u = float(v_text)  # float instead of int for better precision

            # --- Angle ---
            speak("Please speak the angle of projection in degrees.")
            log_message("Phoenix", "Please speak the angle of projection in degrees.")
            a = Recognizer.listen(source)
            a_text = Recognizer.recognize_google(a)
            angle = float(a_text)  # again, float preferred
            angle_radians = math.radians(angle)

            # --- Height Calculation ---
            Height = (u ** 2 * math.sin(angle_radians) ** 2) / (2 * 9.8)
            speak(f"The maximum height attained by the projectile is {Height:.2f} meters.")
            log_message("Phoenix", f"The maximum height attained by the projectile is {Height:.2f} meters.")

        except sr.UnknownValueError:
            speak("Sorry, I could not understand the input. Please try again.")
            log_message("Phoenix", "Speech Recognition failed to understand the input.")

        except sr.RequestError as e:
            speak("Could not request results from Google Speech Recognition service.")
            log_message("Phoenix", f"Speech Recognition service error: {e}")

        except ValueError:
            speak("Input could not be converted to a number. Please speak clearly.")
            log_message("Phoenix", "ValueError: Could not convert speech to float.")

#Time of flight
def calculate_time_of_flight():
    import math
    import speech_recognition as sr

    Recognizer = sr.Recognizer()
    Mic = sr.Microphone()

    with Mic as source:
        try:
            speak("Let's calculate the time of flight of the projectile.")
            log_message("Phoenix", "Starting Time of Flight calculation.")

            speak("Please speak the initial velocity in meters per second.")
            log_message("Phoenix", "Prompting for velocity.")
            Recognizer.adjust_for_ambient_noise(source)
            v = Recognizer.listen(source)
            u = float(Recognizer.recognize_google(v))
            log_message("Phoenix", f"Velocity received: {u} m/s")

            speak("Please speak the angle of projection in degrees.")
            log_message("Phoenix", "Prompting for angle.")
            a = Recognizer.listen(source)
            angle = float(Recognizer.recognize_google(a))
            log_message("Phoenix", f"Angle received: {angle} degrees")

            angle_radians = math.radians(angle)
            g = 9.8
            T = (2 * u * math.sin(angle_radians)) / g

            speak(f"The time of flight is approximately {T:.2f} seconds.")
            log_message("Phoenix", f"Time of flight calculated: {T:.2f} s")

        except sr.UnknownValueError:
            speak("Sorry, I could not understand what you said.")
            log_message("Phoenix", "Speech recognition could not understand input.")

        except sr.RequestError as e:
            speak("Could not connect to speech recognition service.")
            log_message("Phoenix", f"Speech API error: {e}")

        except ValueError:
            speak("Please speak numbers clearly.")
            log_message("Phoenix", "ValueError: Invalid numeric input.")

#Range of projectile
def calculate_range():
    import math
    import speech_recognition as sr

    Recognizer = sr.Recognizer()
    Mic = sr.Microphone()

    with Mic as source:
        try:
            speak("Let's calculate the range of the projectile.")
            log_message("Phoenix", "Starting Range calculation.")

            speak("Please speak the initial velocity in meters per second.")
            log_message("Phoenix", "Prompting for velocity.")
            Recognizer.adjust_for_ambient_noise(source)
            v = Recognizer.listen(source)
            u = float(Recognizer.recognize_google(v))
            log_message("Phoenix", f"Velocity received: {u} m/s")

            speak("Please speak the angle of projection in degrees.")
            log_message("Phoenix", "Prompting for angle.")
            a = Recognizer.listen(source)
            angle = float(Recognizer.recognize_google(a))
            log_message("Phoenix", f"Angle received: {angle} degrees")

            angle_radians = math.radians(angle)
            g = 9.8
            R = (u ** 2 * math.sin(2 * angle_radians)) / g

            speak(f"The range of the projectile is approximately {R:.2f} meters.")
            log_message("Phoenix", f"Range calculated: {R:.2f} m")

        except sr.UnknownValueError:
            speak("Sorry, I could not understand what you said.")
            log_message("Phoenix", "Speech recognition could not understand input.")

        except sr.RequestError as e:
            speak("Could not connect to speech recognition service.")
            log_message("Phoenix", f"Speech API error: {e}")

        except ValueError:
            speak("Please speak numbers clearly.")
            log_message("Phoenix", "ValueError: Invalid numeric input.")

#Quotes
def Quotes():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()[0]
            quote = f'"{data["q"]}" — {data["a"]}'
            log_message("Phoenix", quote)
            speak(data["q"])
        else:
            log_message("Phoenix", "Failed to get quote from ZenQuotes.")
            speak("Sorry, couldn't fetch a quote.")
    except Exception as e:
        log_message("Phoenix", f"Quote Error: {str(e)}")
        speak("Something went wrong while fetching the quote.")

#Number guessing game
def guess_game():
    speak("I'm thinking of a number between 1 to 20. You have 3 chances to guess it.")
    log_message("Phoenix", "I'm thinking of a number between 1 to 20. You have 3 chances to guess it.")
    
    pheonix_number = random.randint(1, 20)

    for attempt in range(1, 4): 
        speak(f"Attempt {attempt}. Go ahead and guess.")
        log_message("Phoenix", f"Attempt {attempt}: Waiting for user guess.")

        try:
            with sr.Microphone() as source:
                Recognizer.adjust_for_ambient_noise(source)
                audio = Recognizer.listen(source, timeout=None)

            guess_text = Recognizer.recognize_google(audio)
            log_message("User", f"Guessed: {guess_text}")

            if guess_text.isdigit():
                guess = int(guess_text)

                if guess < 1 or guess > 20:
                    speak("Please guess a number between 1 and 20.")
                    log_message("Phoenix", "Out of range guess.")
                    continue

                if guess == pheonix_number:
                    speak("🎉 Congratulations! You guessed the correct number!")
                    log_message("Phoenix", "Correct guess!")
                    return
                elif guess < pheonix_number:
                    speak(f"Too low! {3 - attempt} chance(s) left.")
                    log_message("Phoenix", "Too low.")
                else:
                    speak(f"Too high! {3 - attempt} chance(s) left.")
                    log_message("Phoenix", "Too high.")
            else:
                speak("Please say a valid number.")
                log_message("Phoenix", "Invalid spoken input.")
        except Exception as e:
            speak("Sorry, I couldn't understand. Please try again.")
            log_message("Phoenix", f"Error recognizing speech: {e}")
    speak(f"Game over! The correct number was {pheonix_number}. Better luck next time!")
    log_message("Phoenix", f"Game over. Number was {pheonix_number}.")

#Weather

def Weather(city):
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            weather_report = response.text.strip()  
            log_message("Phoenix", weather_report)

            # Split and parse components
            if ":" in weather_report:
                parts = weather_report.split(":")
                location = parts[0].strip()
                condition = parts[1].strip()

                # Extract emoji and temp
                emoji = ''.join([char for char in condition if char in "☀️🌤️⛅☁️🌧️⛈️🌩️🌨️❄️🌪️🌫️🌦️"])
                temp = ''.join([char for char in condition if char.isdigit() or char in "+°C"])

                # Map emoji to readable description
                emoji_map = {
                    "☀️": "sunny",
                    "🌤️": "partly sunny",
                    "⛅": "partly cloudy",
                    "☁️": "cloudy",
                    "🌧️": "rainy",
                    "🌦️": "light rain",
                    "⛈️": "thunderstorms",
                    "🌩️": "lightning",
                    "🌨️": "snowing",
                    "❄️": "snow",
                    "🌫️": "foggy",
                    "🌪️": "stormy"
                }

                condition_text = emoji_map.get(emoji, "weather condition unknown")
                spoken_weather = f"It's {condition_text} and {temp} in {location}."
                speak(spoken_weather)
            else:
                speak(f"Weather in {city}: {weather_report}")
        else:
            log_message("Phoenix", "Couldn't fetch weather data.")
            speak("Sorry, I couldn't fetch the weather.")
    except Exception as e:
        log_message("Phoenix", f"Weather Error: {str(e)}")
        speak("Something went wrong while getting the weather.")

def exiting():
    global access_granted
    access_granted = False
    log_message("Phoenix", "Exiting Phoenix...")
    speak("Exiting Phoenix...")
    root.quit()


def NEWS():
    api_key = "051818fcfbefa2a658ffeff746d4d2e3" 
    url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=in&max=1&token={api_key}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            if not articles:
                log_message("Phoenix", "No news found.")
                speak("I couldn't find any news right now.")
                return

            speak("Here's the top news headline.")
            for article in articles:
                title = article.get('title')
                description = article.get('description')
                if title:
                    log_message("Phoenix", f"📰 {title}")
                    speak(title)
                if description:
                    log_message("Phoenix", f"📝 {description}")
        else:
            print("Error Response Code:", response.status_code)
            print("Error Message:", response.text)
            log_message("Phoenix", "Failed to fetch news.")
            speak("Sorry, I couldn’t get the news.")
    except Exception as e:
        print("Exception Occurred:", e)
        log_message("Phoenix", f"News Error: {str(e)}")
        speak("Something went wrong while fetching the news.")

# === Global Access Flag ===
access_granted = False

def user_accessgranted():
    global access_granted
    access_granted = True
    log_message("Phoenix", "Access Granted.")
    speak("Access Granted.")
    log_message("Phoenix", "How may I help you?")
    speak("How may I help you?")
    while access_granted and root.winfo_exists():
        try:
            with Mic as source:
                Recognizer.adjust_for_ambient_noise(source)
                User_command = Recognizer.listen(source, timeout=None)
                User_command_text = Recognizer.recognize_google(User_command)
                log_message("Chirayu", User_command_text)

                if User_command_text.lower() in ["open google", "google", "can you open google"]:
                    speak("Would you like to search something specific on Google?")
                    log_message("Phoenix", "Would you like to search something specific on Google?")
                    Recognizer.adjust_for_ambient_noise(source)
                    Quary = Recognizer.listen(source, timeout=None)
                    Quary_text = Recognizer.recognize_google(Quary)
                    log_message("Chirayu", Quary_text)
                    if any(word in Quary_text.lower() for word in ["no", "nope"]):
                        log_message("Phoenix", "Opening Google")
                        webbrowser.open_new('https://www.google.com/')
                    else:
                        log_message("Phoenix", f"Searching for {Quary_text} on Google.")
                        pywhatkit.search(Quary_text)

                elif User_command_text.lower() in ["youtube", "open youtube", "can you open youtube"]:
                    speak("Would you like to search something specific on YouTube?")
                    log_message("Phoenix", "Would you like to search something specific on YouTube?")
                    Recognizer.adjust_for_ambient_noise(source)
                    Quary = Recognizer.listen(source, timeout=None)
                    Quary_text = Recognizer.recognize_google(Quary)
                    log_message("Chirayu", Quary_text)
                    if any(word in Quary_text.lower() for word in ["no", "nope"]):
                        log_message("Phoenix", "Opening YouTube.")
                        webbrowser.open_new("https://www.youtube.com/")
                    else:
                        log_message("Phoenix", f"Searching for {Quary_text} on YouTube.")
                        pywhatkit.playonyt(Quary_text)

                elif User_command_text.lower() in ["time","tell time","what's the time","what is the time","tell me time again"]:
                    Time()

                elif User_command_text.lower() in ["joke", "tell me a joke","i want to hear a joke",
                                                   "can you tell me a joke","can you crack a joke",
                                                   "i wanna hear a joke","another joke","crack a better joke",
                                                   "get a good joke","crack a joke"]:
                    Joke()
                elif User_command_text.lower() in ["tell me a quote","quote","get a quote",
                                                   "give me a quote","better quote","tell me a better quote"]:
                    Quotes()

                elif "weather" in User_command_text.lower():
                    words = User_command_text.lower().split()
                    city = None
                    if "in" in words:
                        idx = words.index("in")
                        if idx + 1 < len(words):
                            city = ' '.join(words[idx + 1:])
                        if city:
                            Weather(city)
                    else:
                        speak("Could not extract city name.")
                        log_message("Phoenix", "Could not extract city name.")
                elif "news" in User_command_text.lower():
                    NEWS()
                elif User_command_text.lower() in ["how r you" , "how are you" , "how are you doing"]:
                    speak("All functionalities are operating smoothly.")
                    log_message("Pheonix", "All functionalities are operating smoothly.")  

                elif "search" in User_command_text.lower() and "on google" in User_command_text.lower():
                    try:
                        words = User_command_text.lower().split()
                        search_index = words.index("search")
                        google_index = words.index("google")

                        search_query = " ".join(words[search_index + 1 : google_index - 1])

                        if search_query:
                            log_message("Phoenix", f"Searching Google for: {search_query}")
                            speak(f"Searching Google for {search_query}")
                            
                            result = list(search(search_query, num_results=1))
                            if result:
                                webbrowser.open_new(result[0])
                            else:
                                speak("No results found.")
                                log_message("Phoenix", "No results found.")
                        else:
                            speak("What should I search on Google?")
                            log_message("Phoenix", "Search query was empty.")
                    except Exception as e:
                        speak("Sorry, I couldn't understand your search command.")
                        log_message("Phoenix", f"Search error: {str(e)}")

                elif "open chrome" in User_command_text.lower():
                    speak("Opening Google Chrome")
                    log_message("Phoenix", "Opening Google Chrome")
                    import os
                    try:
                        os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
                    except FileNotFoundError:
                        os.startfile("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")

                elif "close chrome" in User_command_text.lower():
                    speak("Closing Google Chrome")
                    import os
                    log_message("Phoenix", "Closing Google Chrome")
                    os.system("taskkill /f /im chrome.exe")

                elif "open notepad" in User_command_text.lower():
                    speak("Opening Notepad")
                    import os
                    log_message("Phoenix", "Opening Notepad")
                    os.system("notepad")

                elif "close notepad" in User_command_text.lower():
                    speak("Closing Notepad")
                    import os
                    log_message("Phoenix", "Closing Notepad")
                    os.system("taskkill /f /im notepad.exe")

                elif "open calculator" in User_command_text.lower():
                    speak("Opening Calculator")
                    import os
                    log_message("Phoenix", "Opening Calculator")
                    os.system("calc")

                elif "close calculator" in User_command_text.lower():
                    speak("Closing Calculator")
                    log_message("Phoenix", "Closing Calculator")
                    import os
                    os.system("taskkill /f /im Calculator.exe")

                elif "shutdown" in User_command_text.lower():
                    speak("Shutting down the system")
                    log_message("Phoenix", "Shutting down the system")
                    import os
                    os.system("shutdown /s /t 1")

                elif "restart" in User_command_text.lower():
                    speak("Restarting the system")
                    log_message("Phoenix", "Restarting the system")
                    import os
                    os.system("shutdown /r /t 1")

                elif "log out" in User_command_text.lower():
                    speak("Logging out")
                    import os
                    log_message("Phoenix", "Logging out")
                    os.system("shutdown -l")

                elif "increase volume" in User_command_text.lower():
                    speak("Increasing volume")
                    import os
                    log_message("Phoenix", "Increasing volume")
                    for _ in range(5):
                        pyautogui.press("volumeup")

                elif "decrease volume" in User_command_text.lower():
                    speak("Decreasing volume")
                    import os
                    log_message("Phoenix", "Decreasing volume")
                    for _ in range(5):
                        pyautogui.press("volumedown")

                elif "mute" in User_command_text.lower():
                    speak("Muting volume")
                    import os
                    log_message("Phoenix", "Muting volume")
                    pyautogui.press("volumemute")

                elif "brightness up" in User_command_text.lower():
                    speak("Increasing brightness")
                    import os
                    log_message("Phoenix", "Increasing brightness")
                    pyautogui.press("brightnessup")

                elif "brightness down" in User_command_text.lower():
                    speak("Decreasing brightness")
                    import os
                    log_message("Phoenix", "Decreasing brightness")
                    pyautogui.press("brightnessdown")

                elif "turn on wi-fi" in User_command_text.lower():
                    speak("Turning on Wi-Fi")
                    import os
                    log_message("Phoenix", "Turning on Wi-Fi")
                    os.system('netsh interface set interface name="Wi-Fi" admin=enabled')

                elif "turn off wi-fi" in User_command_text.lower():
                    speak("Turning off Wi-Fi")
                    import os
                    log_message("Phoenix", "Turning off Wi-Fi")
                    os.system('netsh interface set interface name="Wi-Fi" admin=disabled')

                elif "open file explorer" in User_command_text.lower():
                    speak("Opening File Explorer")
                    import os
                    log_message("Phoenix", "Opening File Explorer")
                    os.startfile("explorer")

                elif "close file explorer" in User_command_text.lower():
                    speak("Closing File Explorer")
                    import os
                    log_message("Phoenix", "Closing File Explorer")
                    os.system("taskkill /f /im explorer.exe & start explorer.exe")

                elif "open control panel" in User_command_text.lower():
                    speak("Opening Control Panel")
                    import os
                    log_message("Phoenix", "Opening Control Panel")
                    os.system("control")

                elif "open task manager" in User_command_text.lower():
                    speak("Opening Task Manager")
                    import os
                    log_message("Phoenix", "Opening Task Manager")
                    os.system("taskmgr")

                elif "close task manager" in User_command_text.lower():
                    speak("Closing Task Manager")
                    import os
                    log_message("Phoenix", "Closing Task Manager")
                    os.system("taskkill /f /im Taskmgr.exe")

                elif "lock the screen" in User_command_text.lower() or "lock pc" in User_command_text.lower():
                    speak("Locking the system")
                    import os
                    log_message("Phoenix", "Locking the system")
                    os.system("rundll32.exe user32.dll,LockWorkStation")

                elif "take a screenshot" in User_command_text.lower():
                    speak("Capturing screenshot")
                    import os
                    log_message("Phoenix", "Capturing screenshot")
                    pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
                    if not os.path.exists(pictures_dir):
                        os.makedirs(pictures_dir)
                    ss_path = os.path.join(pictures_dir, f"screenshot_{int(time.time())}.png")
                    pyautogui.screenshot(ss_path)
                    speak("Screenshot taken and saved in Pictures folder")
                    log_message("Phoenix", f"Screenshot saved: {ss_path}")

                elif "open downloads" in User_command_text.lower():
                    import os
                    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                    speak("Opening Downloads folder")
                    log_message("Phoenix", "Opening Downloads folder")
                    os.startfile(downloads_path)

                elif "empty recycle bin" in User_command_text.lower():
                    import os
                    try:
                        speak("Emptying Recycle Bin")
                        log_message("Phoenix", "Emptying Recycle Bin")
                        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                        speak("Recycle Bin emptied")
                        log_message("Phoenix", "Recycle Bin emptied successfully")
                    except Exception as e:
                        speak("Error emptying recycle bin")
                        log_message("Phoenix", f"Recycle bin error: {str(e)}")

                elif "open settings" in User_command_text.lower():
                    speak("Opening Windows Settings")
                    import os
                    log_message("Phoenix", "Opening Windows Settings")
                    os.system("start ms-settings:")

                elif "close settings" in User_command_text.lower():
                    speak("Closing Windows Settings")
                    import os
                    log_message("Phoenix", "Closing Windows Settings")
                    os.system("taskkill /f /im SystemSettings.exe")

                elif "minimize all windows" in User_command_text.lower() or "show desktop" in User_command_text.lower():
                    import os
                    pyautogui.hotkey("win", "d")
                    speak("Minimizing all windows")
                    log_message("Phoenix", "Minimizing all windows")

                elif "check battery" in User_command_text.lower() or "battery level" in User_command_text.lower():
                    import os
                    try:
                        battery = psutil.sensors_battery()
                        if battery:
                            percent = battery.percent
                            plugged = battery.power_plugged
                            msg = f"Battery is at {percent} percent and {'charging' if plugged else 'not charging'}"
                            speak(msg)
                            log_message("Phoenix", msg)
                        else:
                            speak("Battery info not available.")
                            log_message("Phoenix", "Battery info unavailable")
                    except Exception as e:
                        speak("Couldn't get battery status.")
                        log_message("Phoenix", f"Battery check error: {str(e)}")

                elif "hello" in User_command_text.lower() or "hi" in User_command_text.lower():
                    greet = random.choice(["Hello", "Hi", "Hey"])
                    speak(greet)
                    log_message("Phoenix", greet)

                elif "fact" in User_command_text.lower():
                    fact = randomfacts.get_fact()
                    print(fact)
                    speak(f"Here's a fact: {fact}")
                    log_message("Phoenix", fact)

                elif "thanks" in User_command_text.lower() or "thank you" in User_command_text.lower() or "great" in User_command_text.lower():
                    speak("You're welcome. Let me know if you need anything else.")
                    log_message("Phoenix", "You're welcome. Let me know if you need anything else.")

                elif "open visual studio code" in User_command_text.lower() or "vs code" in User_command_text.lower():
                    import os
                    speak("Opening VS code")
                    log_message("Phoenix", "Opening VS code")
                    try:
                        os.startfile("C:/Users/Mahaj/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Visual Studio Code")
                    except Exception as e:
                        speak("Something went wrong while performing that system action.")
                        log_message("Phoenix", f"System Control Error: {str(e)}")


                elif any(guess_word in User_command_text.lower() for guess_word in ["start number guessing game","guessing game","number guessing game","play number guessing game"]):
                    log_message("Pheonix","Starting number guessing game")
                    guess_game()
                
                elif User_command_text.lower() == "who created you":
                    speak("I'm Pheonix and i was created by chirayu")
                    log_message("Pheonix","I'm Pheonix and i was created by chirayu")

                elif any(height_p in User_command_text.lower() for height_p in ["open projectile height calculator", "use projectile height calculator", "projectile height calculator", "start projectile height calculator", "launch projectile height calculator", "run projectile height calculator", "start height calculator for projectile", "open height of projectile calculator", "initiate projectile height calculation", "begin projectile height tool", "I want to calculate projectile height", "help me find the projectile height", "can you calculate the height of a projectile?", "what's the maximum height of a projectile?", "tell me the height reached by a projectile", "find projectile’s peak height", "Phoenix, calculate projectile height", "Phoenix, start height calculator", "Hey assistant, run projectile height calculator", "calculate height in projectile motion", "use tool for projectile height", "access projectile height function", "projectile motion height", "maximum height finder", "height finder tool", "motion calculator – height", "physics tool – projectile height", "vertical height of projectile"
                    ]):
                    speak("Starting Projectile Height calculator.")
                    log_message("Pheonix","Starting Projectile Height calculator.")
                    Height_projectile()
                
                elif any(time_p in User_command_text.lower() for time_p in ["open time of flight calculator", "use time of flight calculator", "projectile time calculator", "start time of flight calculator", "launch time of flight tool", "run projectile time calculator", "start projectile time calculator", "open projectile time of flight", "initiate time of flight calculation", "begin flight time tool", "I want to calculate time of flight", "help me find the projectile time", "can you calculate the time of a projectile?", "what's the time of flight for a projectile?", "tell me the flight duration of a projectile", "find projectile’s flight time", "Phoenix, calculate time of flight", "Phoenix, start time calculator", "Hey assistant, run time of flight calculator", "calculate flight time in projectile motion", "use tool for projectile time", "access projectile time function", "projectile motion time", "total flight time calculator", "time duration finder", "motion calculator – time", "physics tool – time of flight", "flight duration of projectile"
                    ]):
                    speak("Starting Projectile Time Of Flight Calculator.")
                    log_message("Pheonix","Starting Projectile Time Of Flight Calculator.")
                    calculate_time_of_flight()
                
                elif any(range_p in User_command_text.lower() for range_p in ["open projectile range calculator", "use projectile range calculator", "projectile range calculator", "start range calculator", "launch projectile range tool", "run range of projectile calculator", "start projectile range calculator", "open range finder for projectile", "initiate projectile range calculation", "begin projectile range tool", "I want to calculate projectile range", "help me find the range of a projectile", "can you calculate the range of a projectile?", "what's the range of this projectile?", "tell me how far the projectile goes", "find projectile’s horizontal distance", "Phoenix, calculate projectile range", "Phoenix, start range calculator", "Hey assistant, run range calculator", "calculate range in projectile motion", "use tool for projectile range", "access projectile range function", "projectile motion range", "maximum range calculator", "horizontal distance finder", "motion calculator – range", "physics tool – projectile range", "total distance travelled by projectile"
                    ]):
                    speak("Starting Projectile Range calculator.")
                    log_message("Pheonix","Starting Projectile Range calculator.")
                    calculate_range()

                elif "open webcam" in User_command_text.lower() or "open camera" in User_command_text.lower():
                    speak("Opening Camera")
                    log_message("Phoenix", "Opening Camera")
                    
                    import subprocess
                    subprocess.run("start microsoft.windows.camera:", shell=True)

                elif "close webcam" in User_command_text.lower() or "close camera" in User_command_text.lower():
                    speak("Closing Camera")
                    log_message("Phoenix", "Closing Camera")
                    
                    import os
                    os.system("taskkill /f /im WindowsCamera.exe")

                elif "translate" in User_command_text.lower():
                    from deep_translator import GoogleTranslator

                    try:
                        command_text = User_command_text.lower().replace("translate", "").strip()

                        # Extract text and target language
                        if " to " in command_text:
                            text, lang = command_text.split(" to ", 1)
                            text = text.strip()
                            lang = lang.strip().lower()
                        else:
                            text = command_text.strip()
                            lang = "english"

                        speak(f"Translating '{text}' to {lang}")
                        log_message("Phoenix", f"Translating '{text}' to {lang}")

                        # Perform translation (pass full name, not ISO 'hi')
                        translation = GoogleTranslator(source='auto', target=lang).translate(text)

                        speak(f"In {lang.capitalize()}, you say: {translation}")
                        log_message("Phoenix", f"Translation: {translation}")

                    except Exception as e:
                        speak("Sorry, I couldn't translate that.")
                        log_message("Phoenix", f"Translation error: {str(e)}")

                elif any(word in User_command_text.lower() for word in ["exit", "quit", "bye"]):
                    exiting()


        except sr.UnknownValueError:
            log_message("Phoenix", "Sorry, I didn't catch that.")
        except Exception as e:
            log_message("Phoenix", f"Error inside command loop: {str(e)}")


# === Main Assistant Logic ===
def listen_and_respond():
    global access_granted
    while not access_granted and root.winfo_exists():
        try:
            with Mic as source:
                Recognizer.adjust_for_ambient_noise(source)
                log_message("Phoenix", "Listening...")
                audio = Recognizer.listen(source, timeout=None)
            command_text = Recognizer.recognize_google(audio)
            log_message("User", command_text)

            if "phoenix" in command_text.lower():
                response = f"{greetings}"
                log_message("Phoenix", response)
                speak(response)

                while True :
                    with Mic as source:
                        Recognizer.adjust_for_ambient_noise(source)
                        log_message("Phoenix", "Speak the password to continue.")
                        speak("Speak the password to continue.")
                        username_audio = Recognizer.listen(source, timeout=None)
                    username = Recognizer.recognize_google(username_audio)
                    log_message("User", username)

                    if "Pheonix" in username.lower():
                        user_accessgranted()
                        return 
                    elif any(exit_word in username.lower() for exit_word in ["exit", "quit", "bye"]):
                        exiting()
                        return
                    else:
                        log_message("Phoenix", "Access Denied.")
                        speak("Access Denied.")

            elif any(exit_word in command_text.lower() for exit_word in ["exit", "quit", "bye"]):
                exiting()
                return

        except sr.UnknownValueError:
            log_message("Phoenix", "Sorry, I didn't understand.")
        except Exception as e:
            log_message("Phoenix", f"Error: {str(e)}")

# === Start Listening ===
def start_conversation():
    threading.Thread(target=listen_and_respond, daemon=True).start()

root.after(2000, start_conversation)

# === Start Main Loop ===
root.mainloop()