from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.payment_method import PaymentMethod


def seed_database(session: Session):
    """Ensure required database defaults exist without pre-populating categories."""

    # Categories are intentionally left empty by default. Users add their own.
    # We do not create or overwrite default categories here.

    required_methods = ["Cash", "Online"]
    existing_methods = {
        method.name for method in session.query(PaymentMethod)
        .filter(PaymentMethod.name.in_(required_methods))
        .all()
    }

    missing_methods = [
        PaymentMethod(name=name, is_active=True)
        for name in required_methods
        if name not in existing_methods
    ]

    if missing_methods:
        session.add_all(missing_methods)

    session.commit()