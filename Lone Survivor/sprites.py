#imports and starting variables
import pygame#pygame
import math#calculate how much to rotate a sprite
import random #random number module
import pathlib
black = (0,0,0)
width = 550
height = 500
joystick = False
#sprites
#controller stuff
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)

#player
class Player(pygame.sprite.Sprite):#creates player class
    def __init__(self, player_img):#set parameters to be passed in the player and it's image
        pygame.sprite.Sprite.__init__(self)#intiliase pygame sprites
        self.image_orig = player_img
        self.image = self.image_orig
        self.rect = self.image.get_rect()#get rect for image
        self.radius = 12#set a collison radius of 12 pixels from the centre
        self.rect.center = (width/2, height/2)#centre sprite
        self.speedx = 0#set starting x speed to zero
        self.speedy = 0#set starting y speed to zero
        self.lives = 3#set number of player lives
        self.rot = 0
        self.last_update = pygame.time.get_ticks()

    def rotate(self):#function used to rotate the image
        if self.speedx > 0:
            self.rot = -10
        elif self.speedx < 0:
            self.rot = 10
        else:
            self.rot = 0
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            new_image = pygame.transform.rotate(self.image_orig, self.rot)#rotates the original image and sets it to new_image
            old_center = self.rect.center#resets image center to prevent thee collision rectangle not matching the image
            self.image = new_image#sets image to new_image
            self.rect = self.image.get_rect()#creates new collision rectangle
            self.rect.center = old_center#and redefines image center
    
    def update(self):
        self.rotate()
        self.speedx = 0#reset x speed
        self.speedy = 0#reset y speed
        if pygame.joystick.get_count() > 0:
            if abs(joystick.get_axis(0)) > 0.1 or abs(joystick.get_axis(1)) > 0.1:
                self.speedx = 10 * joystick.get_axis(0)
                self.speedy = 10 * joystick.get_axis(1)
        keystate = pygame.key.get_pressed() #get any keys pressed during frame
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:#if [A] or the left arrow key is down x speed is set -8
            self.speedx = -10
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:#if [D] or the right arrow key is down x speed is set 8
            self.speedx = 10
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:#if [W] or the up arrow key is down y speed is set -8
            self.speedy = -10
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:#if [S] or the left arrow key is down y speed is set 8
            self.speedy = 10
        
        
        if self.speedx != 0 and self.speedx != 0:
            self.rect.x += self.speedx/1.414#increase x coordinate by the x speed
            self.rect.y += self.speedy/1.414#increasee y coordinate by the y speed
        else:
            self.rect.x += self.speedx#increase x coordinate by the x speed
            self.rect.y += self.speedy#increasee y coordinate by the y speed
        if self.rect.right > width:#stops player leaving the right side
            self.rect.right = width
        if self.rect.left < 0:#stops player leaving left side of the screen
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
#dart
class Dart(pygame.sprite.Sprite):#create dart calss
    def __init__(self, dart_img):#set parameter that need to be passed in dart image and which dart
        pygame.sprite.Sprite.__init__(self)#intialise pygame sprite
        self.type = "Dart"
        self.image = dart_img#scale dart image that is passed in to 30x30 pixels
        self.rect = self.image.get_rect()#define image rectangle for collision
        self.radius = 15
        self.spawn_zone = random.randrange(1,5)#set spawn zone for dart

        if self.spawn_zone == 1:#spawn zone 1 is along the top of the screen
            self.rect.center = ((random.randrange(0,width-20)), -20)#varies where dart spawns along the width
            self.speedx = random.randrange(1,12)#varies x speed
            self.speedy = random.randrange(1,12)#varies y speed
        if self.spawn_zone == 2:#spawn zone 2 is along the left side of the screen
            self.rect.center = (-20,(random.randrange(0, height-20)))#varies where the dart spawns along the height
            self.speedx = random.randrange(1,12)
            self.speedy = random.randrange(1,12)
        if self.spawn_zone == 3:#spawn zone 3 is along the bottom of the screen
            self.rect.center = (height + 20,(random.randrange(0, height-20)))
            self.speedx = random.randrange(-12,-1)
            self.speedy = random.randrange(-12,-1)
        if self.spawn_zone == 4:#spawn zone 4 is along the right of the screen
            self.rect.center = ((random.randrange(0,width-20)),height + 20)
            self.speedx = random.randrange(-12,-1)
            self.speedy = random.randrange(-12,-1)

        #rotate so that tip is going in direction of travel
        orig_center = self.rect.center
        if(self.spawn_zone == 1) or (self.spawn_zone == 2): #rotates spawn zone 1 and 2 sprites so they point in the correct direction
            self.rot = math.degrees(math.atan(self.speedx/self.speedy))+180#calculates the bearing the dart is going
            self.image = pygame.transform.rotate(self.image, self.rot)#rotates dart image to match the bearing
            self.rect = self.image.get_rect()#corrects image rect
            self.rect.center = orig_center#corrects the image centre
        if (self.spawn_zone == 3) or (self.spawn_zone == 4):#rotates spawn zone 3 and 4 sprites so they point in the correct direction 
            self.rot = math.degrees(math.atan(self.speedx/self.speedy))#calculates bearing the dart is going
            self.image = pygame.transform.rotate(self.image, self.rot)#rotates dart image to match the bearing
            self.rect = self.image.get_rect()#corrects image rect
            self.rect.center = orig_center#corrects the image centre

    def update(self):#updates sprite postion of the display window
        self.rect.x += self.speedx #increase x coordinate by sprites speed
        self.rect.y += self.speedy#increases y coordinate by sprites speed
        if self.spawn_zone == 1 or self.spawn_zone == 2:#check for defective sprites that originate from spawn zone 1 and 2
            if (self.speedx < 5) and (self.speedy < 5):#if both speeds are below 5 units per frame then the sprite is destoried
                self.kill()#kills sprite
            if self.rect.x > width+20:#checks sprite is within screen width
                self.kill()
            if self.rect.y > height+20:#check sprite is within screen height
                self.kill()
        if (self.spawn_zone == 3) or (self.spawn_zone == 4):#checks for defective sprites that originate from zone 3 and 4
            if (self.speedx > -5) and (self.speedy > -5):#if both speeds are below 5 units per frame then the sprite is destoried
                self.kill()#kills sprite
            if self.rect.x < -20:#check sprite is within screen width
                self.kill()
            if self.rect.y < -20:#check sprite is within screen height
                self.kill()
