import re
from datetime import datetime

TYPE_MAPPING = {"Доходы": "income", "Расходы": "expense"}

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        return amount > 0
    except ValueError:
        return False

def clean_comment(comment):
    comment = comment.strip()
    comment = re.sub(r"[^A-Za-zА-Яа-я0-9 .,!?-]", "", comment)
    return comment

def validate_type(type_):
    return type_ in TYPE_MAPPING