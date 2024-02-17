import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import csv
from NewProfile import NewProfile
from UserPiggyBankPage import UserPiggyBankPage

class LabeledEntry(tk.Entry):
    def __init__(self, master=None, label="", placeholder="", **kwargs): #**kwargs used to collect additional keyboard arguments that are not explicitly named in the method
        tk.Entry.__init__(self, master, **kwargs)
        self.label=label
        self.placeholder=placeholder
        self.insert(0, placeholder)
        self.bind("<FocusIn>", self.on_entry_focus_in)
        self.bind("<FocusOut>", self.on_entry_focus_out)

    def on_entry_focus_in(self, event):
        if self.get()==self.placeholder:
            self.delete(0, tk.END)
            self.config(fg="#000")

    def on_entry_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg="grey")

class LoginPage():
    def __init__(self,root): #initial layout and components
        self.root=root #stores a reference to the main window as an instance attribute for easy access within the class
        self.root.title("Personal Piggy Bank")

        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)

        # Username entry
        self.username_entry=LabeledEntry(self.login_frame, placeholder="Username")
        self.username_entry.grid(row=0, column=0, columnspan=2, pady=10)

        # Password entry
        self.password_entry=LabeledEntry(self.login_frame, placeholder="Password", show="*")
        self.password_entry.grid(row=1, column=0, columnspan=2, pady=10)

        # Login button
        self.login_button=tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Sign up button
        self.signup_label=ttk.Label(self.login_frame, text="Don't have a profile? ")
        self.signup_label.grid(row=3, column=0, pady=10)
        self.signup_button=tk.Button(self.login_frame, text="Sign Up here", command=self.signup)
        self.signup_button.grid(row=3, column=1, columnspan=2, pady=10)

    # Authentication functionality
    def login(self):
        username=self.username_entry.get()
        password=self.password_entry.get()

        # Verify credentials from CSV file
        if self.verify_credentials(username, password):
            messagebox.showinfo("Login", f"{username} has logged in")
            self.open_piggy_bank_window(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # Method to verify credentials from CSV file
    def verify_credentials(self, username, password):
        with open('user_info.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >=6 and row[5] == username and row[6] == password:
                    return True
        return False

    # Open user's Piggy Bank window
    def open_piggy_bank_window(self, username):
        piggy_bank_window = UserPiggyBankPage(username)
        piggy_bank_window.mainloop()

    # Signup functionality
    def signup(self):
        signup_page=NewProfile(self.root)