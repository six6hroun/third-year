#Разделение видео на посты с равной суммарной длительностью
def sort_video(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        n, k = map(int, f.readline().split())
        durations = list(map(int, f.readline().split()))

    all_dlitelnost = sum(durations)

    if all_dlitelnost % k != 0:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Нет")
        return "Нет"

    sum_post = all_dlitelnost // k
    segments = []
    sum_seg = 0
    count_seg = 0

    for duration in durations:
        sum_seg += duration
        count_seg += 1

        if sum_seg == sum_post:
            segments.append(count_seg)
            sum_seg = 0
            count_seg = 0
        elif sum_seg > sum_post:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Нет")
            return "Нет"

    if len(segments) == k and sum_seg == 0:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Да\n")
            f.write(" ".join(map(str, segments)))
        return "Да", segments
    else:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Нет")
        return "Нет"

result = sort_video(r'C:\учеба\Интерпретируемые языки программирования\путь\in.txt', output_file= r'C:\учеба\Интерпретируемые языки программирования\путь\out.txt')
print(f"Результат: {result}")