W = [
    "break","case","char","const","continue","do","double",
    "else","extern","float","for","if","int","long","class",
    "return","sizeof","static","switch","typedef","void","while"
]

O = [
    "++", "--", "+=", "-=", "*=", "/=", "%=",
    "==", "!=", "<=", ">=", "&&", "||",
    "+", "-", "*", "/", "%", "=", "<", ">", "!", "&", "|", "^", "~"
]

R = ["(", ")", "{", "}", "[", "]", ";", ",", ".", ":", "?"]

used_keywords = []
used_operators = []
used_separators = []
identifiers = []
numbers = []
strings = []
tokens_by_line = {}
errors = []
in_block_comment = False

def add_token(line, lexema):
    tokens_by_line.setdefault(line, []).append(lexema)

def add_unique(lst, value):
    if value not in lst:
        lst.append(value)
    return lst.index(value) + 1

def lexer(code):
    global in_block_comment
    i = 0
    line = 1
    n = len(code)

    while i < n:
        ch = code[i]

        if ch == "\n":
            line += 1
            i += 1
            continue

        if in_block_comment:
            if code[i:i+2] == "*/":
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue

        if ch.isspace():
            i += 1
            continue

        if code[i:i+2] == "//":
            while i < n and code[i] != "\n":
                i += 1
            continue

        if code[i:i+2] == "/*":
            in_block_comment = True
            i += 2
            continue

        if ch == '"':
            start = i
            i += 1
            escaped = False

            while i < n:
                if code[i] == "\n":
                    errors.append(f"Незакрытая строка, строка {line}")
                    break

                if code[i] == '"' and not escaped:
                    i += 1
                    s = code[start:i]
                    idx = add_unique(strings, s)
                    add_token(line, f"S{idx}")
                    break

                if code[i] == "\\" and not escaped:
                    escaped = True
                else:
                    escaped = False

                i += 1
            continue

        if ch.isalpha() or ch == "_":
            start = i
            while i < n and (code[i].isalnum() or code[i] == "_"):
                i += 1

            word = code[start:i]

            if word in W:
                idx = add_unique(used_keywords, word)
                add_token(line, f"W{idx}")
            else:
                idx = add_unique(identifiers, word)
                add_token(line, f"I{idx}")
            continue

        if ch.isdigit():
            start = i
            dot_count = 0

            while i < n and (code[i].isdigit() or code[i] == "."):
                if code[i] == ".":
                    dot_count += 1
                i += 1

            num = code[start:i]

            if dot_count > 1:
                errors.append(f"Ошибка числа '{num}', строка {line}")
                continue

            if i < n and (code[i].isalpha() or code[i] == "_"):
                start_err = start
                while i < n and (code[i].isalnum() or code[i] == "_"):
                    i += 1
                wrong = code[start_err:i]
                errors.append(f"Неверный идентификатор '{wrong}', строка {line}")
                continue

            idx = add_unique(numbers, num)
            add_token(line, f"N{idx}")
            continue

        if ch in "!<>=&|":
            start = i
            while i < n and code[i] in "!<>=&|":
                i += 1
            seq = code[start:i]

            if seq not in O:
                errors.append(f"Неверный оператор '{seq}', строка {line}")
                continue

            idx = add_unique(used_operators, seq)
            add_token(line, f"O{idx}")
            continue

        matched = False
        for op in sorted(O, key=len, reverse=True):
            if code.startswith(op, i):
                idx = add_unique(used_operators, op)
                add_token(line, f"O{idx}")
                i += len(op)
                matched = True
                break

        if matched:
            continue

        if ch in R:
            idx = add_unique(used_separators, ch)
            add_token(line, f"R{idx}")
            i += 1
            continue

        errors.append(f"Неизвестный символ '{ch}', строка {line}")
        i += 1

    if in_block_comment:
        errors.append("Незакрытый комментарий /* */")

def main():
    filename = "C.txt"
    lex_row_file = "result.txt"
    table_file = "table.txt"
    error_file = "error.txt"

    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    lexer(code)

    lex_row = []
    for line in sorted(tokens_by_line):
        lex_row.append(f"{' '.join(tokens_by_line[line])}")

    table = []

    table.append("Таблица служебных слов")
    for i, v in enumerate(used_keywords, 1):
        table.append(f"{i}. {v}")

    table.append("\nТаблица идентификаторов")
    for i, v in enumerate(identifiers, 1):
        table.append(f"{i}. {v}")

    table.append("\nТаблица операций")
    for i, v in enumerate(used_operators, 1):
        table.append(f"{i}. {v}")

    table.append("\nТаблица разделителей")
    for i, v in enumerate(used_separators, 1):
        table.append(f"{i}. {v}")

    table.append("\nТаблица чисел")
    for i, v in enumerate(numbers, 1):
        table.append(f"{i}. {v}")

    table.append("\nТаблица строк")
    for i, v in enumerate(strings, 1):
        table.append(f"{i}. {v}")

    error = []
    if errors:
        error.extend(errors)

    with open(lex_row_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lex_row))

    with open(table_file, "w", encoding="utf-8") as f:
        f.write("\n".join(table))

    with open(error_file, "w", encoding="utf-8") as f:
        f.write("\n".join(error))

if __name__ == "__main__":
    main()