import tkinter as tk
import csv
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from Calculations import calculate_monthly_totals

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

        # File menu
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="Profile", command=self.show_profile)
        file_menu.add_command(label="Dashboard", command=self.show_dashboard)
        file_menu.add_command(label="Accounts", command=self.show_accounts)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.destroy)

        # Message Label
        self.message_label = tk.Label(self, text="Please make a selection from the menu!", bd=1,
                                      relief=tk.SUNKEN, anchor=tk.W)
        self.message_label.pack(side=tk.TOP, fill=tk.X)

        # Notebook for displaying content
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Call show_accounts to display the "Accounts" tab by default
        self.show_accounts()

        # Create frames for each functionality
        self.accounts_frame = tk.Frame(self.notebook, bg="lightblue")
        self.dashboard_frame = tk.Frame(self.notebook, bg="lightgreen")
        self.profile_frame = tk.Frame(self.notebook)

        # Labels to display user details in the Profile tab
        self.profile_labels = {}

        # Create a dictionary to store data from the Cashflow Form
        self.cashflow_data = {
            "Account Number": tk.StringVar(),
            "Money In/Out": tk.StringVar(),
            "Transaction Date": tk.StringVar(),
            "Transaction Amount": tk.StringVar(),
            "Transaction Scope": tk.StringVar()}

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
                            "Number of Accounts": row[7]}
                        break
        return user_details

    def show_dashboard(self):
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        # Check if the dashboard frame already exists
        if hasattr(self, 'dashboard_frame'):
            # If it exists, destroy it and create a new one
            self.dashboard_frame.destroy()

            # Create a new dashboard frame
            self.dashboard_frame = tk.Frame(self.notebook)
            self.notebook.add(self.dashboard_frame, text="Dashboard")

            # Configure the style for vertical tabs
            style = ttk.Style()
            style.configure("Vertical.TNotebook", tabposition='wn')
            style.map("Vertical.TNotebook.Tab", background=[("active", "darkgrey")])

            # Create a vertical notebook for dashboard tabs
            vertical_notebook = ttk.Notebook(self.dashboard_frame, style="Vertical.TNotebook")
            vertical_notebook.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=10)

            # Create the Cashflow Form tab
            cashflow_frame = tk.Frame(vertical_notebook)
            vertical_notebook.add(cashflow_frame, text="Cashflow Form")

            # Title for the Cashflow Form
            cashflow_title_label = ttk.Label(cashflow_frame, text="Cashflow Form", font=("Arial", 12, "bold"))
            cashflow_title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky='w')

            # List with Account Type and Account Number
            account_options=[]
            with open('account_info.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3 and row[0] == str(self.user_id):
                        account_type = row[1]
                        account_number = row[2]
                        account_options.append(f"{account_type}:{account_number}")


            # Combo button for Account Type and Number
            account_combo_label = ttk.Label(cashflow_frame, text="Account:")
            account_combo_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')
            account_combo = ttk.Combobox(cashflow_frame, values=account_options,
                                         textvariable=self.cashflow_data["Account Number"])
            account_combo.grid(row=1, column=1, pady=10, padx=10, sticky='w')

            # Radio buttons for Spending/Withdrawal or Deposit
            money_inout_label = ttk.Label(cashflow_frame, text="Money In/Out:")
            money_inout_label.grid(row=2, column=0, pady=10, padx=10, sticky='w')
            money_inout_frame = ttk.Frame(cashflow_frame)
            money_inout_frame.grid(row=2, column=1, pady=10, padx=10, sticky='w')
            money_inout_var = self.cashflow_data["Money In/Out"]
            money_inout_radio = ttk.Radiobutton(money_inout_frame, text="Spending",
                                                variable=money_inout_var, value="out")
            money_inout_radio.grid(row=0, column=0, padx=5)
            money_inout_radio = ttk.Radiobutton(money_inout_frame, text="Deposit",
                                                variable=money_inout_var, value="in")
            money_inout_radio.grid(row=0, column=1, padx=5)

            # Date Picker Calendar for Transaction Date
            date_label = ttk.Label(cashflow_frame, text="Transaction Date:")
            date_label.grid(row=3, column=0, pady=10, padx=10, sticky='w')
            date_picker = DateEntry(cashflow_frame, width=12, background='darkblue', foreground='white',
                                    borderwidth=2, textvariable=self.cashflow_data["Transaction Date"])
            date_picker.grid(row=3, column=1, pady=10, padx=10, sticky='w')

            # Textbox for Transaction Amount
            amount_label = ttk.Label(cashflow_frame, text="Transaction Amount:")
            amount_label.grid(row=4, column=0, pady=10, padx=10, sticky='w')
            amount_entry = ttk.Entry(cashflow_frame, textvariable=self.cashflow_data["Transaction Amount"])
            amount_entry.grid(row=4, column=1, pady=10, padx=10, sticky='w')

            # Combo box for Transaction Scope
            scope_label = ttk.Label(cashflow_frame, text="Transaction Scope:")
            scope_label.grid(row=5, column=0, pady=10, padx=10, sticky='w')
            scope_options_mapping = {
                "out": ["Hydro", "Phone", "Internet", "Transport", "Sport", "Groceries",
                             "Health", "Fee","Entertainment", "Fashion"],
                "in": ["Salary", "Dividends", "Interest"]}

            # Function to update Transaction Scope options based on Money In/Out selection
            def update_scope_options(*args):
                selected_money_inout = money_inout_var.get()
                scope_combo["values"] = scope_options_mapping.get(selected_money_inout, [])

            # Bind the function to the Money In/Out variable
            money_inout_var.trace_add("write", update_scope_options)

            # Default options for Transaction Scope
            default_scope_options = scope_options_mapping.get(money_inout_var.get(), [])
            scope_combo = ttk.Combobox(cashflow_frame, values=default_scope_options,
                                       textvariable=self.cashflow_data["Transaction Scope"])
            scope_combo.grid(row=5, column=1, pady=10, padx=10, sticky='w')

            # Save button to save the data to cashflow.csv
            save_button = ttk.Button(cashflow_frame, text="Save", command=self.save_cashflow_data)
            save_button.grid(row=6, column=0, pady=10, padx=10, sticky='w')

            # Create the Transfer tab
            transfer_frame = tk.Frame(vertical_notebook)
            vertical_notebook.add(transfer_frame, text="Transfer")

            # Title for the Transfer form
            cashflow_title_label = ttk.Label(transfer_frame, text="Transfer Form", font=("Arial", 12, "bold"))
            cashflow_title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky='w')

            # Combo button for "From" account
            from_label = ttk.Label(transfer_frame, text="From:")
            from_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')
            self.from_account_combo = ttk.Combobox(transfer_frame, values=account_options,
                                              textvariable=self.cashflow_data["Account Number"])
            self.from_account_combo.grid(row=1, column=1, pady=10, padx=10, sticky='w')

            amount_label_transfer = ttk.Label(transfer_frame, text="Amount:")
            amount_label_transfer.grid(row=2, column=0, pady=10, padx=10, sticky='w')
            amount_entry_transfer = ttk.Entry(transfer_frame, textvariable=self.cashflow_data["Transaction Amount"])
            amount_entry_transfer.grid(row=2, column=1, pady=10, padx=10, sticky='w')

            date_label_transfer = ttk.Label(transfer_frame, text="Transaction Date:")
            date_label_transfer.grid(row=3, column=0, pady=10, padx=10, sticky='w')
            date_picker_transfer = DateEntry(transfer_frame, width=12, background='darkblue', foreground='white',
                                             borderwidth=2, textvariable=self.cashflow_data["Transaction Date"])
            date_picker_transfer.grid(row=3, column=1, pady=10, padx=10, sticky='w')

            # Combo button for "To" account
            to_label = ttk.Label(transfer_frame, text="To:")
            to_label.grid(row=4, column=0, pady=10, padx=10, sticky='w')
            self.to_account_combo = ttk.Combobox(transfer_frame, values=account_options,
                                            textvariable=self.cashflow_data["Transaction Scope"])
            self.to_account_combo.grid(row=4, column=1, pady=10, padx=10, sticky='w')

            save_button_transfer = ttk.Button(transfer_frame, text="Save", command=self.save_transfer_data)
            save_button_transfer.grid(row=5, column=0, pady=10, padx=10, sticky='w')
        else:
            # If it exists, simply show the existing dashboard frame
            self.notebook.add(self.dashboard_frame, text="Dashboard")

    def save_cashflow_data(self):
        account_number = self.cashflow_data["Account Number"].get().split(":")[-1]
        money_inout = self.cashflow_data["Money In/Out"].get()
        transaction_date = self.cashflow_data["Transaction Date"].get()
        transaction_amount = self.cashflow_data["Transaction Amount"].get()
        transaction_scope = self.cashflow_data["Transaction Scope"].get()

        # Convert the transaction date to the desired format
        formatted_date = datetime.strptime(transaction_date, "%m/%d/%y").strftime("%m/%d/%Y")

        with open('cashflow.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.user_id,
                account_number,
                money_inout,
                formatted_date,
                transaction_amount,
                transaction_scope])

        # Call the calculations function after saving cashflow data
        calculate_monthly_totals()

        messagebox.showinfo("Success", "Cashflow data saved successfully!")

    def save_transfer_data(self):
        from_account_number = self.from_account_combo.get().split(":")[-1]
        to_account_number = self.to_account_combo.get().split(":")[-1]

        # Convert the transaction date to the desired format
        formatted_date = datetime.strptime(self.cashflow_data["Transaction Date"].get(), "%m/%d/%y").strftime("%m/%d/%Y")

        # Open 'cashflow.csv' in append mode and write the data
        with open('cashflow.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.user_id,
                from_account_number,
                "out",
                formatted_date,
                self.cashflow_data["Transaction Amount"].get(),
                to_account_number])

            writer.writerow([
                self.user_id,
                to_account_number,
                "in",
                formatted_date,
                self.cashflow_data["Transaction Amount"].get(),
                from_account_number])

        # Call the calculations function after saving transfer data
        calculate_monthly_totals()

        messagebox.showinfo("Success", "Transfer data saved successfully!")

    def show_accounts(self):
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        if self.user_id:
            self.message_label.config(text="")
            self.load_accounts()
        else:
            self.message_label.config(text="User not found.")

    def read_account_monthly_totals(self):
        # Read account monthly totals from the file
        account_totals = {}
        with open('account_monthly_totals.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 5:
                    account_number = row[1]
                    month_year = row[2]
                    total = row[3]
                    prior_total = row[4]
                    account_totals[(account_number, month_year)] = (total, prior_total)
        return account_totals

    def load_accounts(self):
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        # Read account monthly totals from the file
        account_totals = self.read_account_monthly_totals()

        # Add the accounts frame to the notebook
        #self.notebook.add(self.accounts_frame, text="Accounts")

        with open('account_info.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3 and row[0] == str(self.user_id):
                    account_type = row[1]
                    account_number = row[2]

                    # Create a new frame for each account
                    account_frame = tk.Frame(self.notebook)
                    account_frame.pack(expand=True, fill=tk.BOTH)

                    # Display account information
                    account_label_text = f"Account Type: {account_type}\nAccount Number: {account_number}"
                    account_label = tk.Label(account_frame, text=account_label_text)
                    account_label.pack(padx=10, pady=10)

                    # Get and display account monthly totals
                    totals_info = self.get_account_totals_info(account_number, account_totals)
                    totals_label = tk.Label(account_frame, text=totals_info)
                    totals_label.pack(padx=10, pady=10)

                    # Add the frame to the notebook as a tab
                    tab_label = f"{account_type} - {account_number}"
                    self.notebook.add(account_frame, text=tab_label)

    def get_account_totals_info(self, account_number, account_totals):
        # Get account monthly totals information
        current_month_year = datetime.now().strftime("%Y/%m")
        totals_info = account_totals.get((account_number, current_month_year), ("0.00", "0.00"))
        total, prior_total = map(lambda x: "{:.2f}".format(float(x)), totals_info)
        return f"Total for {current_month_year}: ${total} - Prior Month Total: ${prior_total}"

