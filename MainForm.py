import tkinter as tk
from tkinter import ttk

import database

from PIL import ImageTk
from PIL import Image

from SearchDialog import SearchDialog

from AddUpdateDialog import AddDialog
from AddUpdateDialog import UpdateDialog


class MainForm(tk.Frame):
    def __init__(self, root, db):
        super().__init__(root)
        self.root = root
        self.db: database.Database = db

    # init widgets
    def init_main(self):
        #ToolBar
        toolbar = tk.Frame(bg="#d7d7d7", bd=1)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        toolbar2 = tk.Frame(bg="#ebebeb", bd=1)
        toolbar2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Button "Add employeer"
        img = Image.open("./res/add.png")
        self.add_employeer_img = ImageTk.PhotoImage(img.resize((int(img.width*.17),int(img.height*.17))))
        btn_employeer_add = tk.Button(toolbar, image=self.add_employeer_img, bg="#d7d7d7", bd=0, command=self.open_add_dialog)
        self.root.bind("<Control-a>", lambda ev: self.open_add_dialog())
        btn_employeer_add.pack(side=tk.LEFT)

        # Button "Update employeer"
        img = Image.open("./res/update.png")
        self.upd_employeer_img = ImageTk.PhotoImage(img.resize((int(img.width*.17),int(img.height*.17))))
        btn_employeer_upd = tk.Button(toolbar, image=self.upd_employeer_img, bg="#d7d7d7", bd=0, command=self.open_update_dialog)
        self.root.bind("<Control-e>", lambda ev: self.open_update_dialog())
        btn_employeer_upd.pack(side=tk.LEFT)

        # Button "Delete employeer"
        img = Image.open("./res/delete.png")
        self.del_employeer_img = ImageTk.PhotoImage(img.resize((int(img.width*.17),int(img.height*.17))))
        btn_employeer_del = tk.Button(toolbar, image=self.del_employeer_img, bg="#d7d7d7", bd=0, command=self.remove)
        btn_employeer_del.pack(side=tk.LEFT)
        
        # Button "Search employeer"
        img = Image.open("./res/search.png")
        self.srch_employeer_img = ImageTk.PhotoImage(img.resize((int(img.width*.17),int(img.height*.17))))
        btn_employeer_srch = tk.Button(toolbar, image=self.srch_employeer_img, bg="#d7d7d7", bd=0, command=self.open_search_dialog)
        self.root.bind("<Control-f>", lambda ev: self.open_search_dialog())
        btn_employeer_srch.pack(side=tk.LEFT)

        # Button "Search employeer"
        img = Image.open("./res/refresh.png")
        self.updlist_employeer_img = ImageTk.PhotoImage(img.resize((int(img.width*.17),int(img.height*.17))))
        btn_employeer_updlist = tk.Button(toolbar, image=self.updlist_employeer_img, bg="#d7d7d7", bd=0, command=self.view_records)
        self.root.bind("<Control-r>", lambda ev: self.view_records())
        btn_employeer_updlist.pack(side=tk.LEFT)

        # TreeView "Tree"
        self.tree = ttk.Treeview(toolbar2, columns=('ID', 'full_name', 'phone_number', 'email', 'salary'), show='headings')
        
        # TreeView config
        self.tree.column('ID', width=45, anchor="center")
        self.tree.column('full_name', width=300, anchor="center")
        self.tree.column('phone_number', width=150, anchor="center")
        self.tree.column('email', width=150, anchor="center")
        self.tree.column('salary', width=75, anchor="center")

        #add headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('full_name', text='ФИО')
        self.tree.heading('phone_number', text='Номер телефона')
        self.tree.heading('email', text='Электронная почта')
        self.tree.heading('salary', text='Зарплата')

        # add bind for delete
        self.tree.bind("<Delete>", lambda ev: self.remove())
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.view_records()

        #scrollbar
        scrlbar = tk.Scrollbar(toolbar2, command=self.tree.yview)
        scrlbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrlbar.set)


    def record(self, full_name: str, phone: str, email: str, salary: int):
        """records data to database"""

        self.db.insert_data(full_name, phone, email, salary)
        self.view_records()
    
    def update(self, full_name: str, phone: str, email: str, salary: int):
        """updates data to database"""
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.update_data(id, full_name, phone, email, salary)
        self.view_records()

    #init "add employeer"
    def open_add_dialog(self):
        AddDialog(self).init_child()
    
    #init "update employeer"
    def open_update_dialog(self):
        UpdateDialog(self).init_update()
    
    #init "search"
    def open_search_dialog(self):
        SearchDialog(self).init_search()

    def search(self, name):
        for child in self.tree.get_children():
            self.tree.delete(child)
        
        self.db.cur.execute('SELECT * FROM employeer WHERE instr(full_name, ?) > 0', (name,))

        r = self.db.cur.fetchall()

        for child in r:
            self.tree.insert('', 'end', values=child)

    #remove employeer
    def remove(self):
        for id in self.tree.selection():
            self.db.remove_data(self.tree.set(id, '#1'))
        
        self.view_records()
    
    #add data to tree (TreeView)
    def view_records(self):
        """Adds data to TreeView"""

        #clear old data
        for child in self.tree.get_children():
            self.tree.delete(child)
        
        self.db.cur.execute("SELECT * FROM employeer")

        #fill new data
        data = self.db.cur.fetchall()
        for dat in data:
            self.tree.insert('', 'end', values=dat)