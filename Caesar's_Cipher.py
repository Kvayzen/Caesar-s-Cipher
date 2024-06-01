import re

non_alphabetic_characters = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

def is_russian(input_text):
    return bool(re.search('[а-яА-Я]', input_text))

def is_english(input_text):
    return bool(re.search('[a-zA-Z]', input_text))

def caesar_cipher(text, shift_step, language):
    if language == 'англ':
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
    elif language == 'рус':
        alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    else:
        print('Неверный язык, попробуйте снова\n')
        return
    encrypted_text = ''
    for character in text:
        if character in non_alphabetic_characters or character.isspace():
            encrypted_text += character
        else:
            index = alphabet.find(character.lower())
            if index == -1:
                encrypted_text += character
            else:
                new_index = (index + shift_step) % len(alphabet)
                if character.isupper():
                    encrypted_text += alphabet[new_index].upper()
                else:
                    encrypted_text += alphabet[new_index]
    return encrypted_text

def encrypt_with_language_check(text, shift_step, language):
    if language == 'англ':
        # Проверяем, что все символы английские или неалфавитные/пробелы
        if not all(char in non_alphabetic_characters or char.isspace() or is_english(char) for char in text):
            print("Ошибка: Вы выбрали английский язык, но ввели текст, содержащий символы другого языка. Пожалуйста, попробуйте снова.")
            return
    elif language == 'рус':
        # Проверяем, что все символы русские или неалфавитные/пробелы
        if not all(char in non_alphabetic_characters or char.isspace() or is_russian(char) for char in text):
            print("Ошибка: Вы выбрали русский язык, но ввели текст, содержащий символы другого языка. Пожалуйста, попробуйте снова.")
            return
    return caesar_cipher(text, shift_step, language)

def encrypt_individual_words(text, language):
    words = text.split()
    encrypted_words = []
    for word in words:
        shift_step = len(re.findall('[a-zA-Z]', word))  # Сдвиг равен количеству букв в слове
        encrypted_word = caesar_cipher(word, shift_step, language)
        encrypted_words.append(encrypted_word)
    return ' '.join(encrypted_words)

def auto_decrypt(text, language):
    if language == 'англ':
        possible_shifts = range(26)
    elif language == 'рус':
        possible_shifts = range(32)
    else:
        print('Неверный язык, попробуйте снова\n')
        return

    for shift_step in possible_shifts:
        decrypted_text = caesar_cipher(text, -shift_step, language)
        print(f'Сдвиг {shift_step}: {decrypted_text}')
        # Здесь можно добавить логику для определения правильного текста,
        # например, проверку на наличие слов из словаря.

def play_game():
    print('Добро пожаловать в "Шифр Цезаря"!\n')
    
    while True:
        print("Выберите режим работы:")
        print("1 - Обычное шифрование")
        print("2 - Шифрование с индивидуальным сдвигом для каждого слова")
        print("3 - Автоматическая дешифровка с неизвестным сдвигом")
        print("4 - Обычная дешифровка с известным сдвигом")
        mode = input("Введите номер режима или 'выход' для завершения: ").strip()
        if mode.lower() == 'выход':
            print('До свидания!')
            return
        if mode in ['1', '2', '3', '4']:
            break
        else:
            print("Неверный ввод. Пожалуйста, введите 1, 2, 3 или 4.\n")
    
    language = ''
    while not language:
        language_input = input('Введите "англ" или "рус" для выбора языка шифрования или "выход" для завершения:\n').lower().strip()
        if language_input == 'выход':
            print('До свидания!')
            return
        if language_input in ['англ', 'рус']:
            language = language_input
        else:
            print("Неверный ввод. Пожалуйста, введите 'англ' или 'рус'.\n")
    
    while True:
        text_input = input('Введите текст для шифрования или дешифрования или "выход" для завершения:\n').strip()
        if text_input.lower() == 'выход':
            print('До свидания!')
            return
        if language == 'англ' and not all(char in non_alphabetic_characters or char.isspace() or is_english(char) for char in text_input):
            print("Ошибка: Вы выбрали английский язык, но ввели текст, содержащий символы другого языка. Пожалуйста, попробуйте снова.")
            continue
        elif language == 'рус' and not all(char in non_alphabetic_characters or char.isspace() or is_russian(char) for char in text_input):
            print("Ошибка: Вы выбрали русский язык, но ввели текст, содержащий символы другого языка. Пожалуйста, попробуйте снова.")
            continue
        else:
            text = text_input
            break
    
    if mode == '1':
        shift_step = ''
        while not shift_step:
            shift_input = input('Введите шаг сдвига или "выход" для завершения:\n').strip()
            if shift_input.lower() == 'выход':
                print('До свидания!')
                return
            try:
                shift_step = int(shift_input)
                encrypted_text = caesar_cipher(text, shift_step, language)
                print(f'Ваш зашифрованный текст: {encrypted_text}\n')
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите целое число.\n")
    elif mode == '2':
        encrypted_text = encrypt_individual_words(text, language)
        print(f'Ваш зашифрованный текст: {encrypted_text}\n')
    elif mode == '3':
        auto_decrypt(text, language)
    elif mode == '4':
        shift_step = ''
        while not shift_step:
            shift_input = input('Введите шаг сдвига для дешифрования или "выход" для завершения:\n').strip()
            if shift_input.lower() == 'выход':
                print('До свидания!')
                return
            try:
                shift_step = int(shift_input)
                decrypted_text = caesar_cipher(text, -shift_step, language)
                print(f'Ваш дешифрованный текст: {decrypted_text}\n')
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите целое число.\n")
    
    repeat = ''
    while not repeat:
        repeat_input = input('Хотите зашифровать или дешифровать еще текст? (да/нет) или "выход" для завершения:\n').lower().strip()
        if repeat_input.lower() == 'выход':
            print('До свидания!')
            return
        if repeat_input in ['да', 'нет']:
            repeat = repeat_input
            if repeat == 'да':
                play_game()
            elif repeat == 'нет':
                print('Завершение работы программы.')
                print('До свидания!')
                return
        else:
            print("Неверный ввод. Пожалуйста, введите 'да' или 'нет'.\n")

while True:
    user_input = input('Введите "Шифр Цезаря" для шифрования или дешифрования или "выход", чтобы закончить:\n').lower().strip()
    if user_input == 'шифр цезаря':
        play_game()
    elif user_input == 'выход':
        print('До свидания!')
        break
    else:
        print('Неверное название, попробуйте снова\n')