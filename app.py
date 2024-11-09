from customtkinter import *
from home import *
from cards import *
from config import *

class App:
    def __init__(self):
        self.win = CTk(fg_color=dark_bg)
        self.win.configure(title="Expense Tracker")
        self.win.geometry("1200x600")
        self.win._set_appearance_mode("dark")
        init(self.win)

        self.navbar = get_navbar(self)
        self.body = getHome(self)
        self.win.minsize(1000, 550)


        self.win.mainloop()

    def change(self, n=0):
        self.body.destroy()
        refresh()
        match(n):
            case 1:
                self.body = getListPage(self)

            case 2:
                print("view page")
            case 3:
                self.body = getConfigPage(self)
            case default:
                self.body = getHome(self)

    def update_expense(self, id, category, title, amount, note):
        print(id, category, title, amount, note)
        self.change(1)

app = App()