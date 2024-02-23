import tkinter as tk
import csv
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from Calculations import calculate_monthly_totals
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class UserPiggyBankPage(tk.Toplevel):
    def __init__(self, username):
        tk.Toplevel.__init__(self)
        self.title(f"{username}'s Piggy Bank")
        self.geometry("600x400")
        self.username = username
        self.user_id = self.get_user_id_from_csv(username)  # Get user_id from CSV


        # Call the calculations function as soon as the new window appears
        calculate_monthly_totals()

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

        # Create frames for each functionality
        self.accounts_frame = tk.Frame(self.notebook)
        self.dashboard_frame = tk.Frame(self.notebook)
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

        # Call show_dashboard to display the "Dashboard" tab by default
        self.show_dashboard()

    def get_user_id_from_csv(self, username):
        with open('user_info.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 6 and row[5] == username:
                    return row[0]  # Return user_id associated with the username
        return None

    def show_profile(self):
        # Check if the profile frame already exists
        if hasattr(self, 'profile_frame'):
            # If it exists, destroy it and create a new one
            self.profile_frame.destroy()

            # Create a new profile frame
            self.profile_frame = tk.Frame(self.notebook)
            self.notebook.add(self.profile_frame, text="Profile")

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

                # Display credit limit information
                self.display_credit_limit_info()
            else:
                tk.Label(self.profile_frame, text="User details not found.").pack()

    def display_credit_limit_info(self):
        # Get credit limit information from account_info.csv
        credit_limit_info = self.get_credit_limit_info()

        if credit_limit_info:
            for account_number, credit_limit in credit_limit_info.items():
                if credit_limit != "":
                    credit_limit_label_text = f"Credit limit for account {account_number}: ${credit_limit}"
                    credit_limit_label = tk.Label(self.profile_frame, text=credit_limit_label_text)
                    credit_limit_label.grid(pady=5, sticky="w")

        else:
            tk.Label(self.profile_frame, text="Credit limit information not found.").pack()

    def get_credit_limit_info(self):
        # Get credit limit information from account_info.csv
        credit_limit_info = {}
        with open('account_info.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 4 and row[0] == str(self.user_id):
                    account_number = row[2]
                    credit_limit = row[3]
                    credit_limit_info[account_number] = credit_limit
        return credit_limit_info

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

            # Default options for Transaction Scope
            default_scope_options = scope_options_mapping.get(money_inout_var.get(), [])
            scope_combo = ttk.Combobox(cashflow_frame, values=default_scope_options,
                                       textvariable=self.cashflow_data["Transaction Scope"])
            scope_combo.grid(row=5, column=1, pady=10, padx=10, sticky='w')

            # Function to update Transaction Scope options based on Money In/Out selection
            def update_scope_options(*args):
                selected_money_inout = money_inout_var.get()
                scope_combo["values"] = scope_options_mapping.get(selected_money_inout, [])

            # Bind the function to the Money In/Out variable
            money_inout_var.trace_add("write", update_scope_options)

            # Initially update the values based on the default Money In/Out
            update_scope_options()

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

        # Create the Credit Overview tab
        credit_overview_frame = tk.Frame(vertical_notebook)
        vertical_notebook.add(credit_overview_frame, text="Credit Overview")

        # Get user's credit account number from account_info.csv
        user_credit_account_number = self.get_credit_account_number()

        if user_credit_account_number:
            # Get credit overview information
            credit_limit_info = self.get_credit_limit_info()
            credit_balance = self.calculate_credit_balance(user_credit_account_number)
            credit_limit = float(credit_limit_info.get(user_credit_account_number, 0.0))
            available_credit = credit_limit - abs(credit_balance)
            balance_percentage = (abs(credit_balance) / credit_limit) * 100

            # Display credit overview information
            credit_limit_label = ttk.Label(credit_overview_frame, text=f"Credit Limit: ${credit_limit:.2f}")
            credit_limit_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')

            balance_label = ttk.Label(credit_overview_frame, text=f"Balance: ${credit_balance:.2f}")
            balance_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

            available_credit_label = ttk.Label(credit_overview_frame, text=f"Available: ${available_credit:.2f}")
            available_credit_label.grid(row=2, column=0, pady=10, padx=10, sticky='w')

            # Progress bar
            progress_bar_style = ttk.Style()
            balance_percentage = (abs(credit_balance) / credit_limit) * 100

            # Cap the balance_percentage at 100
            balance_percentage = min(balance_percentage, 100)

            # Create the progress bar with the selected style
            progress_bar = ttk.Progressbar(credit_overview_frame, orient=tk.HORIZONTAL, length=300,
                                           mode='determinate', style="Custom.Horizontal.TProgressbar")

            # Apply the style to the progress bar
            progress_bar['value'] = balance_percentage
            progress_bar.grid(row=3, column=0, pady=10, padx=10, sticky='w')

            progress_label = ttk.Label(credit_overview_frame, text=f"You have used {balance_percentage:.2f}%")
            progress_label.grid(row=4, column=0, pady=10, padx=10, sticky='w')

            # Call the calculations function after displaying Credit Overview data
            calculate_monthly_totals()

        else:
            # Display a message if the user doesn't have a credit account
            no_credit_account_label = ttk.Label(credit_overview_frame, text="No credit account found.")
            no_credit_account_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        # Create the Your Spending tab
        self.your_spending_frame = tk.Frame(vertical_notebook)
        vertical_notebook.add(self.your_spending_frame, text="Your Spending")

        # Create and display vertical progress bars for the last 5 months
        self.create_spending_progress_bars()

        # Create the Wallet Graph tab
        wallet_graph_frame = tk.Frame(vertical_notebook)
        vertical_notebook.add(wallet_graph_frame, text="Wallet Graph")

        # Calculate and display pie chart and legend
        self.create_wallet_graph(wallet_graph_frame)

    def get_credit_account_number(self):
        # Get the user's credit account number from account_info.csv
        with open('account_info.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3 and row[0] == str(self.user_id) and row[1].lower() == "credit":
                    return row[2]
        return None

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

        # Reset the fields to empty values
        self.cashflow_data["Account Number"].set("")
        self.cashflow_data["Money In/Out"].set("")
        self.cashflow_data["Transaction Amount"].set("")
        self.cashflow_data["Transaction Scope"].set("")

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

        # Reset the fields to empty values
        self.from_account_combo.set("")
        self.to_account_combo.set("")
        self.cashflow_data["Transaction Amount"].set("")

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

                    # Check if it's a credit account and display additional information
                    if account_type.lower() == "credit":
                        credit_info = self.get_credit_account_info(account_number)
                        credit_label = tk.Label(account_frame, text=credit_info)
                        credit_label.pack(padx=10, pady=10)

                        # If it's a credit account, do not display the monthly totals
                    else:
                        totals_label = tk.Label(account_frame, text=totals_info)
                        totals_label.pack(padx=10, pady=10)

                    # Create a table for transactions
                    tree = ttk.Treeview(account_frame, columns=("Money In/Out", "Date", "Amount", "Scope"),
                                        show="headings")
                    tree.heading("Money In/Out", text="Money In/Out", anchor=tk.CENTER)
                    tree.heading("Date", text="Date", anchor=tk.CENTER)
                    tree.heading("Amount", text="Amount", anchor=tk.CENTER)
                    tree.heading("Scope", text="Scope", anchor=tk.CENTER)
                    tree.column("Money In/Out", width=100)
                    tree.column("Date", width=100)
                    tree.column("Amount", width=100)
                    tree.column("Scope", width=150)
                    tree.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

                    # Insert transactions into the Treeview
                    current_month_year = datetime.now().strftime("%m/%Y")
                    transactions = self.get_transactions_for_month(account_number, current_month_year)
                    for transaction in transactions:
                        # Split the transaction string into a tuple
                        transaction_data = tuple(transaction.split())
                        tree.insert("", "end", values=transaction_data)

                    # Add the frame to the notebook as a tab
                    tab_label = f"{account_type} - {account_number}"
                    self.notebook.add(account_frame, text=tab_label)

    def get_credit_account_info(self, account_number):
        # Calculate credit-related information for credit accounts
        credit_limit_str = self.get_credit_limit_info().get(account_number, "0.0")

        # Convert credit limit to float
        try:
            credit_limit = float(credit_limit_str)
        except ValueError:
            credit_limit = 0.0

        credit_balance = self.calculate_credit_balance(account_number)
        available_credit = credit_limit - abs(credit_balance)

        return f"Credit Limit: ${credit_limit:.2f}  Balance: ${credit_balance:.2f}  Available: ${available_credit:.2f}"

    def calculate_credit_balance(self, account_number_prefix="21"):
        # Read the monthly totals from account_monthly_totals.csv
        monthly_totals = pd.read_csv('account_monthly_totals.csv')

        # Get the current year and month
        current_year_month = datetime.now().strftime('%Y/%m')

        # Filter data for accounts starting with the specified prefix and current year/month
        account_data = monthly_totals[
            (monthly_totals['Account Number'].astype(str).str.startswith(account_number_prefix)) &
            (monthly_totals['Month/Year'] == current_year_month)]

        # Calculate credit balance based on the 'Total' column
        credit_balance = account_data['Total'].sum()

        return credit_balance

    def get_transactions_for_credit_account(self, account_number):
        # Retrieve transactions for a credit account
        transactions = []
        last_in_date = None
        with open('cashflow.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 6 and row[1] == account_number:
                    transaction_date = datetime.strptime(row[3], "%m/%d/%Y").date()
                    if row[2] == "in":
                        last_in_date = transaction_date
                    transactions.append(row)

        # Filter transactions after the last 'in' transaction date
        return [transaction for transaction in transactions if datetime.strptime(transaction[3], "%m/%d/%Y").date() > last_in_date]

    def get_account_totals_info(self, account_number, account_totals):
        # Get account monthly totals information
        current_month_year = datetime.now().strftime("%Y/%m")
        totals_info = account_totals.get((account_number, current_month_year), ("0.00", "0.00"))
        total, prior_total = map(lambda x: "{:.2f}".format(float(x)), totals_info)
        return f"Total for {current_month_year}: ${total} - Prior Month Total: ${prior_total}"

    def get_transactions_for_month(self, account_number, month_year):
        transactions = []
        with open('cashflow.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 6 and row[1] == account_number:
                    transaction_date = datetime.strptime(row[3], "%m/%d/%Y").strftime("%m/%Y")
                    # The scope conditions
                    scope_code = row[5][:2]
                    if scope_code == "11":
                        scope_display = "Debit"
                    elif scope_code == "21":
                        scope_display = "Credit"
                    elif scope_code == "31":
                        scope_display = "Savings"
                    elif scope_code == "41":
                        scope_display = "Investment"
                    elif scope_code == "51":
                        scope_display = "Loan"
                    else:
                        scope_display = row[5].title()
                    if transaction_date == month_year:
                        transaction_info = f"{row[2].capitalize()}    {row[3]}    ${row[4]}    {scope_display}"
                        transactions.append(transaction_info)
        return transactions

    def create_spending_progress_bars(self):
        # Read spending data from avg_spending.csv
        avg_spending = pd.read_csv('avg_spending.csv')

        # Define the mapping of transaction scopes to categories
        scope_category_mapping = {
            "salary": "income",
            "dividends": "income",
            "interest": "income",
            "41": "investments",}

        # Filter relevant scopes for spending and income
        spending_scopes = ["transport", "sport", "rent", "phone", "internet", "hydro", "health",
                           "groceries", "fee", "fashion", "entertainment", "investments"]
        income_scopes = ["salary", "interest", "dividends"]

        # Create a dictionary to store monthly spending and income totals
        monthly_totals = {'spending': [], 'income': []}

        # Iterate over the last 5 months
        for i in range(5):
            # Calculate the month/year for the current iteration
            current_month_year = (datetime.now() - pd.DateOffset(months=i)).strftime("%Y/%m")

            # Filter data for the current month
            current_month_data = avg_spending[avg_spending['Month/Year'] == current_month_year]

            # Sum spending and income based on the defined scopes
            spending_total = current_month_data[current_month_data['Transaction Scope'].isin(spending_scopes)][
                'Monthly Total'].sum()
            income_total = current_month_data[current_month_data['Transaction Scope'].isin(income_scopes)][
                'Monthly Total'].sum()

            # Fetch investments total from the "41" prefixed transaction scopes
            investments_total = current_month_data[current_month_data['Transaction Scope'].str.startswith("41")][
                'Monthly Total'].sum()

            # Append the totals to the dictionary
            monthly_totals['spending'].append(spending_total)
            monthly_totals['income'].append(income_total)

            # Add investments total to the spending total
            monthly_totals['spending'][-1] += investments_total

        # Get the maximum value for the progress bars
        max_value = max(monthly_totals['income'])

        # Create and display vertical progress bars for spending
        for i, (spending_total, month_year) in enumerate(zip(monthly_totals['spending'], reversed(range(5)))):
            # Calculate the month/year for the current iteration
            current_month_year = (datetime.now() - pd.DateOffset(months=month_year)).strftime("%B %Y")

            # Create a label for the month/year
            month_label = tk.Label(self.your_spending_frame, text=current_month_year)
            month_label.grid(row=2, column=i, padx=5, pady=5, sticky='n')

            # Create a progress bar for spending
            progress_bar = ttk.Progressbar(self.your_spending_frame, orient=tk.VERTICAL, length=150, mode='determinate')
            progress_bar.grid(row=0, column=i, padx=5, pady=5, sticky='n')

            # Set the value of the progress bar
            progress_bar['value'] = (spending_total / max_value) * 100

            # Display the spending total as a label below the progress bar
            label = tk.Label(self.your_spending_frame, text=f"{(spending_total / max_value) * 100:.2f}%")
            label.grid(row=1, column=i, padx=5, pady=5, sticky='n')

    def create_wallet_graph(self, frame):
        # Read spending data from avg_spending.csv
        avg_spending = pd.read_csv('avg_spending.csv')

        # Define relevant scopes for income, savings, investments, and spendings
        income_scopes = ["salary", "interest", "dividends"]
        savings_prefix = "31"
        investment_prefix = "41"
        spending_scopes = ["transport", "sport", "rent", "phone", "internet", "hydro", "health",
                           "groceries", "fee", "fashion", "entertainment"]

        # Filter data for the current system year and month
        current_month_year = datetime.now().strftime("%Y/%m")
        current_month_data = avg_spending[avg_spending['Month/Year'] == current_month_year]

        # Sum spending and income based on the defined scopes
        income_total = current_month_data[current_month_data['Transaction Scope'].isin(income_scopes)][
            'Monthly Total'].sum()
        savings_total = current_month_data[current_month_data['Transaction Scope'].str.startswith(savings_prefix)][
            'Monthly Total'].sum()
        investment_total = current_month_data[current_month_data['Transaction Scope'].str.startswith(investment_prefix)][
            'Monthly Total'].sum()
        spending_total = current_month_data[current_month_data['Transaction Scope'].isin(spending_scopes)][
            'Monthly Total'].sum()

        # Create a pie chart
        fig, ax = plt.subplots()
        colors = ['#003f5c', '#7a5195', '#ffa600', '#ef5675']

        labels = ["Income", "Savings", "Investments", "Spendings"]
        values = [income_total, savings_total, investment_total, spending_total]

        ax.pie(values, labels=labels, colors=colors, autopct=lambda p: '{:.1f}%'.format(p), startangle=180)

        # Draw the circle
        centre_circle = plt.Circle((0, 0), 0.50, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        plt.title(f'Wallet Graph - {current_month_year}')

        # Display the pie chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Display the legend
        legend_frame = tk.Frame(frame)
        legend_frame.pack()
        legend_labels = [tk.Label(legend_frame, text=f"{label}: ${value:.2f}", fg=color) for label, value, color in
                         zip(labels, values, colors)]

        for label in legend_labels:
            label.pack(side=tk.LEFT)


