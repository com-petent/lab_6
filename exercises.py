"""Запуск одного упражнения из раздела 10: python exercises.py 1"""

import argparse
from pathlib import Path
from random import Random

from main import binary_search, insertion_sort, linear_search, lower_bound, mean_time_ms, upper_bound


def trace_sort():
    # Ручная трассировка: показана обработанная часть после каждой вставки.
    values = [7, 4, 6, 2, 5]
    prefixes = [[4, 7], [4, 6, 7], [2, 4, 6, 7], [2, 4, 5, 6, 7]]
    print("Исходный список:", values)
    print(" i   key   Упорядоченный префикс")
    for i, prefix in enumerate(prefixes, start=1):
        assert insertion_sort(values[:i + 1]) == prefix
        print(f"{i:2}   {values[i]:3}   {prefix}")


def explain_invariant():
    print("""Инвариант: перед итерацией i первые i элементов упорядочены
и содержат те же значения, что и первые i элементов исходного списка.

Начало. При i = 1 префикс состоит из одного элемента и уже упорядочен.

Шаг. Сохраняем очередной элемент в key. Все элементы префикса,
которые больше key, сдвигаем на одну позицию вправо. Их взаимный
порядок сохраняется. Вставляем key в освободившуюся позицию:
слева значения ≤ key, справа в обработанной части — значения > key.
Теперь первые i + 1 элементов упорядочены, все значения сохранены.

Завершение. Когда обработан последний элемент, префикс охватывает
весь список. Пустой список и список из одного элемента уже упорядочены.""")


def trace_search():
    values = [2, 5, 8, 11, 15, 19, 23, 31]
    print("Список:", values, " (индексы с нуля)")
    # Шаги рассчитаны вручную. Пары границ включают оба конца.
    for target, steps, result in (
        (19, [(0, 3, 7), (4, 5, 7)], 5),
        (20, [(0, 3, 7), (4, 5, 7), (6, 6, 7)], -1),
    ):
        print(f"\ntarget = {target}\nleft  middle  right  значение  следующий шаг")
        for left, middle, right in steps:
            value = values[middle]
            if value < target:
                action = f"left = {middle + 1}"
            elif value > target:
                action = f"right = {middle - 1}"
            else:
                action = f"найден индекс {middle}"
            print(f"{left:4}  {middle:6}  {right:5}  {value:8}  {action}")
        assert binary_search(values, target) == result
        if result == -1:
            print("left = 6 > right = 5. Область пуста, результат: -1.")


def unsorted_input():
    values, target = [7, 1, 3, 5, 9], 7
    print(f"Список: {values}. Ищем {target}.\n")
    result = binary_search(values, target, verbose=True)
    correct = linear_search(values, target)
    print(f"\nБинарный поиск: {result}. Линейный поиск: индекс {correct}.")
    print("На первом шаге 3 < 7, поэтому поиск отбрасывает индексы 0–2.")
    print("Искомая семёрка находится на индексе 0 и теряется на этом шаге.")
    assert result == -1 and correct == 0


def duplicate_bounds():
    values, target = [1, 2, 2, 2, 5, 8], 2
    first = lower_bound(values, target)
    after = upper_bound(values, target)
    assert (first, after) == (1, 4)
    print(f"Список: {values}. Ищем границы для {target}.\n")
    print(f"lower_bound = {first}   Первый индекс со значением ≥ 2.")
    print(f"upper_bound = {after}   Первый индекс со значением > 2.")
    print(f"Срез [{first}:{after}] = {values[first:after]}. Всего совпадений: {after - first}.")


def plot_times():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rng = Random(42)
    sizes = [100, 1000, 5000, 10000]
    times = []
    for n in sizes:
        values = [rng.randint(-10**6, 10**6) for _ in range(n)]
        times.append(mean_time_ms(insertion_sort, values))

    # Нормируем теоретическую кривую по измерению при N = 5000.
    scale = times[2] / sizes[2] ** 2
    curve_n = range(0, sizes[-1] + 1, 50)
    ratio = times[-1] / times[-2]
    fig, ax = plt.subplots(figsize=(9, 5.6), layout="constrained")
    ax.plot(curve_n, [scale * n**2 for n in curve_n], "--", color="#526778",
            label="c · N² (по точке N = 5000)")
    ax.plot(sizes, times, "o", markersize=7, color="#9f371e", label="Измерения")
    ax.set(xlabel="Размер списка N, элементов", ylabel="Время сортировки, мс",
           title="Сортировка вставками на случайных данных")
    ax.set_xlim(-250, 10500)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.2)
    ax.legend(loc="upper left")
    ax.set_xlabel("Размер списка N, элементов\n\n"
                  f"При росте N с 5000 до 10 000 время выросло в {ratio:.2f} раза.\n"
                  "Для зависимости N² ожидается рост в 4 раза. Среднее по трём запускам.")
    output = Path(__file__).resolve().parent / "screenshots" / "06.png"
    output.parent.mkdir(exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)
    print("N       время, мс")
    for n, elapsed in zip(sizes, times):
        print(f"{n:<7} {elapsed:9.3f}")
    print(f"График: {output}")


def random_checks():
    rng = Random(42)
    print("Проверка insertion_sort на 20 случайных списках. Seed = 42.")
    print("Длины от 0 до 50, значения от −20 до 20 включительно.\n")
    for i in range(1, 21):
        values = [rng.randint(-20, 20) for _ in range(rng.randint(0, 50))]
        original = values.copy()
        result = insertion_sort(values)
        assert result == sorted(original), f"Ошибка сортировки в тесте {i}"
        assert values == original, f"Изменился исходный список в тесте {i}"
        if i % 5 == 0:
            print(f"Проверено списков: {i} из 20")
    print("\nВсе 20 проверок пройдены.")


EXERCISES = {
    1: ("Трассировка сортировки", trace_sort),
    2: ("Проверка инварианта", explain_invariant),
    3: ("Бинарный поиск на бумаге", trace_search),
    4: ("Поиск в неотсортированном списке", unsorted_input),
    5: ("Границы повторяющихся элементов", duplicate_bounds),
    6: ("Эксперимент со сложностью", plot_times),
    7: ("Контрольная проверка", random_checks),
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", type=int, choices=EXERCISES)
    number = parser.parse_args().number
    title, exercise = EXERCISES[number]
    print(f"Упражнение {number}. {title}\n")
    exercise()
