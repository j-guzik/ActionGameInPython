import pygame, os, random
import game_module as gm

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

screen = pygame.display.set_mode(gm.SIZESCREEN)
pygame.display.set_caption("Survive and collect")
clock = pygame.time.Clock()
BACKGROUND = pygame.image.load(os.path.join('png', r"C:\image\background.png")).convert()


# klasa gracza
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

    def jump(self):
        self.rect.y += 2
        colliding_platform = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)
        self.rect.y -= 2
        if colliding_platform:
            self.movement_y = -14

    def shoot(self):
        if self.weapon > 0:
            if self.direction_of_movement == 'left':
                self.image = gm.WALK_L2
                arrow = Arrow(gm.ARROW_L, self.direction_of_movement)
            else:
                self.image = gm.WALK_R2
                arrow = Arrow(gm.ARROW_R, self.direction_of_movement)
            arrow.rect.center = (self.rect.centerx, self.rect.centery)
            self.level.set_of_arrows.add(arrow)
            self.weapon -= 1

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

        # spr. kolizji z bronia
        colliding_items = pygame.sprite.spritecollide(self, self.level.set_of_items, False)

        for item in colliding_items:
            if item.name == "arrowFree":
                self.weapon += 2
                item.kill()
            if item.name == "life":
                self.lifes += 1
                item.kill()
            if item.name == 'door':
                del self.level
                self.level = Level_2(self)
                self.level.draw(screen)
                player.rect.bottom = gm.HEIGHT - 400
                player.rect.x = 300
                self.image = gm.STAND
                self.rect.x += 150
                self.stop()
            if item.name == 'fairy1':
                player.fairy1 +=1

        # spr. kolizja z wrogiem lub przepaść

        colliding_enemies = pygame.sprite.spritecollide(self, self.level.set_of_enemies, False)
        for enemy in colliding_enemies:
            if enemy.lifes:
                self.lifes -= 1
                player.rect.bottom = gm.HEIGHT - 450
                player.rect.x = 400 + self.level.world_shift


        colliding_enemy_arrows = pygame.sprite.spritecollide(self, self.level.set_of_enemy_arrows, False)
        for enemy_arrows in colliding_enemy_arrows:
            self.lifes -= 1
            player.rect.bottom = gm.HEIGHT - 450
            player.rect.x = 400 + self.level.world_shift


        if self.rect.top > (gm.HEIGHT - 154):
            self.lifes -= 1
            player.rect.bottom = gm.HEIGHT - 450
            player.rect.x = 400 + self.level.world_shift




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



class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_image, image_list_right, image_list_left, image_list_right_dead, image_list_left_dead,
                 movement_x=0, movement_y=0):
        super().__init__()
        self.image = start_image
        self.rect = self.image.get_rect()
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.direction_of_movement = 'right'
        self.image_list_right = image_list_right
        self.image_list_left = image_list_left
        self.image_list_right_dead = image_list_right_dead
        self.image_list_left_dead = image_list_left_dead
        self._count = 0
        self.lifes = 1

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

    def update(self):
        if not self.lifes and self._count > 7:
            self.kill()

        self.rect.x += self.movement_x

        if self.lifes:
            if self.movement_x > 0:
                self._move(self.image_list_right)
            if self.movement_x < 0:
                self._move(self.image_list_left)
        else:
            if self.direction_of_movement == 'right':
                self._move(self.image_list_right_dead)
            else:
                self._move(self.image_list_left_dead)

        if self.movement_x > 0 and self.direction_of_movement == 'left':
            self.direction_of_movement = 'right'
        if self.movement_x < 0 and self.direction_of_movement == 'right':
            self.direction_of_movement = 'left'


