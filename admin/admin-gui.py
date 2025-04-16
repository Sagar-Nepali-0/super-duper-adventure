import tkinter as tk
from PIL import Image, ImageTk # To handle image files easily
from tkinter import messagebox
from datetime import datetime
import pandas as pd
root = tk.Tk()
root.title("Institution Admin Panel")
# Center the window on the screen
window_width = 800
window_height = 500

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

# Set the geometry of the window
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
PASSWORD_FILE = "data/password.csv"
authentication = pd.read_csv(PASSWORD_FILE)
current_frame = None

SIDEBAR_BG = "#828080"
MAIN_BG = "#D9D9D9"
HEADER_COLOR = "#F5C45E"
BUTTON_BG = "#D9D9D9"
BUTTON_FG = "#000000"
ENTRY_BG = "#FFFFFF"
ENTRY_FG = "#000000"
ERROR_COLOR = "#BE3D2A"
SUCCESS_COLOR = "#3CB371"
TEXT_COLOR = "#000000"  
SIDEBAR_WIDTH = 350


def switch_frame(frame_func):
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = frame_func()
    current_frame.pack(fill="both", expand=True)


def login_screen():
    canvas = tk.Canvas(root, width=800, height=500, bg="white")
    # Draw a rectangle on the canvas
    rectangle = canvas.create_rectangle(100, 80, 700, 400, fill="#828080", outline="black", width=1)
    # Calculate the x-coordinate of the center
    x_center = (100 + 700) // 2  # Average of the left and right x-coordinates
    # Draw a vertical line at the center
    canvas.create_line(x_center, 80, x_center, 400, fill="black", width=2)

    # Admin label
    canvas.create_text(550, 150, text="Admin", fill="black", font=("Arial", 29, "bold"))

    # Username label and entry
    canvas.create_text(465, 200, text="Username:", fill="black", font=("Arial", 14))
    username_entry = tk.Entry(root, width=15, font=("Arial", 14))
    canvas.create_window(600, 200, window=username_entry)  # Position the entry box next to the label

    # Password label and entry
    canvas.create_text(465, 250, text="Password:", fill="black", font=("Arial", 14))
    password_entry = tk.Entry(root, width=15, show="*", font=("Arial", 14))
    canvas.create_window(600, 250, window=password_entry)

    # Load and display the image
    image_path = "img/logo.png"  # Replace with your image file path
    image = Image.open(image_path)  # Open the image file
    resized_image = image.resize((295, 295))  # Resize the image if needed
    image_tk = ImageTk.PhotoImage(resized_image)  # Convert the image for tkinter
    canvas.image_tk = image_tk 
    canvas.create_image(250, 240, image=image_tk, anchor="center")


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
                switch_frame(lambda: admin_dashboard(logged_in_username))
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
            

    button = tk.Button(root, text="Log In", width=26, command=login, font=("Arial", 12, "bold"))
    canvas.create_window(552, 300, window=button)  # Center the button below the input fields
    return canvas


def admin_dashboard(logged_in_username):

    frame = tk.Frame(root, bg=MAIN_BG)

    sidebar = tk.Frame(frame, width=SIDEBAR_WIDTH, bg=SIDEBAR_BG)
    sidebar.pack(side="left", fill="y")

    logo = tk.Label(sidebar, text="[LOGO]", bg=SIDEBAR_BG, fg="white", height=5)
    logo.pack(pady=10)

    tk.Button(sidebar, text="Add User", command=lambda: switch_frame(lambda: add_user_screen(logged_in_username)), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=10)
    tk.Button(sidebar, text="Delete User", command=lambda: switch_frame(lambda: delete_user_screen(logged_in_username)), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=10)

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
    tk.Label(main_area, text=logged_in_username, font=("Arial", 14), bg=MAIN_BG, fg="white").pack(pady=10)
    tk.Button(main_area, text="Log Out", command=lambda: switch_frame(login_screen), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=5)

    return frame


def add_user_screen(logged_in_username):
    frame = tk.Frame(root, bg=MAIN_BG)

    # Sidebar
    sidebar = tk.Frame(frame, width=SIDEBAR_WIDTH, bg=SIDEBAR_BG)
    sidebar.pack(side="left", fill="y")

    logo = tk.Label(sidebar, text="[LOGO]", bg=SIDEBAR_BG, fg="white", height=5)
    logo.pack(pady=10)

    tk.Label(sidebar, text="Role", bg=SIDEBAR_BG, fg="white", font=("Arial", 12)).pack(pady=(10, 0))
    tk.Button(sidebar, text="Admin", command=lambda: load_fields("admin"), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=5)
    tk.Button(sidebar, text="Student", command=lambda: load_fields("student"), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=5)
    tk.Button(sidebar, text="← Back", command=lambda: switch_frame(lambda: admin_dashboard(logged_in_username)), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=20)

    # Main Area
    global main_area
    main_area = tk.Frame(frame, bg=MAIN_BG)
    main_area.pack(fill="both", expand=True, padx=20, pady=20)

    # Default content
    tk.Label(main_area, text="Select a role to add a user", font=("Arial", 18, "bold"), bg=MAIN_BG, fg=HEADER_COLOR).pack(pady=10)

    return frame

