import tkinter as tk
from datetime import datetime

# Helper to switch frames
def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.title("Student Management System")
root.geometry("800x500")
root.configure(bg='lightgray')

# ----------- SIDEBAR -----------
sidebar = tk.Frame(root, bg='gray', width=200)
sidebar.pack(side='left', fill='y')

logo_label = tk.Label(sidebar, text="Logo", bg='gray', font=('Arial', 16))
logo_label.pack(pady=20)

canvas = tk.Canvas(sidebar, width=100, height=100, bg='darkgray')
canvas.pack()
canvas.create_oval(10, 10, 90, 90, fill='black')

student_name = tk.Label(sidebar, text="Student Thapa", bg='gray', font=('Arial', 12))
student_name.pack(pady=10)

btn_update_profile = tk.Button(sidebar, text="Update Profile", command=lambda: show_frame(profile_frame))
btn_update_profile.pack(pady=10)

btn_add_user = tk.Button(sidebar, text="Add User", command=lambda: show_frame(add_user_frame))
btn_add_user.pack(pady=10)

btn_back = tk.Button(sidebar, text="◀ Back", command=lambda: show_frame(profile_frame))
btn_back.pack(side='bottom', pady=10)

# ----------- TOP BAR -----------
top_bar = tk.Frame(root, bg='lightgray', height=40)
top_bar.pack(fill='x')

title = tk.Label(top_bar, text="Student Profile", font=('Arial', 16, 'bold'), bg='lightgray')
title.pack(side='left', padx=10)

logout_btn = tk.Button(top_bar, text="Log Out")
logout_btn.pack(side='right', padx=10)

date_label = tk.Label(top_bar, text=datetime.now().strftime("%m/%d/%Y\n%A"), bg='lightgray')
date_label.pack(side='right')

# ----------- CONTENT AREA -----------
content_area = tk.Frame(root, bg='white')
content_area.pack(fill='both', expand=True)

# ----------------- PROFILE FRAME -----------------
profile_frame = tk.Frame(content_area, bg='white')
profile_frame.place(relwidth=1, relheight=1)

# Tabs
tabs_frame = tk.Frame(profile_frame, bg='lightgray')
tabs_frame.pack(fill='x', pady=5)

for tab in ["Profile", "Grade", "ECA"]:
    tk.Button(tabs_frame, text=tab).pack(side='left', padx=5)

# Profile Fields
fields = ["ID", "Name", "DOB", "Address", "Grade", "Section"]
for idx, field in enumerate(fields):
    tk.Label(profile_frame, text=field, bg='white', font=('Arial', 12)).place(x=220 + (idx % 2) * 250, y=80 + (idx // 2) * 50)
    tk.Entry(profile_frame, width=25).place(x=300 + (idx % 2) * 250, y=80 + (idx // 2) * 50)

# ----------------- ADD USER FRAME -----------------
add_user_frame = tk.Frame(content_area, bg='white')
add_user_frame.place(relwidth=1, relheight=1)

tk.Label(add_user_frame, text="Add User", bg='lightgray', font=('Arial', 16, 'bold')).pack(anchor='nw', padx=10, pady=5)

tk.Label(add_user_frame, text="Update Student Details", font=('Arial', 14, 'bold'), bg='white').place(x=300, y=40)

fields_user = ["ID", "Name", "DOB", "Address", "Grade", "Section", "Username", "Password"]
for idx, field in enumerate(fields_user):
    x = 220 + (idx % 2) * 250
    y = 90 + (idx // 2) * 40
    tk.Label(add_user_frame, text=field, bg='white', font=('Arial', 12)).place(x=x, y=y)
    tk.Entry(add_user_frame, width=25, show="*" if field == "Password" else "").place(x=x + 80, y=y)

tk.Button(add_user_frame, text="Save").place(x=670, y=300)

# Initialize first view
show_frame(profile_frame)

root.mainloop()
