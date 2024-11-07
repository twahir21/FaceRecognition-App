import tkinter as tk
from tkinter import messagebox
import cv2
import csv
import datetime
from PIL import Image, ImageTk
import cv2.face
import winsound

class FaceRecognitionApp:
    def __init__(self, master):
        self.master = master
        master.title("Face Recognition")
        master.geometry("800x600")
        master.resizable(False, False)

        self.background_image = Image.open("images\\bgface.png").resize((800, 600))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(x=0, y=2, relwidth=1, relheight=1)

        self.start_button = tk.Button(master, text="Start Recognition", command=self.start_recognition,
                                      font=("Comic Sans MS", 20, "bold"), cursor="hand2", bg="green", fg="yellow")
        self.start_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    def fetch_student_data(self, student_id):
        try:
            with open("student_details.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 6 and row[4] == student_id:  # Check if the row has enough elements
                        name = row[5]
                        year = row[2]
                        course = row[1]
                        return name, year, course
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def play_sound(self):
        winsound.Beep(1000, 200)  # Beep sound for 200 milliseconds at 1000 Hz

    def start_recognition(self):
        def write_to_csv_once(name, year, department):
            if not hasattr(self, 'csv_written'):
                with open('recognized_students.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    record_datetime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    writer.writerow([name, year, department, record_datetime])
                self.csv_written = True
                self.play_sound()  # Play sound after saving a user

        def recognize_and_mark(img, clf, faceCascade):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, confidence = clf.predict(gray[y:y+h, x:x+w])

                # Check if the face is recognized with confidence level > 77
                if confidence > 77:
                    student_data = self.fetch_student_data(id)
                    if student_data:
                        name, year, course = student_data
                    else:
                        name, year, course = "Unknown", "Unknown", "Unknown"

                    cv2.putText(img, f"Name: {name}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.putText(img, f"Year: {year}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.putText(img, f"Course: {course}", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

                    write_to_csv_once(name, year, course)

                    # Play sound after successful recognition
                    self.play_sound()

                else:
                    cv2.putText(img, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

            return img

        # Initialize face cascade and classifier
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        # Initialize video capture
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture image from webcam.")
                break

            frame = recognize_and_mark(frame, clf, faceCascade)
            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
