import random
import math
total_clients_target = 400  # сколько клиентов обслужит система
time_now = 0
clients_served = 0
clients_lost = 0
queue1 = []
queue2 = []
# время окончания обслуживания на каждой колонке
pump1_free = 0
pump2_free = 0
queue1_lengths = []
queue2_lengths = []
departure_times = []
client_times = []  # время пребывания каждого клиента

def exp(mean):
    return -math.log(1 - random.random()) * mean

next_arrival = exp(0.1)
while clients_served < total_clients_target:
    # Ближайшее событие
    events = [("arrival", next_arrival)]
    if pump1_free > time_now:
        events.append(("pump1_finish", pump1_free))
    if pump2_free > time_now:
        events.append(("pump2_finish", pump2_free))

    next_event = min(events, key=lambda x: x[1])
    event_type, event_time = next_event

    time_now = event_time

    if event_type == "arrival":
        # Прибыл новый клиент
        next_arrival = time_now + exp(0.1)
        # Выбор очереди
        if len(queue1) <= len(queue2) and len(queue1) < 5:
            queue1.append(time_now)  # время прибытия
        elif len(queue2) < 5:
            queue2.append(time_now)
        else:
            clients_lost += 1  # обе очереди заполнены

    elif event_type == "pump1_finish":
        clients_served += 1
        departure_times.append(time_now)
        if queue1: # начинаем обслуживать следующего из очереди 1
            arrival_time = queue1.pop(0)
            client_times.append(time_now - arrival_time)
            pump1_free = time_now + exp(0.5)
        else:
            pump1_free = float('inf')

    elif event_type == "pump2_finish":
        clients_served += 1
        departure_times.append(time_now)
        if queue2:
            arrival_time = queue2.pop(0)
            client_times.append(time_now - arrival_time)
            pump2_free = time_now + exp(0.5)
        else:
            pump2_free = float('inf')


    if pump1_free <= time_now and queue1: # если колонка свободна и есть очередь то начинаем обслуживание
        arrival_time = queue1.pop(0)
        client_times.append(0)
        pump1_free = time_now + exp(0.5)
    if pump2_free <= time_now and queue2:
        arrival_time = queue2.pop(0)
        client_times.append(0)
        pump2_free = time_now + exp(0.5)

    queue1_lengths.append(len(queue1))
    queue2_lengths.append(len(queue2))

departure_intervals = [departure_times[i] - departure_times[i - 1] for i in range(1, len(departure_times))]
print(f"Средняя число клиентов в очереди 1: {sum(queue1_lengths) / len(queue1_lengths):.2f}")
print(f"Средняя число клиентов в очереди 2: {sum(queue2_lengths) / len(queue2_lengths):.2f}")
print(f"Процент отказов: {clients_lost / (clients_served + clients_lost) * 100:.1f}%")
print(f"Средний интервал между отъездами: {sum(departure_intervals) / len(departure_intervals) if departure_intervals else 0:.3f}")
print(f"Среднее время пребывания клиента: {sum(client_times) / len(client_times) if client_times else 0:.3f}")