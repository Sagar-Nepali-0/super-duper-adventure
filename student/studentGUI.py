# ---------------------------
# Module Imports
# ---------------------------
import tkinter as tk
from PIL import Image, ImageTk  # For image handling
from tkinter import messagebox  # For user feedback popups
from datetime import datetime  # For date display
import pandas as pd  # For CSV data handling
import os
import sys



# ---------------------------
# File Path Constants
# ---------------------------
PASSWORD_FILE = "data/password.csv"  # Stores user credentials
GRADE_DATA = "data/grade.csv"       # Academic records
STUDENT_FILE = "data/users/student.csv"  # Student profiles
ECA_FILE = "data/eca.csv"          # Extracurricular activities
image_path = "img/logo.png"         # Application logo

# ---------------------------
# Data Initialization
# ---------------------------
try:
    # Attempt to load all data files
    authentication = pd.read_csv(PASSWORD_FILE)
    read_gradeData = pd.read_csv(GRADE_DATA)
    student_file = pd.read_csv(STUDENT_FILE)
    eca_data = pd.read_csv(ECA_FILE)
    
    # Verify logo exists
    with open(image_path, "rb") as f:
        pass
except FileNotFoundError:
    # Create empty datasets if files missing
    authentication = pd.DataFrame(columns=["ID", "username", "password", "role"])
    read_gradeData = pd.DataFrame()
    student_file = pd.DataFrame()
    eca_data = pd.DataFrame()
    image_path = None

# ---------------------------
# Main Application Window
# ---------------------------
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

        # UI Color scheme
        self.SIDEBAR_BG = "#2C3E50"    # Dark blue
        self.MAIN_BG = "black"         # Primary background
        self.HEADER_COLOR = "#F39C12"  # Orange header
        self.BUTTON_BG = "#FFFFFF"     # White buttons
        self.BUTTON_FG = "#000000"     # Black text
        self.ENTRY_BG = "#FFFFFF"      # White input fields
        self.TEXT_COLOR = "#FFFFFF"    # White text

        self.current_frame = None     # Track active screen
        self.user_data = {}           # Store logged-in user's data

    def switch_frame(self, frame_class, *args):
        """Handle navigation between different screens"""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)


