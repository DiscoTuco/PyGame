import pygame
from math import cos, sin

pygame.init()

win_width = 800
win_height = 600

window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()

run = True


class Entity:
    def __init__(self, root, color, position, controls, size):
        self.root = root
        self.color = color
        self.x, self.y = position
        self.controls = controls
        self.size = size
        self.coordinates = self.x + size, self.y + size

        self.theta = 0
        self.sight_x = sin(self.theta)
        self.sight_y = cos(self.theta)

        self.speed = 5
        self.detected_time = 1


    def self(self):
        pygame.draw.circle(self.root, self.color, (self.x, self.y), self.size)

    def move(self):

        if 'w' in self.controls:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.y += self.sight_y * self.speed
                self.x += self.sight_x * self.speed
            if keys[pygame.K_s]:
                self.y -= self.sight_y * self.speed
                self.x -= self.sight_x * self.speed

        elif 'i' in self.controls:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_j]:
                self.x -= 2
            if keys[pygame.K_l]:
                self.x += 2
            if keys[pygame.K_i]:
                self.y -= 2
            if keys[pygame.K_k]:
                self.y += 2

        self.coordinates = self.x + self.size, self.y + self.size

    def detect(self, other):

        distance = (((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** (1/2))

        # How to do speed = proportional inverse distance?
        while distance <= 100:
            self.x -= ((self.x - other.x)/(self.speed*20))*self.detected_time
            self.y -= ((self.y - other.y)/(self.speed*20))*self.detected_time
            self.detected_time *= 1.005
            print(self.detected_time)
            return pygame.draw.line(self.root, "yellow", (self.x, self.y), (other.x, other.y), 2)
        self.detected_time = 1

    def sight(self):
        pygame.draw.line(self.root, "green", (self.x, self.y), (self.x + self.sight_x*50, self.y + self.sight_y*50), 2)


    def rotate(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.theta += .1
        if keys[pygame.K_d]:
            self.theta -= .1

        self.sight_x = sin(self.theta)
        self.sight_y = cos(self.theta)


player = Entity(window, "red", (win_width/2, win_height/2), ('w', 's', 'a', 'd'), 10)

opp = Entity(window, "blue", (win_width/2+100, win_height/2+100), ('i', 'k', 'j', 'l'), 10)
opp2 = Entity(window, "blue", (win_width/2+200, win_height/2+200), ('i', 'k', 'j', 'l'), 10)


while run:
    clock.tick(60)
    pygame.Surface.fill(window, "black")

    player.move()
    player.rotate()
    opp.move()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    player.self()

    opp.self()

    opp2.self()

    opp.detect(player)
    opp2.detect(player)
    # opp detect opp2 ger bug att om den inte ser båda samtidigt återställs detected_time
    player.sight()

    pygame.display.flip()


pygame.quit()