class PlatformEnemy(Enemy):
    def __init__(self, start_image, image_list_right, image_list_left, image_list_right_dead, image_list_left_dead,
                 platform, movement_x=0, movement_y=0):
        super().__init__(start_image, image_list_right, image_list_left, image_list_right_dead, image_list_left_dead,
                         movement_x, movement_y)
        self.platform = platform
        self.rect.bottom = self.platform.rect.top
        self.rect.centerx = random.randint(self.platform.rect.left + self.rect.width,
                                           self.platform.rect.right - self.rect.width)

    def update(self):
        super(PlatformEnemy, self).update()
        if (self.rect.right > self.platform.rect.right or self.rect.left < self.platform.rect.left):
            self.movement_x *= -1


class FlyingEnemy(Enemy):
    def __init__(self, start_image, image_list_right,
                 image_list_left, image_list_right_dead, image_list_left_dead,
                 movement_x = 0, movement_y = 0, boundary_right = 0, boundary_left = 0,
                 boundary_top = 0, boundary_bottom = 0):
        super().__init__(start_image, image_list_right,
                 image_list_left, image_list_right_dead, image_list_left_dead,
                 movement_x, movement_y)

        self.boundary_right = boundary_right
        self.boundary_left = boundary_left
        self.boundary_top = boundary_top
        self.boundary_bottom = boundary_bottom
        self.level = None
        self.sleep = True
    def shoot(self):
        firebool = Arrow(gm.FIREBOOL, self.direction_of_movement)
        firebool.rect.center = (self.rect.centerx, self.rect.centery)
        self.level.set_of_enemy_arrows.add(firebool)

    def update(self):
        if self.sleep:
            if self.rect.left - self.level.player.rect.right < 500:
                self.sleep = False
        else:
            super().update()
            self.rect.y += self.movement_y
            position = self.rect.x - self.level.world_shift
            if (position < self.boundary_left or
                    position + self.rect.width > self.boundary_right):
                self.movement_x *= -1
            if (self.rect.top < self.boundary_top or
                    self.rect.bottom > self.boundary_bottom):
                self.movement_y *= -1

            # losowe strzały i skoki
            if (self.image_list_left[5] == gm.FAIRY2_L[5] or self.image_list_right[5] == gm.FAIRY2_R[5]):
                if not random.randint(1, 100) % 30:
                    self.shoot()



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

class MovingPlatform(Platform):
    def __init__(self, image_list, width, height, rect_x, rect_y):
        super().__init__(image_list, width, height, rect_x, rect_y)
        self.movement_x = 0
        self.movement_y = 0
        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_right = 0
        self.boundary_left = 0
        self.player = None

    def update(self):
        self.rect.x += self.movement_x
        if pygame.sprite.collide_rect(self, self.player):
            if self.movement_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        self.rect.y += self.movement_y
        if pygame.sprite.collide_rect(self, self.player):
            if self.movement_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        if (self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top):
            self.movement_y *= -1

        position = self.rect.x - self.player.level.world_shift
        if (position + self.width > self.boundary_right or position < self.boundary_left):
            self.movement_x *= -1


# ogolna klasa przedmiotu
class Item(pygame.sprite.Sprite):
    def __init__(self, image, name):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name


class Arrow(pygame.sprite.Sprite):  ##Arrow zamiast Bullet
    def __init__(self, image_file, direction):
        super().__init__()
        self.image = image_file
        self.rect = self.image.get_rect()
        self.direction_of_movement = direction

    def update(self):
        if self.direction_of_movement == 'right':
            self.rect.x += 20
        else:
            self.rect.x -= 20


class Wall(Platform):
    def __init__(self, image_list, image_corner_list, width, height, rect_x, rect_y):
        super().__init__(image_list, width, height, rect_x, rect_y)
        self.image_corner_list = image_corner_list


    def draw(self, surface):
        for row in range(0, self.height, 77):
            if row == 0:
                surface.blit(self.image_corner_list[0], self.rect)
                for column in range(77, self.width - 77, 77):
                    surface.blit(self.image_list[2], [self.rect.x + column, self.rect.y])
                surface.blit(self.image_corner_list[1],
                             [self.rect.x + self.width - 77, self.rect.y])

            elif row == self.height - 77:
                surface.blit(self.image_list[1],
                             [self.rect.x, self.rect.y + row])
                for column in range(77, self.width - 77, 77):
                    surface.blit(self.image_list[4],
                                 [self.rect.x + column, self.rect.y + row])
                surface.blit(self.image_list[3],
                             [self.rect.x + self.width - 77, self.rect.y + row])

            else:
                surface.blit(self.image_list[1],
                             [self.rect.x, self.rect.y + row])
                for column in range(77, self.width - 77, 77):
                    surface.blit(self.image_list[0], [self.rect.x + column, self.rect.y + row])
                surface.blit(self.image_list[3],
                             [self.rect.x + self.width - 77, self.rect.y + row])

