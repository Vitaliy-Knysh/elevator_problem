import asyncio

from app.dto import DisplayButton, ElevatorState


class Elevator:
    SPEED = 0.3

    def __init__(self, floor_count: int):
        self.state = ElevatorState(floor=0, move='STOP')
        self.floor_count = floor_count
        self.floor_queue = []
        self.move_coroutine_running = False

    async def _one_floor_down(self, wait_time: float | int):
        if self.state.floor:
            await asyncio.sleep(wait_time)
            self.state.floor -= 1
            self.state.move = 'DOWN'
            print(f'1 этаж вниз; текущий этаж: {self.state.floor + 1}')  # todo потом сделать логирование

    async def _one_floor_up(self, wait_time: float | int):
        if self.state.floor < self.floor_count:
            await asyncio.sleep(wait_time)
            self.state.floor += 1
            self.state.move = 'UP'
            print(f'1 этаж вверх; текущий этаж: {self.state.floor + 1}')  # todo потом сделать логирование

    async def _wait_on_floor(self, wait_time: float | int):
        print(f'Остановка на этаже: {self.state.floor + 1}')  # todo потом сделать логирование
        await asyncio.sleep(wait_time)

    async def move(self, target_floor: int, wait_time: float | int = SPEED):
        self.move_coroutine_running = True
        if target_floor < 0:
            target_floor = 0
        elif target_floor > self.floor_count:
            target_floor = self.floor_count
        direction = target_floor - self.state.floor
        while self.state.floor != target_floor:
            if direction < 0:
                await self._one_floor_down(wait_time=wait_time)
            if direction > 0:
                await self._one_floor_up(wait_time=wait_time)
        await self._wait_on_floor(wait_time=wait_time)
        self.state.move = 'STOP'
        self.move_coroutine_running = False

    async def logic(self, pressed_buttons: list[DisplayButton]) -> ElevatorState:
        if not self.move_coroutine_running:
            match self.state.move:
                case 'UP':
                    pass
                case 'DOWN':
                    pass
                case 'STOP':
                    if pressed_buttons:
                        t_floor = max([btn.floor for btn in pressed_buttons])
                        await self.move(target_floor=t_floor)
        return self.state