def load_fields(role):
    # Clear the current content in main_area
    for widget in main_area.winfo_children():
        widget.destroy()

    # Define fields for admin and student
    admin_fields = ["ID", "Name", "Username", "Password"]
    student_fields = ["ID", "Name", "DOB", "Address", "Grade", "Section", "Username", "Password"]

    # Select fields based on role
    fields = admin_fields if role == "admin" else student_fields

    # Add a title
    tk.Label(main_area, text=f"Add {role.capitalize()} User", font=("Arial", 18, "bold"), bg=MAIN_BG, fg=HEADER_COLOR).grid(row=0, column=0, columnspan=4, pady=10)

    # Create entry fields dynamically
    entries = {}
    for i, field in enumerate(fields):
        tk.Label(main_area, text=field, bg=MAIN_BG, fg="white").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5)
        entry = tk.Entry(main_area, bg=ENTRY_BG, fg=ENTRY_FG)
        entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
        entries[field] = entry

    # Save button
    def save_user():
        # Collect user data from the entries
        user_data = {field: entry.get() for field, entry in entries.items()}

        # Check for empty fields
        if not all(user_data.get(field) for field in ["ID", "Username", "Password"]):
            messagebox.showerror("Error", "All required fields (ID, Username, Password) must be filled.")
            return

        # Load the existing data from the CSV file
        try:
            existing_data = pd.read_csv(PASSWORD_FILE)
        except FileNotFoundError:
            # If the file doesn't exist, create an empty DataFrame
            existing_data = pd.DataFrame(columns=["ID", "username", "password", "role"])

        # Check for duplicate ID, username, or password
        if (
            user_data["ID"] in existing_data["ID"].astype(str).values or
            user_data["Username"] in existing_data["username"].values or
            user_data["Password"] in existing_data["password"].values
        ):
            messagebox.showerror("Error", "Duplicate ID, Username, or Password found. Please use unique values.")
            return

        # Filter only the required fields
        filtered_data = {
            "ID": user_data.get("ID"),
            "username": user_data.get("Username"),
            "password": user_data.get("Password"),
            "role": role  # Add the role (admin or student)
        }

        # Convert the filtered data to a DataFrame
        new_user_df = pd.DataFrame([filtered_data])

        # Append the new user data to the CSV file
        try:
            new_user_df.to_csv(PASSWORD_FILE, mode='a', index=False, header=False)
            messagebox.showinfo("Saved", f"{role.capitalize()} user added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user: {e}")

    tk.Button(main_area, text="Save", command=save_user, bg=SUCCESS_COLOR, fg=BUTTON_FG).grid(
        row=len(fields) + 1, column=0, columnspan=2, pady=20
    )


def delete_user_screen(logged_in_username):
    frame = tk.Frame(root, bg=MAIN_BG)

    sidebar = tk.Frame(frame, width=SIDEBAR_WIDTH, bg=SIDEBAR_BG)
    sidebar.pack(side="left", fill="y")

    logo = tk.Label(sidebar, text="[LOGO]", bg=SIDEBAR_BG, fg="white", height=5)
    logo.pack(pady=10)

    # Back Button
    tk.Button(sidebar, text="← Back", command=lambda: switch_frame(lambda: admin_dashboard(logged_in_username)), bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=20)

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

        if not user_id:
            messagebox.showwarning("Error", "Please enter an ID.")
            return

        try:
            # Load the CSV file
            df = pd.read_csv(PASSWORD_FILE)

            # Check if the ID exists
            if user_id not in df["ID"].astype(str).values:
                messagebox.showerror("Error", f"User ID {user_id} not found.")
                return

            # Remove the user with the given ID
            df = df[df["ID"].astype(str) != user_id]

            # Save the updated DataFrame back to the CSV file
            df.to_csv(PASSWORD_FILE, index=False)

            messagebox.showinfo("Deleted", f"User ID {user_id} deleted successfully.")
            switch_frame(lambda: delete_user_screen(logged_in_username))  # Refresh the delete user screen
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    tk.Button(main_area, text="Delete", command=delete_user, bg=ERROR_COLOR, fg=BUTTON_FG).pack()

    return frame


switch_frame(login_screen)
root.mainloop()