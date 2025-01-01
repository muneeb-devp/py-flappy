from pygame.sprite import Sprite
from pygame.image import load
from pygame.key import get_pressed
import pygame as pg


class Bird(Sprite):
  def __init__(self, x:int, y:int) -> None:
    super().__init__()

    self.images = list()
    self.index = 0
    self.counter = 0

    for n in range(1, 4): self.images.append(load(f'assets/bird{n}.png'))

    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.gravity = 0
    self.flying = False
    self.game_over = False

  def update(self):
    if pg.mouse.get_pressed()[0] == 1 and self.rect.top > 10 and not self.game_over:
      self.gravity = -8
      
    if self.flying:
      self.gravity += 1

      if self.gravity > 8:
        self.gravity = 8

      if self.rect.bottom < 768:
        self.rect.centery += int(self.gravity)

      self.counter += 1
      self.index = (self.index + 1) % len(self.images) if self.counter % 5 == 0 else self.index
      self.image = self.images[self.index]
      self.image = pg.transform.rotate(self.image, self.gravity * -2)

  def draw(self, win):
    win.blit(self.image, self.rect)
