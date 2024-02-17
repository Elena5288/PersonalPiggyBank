import tkinter as tk
import csv
from tkinter import ttk, messagebox

class UserPiggyBankPage(tk.Toplevel):
    def __init__(self, username):
        tk.Toplevel.__init__(self)
        self.title(f"{username}'s Piggy Bank")
        self.geometry("600x400")
        self.username = username
        self.user_id = self.get_user_id_from_csv(username)  # Get user_id from CSV

        # Menu Bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu (you can add more menus as needed)
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="Profile", command=self.show_profile)
        file_menu.add_command(label="Dashboard", command=self.show_dashboard)
        file_menu.add_command(label="Accounts", command=self.show_accounts)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.destroy)

        # Message Label
        self.message_label = tk.Label(self, text="Please make a selection from the menu!", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.message_label.pack(side=tk.TOP, fill=tk.X)

        # Notebook for displaying content
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Create frames for each functionality
        self.accounts_frame = tk.Frame(self.notebook, bg="lightblue")
        self.dashboard_frame = tk.Frame(self.notebook, bg="lightgreen")
        self.profile_frame = tk.Frame(self.notebook)

        # Labels to display user details in the Profile tab
        self.profile_labels = {}

    def get_user_id_from_csv(self, username):
        with open('user_info.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 6 and row[5] == username:
                    return row[0]  # Return user_id associated with the username
        return None

    def show_profile(self):
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        # Add the profile frame to the notebook
        self.notebook.add(self.profile_frame, text="Profile")

        # Read user details from user_info.csv
        user_details = self.get_user_details_from_csv()

        # Display user details in the Profile tab
        if user_details:
            for key, value in user_details.items():
                label_text = f"{key}: {value}"
                label = tk.Label(self.profile_frame, text=label_text)
                label.grid(pady=5, sticky="w")
                self.profile_labels[key] = label
        else:
            tk.Label(self.profile_frame, text="User details not found.").pack()

        print("Showing Profile")

    def get_user_details_from_csv(self):
        user_details = {}
        if self.user_id:
            with open('user_info.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 8 and row[0] == str(self.user_id):
                        user_details = {
                            "First Name": row[1],
                            "Last Name": row[2],
                            "Date of Birth": row[3],
                            "Employment Type": row[4],
                            "Number of Accounts": row[7]
                        }
                        break
        return user_details

    def show_dashboard(self):
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        # Add the dashboard frame to the notebook
        self.notebook.add(self.dashboard_frame, text="Dashboard")

        # Configure the style for vertical tabs
        style = ttk.Style()
        style.configure("Vertical.TNotebook", tabposition='wn')
        style.map("Vertical.TNotebook.Tab", background=[("active", "darkgrey")])

        # Create a vertical notebook for dashboard tabs
        vertical_notebook = ttk.Notebook(self.dashboard_frame, style="Vertical.TNotebook")
        vertical_notebook.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=10)

        # Define the tabs for the vertical notebook along with their background colors
        dashboard_tabs = {
            "Cashflow Form": "lightblue",
            "Payments Calendar": "lightgreen",
            "Budget Overview": "lightyellow",
            "Forecast": "lightcoral",
            "Spend Tracker": "lightpink"
        }

        # Create frames for each dashboard tab and add them to the vertical notebook
        for tab_title, tab_color in dashboard_tabs.items():
            tab_frame = tk.Frame(vertical_notebook, bg=tab_color)
            tab_label = ttk.Label(tab_frame, text=tab_title, font=("Arial", 12, "bold"))
            tab_label.pack(padx=15, pady=15)
            vertical_notebook.add(tab_frame, text=tab_title)

        print("Showing Dashboard with Colored Tabs")

    def show_accounts(self):
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        if self.user_id:
            self.message_label.config(text="")
            self.load_accounts()
        else:
            self.message_label.config(text="User not found.")

    def load_accounts(self):
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        # Add the accounts frame to the notebook
        self.notebook.add(self.accounts_frame, text="Accounts")

        # Adjust the file name/path
        with open('account_info.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 4 and row[0] == str(self.user_id):
                    account_name = row[1]
                    account_type = row[2]
                    account_number = row[3]

                    # Create a new frame for each account
                    account_frame = tk.Frame(self.notebook)
                    account_frame.pack(expand=True, fill=tk.BOTH)

                    account_label = tk.Label(account_frame, text=f"Account Type: {account_type}\nAccount Number: {account_number}")
                    account_label.pack(padx=10, pady=10)

                    # Add the frame to the notebook as a tab
                    tab_label = f"{account_type}: {account_number}"
                    self.notebook.add(account_frame, text=tab_label)
