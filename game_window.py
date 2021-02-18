import pygame, os, random
import game_module as gm

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

screen = pygame.display.set_mode(gm.SIZESCREEN)
pygame.display.set_caption("Survive and collect")
clock = pygame.time.Clock()
BACKGROUND = pygame.image.load(os.path.join('png', r"\image\background.png")).convert()



class Player(pygame.sprite.Sprite):
    def __init__(self, file_image):
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.items = {}
        self.movement_x = 0
        self.movement_y = 0
        self._count = 0
        self.lifes = 3
        self.level = None
        self.direction_of_movement = 'right'
        self.weapon = 0
        self.fairy1 = 0


    def turn_right(self):
        self.direction_of_movement = 'right'
        self.movement_x = 9

    def turn_left(self):
        self.direction_of_movement = 'left'
        self.movement_x = -9

    def stop(self):
        self.movement_x = 0

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.turn_right()
            if event.key == pygame.K_a:
                self.turn_left()
            if event.key == pygame.K_w:
                self.jump()
            if event.key == pygame.K_f:
                self.shoot()


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.movement_x > 0:
                self.stop()
            if event.key == pygame.K_a and self.movement_x < 0:
                self.stop()

    def update(self):
        self._gravitation()

        self.rect.x += self.movement_x

        if self.movement_x > 0:
            self._move(gm.IMAGES_R)
        if self.movement_x < 0:
            self._move(gm.IMAGES_L)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def _move(self, image_list):
        if self._count < 1:
            self.image = image_list[0]
        elif self._count < 2:
            self.image = image_list[1]
        elif self._count < 3:
            self.image = image_list[2]
        elif self._count < 4:
            self.image = image_list[3]
        elif self._count < 5:
            self.image = image_list[4]
        elif self._count < 6:
            self.image = image_list[5]
        elif self._count < 7:
            self.image = image_list[6]
        elif self._count < 8:
            self.image = image_list[7]
        elif self._count < 9:
            self.image = image_list[8]
        elif self._count < 10:
            self.image = image_list[9]
        if self._count >= 10:
            self._count = 0
        else:
            self._count += 1


# konkretyzacja obiektow
player = Player(gm.STAND_R)
player.rect.center = screen.get_rect().center

# glowna petla
window_open = True
active_game = False
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