import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView

class SignupLoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Signup/Login Page")

        # Create map widget
        self.map_widget = TkinterMapView(root, width=800, height=600)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_widgets()

    def create_widgets(self):
        # Signup Frame
        signup_frame = ttk.LabelFrame(self.root, text="Signup", padding=(20, 20))
        signup_frame.grid(row=0, column=0, padx=20, pady=20)

        ttk.Label(signup_frame, text="Username:").grid(row=0, column=0, sticky="w")
        ttk.Entry(signup_frame).grid(row=0, column=1)

        ttk.Label(signup_frame, text="Password:").grid(row=1, column=0, sticky="w")
        ttk.Entry(signup_frame, show="*").grid(row=1, column=1)

        signup_button = ttk.Button(
            signup_frame, text="Signup", command=self.signup
        )
        signup_button.grid(row=2, columnspan=2)

        # Login Frame
        login_frame = ttk.LabelFrame(self.root, text="Login", padding=(20, 20))
        login_frame.grid(row=0, column=1, padx=20, pady=20)

        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="w")
        ttk.Entry(login_frame).grid(row=0, column=1)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="w")
        ttk.Entry(login_frame, show="*").grid(row=1, column=1)

        login_button = ttk.Button(
            login_frame, text="Login", command=self.login
        )
        login_button.grid(row=2, columnspan=2)

    def signup(self):
        # Implement signup logic here
        print("Signup button clicked.")

    def login(self):
        # Implement login logic here
        print("Login button clicked.")

def main():
    root = tk.Tk()
    app = SignupLoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
