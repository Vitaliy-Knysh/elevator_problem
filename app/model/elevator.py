from datetime import datetime, timedelta

from app.dto import DisplayButton, ElevatorState


class Elevator:
    SPEED = 0.3

    def __init__(self, floor_count: int):
        self.state = ElevatorState(floor=0, move='STOP')
        self.floor_count = floor_count
        self.floor_queue = []
        self.last_move_ts = datetime.now()  # todo возможны проблемы на 1 итерации

    def _one_floor_down(self):
        time_diff_seconds = ((ts_now := datetime.now()) - self.last_move_ts).seconds
        if self.state.floor and time_diff_seconds:
            self.state.floor -= 1
            self.state.move = 'DOWN'
            self.last_move_ts = ts_now
            print(f'1 этаж вниз; текущий этаж: {self.state.floor + 1}')  # todo потом сделать логирование

    def _one_floor_up(self):
        time_diff_seconds = ((ts_now := datetime.now()) - self.last_move_ts).seconds
        if self.state.floor < self.floor_count and time_diff_seconds:
            self.state.floor += 1
            self.state.move = 'UP'
            self.last_move_ts = ts_now
            print(f'1 этаж вверх; текущий этаж: {self.state.floor + 1}')  # todo потом сделать логирование

    def _wait_on_floor(self):
        print(f'Остановка на этаже: {self.state.floor + 1}')  # todo потом сделать логирование

    def move(self, target_floor: int, time_diff: timedelta):
        direction = target_floor - self.state.floor
        print(self.state.move)
        if direction < 0 and time_diff.seconds:
            self._one_floor_down()
            self.state.move = 'STOP' if self.state.floor == target_floor else 'DOWN'
        if direction > 0 and time_diff.seconds:
            self._one_floor_up()
            self.state.move = 'STOP' if self.state.floor == target_floor else 'UP'

    def logic(self, pressed_buttons: list[DisplayButton], time_diff: timedelta) -> ElevatorState:
        """
        Логика поведения лифта, запрашивается каждый кадр
        """
        if not pressed_buttons:
            return self.state
        target_floor = self.get_target_floor(pressed_buttons=pressed_buttons)
        if target_floor == self.state.floor:
            self.state.move = 'STOP'
            return self.state

        match self.state.move:
            case 'UP':
                pass  # пока просто везем пассажира на этаж
            case 'DOWN':
                pass
            case 'STOP':
                self.last_move_ts = datetime.now()
        self.move(target_floor=target_floor, time_diff=time_diff)
        return self.state

    def get_target_floor(self, pressed_buttons: list[DisplayButton]) -> int | None:
        if pressed_buttons:
            return max([btn.floor for btn in pressed_buttons])  # todo ПОТОМ РАСШИРИТЬ