# ---------------------------
# Login Screen
# ---------------------------
class LoginScreen(tk.Frame):
    """Handles user authentication with username/password"""
    def __init__(self, parent, main_window):
        super().__init__(parent.root, bg="black")
        
        # Canvas for login UI elements
        canvas = tk.Canvas(self, width=800, height=500, bg="black", highlightthickness=0)
        canvas.pack(expand=True)
        
        # Login form elements
        canvas.create_rectangle(2, 80, 800, 400, fill="black", outline="black", width=1)
        x_center = (100 + 700) // 2
        canvas.create_line(x_center, 80, x_center, 400, fill="black", width=2)

        # Load and display image
        if image_path:
            image = Image.open(image_path)
            resized_image = image.resize((300, 300))
            image_tk = ImageTk.PhotoImage(resized_image)
            canvas.image_tk = image_tk
            canvas.create_image(220, 260, image=image_tk, anchor="center")

        # Login elements
        canvas.create_text(550, 150, text="Student Login", fill="white", font=("Arial", 29, "bold"))
        
        # Username input
        canvas.create_text(465, 200, text="Username:", fill="white", font=("Arial", 14))
        self.username_entry = tk.Entry(self, width=15, font=("Arial", 14))
        canvas.create_window(600, 200, window=self.username_entry)
        
        # Password input
        canvas.create_text(465, 250, text="Password:", fill="white", font=("Arial", 14))
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
        """Return to login.py script using system call"""
        self.master.destroy()
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        login_script = os.path.join(script_dir, "login.py") 
        os.system(f"python \"{login_script}\"") 
 
    def authenticate(self, main_window):
        """Validate credentials against stored data"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Query authentication database
        user = authentication[
            (authentication["username"] == username) & 
            (authentication["password"] == password) & 
            (authentication["role"] == "student")
        ]
        
        if not user.empty:
            # Fetch the student data
            student_data = student_file[student_file["username"] == username]
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
            messagebox.showerror("Error", "Incorrect Username or Password")

# ---------------------------
# Student Dashboard
# ---------------------------
class StudentDashboard(tk.Frame):
    """Main interface showing profile, grades, and activities"""
    def __init__(self, parent):
        super().__init__(parent.root, bg="#f5f5f5")
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.root = parent.root
        self.root.title("Student Dashboard")
        
        # Sidebar configuration
        sidebar_width = 200
        sidebar = tk.Frame(self, bg="#1e88e5", width=sidebar_width)
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
        header = tk.Frame(self, bg="#0d47a1", height=50)
        header.pack(side="top", fill="x")
        
        tk.Label(header, text="Student Dashboard", bg="#0d47a1", fg="white",
                font=("Arial", 20, "bold")).pack(pady=10, side="left")
        
        # Divide the sidebar into two sections: upper and lower
        upper_section = tk.Frame(sidebar, bg="#1e88e5")
        upper_section.pack(fill="x", pady=20)

        # Add a horizontal line to divide the sections
        divider = tk.Frame(sidebar, bg="#000000", height=2)
        divider.pack(fill="x")

        lower_section = tk.Frame(sidebar, bg="#1e88e5")  # Updated background color
        lower_section.pack(fill="x", pady=(10, 20), expand=True)
        
        # Sidebar content
        tk.Label(upper_section, text="ABC School", bg="#1e88e5", fg="black",
                font=("Arial", 22, "bold")).pack(pady=15, anchor="n")

        tk.Button(lower_section, 
                  text="Profile", 
                  command=lambda: self.show_content("profile"), 
                  width=15, 
                  font=("Arial", 10, "bold")).pack(pady=(5, 5), anchor="n")
        tk.Button(lower_section, text="Grades", 
                  command=lambda: self.show_content("grades"), 
                  width=15, 
                  font=("Arial", 10, "bold")).pack(pady=(5, 5), anchor="n")
        tk.Button(lower_section, text="ECA", 
                  command=lambda: self.show_content("eca"), 
                  width=15, 
                  font=("Arial", 10, "bold")).pack(pady=(5, 5), anchor="n")
        
        add_update_button = tk.Button(
            lower_section,
            text="Update Profile",
            command=lambda: parent.switch_frame(ProfileUpdate, self.parent.user_data["username"]),
            font=("Arial", 10, "bold"),
            width=15
        )
        add_update_button.pack(pady=(5, 5), anchor="n")

        tk.Button(header, text="Log Out", command=lambda: parent.switch_frame(LoginScreen, parent), 
        bg=parent.BUTTON_BG, fg=parent.BUTTON_FG, font=("Arial", 8)).pack(pady=10, padx=10 ,side="right")        
        # Main content area
        main_area = tk.Frame(self, bg=parent.MAIN_BG)
        main_area.pack(fill="both", expand=True)

        # Content display area
        self.content_area = tk.Frame(main_area, bg=parent.MAIN_BG)
        self.content_area.pack(fill="both", expand=True, pady=20)
        
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
            self.show_eca()

    def show_profile(self):
        """Display student's personal information"""
        profile_box = tk.Frame(self.content_area, bg="#e3f2fd", bd=2, relief="solid")
        profile_box.pack(pady=20, padx=20, fill="both", expand=False)

        tk.Label(profile_box, text="Student Profile", font=("Arial", 18, "bold"),
                bg="#e3f2fd", fg="#212121").pack(pady=10, side="top")

        fields = ["ID", "Name", "DOB", "Address", "Grade", "Section"]
        for i, field in enumerate(fields):
            row = tk.Frame(profile_box, bg="white")
            row.pack(anchor="w", pady=2, padx=10)
            tk.Label(row, text=f"{field}:", width=9, anchor="w",
                    bg="#e3f2fd", fg="#212121", font=("Arial", 14, "bold")).pack(side="left")
            tk.Label(row, text=self.parent.user_data.get(field, ""),
                    bg="#e3f2fd", fg="#212121", font=("Arial", 14)).pack(side="left")

            # Optional: Add a separator between rows
            separator = tk.Frame(profile_box, height=1, bg="black")
            separator.pack(fill="x", pady=2)

    def show_grades(self):
        """Display academic performance data"""
        grades_box = tk.Frame(self.content_area, bg="#e3f2fd", bd=2, relief="solid")
        grades_box.pack(pady=20, padx=20, fill="both", expand=False)

        tk.Label(grades_box, text="Student Grades", font=("Arial", 18, "bold"),
                bg="#e3f2fd", fg="#212121").pack(pady=10, side="top")

        grades = read_gradeData[read_gradeData["username"] == self.parent.user_data["username"]]
        if not grades.empty:
            subjects = ["english", "nepali", "math", "science", "computer"]
            for i, subject in enumerate(subjects):
                row = tk.Frame(grades_box, bg="#FDFFE2")
                row.pack(anchor="w", pady=2, padx=10)
                tk.Label(row, text=f"{subject.capitalize()}:", width=9, anchor="w",
                        bg="#e3f2fd", fg="#212121", font=("Arial", 14, "bold")).pack(side="left")
                tk.Label(row, text=grades.iloc[0].get(subject, "N/A"),  # Fallback to "N/A"
                        bg="#e3f2fd", fg="#212121", font=("Arial", 14)).pack(side="left")

                # Optional: Add a separator between rows
                separator = tk.Frame(grades_box, height=1, bg="black")
                separator.pack(fill="x", pady=2)
        else:
            tk.Label(grades_box, text="No grades available",
                    bg="#83B4FF", fg="black", font=("Arial", 14)).pack(pady=10)


    def show_eca(self):
        """Show extracurricular activity enrollment status"""
        eca_box = tk.Frame(self.content_area, bg="#e3f2fd", bd=2, relief="solid")
        eca_box.pack(pady=20, padx=20, fill="both", expand=False)

        # Header for the ECA section
        tk.Label(eca_box, text="Extracurricular Activities", font=("Arial", 18, "bold"),
                bg="#e3f2fd", fg="#212121").pack(pady=10, side="top")

        try:
            # Extract student ECA data
            student_eca = eca_data[eca_data["username"] == self.parent.user_data["username"]]

            if not student_eca.empty:
                student_eca = student_eca.iloc[0]  # Get the first matching record
                self.eca_vars = []  # List to keep references to IntVar

                for activity in student_eca.index[1:]:  # Skip the 'username' column
                    is_enrolled = student_eca[activity]
                    # Ensure the value is an integer (1/0)
                    var = tk.IntVar(value=int(is_enrolled))
                    self.eca_vars.append(var)  # Keep a reference to prevent garbage collection

                    # Create the checkbox with the variable
                    cb = tk.Checkbutton(
                        eca_box,
                        text=activity.capitalize(),
                        bg="#e3f2fd",
                        fg="#212121",
                        selectcolor="black",  # Color of the tick when selected
                        state="disabled",
                        font=("Arial", 14, "bold"),
                        variable=var
                    )
                    cb.pack(anchor="w", pady=2, padx=9)
            else:
                tk.Label(eca_box, text="No extracurricular activities found",
                        bg="#e3f2fd", fg="#212121", font=("Arial", 16)).pack(pady=10)
        except FileNotFoundError:
            tk.Label(eca_box, text="ECA data file not found",
                    bg="#e3f2fd", fg="#212121", font=("Arial", 12)).pack(pady=10)


