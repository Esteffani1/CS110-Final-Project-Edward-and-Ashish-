#This is the Debt Entry module for the debt payment application.
#It allows users to input and manage their debt information.

class DebtEntry:
    def __init__(self, name, amount, interest_rate, minimum_payment):
        self.name = name
        self.amount = amount
        self.interest_rate = interest_rate
        self.minimum_payment = minimum_payment

Debt_List.txt = []

with open("Debt_List.txt", "r") as f:
    for line in f:
        name, amount, interest_rate, minimum_payment = line.strip().split(",")
        Debt_List.append(('\n',name, float(amount), float(interest_rate), float(minimum_payment)))
