def parse_table(filename):
    SECTION_MAP = {
        "Таблица служебных слов": "W",
        "Таблица идентификаторов": "I",
        "Таблица операций": "O",
        "Таблица разделителей": "R",
        "Таблица чисел": "N",
        "Таблица строк": "S"
    }

    tables = {k: {} for k in SECTION_MAP.values()}
    current = None

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line in SECTION_MAP:
                current = SECTION_MAP[line]
                continue

            if current and ". " in line:
                num, val = line.split(". ", 1)
                tables[current][int(num)] = val.strip()

    return tables


def decode_result(filename, tables):
    decoded = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            tokens = line.strip().split()
            decoded_line = []

            for token in tokens:
                t = token[0]
                idx = int(token[1:])
                decoded_line.append(tables[t][idx])

            decoded.append(decoded_line)

    return decoded


def has_errors(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return len(lines) > 1 and lines[0].strip() != ""
    except FileNotFoundError:
        return False


PRIORITY = {
    '=': 1, '+=': 1, '-=': 1, '*=': 1, '/=': 1, '%=': 1,
    '||': 2,
    '&&': 3,
    '|': 4,
    '^': 5,
    '&': 6,
    '==': 7, '!=': 7,
    '<': 8, '>': 8, '<=': 8, '>=': 8,
    '<<': 9, '>>': 9,
    '+': 10, '-': 10,
    '*': 11, '/': 11, '%': 11,
    '(': 0, ')': 0,
}


def is_operator(token):
    return token in PRIORITY and token not in ('(', ')')


def is_unary(context, token):
    if token not in ('+', '-'):
        return False
    return context.get('last_was_operator', True) or context.get('last_was_open_paren', False)


def infix_to_rpn(tokens):
    output = []
    stack = []
    context = {'last_was_operator': True, 'last_was_open_paren': False}

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if (token.isidentifier() or
            token.replace('.', '', 1).replace('-', '', 1).isdigit() or
            (len(token) > 1 and token[0] == '"' and token[-1] == '"')):
            output.append(token)
            context['last_was_operator'] = False
            context['last_was_open_paren'] = False
            i += 1
            continue

        if token == '(':
            stack.append(token)
            context['last_was_operator'] = True
            context['last_was_open_paren'] = True
            i += 1
            continue

        if token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
            context['last_was_operator'] = False
            context['last_was_open_paren'] = False
            i += 1
            continue

        if is_operator(token):
            if is_unary(context, token):
                stack.append(f"u{token}")
            else:
                while (stack and stack[-1] != '(' and
                       is_operator(stack[-1].replace('u', '', 1)) and
                       PRIORITY.get(stack[-1].replace('u', '', 1), 0) >= PRIORITY.get(token, 0)):
                    output.append(stack.pop())
                stack.append(token)

            context['last_was_operator'] = True
            context['last_was_open_paren'] = False
            i += 1
            continue

        i += 1

    while stack:
        output.append(stack.pop())

    return output


class LabelGenerator:
    def __init__(self):
        self.counter = 1

    def new(self):
        label = f"M{self.counter}"
        self.counter += 1
        return label


def to_rpn(tokens):
    output = []
    label_gen = LabelGenerator()
    i = 0
    n = len(tokens)

    while i < n:
        token = tokens[i]

        if token in ('int', 'float', 'double', 'char', 'long', 'short', 'unsigned', 'signed', 'void'):
            i += 1
            continue

        if token == 'return':
            i += 1
            expr = []
            while i < n and tokens[i] != ';':
                expr.append(tokens[i])
                i += 1
            output.extend(infix_to_rpn(expr))
            output.append('return')
            i += 1
            continue

        if token == 'if':
            i += 1

            if i < n and tokens[i] == '(':
                i += 1
                condition = []
                while i < n and tokens[i] != ')':
                    condition.append(tokens[i])
                    i += 1
                i += 1

            output.extend(infix_to_rpn(condition))

            else_label = label_gen.new()
            end_label = label_gen.new()

            output.append(else_label)
            output.append('УПЛ')

            if i < n and tokens[i] == '{':
                i += 1
                then_block = []
                brace_count = 1
                while i < n and brace_count > 0:
                    if tokens[i] == '{':
                        brace_count += 1
                    elif tokens[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            i += 1
                            break
                    then_block.append(tokens[i])
                    i += 1

            output.extend(to_rpn(then_block))

            output.append(end_label)
            output.append('БП')

            output.append(f"{else_label}:")

            if i < n and tokens[i] == 'else':
                i += 1

                if i < n and tokens[i] == '{':
                    i += 1
                    else_block = []
                    brace_count = 1
                    while i < n and brace_count > 0:
                        if tokens[i] == '{':
                            brace_count += 1
                        elif tokens[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                i += 1
                                break
                        else_block.append(tokens[i])
                        i += 1

                output.extend(to_rpn(else_block))

            output.append(f"{end_label}:")
            continue

        if i + 1 < n and tokens[i + 1] in ('+=', '-=', '*=', '/=', '%='):
            var = token
            op = tokens[i + 1][0]

            i += 2

            expr = []
            while i < n and tokens[i] != ';':
                expr.append(tokens[i])
                i += 1

            rpn_expr = infix_to_rpn(expr)

            # var = var op expr
            output.append(var)
            output.append(var)
            output.extend(rpn_expr)
            output.append(op)
            output.append('=')

            i += 1
            continue

        if i + 1 < n and tokens[i + 1] == '=':
            var = token

            i += 2

            expr = []
            while i < n and tokens[i] != ';':
                expr.append(tokens[i])
                i += 1

            rpn_expr = infix_to_rpn(expr)

            output.append(var)
            output.extend(rpn_expr)
            output.append('=')

            i += 1
            continue

        i += 1

    return output


def main():
    table_file = "../lab1/table.txt"
    result_file = "../lab1/result.txt"
    error_file = "../lab1/error.txt"

    if has_errors(error_file):
        print("Ошибки в лексическом анализаторе (error.txt не пуст)")
        return

    tables = parse_table(table_file)
    decoded = decode_result(result_file, tables)

    tokens = []
    for line in decoded:
        tokens.extend(line)

    print("Токены после декодирования:")
    print(tokens)
    print()

    rpn = to_rpn(tokens)

    print("ОПЗ:")
    print(" ".join(rpn))

    with open("rpn.txt", "w", encoding="utf-8") as f:
        f.write(" ".join(rpn))


if __name__ == "__main__":
    main()