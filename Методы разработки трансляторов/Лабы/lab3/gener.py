def read_rpn(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().strip().split()


def generate_java(rpn_tokens):
    stack = []
    i = 0
    n = len(rpn_tokens)
    lines = []
    temp_counter = 1
    indent = "        "

    def new_temp():
        nonlocal temp_counter
        t = f"t{temp_counter}"
        temp_counter += 1
        return t

    while i < n:
        token = rpn_tokens[i]

        if token.endswith(':'):
            i += 1
            continue

        if (token.replace('.', '', 1).isdigit() or
                (token[0].isalpha() and token not in ('УПЛ', 'БП', 'return', 'u-'))):
            stack.append(token)
            i += 1
            continue

        if token == '=':
            value = stack.pop()
            var = stack.pop()
            lines.append(f"{indent}{var} = {value};")
            i += 1
            continue

        if token in ('+', '-', '*', '/', '%', '!=', '==', '<', '>', '<=', '>='):
            right = stack.pop()
            left = stack.pop()
            temp = new_temp()
            lines.append(f"{indent}{temp} = {left} {token} {right};")
            stack.append(temp)
            i += 1
            continue

        if token == 'УПЛ':
            label = stack.pop()
            condition = stack.pop()
            lines.append(f"{indent}if ({condition}) {{")
            indent = "            "
            i += 1
            continue

        if token == 'БП':
            label = stack.pop()
            lines.append(f"{indent}}}")
            indent = "        "
            i += 1
            continue

        if token == 'return':
            value = stack.pop() if stack else "0"
            lines.append(f"{indent}return {value};")
            i += 1
            continue

        if token == 'u-':
            operand = stack.pop()
            temp = new_temp()
            lines.append(f"{indent}{temp} = -{operand};")
            stack.append(temp)
            i += 1
            continue

        i += 1

    return lines


def main():
    rpn_tokens = read_rpn("../lab2/rpn.txt")
    code_lines = generate_java(rpn_tokens)

    variables = set()
    for line in code_lines:
        if ' = ' in line and not line.strip().startswith('if'):
            var = line.split(' = ')[0].strip()
            if var and not var.startswith('t'):
                variables.add(var)

    java_code = []
    java_code.append("public class GeneratedProgram {")
    java_code.append("    public static void main(String[] args) {")

    for var in sorted(variables):
        java_code.append(f"        int {var};")

    if variables:
        java_code.append("")

    java_code.extend(code_lines)

    java_code.append("    }")
    java_code.append("}")

    with open("output.java", "w", encoding="utf-8") as f:
        f.write("\n".join(java_code))

    for line in java_code:
        print(line)


if __name__ == "__main__":
    main()