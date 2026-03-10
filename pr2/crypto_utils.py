"""
Вспомогательные функции для криптоанализа.
Импортируются в hill_attack.py и recur_hill_attack.py
"""

import numpy as np
from main import (
    ALPHABET, M,
    text_to_numbers, numbers_to_text, pad_text,
    matrix_mod_inv, hill_encrypt, hill_decrypt,
    generate_keys, recur_hill_encrypt, recur_hill_decrypt
)


def format_matrix(matrix):
    """Форматирует матрицу для красивого вывода."""
    lines = []
    for row in matrix:
        lines.append("    │ " + "  ".join(f"{x:3d}" for x in row) + " │")
    return "\n".join(lines) + "\n"


def choose(prompt, options):
    """Меню выбора."""
    for num, label in options.items():
        print(f"  {num} — {label}")
    while True:
        c = input(prompt).strip()
        if c in options:
            return c
        print("  Неверный выбор")


def input_text(prompt):
    """Ввод текста с фильтрацией только букв A-Z."""
    text = input(prompt).strip().upper()
    filtered = ''.join(c for c in text if c in ALPHABET)
    if not filtered:
        return None
    if len(filtered) != len(text):
        print(f"  Оставлены только буквы: {filtered}")
    return filtered


def input_block_size():
    """Ввод размера блока."""
    while True:
        try:
            n = int(input("\n  Размер блока n: "))
            if n < 1:
                raise ValueError
            return n
        except ValueError:
            print("  Введите положительное целое число")