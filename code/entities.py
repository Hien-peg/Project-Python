import pygame
from pygame.math import Vector2
from setting import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups,facing_direction):
        super().__init__(groups)
        self.z= WORLD_LAYERS['main']

        #graphics
        self.frames_index, self.frames = 0,frames
        self.facing_direction = facing_direction

        #movement
        self.direction = Vector2()  # Dùng Vector2 thay cho vector()
        self.speed =250

        #sprite setup
        self.image =self.frames[self.get_state()][self.frames_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox =self.rect.inflate(-self.rect.width/2, -60)
        self.y_sort = self.rect.centery


    def animate(self,dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.get_state()][int(self.frames_index % len(self.frames[self.get_state()]))]

    def get_state(self):
        #logic
        moving= bool(self.direction)
        if moving:
            if self.direction.x  !=0:
                self.facing_direction = 'right' if self.direction.x >0 else 'left'
            if self.direction.y  !=0:
                self.facing_direction = 'down' if self.direction.y >0 else 'up'
        return f'{self.facing_direction}{"_idle" if not moving else ""}'

class Character(Entity):
    def __init__(self, pos, frames, groups,facing_direction):
        super().__init__(pos, frames, groups,facing_direction)

class Player(Entity):
    def __init__(self, pos,frames ,groups,facing_direction, collision_sprites):
        super().__init__(pos,frames,groups,facing_direction)
        self.collision_sprites = collision_sprites


    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = Vector2()
        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector.normalize() if input_vector else input_vector


    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.hitbox.centerx = self.rect.centerx
        self.collision('horizontal')

        self.rect.centery += self.direction.y * self.speed * dt
        self.hitbox.centery = self.rect.centery
        self.collision('vertical')

    def collision(self,axis):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x >0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x <0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    if self.direction.y >0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery

    def update(self, dt):
        self.y_sort = self.rect.centery
        self.input()
        self.move(dt)
        self.animate(dt)
