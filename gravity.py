#!/usr/bin/python3

import pygame
import universe

pygame.init()
x=1200
y=x*3/4
window = pygame.display.set_mode((x,y))
clock = pygame.time.Clock()
start = True

#rock1 = universe.Rock(10000.,1024/2,768/3,3,0)
#rock2 = universe.Rock(10000,1024/2,768/2,0,0)
uni = universe.Universe(3000, 75, x, y)
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            start = False
    window.fill("blue")
#    rock1.applyGravity(rock2)
#    rock1.doIteration()
#    rock2.doIteration()
#    rock1.draw(window)
#    rock2.draw(window)
    uni.doIteration()
    uni.draw(window)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
