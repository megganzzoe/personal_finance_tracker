import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict

FILE_NAME = "transactions.csv"
budgets = {}  # key: category, value: limit (float)


# Creating the csv
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Amount", "Category", "Date"])

# functions to add the transactions
def add_transaction(trans_type):
    amount = simpledialog.askfloat(f"Add {trans_type}", "Enter amount:")
    category = simpledialog.askstring(f"Add {trans_type}", "Enter category:")
    date = simpledialog.askstring(f"Add {trans_type}", "Enter date (YYYY-MM-DD):")

    if not all([amount, category, date]):
        messagebox.showerror("Error", "All fields are required!")
        return

    with open(FILE_NAME, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([trans_type, amount, category, date])

    messagebox.showinfo("Success", f"{trans_type} added successfully!")
        # Check budget if it's an expense
    if trans_type == "Expense" and category in budgets:
        total = 0
        with open(FILE_NAME, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Type"] == "Expense" and row["Category"] == category:
                    total += float(row["Amount"])
        if total > budgets[category]:
            messagebox.showwarning("🚨 Budget Exceeded",
                                   f"You've exceeded the ₹{budgets[category]} budget for '{category}'!\nCurrent: ₹{total}")


# functions to view the summary
def view_summary():
    income = expense = 0
    with open(FILE_NAME, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            amt = float(row["Amount"])
            if row["Type"] == "Income":
                income += amt
            else:
                expense += amt
    balance = income - expense
    messagebox.showinfo("📊 Financial Summary",
                        f"💸 Total Income: ₹{income}\n🧾 Total Expenses: ₹{expense}\n💰 Balance: ₹{balance}")

def set_budget():
    category = simpledialog.askstring("Set Budget", "Enter category name:")
    limit = simpledialog.askfloat("Set Budget", "Enter limit amount:")

    if not category or not limit:
        messagebox.showerror("Error", "Both fields are required.")
        return

    budgets[category] = limit
    messagebox.showinfo("Budget Set", f"✅ Budget for '{category}' set to ₹{limit}")

# graphical reports
import numpy as np  # make sure this is at the top

def view_category_report():
    category_totals = defaultdict(float)

    with open(FILE_NAME, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Type"] == "Expense":
                category_totals[row["Category"]] += float(row["Amount"])

    if not category_totals:
        messagebox.showinfo("No Data", "No expense data to display.")
        return

    categories = list(category_totals.keys())
    values = list(category_totals.values())

   
    soft_blue_palette = [
        "#7da0ca",  # Muted light blue
        "#a2b9e0",  # Baby blue
        "#bcd4f2",  # Very light blue
        "#9aafd5",  # Steel blue
        "#d2e3f3",  # Ice blue
        "#c4c8e2",  # Soft periwinkle
        "#a5b3d1",  # Dusty lavender
        "#8fa9ce"   # Denim tone
    ]

    
    colors = soft_blue_palette[:len(categories)]

    
    fig, ax = plt.subplots(figsize=(6, 6), facecolor="#050f36")
    wedges, texts, autotexts = ax.pie(
        values,
        labels=categories,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'color': '#f1f1f1'}
    )

    ax.set_title("🧾 Expenses by Category", fontsize=14, color="#f1f1f1")
    ax.axis('equal')  # Circle
    plt.tight_layout()
    plt.show()


# GUI 
app = tk.Tk()
app.title("💼 Finance Tracker")
app.geometry("520x500")
app.configure(bg="#050f36")  # Dark blue background

# Fonts
HEADER_FONT = ("Candara", 22, "bold")
BTN_FONT = ("Century Gothic", 12)

# Style for ttk buttons
style = ttk.Style(app)
style.theme_use("clam")
style.configure("TButton",
                background="#1e3d59",  # Midnight blue
                foreground="#f1f1f1",  # Off-white
                font=BTN_FONT,
                padding=10,
                relief="flat")
style.map("TButton",
          background=[("active", "#468faf")])  # Electric blue on hover

# Title
title = tk.Label(app,
                 text="Personal Finance Tracker",
                 font=HEADER_FONT,
                 bg="#050f36",
                 fg="#f1f1f1")
title.pack(pady=30)

# Button Frame
btn_frame = tk.Frame(app, bg="#050f36")
btn_frame.pack()

# Buttons
ttk.Button(btn_frame, text="➕ Add Income", width=25,
           command=lambda: add_transaction("Income")).pack(pady=10)

ttk.Button(btn_frame, text="➖ Add Expense", width=25,
           command=lambda: add_transaction("Expense")).pack(pady=10)

ttk.Button(btn_frame, text="🎯 Set Budget", width=25,
           command=set_budget).pack(pady=10)

ttk.Button(btn_frame, text="📈 View Summary", width=25,
           command=view_summary).pack(pady=10)

ttk.Button(btn_frame, text="💡 Category Report", width=25,
           command=view_category_report).pack(pady=10)

ttk.Button(btn_frame, text="❌ Exit", width=25,
           command=app.destroy).pack(pady=15)



app.mainloop()
