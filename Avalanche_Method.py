#This is the Avalanche method for paying off debt.
#The method involves paying the minimum amount on all debts except the one with the highest interest rate,
#which is paid off as quickly as possible before moving on to the next highest interest rate debt.
from Debt_Entry import DebtEntry, write_debt_entries_to_file


def read_debt_entries_from_file(path="Debt_List.txt"):
    """Read DebtEntry objects from Debt_List.txt."""
    entries = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 4:
                raise ValueError(f"Invalid line in debt list: {line}")
            name, balance, interest_rate, minimum_payment = parts
            entries.append(
                DebtEntry(
                    name.strip(),
                    float(balance),
                    float(interest_rate),
                    float(minimum_payment),
                )
            )
    return entries

def get_interest_rate(entry):
    return entry.interest_rate

def sort_debt_entries_by_interest(entries):
    """Return a new list sorted from largest interest rate to smallest."""
    return sorted(entries, key=get_interest_rate, reverse=True)


def load_and_sort_debts(path="Debt_List.txt"):
    debts = read_debt_entries_from_file(path)
    sorted_debts = sort_debt_entries_by_interest(debts)
    write_debt_entries_to_file(sorted_debts)
    return sorted_debts


if __name__ == "__main__":
    sorted_debts = load_and_sort_debts()
    print("Debts sorted by interest rate (largest to smallest):")
    for debt in sorted_debts:
        print(f"{debt.name}: ${debt.balance:.2f} | Interest: {debt.interest_rate:.2%} | Minimum: ${debt.minimum_payment:.2f}")
    print(f"\nSaved sorted debt list to: Debt_List.txt")