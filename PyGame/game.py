# 1 - Import library
import pygame
from pygame.locals import *
import math
import random
import time

# 2 - Initialize the game's main function as well as the first parameters
def main():
    
    pygame.init()
    clock = pygame.time
    width, height = 1000, 600
    screen=pygame.display.set_mode((width, height))
    keys = [False, False, False, False]
    playerpos=[100,100]
    acc=[0,0]
    arrows=[]
    badtimer=100
    badtimer1=0
    badguys=[[640,100]]
    healthvalue=194
    pygame.mixer.init()
    accuracy=0
    exitcode=0


    black=(0,0,0)
    end_it=False
    while (end_it==False):          # 2.1- this is the first while loop with 2 lables that will work as welcome screen and instructions 
        screen.fill(black)
        myfont=pygame.font.SysFont("Britannic Bold", 40)
        nlabel=myfont.render("Use the WASD keys to move and click to shoot. Survive 90 seconds.", 1, (255, 0, 0))
        nlabe2=myfont.render("Press R to restart once the match ends.", 1, (255, 0, 0))
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONDOWN:
                end_it=True
        screen.blit(nlabel,(50,250))
        screen.blit(nlabe2,(50,300))
        pygame.display.flip()

    # 3 - this will load images into the main while loop
    player = pygame.image.load("resources/images/dude.png")
    grass = pygame.image.load("resources/images/grass.png")
    castle = pygame.image.load("resources/images/castle.png")
    arrow = pygame.image.load("resources/images/bullet.png")
    badguyimg1 = pygame.image.load("resources/images/badguy.png")
    badguyimg=badguyimg1
    healthbar = pygame.image.load("resources/images/healthbar.png")
    health = pygame.image.load("resources/images/health.png")
    gameover = pygame.image.load("resources/images/gameover.png")
    youwin = pygame.image.load("resources/images/youwin.png")
    # 3.1 - this will load audio into the main while loop
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
    shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
    hit.set_volume(0.05)
    enemy.set_volume(0.05)
    shoot.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/moonlight.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)

    # 4 - the main while loop starts here but we first have to set the win/lose parameters to initial value



    running = 1
    exitcode = 0

    while running:
        badtimer-=1
        # 5 - clear the screen before drawing it again
        screen.fill(0)
        # 6 - we draw the player and assets at our designated location
        for x in range(int(width/grass.get_width()+1)):
            for y in range(int(height/grass.get_height()+1)):
                screen.blit(grass,(x*100,y*100))
        screen.blit(castle,(0,30))
        screen.blit(castle,(0,135))
        screen.blit(castle,(0,240))
        screen.blit(castle,(0,345 ))
        # 6.1 - Set player position and rotation 
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
        playerrot = pygame.transform.rotate(player, 360-angle*57.29)
        playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
        screen.blit(playerrot, playerpos1) 
        # 6.2 - we draw the arrows on the screen and set their speed
        for bullet in arrows:
            index=0
            velx=math.cos(bullet[0])*10
            vely=math.sin(bullet[0])*10
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<-64 or bullet[1]>1000 or bullet[2]<-64 or bullet[2]>480:
                arrows.pop(index)
            index+=1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                screen.blit(arrow1, (projectile[1], projectile[2]))
        # 6.3 - with this code we draw the monsters and state when and where they will spawn (randomly in this case)
        if badtimer==0:
            badguys.append([1000, random.randint(50,430)])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=35
            else:
                badtimer1+=5
        index=0
        for badguy in badguys:
            if badguy[0]<-64:
                badguys.pop(index)
            badguy[0]-=7
            # 6.3.1 - here we set the monsters to attack the castle
            badrect=pygame.Rect(badguyimg.get_rect())
            badrect.top=badguy[1]
            badrect.left=badguy[0]
            if badrect.left<64:
                hit.play()
                healthvalue -= random.randint(5,20)
                badguys.pop(index)
            #6.3.2 - this will check for actual collisions between textures of arrows and enmies
            index1=0
            for bullet in arrows:
                bullrect=pygame.Rect(arrow.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0]+=1
                    badguys.pop(index)
                    arrows.pop(index1)
                index1+=1
            # 6.3.3 - this will add more than 1 enemy to the game at once
            index+=1
        for badguy in badguys:
            screen.blit(badguyimg, badguy)
        # 6.4 - Draw health bar
        screen.blit(healthbar, (5,5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1+8,8))
                # 6.4.1 - Draw clock to display remaining time to the player
        font = pygame.font.Font(None, 24)
        survivedtext = font.render(str((90000-clock.get_ticks())/60000)+":"+str((90000-clock.get_ticks())/1000%60).zfill(2), True, (0,0,0))
        textRect = survivedtext.get_rect()
        textRect.topright=[635,5]
        screen.blit(survivedtext, textRect)
        # 7 - update the screen
        pygame.display.flip()
        # 8 - loop through the events that will read the key presses
        for event in pygame.event.get():
            # check if the event is the X button on the window 
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key==K_w:
                    keys[0]=True
                elif event.key==K_a:
                    keys[1]=True
                elif event.key==K_s:
                    keys[2]=True
                elif event.key==K_d:
                    keys[3]=True
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w:
                    keys[0]=False
                elif event.key==pygame.K_a:
                    keys[1]=False
                elif event.key==pygame.K_s:
                    keys[2]=False
                elif event.key==pygame.K_d:
                    keys[3]=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                shoot.play()
                position=pygame.mouse.get_pos()
                acc[1]+=1
                arrows.append([math.atan2(position[1]-(playerpos1[1]+110),position[0]-(playerpos1[0]+30)),playerpos1[0]+110,playerpos1[1]+110])
                    
        # 9 - Move player by changing the preset ''keys'' variables to True and allow the player position to change
        if keys[0]:
            playerpos[1]-=5
        elif keys[2]:
            playerpos[1]+=5
        if keys[1]:
            playerpos[0]-=5
        elif keys[3]:
            playerpos[0]+=5


        #10 - Win/Lose check if the timer ticks are over a certain value or if the HP is equal to or less than 0 (it might happen that 2 enemies deal the final blow at once thus reducing the HP to 0<=)
        if pygame.time.get_ticks()>= 90000:
            running=0
            exitcode=1
            break
        if healthvalue<=0:
            running=0
            exitcode=0
            break
        if acc[1]!=0:
            accuracy=acc[0]*1.0/acc[1]*100
        else:
            accuracy=0

        



            
        # 11 - this will display the win or lose interfaces + accuracy check



    if exitcode==0:
        pygame.font.init()
        font = pygame.font.Font(None, 24)
        text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        screen.blit(gameover, (200,0))
        screen.blit(text, textRect)

    else:
        pygame.font.init()
        font = pygame.font.Font(None, 24)
        text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        screen.blit(youwin, (200,0))
        screen.blit(text, textRect)


    # 12 - this is the tertiary while loop that will check whether the player has pressed the R key to restart the game or quit the game entirely        
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # 12.1 - this resets the pygame internal timer and restarts the function that wraps the 3 main loops
                    pygame.quit()
                    main()
            elif event.type == QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()



main()



    
	





