from constants import *
import math
from customtkinter import *
from PIL import Image
from home import format, init

CATEGORIES = ["Food and Snacks", "Shopping and Clothing", "Mediacl and Healthcar", "Utilities", "Rent and Recharges", "Miscellaneous"]

edit_btn_img = None
UNIT = "$"
EXPENSES = [
    [0, "Prateek Birthday", "Miscellaneous", 100.00, "12/10/2024", "12:36 PM", "To celebrate Prateek's birthday, we went to Street Cafe where we all collectively bought a cake which cost 500 in total."],
    [1, "Grocery Shopping", "Utilities", 150.25, "13/10/2024", "10:45 AM", "Bought groceries including vegetables, fruits, and other essentials for the week."],
    [2, "Electricity Bill", "Utilities", 75.00, "14/10/2024", "03:20 PM", "Paid the monthly electricity bill for the apartment."],
    [3, "Netflix Subscription", "Miscellaneous", 12.99, "14/10/2024", "07:15 PM", "Renewed the monthly Netflix subscription."],
    [4, "Pharmacy Purchase", "Medical and Healthcare", 35.60, "15/10/2024", "11:30 AM", "Purchased medicines for a cold and cough from the local pharmacy."],
    [5, "Mobile Recharge", "Rent and Recharges", 20.00, "15/10/2024", "09:00 PM", "Recharged the mobile with a monthly plan."],
    [6, "Lunch at Cafe", "Food and Snacks", 45.00, "16/10/2024", "01:00 PM", "Had lunch with friends at the nearby cafe, shared a pizza and drinks."],
    [7, "Winter Clothes Shopping", "Shopping and Clothing", 120.50, "16/10/2024", "05:45 PM", "Bought a winter jacket and a pair of gloves for the upcoming cold season."],
    [8, "Doctor Consultation", "Medical and Healthcare", 50.00, "17/10/2024", "10:00 AM", "Visited the doctor for a routine check-up and consultation."],
    [9, "Monthly Rent", "Rent and Recharges", 800.00, "17/10/2024", "11:00 AM", "Paid the rent for the apartment for the month of October."],
    [10, "Bus Pass", "Utilities", 40.00, "18/10/2024", "08:30 AM", "Purchased a monthly bus pass for commuting to work."],
    [11, "Snacks for Meeting", "Food and Snacks", 25.00, "18/10/2024", "03:00 PM", "Bought snacks for a team meeting at the office."],
    [12, "New Shoes", "Shopping and Clothing", 60.00, "19/10/2024", "04:00 PM", "Purchased a pair of running shoes for daily exercise."],
    [13, "Dentist Appointment", "Medical and Healthcare", 80.00, "19/10/2024", "10:30 AM", "Visited the dentist for a cleaning and a filling."],
    [14, "Gas Bill", "Utilities", 30.00, "20/10/2024", "02:00 PM", "Paid the gas bill for the apartment."],
    [15, "Dinner with Family", "Food and Snacks", 100.00, "20/10/2024", "07:00 PM", "Had a family dinner at a restaurant, shared various dishes."],
    [16, "Laptop Repair", "Miscellaneous", 85.00, "21/10/2024", "01:45 PM", "Got the laptop repaired due to overheating issues."],
    [17, "Clothing Sale", "Shopping and Clothing", 45.99, "22/10/2024", "12:15 PM", "Bought a few t-shirts and jeans during a sale."],
    [18, "Water Bill", "Utilities", 25.00, "22/10/2024", "11:00 AM", "Paid the monthly water bill for the apartment."],
    [19, "Birthday Gift for Friend", "Miscellaneous", 50.00, "23/10/2024", "06:30 PM", "Bought a gift for a friend's birthday, including a watch and a greeting card."],
    [20, "Lunch at Work", "Food and Snacks", 15.50, "23/10/2024", "12:00 PM", "Had lunch at work with colleagues, ordered a sandwich and coffee."],
    [21, "Monthly Gym Membership", "Miscellaneous", 40.00, "24/10/2024", "08:00 AM", "Paid for the gym membership for the month of October."],
]


def update(x):
     print(x)

class EditWindow(CTkToplevel):
    def __init__(self, parent, expense):
        super().__init__(parent.win)
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
        

        def get_values():
            category = cat.get()
            title = ttl.get()
            amount = amnt.get()
            note = nt.get("1.0", "end")
            parent.update_expense(expense[0], category, title, amount, note)

        btn = CTkButton(form, text="Add Expense",
                        fg_color=dark_bg,
                        text_color="white",
                        corner_radius=14,
                        font=("Roboto bold", 16),
                        height=36,
                        hover_color="black",
                        command = lambda: get_values())
        btn.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=10, padx=5)

def Card(master, expense, app):
        

    card = CTkFrame(master, fg_color=sec_bg, corner_radius=18)
    
    header = CTkFrame(card, fg_color="transparent")
    header.pack(side="top",fill="x", padx=5, pady=3)

    time = CTkLabel(header, text_color="white", font=("Roboto", 12), text=expense[5])
    time.pack(side="left", padx=10)

    date = CTkLabel(header, text_color="white", font=("Roboto", 12), text=expense[4])
    date.pack(side="left", padx=10)

    dlt_btn = CTkButton(header, width=16, text="X", font=("Roboto bold", 16),  fg_color="transparent", text_color="red", hover_color="white", border_spacing=0)
    dlt_btn.pack(side="right")

    edit_btn = CTkButton(header, image=edit_btn_img, text="", fg_color="transparent",
                    hover=False, width=16, command=lambda: EditWindow(app, expense))
    edit_btn.pack(side="right")


    title = CTkLabel(card, font=("Roboto bold", 20), text_color='white', text=expense[1])
    title.pack(side="top")

    note = CTkLabel(card, font=("Roboto bold", 10), text_color="white",
                    anchor="center", justify="center",text=expense[6], wraplength=160)
    note.pack(fill="y", expand=True, pady=0)

    amnt = CTkLabel(card, font=("Roboto bold", 25),  text_color="white", text=UNIT+format(expense[3], 9))
    amnt.pack()

    cat = CTkLabel(card, font=("Roboto bold", 10), text_color="white", text=expense[2])
    cat.pack()
    return card

def getListPage(app):
    global edit_btn_img, win
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

    sec.grid_rowconfigure(list(range(len(EXPENSES)//COLS + 1)), minsize=300, weight=1)
    return body
