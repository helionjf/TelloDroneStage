import pygame


# init la fenetre pour recuperer les input clavier

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


# recupe la touche qui a ete appuyer

def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans
