import asyncio

import pytest

from app.model.elevator import Elevator


class TestElevator:
    @pytest.fixture
    def elevator(self):
        return Elevator(floor_count=5)

    @pytest.mark.parametrize('target_floor,wait_time,expected',
                             ((0, 0.1, 0), (-1, 0.1, 0), (-100, 0.1, 0), (5, 0.1, 5), (155, 0.1, 5)))
    def test_move(self, elevator, target_floor, wait_time, expected):
        asyncio.run(elevator.move(target_floor=target_floor, wait_time=wait_time))
        assert elevator.floor == expected
        # print('\n')
