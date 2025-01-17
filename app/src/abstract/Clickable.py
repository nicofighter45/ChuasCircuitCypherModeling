from abc import  abstractmethod

import pygame
import pygame as pg

from app.src.constants import get_font


class Clickable(pg.Rect):

    def __init__(self, color, position, size):
        self.color = color
        super().__init__(position[0], position[1], size[0], size[1])

    def _is_clicked(self, event):
        return event.type == pg.MOUSEBUTTONDOWN and self.collidepoint(event.pos)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)

    @abstractmethod
    def check_clicked(self, event):
        pass


class Button(Clickable):

    def __init__(self, text, color, position, size, function=None):
        self.__action = function
        self.__text = text
        super().__init__(color, position, size)

    def draw(self, screen):
        super().draw(screen)
        text = get_font().render(self.__text, True, pg.Color("black"))
        screen.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y + self.height // 2 - text.get_height() // 2))

    def check_clicked(self, event):
        if self._is_clicked(event):
            if self.__action is not None:
                self.__action()
            return True
        return False
