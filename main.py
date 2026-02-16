
# Простая реализация подстановочных шифров

# Алфавит
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def simple_encrypt(text, key):
    """Шифрование простой заменой"""
    result = ''
    text = text.upper()
    key = key.upper()

    for char in text:
        if char in alphabet:
            pos = alphabet.index(char)
            result += key[pos]
        else:
            result += char
    return result

def simple_decrypt(text, key):
    """Дешифрование простой замены"""
    result = ''
    text = text.upper()
    key = key.upper()

    for char in text:
        if char in key:
            pos = key.index(char)
            result += alphabet[pos]
        else:
            result += char
    return result

# Функция для нахождения обратного элемента по модулю 26
def modinv(a):
    for i in range(26):
        if (a * i) % 26 == 1:
            return i
    return None

def affine_encrypt(text, a, b):
    """Аффинное шифрование: y = (a*x + b) mod 26"""
    result = ''
    text = text.upper()

    for char in text:
        if char in alphabet:
            x = alphabet.index(char)
            y = (a * x + b) % 26
            result += alphabet[y]
        else:
            result += char
    return result


def affine_decrypt(text, a, b):
    """Аффинное дешифрование: x = a^(-1)*(y - b) mod 26"""
    result = ''
    text = text.upper()

    a_inv = modinv(a)
    if a_inv is None:
        return "Ошибка: a не имеет обратного элемента!"

    for char in text:
        if char in alphabet:
            y = alphabet.index(char)
            x = (a_inv * (y - b)) % 26
            result += alphabet[x]
        else:
            result += char
    return result

def affine_recurrent_encrypt(text, a1, b1, a2, b2):
    """Аффинное рекуррентное шифрование"""
    result = ''
    text = text.upper()

    a_list = [a1, a2]
    b_list = [b1, b2]

    for i in range(len(text)):
        char = text[i]
        if char in alphabet:
            x = alphabet.index(char)

            if i < 2:
                y = (a_list[i] * x + b_list[i]) % 26
            else:
                a_new = (a_list[i - 1] * a_list[i - 2]) % 26
                b_new = (b_list[i - 1] + b_list[i - 2]) % 26
                a_list.append(a_new)
                b_list.append(b_new)
                y = (a_new * x + b_new) % 26

            result += alphabet[y]
        else:
            result += char
    return result


def affine_recurrent_decrypt(text, a1, b1, a2, b2):
    """Аффинное рекуррентное дешифрование"""
    result = ''
    text = text.upper()

    a_list = [a1, a2]
    b_list = [b1, b2]
    for i in range(len(text)):
        char = text[i]
        if char in alphabet:
            y = alphabet.index(char)
            if i < 2:
                a_inv = modinv(a_list[i])
                if a_inv is None:
                    return f"Ошибка: a{i + 1} не имеет обратного элемента!"
                x = (a_inv * (y - b_list[i])) % 26
            else:
                a_new = (a_list[i - 1] * a_list[i - 2]) % 26
                b_new = (b_list[i - 1] + b_list[i - 2]) % 26
                a_list.append(a_new)
                b_list.append(b_new)

                a_inv = modinv(a_new)
                if a_inv is None:
                    return f"Ошибка: ключ a={a_new} не имеет обратного элемента!"
                x = (a_inv * (y - b_new)) % 26

            result += alphabet[x]
        else:
            result += char
    return result

def main():
    print("ПРОГРАММА ДЛЯ ШИФРОВАНИЯ")
    print("1. Шифр простой замены")
    print("2. Аффинный шифр")
    print("3. Аффинный рекуррентный шифр")
    print("0. Выход")

    choice = input("Выберите шифр (0-3): ")

    if choice == '0':
        print("До свидания!")
        return

    elif choice == '1':
        print("\nШИФР ПРОСТОЙ ЗАМЕНЫ")
        mode = input("Режим (1 - шифрование, 2 - дешифрование): ")

        print("Алфавит: ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        key = input("Введите ключ (перемешанный алфавит из 26 букв): ")

        if len(key) != 26:
            print("Ошибка: ключ должен содержать 26 букв!")
            return

        text = input("Введите текст: ")

        if mode == '1':
            result = simple_encrypt(text, key)
            print(f"Результат: {result}")
        elif mode == '2':
            result = simple_decrypt(text, key)
            print(f"Результат: {result}")

    elif choice == '2':
        print("\nАФФИННЫЙ ШИФР")
        mode = input("Режим (1 - шифрование, 2 - дешифрование): ")

        try:
            a = int(input("Введите a (должно быть взаимно просто с 26): "))
            b = int(input("Введите b: "))

            if modinv(a) is None:
                print("Ошибка: a не взаимно просто с 26!")
                return

            text = input("Введите текст: ")

            if mode == '1':
                result = affine_encrypt(text, a, b)
                print(f"Результат: {result}")
            elif mode == '2':
                result = affine_decrypt(text, a, b)
                print(f"Результат: {result}")
        except:
            print("Ошибка: введите целые числа!")

    elif choice == '3':
        print("\nАФФИННЫЙ РЕКУРРЕНТНЫЙ ШИФР")
        mode = input("Режим (1 - шифрование, 2 - дешифрование): ")

        try:
            print("Первая ключевая пара:")
            a1 = int(input("a1: "))
            b1 = int(input("b1: "))

            print("Вторая ключевая пара:")
            a2 = int(input("a2: "))
            b2 = int(input("b2: "))

            if modinv(a1) is None or modinv(a2) is None:
                print("Ошибка: a1 и a2 должны быть взаимно просты с 26!")
                return

            text = input("Введите текст: ")

            if mode == '1':
                result = affine_recurrent_encrypt(text, a1, b1, a2, b2)
                print(f"Результат: {result}")
            elif mode == '2':
                result = affine_recurrent_decrypt(text, a1, b1, a2, b2)
                print(f"Результат: {result}")
        except:
            print("Ошибка: введите целые числа!")

if __name__ == "__main__":
    main()