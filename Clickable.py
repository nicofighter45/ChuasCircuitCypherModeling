from abc import  abstractmethod
import pygame as pg


class Clickable(pg.Rect):

    def check_clicked(self, event):
        if self.__is_clicked(event):
            self.__on_click()
            return True
        return False

    def __is_clicked(self, event):
        return event.type == pg.MOUSEBUTTONDOWN and self.collidepoint(event.pos)

    @abstractmethod
    def __on_click(self):
        raise Exception("On clik isn't implemented")


class Button(Clickable):
    def __init__(self):
        pass
