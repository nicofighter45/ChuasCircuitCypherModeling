import threading

import numpy as np
import pygame.draw
import scipy
import matplotlib.pyplot as plt
import matplotlib

from app.src.abstract.Clickable import Button
from app.src.classical_chuascircuit import launch_chua_circuit
from app.src.constants import *
from app.src.cypher.manager import Manager


class App:
    """Generate the interface between the simulations and the user"""


    # init, create buttons and initialize variables
    def __init__(self, title):


        self.__title = title

        # init pygame
        matplotlib.use("Agg")
        pg.init()
        self.__screen = pg.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
        pg.display.set_caption(self.__title)
        icon = pg.image.load('app/ressources/icon.jpg')
        pg.display.set_icon(icon)

        # variables for dynamic windows
        self.__text = ""
        self.__managers = []
        self.__frequencies = [[], [], []]
        self.__graphs = [0, 0]

        # state variables
        self.__in_simulation = False
        self.__should_actualize = True
        self.__threads = []
        self.__multithreading = False

        # buttons
        self.__clickables = [
            Button("Render sinusoidal wave", pg.Color("#3F4FE6"), (750, 70), (300, 50), self.__launch_sinusoid_simulation),
            Button("Render square wave", pg.Color("#2CC7EE"), (750, 140), (300, 50),self.__launch_square_simulation),
            Button("Render sawtooth wave", pg.Color("#24E598"), (750, 210), (300, 50), self.__launch_sawtooth_simulation),
            Button("Reload", pg.Color("#FF4C28"), (950, 300), (100, 50), self.__reload),

            self.__create_menu_button("Results", 0, 0, selected=True),
            self.__create_menu_button("Elec 1", 60, 1),
            self.__create_menu_button("Elec 2", 120, 2),
            self.__create_menu_button("1st char", 580, i=0, selected=True),
            self.__create_menu_button("2nd char", 520, i=1),
            self.__create_menu_button("3rd char", 460, i=2),
            self.__create_menu_button("4th char", 400, i=3),
            self.__create_menu_button("5th char", 340, i=4),
            self.__create_menu_button("6th char", 280, i=5),
            Button("Classic Chua's Scheme", pg.Color("#FFC232"), (750, 630), (300, 60), self.__launch_chua_circuit_simulation),
        ]

        # launch pygame
        self.__run()


    def __run(self):
        """maintain the loop to 60 fps and launch events check"""
        clock = pg.time.Clock()
        while self.__should_actualize:
            for event in pg.event.get():
                self.__check_event(event)
            self.__loop()
            pg.display.update()
            clock.tick(60)


    def __check_event(self, event):
        """Checking events such as keyboard input and button press"""
        if event.type == pg.QUIT:
            self.__should_actualize = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.__should_actualize = False
            exit()
        elif event.type == pg.KEYDOWN and not self.__in_simulation:
            if event.key == pg.K_BACKSPACE:
                self.__text = self.__text[:-1]
            elif event.key:
                if len(self.__text) < 6 and char_to_f(event.unicode) != 0:
                    self.__text += event.unicode
        else:
            for clickable in self.__clickables:
                if clickable.check_clicked(event):
                    break


    def __loop(self):
        """Is called 60 times per second"""
        self.__screen.fill(BACKGROUND_COLOR)
        for clickable in self.__clickables:
            clickable.draw(self.__screen)
        if self.__in_simulation:
            if len(self.__threads) != 0:
                self.__message("Running the Simulation, please wait ...", y=50)
                self.__message(f"{len(self.__text) - len(self.__threads)}/{len(self.__text)} done", y=90)
                self.__message(f"Every char is in it's separate thread,", y=130)
                self.__message(f"so the first 0/{len(self.__text)} can take time", y=170)
                self.__message(f"You can't leave while the computations are made", y=560)
                self.__message("If you press escape it will leave at", y=600)
                self.__message("the end of the computations", y=640)
            elif self.__multithreading:
                self.__multithreading = False
                self.__after_finished_simulation()
            else:
                try:
                    self.__render_simulation()
                except FileNotFoundError:
                    self.__message("Failed to load simulation, try again ...")
        else:
            if self.__text == "":
                # help text message
                text_box = get_font().render("Type up to 6 characters", True, pg.Color("darkgrey"))
                self.__message("Type with your keyboard to enter characters")
                self.__message("Press escape to leave", y=640)
                self.__message("Press one of the Render button", 690, 10, 20)
                self.__message("to run the simulation", 800, 35, 20)
                self.__message("Press to reload the simulation", 690, 360, 20)
                self.__message("Press to see classical chua's", 690, 560, 20)
                self.__message("circuit graphs", 870, 590, 20)
            else:
                text_box = get_font().render(self.__text, True, pg.Color("black"))
            self.__screen.blit(text_box, (100, 50))
            pygame.draw.rect(self.__screen, pg.Color("black"), pg.Rect(80, 30, 350, 70), 2)


    def __render_simulation(self):
        """Render the simulation results"""
        self.__screen.blit(pg.image.load('app/ressources/export/graph' + str(self.__graphs[0]) + str(self.__graphs[1]) + '.png'), (40, 70))
        pg.draw.rect(self.__screen, pg.Color("black"), pg.Rect(30, 30, 640, 530), 2)
        string_p, string_vr = "", ""
        for manager in self.__managers:
            self.__frequencies[1].append(manager.fp)
            self.__frequencies[2].append(manager.fr)
            string_p += f_to_char(manager.fp)
            string_vr += f_to_char(manager.fr)
        self.__message(f"Original characters: {self.__text}", y=580)
        self.__message(f"Decrypted characters: {string_p}", y=620)
        self.__message(f"Decrypted from vr: {string_vr}", y=660)
        start_x = 700 + 40 * (6 - len(self.__frequencies[0]))
        self.__message("f in Hz for each char", 750, 540)
        draw_table(self.__screen, [[ch for ch in self.__text]], start_x, 570, 60, 30)
        draw_table(self.__screen, [["Char"], ["p"], ["d"], ["Vr"]], start_x - 100, 570, 100, 30)
        draw_table(self.__screen, self.__frequencies, start_x, 600, 60, 30)

    def __launch_simulations(self, function):
        """Launch a new simulation"""
        if self.__text == "":
            return
        if self.__in_simulation and len(self.__threads) != 0:
            return
        if self.__in_simulation:
            self.__re_simulate()
        self.__in_simulation = True
        i = 0
        for char in self.__text:
            thread = (threading.Thread(target=lambda: self.__launch_simulation(char, function, i)))
            self.__threads.append(thread)
            thread.start()
            i+=1
        self.__multithreading = True


    def __launch_simulation(self, char, function, i):
        self.__frequencies[0].append(char_to_f(char))
        manager = Manager(self.__frequencies[0][-1], function)
        self.__managers.append(manager)
        manager.export_graphs(i)
        manager.curve_fit()
        self.__threads.remove(threading.current_thread())


    def __after_finished_simulation(self):
        for thread in self.__threads:
            thread.join()
        self.__threads = []
        for i in range(len(self.__text)):
            self.__clickables[7 + i].should_render = True
        for clickable in self.__clickables[4:7]:
            clickable.should_render = True
        self.__clickables[-1].should_render = False


    def __reload(self):
        """Reload the workspace"""
        if len(self.__threads) != 0:
            return
        self.__in_simulation = False
        self.__multithreading = False
        self.__threads = []
        self.__text = ""
        self.__clickables[-1].should_render = True
        self.__re_simulate()

    def __re_simulate(self):
        """Reset the simulation"""
        plt.close('all')
        self.__managers = []
        self.__frequencies = [[], [], []]
        self.__graphs = [0, 0]
        self.selected_button_menu_index = [0, 0]
        for clickable in self.__clickables[4:13]:
            clickable.should_render = False

    def __set_graphs(self, n=None, i=None):
        """Set the graphs to display"""
        if i is not None:
            self.__clickables[7 + self.__graphs[1]].selected = False
            self.__graphs[1] = i
            self.__clickables[7 + self.__graphs[1]].selected = True
        if n is not None:
            self.__clickables[4 + self.__graphs[0]].selected = False
            self.__graphs[0] = n
            self.__clickables[4 + self.__graphs[0]].selected = True

    def __launch_sinusoid_simulation(self):
        """Launch a sinusoidal simulation"""
        self.__launch_simulations(lambda t, f: 0.2 * np.sin(f*t))

    def __launch_square_simulation(self):
        """Launch a square wave simulation"""
        self.__launch_simulations(lambda t, f: 0.2 * np.sign(np.sin(f*t)))

    def __launch_sawtooth_simulation(self):
        """Launch a sawtooth wave simulation"""
        self.__launch_simulations(lambda t, f: 0.2 * scipy.signal.sawtooth((f/2)*t))

    def __launch_chua_circuit_simulation(self):
        """Launch chua circuit simulation"""
        self.__should_actualize = False
        pg.display.quit()
        matplotlib.use("TkAgg")
        launch_chua_circuit()
        self.__init__(self.__title)

    def __message(self, text, x=80, y=150, size=22):
        """Display a message on the screen"""
        self.__screen.blit(get_font(size).render(text, True, pg.Color("black")), (x, y))

    def __create_menu_button(self, name, pos, n=None, i=None, selected=False):
        """Create a button for the menu"""
        return Button(name, pg.Color("#949494"), (30+pos, 30), (60, 30), lambda: self.__set_graphs(n, i),
                      False, text_size=10, black_box=True, selected=selected, selected_color=pg.Color("#545454"))



def draw_table(screen, input_text_table, table_x, table_y, cell_width, cell_height):
    """Draw a table on the screen"""
    for row in range(len(input_text_table)):
        for col in range(len(input_text_table[0])):
            x = table_x + col * cell_width
            y = table_y + row * cell_height
            draw_cell(screen, str(input_text_table[row][col]), x, y, cell_width, cell_height)


def draw_cell(screen, text, x, y, cell_width, cell_height):
    """Draw a cell"""
    pg.draw.rect(screen, pg.Color("grey"), (x, y, cell_width, cell_height), 1)
    text = get_font().render(text, True, pg.Color("black"))
    text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
    screen.blit(text, text_rect)


def char_to_f(char):
    """Convert a character to a frequency"""
    if len(char) == 0:
        return 0
    n = ord(char)
    if not 32 <= n <= 127:
        return 0
    return 2500 + (ord(char)-32) * 10

def f_to_char(f):
    """Convert a frequency to a character"""
    if not 2500 <= f <= 3270:
        return '•'
    return chr(int((f-2500)/10)+32)
