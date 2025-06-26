import timeit
import chardet
from tabulate import tabulate

def read_text_with_detected_encoding(filename):
    with open(filename, "rb") as f:
        raw = f.read()
        detected = chardet.detect(raw)
        encoding = detected['encoding']
    with open(filename, "r", encoding=encoding) as f:
        return f.read()

# Зчитування текстів з локальних файлів
text1 = read_text_with_detected_encoding("стаття 1.txt")
text2 = read_text_with_detected_encoding("стаття 2.txt")

# Створення патернів для пошуку у тексті: існуючий і не існуючий в обох текстах
pattern_existing = "елемент"
pattern_non_existing = "неочікуваності"


# Алгоритм Кнута-Морріса-Пратта \ kmp_search
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

def search_in_text1_existing():
    return kmp_search(text1, pattern_existing)

def search_in_text2_existing():
    return kmp_search(text2, pattern_existing)

def search_in_text1_non_existing():
    return kmp_search(text1, pattern_non_existing)

def search_in_text2_non_existing():
    return kmp_search(text2, pattern_non_existing)

# Вимірювання часу виконання для existing_pattern
kmp_time_text1_existing = timeit.timeit(search_in_text1_existing, number=100)/100
kmp_time_text2_existing = timeit.timeit(search_in_text2_existing, number=100)/100

# Вимірювання часу виконання для non_existing_pattern
kmp_time_text1_non_existing = timeit.timeit(search_in_text1_non_existing, number=100)/100
kmp_time_text2_non_existing = timeit.timeit(search_in_text2_non_existing, number=100)/100


# Алгоритм Боєра-Мура
def build_shift_table(pattern):

    #Створюємо таблицю зсувів для алгоритму Боєра-Мура.
    table = {}
    length = len(pattern)

    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

def boyer_moore_search_in_text1_existing():
    return boyer_moore_search(text1, pattern_existing)

def boyer_moore_search_in_text2_existing():
    return boyer_moore_search(text2, pattern_existing)

def boyer_moore_search_in_text1_non_existing():
    return boyer_moore_search(text1, pattern_non_existing)

def boyer_moore_search_in_text2_non_existing():
    return boyer_moore_search(text2, pattern_non_existing)

# Вимірювання часу виконання для existing_pattern
boyer_time_text1_existing = timeit.timeit(boyer_moore_search_in_text1_existing, number=100)/100
boyer_time_text2_existing = timeit.timeit(boyer_moore_search_in_text2_existing, number=100)/100

# Вимірювання часу виконання для non_existing_pattern
boyer_time_text1_non_existing = timeit.timeit(boyer_moore_search_in_text1_non_existing, number=100)/100
boyer_time_text2_non_existing = timeit.timeit(boyer_moore_search_in_text2_non_existing, number=100)/100


# Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):

    #Повертаємо поліноміальний хеш рядка s.
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):

    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

def rabin_karp_search_in_text1_existing():
    return rabin_karp_search(text1, pattern_existing)

def rabin_karp_search_in_text2_existing():
    return rabin_karp_search(text2, pattern_existing)

def rabin_karp_search_in_text1_non_existing():
    return rabin_karp_search(text1, pattern_non_existing)

def rabin_karp_search_in_text2_non_existing():
    return rabin_karp_search(text2, pattern_non_existing)

# Вимірювання часу виконання для existing_pattern
rabin_karp_time_text1_existing = timeit.timeit(rabin_karp_search_in_text1_existing, number=100)/100
rabin_karp_time_text2_existing = timeit.timeit(rabin_karp_search_in_text2_existing, number=100)/100

# Вимірювання часу виконання для non_existing_pattern
rabin_karp_time_text1_non_existing = timeit.timeit(rabin_karp_search_in_text1_non_existing, number=100)/100
rabin_karp_time_text2_non_existing = timeit.timeit(rabin_karp_search_in_text2_non_existing, number=100)/100


# Вивід усіх результатів тестування у табличному вигляді
headers = ["Pattern", "Area", "kmp_search, sec", "boyer_moore, sec", "rabin_karp, sec"]
table = [
    ["Existing",     "text1", kmp_time_text1_existing,     boyer_time_text1_existing,     rabin_karp_time_text1_existing],
    ["Non-Existing", "text1", kmp_time_text1_non_existing, boyer_time_text1_non_existing, rabin_karp_time_text1_non_existing],
    ["Existing",     "text2", kmp_time_text2_existing,     boyer_time_text2_existing,     rabin_karp_time_text2_existing],
    ["Non-Existing", "text2", kmp_time_text2_non_existing, boyer_time_text2_non_existing, rabin_karp_time_text2_non_existing],
]

print(tabulate(table, headers=headers, floatfmt=".10f", tablefmt="github"))