import tkinter as tk
from tkinter import scrolledtext
import json
import re

# Load rules from rules.json
with open("rules.json", "r") as file:
    rules = json.load(file)

# Match input with rule patterns
def get_response(user_input):
    for rule in rules:
        if re.search(rule["pattern"], user_input, re.IGNORECASE):
            return rule["response"]
    return "I'm not sure I understand. Can you rephrase that?"

# Send message logic
def send_message():
    user_msg = user_input.get()
    if user_msg.strip() == "":
        return
    chat_area.insert(tk.END, "You: " + user_msg + "\n")
    user_input.delete(0, tk.END)
    response = get_response(user_msg)
    chat_area.insert(tk.END, "Bot: " + response + "\n\n")

# Create GUI
window = tk.Tk()
window.title("Rule-Based Chatbot 🤖")
window.geometry("500x600")
window.config(bg="lightblue")

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_input = tk.Entry(window, font=("Arial", 12))
user_input.pack(padx=10, pady=5, fill=tk.X)
user_input.focus()

send_btn = tk.Button(window, text="Send", font=("Arial", 12), bg="white", command=send_message)
send_btn.pack(pady=5)

window.bind('<Return>', lambda event: send_message())

window.mainloop()