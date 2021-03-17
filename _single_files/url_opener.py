import os
import dataset

try:
    import tkinter as tk
except:
    import Tkinter as tk

#assume db has fields 'name' and 'url'.
DB = dataset.connect('test_db.db') 
TABLE = DB['urls']
DATA = []

def open_url(event):
    url = DATA[listbox.curselection()[0]]['url']
    # Windows Chrome path
    #path = "\"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe\" " #options -incognito
    # *nix Chrome path
    path = '/opt/google/chrome/google-chrome  ' #option -incognito
    os.system(path+url)

def add_url(event):
    global TABLE
    name = entry_name.get()
    url = entry_url.get()
    TABLE.insert(dict(name = name, url = url))
    populate_listbox()
    entry_name.delete(0, 'end')
    entry_url.delete(0, 'end')

def delete_url(event):
    global TABLE
    url = DATA[listbox.curselection()[0]]['url']
    TABLE.delete(url = url)
    populate_listbox()

def populate_listbox():
    global DATA, TABLE
    DATA = list(TABLE.all())
    listbox.delete(0, tk.END)
    for item in DATA:
        item_temp = 'Name: ' + item['name']# + ' Url: ' + item['url']
        listbox.insert(tk.END, item_temp)

if __name__ == '__main__':

    root = tk.Tk()
    label = tk.Label(root, text='URL OPENER')
    label_name = tk.Label(root, text='Enter Name:')
    entry_name = tk.Entry(root)
    label_url = tk.Label(root, text='Enter URL:')
    entry_url = tk.Entry(root)
    add_btn = tk.Button(root, text='Add URL')

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
    listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    dlt_btn = tk.Button(root, text='Delete URL')
    open_btn = tk.Button(root, text='Open URL')

    root.minsize(300, 300)
    label.pack(side='top')
    label_name.pack(side='top', anchor='nw')
    entry_name.pack(side='top', anchor='n')
    label_url.pack(side='top', anchor='nw')
    entry_url.pack(side='top', anchor='n')
    listbox.pack(side='bottom', anchor='s', fill='x')
    add_btn.pack(side='left', expand=True)
    dlt_btn.pack(side='left', expand=True)
    open_btn.pack(side='left', expand=True)

    populate_listbox()
    listbox.select_set(first=0)

    open_btn.bind("<Button-1>", open_url)
    dlt_btn.bind("<Button-1>", delete_url)
    add_btn.bind("<Button-1>", add_url)

    root.mainloop()