class ProfileUpdate(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent.root, bg=parent.MAIN_BG)
        self.parent = parent
        self.username = username  # Store the username
        self.pack(fill="both", expand=True)
        self.root = parent.root
        self.root.title("Profile Update")

        # Sidebar setup
        sidebar_width = 200
        sidebar = tk.Frame(self, bg="#1DCD9F", width=sidebar_width)
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

        # Header
        header = tk.Frame(self, bg="#169976", height=50)
        header.pack(side="top", fill="x")
        tk.Label(header, text="Update Personal Information", bg="#169976", fg="white", font=("Arial", 20, "bold")).pack(pady=10, side="left")

        # Divide the sidebar into two sections: upper and lower
        upper_section = tk.Frame(sidebar, bg="#1DCD9F")
        upper_section.pack(fill="x", pady=(20, 10))

        divider = tk.Frame(sidebar, bg="black", height=2)
        divider.pack(fill="x", pady=5)

        lower_section = tk.Frame(sidebar, bg="#1DCD9F")
        lower_section.pack(fill="x", pady=(10, 20), expand=True)

        tk.Label(upper_section, text="ABC School", bg="#1DCD9F", fg="black", font=("Arial", 22, "bold")).pack(pady=15, anchor="n")

        back_button = tk.Button(
            lower_section,
            text="Back",
            command=lambda: parent.switch_frame(StudentDashboard),
            bg=parent.BUTTON_BG,
            fg=parent.BUTTON_FG,
            font=("Arial", 10, "bold"),
            width=15
        )
        back_button.pack(pady=(5, 5), anchor="n")

        # Create a frame to act as the box for the main content
        profile_update_box = tk.Frame(self, bg="#5A72A0", bd=2, relief="solid")
        profile_update_box.pack(pady=20, padx=20, fill="both", expand=False)

        # Display a header inside the box
        tk.Label(profile_update_box, text=f"Update Profile of {self.username}", font=("Arial", 16, "bold"),
                 bg="#5A72A0", fg="white").pack(pady=20)

        # Fields to update
        fields = ["ID", "Name", "DOB", "Address", "Grade", "Section", "username", "password"]
        self.entries = {}

        for field in fields:
            row = tk.Frame(profile_update_box, bg="#1A2130")
            row.pack(anchor="w", pady=2, padx=10)
            tk.Label(row, text=f"{field}:", width=9, anchor="w", bg="#5A72A0", fg="black", font=("Arial", 14, "bold")).pack(side="left")

            entry = tk.Entry(row, font=("Arial", 14))
            entry.pack(side="left", fill="x", expand=True)
            self.entries[field] = entry

            # Pre-fill the entry with existing data
            entry.insert(0, self.parent.user_data.get(field, ""))


        # Save button inside the box
        tk.Button(profile_update_box, text="Save", command=self.save_profile, font=("Arial", 12),
                  bg=parent.BUTTON_BG, fg=parent.BUTTON_FG).pack(pady=5, side="right", padx=5)

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

