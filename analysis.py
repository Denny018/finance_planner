import pandas as pd
from models import FinancialOperation
from datetime import datetime

def operations_to_df(operations):
    data = [op.to_dict() for op in operations]
    df = pd.DataFrame(data)
    df["amount"] = df["amount"].astype(float)
    df["date"] = pd.to_datetime(df["date"])
    return df

def calculate_balance(operations):
    df = operations_to_df(operations)
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    return income - expense

def expenses_by_category(operations):
    df = operations_to_df(operations)
    expenses = df[df["type"] == "expense"]
    result = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)
    return result

def income_expense_by_period(operations, start_date, end_date):
    df = operations_to_df(operations)
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    df_period = df[(df["date"] >= start) & (df["date"] <= end)]
    income = df_period[df_period["type"] == "income"]["amount"].sum()
    expense = df_period[df_period["type"] == "expense"]["amount"].sum()
    return income, expense

def top_expense_categories(operations, n=5):
    expenses = expenses_by_category(operations)
    return expenses.head(n)