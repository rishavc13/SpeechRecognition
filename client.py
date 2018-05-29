#!/usr/bin/python3

# import required audio and speech recognition modules
import speech_recognition as sr
import random
import socket
import pyttsx3
import time

engine=pyttsx3.init()

x=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
r=sr.Recognizer()

mic=sr.Microphone()

# Computer prompts Player1 to select any word from the available list of words
list_of_words='apple banana coconut mango litchi guava orange pineapple strawberry grapes'
engine.say('Select anyone from the folowing list of words')
engine.runAndWait()
print(list_of_words)

# Player1 speaks a random word from the above list of words
print("Speak !!")
with mic as source:
    r.adjust_for_ambient_noise(source)
    audio=r.listen(source)
word=r.recognize_google(audio)
word=word.lower()
print("You said :",word)

# Instruction message sent to Player 2
x.sendto('Player one is thinking of one of the following words'.encode(),("127.0.0.1",9999))
time.sleep(1)
x.sendto(list_of_words.encode(),("127.0.0.1",9999))
time.sleep(1)
x.sendto('You have only three chances to guess the word'.encode(),("127.0.0.1",9999))

# Judging the guesses
chances=3
while(chances>0):
    data=x.recvfrom(1000)
    guess=data[0].decode()
    if(guess.lower()==word):
        x.sendto('Congrats.You got the word right'.encode(),("127.0.0.1",9999))
        break
    else:
        x.sendto('Your guess was wrong. Please try again'.encode(),("127.0.0.1",9999))
        chances=chances-1
if(chances==0):
    x.sendto('You exhausted all your chances. You lost'.encode(),("127.0.0.1",9999))
