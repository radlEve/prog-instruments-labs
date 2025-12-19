import random
import time
from math import erfc
from scipy.special import gammaincc


def frequency_bitwise_test(data: str) -> float:
    """
    Частотный побитовый анализ
    """
    s = 0
    for i in data:
        if i == '0':
            s -= 1
        if i == '1':
            s += 1
    s = s / (len(data) ** 0.5)

    return erfc(abs(s / (2 ** 0.5)))


def consecutive_running_bits_test(data: str) -> float:
    """
    Тест на одинаковые подряд идущие биты
    """
    n_len = len(data)
    s_ones = 0
    for i in data:
        if i == '1':
            s_ones += 1
    zeta = s_ones / n_len

    if not (abs(zeta - 0.5) < (2 / n_len ** 0.5)):
        return 0.0

    v = 0
    for i in range(n_len - 1):
        if data[i] != data[i + 1]:
            v += 1

    return erfc(abs(v - 2 * n_len * zeta * (1 - zeta)) / (
                2 * (2 * n_len) ** 0.5 * zeta * (1 - zeta)))


def longest_sequence_test(data: str) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке
    """
    v_counts = [0, 0, 0, 0]
    m_block_size = 8
    n_blocks = len(data) / m_block_size

    blocks = [data[i:i + m_block_size] for i in
              range(0, len(data), m_block_size)]

    for block in blocks:
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
            else:
                max_run = max(current_run, max_run)
                current_run = 0
        max_run = max(current_run, max_run)

        if max_run <= 1:
            v_counts[0] += 1
        elif max_run == 2:
            v_counts[1] += 1
        elif max_run == 3:
            v_counts[2] += 1
        elif max_run >= 4:
            v_counts[3] += 1

    chi_squared_obs = 0
    for i in range(len(v_counts)):
        # PI - константы вероятностей для блоков длиной 8
        PI = [0.2148, 0.3672, 0.2305, 0.1875]
        chi_squared_obs += (v_counts[i] - n_blocks * PI[i]) ** 2 / (
                    n_blocks * PI[i])

    return gammaincc(3.0 / 2.0, chi_squared_obs / 2.0)


def generate_random_sequence(n):
    print(f"Generating sequence of {n} bits...")
    return "".join([str(random.randint(0, 1)) for _ in range(n)])


def main():
    N = 30_000_000      #размер данных

    data = generate_random_sequence(N)

    print("Starting tests...")
    start_time = time.time()

    # Запускаем тесты
    p_freq = frequency_bitwise_test(data)
    print(f"Frequency test done. Result: {p_freq}")

    p_runs = consecutive_running_bits_test(data)
    print(f"Runs test done. Result: {p_runs}")

    p_longest = longest_sequence_test(data)
    print(f"Longest sequence test done. Result: {p_longest}")

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()