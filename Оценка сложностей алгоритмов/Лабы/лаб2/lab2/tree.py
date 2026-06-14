import time
import random

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self.insert_recursive(self.root, value)

    def insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self.insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self.insert_recursive(node.right, value)


    def count_recursive(self, node=None):
        if node is None:
            return 0
        return 1 + self.count_recursive(node.left) + self.count_recursive(node.right)


    def count_iterative(self):
        if self.root is None:
            return 0

        count = 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            count += 1

            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return count


if __name__ == "__main__":
    """tree = BinaryTree()
    values = [8, 3, 10, 1, 6, 14, 4, 7, 13]
    for v in values:
        tree.insert(v)"""

    sizes = [100, 1000, 5000, 10000]
    for n in sizes:
        tree = BinaryTree()

        values = random.sample(range(n * 10), n)
        for v in values:
            tree.insert(v)

        start = time.time()
        tree.count_recursive(tree.root)
        rec_time = time.time() - start

        start = time.time()
        tree.count_iterative()
        iter_time = time.time() - start

        print(f"n={n}: рекурсивный={rec_time:.6f}, итеративный={iter_time:.6f}")


    print(f"Рекурсивный подсчет: {tree.count_recursive(tree.root)}")
    print(f"Нерекурсивный подсчет: {tree.count_iterative()}")