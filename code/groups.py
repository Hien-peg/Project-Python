from setting import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def draw(self, player_center):
        # Tính offset dựa trên vị trí của player
        self.offset.x = -(player_center[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_center[1] - WINDOW_HEIGHT / 2)

        # Hiển thị tất cả các sprite với offset
        for sprite in self:
            if sprite.image and sprite.rect:  # Kiểm tra sprite hợp lệ
                offset_rect = sprite.rect.copy()
                offset_rect.topleft += self.offset
                self.display_surface.blit(sprite.image, offset_rect)