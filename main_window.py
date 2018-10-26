import tkinter as tk
import tkinter.ttk as ttk
import DicManager


class GcpDictionaryWindow:

    dic_manager = None

    tk_root = None
    fr_text = None
    kr_text = None
    en_text = None
    button_trans = None
    button_play_n = None
    button_play_s = None
    tree_dic = None
    button_delete = None

    def __init__(self):
        self.dic_manager = DicManager.DicManager()
        root = tk.Tk()
        root.title('Google Translation Dictionary')

        myf = 'Sitka Text'
        myfk = 'Malgun Gothic'
        mys = 14
        my_style = ttk.Style()
        my_style.configure('Treeview', font=(myf, 14), rowheight=30)
        my_style.configure('Treeview.Heading', bg='light blue', font=(myf, mys), rowheight=20)

        fm_title = tk.Frame(root)
        label_title = tk.Label(fm_title, text='Google Translation Dictionary V0.1\nby Jiwoong Kim', bg='light blue', font=(myf, mys))
        label_title.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        fm_title.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X, expand=tk.YES)

        fm_word = tk.Frame(root)
        fm_label = tk.Frame(fm_word)
        label_fr = tk.Label(fm_label, text='French', font=(myf, mys))
        label_fr.pack(side=tk.TOP)
        label_kr = tk.Label(fm_label, text='Korean', font=(myf, mys))
        label_kr.pack(side=tk.TOP, pady=2)
        label_en = tk.Label(fm_label, text='English', font=(myf, mys))
        label_en.pack(side=tk.TOP)
        fm_label.pack(side=tk.LEFT, padx=10)
        fm_entry = tk.Frame(fm_word)

        self.fr_text = tk.StringVar()
        entry_fr = tk.Entry(fm_entry, textvariable=self.fr_text, font=(myf, mys))
        entry_fr.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        self.fr_text.set('le français')
        self.kr_text = tk.StringVar()
        entry_kr = tk.Entry(fm_entry, textvariable=self.kr_text, state='readonly', font=(myfk, mys))
        entry_kr.pack(side=tk.TOP, pady=2, anchor=tk.W, fill=tk.X, expand=tk.YES)
        self.kr_text.set('프랑스어')
        self.en_text = tk.StringVar()
        entry_en = tk.Entry(fm_entry, textvariable=self.en_text, state='readonly', font=(myf, mys))
        entry_en.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=tk.YES)
        self.en_text.set('French')
        fm_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=tk.YES)
        fm_word.pack(side=tk.TOP, pady=10, fill=tk.X, expand=tk.YES)

        fm_button = tk.Frame(root)
        self.button_trans = tk.Button(fm_button, text='Translate', font=(myf, mys), bg='light green')
        self.button_trans.pack(side=tk.LEFT)
        self.button_play_n = tk.Button(fm_button, text='Play Normal', font=(myf, mys), bg='light pink')
        self.button_play_n.pack(side=tk.LEFT, padx=20)
        self.button_play_s = tk.Button(fm_button, text='Play Slow', font=(myf, mys), bg='light pink')
        self.button_play_s.pack(side=tk.LEFT)
        fm_button.pack(side=tk.TOP, padx=10, pady=10)

        fm_list = tk.Frame(root)
        scrollbar = tk.Scrollbar(fm_list, orient=tk.VERTICAL)
        self.tree_dic = ttk.Treeview(fm_list, columns=('French', 'Korean', 'English'), yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree_dic.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_dic.heading('#0', text='No')
        self.tree_dic.heading('#1', text='French')
        self.tree_dic.heading('#2', text='Korean')
        self.tree_dic.heading('#3', text='English')
        self.tree_dic.column('#0', width=80)
        self.tree_dic.column('#1', stretch=tk.YES)
        self.tree_dic.column('#2', stretch=tk.YES)
        self.tree_dic.column('#0', stretch=tk.YES)
        self.tree_dic.tag_configure('odd', background='light yellow')
        self.tree_dic.tag_configure('even', background='white')
        self.tree_dic.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        fm_list.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X, expand=tk.YES)

        fm_db_ctrl = tk.Frame(root)
        self.button_delete = tk.Button(fm_db_ctrl, text='Delete', font=(myf, mys), bg='light gray')
        self.button_delete.pack(side=tk.LEFT)
        fm_db_ctrl.pack(side=tk.TOP, padx=10, pady=10)

        self.button_trans.bind('<Button-1>', self.btn_translate)
        self.button_play_n.bind('<Button-1>', self.btn_play_normal)
        self.button_play_s.bind('<Button-1>', self.btn_play_slow)
        self.tree_dic.bind('<ButtonRelease-1>', self.list_selected)
        self.button_delete.bind('<Button-1>', self.btn_delete_record)

        self.tk_root = root

    def set_word_info(self, word):
        self.fr_text.set(word.text)
        self.kr_text.set(word.korean)
        self.en_text.set(word.english)

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

    def btn_translate(self, event):
        text = self.fr_text.get().strip().lower()
        self.dic_manager.set_text(text)
        word_info = self.dic_manager.find_in_dictionary()
        if word_info is not None:
            print('Exist in Dictionary :', word_info)
            self.dic_manager.play_mp3_slow()
        else:
            word_info = self.dic_manager.translate_new()
            self.refresh_dict_list()
            # set_selection_last_word(word_info)
        self.set_word_info(word_info)

    def btn_play_normal(self, event):
        self.dic_manager.play_mp3()

    def btn_play_slow(self, event):
        self.dic_manager.play_mp3_slow()

    def btn_delete_record(self, event):
        cur_item = self.tree_dic.focus()
        index = self.tree_dic.index(cur_item)
        selected_word = self.dic_manager.cur_dictionary[index]
        self.dic_manager.del_word_in_dictionary(selected_word)
        self.refresh_dict_list()

    def list_selected(self, event):
        cur_item = self.tree_dic.focus()
        index = self.tree_dic.index(cur_item)
        selected_word = self.dic_manager.cur_dictionary[index]
        self.dic_manager.set_word(selected_word)
        self.set_word_info(selected_word)
        self.dic_manager.play_mp3_slow()

    def main(self):
        self.refresh_dict_list()
        self.tk_root.mainloop()


if __name__ == '__main__':
    obj = GcpDictionaryWindow()
    obj.main()
