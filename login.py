import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from admin.adminGui import start_admin_gui
from student.studentGUI import start_student_gui

try:
    image_path = "C:\PYTHON\Student\super-duper-adventure\img\logo.png"
except FileNotFoundError:
    image_path = "img/logo.png"  # Default image path

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Log In")
        self.icon = tk.PhotoImage(file=image_path)
        self.root.iconphoto(True, self.icon)

        # Window geometry setup
        window_width = 800
        window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Style configurations
        self.current_frame = None
        self.SIDEBAR_BG = "#828080"
        self.MAIN_BG = "#D9D9D9"
        self.HEADER_COLOR = "#828080"
        self.BUTTON_BG = "#D9D9D9"
        self.BUTTON_FG = "#000000"
        self.ENTRY_BG = "#FFFFFF"
        self.ENTRY_FG = "#000000"

    def switch_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

class LoginScreen(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent.root, bg=main_window.MAIN_BG)
        
        canvas = tk.Canvas(self, width=800, height=500, bg="white")
        canvas.pack(expand=True)
        
        # GUI elements
        canvas.create_rectangle(100, 80, 700, 400, fill=main_window.SIDEBAR_BG, outline="black", width=1)
        x_center = (100 + 700) // 2
        canvas.create_line(x_center, 80, x_center, 400, fill="black", width=2)

        canvas.create_text(400, 50, text="Welcome to the System", font=("Arial", 20, "bold"), fill=main_window.HEADER_COLOR)
        canvas.create_text(550, 150, text="Log In", fill="black", font=("Arial", 29, "bold"))

        # Buttons
        admin_button = tk.Button(self, text="Admin", width=26, 
                               command=lambda: start_admin_gui(parent.root),
                               font=("Arial", 12, "bold"))
        canvas.create_window(552, 250, window=admin_button)

        student_button = tk.Button(self, text="Student", width=26,
                                 command=lambda: start_student_gui(parent.root),
                                 font=("Arial", 12, "bold"))
        canvas.create_window(552, 300, window=student_button)

        # Image handling
        try:
            image = Image.open(image_path)
            resized_image = image.resize((295, 295))
            image_tk = ImageTk.PhotoImage(resized_image)
            canvas.image_tk = image_tk
            canvas.create_image(250, 240, image=image_tk, anchor="center")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file not found: {image_path}")

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.switch_frame(LoginScreen, app)
    root.mainloop()