#asteriod
class Asteroid(pygame.sprite.Sprite):#creates asteroid class that inherits pygame.sprite.Sprite attributes and methods
    def __init__(self,asteroid_img):#defines instatiation
        pygame.sprite.Sprite.__init__(self)
        self.type = "Asteroid"#defines sprite type as aseroid
        self.image_orig = asteroid_img#sets orignal image
        self.image = self.image_orig.copy()#copy base image to attribute self.image
        self.rect = self.image.get_rect()#gets image rect
        self.radius = int(self.rect.width * 0.85 / 2)#sets up image radius based of image rect
        self.rect.x = random.randrange(width - self.rect.width)#sets x position
        self.rect.y = random.randrange(-150, -100)#sets y position
        self.speedy = random.randrange(4, 8)#sets y speed to random value from 4-8
        self.speedx = random.randrange(-3, 3)#sets x speed to random value from -3-3
        self.rot = 0#sets base rotation to zero
        self.rot_speed = random.randrange(-8, 8)#sets speed of rotation from -8-8
        self.last_update = pygame.time.get_ticks()

    def rotate(self):#function used to rotate the image
        now = pygame.time.get_ticks()#sets now as pygame ticks
        if now - self.last_update > 50:#checks if now - last update is greater then 50
            self.last_update = now#sets last update to now
            self.rot = (self.rot + self.rot_speed) % 360#finds the amount to rotate the image as a percentage of 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)#rotates the original image and sets it to new_image
            old_center = self.rect.center#resets image center to prevent thee collision rectangle not matching the image
            self.image = new_image#sets image to new_image
            self.rect = self.image.get_rect()#creates new collision rectangle
            self.rect.center = old_center#and redefines image center

    def update(self):#updates sprite
        self.rotate()#uses rotate method to rotate asteroid
        self.rect.x += self.speedx#increment x coordinate by speedx
        self.rect.y += self.speedy#increment y coordinate by speedy
        if self.rect.y > height + 50:#checks if sprite is not on the display
            self.kill()#kills sprite off screen
