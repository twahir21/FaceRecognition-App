import os
import datetime
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import subprocess
import util
import pygame  # Import pygame for audio

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.resizable(False, False)


        self.main_window.title("Login | Logout webcam")
        self.main_window.iconbitmap("icon.ico")

        self.login_button_main_window = util.get_log_buttons(
            self.main_window,
            'login',
            '#358c4b',
            self.login,
            image_path='nav/login.png'  # Specify the path to your login button image
        )
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_log_buttons(
            self.main_window,
            'logout',
            '#cc5a63',
            self.logout,
            image_path='nav/logout.png'  # Specify the path to your logout button image
        )
        self.logout_button_main_window.place(x=750, y=350)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = 'db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = 'log.txt'

        pygame.mixer.init()  # Initialize the pygame mixer for audio

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)  # Ensure the correct index

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame")
            self._label.after(20, self.process_webcam)
            return

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)  # Load the audio file
        pygame.mixer.music.play()  # Play the audio file

    def login(self):
        unknown_img_path = "tmp.jpg"
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
       
        os.remove(unknown_img_path)
        name = output.split(',')[1][:-5]

       
        if name == 'unknown_person':
            self.play_sound("unknown_user.opus")  # Play audio for unknown user
        elif name == "no_persons_found":
            self.play_sound("sounds/no_person.opus")  # Play audio for no person found
        else:
            self.play_sound("sounds/loginuser.opus")  
            with open(self.log_path, 'a') as f:
                f.write('{},{},in\n'.format(name, datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
                f.close()

    def logout(self):
        unknown_img_path = "tmp.jpg"
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
       
        os.remove(unknown_img_path)
        name = output.split(',')[1][:-5]
       
        if name == 'unknown_person':
            self.play_sound("sounds/unknown_user.opus")  # Play audio for unknown user
        elif name == "no_persons_found":
            self.play_sound("sounds/no_person.opus")  # Play audio for no person found
        else:
            self.play_sound("sounds/logoutuser.opus")  # Play audio for goodbye
            with open(self.log_path, 'a') as f:
                f.write('{},{},out\n'.format(name, datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
                f.close()

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
