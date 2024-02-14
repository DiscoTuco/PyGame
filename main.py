import pygame
from actors import Entity, Player, DoomStyle
from terrain import Obstacle

pygame.init()

win_width = 800
win_height = 600


window = pygame.display.set_mode((win_width, win_height))
doom_surface = pygame.Surface((win_width, win_height))

clock = pygame.time.Clock()

obstacles = []
obstacles.append(Obstacle(window,(50, 50, 200, 100), 'orange'))
obstacles.append(Obstacle(window, (250, 50, 100, 200), 'orange'))
obstacles.append(Obstacle(window,(50, 450, 200, 100), 'orange'))

obstacles.append(Obstacle(window,(0, 0, win_width, 10), 'orange'))
obstacles.append(Obstacle(window,(0, win_height-10, win_width, 10), 'orange'))
obstacles.append(Obstacle(window,(0, 0, 10, win_height-10), 'orange'))
obstacles.append(Obstacle(window,(win_width-10, 0, 10, win_height-10), 'orange'))







doom_style = DoomStyle(doom_surface)
player = Player(doom_style, window, "red", (win_width/2, win_height/2), ('w', 's', 'a', 'd'), 10)

opp = Entity(window, "blue", (win_width/2+100, win_height/2+100), ('i', 'k', 'j', 'l'), 10)
opp2 = Entity(window, "blue", (win_width/2+200, win_height/2+200), ('i', 'k', 'j', 'l'), 10)

run = True
while run:
    clock.tick(60)
    pygame.Surface.fill(window, "black")
    doom_surface.fill("black")

    keys = pygame.key.get_pressed()

    player.move(obstacles, keys)
    player.rotate()
    opp.move(obstacles, keys)
    opp2.move(obstacles, keys)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    for o in obstacles:
        o.draw()

    player.draw(obstacles)

    opp.draw()

    opp2.draw()

    opp.detect(player)
    opp2.detect(player)
    # opp detect opp2 ger bug att om den inte ser båda samtidigt återställs detected_time
    player.sight()

    window.blit(doom_surface, (0, 0, win_width, win_height))

    pygame.display.flip()


pygame.quit()

