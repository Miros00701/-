
from MainForm import MainForm
from tkinter import Tk
from database import Database

# starts program
if __name__ == "__main__":
    root = Tk()
    root.title("Список сотрудников компании")
    root.geometry("800x465")
    root.resizable(False,False)

    db = Database("Employeers.db")

    app = MainForm(root, db)
    app.init_main()
    
    root.mainloop()
