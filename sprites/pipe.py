import pygame as pg


class Pipe(pg.sprite.Sprite):
  def __init__(self, x:int, y:int, is_bottom: bool) -> None:
    super().__init__()

    self.image = pg.image.load('assets/pipe.png')
    if not is_bottom:
      self.image = pg.transform.flip(self.image, False, True)
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y) if is_bottom else (x, y - self.rect.height)
    self.passed = False

  def update(self) -> None:
    self.rect.x -= 4
    if self.rect.right < 0:
      self.kill()

  def draw(self, win: pg.Surface) -> None:
    win.blit(self.image, self.rect.topleft)
