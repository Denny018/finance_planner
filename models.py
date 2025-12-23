from datetime import datetime

class FinancialOperation:
    def __init__(self, amount, category, date, type_, comment=""):
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля")
        self.amount = float(amount)
        self.category = category.strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Дата должна быть в формате YYYY-MM-DD")
        self.date = date
        if type_ not in ("income", "expense"):
            raise ValueError("Тип должен быть 'income' или 'expense'")
        self.type = type_
        self.comment = comment.strip()

    def __str__(self):
        return f"{self.date} | {self.type} | {self.category} | {self.amount} | {self.comment}"

    def to_dict(self):
        return {
            "date": self.date,
            "type": self.type,
            "category": self.category,
            "amount": self.amount,
            "comment": self.comment
        }

class Category:

    def __init__(self, name, type_):
        self.name = name.strip()
        if type_ not in ("income", "expense"):
            raise ValueError("Тип категории должен быть 'income' или 'expense'")
        self.type = type_

    def __str__(self):
        return f"{self.name} ({self.type})"