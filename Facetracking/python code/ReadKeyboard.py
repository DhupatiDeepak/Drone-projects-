import pygame

pygame.init()
virtualTrackWin = pygame.display.set_mode((300,300))

def KeyRead(keyName):
    keyValue = False
    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    Input = getattr(pygame,'K_{}'.format(keyName))
    if keyInput[Input]:
        keyValue = True
    pygame.display.update()
    return keyValue