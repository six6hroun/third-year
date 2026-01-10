import random
import math

def exponential_raspred(mean_time):
    u = random.random()
    return -mean_time * math.log(u)

def normal_raspred(mean_time, std_time):
    t = random.gauss(mean_time, std_time)
    return max(0.1, t)

def simulate(queue_limit=None):
    all_work_time = 360
    interval_client = 3
    service_client = 5
    service_client_otklonenie = 1.5
    tek_time = 0.0
    queue = []
    baristas = [
        {"busy": False, "end_time": 0.0, "busy_time": 0.0},
        {"busy": False, "end_time": 0.0, "busy_time": 0.0}
    ]
    served_clients = 0
    leave_client = 0
    waiting_times = []
    queue_lengths = []
    next_arrival_time = exponential_raspred(interval_client)

    while tek_time < all_work_time:
        service_end_times = [
            b["end_time"] if b["busy"] else float("inf") for b in baristas
        ]
        next_service_end_time = min(service_end_times)

        if next_arrival_time <= next_service_end_time and next_arrival_time <= all_work_time:
            tek_time = next_arrival_time
            queue_lengths.append(len(queue))

            free_barista = None
            for b in baristas:
                if not b["busy"]:
                    free_barista = b
                    break

            if free_barista is not None:
                service_time = normal_raspred(service_client, service_client_otklonenie)
                free_barista["busy"] = True
                free_barista["end_time"] = tek_time + service_time
                free_barista["busy_time"] += service_time
                waiting_times.append(0.0)
                served_clients += 1
            else:
                if queue_limit is None or len(queue) < queue_limit:
                    queue.append(tek_time)
                else:
                    leave_client += 1

            next_arrival_time += exponential_raspred(interval_client)

        else:
            tek_time = next_service_end_time
            index_barista = service_end_times.index(next_service_end_time)
            barista = baristas[index_barista]

            if queue:
                arrival_time = queue.pop(0)
                waiting_time = tek_time - arrival_time
                waiting_times.append(waiting_time)
                served_clients += 1

                service_time = normal_raspred(service_client, service_client_otklonenie)
                barista["end_time"] = tek_time + service_time
                barista["busy_time"] += service_time
            else:
                barista["busy"] = False
                barista["end_time"] = 0.0

    avg_waiting_time = round(
        sum(waiting_times) / len(waiting_times), 2
    ) if waiting_times else 0.0

    avg_queue_length = round(
        sum(queue_lengths) / len(queue_lengths), 2
    ) if queue_lengths else 0.0

    max_queue_length = max(queue_lengths) if queue_lengths else 0

    utilization = round(
        sum(b["busy_time"] for b in baristas) / (2 * all_work_time), 2
    )

    return {
        "Обслужено клиентов": served_clients,
        "Отказов": leave_client,
        "Среднее время ожидания (мин)": avg_waiting_time,
        "Средняя длина очереди": avg_queue_length,
        "Максимальная длина очереди": max_queue_length,
        "Коэффициент загрузки бариста": utilization
    }

random.seed(1)
print("НЕОГРАНИЧЕННАЯ ОЧЕРЕДЬ")
result_1 = simulate()
for key, value in result_1.items():
    print(f"{key}: {value}")

print("\nОЧЕРЕДЬ С ОГРАНИЧЕНИЕМ (3 ЧЕЛОВЕКА)")
result_2 = simulate(queue_limit=3)
for key, value in result_2.items():
    print(f"{key}: {value}")