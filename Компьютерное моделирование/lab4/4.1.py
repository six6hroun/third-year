def multiplicative(x_0, a, m, n):
    X_sequence = [x_0]
    R_sequence = [x_0 / m]
    print("i\tXᵢ\t\tВычисление\t\t\t\tXᵢ₊₁\tRᵢ")
    print("-" * 51)
    period_found = False
    period_length = 0
    for i in range(min(n, m * 2)):
        current_x = X_sequence[-1]
        current_r = R_sequence[-1]
        next_x = (a * current_x) % m
        next_r = next_x / m
        calculation = f"({a} × {current_x}) mod {m}"
        print(f"{i}\t{current_x}\t\t{calculation}\t\t{next_x}\t\t{next_r:.5f}")
        if next_x in X_sequence and i > 0:
            first_occurrence = X_sequence.index(next_x)
            period_length = len(X_sequence) - first_occurrence
            print(f"\nОбнаружено повторение X{len(X_sequence)} = X{first_occurrence} = {next_x}")
            period_found = True
            break
        X_sequence.append(next_x)
        R_sequence.append(next_r)
        if len(X_sequence) >= n + 1:
            break
    if not period_found and len(X_sequence) >= n + 1:
        print(f"\nСгенерировано {n} чисел без повторений")
        period_length = "не определен (последовательность длиннее запрошенного N)"

    return X_sequence, R_sequence, period_length

x_0 = 15
a = 11
m = 127
n = 1000
X_seq, R_seq, period = multiplicative(x_0, a, m, n)