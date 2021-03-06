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

    def jump(self):
        self.rect.y += 2
        colliding_platform = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)
        self.rect.y -= 2
        if colliding_platform:
            self.movement_y = -14

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

        # ----------------- ruch w poziomie-------------------------
        self.rect.x += self.movement_x

        # sprawdzamy kolizję
        colliding_platform = pygame.sprite.spritecollide(self, self.level.set_of_platforms | self.level.set_of_walls, False)
        for p in colliding_platform:
            if self.movement_x > 0:
                self.rect.right = p.rect.left
            if self.movement_x < 0:
                self.rect.left = p.rect.right

        if self.movement_x > 0:
            self._move(gm.IMAGES_R)
        if self.movement_x < 0:
            self._move(gm.IMAGES_L)

        # ----------------------------ruch w pionie------------------------------------
        self.rect.y += self.movement_y

        # sprawdzamy kolizję
        colliding_platform = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)
        for p in colliding_platform:
            if self.movement_y > 0:
                self.rect.bottom = p.rect.top
                if self.direction_of_movement == 'left' and self.movement_x == 0:
                    self.image = gm.STAND_L
                if self.direction_of_movement == 'right' and self.movement_x == 0:
                    self.image = gm.STAND_R
            if self.movement_y < 0:
                self.rect.top = p.rect.bottom

            self.movement_y = 0

            if isinstance(p, MovingPlatform) and self.movement_x == 0:
                self.rect.x += p.movement_x

        self.rect.y += 4
        colliding_platform = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)
        self.rect.y -= 4
        if not colliding_platform:
            if self.movement_y > 0:
                if self.direction_of_movement == 'left':
                    self.image = gm.WALK_L2
                else:
                    self.image = gm.WALK_R2

            if self.movement_y < 0:
                if self.direction_of_movement == 'left':
                    self.image = gm.WALK_L1
                else:
                    self.image = gm.WALK_R1

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

    def _gravitation(self):
        if self.movement_y == 0:
            self.movement_y = 1
        else:
            self.movement_y += 0.55



# klasa platformy
class Platform(pygame.sprite.Sprite):
    def __init__(self, image_list, width, height, rect_x, rect_y):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.image_list = image_list

    def draw(self, surface):
        if (self.width % 227) == 0 :
            surface.blit(self.image_list[2], self.rect)
            for i in range(227, self.width - 227, 227):
                surface.blit(self.image_list[2], [self.rect.x + i, self.rect.y])
            surface.blit(self.image_list[2], [self.rect.x + self.rect.width - 227, self.rect.y])
        elif (self.width % 60) == 0 :
            surface.blit(self.image_list[0], self.rect)
            for i in range(60, self.width - 60, 60):
                surface.blit(self.image_list[0], [self.rect.x + i, self.rect.y])
            surface.blit(self.image_list[0], [self.rect.x + self.rect.width - 60, self.rect.y])
        elif (self.width % 74) == 0:
            surface.blit(self.image_list[1], self.rect)
            for i in range(74, self.width - 74, 74):
                surface.blit(self.image_list[1], [self.rect.x + i, self.rect.y])
            surface.blit(self.image_list[1], [self.rect.x + self.rect.width - 74, self.rect.y])
        elif (self.width % 226) == 0:
            surface.blit(self.image_list[3], self.rect)
            for i in range(226, self.width - 226, 226):
                surface.blit(self.image_list[3], [self.rect.x + i, self.rect.y])
            surface.blit(self.image_list[3], [self.rect.x + self.rect.width - 226, self.rect.y])
        elif (self.width % 63) == 0:
            surface.blit(self.image_list[4], self.rect)
            for i in range(63, self.width - 63, 63):
                surface.blit(self.image_list[4], [self.rect.x + i, self.rect.y])
            surface.blit(self.image_list[4], [self.rect.x + self.rect.width - 63, self.rect.y])
        elif (self.width % 237) == 0:
            surface.blit(self.image_list[5], self.rect)
            for i in range(237, self.width - 237, 237):
                surface.blit(self.image_list[5], [self.rect.x + i, self.rect.y])
            surface.blit(self.image_list[5], [self.rect.x + self.rect.width - 237, self.rect.y])
        else:
            surface.blit(self.image_list[3], self.rect)
            for i in range(179, self.width - 179, 179):
                surface.blit(self.image_list[3], [self.rect.x + i, self.rect.y])
            surface.blit(self.image_list[3], [self.rect.x + self.rect.width - 179, self.rect.y])


#ogólna klasa planszy
class Level:
    def __init__(self, player):
        self.set_of_platforms = set()
        self.player = player

    def update(self):
        for p in self.set_of_platforms:
            p.update()

    def draw(self, surface):
        for p in self.set_of_platforms:
            p.draw(surface)


# klasa planszy nr1
class Level_1(Level):
    def __init__(self, player=None):
        super().__init__(player)
        self._create_platforms()
        self.create_walls()
        self.create_moving_platforms()
        self.create_items()
        self.create_platform_enemies()
        self.create_flaying_enemies()


    def _create_platforms(self):
        ws_platform_static = [[66 * 63, 63, -13, gm.HEIGHT - 63],
                              [9 * 74, 76, 100, 500],
                              [226, 54, 1000, 250],
                              [10 * 60, 40, 3100, 400],
                              [5 * 60, 40, 2900, 200]]

        for ws in ws_platform_static:
            object_P = Platform(gm.GRASS_LIST, *ws)
            self.set_of_platforms.add(object_P)

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

        player.get_event(event)

    # rysowanie i aktualizacja obiektów
    player.update()
    player.draw(screen)
    current_level.draw(screen)

    # aktualizacja okna pygame
    pygame.display.flip()
    clock.tick(30)

pygame.quit()