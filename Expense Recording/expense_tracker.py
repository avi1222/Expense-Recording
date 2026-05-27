import json
from datetime import datetime

FILE_NAME = "expenses.json"

categories = ["Groceries", "Transportation", "Utilities", "Entertainment"]


# ---------------- File Handling ---------------- #

def load_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------------- Add Expense ---------------- #

def add_expense(expenses):
    try:
        amount = float(input("Enter amount spent: ₹"))

        description = input("Enter description: ")

        print("\nAvailable Categories:")
        for i, cat in enumerate(categories, start=1):
            print(f"{i}. {cat}")

        print(f"{len(categories)+1}. Add New Category")

        choice = int(input("Choose category: "))

        if choice == len(categories) + 1:
            new_category = input("Enter new category name: ")
            categories.append(new_category)
            category = new_category
        else:
            category = categories[choice - 1]

        date = input("Enter date (YYYY-MM-DD): ")

        expense = {
            "amount": amount,
            "description": description,
            "category": category,
            "date": date
        }

        expenses.append(expense)

        save_expenses(expenses)

        print("\nExpense added successfully!")

    except ValueError:
        print("Invalid input! Please enter correct values.")


# ---------------- View Expenses ---------------- #

def view_expenses(expenses):

    if not expenses:
        print("\nNo expenses recorded.")
        return

    print("\nExpense Records")
    print("-" * 60)

    for exp in expenses:
        print(
            f"₹{exp['amount']} | "
            f"{exp['category']} | "
            f"{exp['description']} | "
            f"{exp['date']}"
        )


# ---------------- Summary ---------------- #

def expense_summary(expenses):

    if not expenses:
        print("\nNo expenses available.")
        return

    total = 0
    category_totals = {}

    for exp in expenses:

        total += exp["amount"]

        cat = exp["category"]

        if cat in category_totals:
            category_totals[cat] += exp["amount"]
        else:
            category_totals[cat] = exp["amount"]

    print("\nExpense Summary")
    print("-" * 30)

    print(f"Total Spending: ₹{total:.2f}")

    print("\nCategory Breakdown:")

    for cat, amount in category_totals.items():
        print(f"{cat}: ₹{amount:.2f}")


# ---------------- Filter by Period ---------------- #

def view_by_period(expenses):

    if not expenses:
        print("\nNo expenses available.")
        return

    period = input(
        "\nView expenses by (daily/weekly/monthly): "
    ).lower()

    date_input = input(
        "Enter reference date (YYYY-MM-DD): "
    )

    try:
        ref_date = datetime.strptime(
            date_input,
            "%Y-%m-%d"
        )

        print("\nMatching Expenses")
        print("-" * 40)

        for exp in expenses:

            exp_date = datetime.strptime(
                exp["date"],
                "%Y-%m-%d"
            )

            if period == "daily":

                if exp_date.date() == ref_date.date():
                    print(exp)

            elif period == "weekly":

                if (
                    exp_date.isocalendar()[1]
                    ==
                    ref_date.isocalendar()[1]
                ):
                    print(exp)

            elif period == "monthly":

                if (
                    exp_date.month == ref_date.month
                    and
                    exp_date.year == ref_date.year
                ):
                    print(exp)

    except ValueError:
        print("Invalid date format.")


# ---------------- Main Menu ---------------- #

def main():

    expenses = load_expenses()

    while True:

        print("\n===== Expense Recording System =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Expense Summary")
        print("4. View By Period")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            expense_summary(expenses)

        elif choice == "4":
            view_by_period(expenses)

        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()