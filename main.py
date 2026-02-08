"""
Программа для шифрования/дешифрования подстановочных шифров:
1. Шифр простой замены
2. Аффинный шифр
3. Аффинный рекуррентный шифр
"""

import random
import math
from typing import Tuple, List, Optional


class SimpleSubstitutionCipher:
    """Шифр простой замены"""

    def __init__(self, alphabet: str = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"):
        """Инициализация с алфавитом (по умолчанию русский 33 буквы)"""
        self.alphabet = alphabet
        self.char_to_idx = {ch: i for i, ch in enumerate(alphabet)}
        self.idx_to_char = {i: ch for i, ch in enumerate(alphabet)}
        self.m = len(alphabet)

    def generate_key(self) -> str:
        """Генерация случайного ключа-подстановки"""
        shuffled = list(self.alphabet)
        random.shuffle(shuffled)
        return ''.join(shuffled)

    def validate_key(self, key: str) -> bool:
        """Проверка корректности ключа"""
        if len(key) != self.m:
            return False
        if set(key) != set(self.alphabet):
            return False
        return True

    def encrypt(self, plaintext: str, key: str) -> str:
        """Шифрование текста"""
        if not self.validate_key(key):
            raise ValueError(f"Некорректный ключ. Должен быть перестановкой алфавита '{self.alphabet}'")

        ciphertext = []
        for char in plaintext.upper():
            if char in self.char_to_idx:
                idx = self.char_to_idx[char]
                ciphertext.append(key[idx])
            else:
                ciphertext.append(char)  # Неалфавитные символы остаются без изменений
        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str, key: str) -> str:
        """Расшифрование текста"""
        if not self.validate_key(key):
            raise ValueError(f"Некорректный ключ. Должен быть перестановкой алфавита '{self.alphabet}'")

        # Создаем обратное отображение
        key_reverse = {key_char: orig_char for orig_char, key_char in zip(self.alphabet, key)}

        plaintext = []
        for char in ciphertext.upper():
            if char in key_reverse:
                plaintext.append(key_reverse[char])
            else:
                plaintext.append(char)
        return ''.join(plaintext)


class AffineCipher:
    """Аффинный шифр"""

    def __init__(self, alphabet: str = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"):
        """Инициализация с алфавитом"""
        self.alphabet = alphabet
        self.char_to_idx = {ch: i for i, ch in enumerate(alphabet)}
        self.idx_to_char = {i: ch for i, ch in enumerate(alphabet)}
        self.m = len(alphabet)

    def mod_inverse(self, a: int, m: int) -> Optional[int]:
        """Нахождение мультипликативного обратного a^(-1) mod m"""
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    def generate_key(self) -> Tuple[int, int]:
        """Генерация случайного ключа (α, β)"""
        # Находим все числа, взаимно простые с m
        valid_alphas = [i for i in range(1, self.m) if math.gcd(i, self.m) == 1]
        alpha = random.choice(valid_alphas)
        beta = random.randint(0, self.m - 1)
        return alpha, beta

    def validate_key(self, alpha: int, beta: int) -> bool:
        """Проверка корректности ключа"""
        if not (0 <= alpha < self.m and 0 <= beta < self.m):
            return False
        if math.gcd(alpha, self.m) != 1:
            return False
        return True

    def encrypt(self, plaintext: str, alpha: int, beta: int) -> str:
        """Шифрование текста"""
        if not self.validate_key(alpha, beta):
            raise ValueError(f"Некорректный ключ. α={alpha} должно быть взаимно простым с m={self.m}")

        ciphertext = []
        for char in plaintext.upper():
            if char in self.char_to_idx:
                x = self.char_to_idx[char]
                y = (alpha * x + beta) % self.m
                ciphertext.append(self.idx_to_char[y])
            else:
                ciphertext.append(char)
        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str, alpha: int, beta: int) -> str:
        """Расшифрование текста"""
        if not self.validate_key(alpha, beta):
            raise ValueError(f"Некорректный ключ. α={alpha} должно быть взаимно простым с m={self.m}")

        # Находим обратное к alpha
        alpha_inv = self.mod_inverse(alpha, self.m)
        if alpha_inv is None:
            raise ValueError(f"Не существует обратного к α={alpha} по модулю {self.m}")

        plaintext = []
        for char in ciphertext.upper():
            if char in self.char_to_idx:
                y = self.char_to_idx[char]
                x = (alpha_inv * (y - beta)) % self.m
                plaintext.append(self.idx_to_char[x])
            else:
                plaintext.append(char)
        return ''.join(plaintext)


