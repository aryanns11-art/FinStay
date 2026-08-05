from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)


class TransactionTable(QTableWidget):
    """Reusable transaction table."""

    def __init__(self):
        super().__init__()

        self.setColumnCount(5)

        self.setHorizontalHeaderLabels(
            [
                "Date",
                "Time",
                "Category",
                "Amount",
                "Payment",
            ]
        )

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.verticalHeader().setVisible(False)

        self.setAlternatingRowColors(True)

        self.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.setRowCount(1)

        self.setItem(
            0,
            0,
            QTableWidgetItem("No transactions found")
        )

        self.setSpan(0, 0, 1, 5)