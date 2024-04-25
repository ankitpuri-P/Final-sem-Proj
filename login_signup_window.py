import tkinter as tk
from tkinter import ttk, messagebox
from test5 import ParkingApp

class LoginSignupWindow:
    def __init__(self, root, on_login_success=None):
        self.root = root
        self.root.title("Parking Slot Detector")
        self.root.geometry("1200x700")

        self.on_login_success = on_login_success

        # Create Labels and Entry fields for the login and signup page
        self.title_label = ttk.Label(root, text="Parking Slot Detector", font=('Helvetica', 30, 'bold'))
        self.title_label.place(x=400, y=50)

        self.user_label = ttk.Label(root, text="Username",font=('Helvetica', 15))
        self.user_label.place(x=200, y=180)
        self.user_entry = ttk.Entry(root)
        self.user_entry.place(x=400, y=180)

        self.password_label = ttk.Label(root, text="Password",font=('Helvetica', 15))
        self.password_label.place(x=200, y=230)
        self.password_entry = ttk.Entry(root)
        self.password_entry.place(x=400, y=230)
        self.password_entry.configure(show="*")  # to hide password

        self.login_button = ttk.Button(root, text="Login", command=self.login)
        self.login_button.place(x=400, y=280)

    def login(self):
        username = self.user_entry.get()
        password = self.password_entry.get()
        # Add your own logic to validate username and password
        messagebox.showinfo(title="Success", message="Logged in successfully")

        # Call the callback function upon successful login
        if self.on_login_success:
            self.on_login_success()

def main():
    def show_parking_app():
        # Load class_list (simplified for demonstration)
        my_file = open("coco.txt", "r")
        data = my_file.read()
        class_list = data.split("\n")

        # Create an instance of ParkingApp
        parking_root = tk.Tk()
        app = ParkingApp(parking_root, class_list)
        app.update_video()  # Start the video update loop
        parking_root.mainloop()

    # Create the root window
    root = tk.Tk()

    # Create an instance of LoginSignupWindow with the show_parking_app callback function
    login_window = LoginSignupWindow(root, on_login_success=show_parking_app)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
