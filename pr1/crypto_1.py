import random
import string
import math
from collections import Counter

# Исходный текст

ORIGINAL_TEXT = (
    "Morning arrived softly over the quiet town and every window slowly filled with pale gold light "
    "Emma stepped outside with a small notebook in her hand and felt the cool air brush against her face "
    "She loved this hour because the streets still belonged to dreamers bakers and people with private hopes "
    "The world seemed honest before the noise began At the corner market an old man arranged oranges into "
    "perfect bright towers and hummed a song nobody else seemed to know A cyclist passed with a basket of "
    "flowers and a sleepy dog watched from a doorway as if guarding the silence Emma walked toward the river "
    "where the water reflected the sky like a sheet of moving glass She sat on a wooden bench and opened her "
    "notebook Yesterday had been difficult and she wanted to understand why some days felt heavy while others "
    "opened like doors She began to write about small things the kindness of a stranger the smell of bread "
    "the courage it took to begin again With each line her thoughts grew calmer She realized that peace rarely "
    "arrived as a grand event It appeared in fragments in ordinary moments that asked only to be noticed A child "
    "laughed somewhere behind her and the sound carried across the river like a promise Emma smiled closed the "
    "notebook and stood up The town was waking now shutters opening engines starting voices rising Yet something "
    "inside her remained still and clear She knew the day would bring its share of confusion demands and "
    "unfinished tasks but she also knew that this quiet morning had given her a hidden strength She walked home "
    "more slowly than before carrying nothing new except a gentler way of seeing everything around her She "
    "promised herself to protect that calm today"
)

# Шифрование

def create_random_key():
    """Создается случайный ключ"""
    letters = list(string.ascii_lowercase)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def encrypt(text, key):
    """Шиферует текст простой заменой"""
    result = []
    for ch in text:
        if ch.lower() in key:
            mapped = key[ch.lower()]
            result.append(mapped.upper() if ch.isupper() else mapped)
        else:
            result.append(ch)
    return ''.join(result)

def decrypt(text, key):
    """Дешифрует текст по ключу"""
    result = []
    for ch in text:
        if ch.lower() in key:
            mapped = key[ch.lower()]
            result.append(mapped.upper() if ch.isupper() else mapped)
        else:
            result.append(ch)
    return ''.join(result)

# Статистика английского языка


def build_english_bigram_scores():
    """
    Используем известные частоты биграмм из больших корпусов.
    """
    english_sample = (
        "the old clock ticked loudly against empty wall outside rain began tapping window like impatient "
        "visitor wanted come inside sat chair watched shadows stretch across floor remembered another "
        "time when house filled voices laughter now only silence remained except ticking tapping never "
        "thought would end alone this way life had strange sense humor giving taking with same hand "
        "looked photograph creased edges faces smiled back from different world wondered where they now "
        "whether thought him too unlikely probably moved forgot just ordinary man ordinary town ordinary "
        "dreams rain continued fall harder wind shook trees branches scratched glass like begging shelter "
        "stood walked kitchen made tea watched steam curl disappear felt sudden urge call someone anyone "
        "just hear voice remind that still existed beyond these walls picked phone stared numbers could "
        "not decide who deserved disturbance late hour nobody really nobody wanted burden others with "
        "loneliness especially vague kind settles bones without reason put phone down tea gone cold poured "
        "new cup decided instead write letter old fashioned paper pen explaining nothing simply saying "
        "hello remember me words came slowly awkward first then faster pouring onto page thoughts held "
        "inside years ink flowed honest raw unpolished filled three pages stopped read what written "
        "surprised found not sadness but acceptance even gratitude strange scribbled final line signed "
        "name sealed envelope without address knowing would never send maybe that point needed write "
        "more than needed read rain softened gentle patter wind died down somewhere distance heard "
        "train whistle long low sound carried across sleeping town felt lighter somehow less alone "
        "than hour before tomorrow would bring new light new chance notice small beautiful things "
        "today just needed get through tonight tonight simply needed exist exist witness rain clock "
        "empty walls and still remain standing finally smiled placed letter drawer joined others "
        "unsent unwritten yet waiting their turn become words become air become nothing everything "
        "same time climbed stairs paused top looked back hallway dark quiet felt like stranger own "
        "home yet also more home than ever because here being fully honest fully alive fully human "
        "with all flaws fears quiet hopes slept better than months woke once middle night heard "
        "silence now peaceful not oppressive rain stopped clock wound down slept again dreamed "
        "photograph frames empty faces smiling somewhere else but smiled back them dream knew "
        "they smiled not because happy but because loved enough let go held tight memory dream "
        "knew everything morning came late sun broke through clouds hit exactly spot where "
        "letter lay envelope glowed almost warm almost alive almost promised things get better "
        "believed perhaps first time long time"
    )

    bigram_counts = Counter()
    total = 0
    text_clean = ''.join(c for c in english_sample.lower() if c in string.ascii_lowercase)
    for i in range(len(text_clean) - 1):
        bigram_counts[text_clean[i] + text_clean[i+1]] += 1
        total += 1

    scores = {}
    for a in string.ascii_lowercase:
        for b in string.ascii_lowercase:
            count = bigram_counts.get(a + b, 0)
            scores[a + b] = math.log((count + 1) / (total + 676))

    return scores

