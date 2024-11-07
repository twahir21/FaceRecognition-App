import os
import cv2
from PIL import Image, ImageTk
import face_recognition
import tkinter as tk
import util
import pygame  # Import pygame

class AddUser:
    def __init__(self, db_dir):
        self.db_dir = db_dir
        self.setup_main_window()
        self.setup_webcam()
        pygame.mixer.init()  # Initialize the pygame mixer
        


    def setup_main_window(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+370+120")

        self.main_window.title("Add User")
        self.main_window.iconbitmap("icon.ico")
        self.main_window.resizable(False, False)


        self.accept_button = util.get_button(self.main_window, 'Accept', 'green', self.confirm_accept_register_new_user)
        self.accept_button.place(x=750, y=350)

        self.capture_label = util.get_img_label(self.main_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.entry_text = tk.Entry(self.main_window, font=("sans-serif", 27), width=17)  # Increased width for better visibility
        self.entry_text.place(x=750, y=150, height=80)  # Use a height parameter if applicable

        self.text_label = tk.Label(self.main_window, text='Please, \ninput username:', font=("sans-serif", 25))
        self.text_label.place(x=750, y=70)

    def setup_webcam(self):
        self.cap = cv2.VideoCapture(0)  # Use the correct index if needed
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame")
            return

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self.capture_label.imgtk = imgtk                                
        self.capture_label.configure(image=imgtk)

        # Update the `capture` attribute
        self.capture = self.most_recent_capture_arr.copy()

        self.capture_label.after(20, self.process_webcam)

    def add_img_to_label(self):
        """Update the image in the label."""
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self.capture_label.imgtk = imgtk
        self.capture_label.configure(image=imgtk)
        
        # Ensure that `self.capture` is updated with the latest frame
        self.capture = self.most_recent_capture_arr.copy()

    def confirm_accept_register_new_user(self):
        self.accept_register_new_user()

    def accept_register_new_user(self):
        name = self.entry_text.get().strip()  # Correct reference to entry_text

        if not name:
            pygame.mixer.music.load("sounds/no_username.opus")  # Load the audio file
            pygame.mixer.music.play()  # Play the audio file
        
            return

        img_path = os.path.join(self.db_dir, f'{name}.jpg')

        # Check if the username already exists
        if os.path.exists(img_path):
            pygame.mixer.music.load("sounds/username.opus")
            pygame.mixer.music.play()
            return

        # Compute the face encoding for the new image
        new_image_encoding = self.compute_face_encoding(self.capture)  # Use `self.capture` for the image
        if new_image_encoding is None:
            pygame.mixer.music.load("sounds/better_image.opus")
            pygame.mixer.music.play()
            return

        # Compare with existing images in the database
        is_similar = False
        confidence_score = 1.0  # Initialize confidence score to maximum (100%)
        for filename in os.listdir(self.db_dir):
            if filename.endswith('.jpg'):
                existing_image_path = os.path.join(self.db_dir, filename)
                existing_image = face_recognition.load_image_file(existing_image_path)
                existing_image_encoding = face_recognition.face_encodings(existing_image)
                if existing_image_encoding:
                    # Compute the distance between the new and existing encodings
                    distance = face_recognition.face_distance([existing_image_encoding[0]], new_image_encoding)[0]
                    confidence_threshold = 0.6  # This is an example threshold; adjust as needed
                    confidence_score = 1 - distance  # Confidence score based on distance
                    if distance < confidence_threshold:
                        is_similar = True
                        break

        if is_similar:
            util.msg_box('Error', f'A similar face already exists in the database with a confidence score of {confidence_score * 100:.2f}%.')
            return

        # Save the new user's image
        cv2.imwrite(img_path, self.capture)
        pygame.mixer.music.load("sounds/register.opus")
        pygame.mixer.music.play()
        

    def compute_face_encoding(self, image):
        """Compute the face encoding for the given image."""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces and compute encodings
        face_locations = face_recognition.face_locations(rgb_image)
        if not face_locations:
            return None

        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        # Validate that at least one face encoding was found
        if not face_encodings:
            return None

        # Optionally, include more checks, such as the confidence score of the encoding
        # For simplicity, we assume the first encoding is sufficient
        return face_encodings[0]

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    db_dir = 'db'  # Set your database directory here
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app = AddUser(db_dir)
    app.start()
