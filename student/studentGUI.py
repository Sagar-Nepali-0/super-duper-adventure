import tkinter as tk
from tkinter import messagebox
import csv


root = tk.Tk()
root.title("Student Login")
root.geometry("1000x1000")
root.config(bg="#2C3E50")

current_frame = None


SIDEBAR_BG = "#2C3E50"
MAIN_BG = "#34495E"
HEADER_COLOR = "#F39C12"
BUTTON_BG = "#1A1A1A"
BUTTON_FG = "#000000"
ENTRY_BG = "#1A1A1A"
ENTRY_FG = "#F7F9FB"


GREY_SIDEBAR_BG = "#7F8C8D"
GREY_MAIN_BG = "#BDC3C7"
GREY_HEADER_COLOR = "#2C3E50"
GREY_ENTRY_FG = "#2C3E50"

user_data = {}

def switch_frame(frame_func):
    global current_frame
    if current_frame:
        current_frame.destroy()
    current_frame = frame_func()
    current_frame.pack(fill="both", expand=True)

def login_screen():
    frame = tk.Frame(root, bg=MAIN_BG)

    tk.Label(frame, text="[LOGO]", font=("Arial", 14), bg=SIDEBAR_BG, fg="white", width=20, height=10).grid(row=0, column=0, rowspan=4, padx=20, pady=20)

    tk.Label(frame, text="Student Login", font=("Arial", 18, "bold"), bg=MAIN_BG, fg=HEADER_COLOR).grid(row=0, column=1, pady=(30, 10))
    tk.Label(frame, text="Username", bg=MAIN_BG, fg="black").grid(row=1, column=1)
    username_entry = tk.Entry(frame, bg="white", fg="black")
    username_entry.grid(row=1, column=2)

    tk.Label(frame, text="Password", bg=MAIN_BG, fg="white").grid(row=2, column=1)
    password_entry = tk.Entry(frame, show="*", bg="White", fg="black")
    password_entry.grid(row=2, column=2)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        try:
            with open("student.csv", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['username'] == username and row['password'] == password:
                        global user_data
                        user_data = row
                        switch_frame(student_dashboard)
                        return
                messagebox.showerror("Login Failed", "Invalid student credentials")
        except FileNotFoundError:
            messagebox.showerror("Error", "CSV file not found.")

    tk.Button(frame, text="Log In", command=login, bg="White", fg="Black").grid(row=3, column=1, columnspan=2, pady=10)
    return frame


def student_dashboard():
    frame = tk.Frame(root, bg=GREY_MAIN_BG)

    sidebar = tk.Frame(frame, width=150, bg=GREY_SIDEBAR_BG)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="[LOGO]", bg=GREY_SIDEBAR_BG, fg="white", height=5).pack(pady=10)
    tk.Button(sidebar, text="Log Out", command=lambda: switch_frame(login_screen), bg="white", fg=BUTTON_FG).pack(pady=80)

    
    main_area = tk.Frame(frame, bg=GREY_MAIN_BG)
    main_area.pack(fill="both", expand=True, padx=20, pady=20)
# ('Username', 'Student')
    welcome_label = tk.Label(main_area, text=f"Welcome, {user_data.get('Username', 'Student')}!", font=("Arial", 16, "bold"), bg=GREY_MAIN_BG, fg=GREY_HEADER_COLOR)
    welcome_label.pack(pady=(10, 5))
    intro_label = tk.Label(main_area, text="Access your academic info below:", font=("Arial", 12), bg=GREY_MAIN_BG, fg="black")
    intro_label.pack(pady=(0, 15))

    button_row = tk.Frame(main_area, bg=GREY_MAIN_BG)
    button_row.pack(pady=5)

    content_area = tk.Frame(main_area, bg=GREY_MAIN_BG)
    content_area.pack(fill="both", expand=True)

    def clear_content():
        for widget in content_area.winfo_children():
            widget.destroy()

    def show_profile():
        clear_content()
        tk.Label(content_area, text="Student Profile", font=("Arial", 18, "bold"), bg=GREY_MAIN_BG, fg=GREY_HEADER_COLOR).pack(pady=10)
        profile_keys = ["Id", "Fullname", "DOB", "Address", "GPA", "Section", "username"]
        for key in profile_keys:
            row = tk.Frame(content_area, bg=GREY_MAIN_BG)
            row.pack(anchor="w", pady=5)
            tk.Label(row, text=f"{key.capitalize()}:", fg="black", bg=GREY_MAIN_BG, width=15, anchor="w").pack(side="left")
            tk.Label(row, text=user_data.get(key, ""), fg=GREY_ENTRY_FG, bg=GREY_MAIN_BG).pack(side="left")

    def show_grades():
        clear_content()
        tk.Label(content_area, text="Your Grades", font=("Arial", 18, "bold"), bg=GREY_MAIN_BG, fg=GREY_HEADER_COLOR).pack(pady=10)

        subjects = ["Math", "Physic", "Chemistry", "Computer", "English"]
        for subject in subjects:
            row = tk.Frame(content_area, bg=GREY_MAIN_BG)
            row.pack(anchor="w", pady=5)
            tk.Label(row, text=f"{subject}:", fg="black", bg=GREY_MAIN_BG, width=15, anchor="w").pack(side="left")
            tk.Label(row, text=user_data.get(subject, "N/A"), fg=GREY_ENTRY_FG, bg=GREY_MAIN_BG).pack(side="left")

# okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk






    def show_eca():
        clear_content()
        tk.Label(content_area, text="Extracurricular Activities", font=("Arial", 18, "bold"), bg=GREY_MAIN_BG, fg=GREY_HEADER_COLOR).pack(pady=10)

        selected_ecas = user_data.get("eca", "").split(",") 
        selected_ecas = [eca.strip() for eca in user_data.get("eca", "").split(",")]


        def make_checkbox(label, category):
            var = tk.IntVar(value=1 if label in selected_ecas else 0)
            cb = tk.Checkbutton(content_area, text=label, variable=var, bg=GREY_MAIN_BG, fg="black", selectcolor=GREY_MAIN_BG)
            cb.pack(anchor="w")

        tk.Label(content_area, text="Sports and Physical Activities", font=("Arial", 14), bg=GREY_MAIN_BG, fg="black").pack(anchor="w", pady=5)
        for sport in ["Football", "Basketball"]:
            make_checkbox(sport, "Sports")

        tk.Label(content_area, text="Art and Culture", font=("Arial", 14), bg=GREY_MAIN_BG, fg="black").pack(anchor="w", pady=10)
        for art in ["Drawing", "Singing", "Dancing"]:
            make_checkbox(art, "Art")

        tk.Label(content_area, text="Technical", font=("Arial", 14), bg=GREY_MAIN_BG, fg="black").pack(anchor="w", pady=10)
        make_checkbox("Coding", "Technical")

    
    btn_style = {
        "bg": "white",
        "fg": "black",
        "font": ("Arial", 10),
        "width": 12,
        "height": 1,
    }

    tk.Button(button_row, text="Profile", command=show_profile, **btn_style).pack(side="left", padx=5)
    tk.Button(button_row, text="Grades", command=show_grades, **btn_style).pack(side="left", padx=5)
    tk.Button(button_row, text=" ECA", command=show_eca, **btn_style).pack(side="left", padx=5)

    return frame

switch_frame(login_screen)
root.mainloop()