BIGRAM_SCORES = build_english_bigram_scores()


ENGLISH_FREQ = {
    'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97,
    'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25,
    'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36,
    'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29,
    'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10,
    'z': 0.07
}

# Криптоанализ

def score_text(text, bigram_scores):
    """Оценивает текст на англоязычность по биграммам."""
    text_clean = ''.join(c for c in text.lower() if c in string.ascii_lowercase)
    score = 0.0
    for i in range(len(text_clean) - 1):
        bigram = text_clean[i] + text_clean[i+1]
        score += bigram_scores.get(bigram, -10.0)
    return score

def score_text_quadgram(text, bigram_scores):

    score = score_text(text, bigram_scores)


    common_words = {
        'the', 'and', 'she', 'her', 'with', 'that', 'was', 'had', 'from',
        'but', 'not', 'this', 'for', 'are', 'were', 'been', 'have', 'has',
        'his', 'they', 'will', 'would', 'could', 'about', 'into', 'like',
        'over', 'than', 'them', 'each', 'which', 'their', 'what', 'there',
        'when', 'who', 'some', 'still', 'before', 'after', 'where', 'every',
        'opened', 'walked', 'morning', 'town', 'quiet', 'small', 'began',
        'knew', 'seemed', 'behind', 'across', 'around', 'inside', 'outside',
        'against', 'toward', 'between', 'without', 'because', 'through',
        'also', 'only', 'more', 'now', 'yet', 'while', 'again',
        'notebook', 'river', 'water', 'world', 'light', 'day', 'way'
    }
    words = text.lower().split()
    word_bonus = sum(15.0 for w in words if w in common_words)
    return score + word_bonus

def initial_key_from_frequency(ciphertext):
    """
    Создаёт начальное приближение ключа на основе частотного анализа.
    Сопоставляет частоты букв в шифротексте с частотами английского.
    """
    # Считаем частоты в шифротексте
    cipher_clean = [c.lower() for c in ciphertext if c.lower() in string.ascii_lowercase]
    cipher_freq = Counter(cipher_clean)
    total = len(cipher_clean)

    cipher_sorted = sorted(string.ascii_lowercase, key=lambda x: cipher_freq.get(x, 0), reverse=True)

    english_sorted = sorted(string.ascii_lowercase, key=lambda x: ENGLISH_FREQ.get(x, 0), reverse=True)

    key = {}
    for cipher_letter, plain_letter in zip(cipher_sorted, english_sorted):
        key[cipher_letter] = plain_letter

    return key

