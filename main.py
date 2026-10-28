import math
from datetime import date, datetime

import storage
import expenses


# ---------- Input helpers: keep asking until the answer is valid ----------

def ask_amount():
    while True:
        text = input("Amount: ").strip()
        try:
            amount = float(text)
        except ValueError:
            print("  Please enter a number, like 12.50")
            continue
        if not math.isfinite(amount) or amount <= 0:
            print("  Amount must be a number greater than zero.")
            continue
        return round(amount, 2)


def ask_category():
    while True:
        text = input("Category (e.g. Food, Transport, Rent): ").strip()
        if text:
            return text.title()  # "food" becomes "Food"
        print("  Category cannot be empty.")


def ask_date():
    while True:
        text = input("Date (YYYY-MM-DD, or press Enter for today): ").strip()
        if text == "":
            return date.today().isoformat()
        try:
            parsed = datetime.strptime(text, "%Y-%m-%d")
            return parsed.date().isoformat()
        except ValueError:
            print("  Please use the format YYYY-MM-DD, like 2026-10-28")


def ask_description():
    return input("Description (optional): ").strip()


def ask_optional_date(prompt):
    """Like ask_date, but pressing Enter means 'skip this filter'."""
    while True:
        text = input(prompt).strip()
        if text == "":
            return ""
        try:
            parsed = datetime.strptime(text, "%Y-%m-%d")
            return parsed.date().isoformat()
        except ValueError:
            print("  Please use the format YYYY-MM-DD, like 2026-10-28")


def ask_optional_month(prompt):
    """Ask for a month like 2026-10. Pressing Enter returns '' (go back)."""
    while True:
        text = input(prompt).strip()
        if text == "":
            return ""
        try:
            parsed = datetime.strptime(text, "%Y-%m")
            return parsed.strftime("%Y-%m")
        except ValueError:
            print("  Please use the format YYYY-MM, like 2026-10")


def ask_expense_number(maximum):
    """Ask for a number from 1 to maximum. Enter returns None (cancel)."""
    while True:
        text = input("\nNumber of the expense to delete (Enter to cancel): ").strip()
        if text == "":
            return None
        try:
            number = int(text)
        except ValueError:
            print(f"  Please type a whole number from 1 to {maximum}.")
            continue
        if 1 <= number <= maximum:
            return number
        print(f"  Please type a number from 1 to {maximum}.")


# ---------- Menu actions ----------

def add_expense_flow(all_expenses):
    print("\n--- Add a new expense ---")
    amount = ask_amount()
    category = ask_category()
    when = ask_date()
    description = ask_description()

    all_expenses.append(expenses.make_expense(amount, category, when, description))
    storage.save_expenses(all_expenses)
    print("Expense saved!")


def search_flow(all_expenses):
    print("\n--- Search / filter (press Enter to skip any filter) ---")
    category = input("Category: ").strip()
    keyword = input("Word in description: ").strip()
    start = ask_optional_date("From date (YYYY-MM-DD): ")
    end = ask_optional_date("To date (YYYY-MM-DD): ")

    if start and end and start > end:
        print("  The 'from' date is after the 'to' date. Nothing can match that.")
        return

    results = expenses.filter_expenses(all_expenses, category, keyword, start, end)

    if not results:
        print("\nNo expenses match your filters.")
        return

    expenses.show_expenses(results)
    print(f"Total of these expenses: {expenses.calculate_total(results):.2f}")


def monthly_flow(all_expenses):
    print("\n--- Monthly summary ---")
    expenses.show_monthly_overview(all_expenses)
    if not all_expenses:
        return

    month = ask_optional_month("\nType a month (YYYY-MM) for details, or press Enter to go back: ")
    if month:
        expenses.show_month_detail(all_expenses, month)


def delete_flow(all_expenses):
    print("\n--- Delete an expense ---")
    if not all_expenses:
        print("No expenses to delete.")
        return

    expenses.show_expenses(all_expenses)
    ordered = expenses.sorted_expenses(all_expenses)  # same order as the table

    number = ask_expense_number(len(ordered))
    if number is None:
        print("Cancelled. Nothing was deleted.")
        return

    chosen = ordered[number - 1]
    question = (
        f"Delete {chosen['date']} | {chosen['category']} | "
        f"{chosen['amount']:.2f} | {chosen['description']}? (y/n): "
    )
    if input(question).strip().lower() == "y":
        all_expenses.remove(chosen)
        storage.save_expenses(all_expenses)
        print("Expense deleted.")
    else:
        print("Cancelled. Nothing was deleted.")


def main():
    all_expenses = storage.load_expenses()
    print(f"Welcome to Fenet's Expense Tracker. {len(all_expenses)} expense(s) loaded.")

    while True:
        print("\n==== MENU ====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View totals")
        print("4. Search / filter")
        print("5. Monthly summary")
        print("6. Delete expense")
        print("7. Quit")
        choice = input("Choose 1-7: ").strip()

        if choice == "1":
            add_expense_flow(all_expenses)
        elif choice == "2":
            expenses.show_expenses(all_expenses)
        elif choice == "3":
            expenses.show_totals(all_expenses)
        elif choice == "4":
            search_flow(all_expenses)
        elif choice == "5":
            monthly_flow(all_expenses)
        elif choice == "6":
            delete_flow(all_expenses)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Please type a number from 1 to 7.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")