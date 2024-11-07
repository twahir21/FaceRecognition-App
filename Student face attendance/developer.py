import tkinter as tk
from PIL import Image, ImageTk

class DeveloperDetailsGUI:
    def __init__(self, master):
        self.master = master
        master.title("Developer Details")
        master.geometry("800x500")

        # Background Image
        self.background_image = Image.open("images/bgdeveloper2.png").resize((1600, 800))  
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(x=0, y=2, relwidth=1, relheight=1)  

        # Developer details
        self.developer_name = "Twahir Sudy"
        self.location = "Dar es Salaam, Tanzania"
        self.email = "twahirsudy3@gmail.com"
        self.phone_number = "+255 62 103 1195"
        self.whatsApp = "+255 67 429 1587"

        # Load and display the developer's picture
        self.developer_image = Image.open("images/twahir.jpg").resize((300, 400))  
        self.photo = ImageTk.PhotoImage(self.developer_image)
        self.image_label = tk.Label(master, image=self.photo, bg="white")
        self.image_label.place(relx=0.25, rely=0.46, anchor="center")

        # Display developer details with Comic Sans MS font
        font_style = ("Comic Sans MS", 15)
        self.name_label = tk.Label(master, text="Name: " + self.developer_name, font=font_style, fg="blue", bg="white")
        self.name_label.place(relx=0.75, rely=0.2, anchor="center")

        self.location_label = tk.Label(master, text="Location: " + self.location, font=font_style, fg="blue", bg="white")
        self.location_label.place(relx=0.75, rely=0.3, anchor="center")

        self.email_label = tk.Label(master, text="Email: " + self.email, font=font_style, fg="blue", bg="white")
        self.email_label.place(relx=0.75, rely=0.4, anchor="center")

        self.phone_label = tk.Label(master, text="Phone: " + self.phone_number, font=font_style, fg="blue", bg="white")
        self.phone_label.place(relx=0.75, rely=0.5, anchor="center")

        self.whatsapp_label = tk.Label(master, text="WhatsApp: " + self.whatsApp, font=font_style, fg="blue", bg="white")
        self.whatsapp_label.place(relx=0.75, rely=0.6, anchor="center")

        # Create a button to close the window
        self.close_button = tk.Button(master, text="Back", command=master.destroy, font=font_style, bg="blue", fg="white", cursor="hand2")
        self.close_button.place(relx=0.75, rely=0.75, anchor="center")

def main():
    root = tk.Tk()
    app = DeveloperDetailsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
