import pygame
import datetime
import math

class MickeyClock:
    def __init__(self, screen, center):
        self.screen = screen
        self.center = center
        self.hand_img = pygame.image.load("images/mickey_hand.png").convert_alpha()

    def draw_hand(self, angle, length):
        rotated = pygame.transform.rotate(self.hand_img, -angle)
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect)

    def update(self):
        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute

        
        sec_angle = seconds * 6        
        min_angle = minutes * 6

        
        self.draw_hand(sec_angle, 100)
        self.draw_hand(min_angle, 70)