import pygame, os, random
import game_module as gm

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

screen = pygame.display.set_mode(gm.SIZESCREEN)
pygame.display.set_caption("Survive and collect")
clock = pygame.time.Clock()
BACKGROUND = pygame.image.load(os.path.join('png', r"\image\background.png")).convert()

window_open = True
while window_open:
    screen.fill(gm.LIGHTBLUE)
    # pętla zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        elif event.type == pygame.QUIT:
            window_open = False

    # aktualizacja okna pygame
    pygame.display.flip()
    clock.tick(30)

pygame.quit()