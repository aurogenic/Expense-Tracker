from constants import *
import math
from customtkinter import *
from PIL import Image

UNIT = "$"
LIMITS = [150, 1200.00, 4500.00]
TOTALS = [140, 1401.00, 2410]

CATEGORIES = ["Food and Snacks", "Shopping and Clothing", "Mediacl and Healthcar", "Utilities", "Rent and Recharges", "Miscellaneous"]

TODAYTOT = 0
WEEKTOT = 0
MONTHTOT = 0


validate_num = None
validate_hrs = None
validate_mins = None


#images referneces
logo_img = CTkImage(Image.open("assets/logo.png"), size = (300, 50))
config_logo_img = CTkImage(Image.open("assets/config.png"), size = (50, 50))

def get_navbar(app):
    nav_bar = CTkFrame(app.win, height=60, fg_color=light_bg, corner_radius=0)
    nav_bar.pack(fill="x")

    nav_left = CTkFrame(nav_bar, fg_color="transparent", height=60)
    nav_right = CTkFrame(nav_bar, fg_color="transparent", height=60)

    nav_left.pack(side="left", padx=10, ipady=0)
    nav_right.pack(side="right", padx=10)

    home_btn = CTkButton(nav_left,
                        image=logo_img,
                        text="",
                        fg_color="transparent",
                        hover=False,
                        command=lambda: app.change(0))

    home_btn.pack(side="left")

    config_btn = CTkButton(nav_right,
                        image=config_logo_img,
                        text="",
                        fg_color="transparent",
                        hover=False,
                        width=50,
                        command=lambda: app.change(3))
    config_btn.pack(side="right")

    expenses_btn = CTkButton(nav_right,
                            text="Expenses",
                            fg_color=dark_bg,
                            font=("Roboto bold", 24),
                            height=40,
                            command=lambda: app.change(1),
                            hover_color="black")
    expenses_btn.pack(side="left")

    return nav_bar


