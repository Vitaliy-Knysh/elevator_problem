import pygame
from os.path import abspath


class View:
    BACKGROUND = (108, 216, 230)
    WHITE = (255, 255, 255)
    GRAY = (215, 215, 215)
    BLACK = (0, 0, 0)
    IMG_ELEVATOR = pygame.image.load(abspath('../app/resources/elevator.png'))
    IMG_ELEVATOR_HEIGHT = IMG_ELEVATOR.get_height()
    IMG_ELEVATOR_OPENED = pygame.image.load(abspath('../app/resources/elevator_opened.png'))
    IMG_ARROW = pygame.image.load(abspath('../app/resources/arrow.png'))
    WIDTH = 600

    def __init__(self, floor_count: int):
        self.floor = 1
        self.doors_opened = False
        self.floor_count = floor_count if floor_count > 0 else 1
        window_size = (self.WIDTH, floor_count * self.IMG_ELEVATOR_HEIGHT)
        self.floor_rects, self.floor_num_rects, self.button_rects = self._get_rects()
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Симулятор лифта')
        self.clock = pygame.time.Clock()

    def display(self):
        while True:
            self._draw_background()
            self._draw_buttons()
            self._draw_current_floor()
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and (
                        button_id := self._check_button_collisions(e)):
                    self.floor = button_id
                    self.doors_opened = True
                    self._draw_button_pressed(button_id)

                if e.type == pygame.QUIT:
                    exit()  # todo жестко гасим весь python. Насколько обоснованно?
                pygame.display.update()
            self.clock.tick(30)

    def _draw_background(self):
        self.screen.fill(color=self.BACKGROUND)
        font = pygame.font.SysFont(name=None, size=65, bold=True)
        for r in self.floor_rects:
            self.screen.blit(self.IMG_ELEVATOR, r)
        if self.doors_opened:
            self.screen.blit(self.IMG_ELEVATOR_OPENED, self.floor_rects[self.floor - 1])
        for count, r in enumerate(self.floor_num_rects):
            floor_num = font.render(str(count + 1), True, self.GRAY)
            self.screen.blit(floor_num, r)

    def _get_rects(self) -> tuple[list[pygame.Rect], list[pygame.Rect], list[pygame.Rect]]:
        """
        Возвращает объекты-прямоугольники для этажей, номеров этажей и кнопок.
        Для того, нумерация этажей была снизу вверх, в конце список разворачивается.
        """
        left_corner_x_pos = self.WIDTH // 2 - self.IMG_ELEVATOR_HEIGHT // 2
        left_corner_y_pos = self.IMG_ELEVATOR_HEIGHT // 2
        floor_rects = [pygame.Rect(left_corner_x_pos, i * self.IMG_ELEVATOR_HEIGHT, 100, 30)
                       for i in range(self.floor_count)
                       ][::-1]
        floor_num_rects = [pygame.Rect(left_corner_x_pos, i * self.IMG_ELEVATOR_HEIGHT + 70, 100, 30)
                           for i in range(self.floor_count)
                           ][::-1]
        button_rects = [pygame.Rect(left_corner_x_pos + self.IMG_ELEVATOR_HEIGHT,
                                    i * self.IMG_ELEVATOR_HEIGHT + left_corner_y_pos, 100, 30)
                        for i in range(self.floor_count)
                        ][::-1]
        return floor_rects, floor_num_rects, button_rects

    def _draw_buttons(self):
        font = pygame.font.SysFont(name=None, size=18)
        text = font.render("Вызвать лифт", True, self.BLACK)
        for r in self.button_rects:
            pygame.draw.rect(self.screen, self.WHITE, rect=r, border_radius=10)
            self.screen.blit(text, dest=text.get_rect(center=r.center))

    def _draw_button_pressed(self, button_id: int):
        font = pygame.font.SysFont(name=None, size=18)
        text = font.render("Вызвать лифт", True, self.BLACK)
        rect = self.button_rects[button_id - 1]
        pygame.draw.rect(self.screen, self.GRAY, rect=rect, border_radius=10)
        self.screen.blit(text, dest=text.get_rect(center=rect.center))

    def _check_button_collisions(self, event: pygame.event) -> int:
        for count, r in enumerate(self.button_rects):
            if r.collidepoint(event.pos):
                return count + 1
        return 0

    def _draw_current_floor(self):
        left_corner_x_pos = self.WIDTH // 2 - 5
        left_corner_y_pos = 28
        font = pygame.font.SysFont(name=None, size=20, bold=True)
        text = font.render(str(self.floor), True, self.WHITE)
        for i in range(self.floor_count):
            self.screen.blit(text, dest=(left_corner_x_pos, i * self.IMG_ELEVATOR_HEIGHT + left_corner_y_pos))

    def _draw_control_panel(self):
        pass