import time
import random


from optimization import (
    frequency_bitwise_test as old_freq,
    consecutive_running_bits_test as old_runs,
    longest_sequence_test as old_long
)

from optimized import (
    frequency_bitwise_test_opt as new_freq,
    consecutive_running_bits_test_opt as new_runs,
    longest_sequence_test_opt as new_long
)


def generate_random_sequence(n):
    print(f"Generating sequence of {n} bits...")
    return "".join([str(random.randint(0, 1)) for _ in range(n)])


def run_tests(data, freq_func, runs_func, long_func, name):
    print(f"--- Запуск {name} версии ---")
    start = time.time()

    freq_func(data)
    runs_func(data)
    long_func(data)

    end = time.time()
    duration = end - start
    print(f"Готово. Время: {duration:.4f} сек\n")
    return duration


def main():
    N = 30_000_000

    print("Генерация данных...")
    data = generate_random_sequence(N)
    print("Данные готовы.\n")

    # 1. Запуск старой версии
    time_old = run_tests(data, old_freq, old_runs, old_long, "ОРИГИНАЛЬНОЙ")

    # 2. Запуск новой версии
    time_new = run_tests(data, new_freq, new_runs, new_long,
                         "ОПТИМИЗИРОВАННОЙ")

    # 3. Вывод итогов
    print("-" * 40)
    print("РЕЗУЛЬТАТЫ СРАВНЕНИЯ:")
    print(f"Оригинальная версия:   {time_old:.4f} сек")
    print(f"Оптимизированная версия: {time_new:.4f} сек")

    speedup = time_old / time_new
    diff = time_old - time_new

    print(f"Ускорение: {speedup:.2f}x")
    print(f"Оптимизированная версия быстрее на {diff:.4f} сек")
    print("-" * 40)


if __name__ == "__main__":
    main()
