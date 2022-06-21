# coding: utf-8
# license: GPLv3

import tkinter
from PIL import Image, ImageTk, ImageDraw
from tkinter.filedialog import *
from solar_vis import *
from solar_model import *
from solar_input import *

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""

call_count = 0

black_img = Image.new("RGBA", (window_width, window_height), (0, 0, 0, 255))

show_tracks = False

def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global physical_time
    global displayed_time
    global track_drawer
    global black_img
    global tracks
    global tracks_img
    global tracks_container
    global call_count
    global space
    recalculate_space_objects_positions(space_objects, time_step.get())
    call_count += 1

    if call_count % 2 == 0 and show_tracks:
        tracks = Image.blend(tracks, black_img, 0.02)
        track_drawer = ImageDraw.Draw(tracks, "RGBA")

    for body in space_objects:
        update_object_position(space, body)
        if show_tracks:
            draw_track(track_drawer, body)

    if show_tracks:
        space.delete(tracks_container)
        tracks_img = ImageTk.PhotoImage(tracks)
        tracks_container = space.create_image(0, 0, image=tracks_img, anchor=tkinter.NW)
        space.tag_lower(tracks_container, space.find_all()[0])


    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")

    if perform_execution:
        space.after(101 - int(time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    start_button['text'] = "Stop"
    start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def toggle_track():
    global show_tracks
    global track_button
    global track_drawer
    global black_img
    global tracks
    global tracks_container
    global space
    if show_tracks:
        show_tracks = False
        track_button['text'] = "Show track"
        space.delete(tracks_container)
        tracks = Image.blend(tracks, black_img, 1)
        track_drawer = ImageDraw.Draw(tracks, "RGBA")
    else:
        show_tracks = True
        track_button['text'] = "Put away track"


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global perform_execution
    perform_execution = False
    for obj in space_objects:
        space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

    for obj in space_objects:
        if type(obj) is Planet:
            create_planet_image(space, obj)
        else:
            raise AssertionError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    write_space_objects_data_to_file(out_filename, space_objects)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global tracks
    global tracks_img
    global tracks_container
    global tracks_container
    global track_drawer
    global track_button

    print('Modelling started!')
    physical_time = 0

    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(side=tkinter.TOP)

    tracks = Image.new("RGBA", (window_width, window_height))
    track_drawer = ImageDraw.Draw(tracks, "RGBA")
    tracks_img = ImageTk.PhotoImage(tracks)
    tracks_container = space.create_image(0, 0, image=tracks_img, anchor=tkinter.NW)

    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    start_button.pack(side=tkinter.LEFT)
    

    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save file", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    track_button = tkinter.Button(frame, text="Show track", command=toggle_track, width=12)
    track_button.pack(side=tkinter.LEFT)

    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print('Modelling finished!')

if __name__ == "__main__":
    main()
