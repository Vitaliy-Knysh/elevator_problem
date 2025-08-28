import asyncio


class Elevator:
    def __init__(self, floor_count: int):
        self.floor = 0
        self.floor_count = floor_count
        self.floors_queue = []

    async def _one_floor_down(self, wait_time: float | int) -> int:
        if self.floor:
            await asyncio.sleep(wait_time)
            self.floor -= 1
            print(f'1 этаж вниз; текущий этаж: {self.floor}')  # todo потом сделать логирование
        return self.floor

    async def _one_floor_up(self, wait_time: float | int) -> int:
        if self.floor < self.floor_count:
            await asyncio.sleep(wait_time)
            self.floor += 1
            print(f'1 этаж вверх; текущий этаж: {self.floor}')  # todo потом сделать логирование
        return self.floor

    async def move(self, target_floor: int, wait_time: float | int = 1):
        if target_floor < 0:
            target_floor = 0
        elif target_floor > self.floor_count:
            target_floor = self.floor_count
        direction = target_floor - self.floor
        while self.floor != target_floor:
            if direction < 0:
                await self._one_floor_down(wait_time=wait_time)
            if direction > 0:
                await self._one_floor_up(wait_time=wait_time)
