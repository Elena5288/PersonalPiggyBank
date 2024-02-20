import numpy as np
import pandas as pd


def calculate_monthly_totals():
    # Load user_info.csv, account_info.csv, and cashflow.csv into DataFrames
    user_info = pd.read_csv('user_info.csv')
    account_info = pd.read_csv('account_info.csv')
    cashflow = pd.read_csv('cashflow.csv')

    # Remove extra slashes from the 'Transaction Date' column
    cashflow['Transaction Date'] = cashflow['Transaction Date'].str.strip('/')

    # Convert 'Transaction Date' to datetime with format='%m/%d/%Y'
    cashflow['Transaction Date'] = pd.to_datetime(cashflow['Transaction Date'], format='%m/%d/%Y')

    # Merge DataFrames to get a single DataFrame with relevant information
    merged_data = pd.merge(user_info, account_info, on='ID', how='left')
    merged_data = pd.merge(merged_data, cashflow, on=['ID', 'Account Number'])

    # Convert 'Transaction Date' to 'yyyy/m' format
    merged_data['Month/Year'] = merged_data['Transaction Date'].dt.strftime('%Y/%m')

    # Map 'Money in/out' to 'deposit', 'withdrawal', and 'spending'
    merged_data['Money in/out'] = merged_data['Money in/out'].map({'in': 'deposit', 'out': 'withdrawal'})

    # Calculate monthly totals based on 'Money in/out'
    merged_data['Total'] = np.where(merged_data['Money in/out'].isin(['deposit']), merged_data['Transaction Amount'],
                                    -merged_data['Transaction Amount'])

    # Group by user_id, account_number, and month/year and sum the totals
    monthly_totals = merged_data.groupby(['ID', 'Account Number', 'Month/Year'])['Total'].sum().reset_index()

    # Sort by ID, Account Number, and Month/Year for calculating prior month total
    monthly_totals = monthly_totals.sort_values(['ID', 'Account Number', 'Month/Year'])

    # Calculate the prior month total and add it to the current month total
    monthly_totals['Prior Month Total'] = monthly_totals.groupby(['ID', 'Account Number'])['Total'].shift(fill_value=0)

    # Iterate through months to accumulate totals
    for i in range(1, len(monthly_totals)):
        monthly_totals.loc[i, 'Total'] += monthly_totals.loc[i - 1, 'Total']

    # Save the result to account_monthly_totals.csv
    monthly_totals.to_csv('account_monthly_totals.csv', index=False)


