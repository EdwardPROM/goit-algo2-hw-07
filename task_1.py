import random
import time
from collections import OrderedDict

# Клас LRU Cache
class LRUCache:
    def __init__(self, capacity=1000):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# Функції без кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

# Функції з кешем
def range_sum_with_cache(array, L, R, cache):
    key = (L, R)
    cached_sum = cache.get(key)
    if cached_sum is not None:
        return cached_sum
    result = sum(array[L:R+1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value, cache):
    array[index] = value
    cache.cache.clear()  # Очищаємо кеш після оновлення

# Генерація масиву та запитів
N = 100_000
Q = 50_000

array = [random.randint(1, 1000) for _ in range(N)]

queries = []
for _ in range(Q):
    if random.random() < 0.5:
        L = random.randint(0, N-1)
        R = random.randint(L, N-1)
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, N-1)
        value = random.randint(1, 1000)
        queries.append(('Update', index, value))

# Тестування без кешу
array_copy_no_cache = array.copy()
start_time = time.time()

for query in queries:
    if query[0] == 'Range':
        _, L, R = query
        range_sum_no_cache(array_copy_no_cache, L, R)
    else:
        _, index, value = query
        update_no_cache(array_copy_no_cache, index, value)

time_no_cache = time.time() - start_time
print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")

# Тестування з кешем
array_copy_with_cache = array.copy()
cache = LRUCache(capacity=1000)

start_time = time.time()

for query in queries:
    if query[0] == 'Range':
        _, L, R = query
        range_sum_with_cache(array_copy_with_cache, L, R, cache)
    else:
        _, index, value = query
        update_with_cache(array_copy_with_cache, index, value, cache)

time_with_cache = time.time() - start_time
print(f"Час виконання з LRU-кешем: {time_with_cache:.2f} секунд")
