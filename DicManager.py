import GCPutil
import SoundUtil
import DictionaryUtil


class DicManager:

    translator = None
    tts = None
    sound_player = None
    dic_db = None
    cur_word = None
    new_word = None
    cur_dictionary = None

    def __init__(self):
        print('Initialize Dictionary Manager...')
        self.translator = GCPutil.GTranslator()
        self.tts = GCPutil.GTextToSpeech()
        self.sound_player = SoundUtil.PlaySound()
        self.dic_db = DictionaryUtil.DictionaryDB()
        self.cur_word = DictionaryUtil.DictionaryWord()
        self.new_word = DictionaryUtil.DictionaryWord()
        self.dic_db.connect_db()
        print('Initialize Done!')

    def set_text(self, text):
        self.cur_word = DictionaryUtil.DictionaryWord()
        self.cur_word.set_input_text(text)
        self.new_word = DictionaryUtil.DictionaryWord()
        self.new_word.set_input_text(text)

    def is_exist_in_dictionary(self):
        cur_record = self.dic_db.find_record(self.cur_word.fr_word)
        print('[check_dictionary] :', cur_record)
        if cur_record is not None:
            self.cur_word.set_from_db_record(cur_record)
            return True
        else:
            return False

    def find_in_dictionary(self):
        cur_record = self.dic_db.find_record(self.cur_word.fr_word)
        print('[check_dictionary] :', cur_record)
        if cur_record is not None:
            self.cur_word.set_from_db_record(cur_record)
            return self.cur_word
        else:
            return None

    def get_word_index(self, word):
        index = 0
        for cur_word in self.cur_dictionary:
            if cur_word.fr_word == word.fr_word:
                break
            index += 1
        return index

    def get_word_record(self):
        return self.cur_word.get_record()

    def play_mp3(self):
        if self.cur_word.mp3_file is not None and self.cur_word.mp3_file != '':
            self.sound_player.mp3_play(self.cur_word.mp3_file, 'mp3')

    def play_mp3_slow(self):
        if self.cur_word.mp3_file_slow is not None and self.cur_word.mp3_file_slow != '':
            self.sound_player.mp3_play(self.cur_word.mp3_file_slow, 'mp3')

    def translate_new(self):
        self.new_word.korean = self.translator.trans_to_kor(self.new_word.text)
        self.new_word.english = self.translator.trans_to_eng(self.new_word.text)
        self.new_word.mp3_file = self.tts.tts_to_mp3(self.new_word.text, 1.0)
        self.new_word.mp3_file_slow = self.tts.tts_to_mp3(self.new_word.text, 0.7)
        self.new_word.set_time()
        self.dic_db.insert_record_by_word(self.new_word)
        self.sound_player.mp3_play(self.new_word.mp3_file_slow, 'mp3')
        self.cur_word = self.new_word
        return self.new_word

    def get_cur_dictionary(self):
        self.cur_dictionary = self.dic_db.read_all()
        return self.cur_dictionary

    def del_word_in_dictionary(self, word):
        self.dic_db.delete_record(word)

    def set_word(self, word):
        self.cur_word = word

    def on_close(self):
        self.dic_db.disconnect_db()
