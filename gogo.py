import tkinter as tk
from login_signup_window import LoginSignupWindow
from test5 import ParkingApp

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
