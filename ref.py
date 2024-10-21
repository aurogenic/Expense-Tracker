
import customtkinter as ctk
from pathlib import Path

# Constants
unit = "$"
daily_limit = 150.00
weekly_limit = 1050.00
monthly_limit = 4500.00

todays_exp_total = 43129.12
this_week_exp_total = 751190.35
this_month_exp_total = 3156297.47
todays_rate = 12.3
weeks_rate = -3.21
months_rate = -19.34


class HomeFrame:
    def __init__(self, root, frame_changer):
        # Create the main frame that will hold all sections
        main_frame = ctk.CTkFrame(root, width=1000, height=600)
        main_frame.pack(fill="both", expand=True)

        # Today Section
        self.create_section(main_frame, 60, 135, "Today", todays_exp_total, todays_rate, daily_limit)

        # This Week Section
        self.create_section(main_frame, 380, 135, "This Week", this_week_exp_total, weeks_rate, weekly_limit)

        # This Month Section
        self.create_section(main_frame, 700, 135, "This Month", this_month_exp_total, months_rate, monthly_limit)

        # Add Expense Section
        self.add_expense_section(main_frame)

        # Category-wise Comparison Section
        self.create_category_section(main_frame)

    def create_section(self, parent, x, y, title, total, rate, limit):
        # Create a frame with shadow and rounded corners for the section background
        section_frame = ctk.CTkFrame(parent, width=300, height=150, corner_radius=15)
        section_frame.place(x=x, y=y)

        # Title
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Roboto Bold", 14), text_color="white")
        title_label.place(x=15, y=10)

        # Total Expense
        total_label = ctk.CTkLabel(section_frame, text=unit + str(total), font=("Roboto Bold", 22), text_color="white")
        total_label.place(x=15, y=40)

        # Rate (with color change based on positive or negative rate)
        rate_label_color = "#00FF00" if rate > 0 else "#FF0000"
        rate_label = ctk.CTkLabel(section_frame, text=f"{rate}%", font=("Roboto Bold", 25), text_color=rate_label_color)
        rate_label.place(x=210, y=50)

        # Limit
        limit_label = ctk.CTkLabel(section_frame, text=f"{title.lower()} limit: {unit}{limit}", font=("Roboto", 12), text_color="gray")
        limit_label.place(x=15, y=90)

    def add_expense_section(self, parent):
        # Create frame for expense section
        expense_frame = ctk.CTkFrame(parent, width=300, height=300, corner_radius=15)
        expense_frame.place(x=60, y=300)

        # Labels
        expense_title = ctk.CTkLabel(expense_frame, text="Expense", font=("Roboto Bold", 20), text_color="white")
        expense_title.place(x=10, y=10)

        self.create_label(expense_frame, 10, 50, "Category:")
        self.create_label(expense_frame, 10, 90, "Title:")
        self.create_label(expense_frame, 10, 130, "Amount:")
        self.create_label(expense_frame, 10, 170, "Time:")
        self.create_label(expense_frame, 10, 210, "Note:")

        # Inputs
        self.cat_inp = ctk.CTkEntry(expense_frame, width=150)
        self.cat_inp.place(x=100, y=50)

        self.title_inp = ctk.CTkEntry(expense_frame, width=150)
        self.title_inp.place(x=100, y=90)

        self.amnt_inp = ctk.CTkEntry(expense_frame, width=150)
        self.amnt_inp.place(x=100, y=130)

        self.time_inp = ctk.CTkEntry(expense_frame, width=150)
        self.time_inp.place(x=100, y=170)

        self.note_inp = ctk.CTkTextbox(expense_frame, width=150, height=50)
        self.note_inp.place(x=100, y=210)

        # Add Expense Button
        self.add_expense_btn = ctk.CTkButton(expense_frame, text="Add Expense", corner_radius=8, command=self.add_expense_action)
        self.add_expense_btn.place(x=75, y=270)

    def create_category_section(self, parent):
        # Create frame for category section
        category_frame = ctk.CTkFrame(parent, width=300, height=300, corner_radius=15)
        category_frame.place(x=380, y=300)

        # Category Title
        category_title = ctk.CTkLabel(category_frame, text="Categories", font=("Roboto Bold", 20), text_color="white")
        category_title.place(x=10, y=10)

        # Add buttons for pie and bar
        pie_btn = ctk.CTkButton(category_frame, text="Pie Chart", width=100, corner_radius=8, command=lambda: print("Pie button clicked"))
        pie_btn.place(x=20, y=60)

        bar_btn = ctk.CTkButton(category_frame, text="Bar Chart", width=100, corner_radius=8, command=lambda: print("Bar button clicked"))
        bar_btn.place(x=150, y=60)

    def create_label(self, frame, x, y, text):
        label = ctk.CTkLabel(frame, text=text, font=("Roboto Bold", 16), text_color="white")
        label.place(x=x, y=y)

    def add_expense_action(self):
        # Action for adding expense goes here
        print("Add expense button clicked")
        
        # Clear inputs after adding an expense
        self.clear_inputs()

    def clear_inputs(self):
        """Clears all input fields."""
        self.cat_inp.delete(0, 'end')
        self.title_inp.delete(0, 'end')
        self.amnt_inp.delete(0, 'end')
        self.time_inp.delete(0, 'end')
        self.note_inp.delete('1.0', 'end')  # Textboxes require '1.0' for the first position to clear all text


# Initialize the CustomTkinter application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("1000x600")

    frame = HomeFrame(root, None)  # Adjust frame_changer accordingly
    root.mainloop()
