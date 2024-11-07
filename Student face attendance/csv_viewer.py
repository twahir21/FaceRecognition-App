import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import csv
import os
from datetime import datetime

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        root.title("Attendance Tracker")
        root.resizable(False, False)

        # Title label
        self.title_label = ttk.Label(root, text="Attendance Tracker", font=("Comic Sans MS", 25, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(10, 20))

        # Left Frame for displaying selected data and input for filtering
        self.left_frame = ttk.Frame(root, padding="20")
        self.left_frame.grid(row=1, column=0)

        self.selected_data_label = ttk.Label(self.left_frame, text="Selected Data:", font=("Comic Sans MS", 15, "bold"))
        self.selected_data_label.grid(row=0, column=0, columnspan=2, sticky="w")

        labels = ["Name", "Academic Year", "Course", "Time", "Appearance", "Current Time"]
        self.data_inputs = []
        for i, label in enumerate(labels):
            label = ttk.Label(self.left_frame, text=f"{label}:", font=("Comic Sans MS", 13))
            label.grid(row=i+1, column=0, sticky="w")
            entry = ttk.Entry(self.left_frame, width=20, font=("Comic Sans MS", 13), state="readonly")
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            self.data_inputs.append(entry)

        # Add label and input widget for filtering
        filter_label = ttk.Label(self.left_frame, text="Enter Name:", font=("Comic Sans MS", 13))
        filter_label.grid(row=len(labels) + 1, column=0, sticky="w")

        self.filter_entry = ttk.Entry(self.left_frame, width=20, font=("Comic Sans MS", 13))
        self.filter_entry.grid(row=len(labels) + 1, column=1, padx=5, pady=5)

        # Filter data button
        filter_button = ttk.Button(self.left_frame, text="Filter by Name", command=self.filter_data, style="Custom.TButton", cursor="hand2")
        filter_button.grid(row=len(labels) + 2, column=0, columnspan=2, pady=10)

        # Show All button
        show_all_button = ttk.Button(self.left_frame, text="Show All", command=self.show_all_data, style="Custom.TButton", cursor="hand2")
        show_all_button.grid(row=len(labels) + 3, column=0, columnspan=2, pady=10)

        # Right Frame for displaying CSV data
        self.right_frame = ttk.Frame(root, padding="20")
        self.right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Right widget with column titles
        self.setup_right_widget()

        # Load CSV data
        self.load_csv_data("recognized_students.csv")  # Replace "recognized_students.csv" with your CSV file path

        # Bind TreeviewSelect event
        self.csv_tree.bind("<<TreeviewSelect>>", self.populate_input_fields)

        # Buttons for additional functionalities
        self.add_buttons()

        # Display current time
        self.display_current_time()

    # Rest of the class methods remain the same

    def setup_right_widget(self):
        # Treeview widget for displaying CSV data with column titles
        self.csv_tree = ttk.Treeview(self.right_frame, columns=["Name", "Academic Year", "Course", "Time"], show="headings")
        self.csv_tree.grid(row=0, column=0, sticky="nsew")

        # Add column headings
        for col in ["Name", "Academic Year", "Course", "Time"]:
            self.csv_tree.heading(col, text=col)

        # Vertical Scrollbar
        scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.csv_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.csv_tree.configure(yscrollcommand=scrollbar.set)

        # Ensure the scrollbar is always visible
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
    
    def show_all_data(self):
        self.filter_entry.delete(0, tk.END)  # Clear the filter entry
        self.clear_treeview_data()  # Clear the current data in the Treeview
        self.show_csv_data()  # Show all data from the CSV file

    def load_csv_data(self, file_path):
        try:
            df = pd.read_csv(file_path)
            self.csv_data = df
            self.show_csv_data()
        except Exception as e:
            print("Error:", e)

    def show_csv_data(self):
        # Add data rows
        for index, row in self.csv_data.iterrows():
            self.csv_tree.insert("", "end", values=list(row))

    def populate_input_fields(self, event):
        selected_items = self.csv_tree.selection()
        if selected_items:  # Check if selection is not empty
            selected_item = selected_items[0]
            values = self.csv_tree.item(selected_item, "values")
            for entry, value in zip(self.data_inputs[:-1], values):  # Exclude the "Current Time" input
                entry.config(state="normal")  # Enable the entry widget for updating
                entry.delete(0, tk.END)
                entry.insert(0, value)
                entry.config(state="readonly")  # Set the entry widget back to read-only

            # Count appearances of the name and populate the "Appearance" input field
            name = values[0]  # Assuming the name is in the first column
            appearance_count = self.csv_data.iloc[:, 0].tolist().count(name)
            self.data_inputs[-2].config(state="normal")  # Enable the entry widget for updating
            self.data_inputs[-2].delete(0, tk.END)
            self.data_inputs[-2].insert(0, appearance_count)
            self.data_inputs[-2].config(state="readonly")  # Set the entry widget back to read-only

    def add_buttons(self):
        # Clear CSV data button
        clear_button = ttk.Button(self.right_frame, text="Clear All Data", command=self.clear_csv_data, style="Custom.TButton", cursor="hand2")
        clear_button.grid(row=1, column=0, pady=10)

        # Print button
        print_button = ttk.Button(self.right_frame, text="Print All Data", command=self.print_all_data, style="Custom.TButton", cursor="hand2")
        print_button.grid(row=2, column=0, pady=10)

        # Create a custom style for buttons
        style = ttk.Style()
        style.configure("Custom.TButton", foreground="black", background="#ff9900", font=("Arial", 15))

    def clear_treeview_data(self):
        # Clear all rows in the Treeview
        for child in self.csv_tree.get_children():
            self.csv_tree.delete(child)
    
    def clear_csv_data(self):
        # Display a confirmation messagebox
        confirm = messagebox.askokcancel("Confirmation", "Are you sure you want to clear all data?", parent=self.root)

        if confirm:
            # Clear all rows of the CSV file and overwrite the file
            try:
                with open("recognized_students.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(self.csv_data.columns)  # Write column names
            except Exception as e:
                print("Error:", e)

            # Clear all rows in the Treeview
            self.clear_treeview_data()

            # Set input fields editable
            for entry in self.data_inputs:
                entry.config(state="normal")

            # Clear all input fields except the "Current Time" input
            for entry in self.data_inputs[:-1]:  # Exclude the "Current Time" input
                entry.delete(0, tk.END)
                entry.insert(0, "")

            # Set input fields back to read-only
            for entry in self.data_inputs:
                entry.config(state="readonly")

            # Clear the filter entry
            self.filter_entry.delete(0, tk.END)

    def filter_data(self):
        # Filter data based on user input
        filter_text = self.filter_entry.get().strip()
        if filter_text:
            filtered_rows = self.csv_data[self.csv_data["Name"].str.contains(filter_text, case=False)]
            self.clear_treeview_data()  # Clear the current data in the Treeview
            self.show_filtered_data(filtered_rows)  # Show the filtered data
        else:
            # If no filter text provided, show all data
            self.clear_treeview_data()  # Clear the current data in the Treeview
            self.show_csv_data()  # Show all data from the CSV file

    def show_filtered_data(self, data):
        # Add filtered data rows
        for index, row in data.iterrows():
            self.csv_tree.insert("", "end", values=list(row))

    def display_current_time(self):
        # Display the current time in the "Current Time" input field
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.data_inputs[-1].config(state="normal")  # Enable the entry widget for updating
        self.data_inputs[-1].delete(0, tk.END)
        self.data_inputs[-1].insert(0, current_time)
        self.data_inputs[-1].config(state="readonly")  # Set the entry widget back to read-only

        # Schedule the next update after 1000 milliseconds (1 second)
        self.root.after(1000, self.display_current_time)

    def print_all_data(self):
        try:
            # Export the data to a temporary text file
            with open("print_data.txt", "w") as file:
                writer = csv.writer(file)
                writer.writerow(self.csv_data.columns)  # Write the header
                writer.writerows(self.csv_data.values)  # Write the data rows

            # Print the file (this will work on Windows; for other systems, the print command might differ)
            if os.name == "nt":
                os.startfile("print_data.txt", "print")
            else:
                print_command = f"lp print_data.txt"
                os.system(print_command)

            messagebox.showinfo("Success", "Data sent to the printer successfully.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print data. Error: {e}", parent=self.root)

def main():
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
