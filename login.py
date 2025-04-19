import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from admin.adminGui import start_admin_gui
from student.studentGUI import start_student_gui

try:
    image_path = "img/logo.png"
except FileNotFoundError:
    image_path = "img/logo.png"  # Default image path

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Log In")
        self.icon = tk.PhotoImage(file=image_path)
        self.root.iconphoto(True, self.icon)

        # Window geometry setup
        window_width = 650
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Style configurations
        self.current_frame = None
        self.SIDEBAR_BG = "black"
        self.MAIN_BG = "black"
        self.HEADER_COLOR = "white"

    def switch_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

class LoginScreen(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent.root, bg=main_window.MAIN_BG)
        
        canvas = tk.Canvas(self, width=800, height=500, bg="black", highlightthickness=0)
        canvas.pack(expand=True)
        
        # GUI elements
        canvas.create_rectangle(2, 80, 800, 400, fill=main_window.SIDEBAR_BG, outline="")
        x_center = (2 + 800) // 2
        canvas.create_line(x_center, 80, x_center, 400, fill="black")

        canvas.create_text(418, 150, text="Log In", fill="white", font=("Arial", 30))

        # Buttons
        admin_button = tk.Button(self, text="Admin", width=26, 
                               command=lambda: start_admin_gui(parent.root),
                               font=("Arial", 12, "bold"))
        canvas.create_window(500, 215, window=admin_button)

        student_button = tk.Button(self, text="Student", width=26,
                                 command=lambda: start_student_gui(parent.root),
                                 font=("Arial", 12, "bold"))
        canvas.create_window(500, 260, window=student_button)

        # Image handling
        try:
            image = Image.open(image_path)
            resized_image = image.resize((300, 300))
            image_tk = ImageTk.PhotoImage(resized_image)
            canvas.image_tk = image_tk
            canvas.create_image(190, 210, image=image_tk, anchor="center")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file not found: {image_path}")

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.switch_frame(LoginScreen, app)
    root.mainloop()