#bomb
timer = [str(pathlib.Path.cwd().joinpath('img','timer','timer-8.png')),str(pathlib.Path.cwd().joinpath('img','timer','timer-7.png')),str(pathlib.Path.cwd().joinpath('img','timer','timer-6.png')),str(pathlib.Path.cwd().joinpath('img','timer','timer-5.png')),str(pathlib.Path.cwd().joinpath('img','timer','timer-4.png')),str(pathlib.Path.cwd().joinpath('img','timer','timer-3.png')),str(pathlib.Path.cwd().joinpath('img','timer','timer-2.png')),str(pathlib.Path.cwd().joinpath('img','timer','timer-1.png'))]
phase = [str(pathlib.Path.cwd().joinpath('img','phase00.png')),str(pathlib.Path.cwd().joinpath('img','phase01.png')),str(pathlib.Path.cwd().joinpath('img','phase02.png')),str(pathlib.Path.cwd().joinpath('img','phase03.png')),str(pathlib.Path.cwd().joinpath('img','phase04.png')),str(pathlib.Path.cwd().joinpath('img','phase05.png')),str(pathlib.Path.cwd().joinpath('img','phase06.png')),str(pathlib.Path.cwd().joinpath('img','phase07.png'))]#array holding all the images used in the explosion
class Bomber(pygame.sprite.Sprite):#creates bomber class that inherits pygame.sprite.Sprite methods and attributes
    def __init__(self,bomber_img,fps):
        pygame.sprite.Sprite.__init__(self)
        self.type = "Bomber"#sets enemy type to bomber
        self.image = pygame.image.load(timer[0])#sets image as the bomber image passed in
        self.rect = self.image.get_rect()#creates image image rectangle
        self.rect.center = (random.randrange(50,width),random.randrange(50,height))#sets bomber position to random spot on the screen
        self.radius = 0#sets a zero radius to begin
        self.last_update = pygame.time.get_ticks()#gets ticks
        self.phase = 0#sets default phase value to start of the array
        self.time = 4#sets timer to 3 for the start
        self.fps = fps#sets self.fps to the fps passed in
        self.explode = False#sets self.explode to false

    def explosion(self):#function used for explosion
        instant = pygame.time.get_ticks()#sets instant to ticks
        center = self.rect.center#takes image center to start
        if (instant-self.last_update > self.fps):#checks if instant - last update is greater then fps
            self.last_update = instant#sets last update to the value of instant
            phase_img = phase[self.phase]#gets phase image from the array of images
            self.image = pygame.image.load(phase_img).convert_alpha()#displays image relevant to explosion phase
            self.rect = self.image.get_rect()#sets new collision rect
            self.rect.center = center#sets image center back to original center so the image doesn't wonder
            self.radius = int(self.rect.width//2)#sets self.radius to non zero value now that it has exploded
            self.phase += 1#increases value of self.phase by 1
        if self.phase >= 8:#kills sprite when at the end of phase to prevent going out of array
            self.kill()#kills
        if self.explode == False:#checks if bomb has started explosion
            self.explode = True#sets the self.explode value to true now that it has started
            sound = (pygame.mixer.Sound(str(pathlib.Path.cwd().joinpath('snd','explosion.wav'))))#stores sound effect
            sound.play()#plays sound
    def update(self):#function used to update sprite
        self.time -= 1/self.fps#increments the timer by the inverse of self.fps
        if self.time > 0:
            self.image = pygame.image.load(timer[int(self.time*2)-1]).convert_alpha()
        if self.time < 0:#checks if timer is less than zero
            self.explosion()#function used to manage explosion
#shifter
class Shifter(pygame.sprite.Sprite):#creates shifter and inherits pygame.sprite.Sprite attributes adn methods
    def __init__(self,shifter_img):
        pygame.sprite.Sprite.__init__(self)
        self.type = "Shifter"#sets sprite type to shifter
        self.image_orig = shifter_img#stores the original image
        self.image = self.image_orig.copy()#copies original image to self.image
        self.rect = self.image.get_rect()#gets shifter collision rectangle
        self.rect.x = random.randrange(width - self.rect.width)#sets x coordinate to start at
        self.rect.y = random.randrange(-150, -100)#sets y coordinate to start at
        self.speedy = random.randrange(4, 8)#sets y speed from 4-8
        self.speedx = random.randrange(-3, 3)#sets x speed from -3-3
        self.rot = 0#sets the amount the image has been rotated to
        self.rot_speed = random.randrange(-8, 8)#sets random rotation speed -8-8
        while self.rot_speed == 0:#gets new random value for rotation to prevent no rotation occuring
            self.rot_speed = random.randrange(-8, 8)#sets random rotation speed from -8-8
        self.last_update = pygame.time.get_ticks()#sets lasst update to ticks

    def rotate(self):#function used to rotate the sprite
        now = pygame.time.get_ticks()#sets now to ticks
        if now - self.last_update > 50:#checks if now - last update is greater than 50
            self.last_update = now#sets last update to now
            self.rot = (self.rot + self.rot_speed) % 360#finds amount to rotate image as a percentage of image
            new_image = pygame.transform.rotate(self.image_orig, self.rot)#rotates original image and stores it as new_image
            old_center = self.rect.center#stores old center
            self.image = new_image#sets image to new image that has been rotated
            self.rect = self.image.get_rect()#gets collision rectangle
            self.rect.center = old_center#sets image center to old center to prevent image wondering

    def update(self):#method used to update sprite
        self.rotate()#rotates sprite using rotate method
        self.rect.x += self.speedx#increments x coordinate by x speed
        self.rect.y += self.speedy#increments y coordinate by y speed
        if self.rect.y > height + 50:#checks if sprite is off display
            self.kill()#kills sprite off display
#Glitch
class Glitch(pygame.sprite.Sprite):#create glitch calss
    def __init__(self, glitch_img):#set parameter that need to be passed in dart image and which dart
        pygame.sprite.Sprite.__init__(self)#intialise pygame sprite
        self.type = "Glitch"
        self.image = glitch_img#scale dart image that is passed in to 30x30 pixels
        self.rect = self.image.get_rect()#define image rectangle for collision
        self.radius = 15
        self.rect.center = ((random.randrange(0,width-20)),height + 20)#sets a random position along the bottom of the screen
        self.speedx = random.randrange(-8,8)#sets random horizontal speed to start
        self.speedy = random.randrange(-8,-6)#sets random vertical speed to start with
        self.time = 0.1#self time is assigned to be used to manage the delay later

    def update(self):
        self.rect.y += self.speedy#increases y cooridnate by y speeed
        self.rect.x += self.speedx#increases x cooridnate by x speeed
        if self.time < 0:#checks if the time is less than zero
            self.time = 0.1#timer is reset
            self.speedx = random.randrange(-8,8)#new horizontal speed is set
        self.time -= 1/30#time is reduced by 1/30 to account for frame
        if self.rect.x < -20:#check sprite is within screen width
            self.kill()
        if self.rect.y < -20:#check sprite is within screen height
            self.kill()
#Titan
class Titan(pygame.sprite.Sprite):#creates titan classs and inherits pygame.sprite.Sprite attributes and methods
    def __init__(self,titan_img):
        pygame.sprite.Sprite.__init__(self)
        self.type = "Titan"#defines sprite type as Titan
        self.image = titan_img#sets image to Titan
        self.rect = self.image.get_rect()#gets image rectangle
        self.radius = int(self.rect.width * 0.85 / 2)#gets radius by adjusting image rectangle
        self.rect.x = random.randrange(100,width-100)#sets x to random position
        self.rect.y = (-250)#sets y to -100
        self.lives = 5#sets lives to 5
        self.speedy = random.randrange(1,3)#sets speed from 1-3

    def update(self):#method used to update sprite
        self.rect.y += self.speedy#increments y by y speed
        if self.lives < 0:#kills if it runs out of lives
            self.kill()
        if self.rect.y > height + 250:#checks if sprite is off display
            self.kill()#kills sprite off display
#JSH