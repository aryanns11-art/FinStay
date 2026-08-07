from datetime import datetime,date
from PySide6.QtWidgets import ( QGridLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView)
from PySide6.QtCore import Qt


from app.views.widgets.stat_card import StatCard
from app.controllers.transaction_controller import (TransactionController)
from app.controllers.daily_balance_controller import (DailyBalanceController)
from app.views.dialogs.opening_balance_dialog import (OpeningBalanceDialog)


class CashPage(QWidget):
    """Cash management page."""

    def __init__(self, session):
        super().__init__()

        self.session = session
        self.transaction_controller = (TransactionController(session))
        self.daily_balance_controller = ( DailyBalanceController(session))

        self.init_ui()
        self.load_page()

    def init_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(20,20,20,20,)
        main_layout.setSpacing(20)

        # =====================================================
        # Header
        # =====================================================

        header_layout = QHBoxLayout()

        title = QLabel("Cash Management")
        title.setObjectName("pageTitle")

        date_label = QLabel(datetime.now().strftime("%A, %d %b %Y"))
        date_label.setObjectName("dateLabel")

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(date_label)
        main_layout.addLayout(header_layout)

        # =====================================================
        # Toolbar
        # =====================================================

        toolbar = QHBoxLayout()
        toolbar.addStretch()
        self.opening_button = QPushButton("Set Opening Balance")

        self.opening_button.clicked.connect(self.open_opening_balance_dialog)

        toolbar.addWidget(self.opening_button)
        main_layout.addLayout(toolbar)

        # =====================================================
        # Cash
        # =====================================================

        cash_title = QLabel("Cash")
        cash_title.setObjectName("sectionTitle")
        main_layout.addWidget(cash_title)
        cash_layout = QGridLayout()
        cash_layout.setSpacing(15)

        self.cash_opening_card = StatCard("Opening","₹0",)
        self.cash_income_card = StatCard("Income","₹0",)
        self.cash_expense_card = StatCard("Expense","₹0",)
        self.cash_closing_card = StatCard("Closing","₹0",)

        cash_layout.addWidget(self.cash_opening_card,0,0,)
        cash_layout.addWidget(self.cash_income_card,0,1,)
        cash_layout.addWidget(self.cash_expense_card,0,2,)
        cash_layout.addWidget(self.cash_closing_card,0,3,)

        main_layout.addLayout(cash_layout)

        # =====================================================
        # Online
        # =====================================================

        online_title = QLabel("Online")
        online_title.setObjectName("sectionTitle")

        main_layout.addWidget(online_title)

        online_layout = QGridLayout()
        online_layout.setSpacing(15)


        self.online_opening_card = StatCard("Opening","₹0")
        self.online_income_card = StatCard("Income","₹0")
        self.online_expense_card = StatCard("Expense","₹0")
        self.online_closing_card = StatCard("Closing","₹0")

        online_layout.addWidget(self.online_opening_card,0,0)
        online_layout.addWidget(self.online_income_card,0,1)
        online_layout.addWidget(self.online_expense_card,0,2)
        online_layout.addWidget(self.online_closing_card,0,3)

        main_layout.addLayout(online_layout)

        # =====================================================
        # Today's Transactions
        # =====================================================

        table_title = QLabel("Today's Transactions")
        table_title.setObjectName("sectionTitle")

        main_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                "Date",
                "Time",
                "Category",
                "Payment",
                "Amount",
                "Description",
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setRowCount(1)
        self.table.setItem(0,0,QTableWidgetItem(    "No transactions found."),)
        self.table.setSpan(0,0,1,6,)

        main_layout.addWidget(self.table)

    def load_page(self):
        """Load today's cash data."""

        self.load_daily_balance()
        self.load_summary()
        self.load_transactions()


    def load_transactions(self):

        today = date.today()

        transactions = (
            self.transaction_controller
            .get_today_transactions(today)
        )

        self.populate_table(transactions)



    def load_daily_balance(self):

        today = date.today()
        self.balance = (self.daily_balance_controller.get_balance(today))


        if self.balance:
        
            self.opening_button.setText("Update Opening Balance")
            self.cash_opening_card.set_value(f"₹ {self.balance.cash_opening:.2f}")
            self.online_opening_card.set_value(f"₹ {self.balance.online_opening:.2f}")

        else:
        
            self.opening_button.setText("Set Opening Balance")
            self.cash_opening_card.set_value("₹ 0.00")
            self.online_opening_card.set_value("₹ 0.00")


    def load_summary(self):

        today = date.today()

        cash_income = (self.transaction_controller.get_today_cash_income(today))
        cash_expense = (self.transaction_controller.get_today_cash_expense(today))
        online_income = (self.transaction_controller.get_today_online_income(today))
        online_expense = (self.transaction_controller.get_today_online_expense(today))


        self.cash_income_card.set_value(f"₹ {cash_income:.2f}")
        self.cash_expense_card.set_value(f"₹ {cash_expense:.2f}")
        self.online_income_card.set_value(f"₹ {online_income:.2f}")
        self.online_expense_card.set_value(f"₹ {online_expense:.2f}")


        balance = self.balance

        cash_opening = (
            balance.cash_opening
            if balance else 0
        )

        online_opening = (
            balance.online_opening
            if balance else 0
        )

        cash_closing = (
            cash_opening
            + cash_income
            - cash_expense
        )

        online_closing = (
            online_opening
            + online_income
            - online_expense
        )


        self.cash_closing_card.set_value(f"₹ {cash_closing:.2f}")
        self.online_closing_card.set_value(f"₹ {online_closing:.2f}")




    def populate_table(self, transactions):
        self.table.clearContents()
        self.table.clearSpans()
        self.table.setRowCount(len(transactions))
        for row, transaction in enumerate(transactions):
            self.table.setRowHeight(row, 40)
            date_item = QTableWidgetItem(transaction.transaction_date.strftime("%d-%m-%Y"))
            date_item.setData(Qt.UserRole,transaction.id)
            self.table.setItem(row,0,date_item)
            self.table.setItem(row,1,QTableWidgetItem(transaction.transaction_time.strftime("%H:%M")))
            self.table.setItem(row,2,QTableWidgetItem(transaction.category.name))
            self.table.setItem(row,3,QTableWidgetItem(transaction.payment_method.name))
            self.table.setItem(row,4,QTableWidgetItem(f"₹ {transaction.amount:.2f}"))
            self.table.setItem(row,5,QTableWidgetItem(transaction.description or ""))
        if not transactions:
            self.table.setRowCount(1)
            self.table.clearSelection()
            self.table.setItem(
                0,
                0,
                QTableWidgetItem("No transactions found.")
            )
            self.table.setSpan(0, 0, 1, 6)


    def open_opening_balance_dialog(self):

        today = date.today()

        balance = self.daily_balance_controller.get_balance(today)

        cash = balance.cash_opening if balance else 0
        online = balance.online_opening if balance else 0

        dialog = OpeningBalanceDialog(cash,online,)

        if dialog.exec():
            cash = dialog.get_cash_opening()
            online = dialog.get_online_opening()

            today = date.today()
            balance = (self.daily_balance_controller.get_balance(today))

            if balance:
                balance.cash_opening = cash
                balance.online_opening = online
                self.daily_balance_controller.update_balance()
            else:
                self.daily_balance_controller.create_balance(today,cash,online)

            self.load_page()