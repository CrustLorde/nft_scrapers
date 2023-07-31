import requests
import json
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext as st
from tkinter import ttk

import pyperclip
from dateutil.parser import parse


# Function to obtain sales data
def get_nft_sales_data(contract_address):
        url = f'https://api.opensea.io/api/v1/events'
        headers = {
        'Accept': 'application/json',
        'X-API-KEY': 'api_key',
    }
        params = {
        'asset_contract_address': contract_address,
        'event_type': 'successful',
        'only_opensea': 'false',
        'limit': 50,
    }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data. Status code: {response.status_code}, Error: {response.text}")

def format_nft_sales_data(sales_data):
    # Extract relevant information (e.g., NFT names, prices, sale dates, etc.)
    formatted_data = []
    for event in sales_data.get('asset_events', []):
        nft_name = event['asset']['name']
        price = event['total_price']
        sale_date = event['transaction']['timestamp']
        formatted_data.append({
            'NFT Name': nft_name,
            'Price (ETH)': float(price) / 10**18,  # Convert from wei to ETH
            'Sale Date': parse(sale_date, ignoretz=True).strftime('%Y-%m-%d %H:%M:%S')
        })
    return formatted_data

def fetch_sales_data():
    contract_address = contract_address_entry.get()
    api_key = api_key_entry.get() # get api key from the entry widget
    try:
        status_message.set("Fetching data...")
        root.update_idletasks()
        
        sales_data = get_nft_sales_data(contract_address, api_key) # passes APi key tot he function
        formatted_data = format_nft_sales_data(sales_data)
        
        df = pd.DataFrame(formatted_data)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, df.to_string(index=False))
        
        status_message.set("Data fetched successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_message.set("Error occurred while fetching data.")

def clear_result_text():
    result_text.delete(1.0, tk.END)

def copy_to_clipboard():
    data = result_text.get(1.0, tk.END)
    pyperclip.copy(data)

# Create the main window
root = tk.Tk()
root.title("OpenSea NFT Sales Data")

# Use a modern theme for ttk widgets (ttkthemes library required)
style = ttk.Style()
style.theme_use("clam")  # Choose a theme: "clam", "alt", "default", etc.

# Create and place widgets with ttk styling
contract_address_label = ttk.Label(root, text="Contract Address:")
contract_address_label.pack(pady=5)

contract_address_entry = ttk.Entry(root, width=40)
contract_address_entry.pack(pady=5)

api_key_label = ttk.Label(root, text="API Key:")
api_key_label.pack(pady=5)

api_key_entry = ttk.Entry(root, width=40)
api_key_entry.pack(pady=5)

fetch_button = ttk.Button(root, text="Fetch Sales Data", command=fetch_sales_data)
fetch_button.pack(pady=10)

clear_button = ttk.Button(root, text="Clear Results", command=clear_result_text)
clear_button.pack(pady=5)

copy_button = ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=5)

status_message = tk.StringVar()
status_label = ttk.Label(root, textvariable=status_message)
status_label.pack()

result_text = st.ScrolledText(root, width=80, height=20)
result_text.pack()

# Start the GUI event loop
root.mainloop()
