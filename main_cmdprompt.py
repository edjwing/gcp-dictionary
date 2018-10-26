import DicManager

print('+++ Program Start! +++')

dic_manager = DicManager.DicManager()

while True:
    input_text = input('Enter Text : ')
    input_text = input_text.strip().lower()
    if input_text == 'exit':
        break

    if len(input_text) < 1:
        continue

    print('Your Text =', input_text)
    confirm = input('Is it correct? (y/n) : ')
    if confirm.lower() == 'n':
        continue

    dic_manager.set_text(input_text)
    is_exist = dic_manager.is_exist_in_dictionary()
    if is_exist:
        print('Exist word in my dictionary :', dic_manager.get_word_record())
        dic_manager.play_mp3_slow()
    else:
        dic_manager.translate_new()

dic_manager.on_close()

print('--- Program End! ---')