# ogolna klasa planszy
class Level:
    def __init__(self, player):
        self.set_of_platforms = set()
        self.set_of_walls = set()
        self.set_of_items = pygame.sprite.Group()
        self.set_of_enemy_arrows = pygame.sprite.Group()
        self.set_of_arrows = pygame.sprite.Group()
        self.set_of_enemies = pygame.sprite.Group()
        self.player = player
        self.world_shift = 0

    def update(self):
        self.__delete__arrows()
        for p in self.set_of_platforms:
            p.update()
        self.set_of_arrows.update()
        self.set_of_enemies.update()
        self.set_of_enemy_arrows.update()

        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500
            self.player.rect.right = 500
            self._shift_world(-diff)

        if self.player.rect.left <= 150:
            diff = 150 - self.player.rect.left
            self.player.rect.left = 150
            self._shift_world(diff)


    def __delete__arrows(self):

        pygame.sprite.groupcollide(self.set_of_arrows,
                                   self.set_of_enemy_arrows, True, True)
        pygame.sprite.groupcollide(self.set_of_enemy_arrows,
                                   self.set_of_platforms | self.set_of_walls, True, False)
        pygame.sprite.groupcollide(self.set_of_arrows,
                                   self.set_of_platforms | self.set_of_walls, True, False)
        for arrow in self.set_of_arrows:
            if arrow.rect.left > gm.WIDTH or arrow.rect.right < 0:
                arrow.kill()

            colliding_enemies = pygame.sprite.spritecollide(
                arrow, self.set_of_enemies, False)
            for enemy in colliding_enemies:
                arrow.kill()
                if enemy.lifes:
                    enemy.lifes -= 1
                    if not enemy.lifes:
                        enemy._count = 0

    def draw(self, surface):
        for p in self.set_of_platforms | self.set_of_walls:
            p.draw(surface)

        self.set_of_items.draw(surface)
        self.set_of_arrows.draw(surface)
        self.set_of_enemies.draw(surface)
        self.set_of_enemy_arrows.draw(surface)

        # rysowanie strzal
        for i in range(player.weapon):
            surface.blit(gm.ARROW, [40 * i + 20, 15])

        for i in range(player.lifes):
            surface.blit(gm.HEARTS, [40*i + 1000, 25])


    def _shift_world(self, shift_x):
        self.world_shift += shift_x

        for p in self.set_of_platforms | self.set_of_walls:
            p.rect.x += shift_x

        for item in self.set_of_items:
            item.rect.x += shift_x

        for a in self.set_of_arrows:
            a.rect.x += shift_x

        for f in self.set_of_enemy_arrows:
            f.rect.x += shift_x

        for e in self.set_of_enemies:
            e.rect.x += shift_x



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

    def create_moving_platforms(self):
        mp_x = MovingPlatform(gm.GRASS_LIST, 227, 27, 1900, 550)
        mp_x.boundary_right = 2200
        mp_x.boundary_left = 1700
        mp_x.movement_x = -2
        mp_x.player = self.player
        self.set_of_platforms.add(mp_x)

        mp_y = MovingPlatform(gm.GRASS_LIST, 4 * 60, 40, 1400, 400)
        mp_y.boundary_top = 350
        mp_y.boundary_bottom = 550
        mp_y.movement_y = 1
        mp_y.player = self.player
        self.set_of_platforms.add(mp_y)

        mp_y = MovingPlatform(gm.GRASS_LIST, 227, 27, 2050, 400)
        mp_y.boundary_top = 350
        mp_y.boundary_bottom = 500
        mp_y.movement_y = 1
        mp_y.player = self.player
        self.set_of_platforms.add(mp_y)

    def create_items(self):
        # strzaly
        arrowFree = Item(gm.ARROWFREE, "arrowFree")
        arrowFree.rect.center = [300, gm.HEIGHT - 280]
        self.set_of_items.add(arrowFree)

        arrowFree = Item(gm.ARROWFREE, "arrowFree")
        arrowFree.rect.center = [1180, gm.HEIGHT - 535]
        self.set_of_items.add(arrowFree)

        arrowFree = Item(gm.ARROWFREE, "arrowFree")
        arrowFree.rect.center = [3100, 370]
        self.set_of_items.add(arrowFree)
        #znak
        sign = Item(gm.JM, 'sign')
        sign.rect.center = [400, gm.HEIGHT - 165 - 2 * sign.rect.h]
        self.set_of_items.add(sign)
        #drzwi
        door = Item(gm.DOOR, 'door')
        door.rect.center = [3500, gm.HEIGHT - 85 - 2 * door.rect.h]
        self.set_of_items.add(door)
        #drzewo
        tree = Item(gm.TREE, 'tree')
        tree.rect.center = [1100, gm.HEIGHT - 255 - 2 * tree.rect.h]
        self.set_of_items.add(tree)

    def create_platform_enemies(self):
        ws_platform_static = [[2*179, 54, 950, 400], [5 * 60, 40, 2400, 260]]
        for ws in ws_platform_static:
            platform = Platform(gm.GRASS_LIST, *ws)
            self.set_of_platforms.add(platform)
            platform_enemy = PlatformEnemy(gm.WARRIOR_STAND, gm.WARRIOR_R, gm.WARRIOR_L, gm.WARRIOR_DEAD_R,
                                           gm.WARRIOR_DEAD_L, platform,
                                           random.choice([-3, -2, -1, 1, 2, 3]))

            self.set_of_enemies.add(platform_enemy)

    def create_walls(self):
        ws_wall = [[4 * 77, 10 * 77, -4 * 77, 0], [10 * 77, 10 * 77, 4100, 0]]
        for ws in ws_wall:
            wall = Wall(gm.WALL_LIST, gm.WALL_CORNER_LIST, *ws)
            self.set_of_walls.add(wall)


    def create_flaying_enemies(self):
        fairy = FlyingEnemy(gm.FAIRY2_FLYATTACK_R0, gm.FAIRY2_R,
                          gm.FAIRY2_L, gm.FAIRY2_DEAD_R, gm.FAIRY2_DEAD_L,
                          boundary_right=2200,
                          boundary_left=1200,
                          boundary_top=70,
                          boundary_bottom=330,
                          movement_x=random.choice([-4,-3,-2,2,3,4]),
                          movement_y=random.choice([-4,-3,-2,-1,1,2,3,4]))
        fairy.level = self
        fairy.rect.x = 1400
        fairy.rect.y = 70
        self.set_of_enemies.add(fairy)

