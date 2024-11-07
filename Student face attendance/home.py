# import tkinter and Pillow
from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import numpy as np
import cv2
import mysql.connector
import datetime
import csv
import subprocess
import sys
import os
import platform


from student import Student
from csv_viewer import CSVViewerApp
from developer import DeveloperDetailsGUI
from faceRecognizer import FaceRecognitionApp
from ChatBot import ChatBotApp

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class FaceRecognitionSystem:
    def __init__(self, root):

        self.root = root
        self.root.geometry("1530x790")

        self.root.title("Face Recognition System")

        # Load and resize images
        img1 = Image.open(resource_path("images\\title.png")).resize((500, 130))
        img2 = Image.open(resource_path("images\\title2.png")).resize((500, 130))
        img3 = Image.open(resource_path("images\\image.jpg")).resize((500, 130))
        # background image
        background = Image.open(resource_path("images\\bg.png")).resize((1530, 710))
        # buttons
        student = Image.open(resource_path("images\\student.png")).resize((250,220))
        face = Image.open(resource_path("images\\face.png")).resize((250,220))
        attendance = Image.open(resource_path("images\\title1.png")).resize((300,220))
        helpdesk = Image.open(resource_path("images\\helpDesk.png")).resize((220,220))
        train = Image.open(resource_path("images\\train.png")).resize((500,220))
        photos = Image.open(resource_path("images\\photo.png")).resize((350,220))
        developer = Image.open(resource_path("images\\developer.png")).resize((500,220))
        nane = Image.open(resource_path("images\\exit.png")).resize((250,220))

        # Convert images to PhotoImage
        self.photoImg1 = ImageTk.PhotoImage(img1)
        self.photoImg2 = ImageTk.PhotoImage(img2)
        self.photoImg3 = ImageTk.PhotoImage(img3)
        self.photoImg4 = ImageTk.PhotoImage(background)
        self.photoImg5 = ImageTk.PhotoImage(student)
        self.photoImg6 = ImageTk.PhotoImage(face)
        self.photoImg7 = ImageTk.PhotoImage(attendance)
        self.photoImg8 = ImageTk.PhotoImage(helpdesk)
        self.photoImg9 = ImageTk.PhotoImage(train)
        self.photoImg10 = ImageTk.PhotoImage(photos)
        self.photoImg11 = ImageTk.PhotoImage(developer)
        self.photoImg12 = ImageTk.PhotoImage(nane)

        # Place images in a single row
        f_lbl1 = Label(self.root, image=self.photoImg1)
        f_lbl1.place(x=0, y=0, width=500, height=130)

        f_lbl2 = Label(self.root, image=self.photoImg2)
        f_lbl2.place(x=450, y=0, width=500, height=130)

        f_lbl3 = Label(self.root, image=self.photoImg3)
        f_lbl3.place(x=900, y=0, width=500, height=130)

        f_lbl4 = Label(self.root, image=self.photoImg4)
        f_lbl4.place(x=0, y=130, width=1530, height=710)

        title_lbl = Label(self.root, text="ATTENDANCE SYSTEM BY FACE RECOGNITION", font=("Tahoma", 35, "bold"), bg="white", fg="brown")
        title_lbl.place(x=0, y=130, width=1530, height=45)



        # student button
        b1 = Button(self.root, image=self.photoImg5, command=self.student_details, cursor="hand2")
        b1.place(x=100, y=200, width=220, height=220)

        b1 = Button(self.root, text="Student Details", command=self.student_details, cursor="hand2", font=("Comic Sans MS", 15, "bold"), bg="dark blue", fg="white")
        b1.place(x=100, y=400, width=220, height=40)

        # Photos button
        b2 = Button(self.root, image=self.photoImg10, command=self.open_image, cursor="hand2")
        b2.place(x=400, y=200, width=220, height=220)

        b2 = Button(self.root, text="View Photos", command=self.open_image, cursor="hand2", font=("Comic Sans MS", 15, "bold"), bg="dark blue", fg="white")
        b2.place(x=400, y=400, width=220, height=40)

        # Train Datasets
        b2 = Button(self.root, image=self.photoImg9, command=self.train_data, cursor="hand2")
        b2.place(x=700, y=200, width=220, height=220)

        b2 = Button(self.root, text="Train Datasets", command=self.train_data, cursor="hand2", font=("Comic Sans MS", 15, "bold"), bg="dark blue", fg="white")
        b2.place(x=700, y=400, width=220, height=40)

        # Face Recognizer
        b2 = Button(self.root, image=self.photoImg6, command=self.face_recog, cursor="hand2")
        b2.place(x=1000, y=200, width=220, height=220)

        b2 = Button(self.root, text="Face Recognizer", cursor="hand2", command=self.face_recog, font=("Comic Sans MS", 15, "bold"), bg="dark blue", fg="white")
        b2.place(x=1000, y=400, width=220, height=40)

        # View Attendance
        b2 = Button(self.root, image=self.photoImg7, command=self.csv_viewer, cursor="hand2")
        b2.place(x=100, y=450, width=220, height=220)

        b2 = Button(self.root, text="View Attendance", command=self.csv_viewer, cursor="hand2", font=("Comic Sans MS", 15, "bold"), bg="dark blue", fg="white")
        b2.place(x=100, y=650, width=220, height=40)

        # Help desk chatbot
        b2 = Button(self.root, image=self.photoImg8, command=self.open_robot_gui, cursor="hand2")
        b2.place(x=400, y=450, width=220, height=220)

        b2 = Button(self.root, text="Chat_Bot", command=self.open_robot_gui, cursor="hand2", font=("Comic Sans MS", 15, "bold"), bg="dark blue", fg="white")
        b2.place(x=400, y=650, width=220, height=40)

        # developer
        b2 = Button(self.root, image=self.photoImg11, command=self.developer, cursor="hand2")
        b2.place(x=700, y=450, width=220, height=220)

        b2 = Button(self.root, text="Developer", command=self.developer, cursor="hand2", font=("Comic Sans MS", 15, "bold"), bg="dark blue", fg="white")
        b2.place(x=700, y=650, width=220, height=40)

        # exit
        b2 = Button(self.root, image=self.photoImg12, command=self.close_window, cursor="hand2")
        b2.place(x=1000, y=450, width=220, height=220)

        b2 = Button(self.root, text="Exit", command=self.close_window, cursor="hand2", font=("Comic Sans MS", 15, "bold"), bg="dark blue", fg="white")
        b2.place(x=1000, y=650, width=220, height=40)

     # ====================Function Buttons===================
    def student_details(self):
            self.new_window = Toplevel(self.root)
            self.app = Student(self.new_window)

    def open_image(self):
         os.startfile("data")


    def train_data(self):
        data_dir = ("data")
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []


        for image in path:
            img = Image.open(image).convert('L') # Gray scale image
            imgNp = np.array(img, 'uint8')

            # image = r"C:\Users\Twahir Sudy\Desktop\user\pythonProje\GUI\data\8_1.jpg"  # Example image path
            id = int(os.path.split(image)[1].split('_')[0])

            img_resized = cv2.resize(imgNp, (300, 300))  
            faces.append(imgNp)
            ids.append(id)
            cv2.imshow("Training", img_resized)
            cv2.waitKey(1) == 13
            cv2.namedWindow("Training", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Training", 300, 300) 
            

        ids = np.array(ids)

        # ============== Train the classifier and save================
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        classifier_path = "classifier.xml"
        clf.write(classifier_path)

        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Training Data Sets completed.", parent=self.root)


    def close_window(self):
         if messagebox.askokcancel("Quit", "Do you want to quit", parent=self.root):
            self.root.destroy()
         else:
            return

    def csv_viewer(self):
        self.new_window = Toplevel(self.root)
        self.app = CSVViewerApp(self.new_window)

    def open_robot_gui(self):
        self.new_window = Toplevel(self.root)
        self.app = ChatBotApp(self.new_window) 
    
    def developer(self):
        self.new_window = Toplevel(self.root)
        self.app = DeveloperDetailsGUI(self.new_window) 
    
    def face_recog(self):
        self.new_window = Toplevel(self.root)
        self.app = FaceRecognitionApp(self.new_window) 


    def run(self):
        self.root.mainloop()

  

if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognitionSystem(root)
    obj.run()