def format (n, i=4, exact=False):
    i -= 1 if n < 0 else 0
    sign = '-' if n<0 else ''
    n = abs(n)
    digits = int(math.log10(n)) + 1
    if digits <= i or i < 3:
        i -= digits
        i = i if (exact or i < 3) else 2
        st = str( round(n, i) + 1 / 10**(i+1))[:i+1+digits]
        st = st if i > 0 else st[:-1]
        return  sign + st
    suffices = ['', 'k', 'M', 'B', 'T']
    mg = min((digits - 1) // 3, len(suffices) -1)
    n = n / 10**(mg * 3)
    return  sign + format(n, i-1) + suffices[mg]    

def small_sec(master, i, span):
    sec = CTkFrame(master, width=270, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=1, column=i*2+1, sticky="nsew", pady=20)
    r = (TOTALS[i] - LIMITS[i]) / LIMITS[i] * 100
    left = CTkFrame(sec, fg_color="transparent", )
    right = CTkFrame(sec, fg_color="transparent", bg_color="transparent", corner_radius=24)
    left.pack(side="left", pady=10, padx=10)
    right.pack(side="right", pady=10, padx=10)
    title = CTkLabel(left,
                    text=span,
                    text_color="white",
                    font=("Roboto bold", 14),
                    width=100,
                    anchor="w"
                    )
    amnt = CTkLabel(left,
                    text=UNIT + format(TOTALS[i], 6),
                    text_color="white",
                    font=("Roboto bold", 30))
    rate = CTkLabel(right,
                    text= format(r)+"%",
                    text_color= "red" if r > 0 else "green",
                    font=("Roboto bold", 30),
                    fg_color="transparent",
                    anchor='s',
                    width=120
                    )
    limits = ["Daily limit: ", "Weekly limit: ", "Monthly limit: "]
    limit = CTkLabel(right,
                     text= limits[i] + UNIT + format(LIMITS[i], 5),
                     font=("Roboto bold", 12),
                     text_color="white",
                     fg_color="transparent",
                     anchor="s")
    title.grid(sticky="SW", padx=5)
    amnt.grid(sticky="NW")
    rate.pack(side="top")
    limit.pack(side="right", padx=5)
    return sec

def add_expense_sec(master):
    sec = CTkFrame(master, width=270, height=400, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)

    form = CTkFrame(sec, fg_color="transparent", corner_radius=24,)
    form.pack(fill="both", expand=True, pady=7, padx=20)

    title = CTkLabel(form,
                     text="Add Expense",
                     font=("Roboto bold", 24),
                     text_color="white",)
    title.grid(row=0, column=0, sticky="nsew", pady=5, columnspan=2)
    
    for i , txt in enumerate(["Category", "Title", "Amount", "Time", "Note"]):
        lbl = CTkLabel(form,
                        text=txt,
                        font=("Roboto bold", 15),
                        text_color="white",
                        anchor="w",
                        width=100)
        lbl.grid(row=i+1, column=0, pady=5, sticky="nsew")
        form.grid_rowconfigure(i, weight=1)

    form.grid_rowconfigure(5, weight=4)
    form.grid_rowconfigure(6, weight=1)
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

    tm = CTkFrame(form, fg_color="transparent")
    tm.grid(row=4, column=1, sticky="nsew", pady=7)

    hrs = CTkEntry(tm, width=40, validate="key", validatecommand=(validate_hrs, '%P'))
    mins = CTkEntry(tm, width=40, validate="key", validatecommand=(validate_mins, '%P'))
    per = CTkOptionMenu(tm, width=80, values=["AM", "PM"],
                        fg_color=dark_bg, dropdown_hover_color=light_bg,
                        button_color=dark_bg, button_hover_color=clr1)

    hrs.pack(side="left", fill="both", expand=True)
    mins.pack(side="left", fill="both", expand=True, padx=5)
    per.pack(side="right", expand=False)

    nt = CTkTextbox(form, corner_radius=6, height=50, width=150)
    nt.grid(row=5, column=1, sticky="nsew", pady=7)

    def get_values():
        category = cat.get()
        title = ttl.get()
        amount = amnt.get()
        time = hrs.get() + mins.get() + per.get()
        note = nt.get("1.0", "end")
        print("category: ", category , "\ntitle: ", title, "\namount: ", amount, "\ntime: ", time, "\nNote: ", note)

    btn = CTkButton(form, text="Add Expense",
                    fg_color=dark_bg,
                    text_color="white",
                    corner_radius=14,
                    font=("Roboto bold", 16),
                    height=36,
                    hover_color="black",
                    command = lambda: get_values())
    btn.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10, padx=5)


def add_category_sec(master):
    sec = CTkFrame(master, width=270, height=400, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=3, column=3, sticky="nsew", padx=20, pady=20)
    sub =  CTkFrame(sec, fg_color="transparent", corner_radius=24,)
    sub.pack(fill="both", expand=True, pady=7, padx=20)

    title = CTkLabel(sub,
                     text="Categories",
                     font=("Roboto bold", 24),
                     text_color="white")
    title.grid(row=0, column=0, sticky="nsew", pady=5, columnspan=2)

    m1 = CTkOptionMenu(sub, values=["Daily", "Weekly", "Monthly"],
                        fg_color=dark_bg,
                        button_color=dark_bg,
                        button_hover_color=clr1,
                        dropdown_hover_color=light_bg,
                        corner_radius=6, height=28, width=100)
    m1.grid(row = 1, column=0, sticky="nsew", pady=5, padx=10)

    def get_range():
        type = m1.get()
        if type == "Daily":
             return ['12-10-2024', '13-10-2024', '14-10-2024','15-10-2024','16-10-2024','17-10-2024','18-10-2024']
        if type=="Weekly":
            return ["01-07/10/24", "08-14/10/24", "15-21/10/24", "22-28/10/24"]
        if type=="Monthly":
            return [x+" 2024" for x in ["Jan", "Feb", "Oct", "Dec"]]

    m2 = CTkOptionMenu(sub, values=get_range(),
                        fg_color=dark_bg,
                        button_color=dark_bg,
                        button_hover_color=clr1,
                        dropdown_hover_color=light_bg,
                        corner_radius=6, height=28)
    m2.grid(row = 1, column=1, sticky="nsew", pady=5, padx=10)

    sub.grid_columnconfigure(0, weight=1)
    sub.grid_columnconfigure(1, weight=1)

