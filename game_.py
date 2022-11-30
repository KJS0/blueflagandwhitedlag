import os
import sys
import time
import math
import random
from pymata4 import pymata4

# gTTS
import speech_recognition as sr
from glob import glob
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

my_board = pymata4.Pymata4()
my_board.set_pin_mode_servo(6) # 청기
my_board.set_pin_mode_servo(7) # 백기
my_board.servo_write(7, 10)
my_board.servo_write(6, 110)

flag1 = []
flag2 = []
tmp_tts = []
voice = ''

"""
메인 화면
"""
def main():
    while True:
        os.system("cls") # cls = 화면 지우기
        print("청기백기 게임")
        print("1. 시작")
        print("2. 종료")
            
        key = input("키보드로 숫자를 입력하고 [Enter] 키를 눌러주세요 >> ")
        if key == "1":
            gameStart() # 시작
        elif key == "2":
            gameExit() # 종료
        else:
            os.system("cls")
            print("[INFO] 다시 입력해주세요.\n")
            time.sleep(3)

"""
청기백기 구현
"""
def gameStart():
    global flag1, flag2
    os.system("cls")
    
    level = 1 # 초기 레벨
    life = 3 # 초기 생명 수
    chance = 3 # 기회
    ran1 = random.randrange(0, 2) # 초기 깃발 색상
    ran2 = 0 # 질문 ex) 올려, 내려, 내리지 말고 ...
    tmp_tts = ''
    
    FLAGS_TXT = [ "청기", "백기" ]
    QUESTION_TXT = [ "올려", "올리고", "올리지 말고", "내려", "내리고", "내리지 말고" ]
    
    print("청기백기 게임에 참여하는 여러분! 환영합니다")
    print("규칙은 다음과 같습니다.")
    #tts("청기백기 게임에 참여하는 여러분! 환영합니다")
    #tts("규칙은 다음과 같습니다.")
    
    os.system("cls")
    print("1. 지시된 명령을 듣고, 최종적으로 올리거나 내려야 할 깃발을 음성으로 말해야합니다.")
    print("2. 음성은 ""백기 올려""와 같이 두 단어로만 대답해야합니다.")
    print("3. 만약 음성을 인식하지 못하는 상황을 대비해, 세번까지 기회가 주어집니다.")
    #tts("1. 지시된 명령을 듣고, 최종적으로 올리거나 내려야 할 깃발을 음성으로 말해야합니다.")
    #tts("2. 음성은 ""백기 올려""와 같이 두 단어로만 대답해야합니다.")
    #tts("3. 만약 음성을 인식하지 못하는 상황을 대비해, 세번까지 기회가 주어집니다.")
    
    os.system("cls")
    tts("지금부터 게임을 시작하겠습니다.")
    print("지금부터 게임을 시작하겠습니다.")
    
    
    while True:
        chance = 3
        os.system("cls")
        if life == 0:
            print("GAME OVER")
            print("5초 후에 메인 화면으로 이동합니다.")
            time.sleep(5)
            break
        
        flag1 = [ False, False ]
        flag2 = [ False, False ]
        
        level_num = math.floor(level ** 0.5) # 레벨 함수 수식 (수정 가능)
        tts(f"{level} 단계 시작")
        print(f"{level} 레벨, {life}")
        
        print(FLAGS_TXT[ran1])
        tmp_tts = tmp_tts + FLAGS_TXT[ran1]
        for i in range(1, level_num + 1):
            if level_num == 1 or i == level_num:
                ran2 = random.choice([0, 3]) # 올려, 내려
            else:
                ran2 = random.choice([1, 2, 4, 5]) # 올리고, 올리지 말고, 내리고, 내리지 말고
            
            if 0 <= ran2 <= 1: # 올려, 올리고
                flag1[ran1 - 1] = True
            elif 3 <= ran2 <= 4: # 내려, 내리고
                flag1[ran1 - 1] = False
            tmp_tts = tmp_tts + (QUESTION_TXT[ran2] + ' ')
            print(QUESTION_TXT[ran2], end = ' ')
        
        global voice
        tts(tmp_tts)
        
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=5)
                
        voice = r.recognize_google(audio, language='ko-KR')
        print(voice)
        if voice.find("백기") >= 1 and voice.find("올려") >= 1:
            my_board.servo_write(7, 10)
            flag2[0] = True
        if voice.find("백기") >= 1 and voice.find("내려") >= 1:
            my_board.servo_write(7, 95)
            flag2[0] = False
        elif voice.find("청기") >= 1 and voice.find("올려") >= 1:
            my_board.servo_write(6, 10)
            flag2[1] = True
        elif voice.find("청기") >= 1 and voice.find("내려") >= 1:
            my_board.servo_write(6, 110)
            flag2[1] = False
        else:
            tts("뭐라고 했는지 이해가 안되요")
            chance -= 1
                
            if chance != 0:
                chance -= 1
            elif chance == 0:
                break
        
        time.sleep(3)
        
        if flag1 == flag2:
            os.system("cls")
            print(f"\n{level} 단계 통과!")
            tts(f"{level} 단계 통과!")
            level += 1
            
            if level % 5 == 0: # x5, x0 레벨 통과 시 기회 1회 더 부여
                print(f"LIFE +1")
                tts(f"{level} 단계를 통과했으므로, 기회를 한번 더 드리겠습니다.")
                life += 1
        elif chance == 0 or flag1 != flag2:
            os.system("cls")
            life -= 1
            
            print(f"{level} 단계 통과 실패!")
            print(f"앞으로 {life}번 남았습니다.")
            
            tts(f"{level} 단계 통과 실패!")
            tts(f"앞으로 {life}번 남았습니다.")
        
        tmp_tts = ' '
        
        time.sleep(1.5)
        print("\n")

"""
게임 종료
"""
def gameExit():
    sys.exit(0)

"""
TTS 구현 (gTTS 2.3.0)
"""
def tts(word, toSlow=False):
    tts = gTTS(text=word, lang="ko", slow=toSlow)
    
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    song = AudioSegment.from_file(fp, format="mp3")
    play(song)
    
    fileList = glob("./ffcache*")
    for filePath in fileList:
        os.remove(filePath)

try:
    main()
except SystemExit:
    pass
except KeyboardInterrupt:
    gameExit()
#except:
#    print("[ERROR] 오류 발생")
#    gameExit()
