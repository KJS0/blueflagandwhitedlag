import sys
import time
import scipy.io as sio
import scipy.io.wavfile
import sounddevice as sd
from pymata4 import pymata4
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr

ttsText="모터를 움직였습니다."
tts = gTTS(text=ttsText, lang='ko')
tts.save("moterKo.mp3")
right="오른쪽 90도"
left="왼쪽 90도"
setup="초기 위치"
board = pymata4.Pymata4()
def servo1(my_board, pin):
    my_board.set_pin_mode_servo(pin)
    my_board.servo_write(8, 170)
    time.sleep(1)
    
def servo2(my_board, pin):
    my_board.set_pin_mode_servo(pin)
    my_board.servo_write(8, 10)
    time.sleep(1)
    
def servo3(my_board, pin):
    my_board.set_pin_mode_servo(pin)
    my_board.servo_write(8, 90)
    time.sleep(1)
try:
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        print("you said: " + r.recognize_google(audio,language = 'ko-KR'))
        text = r.recognize_google
        if(r.recognize_google(audio,language='ko-KR')==setup):
            servo3(board,8);
            playsound("moterKo.mp3")
            time.sleep(2)
        elif(r.recognize_google(audio,language='ko-KR')==right):
            servo1(board,8);
            playsound("moterKo.mp3")
            time.sleep(2)
        elif(r.recognize_google(audio,language='ko-KR')==left):
            servo2(board,8);
            playsound("moterKo.mp3")
            time.sleep(2)
except KeyboardInterrupt:
         board.shutdown()
         sys.exit(0)        

    


