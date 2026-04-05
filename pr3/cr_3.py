ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

COMMON_STARTS_3 = {
    "THE", "AND", "THA", "FOR", "PRO", "CON", "INT", "COM", "SHE", "WHO", "WHI",
    "ALL", "ANY", "ARE", "BUT", "CAN", "DID", "GET", "HAS", "HAD", "HOW", "HIS",
    "HER", "OUT", "ONE", "OUR", "SEE", "TOO", "USE", "WAS", "WAY", "YOU"
}

COMMON_STARTS_2 = {
    "TH", "HE", "IN", "AN", "RE", "ON", "AT", "EN", "OF", "IS", "IT", "AL", "AR",
    "ST", "TO", "SE", "HA", "AS", "OU", "CO", "ME", "DE", "HI", "RO", "NE", "EA",
    "CE", "LI", "CH", "BE", "MA", "SI", "WH", "SH", "WE", "DO", "GO", "NO", "SO",
    "MY", "BY", "UP", "US", "IF", "PR", "TR", "GR", "PL", "CR", "BL", "FL"
}


def decrypt_ciphertext_autokey_1char(ciphertext, primer_char):
    """
    Дешифровка самоключа по ШИФРТЕКСТУ.
    """
    plaintext = []
    current_key = primer_char.upper()

    for char in ciphertext.upper():
        if char in ALPHABET:
            c_idx = ALPHABET.index(char)
            k_idx = ALPHABET.index(current_key)

            p_idx = (c_idx - k_idx) % 26
            plaintext.append(ALPHABET[p_idx])

            current_key = char
        else:
            plaintext.append(char)

    return "".join(plaintext)


def evaluate_start(text):

    clean_text = [c for c in text.upper() if c in ALPHABET]
    if not clean_text: return 0

    score = 0
    prefix2 = "".join(clean_text[:2])
    prefix3 = "".join(clean_text[:3])

    if prefix3 in COMMON_STARTS_3:
        score += 100
    elif prefix2 in COMMON_STARTS_2:
        score += 30

    bad_starts = ["UH", "BH", "QH", "YH", "XH", "ZH", "JH", "VH", "QZ", "QX", "JX", "ZX", "HX"]
    if prefix2 in bad_starts:
        score -= 50

    return score


def main():
    print("Криптоанализ самоключа по ШИФРТЕКСТУ\n")

    ciphertext = input("Введите зашифрованный текст:\n").strip()
    if not ciphertext: return

    print("\n[*] Анализирую 26 вариантов начального символа...")

    results = []
    for primer in ALPHABET:
        decrypted_text = decrypt_ciphertext_autokey_1char(ciphertext, primer)
        score = evaluate_start(decrypted_text)
        results.append((score, primer, decrypted_text))

    results.sort(key=lambda x: x[0], reverse=True)

    print("\n[+] ТОП-5 самых вероятных расшифровок:\n")
    for i, (score, primer, text) in enumerate(results[:5], 1):
        print(f"{i}. Ключ: '{primer}' | Баллы: {score}")
        print(f"   Текст: {text[:80]}...\n")


if __name__ == "__main__":
    main()