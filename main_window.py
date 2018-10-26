import tkinter as tk
import tkinter.ttk as ttk
import DicManager


dic_manager = DicManager.DicManager()
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

fr_text = tk.StringVar()
entry_fr = tk.Entry(fm_entry, textvariable=fr_text, font=(myf, mys))
entry_fr.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
fr_text.set('le français')
kr_text = tk.StringVar()
entry_kr = tk.Entry(fm_entry, textvariable=kr_text, state='readonly', font=(myfk, mys))
entry_kr.pack(side=tk.TOP, pady=2, anchor=tk.W, fill=tk.X, expand=tk.YES)
kr_text.set('프랑스어')
en_text = tk.StringVar()
entry_en = tk.Entry(fm_entry, textvariable=en_text, state='readonly', font=(myf, mys))
entry_en.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=tk.YES)
en_text.set('French')
fm_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=tk.YES)
fm_word.pack(side=tk.TOP, pady=10, fill=tk.X, expand=tk.YES)

fm_button = tk.Frame(root)
button_trans = tk.Button(fm_button, text='Translate', font=(myf, mys), bg='light green')
button_trans.pack(side=tk.LEFT)
button_play_n = tk.Button(fm_button, text='Play Normal', font=(myf, mys), bg='light pink')
button_play_n.pack(side=tk.LEFT, padx=20)
button_play_s = tk.Button(fm_button, text='Play Slow', font=(myf, mys), bg='light pink')
button_play_s.pack(side=tk.LEFT)
fm_button.pack(side=tk.TOP, padx=10, pady=10)

fm_list = tk.Frame(root)
scrollbar = tk.Scrollbar(fm_list, orient=tk.VERTICAL)
tree_dic = ttk.Treeview(fm_list, columns=('French', 'Korean', 'English'), yscrollcommand=scrollbar.set)
scrollbar.config(command=tree_dic.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree_dic.heading('#0', text='No')
tree_dic.heading('#1', text='French')
tree_dic.heading('#2', text='Korean')
tree_dic.heading('#3', text='English')
tree_dic.column('#0', width=80)
tree_dic.column('#1', stretch=tk.YES)
tree_dic.column('#2', stretch=tk.YES)
tree_dic.column('#0', stretch=tk.YES)
tree_dic.tag_configure('odd', background='light yellow')
tree_dic.tag_configure('even', background='white')
tree_dic.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
fm_list.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X, expand=tk.YES)

fm_db_ctrl = tk.Frame(root)
button_delete = tk.Button(fm_db_ctrl, text='Delete', font=(myf, mys), bg='light gray')
button_delete.pack(side=tk.LEFT)
fm_db_ctrl.pack(side=tk.TOP, padx=10, pady=10)


def set_word_info(word):
    fr_text.set(word.text)
    kr_text.set(word.korean)
    en_text.set(word.english)


def refresh_dict_list():
    for item in tree_dic.get_children():
        tree_dic.delete(item)
    cur_dict = dic_manager.get_cur_dictionary()
    i = 0
    if cur_dict is not None and len(cur_dict) > 0:
        for word in cur_dict:
            i += 1
            if i % 2 == 0:
                tree_dic.insert('', 'end', text=str(i), values=(word.text, word.korean, word.english), tags=('even',))
            else:
                tree_dic.insert('', 'end', text=str(i), values=(word.text, word.korean, word.english), tags=('odd',))


def set_selection_last_word(word):
    tree_dic.focus((word.text, word.korean, word.english))


def btn_translate(event):
    text = fr_text.get().strip().lower()
    dic_manager.set_text(text)
    word_info = dic_manager.find_in_dictionary()
    if word_info is not None:
        print('Exist in Dictionary :', word_info)
        dic_manager.play_mp3_slow()
    else:
        word_info = dic_manager.translate_new()
        refresh_dict_list()
        # set_selection_last_word(word_info)
    set_word_info(word_info)


def btn_play_normal(event):
    dic_manager.play_mp3()


def btn_play_slow(event):
    dic_manager.play_mp3_slow()


def btn_delete_record(event):
    cur_item = tree_dic.focus()
    index = tree_dic.index(cur_item)
    selected_word = dic_manager.cur_dictionary[index]
    dic_manager.del_word_in_dictionary(selected_word)
    refresh_dict_list()


def list_selected(event):
    cur_item = tree_dic.focus()
    index = tree_dic.index(cur_item)
    selected_word = dic_manager.cur_dictionary[index]
    dic_manager.set_word(selected_word)
    set_word_info(selected_word)
    dic_manager.play_mp3_slow()


button_trans.bind('<Button-1>', btn_translate)
button_play_n.bind('<Button-1>', btn_play_normal)
button_play_s.bind('<Button-1>', btn_play_slow)
tree_dic.bind('<ButtonRelease-1>', list_selected)
button_delete.bind('<Button-1>', btn_delete_record)

refresh_dict_list()
root.mainloop()