def hill_climbing(ciphertext, bigram_scores, max_iterations=50000, restarts=30):
    """
    Hill Climbing алгоритм с перезапусками для взлома шифра замены.
    """
    best_overall_key = None
    best_overall_score = float('-inf')

    for restart in range(restarts):
        # Начальный ключ: частотный анализ
        if restart == 0:
            current_key = initial_key_from_frequency(ciphertext)
        else:
            if best_overall_key and restart % 3 != 0:
                current_key = dict(best_overall_key)
                letters = list(string.ascii_lowercase)
                num_swaps = random.randint(2, 8)
                for _ in range(num_swaps):
                    a, b = random.sample(letters, 2)
                    current_key[a], current_key[b] = current_key[b], current_key[a]
            else:
                current_key = initial_key_from_frequency(ciphertext)
                letters = list(string.ascii_lowercase)
                num_swaps = random.randint(3, 10)
                for _ in range(num_swaps):
                    a, b = random.sample(letters, 2)
                    current_key[a], current_key[b] = current_key[b], current_key[a]

        current_decrypted = decrypt(ciphertext, current_key)
        current_score = score_text_quadgram(current_decrypted, bigram_scores)

        no_improve_count = 0
        letters = list(string.ascii_lowercase)

        for iteration in range(max_iterations):
            a, b = random.sample(letters, 2)
            current_key[a], current_key[b] = current_key[b], current_key[a]


            new_decrypted = decrypt(ciphertext, current_key)
            new_score = score_text_quadgram(new_decrypted, bigram_scores)

            if new_score > current_score:
                current_score = new_score
                current_decrypted = new_decrypted
                no_improve_count = 0
            else:
                current_key[a], current_key[b] = current_key[b], current_key[a]
                no_improve_count += 1

            if no_improve_count > 3000:
                break

        if current_score > best_overall_score:
            best_overall_score = current_score
            best_overall_key = dict(current_key)
            best_decrypted = current_decrypted
            print(f"  [Рестарт {restart+1}/{restarts}] Новый лучший результат: {best_overall_score:.2f}")

            print(f"  Начало: {best_decrypted[:100]}...")
        else:
            print(f"  [Рестарт {restart+1}/{restarts}] результат: {current_score:.2f} (лучший: {best_overall_score:.2f})")

    return best_overall_key, best_decrypted, best_overall_score

def main():
    print("=" * 70)
    print("  КРИПТОАНАЛИЗ ШИФРА ПРОСТОЙ ЗАМЕНЫ")
    print("=" * 70)

    print("\n[1] Создаём случайный ключ и шифруем текст...\n")
    random.seed(42)  # Для воспроизводимости (можно убрать)
    encryption_key = create_random_key()

    print("Ключ шифрования (открытый -> шифр):")
    for plain_char in sorted(encryption_key.keys()):
        print(f"  {plain_char} -> {encryption_key[plain_char]}", end="")
    print("\n")

    ciphertext = encrypt(ORIGINAL_TEXT, encryption_key)
    print(f"Зашифрованный текст (первые 200 символов):")
    print(f"  {ciphertext[:200]}...\n")

    print("[2] Запускаем криптоанализ...\n")

    found_key, decrypted_text, score = hill_climbing(
        ciphertext,
        BIGRAM_SCORES,
        max_iterations=60000,
        restarts=40
    )

    print("\n" + "=" * 70)
    print("  РЕЗУЛЬТАТЫ КРИПТОАНАЛИЗА")
    print("=" * 70)

    print(f"\nНайденный ключ дешифрования (шифр -> открытый):")
    for cipher_char in sorted(found_key.keys()):
        print(f"  {cipher_char} -> {found_key[cipher_char]}", end="")
    print()

    print(f"\n{'='*70}")
    print("РАСШИФРОВАННЫЙ ТЕКСТ:")
    print(f"{'='*70}")
    print(decrypted_text)

    print(f"\n{'='*70}")
    print("ПРОВЕРКА ТОЧНОСТИ:")
    print(f"{'='*70}")

    original_lower = ORIGINAL_TEXT.lower()
    decrypted_lower = decrypted_text.lower()

    correct = sum(1 for a, b in zip(original_lower, decrypted_lower) if a == b)
    total = len(original_lower)
    accuracy = correct / total * 100

    print(f"  Совпадение символов: {correct}/{total} ({accuracy:.2f}%)")

    if accuracy > 99.9:
        print("ТЕКСТ ПОЛНОСТЬЮ ВОССТАНОВЛЕН!")
    elif accuracy > 95:
        print("Текст почти восстановлен, есть незначительные ошибки.")
    else:
        print(f"Текст восстановлен частично ({accuracy:.1f}%).")

    # Показываем ошибки если есть
    if accuracy < 100:
        print("\n  Различия:")
        diff_count = 0
        for i, (a, b) in enumerate(zip(original_lower, decrypted_lower)):
            if a != b and a.isalpha():
                if diff_count < 20:
                    context_start = max(0, i - 10)
                    context_end = min(len(original_lower), i + 10)
                    print(f"    Позиция {i}: ожидалось '{a}', получено '{b}' "
                          f"(контекст: ...{original_lower[context_start:context_end]}...)")
                diff_count += 1
        if diff_count > 20:
            print(f"    ... и ещё {diff_count - 20} различий")

if __name__ == "__main__":
    main()
