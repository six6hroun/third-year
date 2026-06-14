class Node:

    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, node):
        if node:
            self.children.append(node)

    def print_tree(self, level=0):
        print("│   " * level + "├── " + self.name)

        for child in self.children:
            child.print_tree(level + 1)


class Parser:

    def __init__(self):
        self.tokens = self.load_tokens()
        self.pos = 0

        if self.tokens:
            self.current = self.tokens[0]
        else:
            self.current = None

    def load_table(self):
        table = {}
        current = None

        with open("../lab1/table.txt", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if "служебных" in line:
                current = "W"
                continue

            elif "идентификаторов" in line:
                current = "I"
                continue

            elif "операций" in line:
                current = "O"
                continue

            elif "разделителей" in line:
                current = "R"
                continue

            elif "чисел" in line:
                current = "N"
                continue

            elif "строк" in line:
                current = "S"
                continue

            if "." in line:
                num, value = line.split(".", 1)
                key = current + num.strip()
                table[key] = value.strip()

        return table

    def load_tokens(self):
        table = self.load_table()
        tokens = []

        with open("../lab1/result.txt", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            for token in line.split():

                if token in table:
                    tokens.append(table[token])
                else:
                    tokens.append(token)

        return tokens

    def next(self):
        self.pos += 1

        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = None

    def error(self, msg):
        print("СИНТАКСИЧЕСКАЯ ОШИБКА")
        print(f"\nПозиция: {self.pos}")
        print(f"Ожидалось: {msg}")
        print(f"Найдено: {self.current}")
        print()

        exit()

    def match(self, token):
        if self.current == token:
            self.next()
        else:
            self.error(token)

    def is_identifier(self):
        reserved = [
            "int",
            "float",
            "char",
            "if",
            "else",
            "return"
        ]

        if self.current is None:
            return False

        return (
            self.current[0].isalpha()
            and
            self.current not in reserved
        )

    def is_number(self):
        if self.current is None:
            return False

        try:
            float(self.current)
            return True
        except:
            return False

    def is_type(self):
        return self.current in [
            "int",
            "float",
            "char"
        ]

    def program(self):
        root = Node("PROGRAM")

        self.match("int")
        self.match("main")
        self.match("(")
        self.match(")")

        block = self.block()

        root.add(block)

        return root

    def block(self):
        root = Node("BLOCK")

        self.match("{")

        while self.current != "}":
            root.add(
                self.statement()
            )

        self.match("}")

        return root

    def statement(self):

        if self.is_type():
            return self.declaration()

        elif self.current == "if":
            return self.if_statement()

        elif self.current == "return":
            return self.return_statement()

        elif self.is_identifier():
            return self.assignment()

        else:
            self.error("оператор")

    def declaration(self):
        root = Node("DECLARE")
        t = self.current
        root.add(
            Node(
                f"TYPE({t})"
            )
        )

        self.next()
        if not self.is_identifier():
            self.error("идентификатор")

        var = self.current
        root.add(
            Node(
                f"ID({var})"
            )
        )

        self.next()

        if self.current == "=":
            root.add(Node("="))
            self.next()
            root.add(
                self.expression()
            )

        self.match(";")
        return root

    def assignment(self):
        root = Node("ASSIGN")
        var = self.current
        root.add(
            Node(
                f"ID({var})"
            )
        )

        self.next()
        operators = [
            "=",
            "+=",
            "-=",
            "*=",
            "/="
        ]

        if self.current not in operators:
            self.error(
                "оператор присваивания"
            )
        op = self.current
        root.add(
            Node(op)
        )
        self.next()
        root.add(
            self.expression()
        )
        self.match(";")
        return root

    def if_statement(self):
        root = Node("IF")
        self.match("if")
        self.match("(")
        root.add(
            self.condition()
        )

        self.match(")")
        root.add(
            self.block()
        )

        if self.current == "else":
            else_node = Node("ELSE")
            self.next()
            else_node.add(
                self.block()
            )
            root.add(
                else_node
            )

        return root

    def return_statement(self):
        root = Node("RETURN")

        self.match("return")

        root.add(
            self.expression()
        )

        self.match(";")

        return root

    def condition(self):
        left = self.expression()

        operators = [
            "==",
            "!=",
            "<",
            ">",
            "<=",
            ">="
        ]

        if self.current not in operators:
            self.error(
                "оператор сравнения"
            )

        op = self.current

        self.next()

        right = self.expression()

        root = Node(op)

        root.add(left)
        root.add(right)

        return root

    def expression(self):
        left = self.term()

        while self.current in ["+", "-"]:
            op = self.current

            self.next()

            right = self.term()

            parent = Node(op)

            parent.add(left)
            parent.add(right)

            left = parent

        return left

    def term(self):
        left = self.factor()

        while self.current in ["*", "/", "%"]:
            op = self.current

            self.next()

            right = self.factor()

            parent = Node(op)

            parent.add(left)
            parent.add(right)

            left = parent

        return left

    def factor(self):

        if self.current == "-":
            self.next()
            root = Node("NEG")
            root.add(
                self.factor()
            )

            return root

        if self.is_identifier():
            node = Node(
                f"ID({self.current})"
            )
            self.next()
            return node

        if self.is_number():
            node = Node(
                f"NUM({self.current})"
            )
            self.next()
            return node

        if self.current == "(":
            self.next()
            node = self.expression()
            self.match(")")
            return node

        self.error("выражение")


def main():
    parser = Parser()
    tree = parser.program()
    print("ДЕРЕВО РАЗБОРА")
    tree.print_tree()


if __name__ == "__main__":
    main()