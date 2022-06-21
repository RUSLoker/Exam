# coding: utf-8
# license: GPLv3

from solar_objects import Planet


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            planet = Planet()
            parse_planet_parameters(line, planet)
            objects.append(planet)

    return objects


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """
    args = line.split()
    if len(args) != 8:
        print("Ты ввел хуйню!")
        print(line)
    else:
        planet.name = args[0]
        planet.R = float(args[1])
        planet.color = args[2]
        planet.m = float(args[3])
        planet.x = float(args[4])
        planet.y = float(args[5])
        planet.Vx = float(args[6])
        planet.Vy = float(args[7])


def write_space_objects_data_to_file(output_filename, space_objects: list[Planet]):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            print(f"{obj.name} {obj.R} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}", file=out_file)

if __name__ == "__main__":
    print("This module is not for direct call!")
