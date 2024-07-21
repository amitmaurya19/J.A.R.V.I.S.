import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import psutil
import threading

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    """Function to convert text to speech."""
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    """Function to wish the user based on the current time."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. Please tell me how may I help you")

def take_command():
    """Function to take microphone input from the user and return a string output."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again, please...")
        return "None"
    return query.lower()

def get_time():
    """Function to get the current time."""
    str_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Sir, the time is {str_time}")
    return str_time

def open_website(url):
    """Function to open a website."""
    webbrowser.open(url)

def search_wikipedia(query):
    """Function to search Wikipedia."""
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        return results
    except Exception as e:
        speak("Sorry, I couldn't find anything on Wikipedia.")
        return "No results found."

def get_system_info():
    """Function to get system information."""
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    info = f"CPU Usage: {cpu_usage}%\nMemory Usage: {memory_info.percent}%"
    speak(info)
    return info

def perform_task(query):
    """Function to perform tasks based on the query."""
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = search_wikipedia(query)
        return results
    elif 'open youtube' in query:
        speak("Opening YouTube")
        open_website("https://www.youtube.com")
        return "Opened YouTube"
    elif 'open google' in query:
        speak("Opening Google")
        open_website("https://www.google.com")
        return "Opened Google"
    elif 'open stackoverflow' in query:
        speak("Opening Stack Overflow")
        open_website("https://www.stackoverflow.com")
        return "Opened Stack Overflow"
    elif 'the time' in query:
        return get_time()
    elif 'open code editor' in query:
        speak("Opening Visual Studio Code")
        code_path = "C:\\Users\\amitm\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(code_path)
        return "Opened Visual Studio Code"
    elif 'system info' in query:
        return get_system_info()
    else:
        speak("I am not sure how to do that yet. Please try something else.")
        return "Command not recognized."

def show_task_list():
    """Function to display the list of tasks Jarvis can perform."""
    tasks = [
        "1. Search on Wikipedia",
        "2. Open YouTube",
        "3. Open Google",
        "4. Open Stack Overflow",
        "5. Get the current time",
        "6. Open Visual Studio Code",
        "7. Get system information"
    ]
    task_list = "\n".join(tasks)
    speak("Here are the tasks I can perform:")
    speak(task_list)
    messagebox.showinfo("Jarvis Tasks", task_list)

def gui_main():
    """Function to create the main GUI."""
    root = tk.Tk()
    root.title("Jarvis Assistant")

    # Configure the window to fill the screen
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}+0+0")

    # Load the Iron Man image
    try:
        image = Image.open("iron_man.jpg")  # Replace with the path to your Iron Man image
        image = image.resize((width, height), Image.LANCZOS)  # Use LANCZOS for resizing
        bg_image = ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image: {e}")
        bg_image = None

    # Create a background label
    if bg_image:
        bg_label = tk.Label(root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=10)
    style.configure('TLabel', font=('Arial', 12), padding=10)

    frame = ttk.Frame(root, style='TFrame')
    frame.place(relx=0.5, rely=0.1, anchor=tk.N)

    command_label = ttk.Label(frame, text="Enter Command:", style='TLabel')
    command_label.grid(row=0, column=0, padx=10, pady=10)

    entry = ttk.Entry(frame, font=('Arial', 14), width=50)
    entry.grid(row=0, column=1, padx=10, pady=10)

    console_frame = ttk.Frame(root)
    console_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    console = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, width=80, height=20, font=("Arial", 12))
    console.grid(row=0, column=0, padx=10, pady=10)

    def speak_command():
        """Function to handle the Speak button command."""
        command = entry.get()
        if command:
            result = perform_task(command.lower())
            console.insert(tk.END, f"User: {command}\nJarvis: {result}\n\n")
            console.yview(tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a command")

    speak_button = ttk.Button(frame, text="Speak", command=speak_command)
    speak_button.grid(row=0, column=2, padx=10, pady=10)

    def voice_command():
        """Function to handle voice commands."""
        def threaded_command():
            query = take_command()
            if query:
                result = perform_task(query)
                console.insert(tk.END, f"User: {query}\nJarvis: {result}\n\n")
                console.yview(tk.END)
        
        threading.Thread(target=threaded_command).start()

    voice_button = ttk.Button(frame, text="Voice Command", command=voice_command)
    voice_button.grid(row=1, column=0, padx=10, pady=10)

    time_button = ttk.Button(frame, text="Get Time", command=lambda: console.insert(tk.END, f"Time: {get_time()}\n\n"))
    time_button.grid(row=1, column=1, padx=10, pady=10)

    system_info_button = ttk.Button(frame, text="System Info", command=lambda: console.insert(tk.END, f"{get_system_info()}\n\n"))
    system_info_button.grid(row=1, column=2, padx=10, pady=10)

    task_list_button = ttk.Button(frame, text="Task List", command=show_task_list)
    task_list_button.grid(row=1, column=3, padx=10, pady=10)

    root.after(1000, wish_me)  # Call wish_me after 1 second to ensure the GUI is displayed first

    root.mainloop()

if __name__ == "__main__":
    gui_main()
