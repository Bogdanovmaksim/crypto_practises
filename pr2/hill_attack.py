"""
Криптоанализ шифра Хилла.
Атака на основе известного открытого текста
"""

import numpy as np

from main import (
    ALPHABET, M,
    text_to_numbers, pad_text,
    matrix_mod_inv, hill_decrypt
)
from crypto_utils import format_matrix, choose, input_text, input_block_size



#  Атака на шифр Хилла


def hill_known_plaintext_attack(plaintext, ciphertext, n):
    """
    Восстанавливает ключевую матрицу K шифра Хилла.
    """
    p_nums = pad_text(text_to_numbers(plaintext), n)
    c_nums = pad_text(text_to_numbers(ciphertext), n)

    needed = n * n
    if len(p_nums) < needed or len(c_nums) < needed:
        raise ValueError(
            f"Недостаточно текста: нужно минимум {needed} символов "
            f"(n²={n}²), получено P={len(p_nums)}, C={len(c_nums)}"
        )

    P = np.zeros((n, n), dtype=int)
    C = np.zeros((n, n), dtype=int)
    for i in range(n):
        P[:, i] = p_nums[i * n:(i + 1) * n]
        C[:, i] = c_nums[i * n:(i + 1) * n]

    P = np.mod(P, M).astype(int)
    C = np.mod(C, M).astype(int)

    print(f"\n  Матрица открытого текста P ({n}×{n}):")
    print(format_matrix(P))
    print(f"  Матрица шифртекста C ({n}×{n}):")
    print(format_matrix(C))

    try:
        P_inv = matrix_mod_inv(P, M)
    except ValueError:
        raise ValueError(
            "Матрица P необратима по mod 26.\n"
            "  Попробуйте другой набор открытого текста."
        )

    print(f"  P⁻¹ (mod {M}):")
    print(format_matrix(P_inv))

    K = np.mod(C @ P_inv, M).astype(int)
    print(f"  ✓ Восстановленный ключ K = C · P⁻¹ (mod {M}):")
    print(format_matrix(K))

    return K

def interactive_hill_attack():
    """Интерактивная атака на шифр Хилла."""
    n = input_block_size()
    print(f"  Нужно минимум {n * n} символов открытого текста и шифртекста.\n")

    plaintext = input_text("  Известный открытый текст: ")
    if not plaintext:
        print("  Текст не содержит букв A-Z")
        return

    ciphertext = input_text("  Соответствующий шифртекст: ")
    if not ciphertext:
        print("  Текст не содержит букв A-Z")
        return

    try:
        K = hill_known_plaintext_attack(plaintext, ciphertext, n)

        extra = input_text("\n  Шифртекст для расшифровки найденным ключом (или Enter): ")
        if extra:
            decrypted = hill_decrypt(extra, K)
            print(f"  Расшифровано: {decrypted}")

    except ValueError as e:
        print(f"\n  ✗ Ошибка: {e}")


# Меню

def main():
    print("  КРИПТОАНАЛИЗ ШИФРА ХИЛЛА")
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
            interactive_hill_attack()


if __name__ == "__main__":
    main()