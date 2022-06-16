import pygame
import sys
import random

width = 500
height = 500
fps = 30
black = (0,0,0)
white= (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
score = 0

player_img = pygame.image.load("player.png")
target_img = pygame.image.load("target.png")

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Aim Trainer")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

#text
def draw_text_mid(surf, text, size, x, y, colour):#takes in surface, text to output, size of text, and x and y coordinates
    font_name = pygame.font.match_font("comic sans ms")#sets font to comic sans
    font = pygame.font.Font(font_name,size)#gets special font and defines the text size
    text_surface = font.render(text, True, colour)#renders text
    text_rect = text_surface.get_rect()#draws rect for text to be in
    text_rect.midtop = (x, y)#uses x and y coordinates to place the top middle of the box
    surf.blit(text_surface, text_rect)#displays it on the screen

#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.center = (width/2, height/2)
        self.time = 30
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

#target
class Target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = target_img
        self.rect = self.image.get_rect()
        self.radius = (self.image.get_width()//2)
        self.spawn = random.randrange(1,5)
        if self.spawn == 1:
            self.rect.center = (random.randrange(20,width-20), -5)
        if self.spawn == 2:
            self.rect.center = (random.randrange(20,width-20), height+5)
        if self.spawn == 3:
            self.rect.center = (-5,random.randrange(20,height-20))
        if self.spawn == 4:
            self.rect.center = (width-5,random.randrange(20,height-20))
        self.speedx = random.randrange(3,6)
        self.speedy = random.randrange(3,6)
        self.time = 1
    def update(self):
        self.time -= 1/fps
        if self.time < 0:
            self.speedx = random.randrange(-3,6)
            self.speedy = random.randrange(-3,6)
            self.time = 1
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.y >= height:
             self.speedy = random.randrange(-6,-3)
             self.time = 1
        if self.rect.y < 0:
            self.speedy = random.randrange(3,6)
            self.time = 1
        if self.rect.x > width:
            self.speedx = random.randrange(-6,-3)
            self.time =1
        if self.rect.x < 0:
            self.speedx = random.randrange(3,6)
            self.time = 1

targets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

def new_target():
    t = Target()
    all_sprites.add(t)
    targets.add(t)

for i in range(3):
    new_target()

pygame.mouse.set_visible(False)
while True:
    clock.tick(fps)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            hits = pygame.sprite.spritecollide(player, targets, True, pygame.sprite.collide_circle)
            for hit in hits:
                hit.kill()
                score += 1
    
    while len(targets) <  3:
        new_target()

    player.time -= (1/fps)
    if player.time < 0:
        pygame.quit()
        sys.exit()

    all_sprites.update()
    screen.fill(black)
    all_sprites.draw(screen)
    draw_text_mid(screen,str(score),20,width//2,10,red)
    draw_text_mid(screen,str(int(player.time)),20,width//10,10,red)
    pygame.display.flip()
