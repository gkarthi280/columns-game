## Goutham Karthi, Student ID: 19652712
import pygame
import gamestate
import random
import sys
import time

_INITIAL_WIDTH = 450
_INITIAL_HEIGHT = 900
_BACKGROUND_COLOR = pygame.Color(0, 0, 0)


class ColumnsGame:
    def __init__(self):
        self._state = gamestate.GameState(
            '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \n      \n      ')
        self._game_over: bool = False
        self._positions: dict = {}
        for i in range(len(self._state.field())):
            for j in range(len(self._state.field()[0])):
                self._positions[(i, j)] = pygame.Rect(75 * j, 75 * i, 75, 75)

        self._gem_colors: dict = {'S': pygame.Color(230, 86, 34),
                                  'T': pygame.Color(242, 190, 46),
                                  'V': pygame.Color(72, 171, 10),
                                  'W': pygame.Color(12, 151, 201),
                                  'X': pygame.Color(112, 79, 184),
                                  'Y': pygame.Color(184, 32, 201),
                                  'Z': pygame.Color(34, 238, 245)}

    def run(self) -> None:
        pygame.init()
        # self._state.display_field()
        try:
            clock = pygame.time.Clock()

            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))

            while not self._game_over:
                clock.tick(1)
                temp: tuple = create_random_faller()
                self._faller: gamestate.Faller = temp[1]
                faller_str: str = temp[0]
                game_end: bool = True
                for i in range(self._state.rows()):
                    if self._state.field()[i][self._faller.column_to_drop()].state() == 'empty':
                        game_end = False
                if game_end:
                    break
                self._state.drop_faller(self._faller, 'F ' + faller_str)
                self._draw_frame()
                time.sleep(3)
                while True:
                    clock.tick(1)
                    self._draw_frame()
                    message: str = self._state.drop_faller(self._faller, '')
                    self._handle_events()
                    self._draw_frame()
                    if message == 'faller has frozen' or message == 'game over':
                        if message == 'game over':
                            self._game_over = True
                        break
            self._draw_game_over()

        finally:
            time.sleep(5)
            pygame.quit()

    def _create_surface(self, size: (int, int)) -> None:
        '''creates the surface with given size'''
        self._surface = pygame.display.set_mode(size)

    def _stop_running(self) -> None:
        '''ends program'''
        sys.exit()

    def _draw_game_over(self) -> None:
        '''draws game over screen and displays it'''
        self._surface.fill(_BACKGROUND_COLOR)
        self._draw_text(pygame.font.SysFont(None, 50), 'GAME OVER')
        pygame.display.flip()

    def _handle_events(self) -> None:
        '''handles all events'''
        for event in pygame.event.get():
            self._handle_event(event)

    def _handle_event(self, event) -> None:
        '''handle individual events for quitting game, left arrow, right arrow, and spacebar'''
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._state.drop_faller(self._faller, 'R')
            if event.key == pygame.K_LEFT:
                self._state.drop_faller(self._faller, '<')
            if event.key == pygame.K_RIGHT:
                self._state.drop_faller(self._faller, '>')
        else:
            pass

    def _draw_frame(self) -> None:
        '''draws the current state of the game and all the contents of the field'''
        self._surface.fill(_BACKGROUND_COLOR)
        for i in range(len(self._state.field())):
            for j in range(len(self._state.field()[0])):
                if self._state.field()[i][j].state() == 'frozen' or self._state.field()[i][j].state() == 'faller':
                    pygame.draw.rect(self._surface, self._gem_colors[self._state.field()[i][j].gem()],
                                     self._positions[(i, j)])
                elif self._state.field()[i][j].state() == 'landed':
                    pygame.draw.rect(self._surface, pygame.Color(255, 255, 255), self._positions[(i, j)])
                elif self._state.field()[i][j] == 'empty':
                    pygame.draw.rect(self._surface, _BACKGROUND_COLOR, self._positions[(i, j)])
        self._draw_grid()
        pygame.display.flip()


    def _draw_text(self, font: pygame.font.SysFont, text: str) -> None:
        text_image = font.render(text, True, pygame.Color(255, 255, 255))
        self._surface.blit(text_image, (50,50))

    def _draw_grid(self) -> None:
        '''draws grid of the field'''
        for i in range(0, _INITIAL_WIDTH + 1, 75):
            pygame.draw.line(self._surface, pygame.Color(255, 255, 255), (i, 0), (i, _INITIAL_HEIGHT), 3)
        for i in range(0, _INITIAL_HEIGHT + 1, 75):
            pygame.draw.line(self._surface, pygame.Color(255, 255, 255), (0, i), (_INITIAL_WIDTH, i), 3)


def create_random_faller() -> tuple:
    '''creates a random faller, and returns s tuple containing the faller string and faller object'''
    random_column: int = random.randint(1, 6)
    gems: list = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
    faller_str: str = str(random_column) + ' ' + gems[random.randint(0, 6)] + ' ' + gems[random.randint(0, 6)] + ' ' + gems[random.randint(0, 6)]
    return (faller_str, gamestate.Faller(faller_str))


if __name__ == '__main__':
    ColumnsGame().run()
