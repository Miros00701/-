import tkinter as tk
from tkinter.messagebox import showerror

class AddDialog(tk.Toplevel):

    def __init__(self, view) -> None:
        super().__init__()
        self.view = view

    #init widgets of child
    def init_child(self):
        self.title("Добавить сотрудника")
        self.geometry("600x200")
        self.resizable(False, False)

        #grab and focus set
        self.grab_set()
        self.focus_set()

        #labels
        label_name = tk.Label(self, text='ФИО')
        label_phone = tk.Label(self, text='Номер телефона')
        label_email = tk.Label(self, text='Почта')
        label_salary = tk.Label(self, text ='Зарплата')
        label_name.place(x=60, y=20)
        label_phone.place(x=60, y=50)
        label_email.place(x=60, y=80)
        label_salary.place(x=60, y=110)

        self.entry_name = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_salary = tk.Entry(self)
        self.entry_name.place(x=220, y=20)
        self.entry_phone.place(x=220, y=50)
        self.entry_email.place(x=220, y=80)
        self.entry_salary.place(x =220,y= 110)
        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=220, y=160)

        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: (self.view.record(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            int(self.entry_salary.get())
        ), self.destroy()))
        self.btn_ok.place(x=290, y=160)

        # Bind for AddDialog
        self.bind('<Return>', lambda ev: (self.view.record(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            int(self.entry_salary.get())
        ), self.destroy()))


class UpdateDialog(AddDialog):
    def __init__(self, view) -> None:
        super().__init__(view)
        self.init_child()

    #init update
    def init_update(self): 
        if self.get_data() is IndexError:
            return self.destroy()
        self.title("Изменить информацию о сотруднике")
        self.btn_ok.destroy()

        # Button "update"
        self.btn_upd = tk.Button(self, text="Изменить")
        self.btn_upd.bind("<Button-1>", lambda ev: 
        (
            self.view.update
            (
                self.entry_name.get(),
                self.entry_phone.get(),
                self.entry_email.get(),
                int(self.entry_salary.get())
            ), 
            self.destroy()
        ))
        self.btn_upd.place(x=300, y=160)

        # Bind for AddDialog
        self.bind('<Return>', lambda ev: (self.view.update(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            int(self.entry_salary.get())
        ), self.destroy()))
    
    #get data from selected item in TreeView
    def get_data(self):
        try:
            id = self.view.tree.set(self.view.tree.selection()[0], "#1")
            self.view.db.cur.execute('SELECT * FROM employeer WHERE id = ?', (id,))
            row = self.view.db.cur.fetchone()
            self.entry_name.insert(0, row[1])
            self.entry_phone.insert(0, row[2])
            self.entry_email.insert(0, row[3])
            self.entry_salary.insert(0, row[4])
        except:
            showerror("Error", "Не был выделен 1 сотрудник")
            return IndexError
    