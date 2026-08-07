from datetime import datetime
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (QComboBox,QFrame,QGridLayout,QHBoxLayout,QLabel,QPushButton,QVBoxLayout,QWidget)
from PySide6.QtCharts import ( QBarCategoryAxis, QBarSeries, QBarSet, QChart, QChartView, QValueAxis)
from PySide6.QtGui import (QPainter,QColor)

from PySide6.QtCharts import QChart

from app.views.widgets.stat_card import StatCard
from app.controllers.transaction_controller import (TransactionController)

class ReportsPage(QWidget):
    """Reports and analytics page."""

    def __init__(self,session):
        super().__init__()

        self.session = session
        self.transaction_controller = (TransactionController(session))

        self.init_ui()
        self.generate_report()

    def init_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(20,20,20,20)

        main_layout.setSpacing(20)

        # =====================================================
        # Header
        # =====================================================

        header_layout = QHBoxLayout()

        title = QLabel("Reports")
        title.setObjectName("pageTitle")


        date_label = QLabel(datetime.now().strftime("%A, %d %b %Y"))

        date_label.setObjectName("dateLabel")


        header_layout.addWidget(title)

        header_layout.addStretch()

        header_layout.addWidget(date_label)

        main_layout.addLayout(header_layout)

        # =====================================================
        # Report Filters
        # =====================================================

        filter_layout = QHBoxLayout()

        self.month_combo = QComboBox()

        self.month_combo.addItems(
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ]
        )

        self.month_combo.setCurrentIndex(datetime.now().month - 1)
        self.year_combo = QComboBox()

        current_year = datetime.now().year

        for year in range(current_year - 5,current_year + 1):
            self.year_combo.addItem(str(year))

        self.year_combo.setCurrentText(str(current_year))

        self.generate_button = QPushButton("Generate Report")

        self.generate_button.clicked.connect(self.generate_report)

        filter_layout.addWidget(self.month_combo)
        filter_layout.addWidget(self.year_combo)
        filter_layout.addStretch()
        filter_layout.addWidget(self.generate_button)

        main_layout.addLayout(filter_layout)


        # =====================================================
        # Financial Overview
        # =====================================================

        overview_title = QLabel("Financial Overview")
        overview_title.setObjectName("sectionTitle")

        main_layout.addWidget(overview_title)


        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)


        self.income_card = StatCard("Monthly Income","₹0")

        self.expense_card = StatCard("Monthly Expense","₹0")

        self.profit_card = StatCard("Net Profit","₹0")

        self.transaction_card = StatCard("Transactions","0")

        cards_layout.addWidget(self.income_card,0,0)

        cards_layout.addWidget(self.expense_card,0,1)

        cards_layout.addWidget(self.profit_card,0,2)

        cards_layout.addWidget(self.transaction_card,0,3)

        main_layout.addLayout(cards_layout)

        # =====================================================
        # Analytics
        # =====================================================

        analytics_title = QLabel("Analytics")

        analytics_title.setObjectName("sectionTitle")

        main_layout.addWidget(analytics_title)

        charts_layout = QGridLayout()

        charts_layout.setSpacing(15)

        self.income_breakdown_chart = self.create_chart_placeholder("Income Breakdown")

        self.expense_breakdown_chart = self.create_chart_placeholder("Expense Breakdown")

        charts_layout.addWidget(self.income_breakdown_chart,0,0)

        charts_layout.addWidget(self.expense_breakdown_chart,0,1)

        main_layout.addLayout(charts_layout)


    def create_chart_placeholder(self, title):
    
        frame = QFrame()
        frame.setObjectName("chartCard")
        frame.setMinimumHeight(380)
    
        layout = QVBoxLayout(frame)
    
        title_label = QLabel(title)
        title_label.setObjectName("chartTitle")
        title_label.setAlignment(Qt.AlignCenter)
    
        layout.addWidget(title_label)
    
        chart_container = QWidget()
    
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.setSpacing(0)
    
        layout.addWidget(chart_container, 1)
    
        frame.chart_container = chart_container
        frame.setContentsMargins(0, 0, 0, 0)
    
        return frame
    

    def generate_report(self):

        month = (
            self.month_combo.currentIndex() + 1
        )

        year = int(
            self.year_combo.currentText()
        )

        income = (
            self.transaction_controller
            .get_monthly_income(month, year)
        )

        expense = (
            self.transaction_controller
            .get_monthly_expense(month, year)
        )

        transactions = (
            self.transaction_controller
            .get_monthly_transaction_count(
                month,
                year,
            )
        )

        profit = income - expense

        self.income_card.set_value(
            f"₹ {income:.2f}"
        )

        self.expense_card.set_value(
            f"₹ {expense:.2f}"
        )

        self.profit_card.set_value(
            f"₹ {profit:.2f}"
        )

        self.transaction_card.set_value(
            str(transactions)
        )

        income_categories = (
            self.transaction_controller.get_income_by_category(
                month,
                year,
            )
        )

        expense_categories = (
            self.transaction_controller.get_expense_by_category(
                month,
                year,
            )
        )

        self.show_category_chart(self.income_breakdown_chart,income_categories,"Income Breakdown",)

        self.show_category_chart(self.expense_breakdown_chart,expense_categories,"Expense Breakdown",)

    def show_category_chart(self,chart_frame,data,chart_title,):
        """Display category-wise vertical bar chart."""

        layout = chart_frame.chart_container.layout()

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        series = QBarSeries()

        categories = []

        colors = [
            QColor("#4CAF50"),
            QColor("#2196F3"),
            QColor("#FF9800"),
            QColor("#9C27B0"),
            QColor("#F44336"),
            QColor("#00BCD4"),
            QColor("#795548"),
            QColor("#607D8B"),
        ]

        maximum = 0

        for index, (name, amount) in enumerate(data):

            bar = QBarSet(name)

            value = float(amount)

            bar.append(value)

            bar.setColor(colors[index % len(colors)])

            series.append(bar)

            categories.append(name)

            maximum = max(maximum, value)

        chart = QChart()

        chart.addSeries(series)

        chart.setTitle("")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        axis_x = QBarCategoryAxis()

        axis_x.append(categories)

        # Optional (if your PySide6 version supports it)
        axis_x.setLabelsAngle(-30)

        axis_x.setGridLineVisible(False)


        chart.addAxis(axis_x, Qt.AlignBottom)

        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        
        axis_y.setRange(
            0,
            maximum * 1.2 if maximum else 100
        )
        
        axis_y.setTickCount(5)
        
        axis_y.setLabelFormat("₹ %.0f")
        
        axis_y.setGridLineVisible(True)
        

        chart.addAxis(
            axis_y,
            Qt.AlignLeft,
        )

        series.attachAxis(axis_y)

        chart_view = QChartView(chart)

        chart_view.setRenderHint(
            QPainter.Antialiasing
        )

        layout.addWidget(chart_view)