class Level_2(Level):
    def __init__(self, player=None):
        super().__init__(player)
        self.create_walls()
        self.create_moving_platforms()
        self._create_platforms()
        self.create_knight()
        self.create_items()
        self.create_platform_enemies()
        self.create_flaying_enemies()


    def _create_platforms(self):
        ws_platform_static = [[75 * 63, 63, -13, gm.HEIGHT - 63],
                              [15*40, 60, 100, 300],
                              [4*227, 27, 2500,300],
                              [227, 27, 4181,550]]

        for ws in ws_platform_static:
            object_P = Platform(gm.GRASS_LIST, *ws)
            self.set_of_platforms.add(object_P)
    def create_moving_platforms(self):
        mp_x = MovingPlatform(gm.GRASS_LIST, 237, 27, 200, 650)
        mp_x.boundary_right = 900
        mp_x.boundary_left = 50
        mp_x.movement_x = -4
        mp_x.player = self.player
        self.set_of_platforms.add(mp_x)
        mp_y = MovingPlatform(gm.GRASS_LIST, 2*227, 40, 1400, 400)
        mp_y.boundary_top = 300
        mp_y.boundary_bottom = 450
        mp_y.movement_y = 1
        mp_y.player = self.player
        self.set_of_platforms.add(mp_y)
        mp_y = MovingPlatform(gm.GRASS_LIST, 227, 27, 2050, 400)
        mp_y.boundary_top = 350
        mp_y.boundary_bottom = 500
        mp_y.movement_y = 1
        mp_y.player = self.player
        self.set_of_platforms.add(mp_y)
    def create_items(self):
        # strzaly
        arrowFree = Item(gm.ARROWFREE, "arrowFree")
        arrowFree.rect.center = [400, gm.HEIGHT -130 - 2 * arrowFree.rect.h]
        self.set_of_items.add(arrowFree)
        arrowFree = Item(gm.ARROWFREE, "arrowFree")
        arrowFree.rect.center = [100, gm.HEIGHT - 130 - 2 * arrowFree.rect.h]
        self.set_of_items.add(arrowFree)
        arrowFree = Item(gm.ARROWFREE, "arrowFree")
        arrowFree.rect.center = [1180, gm.HEIGHT - 125 - 2 * arrowFree.rect.h]
        self.set_of_items.add(arrowFree)
        arrowFree = Item(gm.ARROWFREE, "arrowFree")
        arrowFree.rect.center = [1480, gm.HEIGHT - 125 - 2 * arrowFree.rect.h]
        self.set_of_items.add(arrowFree)
        #życie
        life = Item(gm.HEARTS, 'life')
        life.rect.center = [500, gm.HEIGHT + 14 - 8 * life.rect.h]
        self.set_of_items.add(life)
        #znak
        sign = Item(gm.JM, 'sign')
        sign.rect.center = [400, gm.HEIGHT - 365 - 2 * sign.rect.h]
        self.set_of_items.add(sign)
        #drzwi
        door2 = Item(gm.DOOR2, 'door2')
        door2.rect.center = [500, gm.HEIGHT - 185 - 2 * door2.rect.h]
        self.set_of_items.add(door2)
        #wrozka
        fairy1 = Item(gm.FAIRY_L0, 'fairy1')
        fairy1.rect.center = [4300, gm.HEIGHT - 250]
        self.set_of_items.add(fairy1)

    227, 27, 4181, 550
    def create_platform_enemies(self):
        ws_platform_static = [[4*60, 27, 1200, 600], [4*60, 27, 1800, 600], [227, 27, 2500,300], [227, 27, 2728,300]]
        for ws in ws_platform_static:
            platform = Platform(gm.GRASS_LIST, *ws)
            self.set_of_platforms.add(platform)
            platform_enemy = PlatformEnemy(gm.WARRIOR_STAND, gm.WARRIOR_R, gm.WARRIOR_L, gm.WARRIOR_DEAD_R,
                                           gm.WARRIOR_DEAD_L, platform,
                                           random.choice([-3, -2, -1, 1, 2, 3]))
            self.set_of_enemies.add(platform_enemy)
    def create_knight(self):
        ws_platform_static = [[3*227, 27, 3500,550]]
        for ws in ws_platform_static:
            platform = Platform(gm.GRASS_LIST, *ws)
            self.set_of_platforms.add(platform)
            platform_enemy = PlatformEnemy(gm.KNIGHT_WALK_R0, gm.KNIGHT_R, gm.KNIGHT_L, gm.KNIGHT_DEAD_R,
                                           gm.KNIGHT_DEAD_L, platform,
                                           random.choice([-3, -2, -1, 1, 2, 3]))
            self.set_of_enemies.add(platform_enemy)




    def create_walls(self):
        ws_wall = [[4 * 77, 10 * 77, -4 * 77, 0], [10 * 77, 10 * 77, 4700, 0]]
        for ws in ws_wall:
            wall = Wall(gm.WALL_LIST, gm.WALL_CORNER_LIST, *ws)
            self.set_of_walls.add(wall)

    def create_flaying_enemies(self):
        fairy = FlyingEnemy(gm.FAIRY2_FLYATTACK_R0, gm.FAIRY2_R,
                          gm.FAIRY2_L, gm.FAIRY2_DEAD_R, gm.FAIRY2_DEAD_L,
                          boundary_right=2600,
                          boundary_left=1800,
                          boundary_top=70,
                          boundary_bottom=330,
                          movement_x=random.choice([-3,-2,2,3]),
                          movement_y=random.choice([-3,-2,-1,1,2,3]))
        fairy.level = self
        fairy.rect.x = 2000
        fairy.rect.y = 70
        self.set_of_enemies.add(fairy)



