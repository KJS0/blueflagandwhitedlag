import os
import sys
import time

import math
import random

from glob import glob
from io import BytesIO

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

flag1 = []
flag2 = []
tmp_tts = []

"""
메인 화면
"""
def main():
    while True:
        os.system("cls")
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

def gameStart():
    global flag1, flag2
    os.system("cls")
    
    level = 1 # 초기 레벨
    life = 3 # 초기 생명 수
    ran1 = random.randrange(0, 2) # 초기 깃발 색상
    ran2 = 0 # 질문 ex) 올려, 내려, 내리지 말고 ...
    tmp_tts = ''
    
    FLAGS_TXT = [ "청기", "백기" ]
    QUESTION_TXT = [ "올려", "올리고", "올리지 말고", "내려", "내리고", "내리지 말고" ]
    
    while True:
        os.system("cls")
        if life == 0:
            print("GAME OVER")
            print("5초 후에 메인 화면으로 이동합니다.")
            time.sleep(5)
            break
        
        flag1 = False
        flag2 = [ False, False ]
        
        level_num = math.floor(level ** 0.5)
        print(f"{level}렙, {life}")
        
        print(FLAGS_TXT[ran1])
        for i in range(1, level_num + 1):
            if level_num == 1 or i == level_num:
                ran2 = random.choice([0, 3])
            else:
                ran2 = random.choice([1, 2, 4, 5])
            
            if 0 <= ran2 <= 1: # 올려, 올리고
                flag1 = True
            elif 3 <= ran2 <= 4: # 내려, 내리고
                flag1 = False
            tmp_tts = tmp_tts + (QUESTION_TXT[ran2] + ' ')
            print(QUESTION_TXT[ran2], end = ' ')
        
        tts(tmp_tts)
        if flag1 == flag2[len(flag2) - 1]:
            print(f"\n{level} 레벨 통과!")
            
            if level % 5 == 0:
                print(f"LIFE +1")
                life += 1
        
        tmp_tts = ' '
        level += 1
        time.sleep(1.5)
        print("\n")

def gameExit():
    sys.exit(0)

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