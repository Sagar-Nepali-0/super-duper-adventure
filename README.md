# Super Duper Adventure

Super Duper Adventure is a Python-based GUI application for managing student and admin accounts. It provides separate interfaces for students and administrators, allowing them to log in and perform various tasks such as viewing profiles, updating information, and managing user records.

## Features

### Admin Features
- **Add User**: Add new admin or student accounts.
- **Delete User**: Remove existing user accounts.
- **View Student Records**: View and analyze student grades using visualizations.

### Student Features
- **Login**: Students can log in to access their dashboard.
- **View Profile**: Students can view their personal information.
- **Update Profile**: Students can update their personal details.
- **View Grades**: Students can view their grades for various subjects.
- **View Extracurricular Activities (ECA)**: Students can see their enrolled extracurricular activities.

## Project Structure

### Key Files
- **`login.py`**: Entry point of the application. Provides the main login interface for both students and admins.
- **`admin/admin-gui.py`**: Admin interface for managing users and viewing student records.
- **`student/studentGUI.py`**: Student interface for accessing personal information, grades, and extracurricular activities.
- **`data/`**: Contains CSV files for storing user credentials, grades, and extracurricular activities.
- **`img/logo.png`**: Logo used in the application.

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `tkinter`
  - `Pillow`
  - `pandas`
  - `matplotlib`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/super-duper-adventure.git
   cd super-duper-adventure
