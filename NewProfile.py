import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
from datetime import datetime
import random as r

my_entries = []
count = 0  # To keep track of inserted entries

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

class NewProfile(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.title("Create new profile")
        self.user_id = r.randint(10000,99999) # Random user_id between 10000 and 99999
        self.first_name = ""
        self.last_name = ""
        self.dob = ""
        self.employment = ""
        self.num_accounts = 0

        # Sign up frame
        self.signup_frame = ttk.Frame(self)
        self.signup_frame.grid(row=0, column=0, padx=20, pady=20)

        # First name entry
        self.first_name_entry = LabeledEntry(self.signup_frame, label="First Name", placeholder="First Name")
        self.first_name_entry.grid(row=0, column=0, pady=10)

        # Last name entry
        self.last_name_entry = LabeledEntry(self.signup_frame, label="Last Name", placeholder="Last Name")
        self.last_name_entry.grid(row=0, column=2, pady=10)

        # Date of birth
        self.dob_label = ttk.Label(self.signup_frame, text="Date of birth")
        self.dob_label.grid(row=1, column=0, pady=10, sticky="w")

        self.day_spinbox = ttk.Spinbox(self.signup_frame, from_=1, to=31, width=5, wrap=True, state="readonly")
        self.day_spinbox.grid(row=1, column=1, pady=10, sticky="w")
        self.month_spinbox = ttk.Spinbox(self.signup_frame, values=("January", "February", "March", "April", "May", "June",
                                                                    "July", "August", "September", "October", "November",
                                                                    "December"),width=15, wrap=True, state="readonly")
        self.month_spinbox.grid(row=1, column=2, pady=10, sticky="we")
        self.year_spinbox = ttk.Spinbox(self.signup_frame, from_=1900, to=2011, width=8, wrap=True, state="readonly")
        self.year_spinbox.grid(row=1, column=3, pady=10, sticky="w")

        # Type of employment
        self.employment_options = ["Employee", "Self-employed", "Homemaker", "Student"]
        self.employment_var=tk.StringVar(self)
        self.employment_var.set(self.employment_options[0])
        self.employment_combobox = ttk.Combobox(self.signup_frame, textvariable=self.employment_var,
                                                values=self.employment_options, state="readonly")
        self.employment_combobox.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")

        # Username entry
        self.username_entry = LabeledEntry(self.signup_frame, placeholder="Username")
        self.username_entry.grid(row=3, column=0, pady=10, sticky="w")

        # Password
        self.password_entry = LabeledEntry(self.signup_frame, placeholder="Password")
        self.password_entry.grid(row=3, column=2, pady=10)

        # Bank account frame
        self.bank_info_frame = ttk.Frame(self)
        self.bank_info_frame.grid(row=1, column=0, padx=20)

        # Initialize bank_info_widgets list
        self.bank_info_widgets = []

        # Number of accounts entry
        self.num_accounts_label = ttk.Label(self.signup_frame, text="Number of Accounts")
        self.num_accounts_label.grid(row=4, column=0, pady=10, sticky="w")
        self.num_accounts_entry = ttk.Entry(self.signup_frame, width=5)
        self.num_accounts_entry.grid(row=4, column=1, pady=10, sticky="w")

        # Add account button
        self.add_account_button = tk.Button(self.bank_info_frame, text="Add Account", command=self.add_account)
        self.add_account_button.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        # Save profile button
        self.save_profile_button = tk.Button(self.bank_info_frame, text="Save profile", command=self.save_profile)
        self.save_profile_button.grid(row=0, column=2, columnspan=2, pady=10, sticky="w")

    def add_account(self):
        # Get the number of accounts to add
        num_accounts = int(self.num_accounts_entry.get())

        # Create widgets for each account and add them to the bank_info_frame
        for i in range(num_accounts):
            account_label = ttk.Label(self.bank_info_frame, text=f"Account {i + 1}")
            account_label.grid(row=i + 1, column=0, pady=5, sticky="w")

            # Type of account dropdown
            account_type_options = ["Debit", "Credit", "Savings", "Investment", "Loan"]
            account_type_var = tk.StringVar(self.bank_info_frame)
            account_type_var.set(account_type_options[0])
            account_type_dropdown = ttk.Combobox(self.bank_info_frame, textvariable=account_type_var,
                                                 values=account_type_options, state="readonly")
            account_type_dropdown.grid(row=i + 1, column=1, pady=5, sticky="w")

            # Account number entry
            account_number_entry = LabeledEntry(self.bank_info_frame, placeholder="Account Number")
            account_number_entry.grid(row=i + 1, column=2, pady=5, sticky="w")

            # Credit limit entry (only for "Credit" account type)
            credit_limit_label = ttk.Label(self.bank_info_frame, text="Credit Account Limit:")
            credit_limit_entry = LabeledEntry(self.bank_info_frame, placeholder="Credit Limit")

            # Keep track of created widgets to clear them later
            self.bank_info_widgets.extend(
                [account_label, account_type_dropdown, account_number_entry, credit_limit_label, credit_limit_entry])

            def on_account_type_change(event):
                if account_type_var.get() == "Credit":
                    credit_limit_label.grid(row=i + 1, column=3, pady=5, sticky="w")
                    credit_limit_entry.grid(row=i + 1, column=4, pady=5, sticky="w")
                else:
                    credit_limit_label.grid_forget()
                    credit_limit_entry.grid_forget()

            account_type_dropdown.bind("<<ComboboxSelected>>", on_account_type_change)

            # Bind the function once to check the initial value
            on_account_type_change(None)

    def save_profile(self):
        self.first_name = self.first_name_entry.get()
        self.last_name = self.last_name_entry.get()
        self.dob = f"{self.day_spinbox.get()} {self.month_spinbox.get()} {self.year_spinbox.get()}"
        self.employment = self.employment_var.get()
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        # Check if any of the fields are empty
        empty_fields = []

        if self.first_name == self.first_name_entry.placeholder:
            empty_fields.append(self.first_name_entry)
        if self.last_name == self.last_name_entry.placeholder:
            empty_fields.append(self.last_name_entry)
        if self.username == self.username_entry.placeholder:
            empty_fields.append(self.username_entry)
        if self.password == self.password_entry.placeholder:
            empty_fields.append(self.password_entry)

        for entry_widget in empty_fields:
            entry_widget.configure(background="red")

        if empty_fields:
            messagebox.showwarning("Error", "Please fill in all fields.")
            return
        else:
            for entry_widget in [self.first_name_entry, self.last_name_entry, self.username_entry, self.password_entry]:
                entry_widget.config(bg="#fff")

        # Save user information
        num_accounts = int(self.num_accounts_entry.get())
        user_info = [self.user_id, self.first_name, self.last_name, self.dob, self.employment, self.username,
                     self.password, num_accounts]
        with open("user_info.csv", "a", newline="") as user_file:
            user_writer = csv.writer(user_file)
            user_writer.writerow(user_info)

        # Save account information
        account_info = []
        for i in range(len(self.bank_info_widgets) // 5):  # Five widgets per account
            account_type = self.bank_info_widgets[i * 5 + 1].get()
            account_number = self.bank_info_widgets[i * 5 + 2].get()

            # Check if the account type is "Credit" to include Credit Limit in account_info
            if account_type == "Credit":
                if len(self.bank_info_widgets) > i * 5 + 4:  # Ensure the index is within bounds
                    credit_limit_entry = self.bank_info_widgets[i * 5 + 4]
                    credit_limit = credit_limit_entry.get() if isinstance(credit_limit_entry, LabeledEntry) else ""
                else:
                    credit_limit = ""
                account_info.append([self.user_id, account_type, account_number, credit_limit])
            else:
                account_info.append([self.user_id, account_type, account_number])

        with open("account_info.csv", "a", newline="") as account_file:
            account_writer = csv.writer(account_file)
            account_writer.writerows(account_info)

        # Inform the user that the profile has been saved
        messagebox.showinfo("Success", "Profile has been saved.")

        # Clear bank info fields
        for widget in self.bank_info_widgets:
            widget.destroy()
        self.bank_info_widgets = []

        self.destroy()

