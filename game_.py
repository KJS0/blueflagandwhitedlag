import os,sys,time,math,random
from hashlib import md5
from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
from pymata4 import pymata4

#포트이쥬?
BLUE = 5
WHITE = 6

#각이쥬?
BLUE_ON = 0
BLUE_OFF = 90
BLUE_MID = 45
WHITE_ON = 180
WHITE_OFF = 90
WHITE_MID = 135

ON=True
OFF=False

my_board = pymata4.Pymata4()
my_board.set_pin_mode_servo(BLUE) # 청기
my_board.set_pin_mode_servo(WHITE) # 백기

def White(i):
    global my_board
    if(i==True): my_board.servo_write(WHITE, WHITE_ON) #올림
    elif(i==False): my_board.servo_write(WHITE, WHITE_OFF) #내림
    elif(i==5):  my_board.servo_write(WHITE, WHITE_MID) #중간
def Blue(i):
    global my_board
    if(i==True): my_board.servo_write(BLUE, BLUE_ON)
    elif(i==False): my_board.servo_write(BLUE, BLUE_OFF)
    elif(i==5):  my_board.servo_write(BLUE, BLUE_MID)

def TTS(text):
    MD5 = md5()
    MD5.update(text.encode('UTF-8'))
    filename = MD5.hexdigest() # 텍스트를 md5해시화해서 파일이름으로 사용
    if os.path.exists(f"{filename}.mp3"): # 동일 내용을 저장하여 속도 개선
        playsound(f"{filename}.mp3", block=True) 
    else:
        try:
            tts = gTTS(text,lang='ko')
            tts.save(f"{filename}.mp3")
            playsound(f"{filename}.mp3", block=True)
        except Exception as e:
            print("TTS 실행 중 오류")
            print(e)
            os.system("pause")
            sys.exit(0)

def STT():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=5)
            voice = r.recognize_google(audio, language='ko-KR')
        return voice
    except:
        return STT() #재시도

def voice_clean(voice):
    #인식 오류를 줄이기 위한 처절한 몸부림
    voice = voice.replace("전기","청기")
    voice = voice.replace("정기","청기")
    voice = voice.replace("천기","청기")
    voice = voice.replace("청기와","청기")
    voice = voice.replace("청기력","청기 올려")
    voice = voice.replace("성기","청기")
    voice = voice.replace("창기","청기")
    voice = voice.replace("경기","청기")
    voice = voice.replace("원료","올려")
    voice = voice.replace("울려","올려")
    voice = voice.replace("얼려","올려")
    voice = voice.replace("울어","올려")
    voice = voice.replace("액기","백기")
    voice = voice.replace("밝기","백기")
    voice = voice.replace("맥기","백기")
    voice = voice.replace("백조","백기")
    voice = voice.replace("100조","백기")
    voice = voice.replace("100개","백기")
    voice = voice.replace("100기","백기")
    return voice

