from random import Random
from time import perf_counter


def insertion_sort(values):
    """Возвращает отсортированную копию списка."""
    result = values.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def binary_search(sorted_values, target, verbose=False):
    """Ищет в списке по возрастанию. Возвращает индекс совпадения или -1."""
    left, right = 0, len(sorted_values) - 1
    while left <= right:
        middle = (left + right) // 2
        value = sorted_values[middle]
        if verbose:
            print(f"left={left}, middle={middle}, right={right}, value={value}")
        if value == target:
            return middle
        if value < target:
            left = middle + 1
        else:
            right = middle - 1
    if verbose:
        print(f"left={left}, right={right} — область поиска пуста")
    return -1


def linear_search(values, target):
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


def lower_bound(sorted_values, target):
    """Первый индекс со значением >= target или длина списка."""
    left, right = 0, len(sorted_values)
    while left < right:
        middle = (left + right) // 2
        if sorted_values[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left


def upper_bound(sorted_values, target):
    """Первый индекс со значением > target или длина списка."""
    left, right = 0, len(sorted_values)
    while left < right:
        middle = (left + right) // 2
        if sorted_values[middle] <= target:
            left = middle + 1
        else:
            right = middle
    return left


def check_algorithms():
    cases = [[], [7], [5, 1, 5, 2, 5], [1, 2, 3], [3, 2, 1], [-2, 0, -1, 4]]
    for values in cases:
        original = values.copy()
        ordered = insertion_sort(values)
        assert ordered == sorted(original)
        assert values == original and ordered is not values
        for search in (binary_search, linear_search):
            for target in original:
                index = search(ordered, target)
                assert 0 <= index < len(ordered) and ordered[index] == target
            assert search(ordered, 100) == -1

    repeats = [1, 2, 2, 2, 5]
    assert lower_bound(repeats, 2) == 1
    assert lower_bound(repeats, 3) == 4
    assert lower_bound(repeats, 9) == len(repeats)
    assert lower_bound(repeats, 0) == 0
    assert lower_bound([], 2) == 0
    print("Контрольные тесты пройдены.")


def run_queries(search, ordered, queries):
    for target in queries:
        search(ordered, target)


def mean_time_ms(function, *args):
    total = 0.0
    for _ in range(3):
        start = perf_counter()
        function(*args)
        total += perf_counter() - start
    return total * 1000 / 3


def benchmark():
    rng = Random(42)
    print("\nСортировка. Среднее время за 3 запуска, мс")
    print(f"{'N':>7}  {'Порядок':<16} {'Вставками':>12} {'sorted()':>12}")
    search_inputs = []
    for n in (100, 1000, 5000, 10000):
        data = [rng.randint(-10**6, 10**6) for _ in range(n)]
        ordered = insertion_sort(data)
        assert ordered == sorted(data)
        search_inputs.append(ordered)
        for label, values in (("случайный", data),
                              ("по возрастанию", ordered),
                              ("по убыванию", ordered[::-1])):
            insertion_ms = mean_time_ms(insertion_sort, values)
            builtin_ms = mean_time_ms(sorted, values)
            print(f"{n:7}  {label:<16} {insertion_ms:12.3f} {builtin_ms:12.3f}")

    # Для самого большого объёма исследуем только поиск.
    search_inputs.append(list(range(100000)))
    print("\nПоиск. Среднее время за 1000 запросов по трём запускам, мс")
    print(f"{'N':>7}  {'Линейный':>12} {'Бинарный':>12}")
    for ordered in search_inputs:
        queries = [rng.choice(ordered) for _ in range(1000)]
        linear_ms = mean_time_ms(run_queries, linear_search, ordered, queries)
        binary_ms = mean_time_ms(run_queries, binary_search, ordered, queries)
        print(f"{len(ordered):7}  {linear_ms:12.3f} {binary_ms:12.3f}")


if __name__ == "__main__":
    check_algorithms()
    example = [3, 8, 12, 17, 21, 25, 30]
    for target in (21, 20):
        print(f"\nПоиск {target} в {example}")
        index = binary_search(example, target, verbose=True)
        print(f"Результат: {index}")
    benchmark()
