import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import os
import sys


PASSWORD_FILE = "data/password.csv"
GRADE_DATA = "data/grade.csv"
STUDENT_FILE = "data/users/student.csv"
ECA__FILE = "data/eca.csv"
try:
    authentication = pd.read_csv(PASSWORD_FILE)
    read_gradeData = pd.read_csv(GRADE_DATA)
    student_file = pd.read_csv(STUDENT_FILE)
    eca_data = pd.read_csv(ECA__FILE)
    image_path = "img/logo.png"
    # Verify if the file exists
    with open(image_path, "rb") as f:
        pass
except FileNotFoundError:
    authentication = pd.DataFrame(columns=["ID", "username", "password", "role"])
    read_gradeData = pd.DataFrame()
    student_file = pd.DataFrame()
    eca_data = pd.DataFrame()
    image_path = None  # Set to None if the file is not found

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Login")
        self.icon = tk.PhotoImage(file=image_path)
        self.root.iconphoto(True, self.icon)

        # Window dimensions and positioning
        window_width = 800
        window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Color scheme
        self.SIDEBAR_BG = "#2C3E50"
        self.MAIN_BG = "#34495E"
        self.HEADER_COLOR = "#F39C12"
        self.BUTTON_BG = "#FFFFFF"
        self.BUTTON_FG = "#000000"
        self.ENTRY_BG = "#FFFFFF"
        self.ENTRY_FG = "#000000"
        self.TEXT_COLOR = "#FFFFFF"

        self.current_frame = None
        self.user_data = {}

    def switch_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.destroy()
        print(f"Switching to frame: {frame_class.__name__}")  # Debugging
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

class LoginScreen(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent.root, bg=main_window.MAIN_BG)
        
        canvas = tk.Canvas(self, width=800, height=500, bg="white")
        canvas.pack(expand=True)
        
        # Create login interface
        canvas.create_rectangle(100, 80, 700, 400, fill=main_window.SIDEBAR_BG, outline="black", width=1)
        x_center = (100 + 700) // 2
        canvas.create_line(x_center, 80, x_center, 400, fill="black", width=2)

        # Load and display image
        if image_path:
            image = Image.open(image_path)
            resized_image = image.resize((295, 295))
            image_tk = ImageTk.PhotoImage(resized_image)
            canvas.image_tk = image_tk
            canvas.create_image(250, 240, image=image_tk, anchor="center")
        else:
            messagebox.showerror("Error", "Logo image not found")

        # Login elements
        canvas.create_text(550, 150, text="Student Login", fill="black", font=("Arial", 29, "bold"))
        
        # Username
        canvas.create_text(465, 200, text="Username:", fill="black", font=("Arial", 14))
        self.username_entry = tk.Entry(self, width=15, font=("Arial", 14))
        canvas.create_window(600, 200, window=self.username_entry)
        
        # Password
        canvas.create_text(465, 250, text="Password:", fill="black", font=("Arial", 14))
        self.password_entry = tk.Entry(self, width=15, show="*", font=("Arial", 14))
        canvas.create_window(600, 250, window=self.password_entry)
        
        # Login button
        login_btn = tk.Button(self, text="Log In", command=lambda: self.authenticate(main_window), 
                            width=26, font=("Arial", 12, "bold"))
        canvas.create_window(552, 300, window=login_btn)

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
 
    def authenticate(self, main_window):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Filter the authentication DataFrame
        user = authentication[
            (authentication["username"] == username) & 
            (authentication["password"] == password) & 
            (authentication["role"] == "student")
        ]
        
        if not user.empty:
            # Fetch the student data
            student_data = student_file[student_file["username"] == username]
            print(student_data)  # Debugging: Check if student data is fetched correctly
            if not student_data.empty:
                student_data = student_data.iloc[0]
                main_window.user_data = {
                    "ID": student_data["ID"],
                    "Name": student_data["Name"],
                    "DOB": student_data["DOB"],
                    "Address": student_data["Address"],
                    "Grade": student_data["Grade"],
                    "Section": student_data["Section"],
                    "username": username,
                    "password": password
                }
                main_window.switch_frame(StudentDashboard)
            else:
                messagebox.showerror("Error", "Student data not found")
        else:
            messagebox.showerror("Error", "Invalid credentials")

class StudentDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent.root, bg=parent.MAIN_BG)
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.root = parent.root
        self.root.title("Student Dashboard")
        
        # Sidebar setup
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

        # Header
        header = tk.Frame(self, bg=parent.HEADER_COLOR, height=50)
        header.pack(side="top", fill="x")
        
        tk.Label(header, text="Student Dashboard", bg=parent.HEADER_COLOR, 
                font=("Arial", 20, "bold")).pack(pady=10, side="left")
        
        # Divide the sidebar into two sections: upper and lower
        upper_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        upper_section.pack(fill="x", pady=(20, 10))

        # Add a horizontal line to divide the sections
        divider = tk.Frame(sidebar, bg="black", height=2)
        divider.pack(fill="x", pady=5)

        lower_section = tk.Frame(sidebar, bg=parent.SIDEBAR_BG)
        lower_section.pack(fill="x", pady=(10, 20), expand=True)
        
        # Sidebar content
        if image_path:
            image = Image.open(image_path)
            resized_image = image.resize((120, 120))
            self.sidebar_image = ImageTk.PhotoImage(resized_image)
            image_label = tk.Label(upper_section, image=self.sidebar_image, bg=parent.SIDEBAR_BG)
            image_label.pack(pady=10)
        else:
            messagebox.showerror("Error", "Logo image not found")

        # Add buttons to the lower section
        add_update_button = tk.Button(
            lower_section,
            text="Update Profile",
            command=lambda: parent.switch_frame(ProfileUpdate, self.parent.user_data["username"]),
            bg=parent.BUTTON_BG,
            fg=parent.BUTTON_FG,
            font=("Arial", 10, "bold"),
            width=15
        )
        add_update_button.pack(pady=(5, 5), anchor="n")  # Adjusted padding and anchored to the top


        
        tk.Button(header, text="Log Out", command=lambda: parent.switch_frame(LoginScreen, parent), 
        bg=parent.BUTTON_BG, fg=parent.BUTTON_FG, font=("Arial", 12)).pack(pady=10, padx=10 ,side="right")        
        # Main content area
        main_area = tk.Frame(self, bg=parent.MAIN_BG)
        main_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Navigation buttons
        btn_frame = tk.Frame(main_area, bg=parent.MAIN_BG)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Profile", command=lambda: self.show_content("profile"), 
                width=15, font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Grades", command=lambda: self.show_content("grades"), 
                width=15, font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="ECA", command=lambda: self.show_content("eca"), 
                width=15, font=("Arial", 12)).pack(side="left", padx=5)
        
        # Content display area
        self.content_area = tk.Frame(main_area, bg=parent.MAIN_BG)
        self.content_area.pack(fill="both", expand=True)
        
        # Show default content
        self.show_content("profile")

    def show_content(self, section):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        if section == "profile":
            self.show_profile()
        elif section == "grades":
            self.show_grades()
        elif section == "eca":
            self.show_eca()  # Call the refactored show_eca method

    def show_profile(self):

        tk.Label(self.content_area, text="Student Profile", font=("Arial", 18, "bold"),
                bg=self.parent.MAIN_BG, fg="white").pack(pady=10, side="top")
        fields = ["ID", "Name", "DOB", "Address", "Grade", "Section"]
        for i, field in enumerate(fields):
            row = tk.Frame(self.content_area, bg=self.parent.MAIN_BG)
            row.pack(anchor="w", pady=5)
            tk.Label(row, text=f"{field}:", width=15, anchor="w", 
                    bg=self.parent.MAIN_BG, fg="white").pack(side="left")
            tk.Label(row, text=self.parent.user_data.get(field, ""), 
                    bg=self.parent.MAIN_BG, fg="white").pack(side="left")

            separator = tk.Frame(self.content_area, height=1, bg="white")
            separator.pack(fill="x", pady=5)

    def show_grades(self):
        tk.Label(self.content_area, text="Student Grades", font=("Arial", 18, "bold"),
                bg=self.parent.MAIN_BG, fg="white").pack(pady=10, side="top")
        grades = read_gradeData[read_gradeData["username"] == self.parent.user_data["username"]]
        if not grades.empty:
            subjects = ["english", "nepali", "math", "science", "computer"]
            for i, subject in enumerate(subjects):
                row = tk.Frame(self.content_area, bg=self.parent.MAIN_BG)
                row.pack(anchor="w", pady=5)
                tk.Label(row, text=f"{subject.capitalize()}:", width=15, anchor="w", 
                        bg=self.parent.MAIN_BG, fg="white").pack(side="left")
                tk.Label(row, text=grades.iloc[0].get(subject, "N/A"),  # Fallback to "N/A"
                        bg=self.parent.MAIN_BG, fg="white").pack(side="left")
        else:
            tk.Label(self.content_area, text="No grades available", 
                    bg=self.parent.MAIN_BG, fg="white").pack()


    def show_eca(self):
        # Add a header for the ECA section
        tk.Label(self.content_area, text="Extracurricular Activities",
                 font=("Arial", 18, "bold"), bg=self.parent.MAIN_BG, fg="white").pack(pady=10)

        try:
            # Filter the ECA data for the logged-in student
            student_eca = eca_data[eca_data["username"] == self.parent.user_data["username"]]

            if not student_eca.empty:
                student_eca = student_eca.iloc[0]  # Get the first (and only) row for the student

                # Iterate through activities, skipping the "username" column
                for activity in student_eca.index[1:]:  # Skip the "username" column
                    is_enrolled = student_eca[activity] == 1  # Check if the student is enrolled
                    var = tk.IntVar(value=1 if is_enrolled else 0)  # Initialize IntVar with the correct value

                    # Display activity as a checkbox (disabled to prevent modification)
                    tk.Checkbutton(self.content_area, text=activity.capitalize(),
                                   bg=self.parent.MAIN_BG, fg="white", selectcolor="black",
                                   state="disabled", variable=var).pack(anchor="w", padx=10, pady=5)
            else:
                # If no ECA data is found for the student
                tk.Label(self.content_area, text="No extracurricular activities found",
                         bg=self.parent.MAIN_BG, fg="white").pack(pady=10)
        except FileNotFoundError:
            # Handle the case where the ECA file is missing or empty
            tk.Label(self.content_area, text="ECA data file not found",
                     bg=self.parent.MAIN_BG, fg="red").pack(pady=10)
            
