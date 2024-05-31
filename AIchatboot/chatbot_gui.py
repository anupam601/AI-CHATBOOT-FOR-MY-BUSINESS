from tkinter import *
from tkinter import ttk, messagebox
import json
import os
import testing as testpy
import training as trainpy

BG_GRAY = "#ABB2B9"
BG_COLOR = "#000"
TEXT_COLOR = "#FFF"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatBot:
    def __init__(self):
        self.window = Tk()
        self.main_window()
        self.test = testpy.Testing()

    def run(self):
        self.window.mainloop()

    def main_window(self):
        self.window.title("ChatBot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=520, height=520, bg=BG_COLOR)
        self.tab = ttk.Notebook(self.window)
        self.tab.pack(expand=1, fill='both')
        self.bot_frame = ttk.Frame(self.tab, width=520, height=520)
        self.train_frame = ttk.Frame(self.tab, width=520, height=520)
        self.tab.add(self.bot_frame, text='Anupam Bot'.center(100))
        self.tab.add(self.train_frame, text='Train Bot'.center(100))
        self.add_bot()
        self.add_train()

    def add_bot(self):
        head_label = Label(self.bot_frame, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome to Anupam Automobiles", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        line = Label(self.bot_frame, width=450, bg=BG_COLOR)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # Changing the message box colors to blue and orange
        self.text_widget = Text(self.bot_frame, width=20, height=2, bg="#E3F2FD", fg="#1E88E5", font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        bottom_label = Label(self.bot_frame, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # Changing the entry box colors to orange
        self.msg_entry = Entry(bottom_label, bg="#FFCCBC", fg="#E64A19", font=FONT)
        self.msg_entry.place(relwidth=0.788, relheight=0.06, rely=0.008)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.on_enter)
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=8, bg="Green", command=lambda: self.on_enter(None))
        send_button.place(relx=0.80, rely=0.008, relheight=0.06, relwidth=0.20)

    def add_train(self):
        head_label = Label(self.train_frame, bg=BG_COLOR, fg=TEXT_COLOR, text="Train Bot", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        taglabel = Label(self.train_frame, fg="#000", text="Tag", font=FONT)
        taglabel.place(relwidth=0.2, relx=0.008)
        self.tag = Entry(self.train_frame, bg="#fff", fg="#000", font=FONT)
        self.tag.place(relwidth=0.7, relheight=0.06, rely=0.14, relx=0.22)
        self.pattern = []
        for i in range(2):
            patternlabel = Label(self.train_frame, fg="#000", text="Pattern%d" % (i + 1), font=FONT)
            patternlabel.place(relwidth=0.2, relheight=0.06, rely=0.28 + 0.08 * i, relx=0.008)
            self.pattern.append(Entry(self.train_frame, bg="#fff", fg="#000", font=FONT))
            self.pattern[i].place(relwidth=0.7, relheight=0.06, rely=0.28 + 0.08 * i, relx=0.22)
        self.response = []
        for i in range(2):
            responselabel = Label(self.train_frame, fg="#000", text="Response%d" % (i + 1), font=FONT)
            responselabel.place(relwidth=0.2, relheight=0.06, rely=0.50 + 0.08 * i, relx=0.008)
            self.response.append(Entry(self.train_frame, bg="#fff", fg="#000", font=FONT))
            self.response[i].place(relwidth=0.7, relheight=0.06, rely=0.50 + 0.08 * i, relx=0.22)
        bottom_label = Label(self.train_frame, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        train_button = Button(bottom_label, text="Train Bot", font=FONT_BOLD, width=12, bg="Green", command=self.on_train)
        train_button.place(relx=0.20, rely=0.008, relheight=0.06, relwidth=0.60)

    def on_train(self):
        if not self.tag.get() or not any(pattern.get() for pattern in self.pattern) or not any(response.get() for response in self.response):
            messagebox.showerror("Input Error", "All fields must be filled out to train the bot.")
            return
        try:
            with open('intents.json', 'r+') as json_file:
                file_data = json.load(json_file)
                file_data['intents'].append({
                    "tag": self.tag.get(),
                    "patterns": [i.get() for i in self.pattern],
                    "responses": [i.get() for i in self.response],
                    "context": ""
                })
                json_file.seek(0)
                json.dump(file_data, json_file, indent=1)
            train = trainpy.Training()
            train.build()
            messagebox.showinfo("Training", "Trained Successfully")
            self.test = testpy.Testing()
        except FileNotFoundError:
            messagebox.showerror("File Error", "intents.json file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("JSON Error", "Error reading intents.json file.")
        except Exception as e:
            messagebox.showerror("Training Error", f"An error occurred during training: {e}")

    def on_enter(self, event):
        msg = self.msg_entry.get()
        self.my_msg(msg, "You")
        self.bot_response(msg, "Bot")

    def bot_response(self, msg, sender):
        self.text_widget.configure(state=NORMAL)
        response = self.test.response(msg)
        self.text_widget.insert(END, str(sender) + " : " + response + "\n\n")
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

    def my_msg(self, msg, sender):
        if not msg:
            return
        self.msg_entry.delete(0, END)
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, str(sender) + " : " + str(msg) + "\n")
        self.text_widget.configure(state=DISABLED)

if __name__ == "__main__":
    bot = ChatBot()
    bot.run()
