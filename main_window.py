import tkinter as tk
import tkinter.ttk as ttk
import DicManager


class GcpDictionaryWindow:

    dic_manager = None
    tk_root = None
    entry_fr = None
    entry_kr = None
    entry_en = None
    fr_text = None
    kr_text = None
    en_text = None
    button_trans = None
    button_play_n = None
    button_play_s = None
    is_auto_save = None
    tree_dic = None
    button_save = None
    button_delete = None

    def __init__(self):
        self.dic_manager = DicManager.DicManager()
        root = tk.Tk()
        root.title('Google Translation Dictionary')

        my_font = ('Sitka Text', 14)
        my_font_ko = ('Malgun Gothic', 14)
        my_style = ttk.Style()
        my_style.configure('Treeview', font=my_font, rowheight=30)
        my_style.configure('Treeview.Heading', bg='light blue', font=my_font, rowheight=20)

        fm_title = tk.Frame(root)
        label_title = tk.Label(fm_title, text='Google Translation & TTS Dictionary V0.1\nby Jiwoong Kim', bg='light blue', font=my_font)
        label_title.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        fm_title.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X, expand=tk.YES)

        fm_word = tk.Frame(root)
        fm_label = tk.Frame(fm_word)
        label_fr = tk.Label(fm_label, text='French', font=my_font)
        label_fr.pack(side=tk.TOP)
        label_kr = tk.Label(fm_label, text='Korean', font=my_font)
        label_kr.pack(side=tk.TOP, pady=2)
        label_en = tk.Label(fm_label, text='English', font=my_font)
        label_en.pack(side=tk.TOP)
        fm_label.pack(side=tk.LEFT, padx=10)
        fm_entry = tk.Frame(fm_word)

        self.fr_text = tk.StringVar()
        self.entry_fr = tk.Entry(fm_entry, textvariable=self.fr_text, font=my_font)
        self.entry_fr.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        self.fr_text.set('le français')
        self.kr_text = tk.StringVar()
        self.entry_kr = tk.Entry(fm_entry, textvariable=self.kr_text, state='readonly', font=my_font_ko)
        self.entry_kr.pack(side=tk.TOP, pady=2, anchor=tk.W, fill=tk.X, expand=tk.YES)
        self.kr_text.set('프랑스어')
        self.en_text = tk.StringVar()
        self.entry_en = tk.Entry(fm_entry, textvariable=self.en_text, state='readonly', font=my_font)
        self.entry_en.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=tk.YES)
        self.en_text.set('French')
        fm_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=tk.YES)
        fm_word.pack(side=tk.TOP, pady=10, fill=tk.X, expand=tk.YES)

        fm_button = tk.Frame(root)
        self.is_auto_save = tk.IntVar()
        chk_auto_save = tk.Checkbutton(fm_button, text='Auto Save', variable=self.is_auto_save, font=my_font)
        chk_auto_save.pack(side=tk.LEFT, padx=10, anchor=tk.W, fill=tk.X, expand=tk.YES)
        chk_auto_save.select()
        self.button_trans = tk.Button(fm_button, text='Translate', font=my_font, bg='light green')
        self.button_trans.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=tk.YES)
        self.button_play_n = tk.Button(fm_button, text='Play Normal', font=my_font, bg='light pink')
        self.button_play_n.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=tk.YES)
        self.button_play_s = tk.Button(fm_button, text='Play Slow', font=my_font, bg='light pink')
        self.button_play_s.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=tk.YES)
        fm_button.pack(side=tk.TOP, pady=10, fill=tk.X, expand=tk.YES)

        fm_list = tk.Frame(root)
        scrollbar = tk.Scrollbar(fm_list, orient=tk.VERTICAL)
        self.tree_dic = ttk.Treeview(fm_list, columns=('French', 'Korean', 'English'), yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree_dic.yview)
        self.tree_dic.heading('#0', text='No')
        self.tree_dic.heading('#1', text='French')
        self.tree_dic.heading('#2', text='Korean')
        self.tree_dic.heading('#3', text='English')
        self.tree_dic.column('#0', width=80)
        self.tree_dic.column('#1', stretch=tk.YES)
        self.tree_dic.column('#2', stretch=tk.YES)
        self.tree_dic.column('#3', stretch=tk.YES)
        self.tree_dic.tag_configure('odd', background='light yellow')
        self.tree_dic.tag_configure('even', background='white')
        self.tree_dic.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, expand=tk.YES)
        fm_list.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=tk.YES)

        fm_db_ctrl = tk.Frame(root)
        self.button_save = tk.Button(fm_db_ctrl, text='Save', state=tk.DISABLED, font=my_font, bg='light gray')
        self.button_save.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=tk.YES)
        self.button_delete = tk.Button(fm_db_ctrl, text='Delete', state=tk.DISABLED, font=my_font, bg='light gray')
        self.button_delete.pack(side=tk.LEFT, padx=10)
        fm_db_ctrl.pack(side=tk.TOP, pady=10, fill=tk.X, expand=tk.YES)

        chk_auto_save.bind('<ButtonRelease-1>', self.chk_clicked)
        self.button_trans.bind('<Button-1>', self.btn_translate)
        self.entry_fr.bind('<Return>', self.btn_translate)
        self.button_play_n.bind('<Button-1>', self.btn_play_normal)
        self.button_play_s.bind('<Button-1>', self.btn_play_slow)
        self.tree_dic.bind('<ButtonRelease-1>', self.list_selected)

        self.tk_root = root

    def set_word_info(self, word):
        self.fr_text.set(word.text)
        self.entry_fr.update()
        self.kr_text.set(word.korean)
        self.entry_kr.update()
        self.en_text.set(word.english)
        self.entry_en.update()

    def refresh_dict_list(self):
        for item in self.tree_dic.get_children():
            self.tree_dic.delete(item)
        cur_dict = self.dic_manager.get_cur_dictionary()
        i = 0
        if cur_dict is not None and len(cur_dict) > 0:
            for word in cur_dict:
                i += 1
                if i % 2 == 0:
                    self.tree_dic.insert('', 'end', text=str(i), values=(word.text, word.korean, word.english), tags=('even',))
                else:
                    self.tree_dic.insert('', 'end', text=str(i), values=(word.text, word.korean, word.english), tags=('odd',))

    def set_selection_last_word(self, word):
        self.tree_dic.focus((word.text, word.korean, word.english))

    def chk_clicked(self, event):
        print('Check Button Clicked :', self.is_auto_save.get())
        if self.is_auto_save.get() == 1:
            self.button_save.config(state=tk.NORMAL)

    def btn_translate(self, event):
        text = self.fr_text.get().strip().lower()
        self.dic_manager.set_text(text)
        word_info = self.dic_manager.find_in_dictionary()
        if word_info is not None:
            print('Exist in Dictionary :', word_info)
            self.set_word_info(word_info)
            self.dic_manager.play_mp3_slow()
        else:
            word_info = self.dic_manager.translate_new()
            self.set_word_info(word_info)
            self.dic_manager.temp_play_mp3_slow()
            if self.is_auto_save.get() == 1:
                self.dic_manager.save_word()
                self.refresh_dict_list()
            else:
                self.button_save.config(state=tk.NORMAL)
                self.button_save.bind('<Button-1>', self.btn_save)

    def btn_play_normal(self, event):
        self.dic_manager.play_mp3()

    def btn_play_slow(self, event):
        self.dic_manager.play_mp3_slow()

    def btn_save(self, event):
        self.dic_manager.save_word()
        self.refresh_dict_list()
        self.button_save.config(state=tk.DISABLED)
        self.button_save.unbind('<Button-1>')

    def btn_delete(self, event):
        cur_item = self.tree_dic.focus()
        index = self.tree_dic.index(cur_item)
        selected_word = self.dic_manager.cur_dictionary[index]
        self.dic_manager.del_word_in_dictionary(selected_word)
        self.refresh_dict_list()
        self.button_delete.config(state=tk.DISABLED)
        self.button_delete.unbind('<Button-1>')

    def list_selected(self, event):
        cur_item = self.tree_dic.focus()
        index = self.tree_dic.index(cur_item)
        selected_word = self.dic_manager.cur_dictionary[index]
        self.dic_manager.set_word(selected_word)
        self.set_word_info(selected_word)
        self.dic_manager.play_mp3_slow()
        self.button_delete.config(state=tk.NORMAL)
        self.button_delete.bind('<Button-1>', self.btn_delete)

    def main(self):
        self.refresh_dict_list()
        self.tk_root.mainloop()


if __name__ == '__main__':
    obj = GcpDictionaryWindow()
    obj.main()
