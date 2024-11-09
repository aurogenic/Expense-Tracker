import math
from customtkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image
import home
from constants import *
from expenses import export_data,import_data, export_to_csv, clear_data
import constants as const

def add_config_sec(master,  app):
    sec = CTkFrame(master, width=350, height=400, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

    form = CTkFrame(sec, fg_color="transparent", corner_radius=24,)
    form.pack(fill="both", expand=True, pady=12, padx=30)

    title = CTkLabel(form,
                     text="Configuration",
                     font=("Roboto bold", 30),
                     text_color="white",)
    title.grid(row=0, column=0, sticky="nsew", columnspan=2)
    
    for i , txt in enumerate(["Unit", "Daily Limit", "Weekly Limit", "Monlthly Limit"]):
        lbl = CTkLabel(form,
                        text=txt,
                        font=("Roboto bold", 20),
                        text_color="white",
                        anchor="w",
                        width=100)
        lbl.grid(row=i+1, column=0, pady=5, sticky="nsew")
        form.grid_rowconfigure(i, weight=1)

    units_btn = CTkOptionMenu(form, values=list(UNITS),
                        fg_color=dark_bg,
                        button_color=dark_bg,
                        button_hover_color=clr1,
                        dropdown_hover_color=light_bg,
                        corner_radius=6, height=20, font=('Roboto', 18))
    units_btn.grid(row=1, column=1, sticky="nsew", pady=12)
    units_btn.set(get_currency())

    daily_limit_btn = CTkEntry(form, border_width=0, corner_radius=6, font=('Roboto', 18),
                               placeholder_text=int(const.LIMITS[0]), justify="right",
                    validate="key", validatecommand=(home.validate_num, '%S'))
    daily_limit_btn.grid(row=2, column=1, sticky="nsew", pady=12)

    weekly_limit_btn = CTkEntry(form, border_width=0, corner_radius=6, font=('Roboto', 18),
                                 placeholder_text=int(const.LIMITS[1]), justify="right",
                    validate="key", validatecommand=(home.validate_num, '%S'))
    weekly_limit_btn.grid(row=3, column=1, sticky="nsew", pady=12)

    monthly_limit_btn = CTkEntry(form, border_width=0, corner_radius=6, font=('Roboto', 18),
                                  placeholder_text=int(const.LIMITS[2]), justify="right",
                    validate="key", validatecommand=(home.validate_num, '%S'))
    monthly_limit_btn.grid(row=4, column=1, sticky="nsew", pady=12)

    def update():
        unit = units_btn.get()
        daily = float('0' + daily_limit_btn.get())
        weekly = float('0' + weekly_limit_btn.get())
        monthly = float('0' + monthly_limit_btn.get())
        update_config(unit, daily, weekly, monthly)
        app.change(3)

    save_btn = CTkButton(form, text="Add Expense",
                    fg_color=dark_bg,
                    text_color="white",
                    corner_radius=14,
                    font=("Roboto bold", 20),
                    height=56,
                    hover_color="black",
                    command = lambda: update())
    save_btn.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=7, padx=5)

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=2)
    form.grid_rowconfigure([0, 1, 2, 3, 4],weight=1)

def add_data_sec(master):
    sec = CTkFrame(master, width=350, height=400, fg_color=sec_bg, corner_radius=24)
    sec.grid(row=1, column=3, sticky="nsew", padx=20, pady=20)
    form = CTkFrame(sec, fg_color="transparent", corner_radius=24,)
    form.pack(fill="both", expand=True, pady=24, padx=30)

    title = CTkLabel(form,
                     text="Your Data",
                     font=("Roboto bold", 30),
                     text_color="white",)
    title.grid(row=0, column=0, sticky="nsew", columnspan=2)
    

    import_btn = CTkButton(form, text="Import Data",
                    fg_color=dark_bg,
                    text_color="white",
                    corner_radius=14,
                    font=("Roboto bold", 20),
                    height=56,
                    hover_color="black",
                    command = lambda: get_import_file())
    import_btn.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=15, padx=5)

    export_btn = CTkButton(form, text="Export Data",
                    fg_color=dark_bg,
                    text_color="white",
                    corner_radius=14,
                    font=("Roboto bold", 20),
                    height=56,
                    hover_color="black",
                    command = lambda: export_file())
    export_btn.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=15, padx=5)

    tocsv_btn = CTkButton(form, text="Export to CSV",
                    fg_color=dark_bg,
                    text_color="white",
                    corner_radius=14,
                    font=("Roboto bold", 20),
                    height=56,
                    hover_color="black",
                    command = lambda: export_to_csv())
    tocsv_btn.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=15, padx=5)

    clear_btn = CTkButton(form, text="Clear Data",
                    fg_color=dark_bg,
                    text_color="white",
                    corner_radius=14,
                    font=("Roboto bold", 20),
                    height=56,
                    hover_color="red",
                    command = lambda: clear_data())
    clear_btn.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=15, padx=5)

    form.grid_columnconfigure(0, weight=1)
    form.grid_rowconfigure([0, 1, 2, 3, 4, 5],weight=1,minsize=10)
    
def getConfigPage(app):
    body = CTkFrame(app.win, fg_color="transparent", corner_radius=0)
    
    add_config_sec(body, app)
    add_data_sec(body)

    body.grid_columnconfigure([0, 2,  4], weight=1, minsize=60)
    body.grid_rowconfigure([0, 2], weight=1, minsize=5)
    body.grid_rowconfigure(1, weight=3)
    body.columnconfigure([1, 3],weight=2)

    body.pack(fill="both", expand=True)
    return body

def get_import_file():
    filename = askopenfilename()
    import_data(filename)

def export_file():
    filename = asksaveasfilename(defaultextension='.db', filetypes=[('database', '*.db'), ('csv', '*.csv')])
    export_data(filename)

def export_to_csv():
    filename = asksaveasfilename(defaultextension='.csv', filetypes=[ ('csv', '*.csv'), ('database', '*.db')])
    export_data(filename)

