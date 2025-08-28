from app.model.elevator import Elevator
from app.view.view import View

FLOOR_COUNT = 5

view = View(floor_count=FLOOR_COUNT)
elevator = Elevator(floor_count=FLOOR_COUNT)

if __name__ == "__main__":
    view.run(elevator=elevator)
