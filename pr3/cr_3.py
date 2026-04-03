import itertools

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def decrypt_ciphertext_autokey(ciphertext, primer_key):
    """
    Дешифрование Виженера с автоключом по ШИФРТЕКСТУ.
    Ключ формируется как: [Начальный ключ] + [Шифротекст]
    """
    plaintext = ""

    key_stream = list(primer_key.upper()) + list(ciphertext.upper())

    for i, char in enumerate(ciphertext.upper()):
        if char in ALPHABET:
            c_idx = ALPHABET.index(char)
            k_idx = ALPHABET.index(key_stream[i])

            p_idx = (c_idx - k_idx) % len(ALPHABET)
            p_char = ALPHABET[p_idx]

            plaintext += p_char
        else:
            plaintext += char
            key_stream.insert(i, char)

    return plaintext


def attack_known_plaintext(ciphertext, known_start):
    """
    Атака на основе известного открытого текста.
    Мгновенно вычисляет начальный ключ по первым символам и определяет его истинную длину.
    """
    known_start = known_start.upper()
    raw_key = ""

    for i, p_char in enumerate(known_start):
        if i >= len(ciphertext):
            break

        c_char = ciphertext[i].upper()
        if c_char in ALPHABET and p_char in ALPHABET:
            c_idx = ALPHABET.index(c_char)
            p_idx = ALPHABET.index(p_char)

            k_idx = (c_idx - p_idx) % len(ALPHABET)
            raw_key += ALPHABET[k_idx]

    primer_key = raw_key
    for i in range(1, len(raw_key)):
        tail = raw_key[i:]
        if ciphertext.startswith(tail):
            primer_key = raw_key[:i]
            break

    print(f"\n[*] Угаданное начало: {known_start}")
    print(f"[*] Сырой вычисленный ключ: {raw_key}")
    print(f"[*] Истинный начальный ключ (Primer): {primer_key}")

    return decrypt_ciphertext_autokey(ciphertext, primer_key)


def brute_force_attack(ciphertext, max_key_length=3, dictionary=None):
    """
    Атака полным перебором (Brute-force) начального ключа.
    """
    print(f"\n[*] Начинаем перебор ключей до длины {max_key_length}...")
    best_results = []

    for length in range(1, max_key_length + 1):
        for key_tuple in itertools.product(ALPHABET, repeat=length):
            key = "".join(key_tuple)
            decrypted = decrypt_ciphertext_autokey(ciphertext, key)

            if dictionary:
                score = sum(1 for word in dictionary if word in decrypted)
                if score > 0:
                    best_results.append((score, key, decrypted))
            else:
                best_results.append((0, key, decrypted))

    best_results.sort(key=lambda x: x[0], reverse=True)
    return best_results[:5]


def main():
    print("Криптоанализ автоключа по ШИФРТЕКСТУ")

    while True:
        print("\nМеню действий:")
        print("1. Атака по известному началу текста (вычисление ключа)")
        print("2. Атака полным перебором ключа (Brute-force)")
        print("3. Выход")

        choice = input("Выберите действие (1-3): ").strip()

        if choice == '3':
            print("Завершение программы. До свидания!")
            break

        if choice not in ['1', '2']:
            print("Ошибка: Неверный выбор.")
            continue

        target_ciphertext = input("\nВведите зашифрованный текст: ").strip().upper()
        target_ciphertext = target_ciphertext.replace(" ", "")

        if not target_ciphertext:
            continue

        if choice == '1':
            guessed_word = input("Введите предполагаемое начало сообщения: ").strip().upper()
            recovered_text = attack_known_plaintext(target_ciphertext, guessed_word)
            print(f"[+] Результат расшифровки: {recovered_text}")

        elif choice == '2':
            try:
                max_len = int(input("Введите максимальную длину ключа для перебора (рекомендуется 1-4): ").strip())
            except ValueError:
                print("Ошибка: нужно ввести число.")
                continue

            dict_input = input("Введите слова для поиска через запятую (Enter для стандартного словаря):\n").strip()

            if dict_input:
                vocab = [w.strip().upper() for w in dict_input.split(',')]
            else:
                vocab = ["HELLO", "MEET", "ATTACK", "SECRET", "REPORT", "THE", "AND"]

            print(f"[*] Используемый словарь: {', '.join(vocab)}")
            results = brute_force_attack(target_ciphertext, max_key_length=max_len, dictionary=vocab)

            print("\n[+] Лучшие результаты перебора (топ-5):")
            found = False
            for score, key, text in results:
                if score > 0:
                    found = True
                    print(f"Ключ: {key:<6} | Совпадений: {score} | Текст: {text}")

            if not found:
                print("[-] Подходящих вариантов не найдено.")


if __name__ == "__main__":
    main()