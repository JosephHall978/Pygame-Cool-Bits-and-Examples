import pygame
import sys
import random

width = 400
height = 300
fps = 30
black = (0,0,0)
white= (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
score = 0

player_img = pygame.image.load("player.png")
target_img = pygame.image.load("target.png")

#text
def draw_text_mid(surf, text, size, x, y, colour):#takes in surface, text to output, size of text, and x and y coordinates
    font_name = pygame.font.match_font("comic sans ms")#sets font to comic sans
    font = pygame.font.Font(font_name,size)#gets special font and defines the text size
    text_surface = font.render(text, True, colour)#renders text
    text_rect = text_surface.get_rect()#draws rect for text to be in
    text_rect.midtop = (x, y)#uses x and y coordinates to place the top middle of the box
    surf.blit(text_surface, text_rect)#displays it on the screen

#controller setup
pygame.joystick.init()
controller = pygame.joystick.get_count()
print(controller)#prints number of controller joysticks found
if controller > 0:
    controller = True#reuse controller value to hold that controllers are connected True
    joystick = pygame.joystick.Joystick(0)#uses only first joystick connected

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.center = (width/2, height/2)
        self.speedx = 0
        self.speedy = 0
        self.time = 3
    def update(self):
        if controller == True:
            self.speedx = 0
            self.speedy = 0
            axis_x = (joystick.get_axis(2))#axis 0 is x axis left joystick
            axis_y = (joystick.get_axis(3))#axis 1 is y axis left joystick
            right_trigger = (joystick.get_axis(5))
            left_trigger = (joystick.get_axis(4))
            b_button = joystick.get_button(0)
            a_button = joystick.get_button(1)
            up_d_pad = joystick.get_button(11)
            down_d_pad =  joystick.get_button(12)
            left_d_pad = joystick.get_button(13)
            right_d_pad = joystick.get_button(14)
            if abs(axis_x) > 0.1 or abs(axis_y) > 0.1:#prevent movement when no user input cause by controller inaccuracy
                self.speedx = 20*axis_x#multiplies 5 by joystick x coordinate to find speed
                self.speedy = 20*axis_y#multiplies 5 by joystick y coordinate to find speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = target_img
        self.rect = self.image.get_rect()
        self.radius = (self.image.get_width()//2)
        self.rect.center = (random.randrange(20,width-20), random.randrange(20,height-20))
        self.speedx = random.randrange(0,5)
        self.speedy = random.randrange(3,8)
        self.time = 1
    def update(self):
        self.time -= 1/fps
        if self.time < 0:
            self.speedx = random.randrange(-3,3)
            self.speedy = random.randrange(-3,3)
            self.time = 1
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.y > height+40) or (self.rect.y < -20) or (self.rect.x > width+40) or (self.rect.x < -20):
            self.kill()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

def new_target():
    t = Target()
    all_sprites.add(t)
    targets.add(t)

for i in range(4):
    new_target()

run = True
while run:
    clock.tick(fps)
    events = pygame.event.get()
    while len(targets) < 4:
        new_target()
    if controller == True:
        axis_x = (joystick.get_axis(2))#axis 0 is x axis left joystick
        axis_y = (joystick.get_axis(3))#axis 1 is y axis left joystick
        right_trigger = (joystick.get_axis(5))
        left_trigger = (joystick.get_axis(4))
        b_button = joystick.get_button(0)
        a_button = joystick.get_button(1)
        up_d_pad = joystick.get_button(11)
        down_d_pad =  joystick.get_button(12)
        left_d_pad = joystick.get_button(13)
        right_d_pad = joystick.get_button(14)
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if b_button == True:
        pygame.quit()
        sys.exit()
    if right_trigger > 0:
        hits = pygame.sprite.spritecollide(player, targets, True, pygame.sprite.collide_circle)
        for hit in hits:
            hit.kill()
            score+=1
            player.time += 0.7
    
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