class Text:
    def __init__(self, text, text_colour,type_font = None, size=90):
        self.text = str(text)
        self.text_colour = text_colour
        self.type_font = type_font
        self.size = size
        self.font = pygame.font.SysFont(self.type_font, self.size)
        self.image = self.font.render(self.text, 1, self.text_colour)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Button:
    def __init__(self, text, width, height, text_colour,background_colour, centerx, centery, type_font, size):
        self.text = str(text)
        self.text_colour = text_colour
        self.type_font = type_font
        self.size = size
        self.width = width
        self.height = height
        self.background_colour = background_colour
        self.font = pygame.font.SysFont(self.type_font, self.size)
        self.image = self.font.render(self.text, 1, self.text_colour, self.background_colour)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (centerx, centery)
        self.rect_image = self.image.get_rect()
        self.rect_image.center = self.rect.center

    def draw(self, surface):
        surface.fill(self.background_colour, self.rect)
        surface.blit(self.image, self.rect_image)
# konkretyzacja obiektow
player = Player(gm.STAND_R)
current_level = Level_1(player)
player.level = current_level
player.rect.center = screen.get_rect().center
end_text = Text("Koniec gry!", gm.BLACK)
end_text.rect.center = screen.get_rect().center
button = Button("ZACZNIJ GRE!", 300, 250, gm.BLACK,gm.DARKRED, gm.WIDTH//2, gm.HEIGHT//2, 'Arial', 90)
finish_text = Text("Uratowałeś księżniczkę!", gm. LIGHTGREEN)
finish_text.rect.center = screen.get_rect().center
finish_button = Button("Exit!", 400, 150, gm.BLACK,gm.DARKRED, gm.WIDTH//2, gm.HEIGHT//1.5, 'Arial', 90)
# glowna petla
window_open = True
active_game = False
while window_open:
    screen.fill(gm.BLACK)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        elif event.type == pygame.QUIT:
            window_open = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                active_game = True
                pygame.mouse.set_visible(False)
            if finish_button.rect.collidepoint(pygame.mouse.get_pos()):
                window_open = False


        if active_game:
            player.get_event(event)
    if active_game:
        if player.fairy1 > 1:
            active_game = False
            pygame.mouse.set_visible(True)
        if not player.lifes:
            window_open = False

    # rysowanie i aktualizacja obiektow
        screen.blit(BACKGROUND, [0, 0])
        player.update()
        current_level = player.level
        current_level.update()
        current_level.draw(screen)
        player.draw(screen)
    elif (active_game == False) and (player.lifes > 0) and (player.fairy1 > 0):
        pygame.mouse.set_visible(True)
        finish_text.draw(screen)
        # finish_button.draw(screen)
    else:
        pygame.mouse.set_visible(True)
        button.draw(screen)




    # aktualizacja okna pygame
    pygame.display.flip()
    clock.tick(30)


screen.fill(gm.LIGHTGREEN)
end_text.draw(screen)
pygame.display.flip()
pygame.time.delay(3000)
pygame.quit()