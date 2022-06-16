import sys
import pygame
import pathlib
from sprites import * #imports all classes from sprites module
from mechanics import * #imports all functions from mechanics
from miniGame import *

f = open("high score.txt","a")
width = 550#sets width
height = 500#sets height
fps = 30#sets starting fps to 30
score = 0
gameStatus = "Menu"#sets Game Status "Play"
option = 0 #amin selector default option
m = 0 #the music list array default
boss = 1 #sets starting value of number fof bosses to 1
lorax = False
music = [str(pathlib.Path.cwd().joinpath('snd','Beat One.mp3')),str(pathlib.Path.cwd().joinpath('snd','Behind Enemy Lines.mp3')),str(pathlib.Path.cwd().joinpath('snd','Beyond - part 2.mp3')),str(pathlib.Path.cwd().joinpath('snd','Find Them.mp3'))]#list of all the music in the game
if pygame.joystick.get_count() > 0:#checks if there is at least one joystick
    joystick = pygame.joystick.Joystick(0)#uses the first joystick connected
control_delay = 0#sets controller delay to 0

pygame.init()
pygame.mixer.init()#initialise sound mixer
pygame.mixer.music.load(music[m])#load sound
pygame.mixer.music.play(loops=-1)#play sound that has been loaded and loop it

screen = pygame.display.set_mode((width,height))#creates game window
pygame.display.set_caption("Lone Survivor")#game window caption
player_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','player-60x60.png'))).convert_alpha()#gets base player image
dart_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','dart-30x30.png'))).convert_alpha()#gets base dart image
asteroid_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','asteroid-50x42.png'))).convert_alpha()#gets base asteroid image
bomber_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','bomber.png'))).convert_alpha()#gets base image for bomber
shifter_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','shifter.png')))#gets base image for shifter
titan_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','Titan.png'))).convert_alpha()#gets base image for titan
glitch_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','glitch-30x30.png'))).convert_alpha()#gets base image for glitch
background = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','background-1000x1000.png'))).convert_alpha()#gets background image
background_rect = background.get_rect()#gets area of background image
menu_background = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','menu-550x500.png'))).convert_alpha()#base menu option
menu_background_rect = menu_background.get_rect()#gets rectangle for background image
main_menu_background = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','rework menu.png'))).convert_alpha()#reworked main menu background
main_menu_background_rect = main_menu_background.get_rect()#gets rectangle for main menu background
clock = pygame.time.Clock()#starts pygame clock

all_sprites = pygame.sprite.Group()#sets all_sprites as a pygame sprite group
mobs = pygame.sprite.Group()#sets mobs as a pygame spirte group
bosses = pygame.sprite.Group()#sets bosses as a pygame sprite group
player = Player(player_img)#creates player from class Player
all_sprites.add(player)#adds player to sprite group all_sprites

def new_dart(dart_img):#function for creating dart sprite
    d = Dart(dart_img)#creates dart from class Dart
    all_sprites.add(d)#adds sprite to all_sprites group
    mobs.add(d)#adds sprite to mobs group

def new_asteroid(asteroid_img):#function for creating asteroid sprite
    a = Asteroid(asteroid_img)#insantatiate asteroid
    all_sprites.add(a)#adds asteroid to all_sprites group
    mobs.add(a)#adds asteroid to mobs group

def new_bomber(bomber_img,fps):#function for creating bomber
    b = Bomber(bomber_img,fps)#instatiates bomber after basing image and frame rate
    all_sprites.add(b)#adds bomber sprite to all_sprites group
    mobs.add(b)#adds bomber sprite to mobs group

def new_shifter(shifter_img):#function for creating shifter
    s = Shifter(shifter_img)#instatiates shifter after passing in the image for shifter
    all_sprites.add(s)#adds new shifter to all_sprites group
    mobs.add(s)#adds new shifter to mobs group

def new_glitch(glitch_img):
    g = Glitch(glitch_img)
    all_sprites.add(g)
    mobs.add(g)

