from app.model.elevator import Elevator
from app.utils.argument_parser import debug_argument
from app.view.view import View

if __name__ == "__main__":
    if debug_argument():
        floor_count = 5
    else:
        floor_count = int(input('Добро пожаловать в симулятор лифта!\nВведите количество этажей: '))
    elevator = Elevator(floor_count=floor_count)
    view = View(floor_count=floor_count)
    view.run(elevator=elevator)
