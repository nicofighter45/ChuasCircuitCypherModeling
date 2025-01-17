import numpy as np
import pygame.draw
import threading

from app.src.abstract.Clickable import Button
from app.src.constants import *
from app.src.cypher.manager import Manager


class App:
    def __init__(self, title):
        pg.init()
        self.__screen = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption(title)
        icon = pg.image.load('app/ressources/icon.jpg')
        pg.display.set_icon(icon)
        self.text = ""
        self.managers = []
        self.th_function = None
        self.frequencies = [[], [], []]

        self.__in_calculation = False
        self.__in_simulation = False
        self.__in_calculation = False
        self.__should_actualize = True
        self.clickables = [
            Button("Render sinusoidal wave", pg.Color("#3F4FE6"), (750, 70), (300, 50), self.__launch_sinusoid_simulation),
            Button("Render square wave", pg.Color("#2CC7EE"), (750, 140), (300, 50),self.__launch_square_simulation),
            Button("Render sawtooth wave", pg.Color("#24E598"), (750, 210), (300, 50), self.__launch_sawtooth_simulation),
            Button("Reload", pg.Color("#FF4C28"), (950, 300), (100, 50), self.__reload),
        ]

        self.__run()

    def __launch_sinusoid_simulation(self):
        th = (threading.Thread(target=self.__launch_simulation(lambda t, A, B, C: 0.2 * np.sin(A * t - B) + C)))
        th.start()

    def __launch_square_simulation(self):
        th = threading.Thread(target=self.__launch_simulation(lambda t, A, B, C: 0.2 * np.sign(np.sin(A * t - B) + C)))
        th.start()

    def __launch_sawtooth_simulation(self):
        th = threading.Thread(target=self.__launch_simulation(lambda t, A, B, C: 0.2 * np.sign(np.sin(A * t - B) + C)))
        th.start()


    def __run(self):
        clock = pg.time.Clock()
        while self.__should_actualize:
            for event in pg.event.get():
                self.__check_event(event)
            self.__loop()
            pg.display.update()
            clock.tick(60)

    def __reload(self):
        self.__in_simulation = False
        self.__in_calculation = False
        self.__in_calculation = False
        self.managers = []
        self.frequencies = [[], [], []]
        self.text = ""

    def __check_event(self, event):
        if event.type == pg.QUIT:
            self.__should_actualize = False
        elif event.type == pg.KEYDOWN and not self.__in_simulation:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pg.K_RETURN:
                threading.Thread(target=self.__launch_simulation).start()
            elif event.key:
                if len(self.text) < 6 and char_to_f(event.unicode) != 0:
                    self.text += event.unicode
        else:
            for clickable in self.clickables:
                if clickable.check_clicked(event):
                    break

    def __loop(self):
        self.__screen.fill(BACKGROUND_COLOR)
        if self.text == "":
            text_box = get_font().render("Type up to 6 characters", True, pg.Color("darkgrey"))
        else:
            text_box = get_font().render(self.text, True, pg.Color("black"))
        self.__screen.blit(text_box, (100, 50))
        pygame.draw.rect(self.__screen, pg.Color("black"), pg.Rect(80, 30, 350, 70), 2)
        for clickable in self.clickables:
            clickable.draw(self.__screen)
        if self.__in_simulation:
            if self.__in_calculation:
                self.__message("Running the Simulation, please wait ...")
            else:
                try:
                    self.__screen.blit(pg.image.load('app/ressources/graph.png'), (50, 100))
                    string_p, string_vr = "", ""
                    for manager in self.managers:
                        self.frequencies[1].append(manager.fp)
                        self.frequencies[2].append(manager.fr)
                        string_p += f_to_char(manager.fp)
                        string_vr += f_to_char(manager.fr)
                    self.__message(f"Decrypted characters: {string_p}", y=600)
                    self.__message(f"Decrypted from vr: {string_vr}", y=650)
                    start_x = 700 + 40 * (6-len(self.frequencies[0]))
                    self.__message("f in Hz for each char", 750, 540)
                    draw_table(self.__screen, [[ch for ch in self.text]], start_x, 570, 60, 30)
                    draw_table(self.__screen, [["Char"], ["p"], ["d"], ["Vr"]], start_x-100, 570, 100, 30)
                    draw_table(self.__screen, self.frequencies, start_x, 600, 60, 30)
                except FileNotFoundError:
                    self.__message("Failed to load simulation, try again ...")
        else:
            self.__message("Type with your keyboard to enter characters")
            self.__message("Press one of the Render button", 690, 10, 20)
            self.__message("to run the simulation", 800, 35, 20)
            self.__message("Press to reload the simulation", 690, 360, 20)

    def __message(self, text, x=80, y=150, size=22):
        self.__screen.blit(get_font(size).render(text, True, pg.Color("black")), (x, y))

    def __launch_simulation(self, function):
        if self.__in_simulation or self.text == "":
            return
        self.__in_simulation = True
        self.__in_calculation = True
        self.__loop()
        pg.display.update()
        for char in self.text:
            self.frequencies[0].append(char_to_f(char))
            self.managers.append(Manager(self.frequencies[0][-1], function))
        self.managers[-1].export_graphs()
        for manager in self.managers:
            manager.curve_fit()
        self.__in_calculation = False

def draw_table(screen, input_text_table, table_x, table_y, cell_width, cell_height):
    for row in range(len(input_text_table)):
        for col in range(len(input_text_table[0])):
            x = table_x + col * cell_width
            y = table_y + row * cell_height
            draw_cell(screen, str(input_text_table[row][col]), x, y, cell_width, cell_height)


def draw_cell(screen, text, x, y, cell_width, cell_height):
    pg.draw.rect(screen, pg.Color("grey"), (x, y, cell_width, cell_height), 1)
    text = get_font().render(text, True, pg.Color("black"))
    text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
    screen.blit(text, text_rect)


def char_to_f(char):
    if len(char) == 0:
        return 0
    n = ord(char)
    if not 32 <= n <= 127:
        return 0
    return 2500 + (ord(char)-32) * 10

def f_to_char(f):
    if not 2500 <= f <= 3270:
        return '•'
    return chr(int((f-2500)/10)+32)
