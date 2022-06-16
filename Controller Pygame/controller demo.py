import pygame
import sys

width = 300
height = 400
fps = 30
black = (0,0,0)
white= (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
#text
def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('comic sans ms')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
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
        self.image = pygame.Surface((50,50))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.speedx = 0
        self.speedy = 0
    def update(self):
        if controller == True:
            axis_x = (joystick.get_axis(0))#axis 0 is x axis left joystick
            axis_y = (joystick.get_axis(1))#axis 1 is y axis left joystick
            right_trigger = (joystick.get_axis(5))
            left_trigger = (joystick.get_axis(4))
            b_button = joystick.get_button(0)
            a_button = joystick.get_button(1)
            y_button = joystick.get_button(2)
            x_button = joystick.get_button(3)
            minus_button = joystick.get_button(4)
            home_button = joystick.get_button(5)
            plus_button = joystick.get_button(6)
            left_stick_click = joystick.get_button(7)#clicking left stick
            right_stick_click = joystick.get_button(8)#clicking right
            left_bumper = joystick.get_button(9)
            right_bumper = joystick.get_button(10)
            up_d_pad = joystick.get_button(11)
            down_d_pad =  joystick.get_button(12)
            left_d_pad = joystick.get_button(13)
            right_d_pad = joystick.get_button(14)
            if abs(axis_x) > 0.1:#prevent movement when no user input cause by controller inaccuracy
                self.speedx = 5*axis_x#multiplies 5 by joystick x coordinate to find speed
                self.speedy = 5*axis_y#multiplies 5 by joystick y coordinate to find speed
            if b_button == True:
                self.image.fill(red)
            if a_button == True:
                self.image.fill(blue)
            if left_trigger > 0:
                self.image.fill(green)
            if right_trigger > 0 :
                self.image.fill(white)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
run = True
while run:
    clock.tick(fps)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    all_sprites.update()
    screen.fill(black)
    all_sprites.draw(screen)
    pygame.display.flip()
    
    
