import pygame#import pygame
import pathlib

#setup some basic colours for later use
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
yellow = (255,194,0)

#draw text module
def draw_text_mid(surf, text, size, x, y, colour):#takes in surface, text to output, size of text, and x and y coordinates
    font = pygame.font.Font(str(pathlib.Path.cwd().joinpath('SFPixelateShaded.ttf')),size)#gets special font and defines the text size
    text_surface = font.render(text, True, colour)#renders text
    text_rect = text_surface.get_rect()#draws rect for text to be in
    text_rect.midtop = (x, y)#uses x and y coordinates to place the top middle of the box
    surf.blit(text_surface, text_rect)#displays it on the screen

def draw_text_left(surf, text, size, x, y, colour):#takes in surface, text to output, size of text, and x and y coordinates
    font = pygame.font.Font(str(pathlib.Path.cwd().joinpath('SFPixelateShaded.ttf')), size)#sets font and font size
    text_surface = font.render(text, True, colour)#renders text
    text_rect = text_surface.get_rect()#draws rect for text to be in
    text_rect = (x, y)#uses x and y coordinates to place the top middle of the box
    surf.blit(text_surface, text_rect)#displays it on the screen

def game_over(screen, score, height, width):#takes in screen, score, heigh of display, width of display
    if score <= 10:#if score taken in less than 10
        draw_text_mid(screen, "Better luck next time",30, (width//2), (10), yellow)#displays message top middle of the screen
    if score > 10 and score <= 25:#if score is between 10 and 25 then a different message is displayed with the score
        draw_text_mid(screen, "Doing alright", 30,(width//2), (10),yellow)
    if score > 25 and score <= 75:#if score is between 25 and 75 then a different message is displayed
        draw_text_mid(screen, "Impressive score", 30,(width//2), (10),yellow)
    if score > 75:#if score is greater than 75 different message is display
        draw_text_mid(screen, "Nice skills", 30,(width//2), (10),yellow)
    draw_text_left(screen,"Back to menu",15,10,10,yellow)
    draw_text_mid(screen, ("Your score is: "+str(score)), 30,(width//2),(40),yellow)#display the player score
    draw_text_mid(screen, "Press Escape to Return", 30,(width//2),(height-60),yellow)

def hearts(surf,lives,height,width):#displays lives using hearts
    heart_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','heart-25x25.png')))#gets heart image
    for i in range (lives):#draws hearts based on lives
        surf.blit(heart_img,(10+i*30, 10))#renders heart

def menu(screen, height, width):#creates menu to display on the screen
    draw_text_mid(screen, "Lone Survivor", 50,(width//2), (20),yellow)#draws relevant text using draw mid function
    draw_text_mid(screen, "Play", 30,(width//2), (height - 250),yellow)#draws relevant text using draw mid function
    draw_text_mid(screen, "Score Board", 30,(width//2), (height - 200),yellow)#draws relevant text using draw mid function
    draw_text_mid(screen, "Instructions", 30,(width//2), (height - 150),yellow)#draws relevant text using draw mid function
    draw_text_mid(screen, "Music", 30,(width//2), (height - 100),yellow)#draws relevant text using draw mid function

def menu_selector(surf,option,height,width):
    selector_img = pygame.image.load(str(pathlib.Path.cwd().joinpath('img','menu-arrow-25x25.png')))#gets selector image
    if option == 0:#checks option value
        surf.blit(selector_img,(width//2-60,height-252))#renders arrow in relevant positon depending on the option that is passed in
    if option == 1:#checks option value
        surf.blit(selector_img,(width//2-135,height-200))
    if option == 2:#checks option value
        surf.blit(selector_img,(width//2-135,height-150))
    if option == 3:#checks option value
        surf.blit(selector_img,(width//2-75,height-100))

def high_score(screen, gameStatus, width, height):#creates high score board
    s = []#creates an array to hold scores
    f = open("high score.txt","r")#gets scores from high score file
    for j in f:
        s.append(j.strip("\n"))#strips [return] and adds score to array
    n = len(s)#finds length of array
    for j in range(n):
        for v in range(n-j-1):
            if int(s[v]) < int(s[v+1]):#if term is less then next term
                temp=s[v]#stores orignal score
                s[v]=s[v+1]#sets next term to current term
                s[v+1] = temp#sets next term as current term
    f.close()
    for v in range(10):#takes first 10 scores
        if gameStatus == "High Score":
            draw_text_left(screen,"Back to menu",15,10,10,yellow)#draws relevant text of on display using function draw_text_left
            draw_text_mid(screen,"Top 10 Score",30,(width//2),30,yellow)#draws relevant text of on display using function draw_text_mid
        temp = 80+v*35#sets temp to term number times 20 then adds 100
        draw_text_mid(screen, str(s[v]), 30,(width//2), (temp),yellow)#displays scores in order

def music_menu(screen,width,height,m):#function for drawing music menu
    draw_text_left(screen,"Back to menu",15,10,10,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_mid(screen,"Music",25,width//2,50,yellow)#draws relevant text of on display using function draw_text_mid
    images = [str(pathlib.Path.cwd().joinpath('img','beat one.png')),str(pathlib.Path.cwd().joinpath('img','Beyond.png')),str(pathlib.Path.cwd().joinpath('img','Find Them.png'))]#holds all music images
    if m == 0:#checks m value
        draw_text_mid(screen,"Beat One",15,width//2,height-50,yellow)#draws relevant text of on display using function draw_text_mid
        screen.blit(pygame.image.load(images[0]),(width//2-175,80))#draws cover of music
    if m == 1:#checks m value
        draw_text_mid(screen,"Behind Enemy Lines",15,width//2,height-50,yellow)#draws relevant text of on display using function draw_text_mid
        screen.blit(pygame.image.load(images[0]),(width//2-175,80))#draws cover of music
    if m == 2:#checks m value
        draw_text_mid(screen,"Beyond",15,width//2,height-50,yellow)#draws relevant text of on display using function draw_text_mid
        screen.blit(pygame.image.load(images[1]),(width//2-175,80))#draws cover of music
    if m == 3:#checks m value
        draw_text_mid(screen,"Find Them",15,width//2,height-50,yellow)#draws relevant text of on display using function draw_text_mid
        screen.blit(pygame.image.load(images[2]),(width//2-175,80))#draws cover of music

def instructions(screen, width,height):#function used to draw instructions menu
    draw_text_left(screen,"Back to menu",15,10,10,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_mid(screen, "INSTRUCTIONS", 25, width/2, 10,yellow)#displays Instructions top middle
    draw_text_left(screen, "Dodge all enemies", 20, width//20, 60,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_left(screen, "Controls:", 20, width//20, 90,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_left(screen, "Use arrow keys or 'W','A','S','D'", 20, width//14, 120,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_left(screen,"Press escape to pause or return to main menu",20,width//14,150,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_left(screen, "Use left joystick to move", 20, width//14, 180,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_left(screen, "Use A to select option to return to main menu", 20, width//14, 200,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_left(screen, "Music:", 20, width//20, 250,yellow)#draws relevant text of on display using function draw_text_mid
    draw_text_left(screen, "Open the music menu from the main menu", 20, width//14, 280,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_left(screen, "Change Option using up and down key", 20, width//14, 310,yellow)#draws relevant text of on display using function draw_text_left
    draw_text_left(screen, "You can also use 'W' and 'S'", 20, width//14, 340,yellow)#draws relevant text of on display using function draw_text_left
    rock = str(pathlib.Path.cwd().joinpath('img','rock small.png'))#draws small image which is used for button that take player to mini game
    screen.blit(pygame.image.load(rock),(500,450))