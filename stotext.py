# Python program to translate
# speech to text 


import speech_recognition as sr
import pyttsx3 

# Initialize the recognizer 
r = sr.Recognizer() 


def SpeakText(command):
	
	# Initialize the engine
	engine = pyttsx3.init()
	engine.say(command) 
	engine.runAndWait()
	
def speechtotext():
	flag=0
	while(flag==0):
		try:
		
		# using the microphone as source for input.
			with sr.Microphone() as source2:
			
		    	# one second wait time for adjustment
				r.adjust_for_ambient_noise(source2, duration=0.2)

				print("\nSpeak the name of the person to be registered\n")
				SpeakText("Say the name of the person to register")

				#user's input 
				audio2 = r.listen(source2)
			
				MyText = r.recognize_google(audio2)
				MyText = MyText.lower()

				print("\nDid you say ",MyText,"?")
				SpeakText("Did you say"+MyText)

				audio3 = r.listen(source2)
				Myans = r.recognize_google(audio3)
				Myans = Myans.lower()

				print("\nDid you say ",Myans,"?\n")
				#SpeakText("Did you say"+Myans)
				
				if ('s' in Myans) or ('y' in Myans) or ('yes' in Myans):
					flag=1
					return MyText
				else:
					return speechtotext()
			
		except sr.RequestError as e:
			print("Could not request results; {0}".format(e))
		
		except sr.UnknownValueError:
			print("unknown error occurred")
