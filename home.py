from constants import *
import math
from customtkinter import *
from PIL import Image
from expenses import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import to_rgb, to_hex
import numpy as np
from tkcalendar import Calendar
import constants as const

today = datetime.now().date()
expenses = load_expenses()
TODAYTOT = total(expenses_by_day(expenses))
WEEKTOT = total(expenses_by_week(expenses))
MONTHTOT = total(expenses_by_month(expenses))

TOTALS = [TODAYTOT, WEEKTOT, MONTHTOT]

validate_num = None
validate_hrs = None
validate_mins = None

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

def refresh():
    global today, expenses, TODAYTOTAL, WEEKTOTAL, MONTHTOTAL, TOTALS
    today = datetime.now().date()
    expenses = load_expenses()
    TODAYTOT = total(expenses_by_day(expenses))
    WEEKTOT = total(expenses_by_week(expenses))
    MONTHTOT = total(expenses_by_month(expenses))

    TOTALS = [TODAYTOT, WEEKTOT, MONTHTOT]


def format (n, i=4, exact=False):
    if not n:
        return '0.00'
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

def color_gradient(n, c1, c2):
    c1_rgb = np.array(to_rgb(c1))
    if c2:
        c2_rgb = np.array(to_rgb(c2))
        colors = [(1-t) * c1_rgb +t * c2_rgb for t in np.linspace(0, 1, n)]
    else:
        colors = [(1-t)*c1_rgb + t * np.array([1, 1, 1]) for t in np.linspace(0, 1, n)]
    return [to_hex(color) for color in colors]

def small_sec(master, i, span):
    sec = CTkFrame(master, width=270, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=1, column=i*2+1, sticky="nsew", pady=20, padx=10)
    r = (TOTALS[i] - const.LIMITS[i]) / const.LIMITS[i] * 100
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
                    text=const.UNIT + format(TOTALS[i], 6),
                    text_color="white",
                    font=("Roboto bold", 30))
    rate = CTkLabel(right,
                    text= format(r)+"%",
                    text_color= "red" if r > 0 else "#00FF00",
                    font=("Roboto bold", 30),
                    fg_color="transparent",
                    anchor='s',
                    width=120
                    )
    limits = ["Daily limit: ", "Weekly limit: ", "Monthly limit: "]
    limit = CTkLabel(right,
                     text= limits[i] + const.UNIT + format(const.LIMITS[i], 5),
                     font=("Roboto bold", 12),
                     text_color="white",
                     fg_color="transparent",
                     anchor="s")
    title.grid(sticky="SW", padx=5)
    amnt.grid(sticky="NW")
    rate.pack(side="top")
    limit.pack(side="right", padx=5)
    return sec

def add_expense_sec(master, app):
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

    def add():
        category = cat.get()
        title = ttl.get()
        amount = float(amnt.get())
        time = hrs.get() + ":"+ mins.get() +" " + per.get()
        note = nt.get("1.0", "end")
        add_expense(title, category, amount, time, note)
        refresh()
        app.change()

    btn = CTkButton(form, text="Add Expense",
                    fg_color=dark_bg,
                    text_color="white",
                    corner_radius=14,
                    font=("Roboto bold", 16),
                    height=36,
                    hover_color="black",
                    command = lambda: add())
    btn.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10, padx=5)

