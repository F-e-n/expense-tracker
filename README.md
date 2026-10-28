# Expense Tracker

A simple command-line app for tracking personal spending, built with Python.
It uses only Python's built-in features and stores data in a JSON file.

## Features

- Add expenses (amount, category, date, description) with input validation
- Data is saved automatically and persists between runs
- View all expenses in a table
- Totals and spending by category
- Search and filter by category, keyword and date range
- Monthly summary with change from the previous month
- Delete expenses with confirmation

## How to run

1. Install Python 3.10 or newer.
2. Download or clone this project.
3. In a terminal, inside the project folder, run:

```
python main.py
```

Your expenses are saved in `data/expenses.json`, which is created automatically.

## Project structure

- `main.py`: the menu and user input
- `expenses.py`: calculations, filtering and summaries
- `storage.py`: loading and saving the JSON file

## What I learned

Built step by step with AI assistance as a way to learn Python, Git and
project structure.