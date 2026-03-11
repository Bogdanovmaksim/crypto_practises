# файл: cryptanalysis_final.py
from main import alphabet, modinv


def affine_recurrent_cryptanalysis():
    """
    Криптоанализ аффинного рекуррентного шифра
    """
    print("КРИПТОАНАЛИЗ АФФИННОГО РЕКУРРЕНТНОГО ШИФРА")
    print()

    # Ввод данных
    ciphertext = input("Введите зашифрованный текст: ").upper()
    known_plaintext = input("Введите известный открытый текст: ").upper()

    # Проверки
    if len(known_plaintext) < 4:
        print("Ошибка: нужно минимум 4 символа!")
        return

    if len(known_plaintext) > len(ciphertext):
        print("Ошибка: известный текст длиннее шифротекста!")
        return


    pairs = []
    for i in range(len(known_plaintext)):
        if known_plaintext[i] in alphabet and ciphertext[i] in alphabet:
            X = alphabet.index(known_plaintext[i])
            Y = alphabet.index(ciphertext[i])
            pairs.append((X, Y))
        else:
            print(f"Ошибка: символ '{known_plaintext[i]}' или '{ciphertext[i]}' не в алфавите")
            return

    print(f"\nИзвестные пары (X,Y) - всего {len(pairs)} символов:")
    for i, (X, Y) in enumerate(pairs[:10]):
        print(f"  {i}: {known_plaintext[i]}({X}) -> {ciphertext[i]}({Y})")
    if len(pairs) > 10:
        print(f"  ... и еще {len(pairs) - 10} символов")

    print("\nПОИСК КЛЮЧЕЙ")
    print("Перебираем возможные комбинации a1,b1,a2,b2...")

    solutions = []
    checked = 0

    for a1 in range(1, 26, 2):
        if modinv(a1) is None:
            continue

        for b1 in range(26):
            # Проверяем первую позицию
            if (a1 * pairs[0][0] + b1) % 26 != pairs[0][1]:
                continue

            for a2 in range(1, 26, 2):
                if modinv(a2) is None:
                    continue

                for b2 in range(26):
                    checked += 1

                    if (a2 * pairs[1][0] + b2) % 26 != pairs[1][1]:
                        continue

                    valid = True
                    a_prev2, b_prev2 = a1, b1
                    a_prev1, b_prev1 = a2, b2

                    # Проверяем все позиции от 2 до конца
                    for i in range(2, len(pairs)):
                        # Вычисляем ключ для текущей позиции
                        a_curr = (a_prev1 * a_prev2) % 26
                        b_curr = (b_prev1 + b_prev2) % 26

                        if (a_curr * pairs[i][0] + b_curr) % 26 != pairs[i][1]:
                            valid = False
                            break

                        a_prev2, a_prev1 = a_prev1, a_curr
                        b_prev2, b_prev1 = b_prev1, b_curr

                    if valid:
                        solutions.append({
                            'a1': a1, 'b1': b1,
                            'a2': a2, 'b2': b2
                        })

                        # Выводим прогресс
                        print(f"  Найдено решение: a1={a1}, b1={b1}, a2={a2}, b2={b2}")

    print(f"\nПроверено комбинаций: {checked}")
    print(f"Найдено решений: {len(solutions)}")

    if len(solutions) == 0:
        print("\nРешений не найдено!")
        print("Возможные причины:")
        print("1. Неправильно указан известный текст")
        print("2. Это не аффинный рекуррентный шифр")
        return

    if len(solutions) == 1:
        print("НАЙДЕНЫ ТОЧНЫЕ КЛЮЧИ!")
        sol = solutions[0]
        print(f"a1 = {sol['a1']}, b1 = {sol['b1']}")
        print(f"a2 = {sol['a2']}, b2 = {sol['b2']}")

        # Расшифровка всего текста
        if len(ciphertext) > 0:
            print("РАСШИФРОВКА ВСЕГО ТЕКСТА")

            try:
                from main import affine_recurrent_decrypt
                decrypted = affine_recurrent_decrypt(ciphertext, sol['a1'], sol['b1'], sol['a2'], sol['b2'])
                print(f"\nЗашифрованный текст: {ciphertext}")
                print(f"Расшифрованный текст: {decrypted}")


                # Проверяем, что известная часть совпадает
                known_part = decrypted[:len(known_plaintext)]
                if known_part == known_plaintext:
                    print(f"✓ Известная часть совпадает: '{known_part}'")
                else:
                    print(f"✗ Проблема! Ожидалось '{known_plaintext}', получено '{known_part}'")

            except ImportError:
                print(f"\nИспользуйте функцию из main.py для расшифровки")
    else:
        print(f"НАЙДЕНО {len(solutions)} РЕШЕНИЙ")

        # Показываем все решения
        for i, sol in enumerate(solutions):
            print(f"\nВариант {i + 1}: a1={sol['a1']:2d}, b1={sol['b1']:2d}, a2={sol['a2']:2d}, b2={sol['b2']:2d}")

        print(f"\nНужно больше известного текста для определения решения")


        print("\n" + "=" * 50)
        print("ПРИМЕР РАСШИФРОВКИ (первым решением)")
        print("=" * 50)

        try:
            from main import affine_recurrent_decrypt
            sol = solutions[0]
            decrypted = affine_recurrent_decrypt(ciphertext, sol['a1'], sol['b1'], sol['a2'], sol['b2'])
            print(f"Текст: {decrypted[:100]}{'...' if len(decrypted) > 100 else ''}")
        except:
            pass


# Запуск
if __name__ == "__main__":
    affine_recurrent_cryptanalysis()
