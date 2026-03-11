from main import alphabet, modinv, affine_decrypt


def affine_full_bruteforce(ciphertext):
    """
    ПОЛНЫЙ ПЕРЕБОР всех возможных ключей для аффинного шифра
    Выводит ВСЕ возможные варианты расшифровки
    """
    print("ПОЛНЫЙ ПЕРЕБОР АФФИННОГО ШИФРА")
    print(f"Исходный текст: {ciphertext}")
    print(f"Алфавит: {alphabet}")

    valid_a = []
    for a in range(1, 26):
        if modinv(a) is not None:
            valid_a.append(a)

    valid_b = range(26)

    total = len(valid_a) * len(valid_b)
    print(f"Всего комбинаций ключей: {total}")
    print(f"Возможные значения a: {valid_a}")
    print(f"Возможные значения b: 0-25")

    count = 0
    for a in valid_a:
        for b in valid_b:
            count += 1
            decrypted = affine_decrypt(ciphertext, a, b)

            print(f"\n[{count}/{total}] КЛЮЧ: a = {a:2d}, b = {b:2d}")
            print(f"РЕЗУЛЬТАТ: {decrypted}")

            # Если нашли что-то похожее на английский, выделяем
            if 'THE' in decrypted.upper() or 'AND' in decrypted.upper() or 'IS' in decrypted.upper():
                print("  >>> ВОЗМОЖНО АНГЛИЙСКИЙ ТЕКСТ! <<<")

    print("\n" + "=" * 80)
    print(f"ПЕРЕБОР ЗАВЕРШЕН. Всего проверено {count} комбинаций")
    print("=" * 80)


def affine_bruteforce_with_filter(ciphertext, keyword=None):
    """
    Полный перебор с возможностью фильтрации по ключевому слову
    """
    valid_a = [a for a in range(1, 26) if modinv(a) is not None]
    valid_b = range(26)

    total = len(valid_a) * len(valid_b)
    found = 0

    print(f"Полный перебор {total} комбинаций...")

    for a in valid_a:
        for b in valid_b:
            decrypted = affine_decrypt(ciphertext, a, b)

            if keyword:
                if keyword.upper() in decrypted.upper():
                    found += 1
                    print(f"\na={a:2d}, b={b:2d}: {decrypted}")
            else:
                # Иначе показываем все
                print(f"a={a:2d}, b={b:2d}: {decrypted}")

    if keyword:
        print(f"\nНайдено {found} совпадений с ключевым словом '{keyword}'")


# Самая простая версия - просто перебор и вывод всего
def simple_bruteforce(ciphertext):
    """Максимально простой полный перебор"""
    print("ПОЛНЫЙ ПЕРЕБОР АФФИННОГО ШИФРА")

    # Перебираем все a от 1 до 25
    for a in range(1, 26):
        # Проверяем, есть ли обратный элемент
        a_inv = modinv(a)
        if a_inv is None:
            continue

        # Перебираем все b от 0 до 25
        for b in range(26):
            # Дешифруем
            decrypted = affine_decrypt(ciphertext, a, b)

            # Выводим результат
            print(f"a={a:2d}, b={b:2d}: {decrypted}")


def get_user_input():
    """Функция для получения ввода от пользователя"""
    print("АФФИННЫЙ ШИФР - ПОЛНЫЙ ПЕРЕБОР")

    # Запрашиваем шифртекст у пользователя
    ciphertext = input("Введите зашифрованный текст: ").strip()

    if not ciphertext:
        print("Текст не может быть пустым. Использую тестовый текст.")
        ciphertext = "RCLLA CQTPM LMFM FM X RTLTKM UTLXTMT"

    print(f"\nШифртекст: {ciphertext}")
    print("\nВыберите режим:")
    print("1 - Простой полный перебор")
    print("2 - Полный перебор с выделением английских слов")
    print("3 - Перебор с фильтром по ключевому слову")

    try:
        choice = int(input("Ваш выбор (1-3): "))
    except ValueError:
        choice = 2

    return ciphertext, choice


def main():
    """Основная функция программы"""
    # Получаем ввод от пользователя
    ciphertext, choice = get_user_input()

    print("\n" + "=" * 80)

    if choice == 1:
        simple_bruteforce(ciphertext)
    elif choice == 3:
        keyword = input("Введите ключевое слово для фильтрации: ").strip()
        if keyword:
            affine_bruteforce_with_filter(ciphertext, keyword)
        else:
            print("Ключевое слово не введено. Использую обычный перебор.")
            affine_full_bruteforce(ciphertext)
    else:
        affine_full_bruteforce(ciphertext)

    while True:
        again = input("\nХотите расшифровать другой текст? (да/нет): ").strip().lower()
        if again in ['да', 'д', 'yes', 'y']:
            print("\n" * 2)
            main()
            break
        elif again in ['нет', 'н', 'no', 'n']:
            print("Программа завершена.")
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Проверьте, что файл main.py существует и содержит нужные функции.")