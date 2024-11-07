from tkinter import * 
from tkinter import ttk
from PIL import Image, ImageTk
from _tkinter import *
from tkinter import messagebox
# pip install mysql-connector-python
# pip install opencv-python 4.9.0.80

import cv2
import os
import csv

 
class Student:
    def __init__(self, root):
        

        self.root = root
        self.root.geometry("1530x790")
        self.root.title("Face Recognition System")


        #==============Variables====================
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_id = StringVar()
        self.var_gender = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_semester = StringVar()
        self.var_index = StringVar()


        title_lbl = Label(self.root, text="STUDENT MANAGEMENT SYSTEM", font=("Comic Sans MS", 35, "bold"), fg="green", bg="white")
        title_lbl.place(x=0, y=10, width=1530, height=45)


        # Student Details
        main_frame = Frame (self.root, bd=2)
        main_frame.place(x=0, y=60, width=1500, height=625)

        # left label frame
        Left_frame = LabelFrame (main_frame, bd=2, relief=RIDGE, text="Student Details", font=("Comic Sans MS", 12, "bold"), fg="red")
        Left_frame.place(x=10, y=10, width=660, height=620)

        #inserting an image
        img_left = Image.open("images\\youngBoy.png").resize((600, 200))
        self.photoImg5 = ImageTk.PhotoImage(img_left)
        f_lbl5 = Label(self.root, image=self.photoImg5)
        f_lbl5.place(x=60, y=100, width=550, height=200)
 
        # current Course Information
        current_course_frame = LabelFrame (Left_frame, bd=2, relief=RIDGE, text="Current Course Information", font=("Comic Sans MS", 12, "bold"), fg="green")
        current_course_frame.place(x=5, y=205, width=650, height=115)

        # Department
        dep_label = Label(current_course_frame, text="Department", font=("Comic Sans MS", 11, "bold"))
        dep_label.grid(row=0, column=0, padx=10)

        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, font=("Comic Sans MS", 11, "bold"), state="readonly", width="27")
        dep_combo["values"] = ("Select Department", "Computer Studies", "Mechanical", "Civil", "Electrical")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10)

        # Courses
        course_label = Label(current_course_frame, text="Courses", font=("Comic Sans MS", 11, "bold"))
        course_label.grid(row=1, column=0, padx=10)

        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=("Comic Sans MS", 11, "bold"), state="readonly", width="27")
        course_combo["values"] = ("Select Course", "Computer Engineering", "Civil Engineering", "Mechanical Engineering", "Electrical Engineering", "Telecommunication Engineering")
        course_combo.current(0)
        course_combo.grid(row=1, column=1, padx=2, pady=10)


        # Year
        year_label = Label(current_course_frame, text="Year", font=("Comic Sans MS", 11, "bold"))
        year_label.grid(row=0, column=2, padx=10)

        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=("Comic Sans MS", 10, "bold"), state="readonly", width="18")
        year_combo["values"] = ("Select Academic Year", "BENG-20","BENG-21", "BENG-22", "BENG-23", "OD-21", "OD-22", "OD-23")
        year_combo.current(0)
        year_combo.grid(row=0, column=3, padx=2, pady=10)

        # Semester
        semester_label = Label(current_course_frame, text="Semester", font=("Comic Sans MS", 11, "bold"))
        semester_label.grid(row=1, column=2, padx=10)

        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, font=("Comic Sans MS", 10, "bold"), state="readonly", width="18")
        semester_combo["values"] = ("Select Semester", "Semester-1", "Semester-2")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=2, pady=10)

        # Class Student Information
        Class_Student_frame = LabelFrame (Left_frame, bd=2, relief=RIDGE, text="Class Student Information", font=("Comic Sans MS", 12, "bold"), fg="green")
        Class_Student_frame.place(x=5, y=320, width=650, height=270)

        # Student ID
        StudentID_label = Label(Class_Student_frame, text="Student ID: ", font=("Comic Sans MS", 11, "bold"))
        StudentID_label.grid(row=0, column=0, padx=10)

        global StudentID_entry

        StudentID_entry = ttk.Entry(Class_Student_frame, width=20, textvariable=self.var_id, font=("Comic Sans MS", 11, "bold"))
        StudentID_entry.grid(row=0, column=1, padx=10)

        # Gender
        Gender_label = Label(Class_Student_frame, text="Gender", font=("Comic Sans MS", 11, "bold"))
        Gender_label.grid(row=1, column=0, padx=10)

        Gender_combo = ttk.Combobox(Class_Student_frame, textvariable=self.var_gender, font=("Comic Sans MS", 11, "bold"), state="readonly", width="20")
        Gender_combo["values"] = ("Select Gender", "Male", "Female")
        Gender_combo.current(0)
        Gender_combo.grid(row=1, column=1, padx=2, pady=10)

        # Student Name
        name_label = Label(Class_Student_frame, text="Full Name: ", font=("Comic Sans MS", 11, "bold"))
        name_label.grid(row=2, column=0, padx=10, pady=5)

    
        name_entry = ttk.Entry(Class_Student_frame, width=20, textvariable=self.var_name, font=("Comic Sans MS", 11, "bold"))

        name_entry.grid(row=2, column=1, padx=10, pady=5)  

        # Email
        Email_label = Label(Class_Student_frame, text="Email: ", font=("Comic Sans MS", 11, "bold"))
        Email_label.grid(row=2, column=2, padx=10, pady=5)

        Email_entry = ttk.Entry(Class_Student_frame, width=18, textvariable=self.var_email, font=("Comic Sans MS", 11, "bold"))
        Email_entry.grid(row=2, column=3, padx=10, pady=5)

        # Phone Number
        Phone_label = Label(Class_Student_frame, text="Phone: ", font=("Comic Sans MS", 11, "bold"))
        Phone_label.grid(row=0, column=2, padx=10, pady=5)

        Phone_entry = ttk.Entry(Class_Student_frame, width=18, textvariable=self.var_phone, font=("Comic Sans MS", 11, "bold"))

        Phone_entry.grid(row=0, column=3, padx=10, pady=5)  


        # Index
        index_label = Label(Class_Student_frame, text="Form IV index: ", font=("Comic Sans MS", 11, "bold"))
        index_label.grid(row=1, column=2, padx=1, pady=5)


        # Placeholder for index Entry
        index_entry = ttk.Entry(Class_Student_frame, textvariable=self.var_index, width=18, font=("Comic Sans MS", 11, "bold"))

        index_entry.grid(row=1, column=3, padx=10, pady=5)  

        # radio buttons
        self.var_radio1 = StringVar()
        radiobtn1 = ttk.Radiobutton(Class_Student_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes")
        radiobtn1.grid(row=5, column=0)

        radiobtn2  = ttk.Radiobutton(Class_Student_frame, variable=self.var_radio1, text="No Photo Sample", value="No")
        radiobtn2.grid(row=5, column=1)

        
        # buttons Frame
        btn_frame = Frame(Class_Student_frame, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=140, width=645, height=45)

        save_btn = Button(btn_frame, text="Save", command=self.add_data, width=15, font=("Comic Sans MS", 13, "bold"), bg="lightgreen", fg="black", pady=5, cursor="hand2")
        save_btn.pack(side=LEFT, padx=0)

        Update_btn = Button(btn_frame, text="Update",command=self.update_data, width=15, font=("Comic Sans MS", 13, "bold"), bg="lightgreen", fg="black", pady=5, cursor="hand2")
        Update_btn.pack(side=LEFT, padx=10)

        Delete_btn = Button(btn_frame, text="Delete", command=self.delete_data, width=15, font=("Comic Sans MS", 13, "bold"), bg="lightgreen", fg="black", pady=5, cursor="hand2")
        Delete_btn.pack(side=LEFT, padx=10)

        Reset_btn = Button(btn_frame, text="Reset", command=self.reset_data, width=15, font=("Comic Sans MS", 13, "bold"), bg="lightgreen", fg="black", pady=5, cursor="hand2")
        Reset_btn.pack(side=LEFT)


        btn_frame1 = Frame(Class_Student_frame, bd=2, relief=RIDGE)
        btn_frame1.place(x=0, y=190, width=645, height=55)

        TakePhoto_btn = Button(btn_frame1, text="Take Photo Sample", command=self.generate_dataset, width=23, font=("Comic Sans MS", 13, "bold"), bg="green", fg="white", pady=10, cursor="hand2")
        TakePhoto_btn.grid(row=0, column=0)

        DeletePhoto_btn = Button(btn_frame1, text="Delete Photos", command=self.delete_photos_by_entry, width=15, font=("Comic Sans MS", 13, "bold"), bg="green", fg="white", pady=10, cursor="hand2")
        DeletePhoto_btn.grid(row=0, column=1, padx=5)

        UpdatePhoto_btn = Button(btn_frame1, text="Update Photo Sample", command=self.update_photo_samples, width=23, font=("Comic Sans MS", 13, "bold"), bg="green", fg="white", pady=10, cursor="hand2")
        UpdatePhoto_btn.grid(row=0, column=2, padx=5)
 

        # right label frame
        Right_frame = LabelFrame (main_frame, bd=2, relief=RIDGE, text="Saved Details", font=("Comic Sans MS", 12, "bold"), fg="red")
        Right_frame.place(x=680, y=10, width=660, height=613)

        #inserting an image
        img_right = Image.open("images\\youngGirl.png").resize((550, 200))
        self.photoImg6 = ImageTk.PhotoImage(img_right)
        f_lbl6 = Label(self.root, image=self.photoImg6)
        f_lbl6.place(x=740, y=100, width=550, height=220)


        # ============Search System ===============
        # fg is also foreground and bg is also background
        Search_Frame = LabelFrame(Right_frame, foreground="green", bd=2, relief=RIDGE, text="Search System", font=("Comic Sans MS", 12, "bold"))
        Search_Frame.place(x=5, y=230, width=648, height=80)

        search_label = Label(Search_Frame, text="Search By:", font=("Comic Sans MS", 15, "bold"), fg="blue", bg="yellow")
        search_label.grid(row=0, column=0, padx=10, pady=5)

        # make search_combo and search_entry global
        global search_combo, search_entry
        search_combo = ttk.Combobox(Search_Frame, font=("Comic Sans MS", 12), state="readonly", width="10")
        search_combo["values"] = ("Select", "Full Name", "Student ID")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10)

        search_entry = ttk.Entry(Search_Frame, width=15, font=("Comic Sans MS", 13))
        search_entry.grid(row=0, column=2, padx=2)

        # Create the Search and Show All buttons
        search_btn = Button(Search_Frame, text="Search", command=self.search_data, cursor="hand2", font=("Comic Sans MS", 13), bg="lightgreen")
        search_btn.grid(row=0, column=3, padx=4)

        showAll_btn = Button(Search_Frame, text="Show All", command=self.fetch_data, cursor="hand2", font=("Comic Sans MS", 13), bg="lightgreen")
        showAll_btn.grid(row=0, column=4, padx=4)

        #=================Label Frame==============================
        Table_Frame = Frame(Right_frame, bd=2, relief=RIDGE)
        Table_Frame.place(x=5, y=315, width=648, height=263)

        scroll_X = ttk.Scrollbar(Table_Frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(Table_Frame, orient="vertical")

        self.student_table = ttk.Treeview(Table_Frame, columns=("dep", "course", "year", "sem", "id", "name", "gender", "email", "phone", "photo","index"), xscrollcommand=scroll_X.set, yscrollcommand=scroll_y.set)

        scroll_X.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y") 
        scroll_X.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="Student ID")
        self.student_table.heading("name", text="Full Name")  
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("photo", text="Photo Sample Status")
        self.student_table.heading("index", text="Form IV index")
        self.student_table["show"] = "headings"

        
        self.student_table.column("dep", width=150)
        self.student_table.column("course", width=200)
        self.student_table.column("id", width=100)
        self.student_table.column("photo", width=40)
        self.student_table.column("sem", width=100)
        self.student_table.column("name", width=160)  
        self.student_table.column("year", width=80)
        self.student_table.column("email", width=180)
        self.student_table.column("phone", width=100)
        self.student_table.column("index", width=100)
        self.student_table.column("gender", width=80)


        self.student_table.pack(fill="both", expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    #===========Function Declaration======================


    def delete_photos_by_entry(self):
        # Ask for confirmation before proceeding
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete photos for this Student ID?", parent=self.root)
        if not confirmation:
            return

        # Get the Student ID from the Entry widget
        student_id = StudentID_entry.get()

        # Check if the Student ID is provided
        if student_id:
            # Construct the directory path where images are stored
            images_directory = 'data'
            # Check if the images directory exists
            if os.path.exists(images_directory):
                deleted_count = 0  # Counter to track the number of deleted photos
                # Iterate over files in the images directory
                for filename in os.listdir(images_directory):
                    # Check if the filename contains the student_id
                    if student_id in filename:
                        # Construct the full path of the file
                        file_path = os.path.join(images_directory, filename)
                        try:
                            # Delete the file
                            os.remove(file_path)
                            deleted_count += 1
                        except Exception as e:
                            # Show error message if failed to delete the file
                            messagebox.showerror("Error", f"Failed to delete {file_path}: {e}", parent=self.root)
                # Show success message if any photos were deleted
                if deleted_count > 0:
                    messagebox.showinfo("Success", f"{deleted_count} photos deleted successfully for Student ID: {student_id}", parent=self.root)
                else:
                    messagebox.showerror("Error", f"No photos found for Student ID: {student_id}", parent=self.root)
            else:
                # Show an error message if the images directory does not exist
                messagebox.showerror("Error", "Images directory does not exist.", parent=self.root)
        else:
            # Show a message if no Student ID is provided
            messagebox.showerror("Error", "Please enter a Student ID.", parent=self.root)


    def search_data(self):
        # Get the selected search option and input value
        search_option = search_combo.get()
        search_value = search_entry.get()

        if search_option == "Select" or search_value == "":
            messagebox.showerror("Error", "Please select a search option and enter a value.", parent=self.root)
        else:
            try:
                # Open the CSV file in read mode
                with open("student_details.csv", "r") as file:
                    reader = csv.reader(file)
                    data = list(reader)

                # Perform search based on the selected option
                search_results = []
                for row in data:
                    if search_option == "Full Name" and search_value.lower() in row[5].lower():
                        search_results.append(row)
                    elif search_option == "Student ID" and search_value == row[4]:
                        search_results.append(row)

                if len(search_results) != 0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in search_results:
                        self.student_table.insert("", END, values=i)
                else:
                    messagebox.showerror("Error", "No matching records found.", parent=self.root)

            except Exception as e:
                messagebox.showerror("Error", f"Error occurred: {str(e)}", parent=self.root)


    def add_data(self):
        if (self.var_dep.get() == "Select Department" or
            self.var_name.get() == "" or
            self.var_id.get() == "" or
            self.var_course.get() == "Select Course" or
            self.var_email.get() == "" or
            self.var_phone.get() == "" or
            self.var_year.get() == "Select Academic Year" or
            self.var_gender.get() == "Select Gender" or
            self.var_index.get() == "" or
            self.var_radio1.get() == "" or
            self.var_semester.get() == "Select Semester"):

            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                student_id = self.var_id.get()
                phone = self.var_phone.get()
                full_name = self.var_name.get()
                email = self.var_email.get()
                index = self.var_index.get()

                # Open the CSV file in read mode to check for existing entries
                with open("student_details.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if (row[4] == student_id or row[8] == phone or
                            row[5].lower() == full_name.lower() or
                            row[7].lower() == email.lower() or
                            row[10].lower() == index.lower()):
                            messagebox.showerror("Error", "Student already exists.", parent=self.root)
                            return

                # Open the CSV file in append mode
                with open("student_details.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    # Write student details to the CSV file
                    writer.writerow([
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_id.get(),
                        self.var_name.get(),
                        self.var_gender.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_radio1.get(),
                        self.var_index.get()
                    ])
                
                messagebox.showinfo("Success", "Student details have been added Successfully", parent=self.root)
                # Refresh the data in the table view
                self.fetch_data()
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)






    def fetch_data(self):
        try:
            # Open the CSV file and read its contents
            with open("student_details.csv", "r") as file:
                reader = csv.reader(file)
                data = list(reader)

                if len(data) != 0:
                    # Clear existing data in the table
                    self.student_table.delete(*self.student_table.get_children())
                    # Insert data from the CSV into the table
                    for i in data:
                        self.student_table.insert("", END, values=i)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading data: {str(e)}", parent=self.root)

    def get_cursor(self, event=""):
        try:
            # Get the selected row in the table
            cursor_focus = self.student_table.focus()
            content = self.student_table.item(cursor_focus)
            data = content["values"]

            # Populate entry fields with the selected row's data
            if data:
                self.var_dep.set(data[0])
                self.var_course.set(data[1])
                self.var_year.set(data[2])
                self.var_semester.set(data[3])
                self.var_id.set(data[4])
                self.var_name.set(data[5])
                self.var_gender.set(data[6])
                self.var_email.set(data[7])
                self.var_phone.set(data[8])
                self.var_radio1.set(data[9])
                self.var_index.set(data[10])
            else:
                messagebox.showerror("Error", "No Data in the Selected row.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving data: {str(e)}", parent=self.root)


    def update_data(self):
        if (self.var_dep.get() == "Select Department" or
            self.var_name.get() == "" or
            self.var_id.get() == "" or
            self.var_course.get() == "Select Course" or
            self.var_email.get() == "" or
            self.var_phone.get() == "" or
            self.var_year.get() == "Select Academic Year" or
            self.var_gender.get() == "Select Gender" or
            self.var_index.get() == "" or
            self.var_radio1.get() == "" or
            self.var_semester.get() == "Select Semester"):       
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                # Open the CSV file in read mode
                with open("student_details.csv", "r") as file:
                    reader = csv.reader(file)
                    data = list(reader)

                # Find and update the student record in the CSV data
                updated_data = []
                updated = False
                for row in data:
                    if row[4] == self.var_id.get():
                        row = [
                            self.var_dep.get(),
                            self.var_course.get(),
                            self.var_year.get(),
                            self.var_semester.get(),
                            self.var_id.get(),
                            self.var_name.get(),
                            self.var_gender.get(),
                            self.var_email.get(),
                            self.var_phone.get(),
                            self.var_radio1.get(),
                            self.var_index.get()
                        ]
                        updated = True
                    updated_data.append(row)

                # Write the updated data back to the CSV file
                with open("student_details.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_data)

                if updated:
                    messagebox.showinfo("Success", "Student details Successfully updated", parent=self.root)
                    self.fetch_data()
                else:
                    messagebox.showerror("Error", "Student ID cannot be updated, Please delete the student and register again", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    # Delete function

    def clear_widgets(self):
        # Clear all necessary widgets here
        self.var_id.set(""),
        self.var_dep.set("Select Department"),
        self.var_course.set("Select Course"),
        self.var_year.set("Select Academic Year"),
        self.var_semester.set("Select Semester"),
        self.var_name.set(""),
        self.var_gender.set("Select Gender"),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_radio1.set(""),
        self.var_index.set("")

    def delete_data(self):
        if (self.var_dep.get() == "Select Department" or
            self.var_name.get() == "" or
            self.var_id.get() == "" or
            self.var_course.get() == "Select Course" or
            self.var_email.get() == "" or
            self.var_phone.get() == "" or
            self.var_year.get() == "Select Academic Year" or
            self.var_gender.get() == "Select Gender" or
            self.var_radio1.get() == "" or
            self.var_index.get() == "" or
            self.var_semester.get() == "Select Semester"):       
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                # Ask user for confirmation
                confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?", parent=self.root)
                if not confirm:
                    return

                # Open the CSV file in read mode
                with open("student_details.csv", "r") as file:
                    reader = csv.reader(file)
                    data = list(reader)

                # Find and delete the student record from the CSV data
                deleted = False
                updated_data = []
                for row in data:
                    if row[4] != self.var_id.get():
                        updated_data.append(row)
                    else:
                        deleted = True

                # Write the updated data back to the CSV file
                with open("student_details.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_data)

                if deleted:
                    messagebox.showinfo("Success", "Student details Successfully deleted", parent=self.root)
                    # Clear all widgets
                    self.clear_widgets()
                    # Update the display widget
                    self.fetch_data()
                else:
                    messagebox.showerror("Error", "Student not found", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)






    # =======reset=========
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Academic year")
        self.var_semester.set("Select Semester")
        self.var_id.set("")
        self.var_name.set("")
        self.var_gender.set("Select Gender")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_radio1.set("")
        self.var_index.set("")


    #========Generate data set Take Photo Sample ===============

    def update_photo_samples(self):
        output_dir = "data"
        if (self.var_dep.get() == "Select Department" or 
            self.var_name.get() == "" or 
            self.var_id == "" or 
            self.var_course == "Select Course" or 
            self.var_email == "" or 
            self.var_phone == "" or 
            self.var_year == "Select Academic Year" or 
            self.var_gender == "Select Gender" or 
            self.var_index == "" or 
            self.var_semester == "Select Semester"):
            messagebox.showerror("Error", "All Fields are required", parent=self.root)

        elif self.var_radio1.get() == "" or self.var_radio1.get() == "No":
            messagebox.showerror("Error", "Take Photo Sample must be marked 'Yes'", parent=self.root)
            
        else:
            if not any(fname.startswith(self.var_id.get()) for fname in os.listdir(output_dir)):
                messagebox.showerror("Error", "The student photos does not exist. Please use 'Take Photo Sample' to register the photos..", parent=self.root)
            else:
                try:
                    # Create the output directory if it doesn't exist
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    # Load the cascade classifier for face detection
                    cascade_path = "haarcascade_frontalface_default.xml"
                    if not os.path.exists(cascade_path):
                        messagebox.showerror("Error", "Haarcascade XML file not found in the directory.", parent=self.root)
                        return
                    face_cascade = cv2.CascadeClassifier(cascade_path)
                    
                    # Open the webcam
                    cap = cv2.VideoCapture(0) 
                    
                    # Initialize sample counter
                    sample_count = 0

                    # Inform the user about the process
                    messagebox.showinfo("Capture Process", "Please wait while capturing 200 images ...", parent=self.root)
                    
                    # Create a window for displaying webcam feed
                    cv2.namedWindow('Webcam')
                    
                    while True:
                        # Read a frame from the webcam
                        ret, frame = cap.read()
                        
                        # Display the frame
                        cv2.imshow('Webcam', frame)
                        
                        # Convert the frame to grayscale
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        
                        # Detect faces in the frame
                        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                        
                        # Iterate over detected faces
                        for (x, y, w, h) in faces:
                            # Crop the face from the frame
                            face = frame[y:y+h, x:x+w]
                            
                            # Resize the face to a fixed size
                            face = cv2.resize(face, (100, 100))
                            
                            # Generate a unique filename based on timestamp
                            name = self.var_id.get()
                            file_path = os.path.join(output_dir, f"{name}_{sample_count}.jpg")
                            
                            # Save the cropped face to the output directory
                            cv2.imwrite(file_path, face)
                            
                            # Increment the sample counter
                            sample_count += 1
                            
                            # Break out of the loop if the desired number of samples is reached
                            if sample_count == 200:
                                break
                        
                        # Break out of the loop if the desired number of samples is reached
                        if sample_count == 200:
                            break
                        
                        # Break out of the loop if 'q' is pressed
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    
                    # Release the webcam and close all OpenCV windows
                    cap.release()
                    cv2.destroyAllWindows()

                    messagebox.showinfo("Success", f"{sample_count} images captured Successfully and saved to 'data' directory.",parent=self.root)

                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}", parent=self.root)


  

    def generate_dataset(self):
        output_dir = "data"
        
        # Check if all required fields are filled
        if (self.var_dep.get() == "Select Department" or 
            self.var_name.get() == "" or 
            self.var_id.get() == "" or 
            self.var_course.get() == "Select Course" or 
            self.var_email.get() == "" or 
            self.var_phone.get() == "" or 
            self.var_year.get() == "Select Academic Year" or 
            self.var_gender.get() == "Select Gender" or 
            self.var_index.get() == "" or 
            self.var_semester.get() == "Select Semester"):
            
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return
        
        # Check if the 'Take Photo Sample' option is selected
        elif self.var_radio1.get() == "" or self.var_radio1.get() == "No":
            messagebox.showerror("Error", "Take Photo Sample must be marked", parent=self.root)
            return
        
        try:
            # Create the output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Check if any images with the student ID already exist
            student_id = self.var_id.get()
            if any(fname.startswith(student_id) for fname in os.listdir(output_dir)):
                messagebox.showerror("Error", "The student photos already exist. Please use 'Update Photo Sample' to overwrite the photos..", parent=self.root)
                return
            
            # Load the cascade classifier for face detection
            cascade_path = "haarcascade_frontalface_default.xml"
            if not os.path.exists(cascade_path):
                messagebox.showerror("Error", "Haarcascade XML file not found in the directory.", parent=self.root)
                return
            face_cascade = cv2.CascadeClassifier(cascade_path)
            
            # Open the webcam
            cap = cv2.VideoCapture(0) 
            
            # Initialize sample counter
            sample_count = 0
            
            # Inform the user about the process
            messagebox.showinfo("Capture Process", "Please wait while capturing 200 images...", parent=self.root)
            
            # Create a window for displaying webcam feed
            cv2.namedWindow('Webcam')
            
            while True:
                # Read a frame from the webcam
                ret, frame = cap.read()
                
                # Display the frame
                cv2.imshow('Webcam', frame)
                
                # Convert the frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces in the frame
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                # Iterate over detected faces
                for (x, y, w, h) in faces:
                    # Crop the face from the frame
                    face = frame[y:y+h, x:x+w]
                    
                    # Resize the face to a fixed size
                    face = cv2.resize(face, (100, 100))
                    
                    # Generate a unique filename based on timestamp
                    file_path = os.path.join(output_dir, f"{student_id}_{sample_count}.jpg")
                    
                    # Save the cropped face to the output directory
                    cv2.imwrite(file_path, face)
                    
                    # Increment the sample counter
                    sample_count += 1
                    
                    # Break out of the loop if the desired number of samples is reached
                    if sample_count == 200:
                        break
                
                # Break out of the loop if the desired number of samples is reached
                if sample_count == 200:
                    break
                
                # Break out of the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Release the webcam and close all OpenCV windows
            cap.release()
            cv2.destroyAllWindows()
            
            messagebox.showinfo("Success", f"{sample_count} images captured Successfully and saved to 'data' directory.", parent=self.root)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}", parent=self.root)



            


if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()