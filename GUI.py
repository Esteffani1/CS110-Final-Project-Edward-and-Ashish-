#This is the Graphical User Interface module for the debt payment application.
#It provides a visual interface for users to interact with the application.
#It allows users to input their debt information, view their progress, and select a payment method.
#Tkinter is used for creating the GUI.

# Tkinter is used for creating the GUI.
import tkinter as tk
from tkinter import messagebox

from Snowball_Method import load_and_sort_debts as load_snowball
from Avalanche_Method import load_and_sort_debts as load_avalanche
from Debt_Calculator import simulate_debt_payoff


def run_calculation():
    try:
        monthly_budget = float(budget_entry.get())

        if monthly_budget <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Monthly budget must be greater than 0."
            )
            return

        method = method_var.get()

        if method == "Snowball":
            debts = load_snowball()
        else:
            debts = load_avalanche()

        months, total_interest = simulate_debt_payoff(
            debts,
            monthly_budget
        )

        years = months // 12
        remaining_months = months % 12

        total_debt = sum(debt.balance for debt in debts)
        total_paid = total_debt + total_interest

        result_text.delete("1.0", tk.END)

        result_text.insert(
            tk.END,
            f"Method: {method}\n\n"
        )

        result_text.insert(
            tk.END,
            f"Total Debt: ${total_debt:.2f}\n"
        )

        result_text.insert(
            tk.END,
            f"Monthly Budget: ${monthly_budget:.2f}\n\n"
        )

        result_text.insert(
            tk.END,
            f"Months to Pay Off: {months}\n"
        )

        result_text.insert(
            tk.END,
            f"Time: {years} years and {remaining_months} months\n"
        )

        result_text.insert(
            tk.END,
            f"Total Interest Paid: ${total_interest:.2f}\n"
        )

        result_text.insert(
            tk.END,
            f"Total Amount Paid: ${total_paid:.2f}\n"
        )

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter a valid budget amount."
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e))


# Main Window
root = tk.Tk()
root.title("Debt Payoff Calculator")
root.geometry("600x500")

title_label = tk.Label(
    root,
    text="Debt Payoff Calculator",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)

# Method Selection
method_var = tk.StringVar()
method_var.set("Snowball")

tk.Label(
    root,
    text="Choose Method:"
).pack()

tk.Radiobutton(
    root,
    text="Snowball Method",
    variable=method_var,
    value="Snowball"
).pack()

tk.Radiobutton(
    root,
    text="Avalanche Method",
    variable=method_var,
    value="Avalanche"
).pack()

# Budget Entry
tk.Label(
    root,
    text="Monthly Budget ($):"
).pack(pady=5)

budget_entry = tk.Entry(root)
budget_entry.pack()

# Calculate Button
calculate_button = tk.Button(
    root,
    text="Calculate",
    command=run_calculation
)
calculate_button.pack(pady=10)

# Results Box
result_text = tk.Text(
    root,
    height=15,
    width=60
)
result_text.pack(pady=10)

root.mainloop()