#This is the Graphical User Interface module for the debt payment application.
#It provides a visual interface for users to interact with the application.
#It allows users to input their debt information, view their progress, and select a payment method.
#Tkinter is used for creating the GUI.

# Tkinter is used for creating the GUI.
# This is the Graphical User Interface module for the debt payment application.

import tkinter as tk
from tkinter import messagebox

from Debt_Entry import DebtEntry, write_debt_entries_to_file
from Debt_Calculator import simulate_debt_payoff

# Store debts entered through the GUI
debts = []


def add_debt():
    """Add a debt to the list from the entry fields."""
    try:
        name = name_entry.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Please enter a debt name.")
            return

        balance = float(balance_entry.get())
        interest = float(interest_entry.get())
        minimum = float(minimum_entry.get())

        # Convert percentage to decimal if needed
        if interest > 1:
            interest = interest / 100

        debt = DebtEntry(
            name,
            balance,
            interest,
            minimum
        )

        debts.append(debt)

        debt_listbox.insert(
            tk.END,
            f"{name} | Balance: ${balance:.2f} | Interest: {interest*100:.1f}% | Min: ${minimum:.2f}"
        )

        # Clear entry fields
        name_entry.delete(0, tk.END)
        balance_entry.delete(0, tk.END)
        interest_entry.delete(0, tk.END)
        minimum_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numeric values for balance, interest rate, and minimum payment."
        )


def clear_all_debts():
    """Clear all debts from the list."""
    global debts
    if messagebox.askyesno("Clear All", "Are you sure you want to clear all debts?"):
        debts = []
        debt_listbox.delete(0, tk.END)


def run_calculation():
    """Calculate debt payoff using the selected method."""
    try:
        if len(debts) == 0:
            messagebox.showerror(
                "No Debts",
                "Please add at least one debt."
            )
            return

        monthly_budget = float(budget_entry.get())

        if monthly_budget <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Monthly budget must be greater than 0."
            )
            return

        method = method_var.get()

        # Sort debts directly from the list - NO FILE READING!
        if method == "Snowball":
            sorted_debts = sorted(debts, key=lambda d: d.balance)
            method_name = "Snowball (Smallest Balance First)"
        else:
            sorted_debts = sorted(debts, key=lambda d: d.interest_rate, reverse=True)
            method_name = "Avalanche (Highest Interest First)"

        # Optional: Save to file for persistence
        write_debt_entries_to_file(sorted_debts)

        # Calculate using the sorted debts
        months, total_interest = simulate_debt_payoff(
            sorted_debts,
            monthly_budget
        )

        years = months // 12
        remaining_months = months % 12

        total_debt = sum(debt.balance for debt in sorted_debts)
        total_paid = total_debt + total_interest

        # Display results
        result_text.delete("1.0", tk.END)

        result_text.insert(tk.END, "=" * 60 + "\n")
        result_text.insert(tk.END, "                 DEBT PAYOFF RESULTS\n")
        result_text.insert(tk.END, "=" * 60 + "\n\n")

        result_text.insert(tk.END, f"📊 Method: {method_name}\n\n")

        result_text.insert(tk.END, f"💰 Total Debt: ${total_debt:,.2f}\n")
        result_text.insert(tk.END, f"💵 Monthly Budget: ${monthly_budget:,.2f}\n\n")

        result_text.insert(tk.END, f"⏰ Months to Pay Off: {months}\n")
        result_text.insert(tk.END, f"📅 Time Required: {years} years and {remaining_months} months\n\n")

        result_text.insert(tk.END, f"💸 Total Interest Paid: ${total_interest:,.2f}\n")
        result_text.insert(tk.END, f"🏦 Total Amount Paid: ${total_paid:,.2f}\n")

        result_text.insert(tk.END, "\n" + "=" * 60 + "\n")

        # Show debt breakdown
        result_text.insert(tk.END, "\n📋 DEBT BREAKDOWN (in payoff order):\n")
        result_text.insert(tk.END, "-" * 60 + "\n")
        for i, debt in enumerate(sorted_debts, 1):
            result_text.insert(
                tk.END,
                f"  {i}. {debt.name}: ${debt.balance:,.2f} @ {debt.interest_rate*100:.1f}%\n"
            )

        # Show monthly payment allocation
        result_text.insert(tk.END, "\n" + "-" * 60 + "\n")
        result_text.insert(tk.END, "📈 Summary:\n")
        result_text.insert(tk.END, f"  • Number of debts: {len(sorted_debts)}\n")
        result_text.insert(tk.END, f"  • Average interest rate: {sum(d.interest_rate for d in sorted_debts)/len(sorted_debts)*100:.1f}%\n")

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter a valid monthly budget."
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"An error occurred: {str(e)}"
        )


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Debt Payoff Calculator")
root.geometry("850x950")  # 👈 BIGGER WINDOW
root.resizable(True, True)
root.option_add('*tearOff', False)  # Remove the "M" menu indicator

# ---------------- HEADER ----------------

title_label = tk.Label(
    root,
    text="💰 Debt Payoff Calculator",
    font=("Arial", 22, "bold"),
    fg="#2c3e50"
)
title_label.pack(pady=15)

