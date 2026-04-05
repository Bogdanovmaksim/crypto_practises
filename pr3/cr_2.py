from collections import Counter

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Эталонные частоты букв английского языка для оценки осмысленности текста
ENGLISH_FREQS = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00015,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074
}


def decrypt_autokey_1char(ciphertext, primer_char):
    """
    Дешифрование самоключа Виженера с начальным ключом в 1 символ.
    Каждая расшифрованная буква становится ключом для следующей.
    """
    plaintext = []
    current_key = primer_char.upper()

    for char in ciphertext.upper():
        if char in ALPHABET:
            c_idx = ALPHABET.index(char)
            k_idx = ALPHABET.index(current_key)

            p_idx = (c_idx - k_idx) % 26
            p_char = ALPHABET[p_idx]

            plaintext.append(p_char)
            current_key = p_char
        else:
            plaintext.append(char)

    return "".join(plaintext)


def evaluate_text(text):
    """
    Оценка текста по частотности букв.
    Чем меньше значение, тем больше текст похож на нормальный английский.
    """
    clean_text = [c for c in text.upper() if c in ALPHABET]
    if not clean_text: return float('inf')

    freqs = Counter(clean_text)
    score = 0
    length = len(clean_text)

    for char in ALPHABET:
        observed = freqs.get(char, 0)
        expected = length * ENGLISH_FREQS[char]
        if expected > 0:
            score += ((observed - expected) ** 2) / expected

    return score


def main():
    print("Криптоанализ самоключа Виженера\n")

    ciphertext = input("Введите зашифрованный текст: ").strip()
    if not ciphertext:
        print("Текст пуст!")
        return

    print("\n[*] Перебираю все 26 вариантов начального символа...")

    results = []
    # Перебираем все буквы от A до Z
    for primer in ALPHABET:
        decrypted_text = decrypt_autokey_1char(ciphertext, primer)
        score = evaluate_text(decrypted_text)
        results.append((score, primer, decrypted_text))

    results.sort(key=lambda x: x[0])

    print("\n[+] ТОП-5 самых вероятных расшифровок:\n")
    for i, (score, primer, text) in enumerate(results[:5], 1):
        print(f"{i}. Стартовый ключ: '{primer}' (Оценка: {score:.2f})")
        print(f"   Текст: {text[:100]}...\n")


if __name__ == "__main__":
    main()