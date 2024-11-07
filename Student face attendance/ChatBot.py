import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import os
import sys
import random

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        root.title("Chatbot GUI")
        root.resizable(False, False)

        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS2
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        # Calculate the center coordinates
        window_width = 730
        window_height = 650
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set the window size and position
        root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        image = Image.open(resource_path("images\\chatbot.png")).resize((600,150))
        self.photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(root, image=self.photo, width=700, height=150)
        self.image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=65, height=13, font=("Comic Sans MS", 12))
        self.chat_history.tag_config("user", foreground="blue", font=("Comic Sans MS", 13))
        self.chat_history.tag_config("bot", foreground="red", font=("Comic Sans MS", 13))
        self.chat_history.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        self.chat_history.config(state=tk.DISABLED)

        input_box_label = tk.Label(root, text="Type Something here:", font=("Comic Sans MS", 15, "bold"), fg="green")
        input_box_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.input_box = tk.Text(root, wrap=tk.WORD, width=30, height=2, font=("Comic Sans MS", 14))
        self.input_box.grid(row=2, column=1, padx=10, pady=10)
        self.input_box.bind("<KeyRelease>", self.enable_send_button)

        self.send_button = tk.Button(root, text="Send", command=self.send_message, font=("Comic Sans MS", 15), bg="blue", fg="white", cursor="hand2", state=tk.DISABLED)
        self.send_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        self.clear_button = tk.Button(root, text="Clear Chat", command=self.clear_chat, font=("Comic Sans MS", 15), bg="red", fg="white", cursor="hand2")
        self.clear_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Dictionary of question-answer pairs
        self.qa_pairs = {
            "Hi | hello | hey | morning | afternoon | evening | night | Assalam alaykum": ["Hello There!, I am ChatBot assistance and not AI, what can I assist you about this Program?", "Hey! Simply I am assistance chatBot, likely not AI, It is my pleasure to assist you about this app, keep asking", "Am here, I hope you are good, am a user-friend ChatBot assistance for you but absolutely not AI, Feel free ask anything about this Program"],
            "what is your name":  ["My name is Twahir Chatbot Assistance, am not AI. How can I assist you Today about this Program?", "You can call me Twahir assistance Chatbot, specifically not AI, keep on asking questions about this app so that I can assist"],
            "who created you":  ["Twahir is the mastermind behind bringing me to life.","Twahir, the brilliant mind behind my creation", "I was created by Twahir, a talented developer.", "I was created by an amazing Python programmer, named Twahir.", "The genius behind my existence is none other than Twahir.", "My creation stems from the innovative work of Twahir."],
            "What this program can do": ["Attendance Tracking: It can track the attendance of individuals by analyzing their faces recognized in real-time.", "Attendance Recording: The system can record attendance data, including timestamps and the identities of individuals present.", "Automated Processes: It can automate attendance management processes, reducing the need for manual tracking and recording."],
            "who are you":  ["I am a friendly chatbot but not AI, I am designed for this interface.", "As help desk Secretary, I am a simplified user-friendly ChatBot assistance for this app", "I am automated assistance ChatBot, support users in this face Recognitiion System"],
            "what can you do":  ["I can answer your questions about this app only, but to be honest am not AI.", "I can assist users by providing guidelines on how to use and handle this program."],
            "how to avoid errors": ["Student ID should not exceed more than 10 digits", "Ensure Proper lightning condition: Avoid over bright or dim enviromnents","Proper positioning of face infront of a camera", "Make sure you update your photos regularly"], 
            "Thanks": ["You're warmly welcomed! Let me know if there's anything else I can assist you with.", "No problem at all! If you have any more questions or need further assistance, feel free to ask.","Glad I could help! Don't hesitate to reach out if you need assistance with anything else related to the attendance system.", "Anytime! If there's anything else you need or if you have more questions, just let me know."],
            "what is machine learning": ["Machine learning is a subset of artificial intelligence that focuses on enabling machines to learn from data and improve performance on a specific task without being explicitly programmed. It involves algorithms that allow computers to automatically learn and make predictions or decisions based on data.", "It's a field of study that focuses on developing algorithms and models that allow computers to learn patterns and make predictions or decisions based on data.", "It involves training models on labeled data to recognize patterns or infer relationships, which can then be applied to new, unseen data for various applications like image recognition, natural language processing, and recommendation systems."],
            "how many countries use this program":["Many countries around the world use face recognition technology for various purposes, including security, law enforcement, and identity verification. The exact number of countries using this technology may not be readily available.", "As of the latest update, the program has been adopted by organizations in more than 30 countries", "The face attendance system has gained traction across multiple continents, with users spanning over 40 countries."],
            "what is python programmming": ["Python is a high-level programming language known for its simplicity and readability. It is widely used for various purposes, including web development, data analysis, artificial intelligence, and automation.", "Is a versatile language used for various applications, including web development, data analysis, and automation.", "A popular choice for implementing machine learning algorithms and artificial intelligence applications due to its extensive libraries and frameworks."],
            "can you change your name": ["No, as an Assistance ChatBot developed by Twahir, I can't change my name.", "As the chatbot for Twahir's face attendance system, I'm unable to change my name."],
            "how long did this program created": ["It took about two months to complete the whole Project", "It is estimated to be two months simultaneously to complete full designing and coding"],
            "how to use this program": ["You should register yourself in Student Details then you must take a photoSample pictures and train them, thereafter you can view your images in Photos and you can make attendance by face Recognition and view it in Attendance"],
            "what is function of train data": ["Training data is used to train machine learning models. It consists of input-output pairs that the model learns from. The model adjusts its parameters based on the training data to minimize the difference between its predictions and the actual outputs."],
            "what are the requirements of making a program like this?":["Find resources concern about face Recognition System and learn how it works, thereafter implement your knowledge in codes, in this case my expert used Python language"],
            "how to create a program like this?":["Creating a program like this, it involves a series of processes and software development skills, you may contact Twahir for more Details"],
            "how many people can be handled": ["This program can hold about thousands of people, only if the storage is sufficient"],
            "how many people use this program": ["This program can hold about thousands of people, only if the storage is sufficient"],
            "why we take many pictures": ["Taking many pictures helps improve the accuracy and robustness of face recognition systems. It provides a diverse set of facial images that can capture different poses, expressions, lighting conditions, and angles, making the system more reliable in various real-world scenarios."],
            "how to this program works": ["The data you inserted in Student Details are saved in a Programmer's Database and pictures are also saved. When pictures are Trained they will be able to be recognized and when recognized, data are fetched and attendance list is created"],
            "can you solve for errors": ["No, you may contact Twahir in Developer option to handle your problem", "Sorry for that, I cannot do anything to help you, Please contact Twahir in developer details for help"],
            "why it fails to recognize my face": ["This Face recognition System may fail to recognize faces due to various reasons such as poor lighting conditions, occlusions (e.g., wearing glasses or hats), changes in facial appearance (e.g., aging, hairstyle), or limitations of the recognition algorithm itself. You may try to capture and train current images of you"],
            "why can not capture my data ": ["The possible reason maybe failure of data fetch. You can contact a Programmer for help", "Student ID may exceed 10 digits, so your data in face recognition will be set to unkown"],
            "how to to register": ["You should register yourself in Student Details then you must take a photoSample pictures and train them, thereafter you can view your images in Photos and you can make attendance by face Recognition and view it in Attendance"],
            "How many question can you answer":["I can answer about 20 different questions asked in different ways but my overall training is still low. Keep on asking questions about this program", "I have 20 questions in my memory but I can respond with different answers, my expert give me such capability"],
            "what is the advantage of using this program": ["This Program reduces costs of buying fingerPrint sensors or any tool for easy Attendance tracking", "Time-saving: It streamlines the attendance process, eliminating the need for manual entry or verification, thereby saving time for both employees and administrators."],
        }


    def tokenize_set(self, text):
        return set(text.lower().split())

    def calculate_accuracy(self, question_set, pattern_set):
        common_words = question_set.intersection(pattern_set)
        accuracy = len(common_words) / len(pattern_set) if len(pattern_set) > 0 else 0
        return accuracy

    def chatbot_response(self, question):
        question_set = self.tokenize_set(question)

        best_match = None
        best_accuracy = 0

        for q_pattern, answers in self.qa_pairs.items():
            pattern_set = self.tokenize_set(q_pattern)
            accuracy = self.calculate_accuracy(question_set, pattern_set)

            if accuracy > best_accuracy:
                best_match = random.choice(answers)
                best_accuracy = accuracy

        if best_match:
            return best_match
        else:
            return "I'm sorry, I don't understand that question."

    def send_message(self):
        user_input = self.input_box.get("1.0", "end").strip()
        
        if not user_input:
            response = "Please input a question so that I can answer you."
        elif user_input.lower() in ['bye', 'exit', 'quit', 'quit', 'goodbye']:
            response = "Goodbye! Thank you for using me."
            messagebox.showinfo("Chatbot", response)
            self.root.quit()
        else:
            response = self.chatbot_response(user_input)

        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "You: " + user_input + "\n", "user")
        self.chat_history.insert(tk.END, "Chatbot: " + response + "\n", "bot")
        self.chat_history.config(state=tk.DISABLED)
        self.input_box.delete("1.0", "end")
        self.send_button.config(state=tk.DISABLED)  # Disable send button after sending the message

    def enable_send_button(self, event=None):
        user_input = self.input_box.get("1.0", "end").strip()
        if user_input:
            self.send_button.config(state=tk.NORMAL)
        else:
            self.send_button.config(state=tk.DISABLED)

    def clear_chat(self):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