# ---------------- DEBT ENTRY SECTION ----------------

entry_frame = tk.Frame(root, bg="#ecf0f1", relief=tk.GROOVE, bd=2)
entry_frame.pack(pady=10, padx=20, fill=tk.X)

tk.Label(
    entry_frame,
    text="ADD NEW DEBT",
    font=("Arial", 13, "bold"),
    bg="#ecf0f1"
).pack(pady=5)

input_frame = tk.Frame(entry_frame, bg="#ecf0f1")
input_frame.pack(pady=5)

# Row 1: Name
tk.Label(input_frame, text="Debt Name:", bg="#ecf0f1", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=3, sticky="e")
name_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
name_entry.grid(row=0, column=1, padx=5, pady=3)

# Row 2: Balance
tk.Label(input_frame, text="Balance ($):", bg="#ecf0f1", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=3, sticky="e")
balance_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
balance_entry.grid(row=1, column=1, padx=5, pady=3)

# Row 3: Interest Rate
tk.Label(input_frame, text="Interest Rate (%):", bg="#ecf0f1", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=3, sticky="e")
interest_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
interest_entry.grid(row=2, column=1, padx=5, pady=3)

# Row 4: Minimum Payment
tk.Label(input_frame, text="Minimum Payment ($):", bg="#ecf0f1", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=3, sticky="e")
minimum_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
minimum_entry.grid(row=3, column=1, padx=5, pady=3)

# Buttons
button_frame = tk.Frame(entry_frame, bg="#ecf0f1")
button_frame.pack(pady=10)

add_button = tk.Button(
    button_frame,
    text="➕ Add Debt",
    command=add_debt,
    bg="#2ecc71",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=25,
    pady=5
)
add_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(
    button_frame,
    text="🗑️ Clear All",
    command=clear_all_debts,
    bg="#e74c3c",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=25,
    pady=5
)
clear_button.pack(side=tk.LEFT, padx=5)

# ---------------- DEBT LIST SECTION ----------------

tk.Label(
    root,
    text="📋 Your Debts",
    font=("Arial", 13, "bold")
).pack(pady=5)

debt_listbox = tk.Listbox(
    root,
    width=80,  # 👈 WIDER
    height=6,
    font=("Courier", 10)
)
debt_listbox.pack(pady=5, padx=20, fill=tk.X)

# ---------------- METHOD SELECTION ----------------

method_frame = tk.Frame(root)
method_frame.pack(pady=10)

tk.Label(
    method_frame,
    text="Choose Payment Method",
    font=("Arial", 13, "bold")
).pack()

method_var = tk.StringVar()
method_var.set("Snowball")

snowball_radio = tk.Radiobutton(
    method_frame,
    text="❄️ Snowball Method (Smallest Balance First)",
    variable=method_var,
    value="Snowball",
    font=("Arial", 11)
)
snowball_radio.pack(anchor=tk.W, padx=50)

avalanche_radio = tk.Radiobutton(
    method_frame,
    text="🏔️ Avalanche Method (Highest Interest First)",
    variable=method_var,
    value="Avalanche",
    font=("Arial", 11)
)
avalanche_radio.pack(anchor=tk.W, padx=50)

# ---------------- MONTHLY BUDGET ----------------

budget_frame = tk.Frame(root)
budget_frame.pack(pady=10)

tk.Label(
    budget_frame,
    text="Monthly Budget ($):",
    font=("Arial", 12, "bold")
).pack(side=tk.LEFT, padx=5)

budget_entry = tk.Entry(budget_frame, width=15, font=("Arial", 12))
budget_entry.pack(side=tk.LEFT, padx=5)
budget_entry.insert(0, "500")  # Default value

# ---------------- CALCULATE BUTTON ----------------

calculate_button = tk.Button(
    root,
    text="🚀 Calculate",
    command=run_calculation,
    bg="#3498db",
    fg="white",
    font=("Arial", 14, "bold"),
    padx=50,
    pady=12
)
calculate_button.pack(pady=15)

# ---------------- RESULTS AREA ----------------

result_frame = tk.Frame(root)
result_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

tk.Label(
    result_frame,
    text="📊 Results",
    font=("Arial", 13, "bold")
).pack(anchor=tk.W)

# 👇 BIGGER RESULT TEXT BOX - 22 lines tall and 90 chars wide
result_text = tk.Text(
    result_frame,
    width=90,      # 👈 WIDER
    height=22,     # 👈 TALLER (was 15)
    font=("Courier", 11),  # 👈 BIGGER FONT (was 10)
    relief=tk.GROOVE,
    bd=2
)
result_text.pack(pady=5, fill=tk.BOTH, expand=True)

# Add a scrollbar for the results
scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# ---------------- FOOTER ----------------

footer_label = tk.Label(
    root,
    text="Debt Payoff Calculator v1.0 | Snowball & Avalanche Methods",
    font=("Arial", 9),
    fg="#7f8c8d"
)
footer_label.pack(pady=5)

# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    root.mainloop()