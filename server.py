#!/usr/bin/python3

import socket
import pyttsx3
import speech_recognition as sr
import time

# Creating sockets and binding them to the port and IP addresses
x=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
x.bind(("127.0.0.1",9999))

engine=pyttsx3.init()

r=sr.Recognizer()
mic=sr.Microphone()


# Receiving instruction from Player1
count=3
while count>0:
    data=x.recvfrom(1000)
    msg=data[0].decode()
    if(count%2==0):
        print(msg)
    else:
        engine.say(msg)
        engine.runAndWait()
    count=count-1
    port=data[1]


# Attempting to guess the word in required number of attempts
attempt=1
while(attempt<4):
    time.sleep(1)
    msg='Your guess number '+str(attempt)
    engine.say(msg)
    engine.runAndWait()
    print("Speak !!")
    with mic as source:      # Capturing guess from Player2 throgh a microphone
        r.adjust_for_ambient_noise(source)
        audio=r.listen(source)
    guess=r.recognize_google(audio)
    guess=guess.lower()
    print("You said :",guess)
    x.sendto(guess.encode(),port)    # Sending the guess to Player1 for verification
    data=x.recvfrom(1000)
    msg=data[0].decode()
    time.sleep(1)
    if(msg=='Congrats. You got the word right'):
        engine.say(msg)
        engine.runAndWait()
        break
    else:
        engine.say(msg)
        engine.runAndWait()
        attempt=attempt+1
        
# Playing proper message when no. of attempts get exhausted
time.sleep(1)
if(attempt==4):
    data=x.recvfrom(1000)
    msg=data[0].decode()
    engine.say(msg)
    engine.runAndWait()
