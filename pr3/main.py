#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Практическая работа 3: Шифры гаммирования
Алфавит: A-Z (26 букв)
"""

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_SIZE = 26


def to_num(c):
    return ord(c) - ord('A')


def to_char(n):
    return chr((n % ALPHABET_SIZE) + ord('A'))


def prepare(text):
    return ''.join([c.upper() for c in text if c.upper() in ALPHABET])


# Повторение лозунга
def encrypt_repeating(plain, key):
    plain, key = prepare(plain), prepare(key)
    if not plain or not key: return ""
    result = ""
    for i in range(len(plain)):
        result += to_char((to_num(plain[i]) + to_num(key[i % len(key)])))
    return result


def decrypt_repeating(cipher, key):
    cipher, key = prepare(cipher), prepare(key)
    if not cipher or not key: return ""
    result = ""
    for i in range(len(cipher)):
        result += to_char((to_num(cipher[i]) - to_num(key[i % len(key)])))
    return result


# Самоключ по открытому тексту
def encrypt_autokey_plain(plain, key_char):
    plain = prepare(plain)
    key_char = prepare(key_char)
    if not plain or not key_char: return ""
    result = to_char((to_num(plain[0]) + to_num(key_char)))
    for i in range(1, len(plain)):
        result += to_char((to_num(plain[i]) + to_num(plain[i - 1])))
    return result


def decrypt_autokey_plain(cipher, key_char):
    cipher = prepare(cipher)
    key_char = prepare(key_char)
    if not cipher or not key_char: return ""
    result = to_char((to_num(cipher[0]) - to_num(key_char)))
    for i in range(1, len(cipher)):
        result += to_char((to_num(cipher[i]) - to_num(result[i - 1])))
    return result


# Самоключ по шифртексту
def encrypt_autokey_cipher(plain, key_char):
    plain = prepare(plain)
    key_char = prepare(key_char)
    if not plain or not key_char: return ""
    result = to_char((to_num(plain[0]) + to_num(key_char)))
    for i in range(1, len(plain)):
        result += to_char((to_num(plain[i]) + to_num(result[i - 1])))
    return result


def decrypt_autokey_cipher(cipher, key_char):
    cipher = prepare(cipher)
    key_char = prepare(key_char)
    if not cipher or not key_char: return ""
    result = to_char((to_num(cipher[0]) - to_num(key_char)))
    for i in range(1, len(cipher)):
        result += to_char((to_num(cipher[i]) - to_num(cipher[i - 1])))
    return result


if __name__ == "__main__":
    print("ШИФРЫ ГАММИРОВАНИЯ (A-Z)")
    print("1 - повторение лозунга")
    print("2 - самоключ по открытому тексту")
    print("3 - самоключ по шифртексту")

    mode = input("Выберите режим (1-3): ")
    action = input("Шифровать (1) или расшифровать (2)? ")
    text = input("Введите текст: ")
    key = input("Введите ключ: ")

    if mode == '1':
        if action == '1':
            print("Результат:", encrypt_repeating(text, key))
        else:
            print("Результат:", decrypt_repeating(text, key))
    elif mode == '2':
        if action == '1':
            print("Результат:", encrypt_autokey_plain(text, key))
        else:
            print("Результат:", decrypt_autokey_plain(text, key))
    else:
        if action == '1':
            print("Результат:", encrypt_autokey_cipher(text, key))
        else:
            print("Результат:", decrypt_autokey_cipher(text, key))