def new_titan(titan_img):#function creates new titan
    t = Titan(titan_img)#intstatiates titan and passes in titan image
    all_sprites.add(t)#adds new titan to all_sprites
    bosses.add(t)#adds new titan to bosses group

def new_enemy(boss):#class for creating random enemy
    select = random.randrange(0,(6-boss))#random selection value
    if select == 0:
        new_dart(dart_img)#uses new_dart function to create new enmey
    if select == 1:
        new_asteroid(asteroid_img)#uses new_asteroid function to create new enmey
    if select == 2:
        new_bomber(bomber_img,fps)#uses new_bomber function to create new enmey
    if select == 3:
        new_shifter(shifter_img)#uses new_shifter function to create new enemy
    if select == 4:
        new_glitch(glitch_img)
    if select == 5:
        new_titan(titan_img)#uses new_titan function to create new enmey

for i in range (6):#loop to create starting sprites
    new_enemy(boss)
run = True#sets game loop to true
surface = pygame.Surface((550,500))#bgr

while run:#starts gameplay loop
    keystate = pygame.key.get_pressed()#gets keysates of keyboard keys
    game_events = pygame.event.get()#gets events for example mouse button down
    clock.tick(int(fps))#checks clock speed
    screen.blit(menu_background, menu_background_rect)#draws menu  background for other menus
    #screen.fill(blue)#fills background with blue
    if keystate[pygame.K_ESCAPE]: #if statement to pause or return to main menu if escape key is pressed
        if gameStatus == "Game Over":#if statement to reset values if escape is pressed while gameSatus is "Game Over"
            player.lives = 3#sets player lives to 3
            score = 0#resets score
            fps = 30#resets fps back to 30
        gameStatus = "Menu"#sets gameStatus to menu
    if pygame.joystick.get_count() > 0:
        if (joystick.get_button(0) == True) or (joystick.get_button(5) == True):
            if gameStatus == "Game Over":#if statement to reset values if escape is pressed while gameSatus is "Game Over"
                player.lives = 3#sets player lives to 3
                score = 0#resets score
                fps = 30#resets fps back to 30
            gameStatus = "Menu"#sets gameStatus to menu
    for event in game_events:#checks pygame events
            if event.type == pygame.QUIT:#if player clicks X the game closes
                pygame.quit()#stops pygame processes
                sys.exit()#closes terminal in more basic IDLEs

    if gameStatus == "Menu":#menu gameStatus
        control_delay -= 0.1
        screen.blit(main_menu_background, main_menu_background_rect)#draws the main menu background
        mouse = pygame.mouse.get_pos()#store mouse position in mouse 
        menu_selector(screen,option,height,width)#menu selector function to controller where it is displayed
        keystate = pygame.key.get_pressed()#gets keyboard keys keystate
        if (keystate[pygame.K_RETURN]):#if user presses enter key
            if option == 0:
                temp = player.lives
                player.kill()
                player = Player(player_img)#creates player from class Player
                all_sprites.add(player)#adds player to sprite group all_sprites
                player.lives = temp
                gameStatus = "Play"#changes gameStatus so Play phase begins
            if option == 1:
                gameStatus = "High Score"#changes gameStatus so High Score phase begins
            if option == 2:
                gameStatus = "Instructions"#changes gameStatus so Instructions phase begins
            if option == 3:
                gameStatus = "Music"#changes gameStatus so Music phase begins
        if pygame.joystick.get_count() > 0:#used to prevent errors when no controller is connected
            if (joystick.get_axis(1) < -0.1) and (option > 0) and (control_delay <= 0):#if y axis of left joystick is less than -0.1
                option -= 1
                control_delay = 1
            if (joystick.get_axis(1) > 0.1) and (option < 3) and (control_delay <= 0):#if y axis of left joystick is greater than 0.1
                option += 1
                control_delay = 1
            if joystick.get_button(1) == True:#if the A button is pressed
                if option == 0:
                    temp = player.lives
                    player.kill()
                    player = Player(player_img)#creates player from class Player
                    all_sprites.add(player)#adds player to sprite group all_sprites
                    player.lives = temp
                    gameStatus = "Play"#changes gameStatus so Play phase begins
                if option == 1:
                    gameStatus = "High Score"#changes gameStatus so High Score phase begins
                if option == 2:
                    gameStatus = "Instructions"#changes gameStatus so Instructions phase begins
                if option == 3:
                    gameStatus = "Music"#changes gameStatus so Music phase begins
        for event in game_events:#for any events that occur like button down
            if event.type == pygame.KEYDOWN:#if event is keydown checks what to do if certain keys is down
                if (event.key == pygame.K_UP or event.key == ord('w')) and (option > 0):#if W or up arrow key is pressed and option is greater then zero decreases option by 1
                    option -= 1
                if (event.key == pygame.K_DOWN or event.key == ord('s')) and (option < 3):#if S or down arrow key is pressed and option is less then 3 increases option by 1
                    option += 1                
            if event.type == pygame.MOUSEBUTTONUP:#if event is mouse button click
                if  (mouse[0] > (width//2 - 40))  and (mouse[1] < (height - 225) and mouse[1] > (height - 255)):#button range
                    temp = player.lives
                    player.kill()
                    player = Player(player_img)#creates player from class Player
                    all_sprites.add(player)#adds player to sprite group all_sprites
                    player.lives = temp
                    gameStatus = "Play"#changes gameStatus to "Play"
                elif  (mouse[0] > (width//2 - 115))  and (mouse[1] < (height - 170) and mouse[1] > (height - 200)):#button range
                    gameStatus = "High Score"#changes gameStatus to "High Score"
                elif  (mouse[0] > (width//2 - 110))  and (mouse[1] < (height - 125) and mouse[1] > (height - 155)):#button range
                    gameStatus = "Instructions"#changes gameStatus to "Instructions"
                elif (mouse[0] > (width//2 - 50)) and (mouse[1] < (height - 75)) and (mouse[1] > (height - 110)):#button range
                    gameStatus = "Music"#changes gameStatus to "Music"

    if gameStatus == "Instructions":#Instructions menu
        instructions(screen,width,height)#takes in parameters of screen, height, and width so that function can draw text
        mouse = pygame.mouse.get_pos()#store mouse position in mouse
        for event in game_events:
            if event.type == pygame.MOUSEBUTTONUP:#if event is mouse button down
                if (mouse[0]> 10) and (mouse[0] < (135)) and (mouse[1]> 10) and (mouse[1]<35):#button range
                    gameStatus = "Menu"#changes gameStatus to menu so game displays main menu
                if (mouse[0]>450) and (mouse[0]<550) and (mouse[1]>450) and (mouse[1]<500):
                    lorax = mini_game()
                    if lorax == True:
                        player_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','lorax-60x60.png'))).convert_alpha()

    if gameStatus == "High Score":#High score board
        mouse = pygame.mouse.get_pos()#store mouse position in mouse
        for event in game_events:
            if event.type == pygame.MOUSEBUTTONUP:#if event is mouse button down
                if (mouse[0]> 10) and (mouse[0] < (135)) and (mouse[1]> 10) and (mouse[1]<35):#button range
                    gameStatus = "Menu"#changes gameStatus to menu so game displays main menu
        high_score(screen,gameStatus,width,height)#uses function to draw highscore board by taking in the paramters screen, gameStatus, width and height
    if gameStatus == "Music":#Music menu
        control_delay -= 0.1
        temp = m#stores m value at the start
        music_menu(screen,width,height,m)#draws music menu using function taking in the paramters screen, width, height, and m value
        for event in game_events:
            if event.type == pygame.KEYDOWN:#if  event is keydown checks what if a certain key is down
                if (event.key == pygame.K_UP or event.key == ord('w')) and (m > 0):#if up arrow key or W is pressed and m is greater than 0 decreases m by 1
                    m -= 1
                if (event.key == pygame.K_DOWN or event.key == ord('s')) and (m < 3):#if down arrow key or S is pressed and m is less than 3 increase m by 1
                    m += 1
        if pygame.joystick.get_count() > 0:#checks there is at least one josytick connected
            if (joystick.get_axis(1) < -0.1) and (m > 0) and (control_delay <= 0):#checks if the joystick is being moved downwards, there is another option below, and controller delay is < or = to 0
                m -= 1#deecrease the positon by 1
                control_delay = 1#resets controller delay
            if (joystick.get_axis(1) > 0.1) and (m < 3) and (control_delay <= 0):#checks if the joystick is being moved downwards, there is another option below
                m += 1#increases the position by 1
                control_delay = 1#resets controller delay
        if temp != m:#temp and and m are different new music is loaded and played in a loop
            pygame.mixer.music.load(music[m])
            pygame.mixer.music.play(loops=-1)
    if gameStatus == "Play":#if game status is "Play" the game plays through
        boss = len(bosses)#used to regulate boss group spawns

        while len(mobs) < 6:#checks there is 6 mobs alive
            new_enemy(boss)#creates new enemy
            score += 0.5#increases score by 0.5

        if len(bosses) > 1:#checks if there is more then 1 boss enemy
            for kill in bosses:#if more then 1 boss ALL are killed
                kill.kill()#kills boss sprite

        all_sprites.update()#updates all sprite displayed
        fps += 0.01#increases fps 0.01 per frame

        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)# detects if player collides with a mob
        for hit in hits:#checks to see which mobs collided with player
          new_enemy(boss)#spawns new enemy
          if hit.type == "Shifter":#if the class type is shifter the player is teleported to different screen location
              player.rect.center = (random.randrange(100,width-100),random.randrange(100,height-100))#changes player location
          hit.kill()#kills enemy that collide with the player
          player.lives -= 1#reduces player lives by 1
        
        hits = pygame.sprite.spritecollide(player, bosses, True, pygame.sprite.collide_circle)# detects if player collides with a mob
        for hit in hits:
          new_enemy(boss)#spawns new enemy
          hit.kill()#kills enemy that collide with the player
          player.lives -= 1#reduces player lives by 
        
        for b in bosses:
            hits = pygame.sprite.spritecollide(b, mobs, True, pygame.sprite.collide_circle)# detects if boss collides with a mob
            for hit in hits:#checks to see which mob hit the boss
                hit.kill()#kills mob that hit the boss
                b.lives -= 1#take a life from boss

        screen.blit(background, background_rect)#draws game background
        hearts(screen,player.lives,height,width)#uses function in mechanics.py to draw hearts
        all_sprites.draw(screen)#draws all sprite

        draw_text_mid(screen, str(int(score)), 20, width // 2, 10,white)#displays score top middle

        if player.lives < 0:#checks to see if player lives is less then 1
            gameStatus = "Game Over"#sets gameStatus to "Game Over"
            f = open("high score.txt","a")#opens text file to add player score
            f.writelines((str(int(score)),"\n"))#writes new player score to text file
            f.close()#closes file used
    
    if gameStatus == "Game Over":#when gameStatus equals "Game Over" the play stage stop running
        for m in mobs:#loops for num of mobs
            m.kill()#kills mob sprite
        for b in bosses:#loops for the number of bosses
            b.kill()#kills boss sprite
        all_sprites.clear(screen,surface)#clears mobs from all groups
        screen.blit(menu_background, menu_background_rect)#draws menu background
        game_over(screen, int(score), height, width)#displays message appropriate to player performance and score
        high_score(screen, gameStatus, width, height)#takes in the display, width of display, height of the display
        mouse = pygame.mouse.get_pos()#store mouse position in mouse
        for event in game_events:
            if event.type == pygame.MOUSEBUTTONUP:#checks if event contains mouse button down 
                if ((mouse[0]> 10) and (mouse[0] < (135))) and ((mouse[1]> 10) and (mouse[1]<35)):#button range
                    player.lives = 3#resets player health
                    fps = 30#resets fps
                    score = 0#resets score
                    gameStatus = "Menu"#returns to main menu
    pygame.display.flip()
#JSH