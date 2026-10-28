from datetime import datetime


def make_expense(amount, category, date, description):
    """Bundle the details of one expense into a dictionary."""
    return {
        "amount": amount,
        "category": category,
        "date": date,
        "description": description,
    }


def sorted_expenses(expenses):
    """Return the expenses oldest first. The table numbers and delete both use this."""
    return sorted(expenses, key=lambda e: e["date"])


def show_expenses(expenses):
    """Print all expenses as a neat table, oldest first."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    ordered = sorted_expenses(expenses)

    print(f"\n{'#':<4}{'Date':<12}{'Category':<15}{'Amount':>10}  Description")
    print("-" * 60)
    for number, e in enumerate(ordered, start=1):
        print(
            f"{number:<4}{e['date']:<12}{e['category']:<15}"
            f"{e['amount']:>10.2f}  {e['description']}"
        )
    print(f"\n{len(ordered)} expense(s) shown.")


def calculate_total(expenses):
    """Add up the amount of every expense."""
    return sum(e["amount"] for e in expenses)


def totals_by_category(expenses):
    """Return a dictionary like {"Food": 45.5, "Rent": 6000.0}."""
    totals = {}
    for e in expenses:
        category = e["category"]
        totals[category] = totals.get(category, 0) + e["amount"]
    return totals


def show_totals(expenses):
    """Print the grand total and the spending per category."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    grand_total = calculate_total(expenses)
    by_category = totals_by_category(expenses)

    print(f"\nTotal spending: {grand_total:.2f}")
    print(f"\n{'Category':<15}{'Amount':>12}{'Share':>9}")
    print("-" * 36)

    # Biggest spending first
    for category, amount in sorted(by_category.items(), key=lambda item: item[1], reverse=True):
        share = amount / grand_total * 100
        print(f"{category:<15}{amount:>12.2f}{share:>8.1f}%")


def filter_expenses(expenses, category="", keyword="", start_date="", end_date=""):
    """Return only the expenses that match every filter that was filled in.

    An empty filter ("") means "don't filter on this".
    """
    results = []
    for e in expenses:
        if category and e["category"].lower() != category.lower():
            continue
        if keyword and keyword.lower() not in e["description"].lower():
            continue
        if start_date and e["date"] < start_date:
            continue
        if end_date and e["date"] > end_date:
            continue
        results.append(e)
    return results


def expenses_in_month(expenses, month):
    """Return the expenses whose date starts with a month like '2026-10'."""
    return [e for e in expenses if e["date"].startswith(month)]


def month_label(month):
    """Turn '2026-10' into 'October 2026'."""
    return datetime.strptime(month, "%Y-%m").strftime("%B %Y")


def show_monthly_overview(expenses):
    """Print one line per month: count, total, change vs previous month, top category."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    # Collect every month that appears in the data, e.g. {"2026-09", "2026-10"}
    months = sorted({e["date"][:7] for e in expenses})

    print(f"\n{'Month':<18}{'Count':>6}{'Total':>12}{'Change':>10}  Top category")
    print("-" * 62)

    previous_total = None  # "nothing yet": the first month has no previous month

    for month in months:
        month_expenses = expenses_in_month(expenses, month)
        by_category = totals_by_category(month_expenses)
        top_category = max(by_category, key=by_category.get)
        total = calculate_total(month_expenses)

        if previous_total is None:
            change_text = "-"
        else:
            change = (total - previous_total) / previous_total * 100
            change_text = f"{change:+.1f}%"

        print(
            f"{month_label(month):<18}{len(month_expenses):>6}"
            f"{total:>12.2f}{change_text:>10}  {top_category}"
        )

        previous_total = total  # remember this month for the next loop round


def show_month_detail(expenses, month):
    """Print the category breakdown for one month."""
    month_expenses = expenses_in_month(expenses, month)
    if not month_expenses:
        print(f"\nNo expenses found for {month_label(month)}.")
        return

    print(f"\n=== {month_label(month)} ===")
    show_totals(month_expenses)