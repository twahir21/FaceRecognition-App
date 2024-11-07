import os
import pickle
from PIL import Image, ImageTk

import tkinter as tk
from tkinter import messagebox
import face_recognition


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="#3b403c",
                        activeforeground="black",
                        fg=fg,
                        bg=color,
                        command=command,
                        cursor="hand2",
                        height=2,
                        width=20,
                        font=('sans-serif', 25, "bold")
                    )

    return button



def get_log_buttons(window, text, color, command, fg='black', image_path=None):
    # Create the button with appropriate dimensions
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="#3b403c",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=80,  # Adjust height
                        width=300,  # Adjust width
                        font=('sans-serif', 20, "bold"), 
                        padx=20,
                        pady=4,
                        compound=tk.LEFT  # Image will be on the left, text on the right
                    )
    
    # If an image path is provided, set the image on the button
    if image_path:
        # Load the image
        img = Image.open(image_path)
        img = img.resize((50, 50))  # Resize the image to fit well in the button
        img_tk = ImageTk.PhotoImage(img)  # Convert image to ImageTk format
        
        # Set the image on the button
        button.config(image=img_tk)
        button.image = img_tk  # Keep a reference to avoid garbage collection

    return button





def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=20, font=("Arial", 23))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'

