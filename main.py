import pygame as pg
from pygame.locals import *
from constants import *
from random import randint
from sprites.bird import Bird
from sprites.pipe import Pipe
from typing import Tuple

class FlappyBirdGame:
  def __init__(self) -> None:
    pg.init()
    self.win: pg.Surface = pg.display.set_mode((screen_width, screen_height))
    self.fps: pg.time.Clock = pg.time.Clock()
    pg.display.set_caption("Flappy bird")
    pg.display.set_icon(pg.image.load('assets/bird1.png'))

    self.bg: pg.Surface = pg.image.load('assets/bg.png')
    self.bg = pg.transform.scale(self.bg, (900, self.bg.get_height()))

    self.flappy: Bird = Bird(100, screen_height // 2)
    self.bird_group: pg.sprite.Group = pg.sprite.Group()
    self.bird_group.add(self.flappy)

    self.pipe_gap: int = 200
    self.pipe_frequence: int = 1700  # 1.5 seconds
    self.last_pipe: int = pg.time.get_ticks()
    self.pipe_group: pg.sprite.Group = pg.sprite.Group()

    self.ground: pg.Surface = pg.image.load('assets/ground.png')
    self.ground_scroll: int = 0
    self.scroll_speed: int = 4

    self.score: int = 0
    self.font: pg.font.Font = pg.font.SysFont('Arial', 32)

    self.game_over: bool = False
    self.flying: bool = False

    self.restart_btn: pg.Surface = pg.image.load('assets/restart.png')

  def run(self) -> None:
    while not self.game_over or self.flying:
      self.fps.tick(60)
      self.handle_events()
      self.update_game_state()
      self.draw_elements()
      pg.display.update()
    pg.quit()
    exit(0)

  def handle_events(self) -> None:
    for event in pg.event.get():
      if event.type == QUIT:
        self.game_over = True
        pg.quit()
      if event.type == MOUSEBUTTONDOWN and not self.flying:
        self.flappy.flying = self.flying = True

  def update_game_state(self) -> None:
    if pg.time.get_ticks() - self.last_pipe > self.pipe_frequence:
      pipe_height: int = randint(-100, 100)
      p1: Pipe = Pipe(
        screen_width, 
        (screen_height // 2) - self.pipe_gap // 2 + pipe_height, 
        False
      )
      p2: Pipe = Pipe(
        screen_width, 
        (screen_height // 2) + self.pipe_gap // 2 + pipe_height, 
        True
      )
      self.pipe_group.add(p1)
      self.pipe_group.add(p2)
      self.last_pipe = pg.time.get_ticks()

    if self.flappy.rect.bottom >= 768:
      self.flappy.game_over = self.game_over = True

    if not self.game_over:
      self.pipe_group.update()
      self.ground_scroll -= self.scroll_speed
      if abs(self.ground_scroll) > 30:
        self.ground_scroll = 0

      if pg.sprite.groupcollide(self.bird_group, self.pipe_group, False, False):
        self.game_over = self.flappy.game_over = True
        # self.flying = False

      for pipe in self.pipe_group:
        if pipe.rect.right < self.flappy.rect.left and not pipe.passed:
          pipe.passed = True
          self.score += 5
    else:
      mouse_pos: bool = pg.mouse.get_pressed()[0]
      if self.restart_btn.get_rect(
        topleft=(
          screen_width // 2 - self.restart_btn.get_width() // 2, 
          screen_height // 2
        )
      ).collidepoint(pg.mouse.get_pos()) and mouse_pos:
        self.reset_game()

  def draw_elements(self) -> None:
    self.win.blit(self.bg, (0, 0))
    self.bird_group.draw(self.win)
    self.bird_group.update()

    if self.flappy.flying:
      self.pipe_group.draw(self.win)

      if self.game_over:
        msg: pg.Surface = pg.font.SysFont('Arial', 64).render(
          'Game Over', True, (255, 255, 255)
        )
        self.win.blit(
          msg,
          (screen_width // 2 - msg.get_width() // 2, 20)
        )
        self.win.blit(
          self.restart_btn,
          (screen_width // 2 - self.restart_btn.get_width() // 2, screen_height // 2)
        )

      score_text: pg.Surface = self.font.render(
        f'Score: {self.score}', True, (255, 255, 255)
      )
      self.win.blit(score_text, (10, 10))

    # Draw the ground
    self.win.blit(
      self.ground, 
      (0 if not self.flying else self.ground_scroll, self.bg.get_rect().bottomleft[1])
    )

  def reset_game(self) -> None:
    self.flappy = Bird(100, screen_height // 2)
    self.bird_group = pg.sprite.Group()
    self.bird_group.add(self.flappy)

    self.pipe_group = pg.sprite.Group()

    self.ground_scroll = 0

    self.score = 0

    self.game_over = False
    self.flying = False

if __name__ == "__main__":
  game = FlappyBirdGame()
  game.run()
