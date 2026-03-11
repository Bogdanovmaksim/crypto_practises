"""
Криптоанализ рекуррентного шифра Хилла.
Атака на основе известного открытого текста
"""

import numpy as np
from itertools import product

from main import (
    ALPHABET, M,
    text_to_numbers, numbers_to_text, pad_text,
    matrix_mod_inv, generate_keys, recur_hill_decrypt
)
from crypto_utils import format_matrix, choose, input_text, input_block_size

#  Вспомогательные функции

def blocks_from_text(nums, n):
    """Разбивает список чисел на блоки-столбцы размера n."""
    return [np.array(nums[i * n:(i + 1) * n], dtype=int) for i in range(len(nums) // n)]


def solve_key_from_block(p_block, c_block, n):
    equations = []
    for i in range(n):
        # c_block[i] = sum(K[i][j] * p_block[j] for j in range(n)) mod 26
        equations.append((p_block.copy(), c_block[i]))
    return equations


def solve_row(equations, n):
    if len(equations) >= n:

        A = np.zeros((len(equations), n), dtype=int)
        b = np.zeros(len(equations), dtype=int)
        for idx, (p_vec, c_val) in enumerate(equations):
            A[idx] = p_vec
            b[idx] = c_val


        A_sq = A[:n]
        b_sq = b[:n]

        try:
            A_inv = matrix_mod_inv(A_sq, M)
            row = np.mod(A_inv @ b_sq, M).astype(int)

            for p_vec, c_val in equations:
                if np.mod(np.dot(row, p_vec), M) != c_val:
                    return None
            return row
        except ValueError:
            pass

    if n <= 3:
        solutions = []
        for combo in product(range(M), repeat=n):
            k = np.array(combo, dtype=int)
            valid = True
            for p_vec, c_val in equations:
                if np.mod(np.dot(k, p_vec), M) != c_val:
                    valid = False
                    break
            if valid:
                solutions.append(k)
        return solutions if solutions else None

    return None

def recur_hill_known_plaintext_attack(plaintext, ciphertext, n):
    """
    Восстанавливает K1 и K2 рекуррентного шифра Хилла.
    """
    p_nums = pad_text(text_to_numbers(plaintext), n)
    c_nums = pad_text(text_to_numbers(ciphertext), n)

    num_blocks = len(p_nums) // n
    p_blocks = blocks_from_text(p_nums, n)
    c_blocks = blocks_from_text(c_nums, n)

    min_blocks = max(2 * n, 4)
    if num_blocks < min_blocks:
        raise ValueError(
            f"Недостаточно текста: нужно минимум {min_blocks} блоков "
            f"({min_blocks * n} символов), получено {num_blocks} блоков."
        )

    print(f"\n  Всего блоков: {num_blocks}")
    print(f"  Используем блоки 0..{num_blocks - 1}")
    print(f"\n  ── Шаг 1: Восстановление K1 ──")
    print(f"  Из блока 0: C0 = K1 · P0")
    print(f"    P0 = {p_blocks[0]}")
    print(f"    C0 = {c_blocks[0]}")

    k1_row_equations = []
    for i in range(n):
        k1_row_equations.append([(p_blocks[0], c_blocks[0][i])])

    print(f"\n  ── Шаг 2: Восстановление K2 ──")
    print(f"  Из блока 1: C1 = K2 · P1")
    print(f"    P1 = {p_blocks[1]}")
    print(f"    C1 = {c_blocks[1]}")

    k2_row_equations = []
    for i in range(n):
        k2_row_equations.append([(p_blocks[1], c_blocks[1][i])])

    print(f"\n  ── Шаг 3: Перебор с проверкой на блоках 2..{num_blocks - 1} ──")

    k1_candidates = []
    for i in range(n):
        result = solve_row(k1_row_equations[i], n)
        if result is None:
            raise ValueError(f"Не удалось найти строку {i} ключа K1")
        if isinstance(result, np.ndarray):
            k1_candidates.append([result])
        else:
            k1_candidates.append(result)

    k2_candidates = []
    for i in range(n):
        result = solve_row(k2_row_equations[i], n)
        if result is None:
            raise ValueError(f"Не удалось найти строку {i} ключа K2")
        if isinstance(result, np.ndarray):
            k2_candidates.append([result])
        else:
            k2_candidates.append(result)


    print(f"  Кандидатов K1: {' × '.join(str(len(c)) for c in k1_candidates)} "
          f"= {np.prod([len(c) for c in k1_candidates])} комбинаций строк")
    print(f"  Кандидатов K2: {' × '.join(str(len(c)) for c in k2_candidates)} "
          f"= {np.prod([len(c) for c in k2_candidates])} комбинаций строк")

    found = False
    K1_result = None
    K2_result = None

    k1_row_combos = list(product(*k1_candidates))
    k2_row_combos = list(product(*k2_candidates))

    total = len(k1_row_combos) * len(k2_row_combos)
    print(f"  Всего комбинаций для проверки: {total}")

    for k1_rows in k1_row_combos:
        K1 = np.array(k1_rows, dtype=int)

        for k2_rows in k2_row_combos:
            K2 = np.array(k2_rows, dtype=int)

            try:
                keys = generate_keys(K1, K2, num_blocks)
            except Exception:
                continue

            valid = True
            for idx in range(2, num_blocks):
                c_check = np.mod(keys[idx] @ p_blocks[idx], M).astype(int)
                if not np.array_equal(c_check, c_blocks[idx]):
                    valid = False
                    break

            if valid:
                K1_result = K1
                K2_result = K2
                found = True
                break
        if found:
            break

    if not found:
        raise ValueError(
            "Не удалось найти подходящую пару K1, K2.\n"
            "  Попробуйте другой набор открытого текста."
        )

    print(f"\n  ✓ Восстановленный ключ K1:")
    print(format_matrix(K1_result))
    print(f"  ✓ Восстановленный ключ K2:")
    print(format_matrix(K2_result))

    print(f"  ── Верификация на всех {num_blocks} блоках ──")
    keys = generate_keys(K1_result, K2_result, num_blocks)
    all_ok = True
    for i in range(num_blocks):
        c_check = np.mod(keys[i] @ p_blocks[i], M).astype(int)
        if not np.array_equal(c_check, c_blocks[i]):
            print(f"    ✗ Блок {i}: ожидалось {c_blocks[i]}, получено {c_check}")
            all_ok = False
    if all_ok:
        print(f"    ✓ Все {num_blocks} блоков совпадают!")

    return K1_result, K2_result

def interactive_recur_hill_attack():
    """Интерактивная атака на рекуррентный шифр Хилла."""
    n = input_block_size()
    min_chars = max(2 * n, 4) * n
    print(f"  Нужно минимум {min_chars} символов открытого текста и шифртекста.\n")

    plaintext = input_text("  Известный открытый текст: ")
    if not plaintext:
        print("  Текст не содержит букв A-Z")
        return

    ciphertext = input_text("  Соответствующий шифртекст: ")
    if not ciphertext:
        print("  Текст не содержит букв A-Z")
        return

    try:
        K1, K2 = recur_hill_known_plaintext_attack(plaintext, ciphertext, n)

        extra = input_text("\n  Шифртекст для расшифровки найденными ключами (или Enter): ")
        if extra:
            decrypted = recur_hill_decrypt(extra, K1, K2)
            print(f"  Расшифровано: {decrypted}")

    except ValueError as e:
        print(f"\n  ✗ Ошибка: {e}")

def main():
    print("  КРИПТОАНАЛИЗ РЕКУРРЕНТНОГО ШИФРА ХИЛЛА")
    print("  Атака на основе известного открытого текста")
    print(f"  Алфавит: A-Z ({M} символов)")

    while True:
        print()
        mode = choose("Выбор: ", {
            "1": "Сделать атаку",
            "0": "Выйти"
        })

        if mode == "0":
            print("Выход.")
            break
        elif mode == "1":
            interactive_recur_hill_attack()


if __name__ == "__main__":
    main()