class graph_section:
    def __init__(self, frame, mode="categories", title="Categories"):
        master = CTkFrame(frame,fg_color="transparent", corner_radius=24,)
        master.pack(fill="both", expand=True, pady=7, padx=20)
        
        self.title = CTkLabel(master,
                        text=title,
                        font=("Roboto bold", 24),
                        text_color="white")
        self.title.grid(row=0, sticky="new", pady=5)

        self.head = CTkFrame(master, fg_color="transparent")
        self.head.grid(row=1,  sticky="new",  pady=7)
        self.head.grid_columnconfigure(1, weight=1)

        self.body = CTkFrame(master, fg_color="transparent")
        self.body.grid(row=2, sticky="nsew",  pady=7)

        master.grid_columnconfigure(0, weight=1)

        self.type_picker = CTkOptionMenu(self.head, values=["Monthly", "Weekly", "Daily", "Range", "Total"], fg_color=dark_bg,
                    button_color=dark_bg, button_hover_color=clr1, dropdown_hover_color=light_bg,
                corner_radius=6, height=28, width=100, command=self.select_range)
        self.type_picker.grid(row=0, column=0, sticky="nsew", pady=10)

        self.range_picker = CTkFrame(self.head, fg_color="transparent",width=100)
        self.range_picker.grid(row=0, column=2, pady=10, sticky="nsew")

        self.from_date = datetime.now().date()
        self.to_date = datetime.now().date()
        self.selected_date = datetime.now().date()

        self.from_btn = CTkButton(self.range_picker, text='from', width=50,
                fg_color=dark_bg, hover_color="black", height=28,
                command= lambda: self.date_picker(self.set_from_date))
        self.from_btn.pack(side="left", fill='x', expand=True, padx=10)

        self.to_btn = CTkButton(self.range_picker, text='to', width=50,
                        fg_color=dark_bg, hover_color="black", height=28,
                        command= lambda: self.date_picker(self.set_to_date))
        self.to_btn.pack(side="right", fill='x', expand=True)
        
        self.date_picker_btn = CTkButton(self.head, text=str(today),
                    fg_color=dark_bg, hover_color="black", height=28,
                    command= lambda: self.date_picker(self.select_date))
        self.date_picker_btn.grid(row=0, column=2, pady=10, sticky="nsew")

        self.graph_func = self.pie if mode == 'categories' else self.bar
        self.graph_func()

    def select_range(self,  type_):
        if type_ == 'Range':
            self.range_picker.tkraise()
        else:
            self.date_picker_btn.tkraise()
        self.graph_func()

    def set_from_date(self, date_str):
        self.from_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        self.from_btn.configure(text=f"{date_str[:-4]}{date_str[-2:]}")
        self.graph_func()

    def set_to_date(self, date_str):
        self.to_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        self.to_btn.configure(text=f"{date_str[:-4]}{date_str[-2:]}")
        self.graph_func()
    
    def select_date(self, date_str):
        self.selected_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        self.graph_func()

    def date_picker(self, funct):
        def select(top, date_str):
            top.destroy()
            funct(date_str)

        top = CTkToplevel(self.head, fg_color=sec_bg)
        top.title("Select Date")
        top.geometry("300x300")
        top.attributes("-topmost", True)
        top.focus()
        calendar = Calendar(top, selectmode="day", date_pattern="dd-mm-yyyy", maxdate=datetime.now(), 
                            selectbackground = light_bg, disabledbackground = dark_bg, weekendforeground = "tomato", width=400)
        calendar.pack(fill="both", expand=True, pady=15, padx=15)

        btn = CTkButton(top, text="Select", fg_color=dark_bg, text_color="white",
                        corner_radius=14, font=("Roboto bold", 16), height=36,
                        hover_color="black", command=lambda: select(top, calendar.get_date()))
        btn.pack(pady=10)

    def pie(self):
        data = None
        match(self.type_picker.get()):
            case 'Daily':
                lbl = self.selected_date .strftime("Day: %b-%d-%Y")
                data = expenses_by_day(expenses, self.selected_date)
            case 'Monthly':
                lbl = self.selected_date .strftime("Month: %B")
                data = expenses_by_month(expenses, self.selected_date.year, self.selected_date.month)
            case 'Weekly':
                lbl = self.selected_date .strftime("Week: %U %Y")
                data = expenses_by_week(expenses, self.selected_date)
            case 'Range':
                lbl = self.from_date.strftime("From: %b-%d-%Y   ") + self.to_date.strftime("To: %b-%d-%Y")
                data = expenses_between_days(expenses, self.from_date, self.to_date)
            case 'Total':
                lbl = "Total expense"
                data = expenses
        data = category_total(data)
        self.graph = CTkFrame(self.body, fg_color="transparent")
        self.graph.grid(row=2, column=0, columnspan=2, padx=0, pady=0, sticky="NEW")
        if(data):
            fig = Figure(figsize = (3.2, 3), dpi=100, facecolor=sec_bg, layout="constrained")
            plot = fig.add_subplot(111)
            categories = data.keys()
            amounts = list(data.values())
            colors = color_gradient(len(amounts), light_bg, dark_bg)
            colors = [y for _, y in sorted(zip(sorted(amounts), colors), key=lambda pair: amounts.index(pair[0]))]
            
            plot.pie(amounts, autopct='%1.1f%%', textprops={'color': 'White'}, colors = colors)
            plot.legend(labels=categories, loc='lower left')
            self.canvas = canvas = FigureCanvasTkAgg(fig, self.graph)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

            canvas.get_tk_widget().bind("<Button-1>", lambda event: show_pie_chart(data, lbl))


        canvas.get_tk_widget().bind("<Configure>", lambda event: self.on_resize(event))

    def on_resize(self, event):
        self.canvas.get_tk_widget().config(width=event.width, height=event.height)

    def bar(self):
        data = None
        match(self.type_picker.get()):
            case 'Daily':
                data = timeperiod_total(expenses_by_week(expenses, self.selected_date), 'Daily')
                labels = [date.strftime("%Y-%m-%d") for date in data.keys()]
            case 'Monthly':
                data = timeperiod_total(expenses, 'Monthly')
                labels = [f"{year}-{month:02d}" for year, month in data.keys()]
            case 'Weekly':
                data = timeperiod_total(expenses_by_month(expenses, self.selected_date.year, self.selected_date.month), 'Weekly')
                labels = [f"Week {week}" for week in data.keys()]
            case 'Range':
                data = timeperiod_total(expenses_between_days(expenses, self.from_date, self.to_date), 'Daily')
                labels = [date.strftime("%d-%m") for date in data.keys()]
            case 'Total':
                data = timeperiod_total(expenses, 'Monthly')
                labels = [f"{year}-{month:02d}" for year, month in data.keys()]
        self.graph = CTkFrame(self.body, fg_color="transparent")
        self.graph.grid(row=2, column=0, columnspan=2, padx=7, pady=7, sticky="NSEW")
        if(data):
            fig = Figure(figsize = (3.2, 3), dpi=100, facecolor=sec_bg, layout="constrained")
            plot = fig.add_subplot(111, facecolor=sec_bg)
            amounts = list(data.values())
            colors = color_gradient(len(amounts), light_bg, dark_bg)
            colors = [y for _, y in sorted(zip(sorted(amounts), colors), key=lambda pair: amounts.index(pair[0]))]
            plot.bar(labels, amounts, color=colors)
            plot.yaxis.axis_name = "Expenses"

            canvas = FigureCanvasTkAgg(fig, self.graph)
            canvas.draw() 
            canvas.get_tk_widget().pack(fill="both", expand=True)

            canvas.get_tk_widget().bind("<Button-1>", lambda event: show_bar_chart(data, self.type_picker.get()))

def add_category_sec(master):
    sec = CTkFrame(master, width=580, height=400, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=3, column=3, sticky="nsew", padx=20, pady=20)

    graph_sec = graph_section(sec, 'categories', title="Categories")

def add_trend_sec(master):
    
    sec = CTkFrame(master, width=580, height=400, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=3, column=5, sticky="nsew", padx=20, pady=20)

    graph_sec = graph_section(sec, 'trends', title="Trends")

def getHome(app):
    body = CTkFrame(app.win, fg_color="transparent", corner_radius=0)

    t_sec = small_sec(body, 0, "Today     ")
    w_sec = small_sec(body, 1, "This Week ")
    m_sec = small_sec(body, 2, "This Month")

    add_expense_sec(body, app)
    add_category_sec(body)
    add_trend_sec(body)
    
    body.grid_rowconfigure([0, 2, 4], weight=3, minsize=5)
    body.grid_rowconfigure(1, weight=1)
    body.grid_rowconfigure(3, weight=10)
    body.grid_columnconfigure([0, 2, 4, 6], weight=1, minsize=20)
    body.grid_columnconfigure([1, 3, 5], weight=2)

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