import speech_recognition as sr 
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()

newsapi = "Add newsapi here"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    del(engine)
    
def aiProcess(command):
    client = OpenAI(api_key = "Add Openai API here")
    completion = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content":"You are a virtual assistant named jarvis skilled in general tasks like alexa and google cloud in short 30 to 50 words."},
            {"role": "user","content":command}
        ]
    )
    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook " in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
    
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        
        data = r.json()
        articles = data.get('articles', [])
        for article in articles[:5]:
            title=article['title']
            speak(title)
        # if r.status_code == 200:
            # parse the JSON response
            # data = r.json()
            
            # Extract the articles
            # articles = data.get('articles', [])
            
            #print/Speak the headlines
            # for article in articles[:5]:
            #     title=articles.get('title')
                # speak(title)
                # engine.say(title)
            #     print(article['title'])
                
    else:
        # let open ai handle the request
        output = aiProcess(c)
        speak(output)

    
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    # speak("Yaa 1")
    while True:
        # Listen for the wake word "Jarvis"
        # obtaini audio from the microphone
        
        r = sr.Recognizer()
        
        print("Recognizing..")
        try:
            with sr.Microphone() as source:
                # recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = r.listen(source, timeout = 2 , phrase_time_limit=1)
            word = r.recognize_google(audio)
            # speak("Yaa 2")
            if(word.lower() == "jarvis"):
                speak("Yaa")
                # listen for command
                with sr.Microphone() as source:
                    
                    print("Jarvis Activating ...")
                    speak("activated")
                    print("Listening...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    
                    processCommand(command)
            
            
            
        except Exception as e:
            print("Error; {0}".format(e))
