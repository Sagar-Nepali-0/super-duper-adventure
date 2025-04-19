import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import sys
import seaborn as sns

PASSWORD_FILE = "data/password.csv"
GRADE_DATA = "data/grade.csv"
ADMIN_FILE = "data/users/admin.csv"
STUDENT_FILE = "data/users/student.csv"
try:
    authentication = pd.read_csv(PASSWORD_FILE)
    read_gradeData = pd.read_csv(GRADE_DATA)
    admin_file = pd.read_csv(ADMIN_FILE)
    student_file = pd.read_csv(STUDENT_FILE)
    image_path = "img/logo.png"
except FileNotFoundError:
    authentication = pd.DataFrame(columns=["ID", "username", "password", "role"])
    read_gradeData = pd.DataFrame()
    admin_file = pd.DataFrame()
    student_file = pd.DataFrame()
    image_path = "img/logo.png"  # Default image path if the file is not found

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Log In")
        self.icon = tk.PhotoImage(file=image_path)  # Ensure the image is in the same directory or provide a full path
        self.root.iconphoto(True, self.icon)

        # Center the window on the screen
        window_width = 800
        window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Shared properties
        self.current_frame = None
        self.SIDEBAR_BG = "#828080"
        self.MAIN_BG = "#D9D9D9"
        self.HEADER_COLOR = "#828080"
        self.BUTTON_BG = "#D9D9D9"
        self.BUTTON_FG = "#000000"
        self.ENTRY_BG = "#FFFFFF"
        self.ENTRY_FG = "#000000"
        self.ERROR_COLOR = "#BE3D2A"
        self.SUCCESS_COLOR = "#3CB371"
        self.TEXT_COLOR = "#000000"
        self.SIDEBAR_WIDTH = 350

    def switch_frame(self, frame_class, *args):
        """Destroy the current frame and replace it with a new one."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)


class LoginScreen(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent.root, bg="black")

        canvas = tk.Canvas(self, width=800, height=500, bg="black", highlightthickness=0)
        canvas.pack( expand=True)
        # a rectangle is created and divided into two parts
        canvas.create_rectangle(2, 80, 800, 400, fill="black", outline="black", width=1)
        x_center = (100 + 700) // 2  # Center of the rectangle
        canvas.create_line(x_center, 80, x_center, 400, fill="black", width=2) # Vertical line

        # Admin label
        canvas.create_text(480, 150, text="Admin", fill="white", font=("Arial", 29, "bold"))

        # Username label and entry
        canvas.create_text(465, 200, text="Username:", fill="white", font=("Arial", 14))
        username_entry = tk.Entry(self, width=15, font=("Arial", 14))
        canvas.create_window(600, 200, window=username_entry)

        # Password label and entry
        canvas.create_text(465, 250, text="Password:", fill="white", font=("Arial", 14))
        password_entry = tk.Entry(self, width=15, show="*", font=("Arial", 14))
        canvas.create_window(600, 250, window=password_entry)

        # Load and display the image
        image = Image.open(image_path)  # Load the image using PIL
        resized_image = image.resize((300, 300))  # Resize the image if needed
        image_tk = ImageTk.PhotoImage(resized_image)  # Convert the image for tkinter
        canvas.image_tk = image_tk 
        canvas.create_image(220, 260, image=image_tk, anchor="center")

        # Login button
        def login():
            username = username_entry.get()
            password = password_entry.get()

            # Filter the DataFrame to find the matching username and password
            user = authentication[
                (authentication["username"] == username) & (authentication["password"] == password)
            ]

            if not user.empty:  # Check if a matching user exists
                if user.iloc[0]["role"] == "student":  # Access the role of the first matching user
                    messagebox.showerror("Login Failed", "Student cannot log in as admin")
                else:
                    logged_in_username = user.iloc[0]["username"]
                    main_window.switch_frame(AdminDashboard, logged_in_username)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

        login_button = tk.Button(self, text="Log In", width=26, command=login, font=("Arial", 12, "bold"))
        canvas.create_window(552, 300, window=login_button)
        # Modify the Back button
        back_btn = tk.Button(
            self,
            text="Back",
            command=lambda: self.back_to_login(),
            width=26,
            font=("Arial", 12, "bold")
        )
        canvas.create_window(552, 350, window=back_btn)

    def back_to_login(self):
        """Close the current window and navigate back to login.py."""
        self.master.destroy()  # Close the current window
        # Dynamically determine the path to login.py
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  # Get the directory of the current script
        login_script = os.path.join(script_dir, "login.py")  # Construct the path to login.py
        os.system(f"python \"{login_script}\"")  # Use the constructed path to run login.py
 


class AdminDashboard(tk.Frame):  # Inherit directly from tk.Frame
    def __init__(self, parent, username):
        super().__init__(parent.root, bg=parent.MAIN_BG)  # Properly initialize as a tk.Frame
        self.parent = parent
        self.username = username
        self.pack(fill="both", expand=True)
        self.root = parent.root
        self.root.title("Admin Dashboard")

        # Create a sidebar with a fixed width
        sidebar_width = 200
        sidebar = tk.Frame(self, bg=parent.SIDEBAR_BG, width=sidebar_width)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Add a right border to the sidebar
        right_border = tk.Frame(sidebar, bg="black", width=2)  # Black border with 2px width
        right_border.pack(side="right", fill="y")

        # Create a date header
        date_header = tk.Frame(self, height=50)
        date_header.pack(side="top", fill="x")

        current_date = datetime.now().strftime("%A, %Y-%m-%d")
        date_label = tk.Label(date_header, text=current_date, font=("Arial", 14))
        date_label.pack(side="right", padx=10, pady=5)

        # Create a header
        header = tk.Frame(self, bg=parent.HEADER_COLOR, height=50)
        header.pack(side="top", fill="x")

        # Header label
        header_label = tk.Label(header, text="Admin Dashboard", bg=parent.HEADER_COLOR, font=("Arial", 20, "bold"))
        header_label.pack(pady=10, side="left")

        # Log Out button
        header_logout = tk.Button(header, text="Log Out", command=lambda: parent.switch_frame(LoginScreen, parent), font=("Arial", 13, "bold"))
        header_logout.pack(pady=10, padx=10, side="right")

        #text
        welcome_label = tk.Label(self, text=f"Welcome, {username}!", font=("Arial", 18, "bold"), bg=parent.MAIN_BG, fg="black")
        welcome_label.pack(pady=10)
        # how to use this software details
        details_label = tk.Label(self, text="This software is designed for managing student and admin accounts.", font=("Arial", 14), bg=parent.MAIN_BG, fg="black")
        details_label.pack(pady=10)

        # Divide the sidebar into two sections: upper and lower
        upper_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        upper_section.pack(fill="x", pady=(20, 10))

        # Add a horizontal line to divide the sections
        divider = tk.Frame(sidebar, bg="black", height=2)
        divider.pack(fill="x", pady=5)

        lower_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        lower_section.pack(fill="x", pady=(10, 20), expand=True)

        # Load and display the image in the upper section
        try:
            image = Image.open(image_path)
            resized_image = image.resize((120, 120))
            image_tk = ImageTk.PhotoImage(resized_image)
            self.sidebar_image = image_tk
            image_label = tk.Label(upper_section, image=image_tk, bg=parent.SIDEBAR_BG)
            image_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file not found: {image_path}")

        # Add buttons to the lower section

        add_user_button = tk.Button(
            lower_section,
            text="Add User",
            command=lambda: parent.switch_frame(AddUser, self.username),  # Switch to AddUser frame
            bg=parent.BUTTON_BG,
            fg=parent.BUTTON_FG,
            font=("Arial", 10, "bold"),
            width=15
        )
        add_user_button.pack(pady=(5, 5), anchor="n")  # Adjusted padding and anchored to the top


        delete_user_button = tk.Button(
            lower_section,
            text="Delete User",
            command=lambda: parent.switch_frame(DeleteUser, self.username),  # Pass only the required arguments
            bg=parent.BUTTON_BG,
            fg=parent.BUTTON_FG,
            font=("Arial", 10, "bold"),
            width=15,
        )
        delete_user_button.pack(pady=(5, 5), anchor="n")  # Adjusted padding and anchored to the top

        studentRecord_button = tk.Button(
            lower_section,
            text="Student Record",
            command=lambda: parent.switch_frame(StudentRecord, self.username),  # Pass only the required arguments
            bg=parent.BUTTON_BG,
            fg=parent.BUTTON_FG,
            font=("Arial", 10, "bold"),
            width=15,
        )
        studentRecord_button.pack(pady=(5, 5), anchor="n")  # Adjusted padding and anchored to the top

class AddUser(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent.root, bg=parent.MAIN_BG)
        self.parent = parent
        self.username = username
        self.pack(fill="both", expand=True)
        self.root = parent.root
        self.root.title("Add User")

        # Create a sidebar with a fixed width
        sidebar_width = 200
        sidebar = tk.Frame(self, bg=parent.SIDEBAR_BG, width=sidebar_width)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Add a right border to the sidebar
        right_border = tk.Frame(sidebar, bg="black", width=2)
        right_border.pack(side="right", fill="y")

        # Create a date header
        date_header = tk.Frame(self, height=50)
        date_header.pack(side="top", fill="x")

        current_date = datetime.now().strftime("%A, %Y-%m-%d")
        date_label = tk.Label(date_header, text=current_date, font=("Arial", 14))
        date_label.pack(side="right", padx=10, pady=5)

        # Create a header
        header = tk.Frame(self, bg=parent.HEADER_COLOR, height=50)
        header.pack(side="top", fill="x")

        # Header label
        header_label = tk.Label(header, text="Add User", bg=parent.HEADER_COLOR, font=("Arial", 20, "bold"))
        header_label.pack(pady=10, side="left")

        # Divide the sidebar into two sections: upper and lower
        upper_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        upper_section.pack(fill="x", pady=(20, 10))

        # Add a horizontal line to divide the sections
        divider = tk.Frame(sidebar, bg="black", height=2)
        divider.pack(fill="x", pady=5)

        lower_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        lower_section.pack(fill="x", pady=(10, 20), expand=True)

        # Load and display the image in the upper section
        try:
            image = Image.open(image_path)
            resized_image = image.resize((120, 120))
            image_tk = ImageTk.PhotoImage(resized_image)
            self.sidebar_image = image_tk
            image_label = tk.Label(upper_section, image=image_tk, bg=parent.SIDEBAR_BG)
            image_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file not found: {image_path}")

        # Sidebar content
        add_user_admin = tk.Button(
            lower_section,
            text="Admin",
            command=lambda: self.load_fields("admin"),  # Switch to AddUser frame
            bg=parent.BUTTON_BG,
            fg=parent.BUTTON_FG,
            font=("Arial", 10, "bold"),
            width=15
        )
        add_user_admin.pack(pady=(5, 5), anchor="n")  # Adjusted padding and anchored to the top


        add_user_student = tk.Button(
            lower_section,
            text="Student",
            command=lambda: self.load_fields("student"),  # Pass only the required arguments
            bg=parent.BUTTON_BG,
            fg=parent.BUTTON_FG,
            font=("Arial", 10, "bold"),
            width=15,
        )
        add_user_student.pack(pady=(5, 5), anchor="n")  # Adjusted padding and anchored to the top

        back_btn = tk.Button(
            lower_section,
            text="Back",
            command=lambda: parent.switch_frame(AdminDashboard, self.username),  # Pass only the required arguments
            bg=parent.BUTTON_BG,
            fg=parent.BUTTON_FG,
            font=("Arial", 10, "bold"),
            width=15,
        )
        back_btn.pack(pady=(5, 5), anchor="n")

        # Main area
        self.main_area = tk.Frame(self, bg=parent.MAIN_BG)
        self.main_area.pack(fill="both", expand=True, padx=20, pady=20)

        # Default content
        tk.Label(self.main_area, text="Select a role to add a user", font=("Arial", 18, "bold"), bg=parent.MAIN_BG, fg=parent.HEADER_COLOR).pack(pady=10)

    def load_fields(self, role):
        # Clear the current content in main_area
        for widget in self.main_area.winfo_children():
            widget.destroy()

        # Define fields for admin and student
        admin_fields = ["ID", "Name", "Username", "Password"]
        student_fields = ["ID", "Name", "DOB", "Address", "Grade", "Section", "Username", "Password"]

        # Select fields based on role
        fields = admin_fields if role == "admin" else student_fields

        # Add a title
        tk.Label(
            self.main_area,
            text=f"Add {role.capitalize()} User",
            font=("Arial", 18, "bold"),
            bg=self.parent.MAIN_BG,
            fg="black"
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="w", padx=20)  # Aligned to the left with padx

        # Create entry fields dynamically
        self.entries = {}
        for i, field in enumerate(fields):
            tk.Label(
                self.main_area,
                text=field,
                bg=self.parent.MAIN_BG,
                fg="black"
            ).grid(row=1 + i, column=0, padx=(20, 10), pady=5, sticky="w")  # Aligned to the left with padx
            entry = tk.Entry(self.main_area, bg=self.parent.ENTRY_BG, fg=self.parent.ENTRY_FG)
            entry.grid(row=1 + i, column=1, padx=(10, 20), pady=5, sticky="w")  # Aligned to the left with padx
            self.entries[field] = entry

        # Save button
        tk.Button(
            self.main_area,
            text="Save",
            command=lambda: self.save_user(role),
            bg="#D9D9D9",
            fg=self.parent.BUTTON_FG
        ).grid(row=len(fields) + 1, column=0, columnspan=2, pady=20, padx=20, sticky="w")  # Aligned to the left

    def save_user(self, role):
        # Collect user data from the entries
        user_data = {field: entry.get() for field, entry in self.entries.items()}

        # Check for empty fields
        required_fields = ["ID", "Username", "Password"]
        if not all(user_data.get(field) for field in required_fields):
            messagebox.showerror("Error", "All required fields (ID, Username, Password) must be filled.")
            return

        # Define file paths and fields based on role
        file_paths = {"admin": ADMIN_FILE, "student": STUDENT_FILE}
        role_fields = {
            "admin": ["ID", "Name", "Username", "Password"],
            "student": ["ID", "Name", "DOB", "Address", "Grade", "Section", "Username", "Password"]
        }

        file_path = file_paths[role]
        fields = role_fields[role]

        # Load the existing data for the role-specific file
        try:
            existing_data = pd.read_csv(file_path)
        except FileNotFoundError:
            # Create the file with headers if it doesn't exist
            existing_data = pd.DataFrame(columns=fields)
            existing_data.to_csv(file_path, index=False)

        # Check for duplicates in the role-specific file
        if user_data["ID"] in existing_data["ID"].astype(str).values:
            messagebox.showerror("Error", "Duplicate ID found. Please use a unique ID.")
            return
        if user_data["Username"] in existing_data["Username"].values:
            messagebox.showerror("Error", "Duplicate Username found. Please use a unique Username.")
            return

        # Append the new user data to the role-specific file
        new_user_df = pd.DataFrame([{field: user_data.get(field, "") for field in fields}])
        updated_data = pd.concat([existing_data, new_user_df], ignore_index=True)

        # Save the updated data to the role-specific file
        try:
            updated_data.to_csv(file_path, index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user to {file_path}: {e}")
            return

        # Update the password.csv file
        try:
            password_data = pd.read_csv(PASSWORD_FILE)
        except FileNotFoundError:
            # Create the file with headers if it doesn't exist
            password_data = pd.DataFrame(columns=["ID", "username", "password", "role"])
            password_data.to_csv(PASSWORD_FILE, index=False)

        # Check for duplicates in the password.csv file
        if user_data["ID"] in password_data["ID"].astype(str).values:
            messagebox.showerror("Error", "Duplicate ID found in password file. Please use a unique ID.")
            return
        if user_data["Username"] in password_data["username"].values:
            messagebox.showerror("Error", "Duplicate Username found in password file. Please use a unique Username.")
            return
        


        try:
            # Load the grade.csv file
            grade_data = pd.read_csv(GRADE_DATA)
        except FileNotFoundError:
            # Create the file with headers if it doesn't exist
            grade_data = pd.DataFrame(columns=["username", "english", "nepali", "math", "science", "computer"])
            grade_data.to_csv(GRADE_DATA, index=False)

        # Check if the 'username' column exists
        if "username" not in grade_data.columns:
            messagebox.showerror("Error", "The 'username' column is missing in the grade file.")
            return

        # Check for duplicates in the grade.csv file
        if user_data["Username"] in grade_data["username"].values:
            messagebox.showerror("Error", "Duplicate username found in grade file. Please use a unique username.")
            return

        # Append the new user's credentials to the grade.csv file
        new_grade_entry = {
            "username": user_data["Username"],  # Add the username
            "english": "",  # Initialize other columns as empty
            "nepali": "",
            "math": "",
            "science": "",
            "computer": ""
        }
        grade_data = pd.concat([grade_data, pd.DataFrame([new_grade_entry])], ignore_index=True)

        # Append the new user's credentials to the password.csv file
        new_password_entry = {
            "ID": user_data["ID"],
            "username": user_data["Username"],
            "password": user_data["Password"],
            "role": role
        }
        password_data = pd.concat([password_data, pd.DataFrame([new_password_entry])], ignore_index=True)

        # Save the updated password.csv file
        try:
            password_data.to_csv(PASSWORD_FILE, index=False)
            grade_data.to_csv(GRADE_DATA, index=False)
            messagebox.showinfo("Saved", f"{role.capitalize()} user added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update password file: {e}")

class DeleteUser(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent.root, bg=parent.MAIN_BG)
        self.parent = parent
        self.username = username
        self.pack(fill="both", expand=True)
        self.root = parent.root
        self.root.title("Delete User")

        # Create a sidebar with a fixed width
        sidebar_width = 200
        sidebar = tk.Frame(self, bg=parent.SIDEBAR_BG, width=sidebar_width)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Add a right border to the sidebar
        right_border = tk.Frame(sidebar, bg="black", width=2)
        right_border.pack(side="right", fill="y")

        # Create a date header
        date_header = tk.Frame(self, height=50)
        date_header.pack(side="top", fill="x")

        current_date = datetime.now().strftime("%A, %Y-%m-%d")
        date_label = tk.Label(date_header, text=current_date, font=("Arial", 14))
        date_label.pack(side="right", padx=10, pady=5)

        # Divide the sidebar into two sections: upper and lower
        upper_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        upper_section.pack(fill="x", pady=(20, 10))

        # Add a horizontal line to divide the sections
        divider = tk.Frame(sidebar, bg="black", height=2)
        divider.pack(fill="x", pady=5)

        lower_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        lower_section.pack(fill="x", pady=(10, 20), expand=True)

        # Load and display the image in the upper section
        try:
            image = Image.open(image_path)
            resized_image = image.resize((120, 120))
            image_tk = ImageTk.PhotoImage(resized_image)
            self.sidebar_image = image_tk
            image_label = tk.Label(upper_section, image=image_tk, bg=parent.SIDEBAR_BG)
            image_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file not found: {image_path}")

        # Add buttons to the lower section
        back_button = tk.Button(lower_section, text="Back", command=lambda: parent.switch_frame(AdminDashboard, username),
                                bg=parent.BUTTON_BG, fg=parent.BUTTON_FG, font=("Arial", 10, "bold"), width=15)
        back_button.pack(pady=(5, 5), anchor="n")

        # Create a header
        header = tk.Frame(self, bg=parent.HEADER_COLOR, height=50)
        header.pack(side="top", fill="x")

        # Header label
        header_label = tk.Label(header, text="Delete User", bg=parent.HEADER_COLOR, font=("Arial", 20, "bold"))
        header_label.pack(pady=10, side="left")

        # Form frame for delete user functionality
        form_frame = tk.Frame(self, bg=parent.MAIN_BG)
        form_frame.pack(pady=50)

        # User ID entry
        tk.Label(form_frame, text="Enter User ID to Delete:", bg=parent.MAIN_BG, font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.user_id_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.user_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Delete button
        delete_button = tk.Button(
            form_frame,
            text="Delete",
            command=self.delete_user,
            bg=parent.BUTTON_BG,
            fg="black",
            font=("Arial", 14, "bold"),
            border= 6
        )
        delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def delete_user(self):
        user_id = self.user_id_entry.get()
        if not user_id:
            messagebox.showerror("Error", "Please enter a User ID.")
            return

        try:
            df = pd.read_csv(PASSWORD_FILE)
            if user_id not in df["ID"].astype(str).values:
                messagebox.showerror("Error", f"User ID {user_id} not found.")
                return

            df = df[df["ID"].astype(str) != user_id]
            df.to_csv(PASSWORD_FILE, index=False)
            messagebox.showinfo("Success", f"User ID {user_id} deleted successfully.")
            self.parent.switch_frame(DeleteUser, self.username)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

class StudentRecord(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent.root, bg=parent.MAIN_BG)
        self.parent = parent
        self.username = username
        self.pack(fill="both", expand=True)
        self.root = parent.root
        self.root.title("Student Record")

        # Create a sidebar with a fixed width
        sidebar_width = 200
        sidebar = tk.Frame(self, bg=parent.SIDEBAR_BG, width=sidebar_width)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Add a right border to the sidebar
        right_border = tk.Frame(sidebar, bg="black", width=2)
        right_border.pack(side="right", fill="y")

        # Create a date header
        date_header = tk.Frame(self, height=50)
        date_header.pack(side="top", fill="x")

        current_date = datetime.now().strftime("%A, %Y-%m-%d")
        date_label = tk.Label(date_header, text=current_date, font=("Arial", 14))
        date_label.pack(side="right", padx=10, pady=5)

        # Divide the sidebar into two sections: upper and lower
        upper_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        upper_section.pack(fill="x", pady=(20, 10))

        # Add a horizontal line to divide the sections
        divider = tk.Frame(sidebar, bg="black", height=2)
        divider.pack(fill="x", pady=5)

        lower_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        lower_section.pack(fill="x", pady=(10, 20), expand=True)

        # Load and display the image in the upper section
        try:
            image = Image.open(image_path)
            resized_image = image.resize((120, 120))
            image_tk = ImageTk.PhotoImage(resized_image)
            self.sidebar_image = image_tk
            image_label = tk.Label(upper_section, image=image_tk, bg=parent.SIDEBAR_BG)
            image_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file not found: {image_path}")

        # Add buttons to the lower section
        back_button = tk.Button(lower_section, text="Back", command=lambda: parent.switch_frame(AdminDashboard, username),
                                bg=parent.BUTTON_BG, fg=parent.BUTTON_FG, font=("Arial", 10, "bold"), width=15)
        back_button.pack(pady=(5, 5), anchor="n")

        # Create a header
        header = tk.Frame(self, bg=parent.HEADER_COLOR, height=50)
        header.pack(side="top", fill="x")

        # Header label
        header_label = tk.Label(header, text="Student Record", bg=parent.HEADER_COLOR, font=("Arial", 20, "bold"))
        header_label.pack(pady=10, side="left")

        # Create a frame for the plot
        plot_frame = tk.Frame(self, bg=parent.MAIN_BG)
        plot_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create a Matplotlib figure
        figure = Figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111)

        # Set 'username' as index
        read_gradeData.set_index('username', inplace=True)

        # Plot heatmap using Seaborn
        sns.heatmap(read_gradeData, annot=True, fmt="d", cmap="YlGnBu", linewidths=0.5, ax=ax)

        # Customize the chart
        ax.set_title("Student Marks Heatmap", fontsize=16)
        ax.set_xlabel("Subjects")
        ax.set_ylabel("Students")

        # Embed the plot into the tkinter frame
        canvas = FigureCanvasTkAgg(figure, plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


def start_admin_gui(root):
    """Admin GUI starter function"""
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    # Initialize admin interface
    app = MainWindow(root)
    app.switch_frame(LoginScreen, app)
    return app