import pygame
import time
import random
import threading

image_path = 'canvas.jpg'


class Canvas:
    screen_width = 1050
    screen_height = 680

    def __init__(self):
        self.screen = pygame.display.set_mode((Canvas.screen_width, Canvas.screen_height))
        self.bg_img = pygame.image.load(image_path)
        self.ball_color = pygame.Color(255, 0, 0)
        self.old_ball_rect = None

        self.screen.blit(self.bg_img, (0, 0))
        pygame.display.flip()

    @classmethod
    def recalc_coords(cls, coords):
        screen_x = round(cls.screen_width / 100 * float(coords[0]), 0)
        screen_y = round(cls.screen_height / 100 * float(coords[1]), 0)
        return (screen_x,screen_y)

    def move_ball(self, coords):
        screen_coords = Canvas.recalc_coords(coords)
        if self.old_ball_rect:
            self.screen.blit(self.bg_img,self.old_ball_rect.topleft,area=self.old_ball_rect)
            pygame.display.update(self.old_ball_rect)
        new_ball_rect = pygame.draw.circle(self.screen,self.ball_color,screen_coords, 4)
        pygame.display.update(new_ball_rect)
        self.old_ball_rect = new_ball_rect