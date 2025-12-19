from math import erfc
from scipy.special import gammaincc


# оптимизированные функции
def frequency_bitwise_test_opt(data: str) -> float:
    """
    Оптимизация: используем count вместо цикла
    """
    n = len(data)
    count_ones = data.count('1')
    count_zeros = n - count_ones

    s = count_ones - count_zeros
    s = s / (n ** 0.5)

    return erfc(abs(s / (2 ** 0.5)))


def consecutive_running_bits_test_opt(data: str) -> float:
    """
    Оптимизация: count для единиц + оптимизированный подсчет переходов
    """
    n_len = len(data)
    s_ones = data.count('1')  # Ускорение
    zeta = s_ones / n_len

    if not (abs(zeta - 0.5) < (2 / n_len ** 0.5)):
        return 0.0

    # Считаем переходы 0->1 или 1->0
    # Это все еще цикл, но без лишних проверок
    v = 0
    for i in range(n_len - 1):
        if data[i] != data[i + 1]:
            v += 1

    return erfc(abs(v - 2 * n_len * zeta * (1 - zeta)) / (
                2 * (2 * n_len) ** 0.5 * zeta * (1 - zeta)))


def longest_sequence_test_opt(data: str) -> float:
    """
    Оптимизация: Избавляемся от создания огромного списка блоков [data[i:i+8]...]
    Работаем с индексами.
    """
    v_counts = [0, 0, 0, 0]
    m_block_size = 8
    n_len = len(data)
    n_blocks = n_len // m_block_size

    PI = [0.2148, 0.3672, 0.2305, 0.1875]

    for i in range(n_blocks):
        # Берем срез только одного маленького блока, а не всех сразу
        start = i * m_block_size
        block = data[start: start + m_block_size]

        max_run = 0
        current_run = 0

        # Для блока длиной 8 этот цикл очень быстрый
        for bit in block:
            if bit == '1':
                current_run += 1
            else:
                if current_run > max_run:
                    max_run = current_run
                current_run = 0
        if current_run > max_run:
            max_run = current_run

        if max_run <= 1:
            v_counts[0] += 1
        elif max_run == 2:
            v_counts[1] += 1
        elif max_run == 3:
            v_counts[2] += 1
        elif max_run >= 4:
            v_counts[3] += 1

    chi_squared_obs = 0
    for i in range(4):
        chi_squared_obs += (v_counts[i] - n_blocks * PI[i]) ** 2 / (
                    n_blocks * PI[i])

    return gammaincc(3.0 / 2.0, chi_squared_obs / 2.0)