class AffineRecurrentCipher:
    """Аффинный рекуррентный шифр"""

    def __init__(self, alphabet: str = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"):
        """Инициализация с алфавитом"""
        self.alphabet = alphabet
        self.char_to_idx = {ch: i for i, ch in enumerate(alphabet)}
        self.idx_to_char = {i: ch for i, ch in enumerate(alphabet)}
        self.m = len(alphabet)

    def mod_inverse(self, a: int, m: int) -> Optional[int]:
        """Нахождение мультипликативного обратного"""
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    def generate_keys(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Генерация двух начальных ключей"""
        valid_alphas = [i for i in range(1, self.m) if math.gcd(i, self.m) == 1]

        alpha1 = random.choice(valid_alphas)
        beta1 = random.randint(0, self.m - 1)

        alpha2 = random.choice(valid_alphas)
        beta2 = random.randint(0, self.m - 1)

        return (alpha1, beta1), (alpha2, beta2)

    def validate_keys(self, key1: Tuple[int, int], key2: Tuple[int, int]) -> bool:
        """Проверка корректности начальных ключей"""
        alpha1, beta1 = key1
        alpha2, beta2 = key2

        if not (0 <= alpha1 < self.m and 0 <= beta1 < self.m):
            return False
        if not (0 <= alpha2 < self.m and 0 <= beta2 < self.m):
            return False
        if math.gcd(alpha1, self.m) != 1 or math.gcd(alpha2, self.m) != 1:
            return False
        return True

    def generate_key_sequence(self, key1: Tuple[int, int], key2: Tuple[int, int], length: int) -> List[Tuple[int, int]]:
        """Генерация последовательности ключей по рекуррентной формуле"""
        if not self.validate_keys(key1, key2):
            raise ValueError("Некорректные начальные ключи")

        alpha1, beta1 = key1
        alpha2, beta2 = key2

        keys = [(alpha1, beta1), (alpha2, beta2)]

        for i in range(2, length):
            alpha_prev1, beta_prev1 = keys[i - 1]
            alpha_prev2, beta_prev2 = keys[i - 2]

            alpha_i = (alpha_prev1 * alpha_prev2) % self.m
            beta_i = (beta_prev1 + beta_prev2) % self.m

            # Проверяем, что alpha_i взаимно прост с m
            if math.gcd(alpha_i, self.m) != 1:
                # Если нет, корректируем (например, добавляем 1)
                alpha_i = (alpha_i + 1) % self.m
                while math.gcd(alpha_i, self.m) != 1 and alpha_i < self.m:
                    alpha_i = (alpha_i + 1) % self.m

            keys.append((alpha_i, beta_i))

        return keys

    def encrypt(self, plaintext: str, key1: Tuple[int, int], key2: Tuple[int, int]) -> str:
        """Шифрование текста"""
        # Оставляем только символы из алфавита для шифрования
        chars_to_encrypt = [ch for ch in plaintext.upper() if ch in self.char_to_idx]

        if len(chars_to_encrypt) == 0:
            return plaintext

        # Генерируем последовательность ключей
        keys = self.generate_key_sequence(key1, key2, len(chars_to_encrypt))

        ciphertext_chars = []
        char_index = 0

        for char in plaintext.upper():
            if char in self.char_to_idx:
                x = self.char_to_idx[char]
                alpha, beta = keys[char_index]
                y = (alpha * x + beta) % self.m
                ciphertext_chars.append(self.idx_to_char[y])
                char_index += 1
            else:
                ciphertext_chars.append(char)

        return ''.join(ciphertext_chars)

    def decrypt(self, ciphertext: str, key1: Tuple[int, int], key2: Tuple[int, int]) -> str:
        """Расшифрование текста"""
        # Оставляем только символы из алфавита для расшифрования
        chars_to_decrypt = [ch for ch in ciphertext.upper() if ch in self.char_to_idx]

        if len(chars_to_decrypt) == 0:
            return ciphertext

        # Генерируем ту же последовательность ключей
        keys = self.generate_key_sequence(key1, key2, len(chars_to_decrypt))

        plaintext_chars = []
        char_index = 0

        for char in ciphertext.upper():
            if char in self.char_to_idx:
                y = self.char_to_idx[char]
                alpha, beta = keys[char_index]

                # Находим обратное к alpha
                alpha_inv = self.mod_inverse(alpha, self.m)
                if alpha_inv is None:
                    raise ValueError(f"Не существует обратного к α={alpha} по модулю {self.m}")

                x = (alpha_inv * (y - beta)) % self.m
                plaintext_chars.append(self.idx_to_char[x])
                char_index += 1
            else:
                plaintext_chars.append(char)

        return ''.join(plaintext_chars)


def main():
    """Основная функция с консольным интерфейсом"""
    print("=" * 50)
    print("ПРОГРАММА ДЛЯ РАБОТЫ С ПОДСТАНОВОЧНЫМИ ШИФРАМИ")
    print("=" * 50)

    # Создаем экземпляры шифров
    simple_cipher = SimpleSubstitutionCipher()
    affine_cipher = AffineCipher()
    recurrent_cipher = AffineRecurrentCipher()

    while True:
        print("\n" + "=" * 50)
        print("МЕНЮ:")
        print("1. Шифр простой замены")
        print("2. Аффинный шифр")
        print("3. Аффинный рекуррентный шифр")
        print("0. Выход")

        try:
            choice = input("\nВыберите шифр (0-3): ").strip()

            if choice == "0":
                print("Выход из программы.")
                break

            if choice == "1":
                print("\n--- ШИФР ПРОСТОЙ ЗАМЕНЫ ---")
                mode = input("Выберите режим (1-шифрование, 2-расшифрование, 3-сгенерировать ключ): ").strip()

                if mode == "3":
                    key = simple_cipher.generate_key()
                    print(f"\nСгенерированный ключ: {key}")
                    print("Соответствие букв:")
                    for i, (orig, subst) in enumerate(zip(simple_cipher.alphabet, key)):
                        print(f"{orig} → {subst}", end="  ")
                        if (i + 1) % 5 == 0:
                            print()
                    continue

                text = input("Введите текст: ").strip()

                if mode == "1":
                    key_input = input("Введите ключ (33 русские буквы в произвольном порядке): ").strip().upper()
                    if len(key_input) != 33 or not simple_cipher.validate_key(key_input):
                        print("Некорректный ключ! Автоматическая генерация...")
                        key_input = simple_cipher.generate_key()
                        print(f"Сгенерированный ключ: {key_input}")

                    result = simple_cipher.encrypt(text, key_input)
                    print(f"\nШифртекст: {result}")

                elif mode == "2":
                    key_input = input("Введите ключ (33 русские буквы в произвольном порядке): ").strip().upper()
                    result = simple_cipher.decrypt(text, key_input)
                    print(f"\nОткрытый текст: {result}")

            elif choice == "2":
                print("\n--- АФФИННЫЙ ШИФР ---")
                mode = input("Выберите режим (1-шифрование, 2-расшифрование, 3-сгенерировать ключ): ").strip()

                if mode == "3":
                    alpha, beta = affine_cipher.generate_key()
                    print(f"\nСгенерированный ключ: α={alpha}, β={beta}")
                    print(f"Проверка: НОД({alpha}, {affine_cipher.m}) = {math.gcd(alpha, affine_cipher.m)}")
                    continue

                text = input("Введите текст: ").strip()

                try:
                    alpha = int(input("Введите α (должно быть взаимно простым с 33): ").strip())
                    beta = int(input("Введите β (0-32): ").strip())

                    if mode == "1":
                        result = affine_cipher.encrypt(text, alpha, beta)
                        print(f"\nШифртекст: {result}")
                    elif mode == "2":
                        result = affine_cipher.decrypt(text, alpha, beta)
                        print(f"\nОткрытый текст: {result}")

                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif choice == "3":
                print("\n--- АФФИННЫЙ РЕКУРРЕНТНЫЙ ШИФР ---")
                mode = input("Выберите режим (1-шифрование, 2-расшифрование, 3-сгенерировать ключи): ").strip()

                if mode == "3":
                    key1, key2 = recurrent_cipher.generate_keys()
                    print(f"\nСгенерированные ключи:")
                    print(f"k₁ = (α₁={key1[0]}, β₁={key1[1]})")
                    print(f"k₂ = (α₂={key2[0]}, β₂={key2[1]})")
                    continue

                text = input("Введите текст: ").strip()

                try:
                    print("Введите первый ключ k₁:")
                    alpha1 = int(input("  α₁: ").strip())
                    beta1 = int(input("  β₁: ").strip())

                    print("Введите второй ключ k₂:")
                    alpha2 = int(input("  α₂: ").strip())
                    beta2 = int(input("  β₂: ").strip())

                    key1 = (alpha1, beta1)
                    key2 = (alpha2, beta2)

                    if mode == "1":
                        result = recurrent_cipher.encrypt(text, key1, key2)
                        print(f"\nШифртекст: {result}")
                    elif mode == "2":
                        result = recurrent_cipher.decrypt(text, key1, key2)
                        print(f"\nОткрытый текст: {result}")

                except ValueError as e:
                    print(f"Ошибка: {e}")

            else:
                print("Неверный выбор. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()