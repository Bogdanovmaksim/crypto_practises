import itertools

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def decrypt_autokey(ciphertext, primer_key):
    """
    Дешифрование Виженера с автоключом.
    Открытый текст лавинообразно становится продолжением ключа.
    """
    plaintext = ""
    key_stream = list(primer_key.upper())

    for i, char in enumerate(ciphertext.upper()):
        if char in ALPHABET:
            c_idx = ALPHABET.index(char)
            k_idx = ALPHABET.index(key_stream[i])

            p_idx = (c_idx - k_idx) % len(ALPHABET)
            p_char = ALPHABET[p_idx]

            plaintext += p_char
            key_stream.append(p_char)
        else:
            plaintext += char
            key_stream.append(char)

    return plaintext


def attack_known_plaintext(ciphertext, known_start):
    """
    Атака на основе известного открытого текста.
    """
    known_start = known_start.upper()
    primer_key = ""

    for i, p_char in enumerate(known_start):
        # Если угаданное начало длиннее шифротекста - прерываем
        if i >= len(ciphertext):
            break

        c_char = ciphertext[i].upper()
        if c_char in ALPHABET and p_char in ALPHABET:
            c_idx = ALPHABET.index(c_char)
            p_idx = ALPHABET.index(p_char)

            k_idx = (c_idx - p_idx) % len(ALPHABET)
            primer_key += ALPHABET[k_idx]

    print(f"\n[*] Угаданное начало: {known_start}")
    print(f"[*] Вычисленный начальный ключ: {primer_key}")

    return decrypt_autokey(ciphertext, primer_key)


def brute_force_attack(ciphertext, max_key_length=3, dictionary=None):
    """
    Атака полным перебором (Brute-force) с проверкой по словарю.
    """
    print(f"\n[*] Начинаем перебор ключей до длины {max_key_length}...")
    best_results = []

    for length in range(1, max_key_length + 1):
        for key_tuple in itertools.product(ALPHABET, repeat=length):
            key = "".join(key_tuple)
            decrypted = decrypt_autokey(ciphertext, key)

            if dictionary:
                score = sum(1 for word in dictionary if word in decrypted)
                if score > 0:
                    best_results.append((score, key, decrypted))
            else:
                best_results.append((0, key, decrypted))

    best_results.sort(key=lambda x: x[0], reverse=True)
    return best_results[:5]


def main():
    print("Криптоанализ шифра Виженера с автоключом")

    while True:
        print("\nМеню действий:")
        print("1. Атака по известному началу текста")
        print("2. Атака полным перебором ключа (Brute-force)")
        print("3. Выход")

        choice = input("Выберите действие (1-3): ").strip()

        if choice == '3':
            print("Завершение программы. До свидания!")
            break

        if choice not in ['1', '2']:
            print("Ошибка: Неверный выбор. Пожалуйста, введите 1, 2 или 3.")
            continue

        target_ciphertext = input("\nВведите зашифрованный текст: ").strip().upper()
        # Убираем пробелы, чтобы анализировать чистый шифротекст
        target_ciphertext = target_ciphertext.replace(" ", "")

        if not target_ciphertext:
            print("Текст не может быть пустым.")
            continue

        if choice == '1':
            guessed_word = input("Введите предполагаемое начало сообщения (например, HELLO): ").strip().upper()
            recovered_text = attack_known_plaintext(target_ciphertext, guessed_word)
            print(f"[+] Результат расшифровки: {recovered_text}")

        elif choice == '2':
            try:
                max_len = int(input("Введите максимальную длину ключа для перебора (рекомендуется 3-4): ").strip())
            except ValueError:
                print("Ошибка: нужно ввести число.")
                continue

            dict_input = input(
                "Введите слова для поиска через запятую (нажмите Enter для стандартного словаря):\n").strip()

            if dict_input:
                vocab = [w.strip().upper() for w in dict_input.split(',')]
            else:
                vocab = ["HELLO", "GREETINGS", "ATTACK", "TOMORROW", "SECRET", "REPORT", "THE", "AND", "YOU"]

            print(f"[*] Используемый словарь: {', '.join(vocab)}")
            results = brute_force_attack(target_ciphertext, max_key_length=max_len, dictionary=vocab)

            print("\n[+] Лучшие результаты перебора (топ-5):")
            found = False
            for score, key, text in results:
                if score > 0:
                    found = True
                    print(f"Ключ: {key:<6} | Совпадений: {score} | Текст: {text}")

            if not found:
                print(
                    "[-] Подходящих вариантов не найдено. Попробуйте увеличить длину ключа или добавить другие слова в словарь.")


if __name__ == "__main__":
    main()