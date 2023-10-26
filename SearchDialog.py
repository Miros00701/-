import tkinter as tk

#
# TODO: задача для Даши: оптимизировать код и изменить текст интерфейса
#
class SearchDialog(tk.Toplevel):
    def __init__(self, view) -> None:
        super().__init__()
        self.view = view

    #init widgets of child
    def init_search(self):
        self.title("Поиск сотрудника")
        self.geometry("500x150")
        self.resizable(False, False)

        #grab and focus set
        self.grab_set()
        self.focus_set()

        #label
        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=50, y=50)

        #entry
        self.input_name = tk.Entry(self)
        self.input_name.place(x=240, y=50)

        #Button "cancel"
        btn_close = tk.Button(self, text="Отмена", command=self.destroy)
        btn_close.pack(side=tk.BOTTOM, anchor='s')

        #Button "search"
        self.btn_search = tk.Button(self, text="Поиск")
        self.btn_search.bind("<Button-1>", lambda ev: (self.view.search(self.input_name.get()), self.destroy()), add="+")
        self.btn_search.pack(side=tk.BOTTOM, anchor='s')

        # Bind for SearchDialog
        self.bind("<Return>", lambda ev: (self.view.search(self.input_name.get()), self.destroy()), add="+")
