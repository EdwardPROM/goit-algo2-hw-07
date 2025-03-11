import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

# Фібоначчі з LRU Cache
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr

# Реалізація Splay Tree 
class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left_node = None
        self.right_node = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Вставка нового елемента в дерево."""
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert_node(key, value, self.root)

    def _insert_node(self, key, value, current_node):
        """Рекурсивна вставка елемента в дерево."""
        if key < current_node.key:
            if current_node.left_node:
                self._insert_node(key, value, current_node.left_node)
            else:
                current_node.left_node = Node(key, value, current_node)
                self._splay(current_node.left_node)
        elif key > current_node.key:
            if current_node.right_node:
                self._insert_node(key, value, current_node.right_node)
            else:
                current_node.right_node = Node(key, value, current_node)
                self._splay(current_node.right_node)
        else:
            # Оновлюємо значення, якщо ключ уже є, і робимо splay
            current_node.value = value
            self._splay(current_node)

    def find(self, key):
        """Пошук елемента в дереві із застосуванням сплаювання."""
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left_node
            elif key > node.key:
                node = node.right_node
            else:
                self._splay(node)
                return node.value  # Повертаємо значення, якщо знайшли
        return None

    def _splay(self, node):
        """Реалізація сплаювання для переміщення вузла до кореня."""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig-ситуація
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        """Права ротація вузла."""
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Ліва ротація вузла."""
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child

#Фібоначчі з Splay Tree
def fibonacci_splay(n, tree):
    cached = tree.find(n)
    if cached is not None:
        return cached

    if n < 2:
        tree.insert(n, n)
        return n

    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, val)
    return val

#Вимірювання часу
n_values = list(range(0, 951, 50))
lru_times = []
splay_times = []

for n in n_values:
    # Час для lru_cache
    fibonacci_lru.cache_clear() 
    lru_timer = timeit.timeit(lambda: fibonacci_lru(n), number=10)
    lru_times.append(lru_timer / 10)

    # Час для Splay Tree
    tree = SplayTree()
    splay_timer = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10)
    splay_times.append(splay_timer / 10)

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, marker='o', label='LRU Cache')
plt.plot(n_values, splay_times, marker='x', label='Splay Tree')

plt.title('Порівняння часу виконання для LRU Cache та Splay Tree')
plt.xlabel('Число Фібоначчі (n)')
plt.ylabel('Середній час виконання (секунди)')
plt.legend()
plt.grid(True)
plt.show()

# Таблиця результатів
print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)':<25}")
print('-' * 60)
for i in range(len(n_values)):
    print(f"{n_values[i]:<10}{lru_times[i]:<25.10f}{splay_times[i]:<25.10f}")
