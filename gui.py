import tkinter as tk
from tkinter import ttk, messagebox
from models import FinancialOperation
from storage import save_operation, load_operations
from analysis import calculate_balance
from visualization import plot_income_expense_over_time, plot_expenses_pie, plot_top_expenses
from utils import validate_amount, validate_date, clean_comment, TYPE_MAPPING

TYPE_REVERSE = {v: k for k, v in TYPE_MAPPING.items()}

class FinancePlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Личный финансовый планер")
        self.create_widgets()
        self.update_operations_list()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Сумма:").grid(row=0, column=0)
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Дата (YYYY-MM-DD):").grid(row=1, column=0)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Категория:").grid(row=2, column=0)
        self.category_entry = ttk.Entry(frame)
        self.category_entry.grid(row=2, column=1)

        ttk.Label(frame, text="Тип:").grid(row=3, column=0)
        self.type_combobox = ttk.Combobox(frame, values=list(TYPE_MAPPING.keys()), state="readonly", width=17)
        self.type_combobox.grid(row=3, column=1)
        self.type_combobox.current(0)

        ttk.Label(frame, text="Комментарий:").grid(row=4, column=0)
        self.comment_entry = ttk.Entry(frame)
        self.comment_entry.grid(row=4, column=1)

        add_btn = ttk.Button(frame, text="Добавить", command=self.add_operation)
        add_btn.grid(row=5, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(
            self.root,
            columns=("Дата", "Тип", "Категория", "Сумма", "Комментарий"),
            show="headings"
        )
        for col in ("Дата", "Тип", "Категория", "Сумма", "Комментарий"):
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(padx=10, pady=5)

        ttk.Button(btn_frame, text="Баланс", command=self.show_balance).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="График доход/расход", command=self.plot_income_expense).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Круговая диаграмма расходов", command=self.plot_expenses_pie).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Топ расходов", command=self.plot_top_expenses).grid(row=0, column=3, padx=5)

    def add_operation(self):
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        category = self.category_entry.get()
        type_display = self.type_combobox.get()
        comment = self.comment_entry.get()

        type_internal = TYPE_MAPPING.get(type_display)

        if not validate_amount(amount):
            messagebox.showerror("Ошибка", "Некорректная сумма")
            return
        if not validate_date(date):
            messagebox.showerror("Ошибка", "Некорректная дата")
            return
        if type_internal is None:
            messagebox.showerror("Ошибка", "Выберите тип операции")
            return

        comment = clean_comment(comment)
        operation = FinancialOperation(float(amount), category, date, type_internal, comment)
        save_operation(operation)
        self.update_operations_list()

    def update_operations_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        operations = load_operations()
        for idx, op in enumerate(operations):
            self.tree.insert(
                "",
                "end",
                iid=idx,
                values=(op.date, TYPE_REVERSE.get(op.type, op.type), op.category, op.amount, op.comment)
            )

    def show_balance(self):
        operations = load_operations()
        balance = calculate_balance(operations)
        messagebox.showinfo("Баланс", f"Текущий баланс: {balance:.2f}")

    def plot_income_expense(self):
        operations = load_operations()
        plot_income_expense_over_time(operations)

    def plot_expenses_pie(self):
        operations = load_operations()
        plot_expenses_pie(operations)

    def plot_top_expenses(self):
        operations = load_operations()
        plot_top_expenses(operations)

def run_gui():
    root = tk.Tk()
    app = FinancePlannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()