import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMG = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


    

class Bird:
    IMGS = BIRD_IMG
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0 
        self.tick_count = 0 # keeps track of when we last jumped
        self.velocity = 0
        self.height = self.y # keeps track of position when bird last jumped
        self.image_count = 0 #how many times an image has been shown
        self.image = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0 
        self.height = self.y 

    def move(self):
        self.tick_count += 1
        
        s = self.velocity * self.tick_count + 1.5 * self.tick_count**2 #s = vt + 3/2 t^2

        if s >= 16:
            s = 16 #terminal velocity

        if s < 0:
            s -= 2

        self.y += s

        #upward tilt
        if s < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        #Downward Tilt
        else: 
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY
        
    def draw(self, win): #Draw the flappy brird
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_count < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        elif self.image_count < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        elif self.image_count == self.ANIMATION_TIME*4 + 1:
            self.image = self.IMGS[0]
            self.image_count = 0
    
        if self.tilt <= -80:
            self.image = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME * 2
        
        #Rotates Image around its center - source: StackOverFlow
        rotated_image = pygame.transform.rotate(self.image, self.tilt) 
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.x, self.y)).center) 
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    pygame.init()

    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)
    pygame.quit()

if __name__ == "__main__":
    main()