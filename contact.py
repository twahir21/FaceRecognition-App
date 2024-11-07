import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender")
        self.root.iconbitmap('icon.ico')
        self.root.geometry("620x500")
        self.root.resizable(False, False)

        # Set style
        style = ttk.Style()
        style.configure("TLabel", font=('Helvetica', 14))
        style.configure("TButton", font=('Helvetica', 14, 'bold'), background="#4CAF50", foreground="black")
        style.map("TButton", background=[('active', '#45a049')])

        # Frame for the input fields
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Load environment variables from .env file
        load_dotenv()

        # Use the variables
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.password = os.getenv("EMAIL_PASSWORD")

        ttk.Label(frame, text="Sender Email:").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.sender_entry = tk.Entry(frame, font=('Helvetica', 15), width=30)
        self.sender_entry.grid(row=0, column=1, pady=10)

        ttk.Label(frame, text="Subject:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.subject_entry = tk.Entry(frame, font=('Helvetica', 15), width=30)
        self.subject_entry.grid(row=1, column=1, pady=10)

        ttk.Label(frame, text="Email Body:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.body_text = tk.Text(frame, height=10, width=43, font=('Helvetica', 14))
        self.body_text.grid(row=2, column=1, pady=10)

        # Frame for the button
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.send_button = ttk.Button(button_frame, text="Send Email", command=self.send_email)
        self.send_button.pack()

    def send_email(self):
        sender_email = self.sender_entry.get()
        user_subject = self.subject_entry.get()
        body = self.body_text.get("1.0", tk.END).strip()

        if not sender_email or not user_subject or not body:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        # Fixed subject line
        fixed_subject = "My Face Attendance System"
        # Email body including sender email and user subject
        email_body = f"Sender Email: {sender_email}\nUser Subject: {user_subject}\n\n{body}"

        try:
            # Set up the MIME
            msg = MIMEMultipart()
            msg['From'] = sender_email  # Sender email input
            msg['To'] = self.receiver_email
            msg['Subject'] = fixed_subject  # Fixed subject
            msg.attach(MIMEText(email_body, 'plain'))

            # Connect to the server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            
            # Log in to the server with the receiver's credentials
            server.login(self.receiver_email, self.password)
            
            # Send the email
            text = msg.as_string()
            server.sendmail(self.receiver_email, self.receiver_email, text)
            server.quit()

            messagebox.showinfo("Success", "Email sent successfully!")
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Authentication Error", "Failed to authenticate with the email server. Check email and password.")
        except smtplib.SMTPConnectError:
            messagebox.showerror("Connection Error", "Failed to connect to the email server. Check your internet connection.")
        except smtplib.SMTPException as e:
            messagebox.showerror("SMTP Error", f"SMTP error occurred: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()
