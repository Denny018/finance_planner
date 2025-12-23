import csv
import os
from models import FinancialOperation

CSV_FILE = "data/operations.csv"
FIELDNAMES = ["date", "type", "category", "amount", "comment"]

def save_operation(operation):
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    try:
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            writer.writerow(operation.to_dict())
    except Exception as e:
        print(f"Ошибка при сохранении операции: {e}")

def load_operations():
    operations = []
    if not os.path.isfile(CSV_FILE):
        return operations
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    op = FinancialOperation(
                        amount=float(row["amount"]),
                        category=row["category"],
                        date=row["date"],
                        type_=row["type"],
                        comment=row["comment"]
                    )
                    operations.append(op)
                except Exception as e:
                    print(f"Ошибка при чтении строки: {row} | {e}")
    except Exception as e:
        print(f"Ошибка при загрузке операций: {e}")
    return operations

def delete_operation(index):
    operations = load_operations()
    if 0 <= index < len(operations):
        del operations[index]
        try:
            with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()
                for op in operations:
                    writer.writerow(op.to_dict())
        except Exception as e:
            print(f"Ошибка при сохранении после удаления: {e}")
    else:
        print("Неверный индекс операции")