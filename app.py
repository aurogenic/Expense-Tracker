from customtkinter import *
from gui import *


class FrameChanger:
    def __init__(self, win):
        self.win = win

    def change(self, n):
        match(n):
            case 1:
                print("list page")
            case 2:
                print("view page")
            case 3:
                print("config page")
            case default:
                print("home page")

win = CTk(fg_color=dark_bg)
win.configure(title="Expense Tracker")
win.geometry("1000x550")
win._set_appearance_mode("dark")


frame_changer = FrameChanger(win)

navbar = get_navbar(win, frame_changer)
body = getHome(win, 1)

win.minsize(1000, 550)


win.mainloop()