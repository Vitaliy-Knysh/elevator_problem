from app.model.elevator import Elevator
from app.utils.argument_parser import debug_argument
from app.view.view import View

if __name__ == "__main__":
    if debug_argument():
        floor_count = 5
    else:
        floor_count = 0
        print('Добро пожаловать в симулятор лифта!\n')
        while floor_count < 1:
            try:
                floor_count = int(input('Введите количество этажей: '))
                if floor_count < 1:
                    print('Некорректное количество этажей.')
            except (ValueError, NameError):
                print('Некорректное количество этажей.')

    elevator = Elevator(floor_count=floor_count)
    view = View(floor_count=floor_count)
    view.run(elevator=elevator)
