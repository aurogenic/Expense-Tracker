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

#images referneces
logo_img = CTkImage(Image.open("assets/logo.png"), size = (300, 50))
config_logo_img = CTkImage(Image.open("assets/config.png"), size = (50, 50))

def get_navbar(win, frame_changer,):
    nav_bar = CTkFrame(win, height=60, fg_color=light_bg, corner_radius=0)
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
                        command=lambda: frame_changer.change(0))

    home_btn.pack(side="left")

    config_btn = CTkButton(nav_right,
                        image=config_logo_img,
                        text="",
                        fg_color="transparent",
                        hover=False,
                        width=50,
                        command=lambda: frame_changer.change(3))
    config_btn.pack(side="right")

    expenses_btn = CTkButton(nav_right,
                            text="Expenses",
                            fg_color=dark_bg,
                            font=("Roboto bold", 24),
                            height=40,
                            command=lambda: frame_changer.change(1),
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
                     font=("Roboto bold", 10),
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
    empty = CTkFrame(sec, height=10, fg_color="transparent")
    empty.pack(side="top", fill="y")
    title = CTkLabel(sec,
                     text="Add Expense",
                     font=("Roboto bold", 30),
                     text_color="white",)
    title.pack(side="top", fill="x", pady=5, padx=10)

    form = CTkFrame(sec, fg_color="transparent", corner_radius=24,)
    form.pack(fill="both", expand=True, pady=7, padx=7)

    def get_l(master, txt):
        l = CTkLabel(master,
                        text=txt,
                        font=("Roboto bold", 15),
                        text_color="white",
                        anchor="w",
                        width=100)
        l.pack(side="left", anchor="w", fill = 'y')
        
    cat_sec = CTkFrame(form, fg_color="transparent", width=300)
    cat_sec.pack(fill="y", expand=True, padx=20)
    label = get_l(cat_sec, "Category")
    
    cat = CTkOptionMenu(cat_sec, values=CATEGORIES,
                        fg_color=dark_bg,
                        button_color=dark_bg,
                        button_hover_color="black",
                        dropdown_hover_color=light_bg,
                        corner_radius=6, height=28)
    cat.pack(side="right")

    sec = CTkFrame(form, fg_color="transparent")
    sec.pack(fill="y", expand=True, padx=20)
    label = get_l(sec, txt)
    inp = CTkEntry(sec, placeholder_text="Enter " + txt,
                    border_width=0, corner_radius=6)
    inp.pack(side="right")

        
    nsec = CTkFrame(form, fg_color="transparent")
    nsec.pack(fill="y", expand=True, padx=20)
    label = get_l(nsec, "Note: ")
    inp = CTkTextbox(nsec, height=45, width=140, corner_radius=8)
    inp.pack(side="right")

    def get_values():
        category = cat.get()
        print(category)

    btn = CTkButton(form, text="Add Expense",
                    fg_color=dark_bg,
                    text_color="white",
                    corner_radius=14,
                    font=("Roboto bold", 16),
                    height=36,
                    hover_color="black",
                    command = lambda: get_values())
    btn.pack(fill="x", expand=True,  pady=10, padx=60)

def add_grpah_sec(master, i):
    sec = CTkFrame(master, width=270, height=400, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)


def getHome(win, frame_changer):
    body = CTkFrame(win, fg_color="transparent", corner_radius=0)

    t_sec = small_sec(body, 0, "Today     ")
    w_sec = small_sec(body, 1, "This Week ")
    m_sec = small_sec(body, 2, "This Month")
    for i in range(4):
            empty =  CTkFrame(body, width=20, fg_color="transparent", height=0)
            empty.grid(row=1, column=i*2, sticky="nsew", padx=10)
    for i in range(3):
            empty =  CTkFrame(body, height=5, fg_color="transparent", width=0)
            empty.grid(row=i*2, column=0, sticky="nsew", padx=10)

    adder_sec = add_expense_sec(body)
    
    sec2 = CTkFrame(body, width=270, height=400, fg_color=sec_bg, corner_radius=24)
    sec2.grid(row=3, column=3, sticky="nsew", padx=20, pady=20)
    
    sec3 = CTkFrame(body, width=270, height=400, fg_color=sec_bg, corner_radius=24)
    sec3.grid(row=3, column=5, sticky="nsew", padx=20, pady=20)

 
    
    body.grid_rowconfigure(0, weight=3)
    body.grid_rowconfigure(1, weight=1)
    body.grid_rowconfigure(2, weight=3)
    body.grid_rowconfigure(3, weight=10)
    body.grid_rowconfigure(4, weight=3)
    for i in range(7):
        body.grid_columnconfigure(i, weight=1)

    
    body.pack(fill="both", expand=True)

    return body






