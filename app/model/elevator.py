class Elevator:
    def __init__(self, floors_count: int):
        self.floor = 0
        self.floors_count = floors_count

    def _one_floor_down(self) -> int:
        if self.floor:
            self.floor -= 1
        return self.floor

    def _one_floor_up(self) -> int:
        if self.floor < self.floors_count:
            self.floor += 1
        return self.floor

    def move(self, target_floor: int):
        pass
