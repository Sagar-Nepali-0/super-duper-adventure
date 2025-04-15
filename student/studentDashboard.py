import tkinter as tk
from tkinter import ttk
from datetime import datetime

class AddUserApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Add User")
        self.geometry("800x500")
        self.configure(bg='black')

        self.create_widgets()

    def create_widgets(self):
        # Left Panel
        left_frame = tk.Frame(self, width=200, bg="#d9d9d9")
        left_frame.pack(side="left", fill="y")

        logo = tk.Label(left_frame, text=".", bg="#d9d9d9", font=("Arial", 14))
        logo.pack(pady=20)

        user_icon = tk.Label(left_frame, text=" ", font=("Arial", 40), bg="#d9d9d9")
        user_icon.pack()

        student_name = tk.Label(left_frame, text="Student Thapa", font=("Arial", 12), bg="#d9d9d9")
        student_name.pack(pady=10)

        back_btn = tk.Button(left_frame, text="← Back")
        back_btn.pack(side="bottom", pady=20)

        # Right Panel
        right_frame = tk.Frame(self, bg="white")
        right_frame.pack(side="right", expand=True, fill="both")

        date_str = datetime.now().strftime("%m/%d/%Y\n%A")
        date_label = tk.Label(right_frame, text=date_str, font=("Arial", 10), anchor="e", bg="white")
        date_label.pack(anchor="ne", padx=10, pady=5)

        title_label = tk.Label(right_frame, text="Add User", font=("Arial", 16, "bold"), bg="white")
        title_label.pack(anchor="w", padx=20)

        sub_label = tk.Label(right_frame, text="Update Student Details", font=("Arial", 12, "bold"), bg="white")
        sub_label.pack(anchor="w", padx=20, pady=(10, 5))

        form_frame = tk.Frame(right_frame, bg="white")
        form_frame.pack(padx=20, pady=10)

        labels = ["ID", "Name", "DOB", "Address", "Grade", "Section", "Username", "Password"]
        self.entries = {}

        for i in range(4):  # Left column
            tk.Label(form_frame, text=labels[i], bg="white").grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[labels[i]] = entry

        for i in range(4, 8):  # Right column
            tk.Label(form_frame, text=labels[i], bg="white").grid(row=i - 4, column=2, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i - 4, column=3, padx=5, pady=5)
            self.entries[labels[i]] = entry

        save_btn = ttk.Button(right_frame, text="Save", command=self.save_user)
        save_btn.pack(anchor="e", padx=20, pady=10)

    def save_user(self):
        user_data = {label: entry.get() for label, entry in self.entries.items()}
        print("Saved User:", user_data)  # You can replace this with actual saving logic

if __name__ == "__main__":
    app = AddUserApp()
    app.mainloop()
