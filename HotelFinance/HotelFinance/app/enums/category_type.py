from enum import Enum


class CategoryType(str, Enum):
    INCOME = "Income"
    EXPENSE = "Expense"