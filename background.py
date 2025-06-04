import pygame
import sys
import random
from time import sleep

#배경 색 및 가로 세로 설정
BLACK = (0, 0, 0)
padwidth = 720
padheight = 1024

#각 이미지 불러오기
Alienimage = [ 'image/외계인1.png','image/외계인2.png']
AngryAlien = ['image/공격1.png','image/공격2.png']
Bossimage = ['image/보스.png','image/화내는 보스.png']
Henchmanimage = ['image/외계인3.png', 'image/외계인4.png']
Sound = ['폭발1.mp3','폭발2.mp3']

#이미지 게임에 불러오기 함수
def Object(obj, x, y):
    global gamePad 
    gamePad.blit(obj,(x,y))

#게임 화면 구성
def initGame():
    global gamePad, clock, background, fighter, missile, die, A_die, B_die, missilesound, Gameoversound
    pygame.init()
    gamePad = pygame.display.set_mode((padwidth, padheight)) 
    pygame.display.set_caption('shooting_game')
    background = pygame.image.load('image/background.jpg')  #배경 화면
    fighter = pygame.image.load('image/testfighter.png')  #전투기 그림
    missile = pygame.image.load('image/missile.png')  #미사일 그림
    die = pygame.image.load('image/explosion1.png')  #외계인 죽을 때 그림
    A_die = pygame.image.load('image/explosion2.png')  #화난 외계인 죽을 때 그림
    B_die = pygame.image.load('image/explosion3.png')  #보스 죽을 때 그림
    pygame.mixer.music.load('backgroundmusic.wav')  #배경 음악
    pygame.mixer.music.set_volume(0.5)
    Gameoversound = pygame.mixer.Sound('crash.mp3')  #게임 오버 음악
    missilesound = pygame.mixer.Sound('missile.mp3')  #미사일 음악
    pygame.mixer.music.play(-1)  #계속해서 실행
    clock = pygame.time.Clock()

#화면 중간에 메세지 띄우기
def Message(text):
    global gamePad, Gameoversound
    textfont = pygame.font.Font('NanumGothic.ttf',80)
    text = textfont.render(text, True, (255,0,0))
    text_center = text.get_rect()
    text_center.center = ((padwidth/2),(padheight/2))
    gamePad.blit(text,text_center)
    pygame.display.update()

#보스 시간 설정
total_time = 100  #100초 
def timer(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 25)
    text = font.render('남은 시간 :'+str(count)+'초',True,(255,255,255))
    gamePad.blit(text,(520,0))

