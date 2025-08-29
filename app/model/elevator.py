from datetime import datetime, timedelta

from app.dto import DisplayButton, ElevatorState


class Elevator:
    def __init__(self, floor_count: int):
        self.state = ElevatorState(floor=0, move='STOP')
        self.floor_count = floor_count
        self.floor_queue = []
        self.last_move_ts = datetime.now()  # todo возможны проблемы на 1 итерации
        self.need_to_wait = False

    def _one_floor_down(self):
        time_diff_seconds = ((ts_now := datetime.now()) - self.last_move_ts).seconds
        if self.state.floor and time_diff_seconds:
            self.state.floor -= 1
            self.last_move_ts = ts_now
            print(f'1 этаж вниз; текущий этаж: {self.state.floor + 1}')  # todo потом сделать логирование

    def _one_floor_up(self):
        time_diff_seconds = ((ts_now := datetime.now()) - self.last_move_ts).seconds
        if self.state.floor < self.floor_count and time_diff_seconds:
            self.state.floor += 1
            self.last_move_ts = ts_now
            print(f'1 этаж вверх; текущий этаж: {self.state.floor + 1}')  # todo потом сделать логирование

    def _wait_on_floor(self):
        if (datetime.now() - self.last_move_ts).seconds:
            self.need_to_wait = False
            print((datetime.now() - self.last_move_ts).seconds)
            print(f'Остановка на этаже: {self.state.floor + 1}')  # todo потом сделать логирование

    def move(self, target_floor: int, time_diff: timedelta):
        direction = target_floor - self.state.floor
        match self.state.move:
            case 'UP':
                if self.state.floor == target_floor:
                    self.state.move = 'STOP'
                    self.need_to_wait = True
                    self.floor_queue.remove(self.state.floor)
                else:
                    self._one_floor_up()
            case 'DOWN':
                if self.state.floor == target_floor:
                    self.state.move = 'STOP'
                    self.need_to_wait = True
                    self.floor_queue.remove(self.state.floor)
                else:
                    self._one_floor_down()
            case 'STOP':
                if self.need_to_wait:
                    self._wait_on_floor()
                elif direction < 0 and time_diff.seconds:
                    self.state.move = 'DOWN'
                    self.last_move_ts = datetime.now()
                    self._one_floor_down()
                elif direction > 0 and time_diff.seconds:
                    self.state.move = 'UP'
                    self.last_move_ts = datetime.now()
                    self._one_floor_up()

    def logic(self, pressed_buttons: list[DisplayButton], time_diff: timedelta) -> ElevatorState:
        """
        Логика поведения лифта, запрашивается каждый кадр
        """
        if not pressed_buttons:
            return self.state
        target_floor = self.get_target_floor(pressed_buttons=pressed_buttons)
        self.move(target_floor=target_floor, time_diff=time_diff)
        return self.state

    def get_target_floor(self, pressed_buttons: list[DisplayButton]) -> int:
        if not pressed_buttons:
            return self.state.floor
        floors_requested = [btn.floor for btn in pressed_buttons]
        if not self.floor_queue:
            self.floor_queue = floors_requested
        else:
            for btn in floors_requested:
                if btn not in self.floor_queue:
                    self.floor_queue.append(btn)
        match self.state.move:
            case 'UP':
                return self.floor_queue[0]
            case 'DOWN':
                return max([btn.floor for btn in pressed_buttons])
            case 'STOP':
                if self.floor_queue[0] > self.state.floor:
                    return self.floor_queue[0]
                else:
                    return max([btn.floor for btn in pressed_buttons])