def add_trend_sec(master):
    sec = CTkFrame(master, width=270, height=400, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=3, column=5, sticky="nsew", padx=20, pady=20)
    sub =  CTkFrame(sec, fg_color="transparent", corner_radius=24,)
    sub.pack(fill="both", expand=True, pady=7, padx=20)

    title = CTkLabel(sub,
                     text="Expense Trends",
                     font=("Roboto bold", 24),
                     text_color="white")
    title.grid(row=0, column=0, sticky="nsew", pady=5, columnspan=2)

    m1 = CTkOptionMenu(sub, values=["Daily", "Weekly", "Monthly"],
                        fg_color=dark_bg,
                        button_color=dark_bg,
                        button_hover_color=clr1,
                        dropdown_hover_color=light_bg,
                        corner_radius=6, height=28, width=100)
    m1.grid(row = 1, column=0, sticky="nsew", pady=5, padx=10)

    def get_range():
        type = m1.get()
        if type == "Daily":
             return ['12-10-2024', '13-10-2024', '14-10-2024','15-10-2024','16-10-2024','17-10-2024','18-10-2024']
        if type=="Weekly":
            return ["01-07/10/24", "08-14/10/24", "15-21/10/24", "22-28/10/24"]
        if type=="Monthly":
            return [x+" 2024" for x in ["Jan", "Feb", "Oct", "Dec"]]

    m2 = CTkOptionMenu(sub, values=get_range(),
                        fg_color=dark_bg,
                        button_color=dark_bg,
                        button_hover_color=clr1,
                        dropdown_hover_color=light_bg,
                        corner_radius=6, height=28)
    m2.grid(row = 1, column=1, sticky="nsew", pady=5, padx=10)

    sub.grid_columnconfigure(0, weight=1)
    sub.grid_columnconfigure(1, weight=1)

def getHome(app):
    body = CTkFrame(app.win, fg_color="transparent", corner_radius=0)

    t_sec = small_sec(body, 0, "Today     ")
    w_sec = small_sec(body, 1, "This Week ")
    m_sec = small_sec(body, 2, "This Month")
    for i in range(4):
            empty =  CTkFrame(body, width=20, fg_color="transparent", height=0)
            empty.grid(row=1, column=i*2, sticky="nsew", padx=10)
    for i in range(3):
            empty =  CTkFrame(body, height=5, fg_color="transparent", width=0)
            empty.grid(row=i*2, column=0, sticky="nsew", padx=10)

    add_expense_sec(body)
    
    add_category_sec(body)
    
    add_trend_sec(body)

 
    
    body.grid_rowconfigure(0, weight=3)
    body.grid_rowconfigure(1, weight=1)
    body.grid_rowconfigure(2, weight=3)
    body.grid_rowconfigure(3, weight=10)
    body.grid_rowconfigure(4, weight=3)
    for i in range(7):
        body.grid_columnconfigure(i, weight=1)

    
    body.pack(fill="both", expand=True)

    return body


def init(win):
     
    def validate_num_inp(char):
        return char.isdigit() or char in [' ', '.']

    def validate_time_inp(inp, max):
        return inp =="" or (inp.isdigit() and len(inp) < 3 and 0 <= int(inp) <= max)

    global validate_num, validate_hrs, validate_mins
    
    validate_num = win.register(lambda x: validate_num_inp(x))
    validate_hrs = win.register(lambda x: validate_time_inp(x, 12))
    validate_mins = win.register(lambda x: validate_time_inp(x, 60))

    return validate_num