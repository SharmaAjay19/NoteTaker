# NoteTaker

[Instructions](Instructions.txt)

Install the following:
pip install SpeechRecognition

Install pyaudio
pip install pyaudio

Install Pocket Sphinx using pip
pip install --upgrade pocketsphinx

OR

If you encounter build errors, use the .whl binary by downloading from here:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pocketsphinx


Install pyttsx from here:
pip install git+git://github.com/jpercent/pyttsx.git

To resolve No module 'drivers':
Add C:\Program Files\Anaconda3\Lib\site-packages to Environment PATH variable

To resolve No Module named Engine error:
1. In site_packages/pyttsx/init.py, modify "from engine import Engine" --> "from .engine import Engine"
2. Then, in site_packages/pyttsx/engine.py, 
	A. Modify "import driver" --> "from . import driver"
	B. Modify "except Exception, e" --> "except Exception as e"
3. And finally, in site_packages/pyttsx/driver.py modify "except Exception, e" --> "except Exception as e"

Also register a Bing speech recognition app on Azure and get a key. Put the value of this key in the BING_API_KEY variable in NoteTaker.py



If you want to checkout all the voices present on your system, run the VoiceChecker.py file and it will print the id's of each voice as it speaks the sentence in that voice.
Pick up the id you wish for and replace in blank spaces in "engine.setProperty('voice', '______')" on line 6 in NoteTaker.py.
