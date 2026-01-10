import random
import math
total_parts = 500  # сколько деталей обработать
time_now = 0  # текущее время
parts_done = 0  # сколько деталей сделано
queue = []  # очередь заданий
machine_busy = False  # станок занят?
machine_broken = False  # станок сломан?
repair_time_left = 0  # сколько осталось чинить
setup_time_left = 0  # сколько осталось наладки
work_time_left = 0  # сколько осталось работы над деталью
next_break = 0  # когда следующая поломка
next_arrival = 0  # когда следующая деталь придет
total_work_time = 0 # всего работал
total_idle_time = 0 # простоял
part_times = []  # время выполнения каждой детали

def exp(mean):
    return -math.log(1 - random.random()) * mean

def norm(mean, std):
    return random.normalvariate(mean, std)

def unif(a, b):
    return a + random.random() * (b - a)

next_arrival = exp(1)
next_break = norm(20, 2)

while parts_done < total_parts:
    # находим ближайшее событие
    events = []
    if not machine_broken:
        if not machine_busy and queue:
            events.append(("start_setup", time_now))
        if machine_busy and work_time_left > 0:
            events.append(("finish_work", time_now + work_time_left))
        if machine_busy and setup_time_left > 0:
            events.append(("finish_setup", time_now + setup_time_left))
    if machine_broken and repair_time_left > 0:
        events.append(("finish_repair", time_now + repair_time_left))

    events.append(("arrival", next_arrival))
    if next_break > time_now:
        events.append(("break", next_break))

    # выбор ближайшенго события
    next_event = min(events, key=lambda x: x[1])
    event_type, event_time = next_event

    delta = event_time - time_now
    time_now = event_time

    # обнавляем время
    if machine_busy and work_time_left > 0:
        total_work_time += delta
    else:
        total_idle_time += delta

    # обработка события
    if event_type == "arrival":
        queue.append(time_now)  # запоминаем время прибытия
        next_arrival = time_now + exp(1)  # следующее прибытие

    elif event_type == "break":
        machine_broken = True
        machine_busy = False
        repair_time_left = unif(0.1, 0.5)
        if work_time_left > 0:
            queue.insert(0, time_now)
            work_time_left = 0
        next_break = time_now + norm(20, 2)

    elif event_type == "finish_repair":
        machine_broken = False
        repair_time_left = 0

    elif event_type == "start_setup":
        machine_busy = True
        setup_time_left = unif(0.2, 0.5)

    elif event_type == "finish_setup":
        setup_time_left = 0
        work_time_left = norm(0.5, 0.1)

    elif event_type == "finish_work":
        machine_busy = False
        work_time_left = 0
        parts_done += 1
        if queue:
            arrival_time = queue.pop(0)
            part_times.append(time_now - arrival_time)

    # eсли станок свободен и не сломан, и есть очередь — начинаем наладку
    if not machine_broken and not machine_busy and queue:
        machine_busy = True
        setup_time_left = unif(0.2, 0.5)

print(f"Общее время: {time_now:.2f} ч")
print(f"Загрузка станка: {total_work_time / time_now * 100:.1f}%")
print(f"Среднее время выполнения детали: {sum(part_times) / len(part_times):.2f} ч")