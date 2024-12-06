

from  setting import *
from pytmx.util_pygame import load_pygame
from os.path import join
from sprites import Sprite, AnimatedSprite
from groups import AllSprites
from entities import Player
from support import *
import os


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monsters hunter')
        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprites = AllSprites()

        # Import assets and setup
        self.import_assets()
        #cái hospital bị nhỏ di chuyển xuống với qua phải không được
        # self.setup(self.tmx_maps['hospital'], 'world') nhớ tắt code dưới mới chạy được
        self.setup(self.tmx_maps['world'], 'house')

    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(join('..', 'data', 'maps', 'world.tmx')),
                         'hospital': load_pygame(join('..', 'data', 'maps', 'hospital.tmx')),
                         }
        self.overworld_frames ={
            'water': import_folder('..','graphics','tilesets','water'),
            'cost': coast_importer(24,12,'..', 'tilesets', 'coast')
        }



    def setup(self, tmx_map, player_start_pos):
        # Terrain
        for layer in ['Terrain', 'Terrain Top']:
            for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        #object (Không hiển thị object)
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        #Entities (đi xuyên vật thể)
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                self.player = Player((obj.x, obj.y), self.all_sprites)

        #Water
        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites)

        #coast
        for obj in tmx_map.get_layer_by_name('Coast'):
            terrain = obj.properties['terrain']
            side= obj.properties['side']
            AnimatedSprite((obj.x,obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Game logic
            self.all_sprites.update(dt)
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()