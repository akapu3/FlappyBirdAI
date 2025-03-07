import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMG = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

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


class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) # Flipped Pipe
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VELOCITY
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)
    

        if top_point or bottom_point:
            return True
        else:
            return False


class Base:
    VELOCITY = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))



    
def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("SCORE: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 5))
    
    base.draw(win)
    bird.draw(win)


    pygame.display.update()

def main():
    pygame.init()
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    score = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        base.move()
        add_pipe = False
        
        rem = []
        for pipe in pipes:
            if(pipe.collide(bird)):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            
            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        
        for pipe in rem:
            pipes.remove(pipe)

        if bird.y + bird.image.get_height() >= 730:
            pass
        


        draw_window(win, bird, pipes, base, score)
    pygame.quit()

if __name__ == "__main__":
    main()