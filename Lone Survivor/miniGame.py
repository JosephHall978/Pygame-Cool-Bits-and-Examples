#import random and sys modules
import pygame, sys,time
from pygame.locals import *
import random
import pathlib
def mini_game():
    #window size
    width = 550
    height = 500
    FPS = 30
    pygame.init()
    pygame.mixer.init
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My game")
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    running = True
    #colours
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)
    white = (255,255,255)
    black = (0,0,0)
    
    #text
    def draw_text_mid(surf, text, size, x, y, colour):#takes in surface, text to output, size of text, and x and y coordinates
        font_name = pygame.font.match_font("comic sans ms")
        font = pygame.font.Font(font_name,size)#gets special font and defines the text size
        text_surface = font.render(text, True, colour)#renders text
        text_rect = text_surface.get_rect()#draws rect for text to be in
        text_rect.midtop = (x, y)#uses x and y coordinates to place the top middle of the box
        surf.blit(text_surface, text_rect)#displays it on the screen
    
    #player
    image = [str(pathlib.Path.cwd().joinpath('img','rock.png')),str(pathlib.Path.cwd().joinpath('img','paper.png')),str(pathlib.Path.cwd().joinpath('img','scissors.png'))]
    class Player(pygame.sprite.Sprite):#sprite class
        def __init__(self,FPS):
            pygame.sprite.Sprite.__init__(self)
            self.option = 0
            self.image = pygame.image.load(image[self.option]).convert()
            self.rect = self.image.get_rect()
            self.rect.center = (width//2,height//2)
            self.fps = FPS
            self.time = 3
            self.temp = 0
            self.score = 0
        def update(self):
            self.time -= 1/self.fps
            self.image = pygame.image.load(image[self.option]).convert()
            self.rect = self.image.get_rect()
            self.rect.center = (width//2,height//2)
            if self.time > 0:
                self.option = self.temp
    #npc
    class NPC(pygame.sprite.Sprite):#sprite class
        def __init__(self,FPS):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((0,0))
            self.rect = self.image.get_rect()
            self.rect.center = (width//2,height//2)
            self.option = random.randrange(0,3)
            self.score = 0

    player = Player(FPS)
    all_sprites.add(player)
    npc = NPC(FPS)
    all_sprites.add(npc)

    while running:
        clock.tick(FPS)
        all_sprites.update()
        screen.fill(white)
        all_sprites.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == ord('w')) and (player.option > 0):
                    player.temp -= 1
                if (event.key == pygame.K_DOWN or event.key == ord('s')) and (player.option < 2):
                    player.temp += 1
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if player.time <= 0:
            if player.option == 0 and npc.option == 2:
                draw_text_mid(screen,"Player Wins",25,width//2,20,black)
                player.score +=1
            elif player.option == 1 and npc.option == 0:
                draw_text_mid(screen,"Player Wins",25,width//2,20,black)
                player.score +=1
            elif player.option == 2 and npc.option == 1:
                draw_text_mid(screen,"Player Wins",25,width//2,20,black)
                player.score +=1
            elif player.option == npc.option:
                draw_text_mid(screen,"Draw",25,width//2,20,black)
            else:
                draw_text_mid(screen,"NPC Wins",25,width//2,20,black)
                npc.score += 1
            time.sleep(2)
            npc.option = random.randrange(0,2)
            player.option = 0
            player.time = 3
        
        if player.score >= 3:
            winner = True
            break
        if npc.score >= 3:
            winner = False
            break
        
        draw_text_mid(screen,("Player score: "+str(player.score)),25,width//2, 40, black)
        draw_text_mid(screen,("NPC score: "+str(npc.score)),25,width//2, 60, black)
        
        pygame.display.update()
        pygame.display.flip()
    
    return winner
'''
option 0 rock
option 1 paper
option 2 scissors
'''
