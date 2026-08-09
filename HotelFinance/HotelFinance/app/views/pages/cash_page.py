from datetime import datetime,date
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt
from sqlalchemy.exc import SQLAlchemyError


from app.views.widgets.stat_card import StatCard
from app.controllers.transaction_controller import (TransactionController)
from app.controllers.daily_balance_controller import (DailyBalanceController)
from app.controllers.cash_denomination_controller import CashDenominationController
from app.views.dialogs.opening_balance_dialog import (OpeningBalanceDialog)


class CashPage(QWidget):
    """Cash management page."""

    DENOMINATIONS = (500, 200, 100, 50, 20, 10, 5, 2, 1)

    def __init__(self, session):
        super().__init__()

        self.session = session
        self.transaction_controller = TransactionController(session)
        self.daily_balance_controller = DailyBalanceController(session)
        self.cash_denomination_controller = CashDenominationController(session)

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
        # Cash Denominations
        # =====================================================

        self.create_cash_denominations(main_layout)

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
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setRowCount(1)
        self.table.setItem(0,0,QTableWidgetItem(    "No transactions found."),)
        self.table.setSpan(0,0,1,6,)
        self.adjust_table_height()

        main_layout.addWidget(self.table)

    def adjust_table_height(self):
        """Let the page scrollbar, rather than the table, handle vertical overflow."""

        header_height = self.table.horizontalHeader().sizeHint().height()
        frame_height = self.table.frameWidth() * 2
        rows_height = sum(self.table.rowHeight(row) for row in range(self.table.rowCount()))
        self.table.setFixedHeight(header_height + rows_height + frame_height)

    def create_cash_denominations(self, parent_layout):
        """Create the UI-only counter for the cash currently on hand."""

        title = QLabel("Cash Denominations")
        title.setObjectName("sectionTitle")
        parent_layout.addWidget(title)

        section = QFrame()
        section.setObjectName("denominationSection")
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(16, 16, 16, 16)
        section_layout.setSpacing(12)

        self.denomination_inputs = {}
        self.denomination_amount_labels = {}

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        for index, denomination in enumerate(self.DENOMINATIONS):
            row, column = divmod(index, 3)
            grid.addWidget(self.create_denomination_card(denomination), row, column)
            grid.setColumnStretch(column, 1)

        section_layout.addLayout(grid)

        total_layout = QHBoxLayout()
        total_label = QLabel("Total Cash")
        total_label.setObjectName("denominationTotalTitle")
        self.denomination_total_label = QLabel("₹ 0.00")
        self.denomination_total_label.setObjectName("denominationTotal")
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.denomination_total_label)
        section_layout.addLayout(total_layout)

        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        reset_button = QPushButton("Clear")
        reset_button.setObjectName("denominationResetButton")
        reset_button.clicked.connect(self.clear_denominations)
        actions_layout.addWidget(reset_button)
        section_layout.addLayout(actions_layout)

        parent_layout.addWidget(section)

        save_button = QPushButton("Save Denominations")
        save_button.setObjectName("denominationSaveButton")
        save_button.clicked.connect(self.save_denomination_values)
        actions_layout.addWidget(save_button)

    def create_denomination_card(self, denomination):
        """Create one compact denomination card and retain its input widgets."""

        card = QFrame()
        card.setObjectName("denominationCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 12, 14, 12)
        card_layout.setSpacing(7)

        denomination_label = QLabel(f"₹ {denomination}")
        denomination_label.setObjectName("denominationLabel")
        card_layout.addWidget(denomination_label)

        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("Quantity")
        quantity_label.setObjectName("denominationQuantityLabel")
        quantity_input = QSpinBox()
        quantity_input.setObjectName("denominationInput")
        quantity_input.setRange(0, 9999)
        quantity_input.setValue(0)
        quantity_input.valueChanged.connect(self.update_denomination_totals)
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addStretch()
        quantity_layout.addWidget(quantity_input)
        card_layout.addLayout(quantity_layout)

        amount_label = QLabel("Amount: ₹ 0.00")
        amount_label.setObjectName("denominationAmount")
        card_layout.addWidget(amount_label)

        self.denomination_inputs[denomination] = quantity_input
        self.denomination_amount_labels[denomination] = amount_label
        return card

    def update_denomination_totals(self):
        """Refresh denomination amounts and the overall cash total immediately."""

        total = 0
        for denomination, quantity_input in self.denomination_inputs.items():
            amount = denomination * quantity_input.value()
            self.denomination_amount_labels[denomination].setText(
                f"Amount: ₹ {amount:,.2f}"
            )
            total += amount

        self.denomination_total_label.setText(f"₹ {total:,.2f}")

    def clear_denominations(self):
        """Reset the in-memory denomination counter without changing daily balances."""

        for quantity_input in self.denomination_inputs.values():
            quantity_input.setValue(0)
        self.update_denomination_totals()

    def load_denomination_values(self):
        """Load today's saved denomination counts from the database."""

        today = date.today()
        try:
            record = self.cash_denomination_controller.get_by_date(today)
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to load today's cash denominations. Please check the database and try again.",
            )
            return

        if record:
            self.denomination_inputs[500].setValue(record.denomination_500)
            self.denomination_inputs[200].setValue(record.denomination_200)
            self.denomination_inputs[100].setValue(record.denomination_100)
            self.denomination_inputs[50].setValue(record.denomination_50)
            self.denomination_inputs[20].setValue(record.denomination_20)
            self.denomination_inputs[10].setValue(record.denomination_10)
            self.denomination_inputs[5].setValue(record.denomination_5)
            self.denomination_inputs[2].setValue(record.denomination_2)
            self.denomination_inputs[1].setValue(record.denomination_1)
        else:
            self.clear_denominations()

        self.update_denomination_totals()

    def save_denomination_values(self):
        """Save the current denomination counts for today."""

        today = date.today()
        try:
            record = self.cash_denomination_controller.get_or_create(today)
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to save today's cash denominations. Please check the database and try again.",
            )
            return

        record.denomination_500 = self.denomination_inputs[500].value()
        record.denomination_200 = self.denomination_inputs[200].value()
        record.denomination_100 = self.denomination_inputs[100].value()
        record.denomination_50 = self.denomination_inputs[50].value()
        record.denomination_20 = self.denomination_inputs[20].value()
        record.denomination_10 = self.denomination_inputs[10].value()
        record.denomination_5 = self.denomination_inputs[5].value()
        record.denomination_2 = self.denomination_inputs[2].value()
        record.denomination_1 = self.denomination_inputs[1].value()
        record.total = sum(
            denomination * self.denomination_inputs[denomination].value()
            for denomination in self.DENOMINATIONS
        )

        try:
            self.cash_denomination_controller.save_or_update(record)
            self.update_denomination_totals()
            QMessageBox.information(
                self,
                "Saved",
                "Today's denomination counts have been saved.",
            )
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Unable to Save Denominations",
                "The denomination counts could not be saved. Please try again.",
            )

    def load_page(self):
        """Load today's cash data."""

        try:
            self.load_daily_balance()
            self.load_summary()
            self.load_transactions()
            self.load_denomination_values()
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to load today's cash information. Please check the database connection and try again.",
            )


    def load_transactions(self):

        today = date.today()
        transactions = (self.transaction_controller.get_today_transactions(today))
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
            self.table.setItem(0,0,QTableWidgetItem("No transactions found."))
            self.table.setSpan(0, 0, 1, 6)

        self.adjust_table_height()


    def open_opening_balance_dialog(self):

        today = date.today()

        try:
            balance = self.daily_balance_controller.get_balance(today)
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to load the opening balance. Please check the database connection and try again.",
            )
            return

        cash = balance.cash_opening if balance else 0
        online = balance.online_opening if balance else 0

        dialog = OpeningBalanceDialog(cash,online,)

        if dialog.exec():
            cash = dialog.get_cash_opening()
            online = dialog.get_online_opening()

            today = date.today()
            try:
                balance = self.daily_balance_controller.get_balance(today)

                if balance:
                    balance.cash_opening = cash
                    balance.online_opening = online
                    self.daily_balance_controller.update_balance()
                else:
                    self.daily_balance_controller.create_balance(today,cash,online)
            except SQLAlchemyError:
                QMessageBox.critical(
                    self,
                    "Unable to Save Opening Balance",
                    "The opening balance could not be saved. Please try again.",
                )
                return

            self.load_page()
