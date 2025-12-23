import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd
from analysis import operations_to_df, expenses_by_category

def plot_income_expense_over_time(operations):
    df = operations_to_df(operations)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    income = df[df.type=="income"].resample("M").sum()["amount"]
    expense = df[df.type=="expense"].resample("M").sum()["amount"]

    plt.figure(figsize=(10,5))
    plt.plot(income.index, income.values, marker="o", label="Доход")
    plt.plot(expense.index, expense.values, marker="o", label="Расход")
    plt.title("Доходы и расходы по месяцам")
    plt.xlabel("Месяц")
    plt.ylabel("Сумма")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show(block=True)

def plot_expenses_pie(operations):
    expenses = expenses_by_category(operations)
    if expenses.empty:
        print("Нет расходов для отображения")
        return

    plt.figure(figsize=(6,6))
    expenses.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Расходы по категориям")
    plt.ylabel("")
    plt.tight_layout()
    plt.show(block=True)

def plot_top_expenses(operations, n=5):
    top_expenses = expenses_by_category(operations).sort_values(ascending=False).head(n)
    if top_expenses.empty:
        print("Нет расходов для отображения")
        return

    plt.figure(figsize=(8,5))
    top_expenses.plot(kind="bar", color="orange")
    plt.title(f"Топ-{n} категорий расходов")
    plt.xlabel("Категория")
    plt.ylabel("Сумма")
    plt.tight_layout()
    plt.show(block=True)