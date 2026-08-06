from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.payment_method import PaymentMethod


def seed_database(session: Session):
    """Insert default records if tables are empty."""

    # ---------- Categories ----------

    if session.query(Category).count() == 0:

        categories = [

            # Income

            Category(name="Room Booking", type="Income"),

            Category(name="Restaurant Sales", type="Income"),

            Category(name="Laundry Service", type="Income"),

            Category(name="Banquet Booking", type="Income"),

            Category(name="Other Income", type="Income"),

            # Expense

            Category(name="Employee Salary", type="Expense"),

            Category(name="Electricity", type="Expense"),

            Category(name="Water", type="Expense"),

            Category(name="Gas", type="Expense"),

            Category(name="Food Supplies", type="Expense"),

            Category(name="Cleaning Supplies", type="Expense"),

            Category(name="Maintenance", type="Expense"),

            Category(name="Internet", type="Expense"),

            Category(name="Fuel", type="Expense"),

            Category(name="Personal", type="Expense"),

            Category(name="Education", type="Expense"),

            Category(name="Other Expense", type="Expense"),

        ]

        session.add_all(categories)

    # ---------- Payment Methods ----------

    if session.query(PaymentMethod).count() == 0:

        methods = [

            PaymentMethod(name="Cash", is_active=True,),

            PaymentMethod( name="Online", is_active=True,),
        ]

        session.add_all(methods)


    session.commit()