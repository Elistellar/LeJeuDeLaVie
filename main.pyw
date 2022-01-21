import threading
import time

import pygame


class Game:
    """Le Jeu de la Vie

    A simple simulation game.
    You can place cells by clicking,
    restart pressing "r",
    recenter the view pressing "c"
    compute a turn pressing "space",
    compute 2 turns per second pressing "2",
    compute 5 turns per second pressing "3",
    compute 10 turns per second pressing "4",
    and stop auto compute pressing "1"
    """
    
    AUTO_COMPUTE_KEYS = {
        pygame.K_1: 0,
        pygame.K_2: 2,
        pygame.K_3: 5,
        pygame.K_4: 10,
    }
    
    MIN_WINDOW_SIZE = 1280, 720
    
    DEFAULT_CELL_SIZE = 24
    MAX_CELL_SIZE = 75
    
    BUTTON_SIZE = 32
    
    BACKGROUND_COLOR = (255, 255, 255)
    CELL_COLOR = (40, 40, 40)
    BUTTON_COLOR = (230, 230, 230)
    PLAY_BUTTON_COLOR = (0, 220, 30)
    
    def __init__(self) -> None:
        pygame.display.init()
        self.window = pygame.display.set_mode(self.MIN_WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption('Le Jeu de la Vie')
        icon = pygame.image.load('icon.ico')
        pygame.display.set_icon(icon)
        
        self.window_size = self.MIN_WINDOW_SIZE
        
        self.clock = pygame.time.Clock()
        
        self.auto_compute_mode = 0
        self.auto_compute_thread = None

        self.cell_size = self.DEFAULT_CELL_SIZE
        self.cells = [
            (0, 0),
        ]
        
        self.tlx_offset = 0
        self.tly_offset = 0
        self.tlx = (self.window.get_width() - self.cell_size) // 2
        self.tly = (self.window.get_height() - self.cell_size) // 2

        # Buttons
        self.button_pos = None
        
        self.running = True
        self.simulation_started = False
        
    def run(self):
        while self.running:
            self.mainloop()
            self.clock.tick(60)
        pygame.display.quit()
        
    def mainloop(self):
    
        for event in pygame.event.get():
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.compute_turn()
                    
                elif event.key in self.AUTO_COMPUTE_KEYS:
                    
                    self.auto_compute_mode = 0
                    if self.auto_compute_thread:
                        self.auto_compute_thread.join()
                    if self.AUTO_COMPUTE_KEYS[event.key] != 0:
                        self.auto_compute_mode = self.AUTO_COMPUTE_KEYS[event.key]
                        self.auto_compute_thread = threading.Thread(
                            name   = 'AutoCompute',
                            target = self.auto_compute_turns
                        )
                        self.auto_compute_thread.start()
                    
                elif event.key == pygame.K_c:
                    self.tlx_offset = 0
                    self.tly_offset = 0
                    
                elif event.key == pygame.K_r:
                    self.cells = [(0, 0)]
                    self.tlx_offset = 0
                    self.tly_offset = 0
                    
                elif event.key == pygame.K_r:
                    self.cells = [(0, 0)]
                    self.tlx_offset = 0
                    self.tly_offset = 0
            
            # Move grid            
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]: # left button held
                    if abs(event.rel[0]) + abs(event.rel[1]) > 2:
                        self.tlx_offset += event.rel[0]
                        self.tly_offset += event.rel[1]
            
            # Zoom
            elif event.type == pygame.MOUSEWHEEL:
                self.cell_size += event.y
                if self.cell_size > self.MAX_CELL_SIZE:
                    self.cell_size = self.MAX_CELL_SIZE
                elif self.cell_size < 1:
                    self.cell_size = 1
                    
                self.tlx = (self.window.get_width() - self.cell_size) // 2
                self.tly = (self.window.get_height() - self.cell_size) // 2
                
            # Place cells
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left button
                self.button_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # left button
                if not self.simulation_started:
                    if event.pos == self.button_pos:                          
                        x = (event.pos[0] - self.tlx - self.tlx_offset) // self.cell_size
                        y = (event.pos[1] - self.tly - self.tly_offset) // self.cell_size
                        
                        if (x, y) in self.cells:
                            self.cells.remove((x, y))
                        else:
                            self.cells.append((x, y))
            
            # Window resize
            elif event.type == pygame.VIDEORESIZE:
                self.window_size = event.size
                if event.size[0] < self.MIN_WINDOW_SIZE[0] \
                or event.size[1] < self.MIN_WINDOW_SIZE[1]:
                    self.screen = pygame.display.set_mode(self.MIN_WINDOW_SIZE, pygame.RESIZABLE)
                    self.window_size = self.MIN_WINDOW_SIZE
                    
                self.tlx = (self.window.get_width() - self.cell_size) // 2
                self.tly = (self.window.get_height() - self.cell_size) // 2
            
            # Quit
            elif event.type == pygame.QUIT:
                self.auto_compute_mode = 0
                self.running = False
                
        self.render()

    def render(self):
        # Background
        pygame.draw.rect(
            self.window,
            self.BACKGROUND_COLOR,
            (0, 0, *self.window_size)
        )
        
        # Cells
        for (x, y) in self.cells:
            pygame.draw.rect(
                self.window,
                self.CELL_COLOR,
                (self.tlx + self.tlx_offset + x * self.cell_size, self.tly + self.tly_offset + y * self.cell_size, self.cell_size, self.cell_size)
            )
                        
        pygame.display.flip()
        
    def compute_turn(self):
        births, deaths = [], []
        
        for cell in self.cells:
            epa = self.get_empty_places_around(cell)
            
            n = len(epa)
            if n < 5 or n > 6:
                deaths.append(cell)
      
            for empty_cell in epa:
                if len(self.get_empty_places_around(empty_cell)) == 5:
                    if empty_cell not in births:
                        births.append(empty_cell)
        
        for cell in deaths:
            self.cells.remove(cell)
                        
        for cell in births:
            self.cells.append(cell)
            
    def get_empty_places_around(self, cell):
        epa = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0, 0):
                    if (c := (cell[0] + x, cell[1] + y)) not in self.cells:
                        epa.append(c)
        return epa
        
    def auto_compute_turns(self):
        while (freq := self.auto_compute_mode):
            self.compute_turn()
            time.sleep(1 / freq)
        
if __name__ == '__main__':
    g = Game()
    g.run()
