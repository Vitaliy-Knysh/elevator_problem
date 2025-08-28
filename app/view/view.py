from datetime import datetime, timedelta
from os.path import abspath

import pygame

from app.dto import DisplayButton, ElevatorState
from app.model.elevator import Elevator


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
    BTN_WIDTH = 100
    BTN_HEIGHT = 30

    def __init__(self, floor_count: int):
        self.state = ElevatorState(floor=0, move='STOP')
        self.doors_opened = False
        self.floor_count = floor_count if floor_count > 0 else 1
        window_size = (self.WIDTH, floor_count * self.IMG_ELEVATOR_HEIGHT)
        self.floor_rects, self.floor_num_rects = self._get_floor_rects()
        self.buttons = self._create_buttons()
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Симулятор лифта')
        self.clock = pygame.time.Clock()

    def run(self, elevator: Elevator):
        move_ts = datetime.now()
        while True:
            self._draw_scene()
            self._perform_checks()
            time_diff = datetime.now() - move_ts
            self.state = elevator.logic(pressed_buttons=[btn for btn in self.buttons if btn.pressed], time_diff=time_diff)  # todo переименовать по-человечески
            if self.state.move == 'STOP':
                self._unpress_all_buttons()
            pygame.display.update()
            self.clock.tick(30)

    def _perform_checks(self):
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self._check_button_collisions(e)

            if e.type == pygame.QUIT:
                exit()  # todo жестко гасим весь python. годится?

    def _draw_background(self):
        self.screen.fill(color=self.BACKGROUND)
        font = pygame.font.SysFont(name=None, size=65, bold=True)
        for r in self.floor_rects:
            self.screen.blit(self.IMG_ELEVATOR, r)
        if self.state.move == 'STOP':
            self.screen.blit(self.IMG_ELEVATOR_OPENED, self.floor_rects[self.state.floor])
        for count, r in enumerate(self.floor_num_rects):
            floor_num = font.render(str(count + 1), True, self.GRAY)
            self.screen.blit(floor_num, r)

    def _draw_scene(self):
        self._draw_background()
        self._draw_control_panel()
        self._draw_buttons()
        self._draw_current_floor()

    def _get_floor_rects(self) -> tuple[list[pygame.Rect], list[pygame.Rect]]:
        """
        Возвращает объекты-прямоугольники для этажей b, номеров этажей.
        Для того, нумерация этажей была снизу вверх, в конце список разворачивается.
        """
        left_corner_x_pos = 0
        floor_rects = [pygame.Rect(left_corner_x_pos, i * self.IMG_ELEVATOR_HEIGHT, 100, 30)
                       for i in range(self.floor_count)
                       ][::-1]
        floor_num_rects = [pygame.Rect(left_corner_x_pos + 5, i * self.IMG_ELEVATOR_HEIGHT + 70, 100, 30)
                           for i in range(self.floor_count)
                           ][::-1]

        return floor_rects, floor_num_rects

    def _create_buttons(self) -> list[DisplayButton]:
        left_corner_x_pos = 0
        left_corner_y_pos = self.IMG_ELEVATOR_HEIGHT // 2
        buttons = []
        for i in range(self.floor_count, -1, -1):
            buttons.append(
                DisplayButton(
                    rect=pygame.Rect(left_corner_x_pos + self.IMG_ELEVATOR_HEIGHT,
                                     i * self.IMG_ELEVATOR_HEIGHT + left_corner_y_pos, self.BTN_WIDTH, self.BTN_HEIGHT),
                    text='Вызвать лифт',
                    btn_id=f'floor_btn_{i}',
                    btn_type='floor',
                    floor=self.floor_count - i - 1
                )
            )
        left_corner_x_pos = self.WIDTH - 200
        left_corner_y_pos = 70
        for i in range(self.floor_count):
            buttons.append(
                DisplayButton(
                    rect=pygame.Rect(left_corner_x_pos,
                                     i * 40 + left_corner_y_pos, self.BTN_WIDTH, self.BTN_HEIGHT),
                    text=f'{i + 1} Этаж',
                    btn_id=f'control_btn_{i}',
                    btn_type='control',
                    floor=i
                )
            )
        return buttons

    def _draw_buttons(self):
        font = pygame.font.SysFont(name=None, size=18)
        for btn in self.buttons:
            bg_color = self.GRAY if btn.pressed else self.WHITE
            pygame.draw.rect(self.screen, bg_color, rect=btn.rect, border_radius=10)
            text = font.render(btn.text, True, self.BLACK)
            self.screen.blit(text, dest=text.get_rect(center=btn.rect.center))

    def _check_button_collisions(self, event: pygame.event):
        for btn in self.buttons:
            if btn.rect.collidepoint(event.pos):
                btn.pressed = True

    def _draw_current_floor(self):
        left_corner_x_pos = self.IMG_ELEVATOR_HEIGHT // 2 - 5
        left_corner_y_pos = 28
        font = pygame.font.SysFont(name=None, size=20, bold=True)
        text = font.render(str(self.state.floor + 1), True, self.WHITE)
        for i in range(self.floor_count):
            self.screen.blit(text, dest=(left_corner_x_pos, i * self.IMG_ELEVATOR_HEIGHT + left_corner_y_pos))

    def _draw_control_panel(self):
        left_corner_x_pos = self.WIDTH - 250
        left_corner_y_pos = 0
        bg_height = self.BTN_HEIGHT * self.floor_count + 130
        background = pygame.Rect(left_corner_x_pos - 20, left_corner_y_pos - 10, 250, bg_height)
        font = pygame.font.SysFont(name=None, size=40, bold=True)
        text1 = font.render('Управляющая', True, self.WHITE)
        text2 = font.render('панель', True, self.WHITE)
        pygame.draw.rect(self.screen, self.GRAY, rect=background, border_radius=10)
        self.screen.blit(text1, dest=(left_corner_x_pos, left_corner_y_pos))
        self.screen.blit(text2, dest=(left_corner_x_pos, left_corner_y_pos + 25))

    def _unpress_all_buttons(self):
        for btn in self.buttons:
            if btn.pressed:
                btn.pressed = False
