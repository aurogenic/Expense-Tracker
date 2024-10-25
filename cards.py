from constants import *
import math
from customtkinter import *
from PIL import Image
from home import format, init
from expenses import CATEGORIES, load_expenses, delete_expense, update_expense

edit_btn_img = None
UNIT = "$"


def update(x):
     print(x)

class EditWindow(CTkToplevel):
    def __init__(self, parent, expense):
        super().__init__(parent.win)
        self.app = parent
        self.title("Edit Expense")
        self.geometry("350x370")
        self.resizable =[False, False]

        self.attributes("-topmost", True)
        self.focus()

        self.configure(fg_color=sec_bg, corner_radius=24)
        validate_num = init(self)
        form = CTkFrame(self, fg_color="transparent", corner_radius=24,)
        form.pack(fill="both", expand=True, pady=7, padx=20)

        title = CTkLabel(form,
                        text="Edit Expense",
                        font=("Roboto bold", 24),
                        text_color="white",)
        title.grid(row=0, column=0, sticky="nsew", pady=5, columnspan=2)
        
        for i , txt in enumerate(["Category", "Title", "Amount", "Note"]):
            lbl = CTkLabel(form,
                            text=txt,
                            font=("Roboto bold", 15),
                            text_color="white",
                            anchor="w",
                            width=100)
            lbl.grid(row=i+1, column=0, pady=5, sticky="nsew")
            form.grid_rowconfigure(i, weight=1)

        form.grid_rowconfigure(4, weight=4)
        form.grid_rowconfigure(5, weight=1)
        form.grid_columnconfigure(1, weight=2)

        cat = CTkOptionMenu(form, values=CATEGORIES,
                            fg_color=dark_bg,
                            button_color=dark_bg,
                            button_hover_color=clr1,
                            dropdown_hover_color=light_bg,
                            corner_radius=6, height=28)
        cat.grid(row=1, column=1, sticky="nsew", pady=7)

        ttl = CTkEntry(form, border_width=0, corner_radius=6)
        ttl.grid(row=2, column=1, sticky="nsew", pady=7)

        amnt = CTkEntry(form, border_width=0, corner_radius=6,
                        validate="key", validatecommand=(validate_num, '%S'))
        amnt.grid(row=3, column=1, sticky="nsew", pady=7)


        nt = CTkTextbox(form, corner_radius=6, height=50, width=150)
        nt.grid(row=4, column=1, sticky="nsew", pady=7)

        cat.set(expense[2])
        ttl.insert(0, expense[1])
        amnt.insert(0, str(expense[3]))
        nt.insert("0.0", expense[-1])
        

        def update():
            category = cat.get()
            title = ttl.get()
            amount = amnt.get() if amnt.get() else expense[3]
            note = nt.get("1.0", "end")
            update_expense(expense[0], title, category, amount, note)
            self.app.change()
            self.destroy()

        btn = CTkButton(form, text="Update",
                        fg_color=dark_bg,
                        text_color="white",
                        corner_radius=14,
                        font=("Roboto bold", 16),
                        height=36,
                        hover_color="black",
                        command = lambda: update())
        btn.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=10, padx=5)

class DeleteConfirmwindow(CTkToplevel):
    def __init__(self, frame: CTkFrame, app, id):
        super().__init__(frame)
        self.app = app
        self.title("Edit Expense")
        x = app.win.winfo_x()+ frame.winfo_x() + frame.winfo_width()//2 
        y = app.win.winfo_y()+ frame.winfo_y() + frame.winfo_height()//2
        self.geometry(f"100x60+{x}+{y}")
        self.resizable =[False, False]

        self.attributes("-topmost", True)
        self.focus()

        self.configure(fg_color=sec_bg, corner_radius=24)
        self.btn = CTkButton(self, text="Confirm Delete", text_color="red", fg_color="white", command=lambda: self.delete(id))
        self.btn.pack(side='bottom', padx=10, pady=10)

    def delete(self, i):
        delete_expense(i)
        self.app.change()
        self.destroy()

def Card(master, expense, app):
    card = CTkFrame(master, fg_color=sec_bg, corner_radius=18, height=200)
    
    header = CTkFrame(card, fg_color="transparent")
    header.pack(side="top",fill="x", padx=6, pady=4)

    time = CTkLabel(header, text_color="white", font=("Roboto", 12), text=expense[4].strftime("%I:%M %p"))
    time.pack(side="left", padx=10)

    date = CTkLabel(header, text_color="white", font=("Roboto", 12), text=expense[4].date())
    date.pack(side="left", padx=10)

    dlt_btn = CTkButton(header, width=16, text="X", font=("Roboto bold", 16),  fg_color="transparent",
                        text_color="red", hover_color="white", border_spacing=0,
                        command=lambda: DeleteConfirmwindow(card, app, expense[0]))
    dlt_btn.pack(side="right")

    edit_btn = CTkButton(header, image=edit_btn_img, text="", fg_color="transparent",
                    hover=False, width=16, command=lambda: EditWindow(app, expense))
    edit_btn.pack(side="right")


    title = CTkLabel(card, font=("Roboto bold", 20), text_color='white', text=expense[1][:20])
    title.pack(side="top")

    note = CTkLabel(card, font=("Roboto", 10), text_color="gray",
                    anchor="w", justify="left",text=expense[5], wraplength=180)
    note.pack(fill="both", expand=True, pady=2, padx=14)

    amnt = CTkLabel(card, font=("Roboto bold", 25),  text_color="white", text=UNIT+format(expense[3], 9))
    amnt.pack()

    cat = CTkLabel(card, font=("Roboto bold", 10), text_color="white", text=expense[2])
    cat.pack()
    return card

def getListPage(app):
    global edit_btn_img, win
    EXPENSES = load_expenses()
    edit_btn_img = CTkImage(Image.open("assets/edit.png"), size=(16, 16))

    COLS = 5
    body = CTkFrame(app.win, fg_color="transparent", corner_radius=0)
    body.pack(fill="both", expand=True)

    sec = CTkScrollableFrame(body, fg_color="transparent",
                             scrollbar_button_color=sec_bg,
                             scrollbar_button_hover_color=light_bg
                             )
    sec.pack(fill="both", expand=True)
    for i in range(COLS+1): 
        empty = CTkFrame(sec, fg_color="transparent", width=1)
        empty.grid(row=0, column=i*2)
    for i, expense in enumerate(EXPENSES):
        card = Card(sec, expense, app)
        card.grid(row = i//COLS, column = (i%COLS)*2+1, pady=20, sticky="NSEW")

    
    sec.grid_columnconfigure(list(range(COLS*2+1)), weight=1)
    sec.grid_columnconfigure([x*2+1 for x in range(COLS)], weight=0, minsize=280)

    sec.grid_rowconfigure(list(range(len(EXPENSES)//COLS + 1)), minsize=150, weight=1)
    return body
