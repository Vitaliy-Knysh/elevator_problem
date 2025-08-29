from datetime import datetime, timedelta

from app.model.dto import DisplayButton, ElevatorState
from app.utils import logger

logger = logger.get_logger()


class Elevator:
    def __init__(self, floor_count: int):
        self.state = ElevatorState(floor=0, move='STOP')
        self.floor_count = floor_count
        self.floor_queue = []
        self.last_move_ts = datetime.now()
        self.need_to_wait = False

    def _one_floor_down(self):
        time_diff_seconds = ((ts_now := datetime.now()) - self.last_move_ts).seconds
        if self.state.floor and time_diff_seconds:
            if self.state.floor >= 1:
                self.state.floor -= 1
            self.last_move_ts = ts_now
            logger.info(f'1 этаж вниз; текущий этаж: {self.state.floor + 1}')

    def _one_floor_up(self):
        time_diff_seconds = ((ts_now := datetime.now()) - self.last_move_ts).seconds
        if self.state.floor < self.floor_count and time_diff_seconds:
            if self.state.floor < self.floor_count - 1:
                self.state.floor += 1
            self.last_move_ts = ts_now
            logger.info(f'1 этаж вверх; текущий этаж: {self.state.floor + 1}')

    def _wait_on_floor(self):
        if (datetime.now() - self.last_move_ts).seconds:
            self.need_to_wait = False
            logger.info(f'Остановка на этаже: {self.state.floor + 1}')

    def _move(self, target_floor: int, time_diff: timedelta):
        direction = target_floor - self.state.floor
        logger.info(f'DIRECTION: {direction}\nTARGET FLOOR: {target_floor}\nCURRENT_FLOOR: {self.state.floor}')
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
        self._unstuck(target_floor=target_floor)
        self._move(target_floor=target_floor, time_diff=time_diff)
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
                max_available_floor = self.state.floor - 1 if self.state.floor else 0
                for floor in sorted(floors_requested, reverse=True):
                    if floor <= max_available_floor:
                        return floor
                return self.state.floor
            case 'STOP':
                if self.floor_queue[0] > self.state.floor:
                    return self.floor_queue[0]
                else:
                    return max(floors_requested)

    @staticmethod
    def _get_unique_floors(pressed_buttons: list[DisplayButton]) -> list[int]:
        result = []
        for btn in pressed_buttons:
            if btn.floor not in result:
                result.append(btn.floor)
        return result

    def _unstuck(self, target_floor: int):
        """
        исключает очень редкие случаи застревания
        """
        if self.state.move == 'UP' and self.state.floor > target_floor:
            self.state.move = 'STOP'
        if self.state.move == 'DOWN' and self.state.floor < target_floor:
            self.state.move = 'STOP'