class ProfileUpdate(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent.root, bg=parent.MAIN_BG)
        self.parent = parent
        self.username = username  # Store the username
        self.pack(fill="both", expand=True)
        self.root = parent.root
        self.root.title("Profile Update")

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
        header_label = tk.Label(header, text="Update Personal Information", bg=parent.HEADER_COLOR, font=("Arial", 20, "bold"))
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

        # Add buttons to the lower section
        back_button = tk.Button(
            lower_section,
            text="Back",
            command=lambda: parent.switch_frame(StudentDashboard),  # Fixed Back button
            bg=parent.BUTTON_BG,
            fg=parent.BUTTON_FG,
            font=("Arial", 10, "bold"),
            width=15
        )
        back_button.pack(pady=(5, 5), anchor="n")

        # Display a header
        tk.Label(self, text=f"Update Profile for {self.username}", font=("Arial", 16, "bold"), bg=parent.MAIN_BG, fg="white").pack(pady=20)

        # Fields to update
        fields = ["ID", "Name", "DOB", "Address", "Grade", "Section", "username", "password"]
        self.entries = {}

        for field in fields:
            row = tk.Frame(self, bg=parent.MAIN_BG)
            row.pack(anchor="w", pady=5, padx=20)
            tk.Label(row, text=f"{field}:", width=15, anchor="w", bg=parent.MAIN_BG, fg="white").pack(side="left")

     # Allow all fields, including ID, to be editable
            entry = tk.Entry(row, font=("Arial", 12))
            entry.pack(side="left", fill="x", expand=True)
            self.entries[field] = entry

            # Pre-fill the entry with existing data
            entry.insert(0, self.parent.user_data.get(field, ""))

        # Save button
        tk.Button(self, text="Save", command=self.save_profile, font=("Arial", 12), bg=parent.BUTTON_BG, fg=parent.BUTTON_FG).pack(pady=20)

    def save_profile(self):
        # Collect user data from the entries
        user_data = {field: entry.get() for field, entry in self.entries.items()}

        # Check for empty fields
        required_fields = ["Name"]
        if not all(user_data.get(field) for field in required_fields):
            messagebox.showerror("Error", "All required fields must be filled.")
            return

        # Load the existing data
        try:
            existing_data = pd.read_csv(STUDENT_FILE)
        except FileNotFoundError:
            messagebox.showerror("Error", "Student data file not found.")
            return

        # Update the data
        existing_data.loc[existing_data["username"] == self.username, list(user_data.keys())] = list(user_data.values())

        # Save the updated data
        try:
            existing_data.to_csv(STUDENT_FILE, index=False)
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.parent.user_data.update(user_data)  # Update the in-memory user data
            self.parent.switch_frame(StudentDashboard)  # Go back to the dashboard
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profile: {e}")
            
            
# Initialize application
def start_student_gui(root):
    """Use existing root window instead of creating new one"""
    for widget in root.winfo_children():
        widget.destroy()  # Clear existing widgets
    app = MainWindow(root)
    app.switch_frame(LoginScreen, app)
    return app

