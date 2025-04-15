import tkinter as tk
from tkinter import messagebox
from datetime import datetime

root = tk.Tk()
root.title("Institution Admin Panel")
root.geometry("800x500")
root.config(bg="#1E1E1E")

current_frame = None

SIDEBAR_BG = "#2E8B57"
MAIN_BG = "#2B2B2B"
HEADER_COLOR = "#F5C45E"
BUTTON_BG = "#444444"
BUTTON_FG = "#000000"
ENTRY_BG = "#333333"
ENTRY_FG = "#FFFFFF"
ERROR_COLOR = "#BE3D2A"
SUCCESS_COLOR = "#3CB371"
SIDEBAR_WIDTH = 350


def switch_frame(frame_func):
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = frame_func()
    current_frame.pack(fill="both", expand=True)


def login_screen():
    frame = tk.Frame(root, bg=MAIN_BG)

    inner_frame = tk.Frame(frame, bg=MAIN_BG)
    inner_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo = tk.Label(inner_frame, text="[LOGO]", font=("Arial", 14), bg=SIDEBAR_BG, fg="white", width=20, height=10)
    logo.grid(row=0, column=0, rowspan=4, padx=20, pady=20)

    tk.Label(inner_frame, text="Admin", font=("Arial", 18, "bold"), bg=MAIN_BG, fg=HEADER_COLOR).grid(row=0, column=1, pady=(30, 10))
    tk.Label(inner_frame, text="Username", bg=MAIN_BG, fg="white").grid(row=1, column=1)
    username_entry = tk.Entry(inner_frame, bg=ENTRY_BG, fg=ENTRY_FG)
    username_entry.grid(row=1, column=2)

    tk.Label(inner_frame, text="Password", bg=MAIN_BG, fg="white").grid(row=2, column=1)
    password_entry = tk.Entry(inner_frame, show="*", bg=ENTRY_BG, fg=ENTRY_FG)
    password_entry.grid(row=2, column=2)

    def login():
        if username_entry.get() == "admin" and password_entry.get() == "admin":
            switch_frame(admin_dashboard)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(inner_frame, text="Log In", command=login, bg=BUTTON_BG, fg=BUTTON_FG).grid(row=3, column=1, columnspan=2, pady=10)

    return frame


def admin_dashboard():
    frame = tk.Frame(root, bg=MAIN_BG)

    sidebar = tk.Frame(frame, width=SIDEBAR_WIDTH, bg=SIDEBAR_BG)
    sidebar.pack(side="left", fill="y")

    logo = tk.Label(sidebar, text="[LOGO]", bg=SIDEBAR_BG, fg="white", height=5)
    logo.pack(pady=10)

    tk.Button(sidebar, text="Add User", command=lambda: switch_frame(add_user_screen), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=10)
    tk.Button(sidebar, text="Delete User", command=lambda: switch_frame(delete_user_screen), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=10)

    main_area = tk.Frame(frame, bg=MAIN_BG)
    main_area.pack(fill="both", expand=True)

    date_label = tk.Label(
        main_area,
        text=datetime.now().strftime("%A, %Y-%m-%d"),
        bg=MAIN_BG,
        fg="white",
        font=("Arial", 10)
    )
    date_label.pack(anchor="ne", padx=10, pady=5)

    tk.Label(main_area, text="Admin Profile", font=("Arial", 18, "bold"), bg=MAIN_BG, fg=HEADER_COLOR).pack(pady=10)
    tk.Label(main_area, text="Admin Thapa", font=("Arial", 14), bg=MAIN_BG, fg="white").pack(pady=10)
    tk.Button(main_area, text="Log Out", command=lambda: switch_frame(login_screen), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=5)

    return frame


def add_user_screen():
    frame = tk.Frame(root, bg=MAIN_BG)

    sidebar = tk.Frame(frame, width=SIDEBAR_WIDTH, bg=SIDEBAR_BG)
    sidebar.pack(side="left", fill="y")

    logo = tk.Label(sidebar, text="[LOGO]", bg=SIDEBAR_BG, fg="white", height=5)
    logo.pack(pady=10)

    tk.Label(sidebar, text="Role", bg=SIDEBAR_BG, fg="white", font=("Arial", 12)).pack(pady=(10, 0))
    tk.Button(sidebar, text="Admin", bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=5)
    tk.Button(sidebar, text="Student", bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=5)
    tk.Button(sidebar, text="← Back", command=lambda: switch_frame(admin_dashboard), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=20)

    main_area = tk.Frame(frame, bg=MAIN_BG)
    main_area.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(main_area, text="Add User", font=("Arial", 18, "bold"), bg=MAIN_BG, fg=HEADER_COLOR).grid(row=0, column=0, columnspan=4, pady=10)

    fields = ["ID", "Name", "DOB", "Address", "Grade", "Section"]
    entries = {}

    for i, field in enumerate(fields):
        tk.Label(main_area, text=field, bg=MAIN_BG, fg="white").grid(row=1 + i // 2, column=(i % 2) * 2)
        entry = tk.Entry(main_area, bg=ENTRY_BG, fg=ENTRY_FG)
        entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
        entries[field] = entry

    def save_user():
        user_data = {field: entry.get() for field, entry in entries.items()}
        print("Saving user:", user_data)
        messagebox.showinfo("Saved", "User added successfully")

    tk.Button(main_area, text="Save", command=save_user, bg=SUCCESS_COLOR, fg=BUTTON_FG).grid(row=5, column=0, columnspan=4, pady=20)

    return frame


def delete_user_screen():
    frame = tk.Frame(root, bg=MAIN_BG)

    sidebar = tk.Frame(frame, width=SIDEBAR_WIDTH, bg=SIDEBAR_BG)
    sidebar.pack(side="left", fill="y")

    logo = tk.Label(sidebar, text="[LOGO]", bg=SIDEBAR_BG, fg="white", height=5)
    logo.pack(pady=10)

    tk.Button(sidebar, text="← Back", command=lambda: switch_frame(admin_dashboard), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=20)

    main_area = tk.Frame(frame, bg=MAIN_BG)
    main_area.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(main_area, text="Delete User", font=("Arial", 18, "bold"), bg=MAIN_BG, fg=HEADER_COLOR).pack(pady=10)

    form_frame = tk.Frame(main_area, bg=MAIN_BG)
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="ID", bg=MAIN_BG, fg="white").grid(row=0, column=0, padx=10)
    id_entry = tk.Entry(form_frame, bg=ENTRY_BG, fg=ENTRY_FG)
    id_entry.grid(row=0, column=1, padx=10)

    def delete_user():
        user_id = id_entry.get()
        if user_id:
            print(f"Deleting user with ID: {user_id}")
            messagebox.showinfo("Deleted", f"User ID {user_id} deleted.")
        else:
            messagebox.showwarning("Error", "Please enter an ID.")

    tk.Button(main_area, text="Delete", command=delete_user, bg=ERROR_COLOR, fg=BUTTON_FG).pack()

    return frame


switch_frame(login_screen)
root.mainloop()