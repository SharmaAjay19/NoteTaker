import speech_recognition as sr
import pyttsx, sys
import time
import json
config = json.load(open('config.json', 'r'))
dictionary = json.load(open('dictionary.json', 'r'))
engine = pyttsx.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0') #The voice id can be replaced according to instructions in Instructions.txt
BING_KEY = config["BING_API_KEY"]

def processDictionary(litems):
    res = []
    for item in litems:
        res = res + [item, item+'.', item.lower(), item.lower() + '.']
    return res

stopphrases = processDictionary(dictionary['traindata']['stopphrases'])
yesphrases = processDictionary(dictionary['traindata']['yesphrases'])
nophrases = processDictionary(dictionary['traindata']['nophrases'])
startphrases = processDictionary(dictionary['traindata']['startphrases'])

def speak(text):
    engine.say(text)
    engine.runAndWait()

class NoteTaker:
    def __init__(self, title, notetypes=0):
        self.title = title
        self.notes = dict()
        self.phrase_time_limit = (8 if notetypes==1 else 5)
        self.recognizer = sr.Recognizer()
        self.timeout = 2
    def ToFile(self, filename=None):
        text = json.dumps(self.notes, indent=4)
        if filename is None:
            filename = self.title + '.json'
        with open(filename, 'w') as f:
            f.write(text)
            f.close()
    def takeNote(self, note):
        tmstmp = time.strftime("%d/%m/%Y %H:%M:%S")
        self.notes[tmstmp] = note
        self.ToFile()
    def recognizeAudio(self, audio):
        if audio:
            try:
                text = self.recognizer.recognize_bing(audio, key=BING_KEY)
                if text in stopphrases:
                    self.exit()
                else:
                    return text
            except sr.UnknownValueError:
                return "Sorry, I can't understand you."
            except sr.RequestError as e:
                return "Sorry, Unable to connect to Bing API."
        else:
            return None
    def captureAudio(self, short=False):
        try:
            phrase_tl = 2 if short else self.phrase_time_limit
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, phrase_time_limit=phrase_tl, timeout=self.timeout)
            return audio
        except Exception as e:
            print("Error occurred while capturing audio", e)
            return None
    def exit(self):
        speak("Thank you very much!")
        sys.exit()
    def noteConfirmation(self, note):
        speak(note)
        speak("Please confirm")
        conf = self.recognizeAudio(self.captureAudio(short=True))
        while conf is None:
            speak("Please say something")
            conf = self.recognizeAudio(self.captureAudio(short=True))
        if conf in yesphrases:
            return True
        elif conf in nophrases:
            return False
    def startNoteTaking(self):
        while True:
            #speak("I am listening")
            resp = self.recognizeAudio(self.captureAudio(short=True))
            if resp is None:
                continue
                #speak("Please say something")
            elif resp in startphrases:
                speak("You can start telling me")
                resp = self.recognizeAudio(self.captureAudio())
                if self.noteConfirmation(resp):
                    self.takeNote(resp)
                else:
                    while self.noteConfirmation(resp) is False:
                        speak("Please repeat yourself")
                        resp = self.recognizeAudio(self.captureAudio())
                    self.takeNote(resp)

nt = NoteTaker("Notes1")
nt.startNoteTaking()