def main():
    while True:
        os.system("cls") # cls = 화면 지우기 - 윈도우
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
            time.sleep(1)

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
    print("규칙은 다음과 같습니다.\n")
    time.sleep(1)
    
    #os.system("cls")
    print("1. 지시된 명령을 듣고, 최종적으로 올리거나 내려야 할 깃발을 음성으로 말해야합니다.")
    print("2. 음성은 ""백기 올려""와 같이 두 단어로만 대답해야합니다.")
    print("3. 만약 음성을 인식하지 못하는 상황을 대비해, 세번까지 기회가 주어집니다.")
    time.sleep(5)

    os.system("cls")
    print("지금부터 게임을 시작하겠습니다.")
    TTS("지금부터 게임을 시작하겠습니다.")
    print("지금부터 게임을 시작하겠습니다.")
    time.sleep(0.3)
    
    
    while True:
        White(5)
        Blue(5)
        chance = 3
        os.system("cls")
        if life == 0:
            print("GAME OVER")
            print("5초 후에 메인 화면으로 이동합니다.")
            TTS("게임 오버.")
            time.sleep(5)
            break
        
        flag1 = [ False, False ]
        flag2 = [ False, False ]
        falsespeech = False
        
        level_num = math.floor(level ** 0.5) # 레벨 함수 수식 (수정 가능)
        TTS(f"{level} 단계 시작")
        print(f"레벨 {level} / 남은 라이프 {life}")

        if (FLAGS_TXT[ran1] == "청기" and level > 8):
            print("백기 올리지 말고", end = ' ')
            tmp_tts += "백기 올리지 말고"
        elif (FLAGS_TXT[ran1] == "백기" and level > 8):
            print("청기 올리지 말고", end = ' ')
            tmp_tts += "청기 올리지 말고"
        if (level > 11):
            for i in range(random.choice([1, 2])):
                rand_hardmode = QUESTION_TXT[random.choice([2, 4, 5])] #올리지 말고, 내리고, 내리지 말고
                print(rand_hardmode, end = ' ')
                tmp_tts += rand_hardmode
        if (level > 16):
            for i in range(random.choice([4, 3])):
                rand_hardmode = QUESTION_TXT[random.choice([2, 4, 5])] #올리지 말고, 내리고, 내리지 말고
                print(rand_hardmode, end = ' ')
                tmp_tts += rand_hardmode
        print(FLAGS_TXT[ran1], end = ' ')
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
        TTS(tmp_tts)
        
        voice = STT()
        voice = voice_clean(voice)
        
        print("\n")
        print(voice)
        
        if "백기" in voice and "올려" in voice:
            White(ON)
            flag2[0] = True
        elif "백기" in voice and "내려" in voice:
            White(OFF)
            flag2[0] = False
        elif "청기" in voice and "올려" in voice:
            Blue(ON)
            flag2[1] = True
        elif "청기" in voice and "내려" in voice:
            Blue(OFF)
            flag2[1] = False
        else:
            falsespeech = True
            TTS("뭐라고 했는지 이해가 안돼요")
            chance -= 1
            if chance != 0:
                chance -= 1
            elif chance == 0:
                break
        
        time.sleep(2.5)
        
        if (flag1 == flag2) and (not falsespeech):
            os.system("cls")
            print(f"\n{level} 단계 통과!")
            TTS(f"{level} 단계 통과!")
            level += 1
            
            if (level-1) % 5 == 0: # x5, x0 레벨 통과 시 기회 1회 더 부여
                life += 1
                print(f"LIFE +1\n남은 라이프 {life}개")
                TTS(f"{level-1} 단계를 통과했으므로, 기회를 한번 더 드리겠습니다.")
                
        elif (chance == 0 or flag1 != flag2):
            os.system("cls")
            life -= 1
            
            print(f"{level} 단계 통과 실패!")
            print(f"앞으로 {life}번 남았습니다.")
            
            #TTS(f"{level} 단계 통과 실패!")
            TTS(f"앞으로 {life}번 남았습니다.")
        
        tmp_tts = ' '
        
        time.sleep(1.5)
        print("\n")

"""
게임 종료
"""
def gameExit():
    sys.exit(0)

try:
    main()
except SystemExit:
    pass
except KeyboardInterrupt:
    gameExit()




## 테스트용 -------------------------
# def TEST():
#     TTS("청기를 내립니다.")
#     Blue(OFF)
#     time.sleep(1)
#     TTS("청기를 올립니다.")
#     Blue(ON)
#     time.sleep(1)
#     TTS("청기를 내립니다.")
#     Blue(OFF)
#     time.sleep(1)
#     TTS("백기를 내립니다.")
#     White(OFF)
#     time.sleep(1)
#     TTS("백기를 올립니다.")
#     White(ON)
#     time.sleep(1)
#     TTS("백기를 내립니다.")
#     White(OFF)
#     time.sleep(1)
