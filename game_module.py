import pygame, os, random
pygame.init()
#kolory
SKYBLUE = pygame.color.THECOLORS['skyblue']
DARKRED = pygame.color.THECOLORS['darkred']
LIGHTRED = pygame.color.THECOLORS['palevioletred']
DARKGREEN = pygame.color.THECOLORS['darkgreen']
BLACK = pygame.color.THECOLORS['black']
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']

# okno główne
os.environ['SDL_VIDEO_CENTERED'] = '1'    # centrowanie okna
SIZESCREEN = WIDTH, HEIGHT = 1200, 750
screen = pygame.display.set_mode(SIZESCREEN)


# grafika  - wczytywanie znaków
file_names = sorted(os.listdir(r"\image"))
for file_name in file_names:
    image_name = file_name[:-4]
    if '_L' in image_name or '_R' in image_name:
        image_name = image_name.upper()
    elif 'L' in image_name:
        image_name = image_name.replace('L', '_L').upper()
    elif 'R' in image_name:
        image_name = image_name.replace('R', '_R').upper()
    else:
       image_name = image_name.upper()
    if 'PLAYER_' in image_name:
        image_name = image_name.replace('PLAYER_', '').upper()
    globals().__setitem__(image_name, pygame.image.load(
        os.path.join(r"\image", file_name)))


# grafika postać
IMAGES_R = [WALK_R0, WALK_R1, WALK_R2, WALK_R3, WALK_R4, WALK_R5, WALK_R6, WALK_R7, WALK_R8, WALK_R9]
IMAGES_L = [WALK_L0, WALK_L1, WALK_L2, WALK_L3, WALK_L4, WALK_L5, WALK_L6, WALK_L7, WALK_L8, WALK_L9]

# grafika platformy
GRASS_LIST = [GRASS_S, GRASS_M, GRASS_L, GRASS_F, WATER, BOAT]

TREE_LIST = [TREE_S, TREE_M, TREE_L]

# grafika ściany
WALL_LIST = [WALL, WALL_LEFT, WALL_TOP, WALL_RIGHT, WALL_BOTTOM]
WALL_CORNER_LIST = [WALL_TOP_L, WALL_TOP_R, WALL_BOTTOM_R, WALL_BOTTOM_L]