#처치한 외계인 수와 놓친 외계인 수 표시하는 함수
def Score(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('점수 :' + str(count),True,(255,255,255))
    gamePad.blit(text,(10,0))

def Passed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 외계인 :' + str(count),True,(255,0,0))
    gamePad.blit(text,(10,30))

#놓친 외계인 수가 10마리이면 게임 끝을 표시하는 함수
def Gameover():
    global gamePad
    Message('-GAME OVER-')
    pygame.mixer.music.stop()
    Gameoversound.play()
    sleep(10)
    pygame.mixer.music.play(-1) #(-1)은 무한반복을 뜻함
    runGame()

#전투기가 외계인에 3번 충돌하면 게임 끝을 표시하는 함수
def Crash():
    global gamePad
    Message('--전투기 파괴--')
    pygame.mixer.music.stop()
    Gameoversound.play()
    sleep(10)
    pygame.mixer.music.play(-1)
    runGame()

#게임에서 승리할 떄 표시되는 함수
def Win():
    global gamePad
    Message('게임 승리!!')
    pygame.mixer.music.stop()
    sleep(5)
    pygame.quit()
     
#보스 체력 표시 함수
def Health(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('목숨 :{}'.format(str(count)),True,(255,255,255))
    gamePad.blit(text,(200,0))
    
def runGame():
    global gamePad, clock, background, fighter, missile, die, A_die, B_die, missilesound

    #전투기 크기
    f_size = fighter.get_rect().size
    f_wigth = f_size[0]
    f_height = f_size[1]
    
    #전투기 초기 위치
    x = padwidth * 0.45
    y = padheight * 0.9
    fighterX = 0
    fighterY = 0

    #미사일 좌표
    missileXY =[]

    #외계인 랜덤 생성 및 크기 설정
    Alien = pygame.image.load(random.choice(Alienimage))
    A_size = Alien.get_rect().size
    A_width = A_size[0]
    A_height = A_size[1]
    ExplotionSound1 = pygame.mixer.Sound(Sound[0])

    #화난 외계인 랜덤 생성 및 크기 설정
    AAlien = pygame.image.load(random.choice(AngryAlien))
    AA_size = AAlien.get_rect().size
    AA_width = AA_size[0]
    AA_height = AA_size[1]

    #보스 생성 및 크기 설정
    Boss = pygame.image.load(Bossimage[0])
    B_size = Boss.get_rect().size
    B_width = B_size[0]
    B_height = B_size[1]

    #화난 보스 생성 및 크기 설정
    AngryBoss = pygame.image.load(Bossimage[1])
    AB_size = AngryBoss.get_rect().size
    AB_width = AB_size[0]
    AB_height = AB_size[1]
    ExplotionSound2 = pygame.mixer.Sound(Sound[1])

    #보수 부하 생성 및 크기 설정
    Henchman = pygame.image.load(random.choice(Henchmanimage))
    H_size = Henchman.get_rect().size
    H_width = H_size[0]
    H_height = H_size[1]

    #외계인 초기 설정
    AlienX = random.randrange(0, padwidth - A_width)
    AlienY = 0
    A_speed = 2

    #화난 외계인 초기 설정
    AngryAlienX = random.randrange(0, padwidth - AA_width)
    AngryAlienY = 0
    AA_speeed = 3.5

    #보스 초기 설정
    Boss_Health = 100
    BossX = 250
    BossY = 250
    B_speed = 2

    #화난 보스 초기 설정
    ABossX = 250
    ABossY = 250
    AB_speed = 3

    #보스 부하 초기 설정
    HenchmanX = random.randrange(0,padwidth - H_width)
    HenchmanY = 0
    H_speed = 4

    #외계인이 미사일에 맞았을 때
    hit = False
    hitcount = 0
    A_pass = 0

    #화난 외계인이 미사일에 맞았을 때
    A_hit = False

    #보스 부하들이 미사일에 맞았을 때
    H_hit = False
    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            #전투기 움직이기
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX -= 3

                elif event.key == pygame.K_RIGHT:
                    fighterX += 3
            #추가한 요소 / 방향키 위 버튼 누르면 앞으로, 뒤 버튼 누르면 뒤로
                elif event.key == pygame.K_UP:
                    fighterY -= 3

                elif event.key == pygame.K_DOWN:
                    fighterY += 3
            #ESC 누르면 화면 꺼짐
                if event.key == pygame.K_ESCAPE:
                    onGame = True
            #스페이스바 누르면 미사일 발사
                elif event.key == pygame.K_SPACE:
                    missilesound.play()
                    missileX = x + f_wigth/2
                    missileY = y - f_height
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighterY = 0

        Object(background, 0, 0)
        Object(fighter, x, y)

        x += fighterX
        if x < 0:
            x = 0
        elif x > padwidth - f_wigth:
            x = padwidth - f_wigth

        #전투기가 앞으로 가는 구역 제한
        y += fighterY
        if y < 500 :
            y = 500
        elif y> padheight - f_height:
            y = padheight - f_height 

        #전투기가 외계인과 충돌했는지 체크
        if y < AngryAlienY - AA_height:
            if (AngryAlienX > x and AngryAlienX < x + f_wigth) or (AngryAlienX + AA_width > x and AngryAlienX + AA_width < x + f_wigth):
                Crash()

        #미사일 화면에 그리기
        if len(missileXY) != 0:
            for i, xy in enumerate(missileXY):
                xy[1] -= 10
                missileXY[i][1] = xy[1]

                #미사일이 외계인을 맞췄을 경우
                if xy[1] < AlienY:
                    if xy[0] > AlienX and xy[0] < AlienX + A_width:
                        missileXY.remove(xy)
                        hit = True
                        hitcount += 1

                if xy[1] <= 0:
                    try:
                        missileXY.remove(xy)
                    except:
                        pass

                #화난 외계인을 맞췄을 경우
                if xy[1] < AngryAlienY:
                    if xy[0] > AngryAlienX and xy[0] < AngryAlienX + AA_width:
                        missileXY.remove(xy)
                        A_hit = True
                        hitcount += 1

                if xy[1] <= 0:
                    try:
                        missileXY.remove(xy)
                    except:
                        pass

                #보스를 맞출경우
                if xy[1] < BossY:
                    if xy[0] > BossX and xy[0] < BossX + B_width:
                            missileXY.remove(xy)
                            hitcount += 2
                            Boss_Health -= 2

                if xy[1] <= 0:
                    try:
                        missileXY.remove(xy)
                    except:
                        pass
                
        if len(missileXY) != 0:
            for bx, by in missileXY:
                Object(missile, bx, by)
        
        #점수 표시
        Score(hitcount)

        #외계인 움직임
        AlienY += A_speed

        if AlienY > padheight:
            Alien = pygame.image.load(random.choice(Alienimage))
            A_size = Alien.get_rect().size
            A_width = A_size[0]
            A_height = A_size[1]
            AlienX = random.randrange(0,padwidth - A_width)
            AlienY = 0
            A_pass += 1
        
        Passed(A_pass)

        #화난 외계인 움직임
        AngryAlienY += AA_speeed
        if AngryAlienY > padheight:
            AAlien = pygame.image.load(random.choice(AngryAlien))
            AA_size = AAlien.get_rect().size
            AA_width = AA_size[0]
            AA_height = AA_size[1]
            AngryAlienX = random.randrange(0,padwidth - AA_width)
            AngryAlienY = 0

        #만약 그냥 외계인 10마리를 놓치면 게임 끝
        if A_pass == 10:
            Gameover()

        #외계인의 죽음 표시하기
        if hit:
            Object(die, AlienX, AlienY)
            ExplotionSound1.play()  #폭발 사운드

            #새로운 외계인 랜덤 소환
            Alien = pygame.image.load(random.choice(Alienimage))
            A_size = Alien.get_rect().size
            A_width = A_size[0]
            A_height = A_size[1]
            AlienX = random.randrange(0,padwidth - A_width)
            AlienY = 0
            hit = False

            #외계인 3마리 잡을 때 마다 속도 증가 및 유지
            A_speed += 0.2
            if A_speed >= 5:
                A_speed = 5

        #화난 외계인의 죽음 표시하기
        if A_hit:
            Object(A_die, AngryAlienX, AngryAlienY)
            ExplotionSound1.play()  #폭발 사운드

            #새로운 화난 외계인 랜덤 소환
            AAlien = pygame.image.load(random.choice(AngryAlien))
            AA_size = AAlien.get_rect().size
            AA_width = AA_size[0]
            AA_height = AA_size[1]
            AngryAlienX = random.randrange(0,padwidth - AA_width)
            AngryAlienY = 0
            A_hit = False

        #타이머 설정
        B_time = (pygame.time.get_ticks())/1000
        
        #보스 등장
        if hitcount >= 10:
            Object(Boss, BossX, BossY)
            Health(Boss_Health)  #보스 체력 보여주기
            timer(total_time-int(B_time))  #타이머 시작
            AlienY = -100  #화면 위로 올려서 없애기
            AngryAlienY = -100  #화면 위로 올려서 없애기

            BossX += B_speed
            if BossX >= padwidth - B_width:
                B_speed = -B_speed

            elif BossX <= 0:
                B_speed = -B_speed
                BossX = 0

            ABossX += AB_speed
            if ABossX >= padwidth - AB_width:
                AB_speed = -AB_speed

            elif ABossX <= 0:
                AB_speed = -AB_speed
                ABossX = 0

            #시간이 0초 이하가 되면 게임 끝
            if total_time - B_time <= 0:
                Gameover()

            #미사일이 화난 보스를 맞출 경우
            if len(missileXY) != 0:
                for i, xy in enumerate(missileXY):
                    xy[1] -= 10
                    missileXY[i][1] = xy[1]
                if xy[1] < ABossY:
                    if xy[0] > ABossX and xy[0] < ABossX + AB_width:
                            missileXY.remove(xy)
                            hitcount += 4
                            Boss_Health -= 2

                if xy[1] <= 0:
                    try:
                        missileXY.remove(xy)
                    except:
                        pass

            if len(missileXY) != 0:
                for bx, by in missileXY:
                    Object(missile, bx, by)
            
            #보스 체력이 일정 이하로 떨어지면 발생하는 이벤트.
            if Boss_Health <= 50:
                BossY = -300
                Object(Henchman, HenchmanX, HenchmanY)
                Object(AngryBoss, ABossX, ABossY)

                if len(missileXY) != 0:
                    for i, xy in enumerate(missileXY):
                        xy[1] -= 10
                        missileXY[i][1] = xy[1]

                    if xy[1] < HenchmanY:
                        if xy[0] > HenchmanX and xy[0] < HenchmanX + H_width:
                                missileXY.remove(xy)
                                H_hit = True
                                hitcount += 3

                    if xy[1] <= 0:
                        try:
                            missileXY.remove(xy)
                        except:
                            pass

                HenchmanY += H_speed

                if HenchmanY > padheight:
                    Henchman = pygame.image.load(random.choice(Henchmanimage))
                    H_size = Henchman.get_rect().size
                    H_width = H_size[0]
                    H_height = H_size[1]
                    HenchmanX = random.randrange(0,padwidth - H_width)
                    HenchmanY = 0

                if H_hit:
                    Object(die, AlienX, AlienY)
                    ExplotionSound1.play()  #폭발 사운드

                    #새로운 외계인 랜덤 소환
                    Henchman = pygame.image.load(random.choice(Henchmanimage))
                    H_size = Henchman.get_rect().size
                    H_width = H_size[0]
                    H_height = H_size[1]
                    HenchmanX = random.randrange(0,padwidth - H_width)
                    HenchmanY = 0
                    H_hit = False 
                    
                #전투기가 부하와 충돌했는지 체크
                if y < HenchmanY - H_height:
                    if (HenchmanX > x and HenchmanX < x + f_wigth) or (HenchmanX + H_width > x and HenchmanX + H_width < x + f_wigth):
                        Crash()                                   

            if Boss_Health <= 0:
                Object(B_die, BossX, BossY)
                ExplotionSound2.play()
                Win()

        Object(Alien, AlienX, AlienY)
        Object(AAlien, AngryAlienX, AngryAlienY)
        

        pygame.display.update()
        clock.tick(100)
        
    pygame.quit()
        
initGame()
runGame()
