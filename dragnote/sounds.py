import pygame
file = 'sounds/a59760104f31c56.mp3'
# file = 'sounds/erroneous-action.wav'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
pygame.event.wait()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
