import numpy as np
import math

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
M = 26


# Преобразования

def char_to_num(char):
    idx = ALPHABET.find(char.upper())
    if idx == -1:
        raise ValueError(f"Символ '{char}' не входит в алфавит")
    return idx


def text_to_numbers(text):
    return [char_to_num(c) for c in text if c.upper() in ALPHABET]


def numbers_to_text(numbers):
    return ''.join(ALPHABET[n % M] for n in numbers)


def pad_text(numbers, n):
    """Дополняет символом X до кратности n."""
    r = len(numbers) % n
    if r != 0:
        numbers += [ALPHABET.index('X')] * (n - r)
    return numbers


# Арифметика

def mod_inv(a, m=M):
    """Обратный элемент a по модулю m."""
    a = a % m
    if math.gcd(a, m) != 1:
        raise ValueError(f"Обратный элемент для {a} по модулю {m} не существует")

    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x

    _, x, _ = egcd(a, m)
    return x % m


def cofactor(matrix, i, j):
    """Алгебраическое дополнение элемента (i, j)."""
    minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
    if minor.size == 1:
        det_minor = int(minor[0, 0])
    else:
        det_minor = int(round(np.linalg.det(minor)))
    return ((-1) ** (i + j)) * det_minor


def matrix_mod_inv(matrix, m=M):
    """Обратная матрица по модулю m."""
    n = matrix.shape[0]
    det = int(round(np.linalg.det(matrix)))
    det_mod = det % m

    if math.gcd(det_mod, m) != 1:
        raise ValueError(f"Матрица необратима в Z_{m} (det={det_mod}, gcd({det_mod},{m}) ≠ 1)")

    det_inv = mod_inv(det_mod, m)

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            adj[j][i] = cofactor(matrix, i, j)

    return np.mod(det_inv * adj, m).astype(int)


def validate_key(matrix, name="K"):
    """Проверяет обратимость ключевой матрицы."""
    det = int(round(np.linalg.det(matrix))) % M
    if math.gcd(det, M) != 1:
        raise ValueError(f"Матрица {name}: det={det}, gcd({det},{M}) ≠ 1. Ключ необратим.")
    print(f"  ✓ {name} обратима в Z_{M} (det = {det})")


# Шифр Хилла

def hill_encrypt(text, key):
    n = key.shape[0]
    nums = pad_text(text_to_numbers(text), n)
    result = []
    for i in range(0, len(nums), n):
        block = np.array(nums[i:i + n])
        result.extend((key @ block) % M)
    return numbers_to_text(result)


def hill_decrypt(ciphertext, key):
    n = key.shape[0]
    nums = text_to_numbers(ciphertext)
    if len(nums) % n != 0:
        raise ValueError(f"Длина шифртекста не кратна блоку ({n})")
    key_inv = matrix_mod_inv(key)
    result = []
    for i in range(0, len(nums), n):
        block = np.array(nums[i:i + n])
        result.extend((key_inv @ block) % M)
    return numbers_to_text(result)


# Рекуррентный шифр Хилла

def generate_keys(k1, k2, count):

    keys = [np.mod(k1, M).astype(int), np.mod(k2, M).astype(int)]
    for i in range(2, count):
        keys.append(np.mod(keys[i - 1] @ keys[i - 2], M).astype(int))
    return keys[:count]


def recur_hill_encrypt(text, k1, k2):
    n = k1.shape[0]
    nums = pad_text(text_to_numbers(text), n)
    num_blocks = len(nums) // n
    keys = generate_keys(k1, k2, num_blocks)
    result = []
    for i in range(num_blocks):
        block = np.array(nums[i * n:(i + 1) * n])
        result.extend((keys[i] @ block) % M)
    return numbers_to_text(result)


def recur_hill_decrypt(ciphertext, k1, k2):
    n = k1.shape[0]
    nums = text_to_numbers(ciphertext)
    if len(nums) % n != 0:
        raise ValueError(f"Длина шифртекста не кратна блоку ({n})")
    num_blocks = len(nums) // n
    keys = generate_keys(k1, k2, num_blocks)
    result = []
    for i in range(num_blocks):
        block = np.array(nums[i * n:(i + 1) * n])
        key_inv = matrix_mod_inv(keys[i])
        result.extend((key_inv @ block) % M)
    return numbers_to_text(result)


# Ввод данных

def input_matrix(name, size):
    print(f"\n  Матрица {name} ({size}×{size}):")
    rows = []
    for i in range(size):
        while True:
            try:
                row = list(map(int, input(f"    Строка {i + 1}: ").split()))
                if len(row) != size:
                    print(f"    Нужно {size} чисел")
                    continue
                rows.append(row)
                break
            except ValueError:
                print("    Введите целые числа через пробел")
    matrix = np.array(rows, dtype=int)
    validate_key(matrix, name)
    return matrix


def choose(prompt, options):
    for num, label in options.items():
        print(f"  {num} — {label}")
    while True:
        c = input(prompt).strip()
        if c in options:
            return c
        print("  Неверный выбор")


# Меню

def main():
    print("=" * 45)
    print("  ШИФР ХИЛЛА И РЕКУРРЕНТНЫЙ ШИФР ХИЛЛА")
    print(f"  Алфавит: A-Z ({M} символов)")
    print("=" * 45)

    while True:
        print()
        cipher = choose("Выбор: ", {
            "1": "Шифр Хилла",
            "2": "Рекуррентный шифр Хилла",
            "0": "Выход"
        })

        if cipher == "0":
            print("Выход.")
            break

        while True:
            try:
                n = int(input("\nРазмер блока: "))
                if n < 1:
                    raise ValueError
                break
            except ValueError:
                print("Введите положительное целое число")

        try:
            if cipher == "1":
                key = input_matrix("K", n)
            else:
                key1 = input_matrix("K1", n)
                key2 = input_matrix("K2", n)
        except ValueError as e:
            print(f"\n  ✗ Ошибка: {e}")
            continue

        text = input("\nТекст: ")
        filtered = ''.join(c for c in text.upper() if c in ALPHABET)
        if not filtered:
            print("  Текст не содержит букв A-Z")
            continue
        if len(filtered) != len(text):
            print(f"  Оставлены только буквы: {filtered}")

        op = choose("Операция: ", {"1": "Зашифровать", "2": "Расшифровать"})

        try:
            if cipher == "1":
                result = hill_encrypt(filtered, key) if op == "1" else hill_decrypt(filtered, key)
            else:
                result = recur_hill_encrypt(filtered, key1, key2) if op == "1" \
                    else recur_hill_decrypt(filtered, key1, key2)

            label_in = "Открытый текст" if op == "1" else "Шифртекст"
            label_out = "Шифртекст" if op == "1" else "Открытый текст"
            print(f"\n  {label_in}:  {filtered}")
            print(f"  {label_out}: {result}")

        except ValueError as e:
            print(f"\n  ✗ Ошибка: {e}")


if __name__ == "__main__":
    main()