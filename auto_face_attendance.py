import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from reportlab.lib import pagesizes
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import subprocess
import random
from datetime import datetime
import pyttsx3
from tkvideo import tkvideo


class SideNavApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic face attendance")

        # Set a blank icon for the window (optional)
        self.root.iconbitmap('icon.ico')
        self.root.resizable(False, False)


        # Set the background color of the root window
        self.root.configure(bg="lightgray")

        # Set the initial size of the window before it appears
        window_width = 1110
        window_height = 630

        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window on the screen
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the geometry of the window
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Variables to control sidebar expansion
        self.sidebar_expanded = False

        # Create a canvas for the side navigation
        self.side_nav_canvas = tk.Canvas(root, width=110, bg='#80c1ff', highlightthickness=0)  # Set initial width to 110
        self.side_nav_canvas.pack(side=tk.LEFT, fill=tk.Y)

        # Create a frame inside the canvas to hold widgets
        self.side_nav_frame = ttk.Frame(self.side_nav_canvas, width=107)  # Set initial width to 107
        self.side_nav_canvas.create_window((0, 0), window=self.side_nav_frame, anchor=tk.NW)

        # Create a style for the side navigation buttons
        style = ttk.Style()
        style.configure("SideNav.TButton", font=('Helvetica', 12), foreground="black", background="#80c1ff")
        style.map("SideNav.TButton", background=[("active", "#80c1ff")])

        # Load and resize the menu icon
        self.menu_icon = self.load_image("nav/menu.png", (40, 40))

        # Create button for menu at the top of the sidebar
        self.menu_button = ttk.Button(self.side_nav_frame, image=self.menu_icon, style="SideNav.TButton", command=self.toggle_sidebar, cursor="hand2", compound=tk.CENTER)
        self.menu_button.pack(pady=10, padx=0, fill=tk.X)

        # Create label for menu text (initially hidden)
        self.menu_label = tk.Label(self.side_nav_frame, text="Menu", font=('Comic Sans MS', 14), bg='#80c1ff')
        self.menu_label.pack_forget()  # Initially hide the menu label

        # Function to create other buttons
        def create_button(image_path, text, command):
            icon = self.load_image(image_path, (40, 40))
            button = ttk.Button(self.side_nav_frame, image=icon, style="SideNav.TButton", command=command, cursor="hand2", compound=tk.CENTER)
            button.image = icon  # Keep a reference to avoid garbage collection
            button.pack(pady=10, padx=0, fill=tk.X)
            label = tk.Label(self.side_nav_frame, text=text, font=('Comic Sans MS', 14), bg='#80c1ff')
            label.pack_forget()  # Initially hide the label
            return button, label

        # Create other buttons with correct names and commands
        self.buttons = []
        button_labels = [
            ("nav/home.png", "Home", self.display_home),
            ("nav/item1.png", "Add Person", self.display_add_person),
            ("nav/item7.png", "Profile", self.display_profile),
            ("nav/face.png", "Login-Logout", self.display_login_logout),
            ("nav/notes.png", "Notes", self.display_notes),
            ("nav/item8.png", "Attendance", self.display_attendance),
            ("nav/item2.png", "Developer", self.display_developer)
        ]

        for image_path, text, command in button_labels:
            button, label = create_button(image_path, text, command)
            self.buttons.append((button, label))

        # Load and resize the sign out icon
        self.signout_icon = self.load_image("nav/signout.png", (40, 40))

        # Create button for sign out at the bottom of the sidebar
        self.signout_button = ttk.Button(self.side_nav_frame, image=self.signout_icon, style="SideNav.TButton", command=self.confirm_sign_out, cursor="hand2", compound=tk.CENTER)
        self.signout_button.pack(pady=10, padx=0, fill=tk.X, side=tk.BOTTOM)

        # Create label for sign out text (initially hidden)
        self.signout_label = tk.Label(self.side_nav_frame, text="Sign Out", font=('Helvetica', 14), bg='#80c1ff')
        self.signout_label.pack_forget()  # Initially hide the sign out label

        # Create a sub-menu
        self.sub_menu_frame = ttk.Frame(root, width=600, height=400, padding=(10, 10, 10, 10))
        self.sub_menu_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize content with the home page
        self.display_home()

    def load_image(self, path, size):
        image = Image.open(path)
        image = image.resize(size)
        return ImageTk.PhotoImage(image)



    def display_home(self):
        self.clear_sub_menu()

        # Load and display the video
        video_path = "video.mp4"  # Set your video path here
        video_label = tk.Label(self.sub_menu_frame)
        video_label.grid(row=0, column=0, padx=40, pady=20, sticky='n')
        player = tkvideo(video_path, video_label, loop=1, size=(800, 400))
        player.play()

        # Create a frame to hold the read-only input fields at the bottom of the video
        info_frame = ttk.Frame(self.sub_menu_frame)
        info_frame.grid(row=1, column=0, pady=(10, 20), padx=10, sticky='n')

        # Display total users label and input
        total_users = self.get_total_users()  # Function to get the total number of images
        ttk.Label(info_frame, text="Total Users:", font=('Helvetica', 14)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.total_users_var = tk.StringVar(value=total_users)
        total_users_entry = ttk.Entry(info_frame, textvariable=self.total_users_var, font=('Helvetica', 14), state='readonly', width=15)
        total_users_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Display total login users today label and input
        total_logins_today = self.get_total_logins_today()  # Function to get total logins today
        ttk.Label(info_frame, text="Total Logins Today:", font=('Helvetica', 14)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.total_logins_today_var = tk.StringVar(value=total_logins_today)
        total_logins_today_entry = ttk.Entry(info_frame, textvariable=self.total_logins_today_var, font=('Helvetica', 14), state='readonly', width=15)
        total_logins_today_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Display total logout users today label and input
        total_logouts_today = self.get_total_logouts_today()  # Function to get total logouts today
        ttk.Label(info_frame, text="Total Logouts Today:", font=('Helvetica', 14)).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.total_logouts_today_var = tk.StringVar(value=total_logouts_today)
        total_logouts_today_entry = ttk.Entry(info_frame, textvariable=self.total_logouts_today_var, font=('Helvetica', 14), state='readonly', width=15)
        total_logouts_today_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

    def get_total_users(self):

        image_dir = 'db'
        return len([f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))])

    def get_total_logins_today(self):
        # Get today's date in the format used in the log file
        today = datetime.now().strftime("%d-%m-%Y")
        
        logins_today = 0
        
        # Read log file
        with open('log.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    action, timestamp = parts[2], parts[1]
                    if action == 'in' and timestamp.startswith(today):
                        logins_today += 1
        
        return logins_today

    def get_total_logouts_today(self):
        # Get today's date in the format used in the log file
        today = datetime.now().strftime("%d-%m-%Y")
        
        logouts_today = 0
        
        # Read log file
        with open('log.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    action, timestamp = parts[2], parts[1]
                    if action == 'out' and timestamp.startswith(today):
                        logouts_today += 1
        
        return logouts_today


    def display_add_person(self):
        self.clear_sub_menu()
        add_user_script_path = os.path.join(os.path.dirname(__file__), 'adduser.py')
        subprocess.run(["python", add_user_script_path])
        self.print_label = ttk.Label(self.sub_menu_frame, text="Click add Person button again to open a new add User webcam", font=('Helvetica', 23))
        self.print_label.pack(pady=200)

    def display_developer(self):
        self.clear_sub_menu()

        # Create and display developer details frame
        self.developer_frame = ttk.Frame(self.sub_menu_frame, padding=10)
        self.developer_frame.pack(fill=tk.BOTH, expand=True)

        # Background Image
        self.background_image = self.load_image("nav/bgdeveloper2.png", (1200, 800))
        self.background_label = tk.Label(self.developer_frame, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Developer details
        self.developer_name = "Twahir Sudy"
        self.location = "Dar es Salaam, Tanzania"
        self.email = "twahirsudy3@gmail.com"
        self.phone_number = "+255 67 429 1587"
        self.YouTube = "Sudi Technology"

        # Load and display the developer's picture
        self.developer_image = self.load_image("nav/twahir.jpg", (300, 400))
        self.image_label = tk.Label(self.developer_frame, image=self.developer_image, bg="white")
        self.image_label.place(relx=0.25, rely=0.5, anchor="center")

        # Display developer details with Comic Sans MS font
        font_style = ("Comic Sans MS", 15)
        text_color = "blue"
        background_color = "white"

        # Create and place labels in a frame
        self.name_label = tk.Label(self.developer_frame, text="Name: " + self.developer_name, font=font_style, fg=text_color, bg=background_color)
        self.name_label.place(relx=0.55, rely=0.2, anchor="w")

        self.location_label = tk.Label(self.developer_frame, text="Location: " + self.location, font=font_style, fg=text_color, bg=background_color)
        self.location_label.place(relx=0.55, rely=0.3, anchor="w")

        self.email_label = tk.Label(self.developer_frame, text="Email: " + self.email, font=font_style, fg=text_color, bg=background_color)
        self.email_label.place(relx=0.55, rely=0.4, anchor="w")

        self.phone_label = tk.Label(self.developer_frame, text="Phone/WhatsApp: " + self.phone_number, font=font_style, fg=text_color, bg=background_color)
        self.phone_label.place(relx=0.55, rely=0.5, anchor="w")

        self.whatsapp_label = tk.Label(self.developer_frame, text="YouTube: " + self.YouTube, font=font_style, fg=text_color, bg=background_color)
        self.whatsapp_label.place(relx=0.55, rely=0.6, anchor="w")

        # Create a button to go back to the previous menu
        self.close_button = tk.Button(self.developer_frame, text="Contact me!", command=self.open_contact, font=('Comic sans ms', 17, "bold"), bg="blue", fg="#fff", cursor="hand2")
        self.close_button.place(relx=0.65, rely=0.75, anchor="center")

    def open_contact(self):
        try:
            subprocess.Popen(["python", "contact.py"])  # Run the contact.py script
        except Exception as e:
            print(f"Failed to open contact.py: {e}")

    def display_notes(self):
        self.clear_sub_menu()
        self.random_words = [
            "For This System to work well, ensure you do the following:\n - Ensure enough light condition \n - Keep yourself so close to camera for good image processing \n - Register minimum users for reducing waiting time for logins or logouts",
            "If you face so much waiting time, do the following:\n - Reduce number of users or contact a developer to create a system handle many users (but it is not as quick as this system), because this System find a match to a login or logout user in every picture of your users \n - Update user profiles (photos) regularly to ensure accuracy",
            "- For this System, Leaving webcam for a long period of time do not affect anything because your computer will be busy only if you click login or logout buttons",
            "- Making a webcam auto-taking attendance without login or logout buttons, results in following effects:\n - Stucks of the webcam when multiple users access the webcam \n - Overheating of your computer if webcam is on for a long time, since auto-taking webcam is busy all the time",
            "- You can add a category of user in brackets when register username like John (Secretary) for easier way to track attendance of secretaries after printing attendance",
            "- Regular checking of notes, helps you to understand some hidden features of this program",
            "- If you have many users and you face much waiting time, reduce users or you can install this program in other computer and register new users",  
            "- This System can be adjusted to use external camera or internal camera (camera of your computer)",
            "- This system cannot handle many users faster because user is authenticated by looping face match calculations in each user image stored"
        ]
        
        # Initialize the index for random note selection if it doesn't exist
        if not hasattr(self, 'note_index'):
            self.note_index = random.randint(0, len(self.random_words) - 1)
        
        word = self.random_words[self.note_index]

        # Create a Text widget
        self.notes_text = tk.Text(self.sub_menu_frame, wrap='word', bg='lightgray', borderwidth=0, highlightthickness=0)
        self.notes_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Insert title with a tag
        self.notes_text.insert(tk.END, "Message of the Day:\n", "title")
        
        # Insert content with a different tag
        self.notes_text.insert(tk.END, word, "content")
        
        # Configure the tags
        self.notes_text.tag_configure("title", font=('Helvetica', 23, 'bold'), spacing1=10, spacing3=10, lmargin1=20, lmargin2=20, rmargin=20)
        self.notes_text.tag_configure("content", font=('Helvetica', 18), spacing1=10, spacing3=10, lmargin1=20, lmargin2=20, rmargin=20)
        
        # Make the Text widget read-only
        self.notes_text.configure(state='disabled')

        # Add buttons
        button_frame = tk.Frame(self.sub_menu_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

        button_style = {
            "font": ('Helvetica', 16, 'bold'),
            "bg": "#80c1ff",
            "fg": "black",
            "activebackground": "darkblue",
            "activeforeground": "white"
        }

        # Text-to-speech button
        tts_button = tk.Button(button_frame, text="Read Aloud", command=self.read_text_aloud, **button_style)
        tts_button.pack(side=tk.LEFT, padx=10)

        # Previous/Next buttons
        prev_button = tk.Button(button_frame, text="Previous", command=self.show_previous_note, **button_style)
        prev_button.pack(side=tk.RIGHT, padx=10)

        next_button = tk.Button(button_frame, text="Next", command=self.show_next_note, **button_style)
        next_button.pack(side=tk.RIGHT, padx=10)

    def read_text_aloud(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Set female voice and reduce speed
        for voice in voices:
            if 'female' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.setProperty('rate', 150)  # Adjust the speed (lower value means slower)

        engine.say(self.notes_text.get("1.0", tk.END))
        engine.runAndWait()

    def show_previous_note(self):
        self.note_index = (self.note_index - 1) % len(self.random_words)
        self.display_notes()

    def show_next_note(self):
        self.note_index = (self.note_index + 1) % len(self.random_words)
        self.display_notes()





    def display_attendance(self):
        self.clear_sub_menu()

        # Create left-hand side frame for filters and actions
        self.left_frame = ttk.Frame(self.sub_menu_frame, width=200, padding=(10, 10, 10, 10))
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Create right-hand side frame for the log display
        self.right_frame = ttk.Frame(self.sub_menu_frame, padding=(10, 10, 10, 10))
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Filter by name
        self.filter_label = ttk.Label(self.left_frame, text="Filter by Name:", font=("Helvetica", 15))
        self.filter_label.pack(pady=5)

        self.filter_entry = ttk.Entry(self.left_frame, font=("Helvetica", 15))
        self.filter_entry.pack(pady=5)

        self.filter_button = tk.Button(
            self.left_frame,
            text="Filter",
            font=("Helvetica", 14),
            command=self.filter_logs
        )
        self.filter_button.pack(pady=5)

        # Appearance section with label and read-only input in a single row
        appearance_frame = ttk.Frame(self.left_frame)
        appearance_frame.pack(pady=10, fill=tk.X)

        self.appearance_label = ttk.Label(appearance_frame, text="Appearance:", font=("Helvetica", 12))
        self.appearance_label.pack(side=tk.LEFT, padx=5)

        self.appearance_entry = ttk.Entry(appearance_frame, state='readonly', font=("Helvetica", 12))
        self.appearance_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Print attendance button
        self.print_icon = self.load_image("nav/print.png", (30, 30))
        self.print_button = tk.Button(
            self.left_frame,
            image=self.print_icon,
            text=" Print ",
            font=("Helvetica", 15),
            command=self.print_attendance,
            compound=tk.LEFT
        )
        self.print_button.pack(pady=15)

        # Delete selected row button
        self.delete_row_button = tk.Button(
            self.left_frame,
            text="Delete Selected Row",
            font=("Helvetica", 12),
            command=self.delete_selected_row
        )
        self.delete_row_button.pack(pady=5)

        # Delete all logs button
        self.delete_all_button = tk.Button(
            self.left_frame,
            text="Delete All Data",
            font=("Helvetica", 14),
            command=self.delete_all_logs
        )
        self.delete_all_button.pack(pady=5)

        # Read the log file
        log_file_path = 'log.txt'
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                self.logs = log_file.readlines()

        # Create a treeview to display the logs
        columns = ('Name', 'Timestamp', 'Status')
        self.treeview = ttk.Treeview(self.right_frame, columns=columns, show='headings')
        self.treeview.heading('Name', text='Name')
        self.treeview.heading('Timestamp', text='Timestamp')
        self.treeview.heading('Status', text='Status')

        # Add a vertical scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert the logs into the treeview
        for log in self.logs:
            name, timestamp, status = log.strip().split(',')
            self.treeview.insert('', tk.END, values=(name, timestamp, status))

        self.treeview.pack(fill=tk.BOTH, expand=True, pady=10)


  

    def filter_logs(self):
        filter_name = self.filter_entry.get().strip()
        if filter_name:
            filtered_logs = [log for log in self.logs if log.startswith(filter_name)]
            self.update_treeview(filtered_logs)
            appearances = len(filtered_logs)
            self.appearance_entry.configure(state='normal')
            self.appearance_entry.delete(0, tk.END)
            self.appearance_entry.insert(0, str(appearances))
            self.appearance_entry.configure(state='readonly')

    def update_treeview(self, logs):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for log in logs:
            name, timestamp, status = log.strip().split(',')
            self.treeview.insert('', tk.END, values=(name, timestamp, status))

    def print_attendance(self):
        pdf_path = 'attendance.pdf'
        doc = SimpleDocTemplate(pdf_path, pagesize=pagesizes.A4)
        elements = []

        # Add a title
        elements.append(Table([["Attendance Logs"]], colWidths=[doc.width]))
        elements.append(Table([[""]]))

        # Prepare the data for the table
        data = [["Name", "Timestamp", "Status"]]
        for log in self.logs:
            data.append(log.strip().split(','))

        # Create the table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

        # Build the PDF
        doc.build(elements)
        messagebox.showinfo("Success", f"Attendance logs printed to {pdf_path}")

    def delete_selected_row(self):
        selected_item = self.treeview.selection()
        if selected_item:
            log_to_delete = self.treeview.item(selected_item)['values']
            self.treeview.delete(selected_item)
            self.logs = [log for log in self.logs if not (log.startswith(log_to_delete[0]) and log_to_delete[1] in log)]
            self.write_logs_to_file()
            messagebox.showinfo("Success", "Selected row deleted successfully.")
        else:
            messagebox.showwarning("Warning", "No row selected. Please select a row to delete.")

    def delete_all_logs(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all logs?")
        if confirm:
            self.logs = []
            self.update_treeview(self.logs)
            self.write_logs_to_file()
            messagebox.showinfo("Success", "All logs deleted successfully.")


    def write_logs_to_file(self):
        with open('log.txt', 'w') as log_file:
            log_file.writelines(self.logs)

    def display_login_logout(self):
        self.clear_sub_menu()
        login_script_path = os.path.join(os.path.dirname(__file__), 'webcam.py')
        subprocess.run(["python", login_script_path])
        self.print_label = ttk.Label(self.sub_menu_frame, text="Click a login-logout again to open a new login | logout webcam", font=('Helvetica', 23))
        self.print_label.pack(pady=200)



    def display_profile(self):
        self.clear_sub_menu()

        # Create a frame to hold the canvas and scrollbar
        self.canvas_frame = tk.Frame(self.sub_menu_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the canvas
        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the vertical scrollbar
        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the vertical scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Create a frame inside the canvas to hold images
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor=tk.NW)

        # Bind the canvas to update the scroll region when the image_frame is resized
        self.image_frame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

        # Load images into the image_frame
        self.load_images()

        # Create a frame for the buttons immediately below the image frame
        self.button_frame = tk.Frame(self.canvas_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Create and pack the buttons
        self.delete_button = tk.Button(
            self.button_frame,
            text="Delete Selected Photo",
            font=("Helvetica", 15),
            command=self.delete_selected_photo
        )
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_all_button = tk.Button(
            self.button_frame,
            text="Delete All Photos",
            font=("Helvetica", 15),
            command=self.delete_all_photos
        )
        self.delete_all_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def load_images(self):
        # Clear existing images
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Directory where images are stored
        db_dir = 'db'

        # Load and display images in the image_frame
        row = 0
        col = 0
        for image_file in os.listdir(db_dir):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_path = os.path.join(db_dir, image_file)
                image = Image.open(img_path)
                image = image.resize((120, 100))  # Resize as needed
                photo = ImageTk.PhotoImage(image)
                
                label = tk.Label(self.image_frame, image=photo)
                label.image = photo  # Keep a reference to avoid garbage collection
                label.grid(row=row, column=col, padx=10, pady=10)
                label.bind("<Button-1>", lambda e, path=img_path: self.select_image(path))  # Bind click event

                col += 1
                if col >= 5:  # Change 5 to the number of columns you want
                    col = 0
                    row += 1

    def select_image(self, img_path):
        self.selected_image_path = img_path
        # Indicate selection in the UI (optional)
        print(f"Selected image: {self.selected_image_path}")

    def delete_selected_photo(self):
        if hasattr(self, 'selected_image_path') and self.selected_image_path:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this photo?"):
                try:
                    os.remove(self.selected_image_path)
                    self.selected_image_path = None
                    self.load_images()  # Refresh the image list
                    messagebox.showinfo("Success", "Photo deleted successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete photo: {e}")
        else:
            messagebox.showwarning("No Selection", "No photo selected for deletion.")

    def delete_all_photos(self):
        db_dir = 'db'  # Set your database directory here
        if messagebox.askyesno("Confirm Delete All", "Are you sure you want to delete all photos?"):
            try:
                image_files = [f for f in os.listdir(db_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                for image_file in image_files:
                    os.remove(os.path.join(db_dir, image_file))
                self.load_images()  # Refresh the image list
                messagebox.showinfo("Success", "All photos deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete all photos: {e}")


    def clear_sub_menu(self):
        for widget in self.sub_menu_frame.winfo_children():
            widget.destroy()

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.side_nav_canvas.configure(width=110)
            self.side_nav_frame.configure(width=107)
            self.menu_button.configure(image=self.menu_icon, text="", compound=tk.CENTER)
            self.signout_button.configure(image=self.signout_icon, text="", compound=tk.CENTER)
            for button, label in self.buttons:
                button.configure(compound=tk.CENTER, text="", padding=0)
                label.pack_forget()
            self.sidebar_expanded = False
        else:
            self.side_nav_canvas.configure(width=160)
            self.side_nav_frame.configure(width=160)
            self.menu_button.configure(image=self.menu_icon, text="Menu", compound=tk.LEFT, padding=(0, 0, 0, 0))
            self.signout_button.configure(image=self.signout_icon, text="Exit", compound=tk.LEFT, padding=(0, 0, 0, 0))
            for button, label in self.buttons:
                button.configure(compound=tk.LEFT, text=label.cget("text"), padding=(0, 0, 0, 0))
                label.pack_forget()
            self.sidebar_expanded = True

    def confirm_sign_out(self):
        answer = messagebox.askyesno("Confirmation", "Are you sure you want to quit?")
        if answer:
            self.sign_out()

    def sign_out(self):
        # Close the whole window
        self.root.destroy()

if __name__ == "__main__":
    parent = tk.Tk()
    app = SideNavApp(parent)
    parent.mainloop()
