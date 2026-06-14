import time
import random

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

def height_recursive(root):
    if root is None:
        return 0
    return 1 + max(height_recursive(root.left), height_recursive(root.right))

def height_iterative(root):
    if root is None:
        return 0

    queue = [root]
    height = 0

    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.pop(0)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        height += 1

    return height

def generate_tree(n):
    root = None
    for _ in range(n):
        value = random.randint(0, 100000)
        root = insert(root, value)
    return root

def test():
    sizes = [100, 500, 1000, 2000, 5000]

    for n in sizes:
        root = generate_tree(n)

        start = time.time()
        h1 = height_recursive(root)
        t1 = time.time() - start

        start = time.time()
        h2 = height_iterative(root)
        t2 = time.time() - start

        print(f"n = {n}")
        print(f"через рекурсию = {h1}, время = {t1:.6f}")
        print(f"без рекурсии (итеративным способом) = {h2}, время = {t2:.6f}")

if __name__ == "__main__":
    test()