import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv
from cryptography.fernet import Fernet

from home import FaceRecognitionSystem

# Initialize the cryptography key
key = b'TkaKvFAWzRtmjOnIis5XK31UOK61C02Z2cSMvN_efjM='
cipher_suite = Fernet(key)

class ForgetPage:
    def __init__(self, master):
        self.master = master
        master.title("User Forget Page")
        master.geometry("800x600")
        master.resizable(False, False)

        # Load and resize the background images
        bg_image_1 = Image.open("images\\sample.png").resize((300, 600))
        self.bg_photo_1 = ImageTk.PhotoImage(bg_image_1)

        bg_image_2 = Image.open("images\\bgforget.png").resize((500, 600))
        self.bg_photo_2 = ImageTk.PhotoImage(bg_image_2)

        # Create a Canvas to place the background images
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()

        # Place the first background image on the left side of the Canvas
        self.canvas.create_image(0, 0, image=self.bg_photo_1, anchor="nw")

        # Place the second background image on the right side of the Canvas
        self.canvas.create_image(300, 0, image=self.bg_photo_2, anchor="nw")

        # Add other login components
        self.title_label = tk.Label(master, text="FORGOT PASSWORD", font=("Comic Sans MS", 24))
        self.title_label.place(x=550, y=100, anchor="center")

        self.new_password_label = tk.Label(master, text="New Password:", font=("Comic Sans MS", 14))
        self.new_password_label.place(x=350, y=300)
        self.new_password_entry = tk.Entry(master, font=("Comic Sans MS", 15), show="*")
        self.new_password_entry.place(x=500, y=300)

        self.confirm_password_label = tk.Label(master, text="Confirm Password:", font=("Comic Sans MS", 14))
        self.confirm_password_label.place(x=320, y=370)
        self.confirm_password_entry = tk.Entry(master, font=("Comic Sans MS", 15), show="*")
        self.confirm_password_entry.place(x=500, y=370)

        self.email_label = tk.Label(master, text="Email:", font=("Comic Sans MS", 14))
        self.email_label.place(x=400, y=230)
        self.email_entry = tk.Entry(master, font=("Comic Sans MS", 15))
        self.email_entry.place(x=500, y=230)

        self.show_new_password_img = Image.open("images\\eye.png").resize((30, 30))
        self.show_new_password_photo = ImageTk.PhotoImage(self.show_new_password_img)
        self.show_new_password_button = tk.Button(master, image=self.show_new_password_photo, command=self.toggle_new_password_visibility, bd=0)
        self.show_new_password_button.place(x=750, y=300)

        self.show_confirm_password_img = Image.open("images\\eye.png").resize((30, 30))
        self.show_confirm_password_photo = ImageTk.PhotoImage(self.show_confirm_password_img)
        self.show_confirm_password_button = tk.Button(master, image=self.show_confirm_password_photo, command=self.toggle_confirm_password_visibility, bd=0)
        self.show_confirm_password_button.place(x=750, y=370)

        self.sign_up_button = tk.Button(master, text="Submit", font=("Comic Sans MS", 17), command=self.change_password, bg="lightblue", fg="black", cursor="hand2")
        self.sign_up_button.place(x=550, y=500, anchor="center")

    def toggle_new_password_visibility(self):
        if self.new_password_entry.cget('show') == '':
            self.new_password_entry.config(show='*')
        else:
            self.new_password_entry.config(show='')

    def toggle_confirm_password_visibility(self):
        if self.confirm_password_entry.cget('show') == '':
            self.confirm_password_entry.config(show='*')
        else:
            self.confirm_password_entry.config(show='')

    def change_password(self):
        if not self.email_entry.get() or not self.new_password_entry.get() or not self.confirm_password_entry.get():
            messagebox.showerror("Error", "Please fill in all fields")
            return

        email = self.email_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password == confirm_password:
            encrypted_password = cipher_suite.encrypt(new_password.encode()).decode()
            encrypted_email_entered = cipher_suite.encrypt(email.encode()).decode()

            rows = []
            found = False

            # Read the CSV file, update the password if email matches
            with open("users.csv", 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        decrypted_email_in_file = cipher_suite.decrypt(row[2].encode()).decode()
                        if decrypted_email_in_file == email:
                            row[1] = encrypted_password  # Update the password
                            found = True
                    rows.append(row)

            # Write back to the CSV file
            with open("users.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            if found:
                messagebox.showinfo("Success", "Your Password has been changed successfully!")
            else:
                messagebox.showerror("Error", "Email not found.")
        else:
            messagebox.showerror("Error", "Passwords do not match")





class LoginPage:
    def __init__(self, root):
        self.master = root
        root.title("User Login")
        root.geometry("800x600")
        root.resizable(False, False)

        # Load and resize the first background image
        bg_image_1 = Image.open("images\\sample2.png").resize((300, 600))
        self.bg_photo_1 = ImageTk.PhotoImage(bg_image_1)

        # Load and resize the second background image
        bg_image_2 = Image.open("images\\bgsignup.png").resize((500, 600))
        self.bg_photo_2 = ImageTk.PhotoImage(bg_image_2)

        # Create a Canvas to place the background images
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # Place the first background image on the left side of the Canvas
        self.canvas.create_image(0, 0, image=self.bg_photo_1, anchor="nw")

        # Place the second background image on the right side of the Canvas
        self.canvas.create_image(300, 0, image=self.bg_photo_2, anchor="nw")

        # Add other login components (labels, entry fields, buttons) here
        # Title Label
        self.title_label = tk.Label(root, text="USER LOGIN", font=("Comic Sans MS", 24))
        self.title_label.place(x=550, y=100, anchor="center")

        # Username Label and Entry
        self.username_label = tk.Label(root, text="Username:", font=("Comic Sans MS", 14))
        self.username_label.place(x=350, y=200)
        self.username_entry = tk.Entry(root, font=("Comic Sans MS", 15))
        self.username_entry.place(x=500, y=200)

        # Password Label and Entry
        self.password_label = tk.Label(root, text="Password:", font=("Comic Sans MS", 14))
        self.password_label.place(x=350, y=300)
        self.password_entry = tk.Entry(root, font=("Comic Sans MS", 15), show="*")
        self.password_entry.place(x=500, y=300)

        # Forgot Password Link
        self.forgot_password_label = tk.Label(root, text="Forgot Password?", font=("Comic Sans MS", 15), fg="blue", cursor="hand2")
        self.forgot_password_label.place(x=450, y=400)
        self.forgot_password_label.bind("<Button-1>", self.open_forgot_password_url)

        # Toggle Button for Password Visibility
        self.show_password_img = Image.open("images\\eye.png").resize((30, 30))
        self.show_password_photo = ImageTk.PhotoImage(self.show_password_img)
        self.show_password_button = tk.Button(root, image=self.show_password_photo, command=self.toggle_password_visibility, bd=0)
        self.show_password_button.place(x=750, y=300)

        # Login Button
        self.login_button = tk.Button(root, text="Login", font=("Comic Sans MS", 17), command=self.login, bg="yellow", fg="black", cursor="hand2")
        self.login_button.place(x=550, y=500, anchor="center")

    def toggle_password_visibility(self):
        # Toggle password visibility
        if self.password_entry.cget('show') == '':
            self.password_entry.config(show='*')
        else:
            self.password_entry.config(show='')

    def login(self):
        # Get username and password from the entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username or password is empty
        if not username or not password:
            messagebox.showerror("Login", "Please enter both username and password.")
            return

        user_found = False
        with open("users.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:  # Assuming at least two columns (username and password)
                    messagebox.showerror("Error", "Invalid user data")
                    return
                username_in_file, encrypted_password_in_file = row[:2]  # Extract username and encrypted password
                try:
                    decrypted_password_in_file = cipher_suite.decrypt(encrypted_password_in_file.encode()).decode()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to decrypt user data: {e}")
                    return
                if username_in_file == username and decrypted_password_in_file == password:
                    user_found = True
                    break

        if user_found:
            messagebox.showinfo("Login", "Login Successful!")
            self.new_window = tk.Toplevel(self.master)
            self.app = FaceRecognitionSystem(self.new_window)
        else:
            messagebox.showerror("Login", "Invalid username or password")






    def open_forgot_password_url(self, event):
        forget_page_window = tk.Toplevel(self.master)
        forget_page = ForgetPage(forget_page_window)
        forget_page_window.mainloop()

# Create the Tkinter window
root = tk.Tk()
app = LoginPage(root)
root.mainloop()
