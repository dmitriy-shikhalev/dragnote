import pygame.midi


def synths():
    pygame.init()
    pygame.midi.init()
    count = pygame.midi.get_count()
    print("Count of synths is", count)
    for i in range(count):
        info = pygame.midi.get_device_info(i)
        print(i, info)
