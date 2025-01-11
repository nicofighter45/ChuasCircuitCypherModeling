import pygame as pg
from constants import *

class App:
    def __init__(self, title):
        pg.init()
        self.__screen = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption(title)
        self.__font = pg.font.Font('app/assets/Geist_Mono/GeistMono.ttf', 14)
        self.__running = True
        self.__run()
        self.__clickables = [] # list d'instance de Clickable

    def __run(self):
        clock = pg.time.Clock()
        while self.__running:
            for event in pg.event.get():
                self.__check_event(event)
            self.__loop()
            pg.display.update()
            clock.tick(60)

    def __check_event(self, event):
        if event.type == pg.QUIT:
            self.__running = False
        else:
            for clickable in self.__clickables:
                if clickable.check_clicked(event):
                    break

    def __loop(self):
        pass