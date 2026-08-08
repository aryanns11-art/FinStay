from datetime import datetime
from pathlib import Path
import calendar

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)
from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QValueAxis,
)
from sqlalchemy.exc import SQLAlchemyError

from app.services.report_generator import create_monthly_report_pdf
from app.utils.logger import logger

from app.views.widgets.stat_card import StatCard
from app.controllers.settings_controller import SettingsController
from app.controllers.transaction_controller import TransactionController


class ReportsPage(QWidget):
    """Reports and analytics page."""

    def __init__(self, session):
        super().__init__()

        self.session = session
        self.transaction_controller = TransactionController(session)
        self.settings_controller = SettingsController(session)

        self.init_ui()
        self.generate_report()

    # =========================================================
    # MAIN UI
    # =========================================================

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(18)

        self.create_header(main_layout)
        self.create_report_filters(main_layout)
        self.create_financial_overview(main_layout)
        self.create_daily_performance(main_layout)
        self.create_category_analysis(main_layout)

        main_layout.addStretch()

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self, parent_layout):
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)

        title = QLabel("Reports")
        title.setObjectName("pageTitle")

        self.current_date_label = QLabel(datetime.now().strftime("%A, %d %b %Y"))
        self.current_date_label.setObjectName("dateLabel")

        export_layout = QHBoxLayout()
        export_layout.setSpacing(10)

        self.export_pdf_button = QPushButton("Export PDF")
        self.export_pdf_button.clicked.connect(self.export_pdf)

        export_layout.addWidget(self.export_pdf_button)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addLayout(export_layout)
        header_layout.addWidget(self.current_date_label)

        parent_layout.addLayout(header_layout)

    # =========================================================
    # REPORT FILTERS
    # =========================================================

    def create_report_filters(self, parent_layout):
        filter_frame = QFrame()
        filter_frame.setObjectName("reportFilterCard")
        filter_frame.setMinimumHeight(80)

        filter_layout = QHBoxLayout(filter_frame)

        filter_layout.setContentsMargins(20, 15, 20, 15)

        filter_layout.setSpacing(16)

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

        self.month_combo.setFixedWidth(170)

        self.month_combo.setCurrentIndex(datetime.now().month - 1)

        self.year_combo = QComboBox()

        current_year = datetime.now().year

        for year in range(current_year - 5, current_year + 1):
            self.year_combo.addItem(str(year))

        self.year_combo.setFixedWidth(120)

        self.year_combo.setCurrentText(str(current_year))

        self.generate_button = QPushButton("Generate Report")

        self.generate_button.setFixedWidth(180)

        self.generate_button.clicked.connect(self.generate_report)

        filter_layout.addWidget(QLabel("Report Period:"))

        filter_layout.addWidget(self.month_combo)

        filter_layout.addWidget(self.year_combo)

        filter_layout.addStretch()

        filter_layout.addWidget(self.generate_button)

        parent_layout.addWidget(filter_frame)

    # =========================================================
    # FINANCIAL OVERVIEW
    # =========================================================

    def create_financial_overview(self, parent_layout):
        overview_title = QLabel("Financial Overview")

        overview_title.setObjectName("sectionTitle")

        parent_layout.addWidget(overview_title)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)

        self.income_card = StatCard("Monthly Income", "₹0")

        self.expense_card = StatCard("Monthly Expense", "₹0")

        self.profit_card = StatCard("Net Profit", "₹0")

        self.transaction_card = StatCard("Transactions", "0")

        cards_layout.addWidget(self.income_card, 0, 0)

        cards_layout.addWidget(self.expense_card, 0, 1)

        cards_layout.addWidget(self.profit_card, 0, 2)

        cards_layout.addWidget(self.transaction_card, 0, 3)

        for column in range(4):
            cards_layout.setColumnStretch(column, 1)

        parent_layout.addLayout(cards_layout)

    # =========================================================
    # DAILY / WEEKLY PERFORMANCE
    # =========================================================

    def create_daily_performance(self, parent_layout):
        performance_header = QHBoxLayout()

        performance_title = QLabel("Weekly Performance")

        performance_title.setObjectName("sectionTitle")

        self.week_combo = QComboBox()

        self.week_combo.setFixedWidth(140)

        self.week_combo.currentIndexChanged.connect(self.update_selected_week_chart)

        performance_header.addWidget(performance_title)

        performance_header.addStretch()

        performance_header.addWidget(QLabel("View:"))

        performance_header.addWidget(self.week_combo)

        parent_layout.addLayout(performance_header)

        self.daily_performance_chart = self.create_chart_placeholder("Income vs Expense")

        self.daily_performance_chart.setMinimumHeight(380)

        parent_layout.addWidget(self.daily_performance_chart)

    # =========================================================
    # CATEGORY ANALYSIS
    # =========================================================

    def create_category_analysis(self, parent_layout):
        category_title = QLabel("Category Analysis")

        category_title.setObjectName("sectionTitle")

        parent_layout.addWidget(category_title)

        charts_layout = QGridLayout()
        charts_layout.setSpacing(15)

        self.income_breakdown_chart = self.create_chart_placeholder("Income Breakdown")

        self.expense_breakdown_chart = self.create_chart_placeholder("Expense Breakdown")

        charts_layout.addWidget(self.income_breakdown_chart, 0, 0)

        charts_layout.addWidget(self.expense_breakdown_chart, 0, 1)

        charts_layout.setColumnStretch(0, 1)

        charts_layout.setColumnStretch(1, 1)

        parent_layout.addLayout(charts_layout)

    # =========================================================
    # CHART PLACEHOLDER
    # =========================================================

    def create_chart_placeholder(self, title):
        frame = QFrame()

        frame.setObjectName("chartCard")

        frame.setMinimumHeight(360)

        layout = QVBoxLayout(frame)

        layout.setContentsMargins(16, 16, 16, 16)

        layout.setSpacing(10)

        title_label = QLabel(title)

        title_label.setObjectName("chartTitle")

        title_label.setAlignment(Qt.AlignLeft)

        layout.addWidget(title_label)

        chart_container = QWidget()

        chart_layout = QVBoxLayout(chart_container)

        chart_layout.setContentsMargins(0, 0, 0, 0)

        chart_layout.setSpacing(0)

        layout.addWidget(chart_container, 1)

        frame.chart_container = chart_container

        frame.setContentsMargins(0, 0, 0, 0)

        return frame

    # =========================================================
    # GENERATE REPORT
    # =========================================================

    def generate_report(self):
        month = self.month_combo.currentIndex() + 1

        year = int(self.year_combo.currentText())

        try:
            income = self.transaction_controller.get_monthly_income(month, year)
            expense = self.transaction_controller.get_monthly_expense(month, year)
            transactions = self.transaction_controller.get_monthly_transaction_count(month, year)
            self.daily_data = self.transaction_controller.get_daily_income_expense(month, year)
            income_categories = self.transaction_controller.get_income_by_category(month, year)
            expense_categories = self.transaction_controller.get_expense_by_category(month, year)
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to generate the report. Please check the database connection and try again.",
            )
            return

        profit = income - expense

        self.income_card.set_value(f"₹ {income:.2f}")

        self.expense_card.set_value(f"₹ {expense:.2f}")

        self.profit_card.set_value(f"₹ {profit:.2f}")

        self.transaction_card.set_value(str(transactions))

        # -----------------------------------------------------
        # Daily data for selected month
        # -----------------------------------------------------

        # -----------------------------------------------------
        # Update week selector
        # -----------------------------------------------------

        self.update_week_selector(month, year)

        # -----------------------------------------------------
        # Category data
        # -----------------------------------------------------

        self.show_category_chart(self.income_breakdown_chart, income_categories)

        self.show_category_chart(self.expense_breakdown_chart, expense_categories)

    # =========================================================
    # WEEK SELECTOR
    # =========================================================

    def update_week_selector(self, month, year):
        days_in_month = calendar.monthrange(year, month)[1]

        week_count = (days_in_month + 6) // 7

        self.week_combo.blockSignals(True)

        self.week_combo.clear()

        for week in range(1, week_count + 1):
            self.week_combo.addItem(f"Week {week}")

        self.week_combo.blockSignals(False)

        self.week_combo.setCurrentIndex(0)

        self.update_selected_week_chart()

    # =========================================================
    # UPDATE SELECTED WEEK
    # =========================================================

    def update_selected_week_chart(self):
        if not hasattr(self, "daily_data"):
            return

        if not self.daily_data:
            self.show_weekly_bar_chart([])
            return

        week_number = self.week_combo.currentIndex() + 1

        start_day = ((week_number - 1) * 7) + 1

        end_day = (week_number * 7)

        selected_week_data = []

        for row in self.daily_data:
            day = int(row[0])

            if start_day <= day <= end_day:
                selected_week_data.append(row)

        self.show_weekly_bar_chart(selected_week_data)

    # =========================================================
    # WEEKLY BAR CHART
    # =========================================================

    def show_weekly_bar_chart(self, weekly_data):
        layout = self.daily_performance_chart.chart_container.layout()

        # Clear old chart
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not weekly_data:
            empty_label = QLabel("No transaction data available for this week.")

            empty_label.setAlignment(Qt.AlignCenter)

            empty_label.setObjectName("emptyChartLabel")

            layout.addWidget(empty_label)

            return

        # -----------------------------------------------------
        # Income and Expense bar sets
        # -----------------------------------------------------

        income_set = QBarSet("Income")

        expense_set = QBarSet("Expense")

        income_set.setColor(QColor("#16A34A"))

        expense_set.setColor(QColor("#D97706"))

        categories = []

        maximum = 0

        for day, income, expense in weekly_data:

            day_number = int(day)

            income_value = float(income)

            expense_value = float(expense)

            # Actual date shown on X-axis
            month = self.month_combo.currentIndex() + 1

            year = int(self.year_combo.currentText())

            date_value = datetime(year, month, day_number)

            date_label = date_value.strftime("%d %b")

            categories.append(date_label)

            income_set.append(income_value)

            expense_set.append(expense_value)

            maximum = max(maximum, income_value, expense_value)

        # -----------------------------------------------------
        # Bar series
        # -----------------------------------------------------

        series = QBarSeries()

        series.append(income_set)

        series.append(expense_set)

        # Slightly narrower bars for cleaner spacing
        series.setBarWidth(0.65)

        # -----------------------------------------------------
        # Chart
        # -----------------------------------------------------

        chart = QChart()

        chart.addSeries(series)

        chart.setTitle("")

        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart.legend().setVisible(True)

        chart.legend().setAlignment(Qt.AlignBottom)

        chart.layout().setContentsMargins(0, 0, 0, 0)

        chart.setBackgroundRoundness(0)

        # -----------------------------------------------------
        # X Axis - Actual Dates
        # -----------------------------------------------------

        axis_x = QBarCategoryAxis()

        axis_x.append(categories)

        axis_x.setLabelsAngle(0)

        axis_x.setGridLineVisible(False)

        chart.addAxis(axis_x, Qt.AlignBottom)

        series.attachAxis(axis_x)

        # -----------------------------------------------------
        # Y Axis
        # -----------------------------------------------------

        axis_y = QValueAxis()

        if maximum > 0:
            axis_maximum = maximum * 1.20
        else:
            axis_maximum = 100

        axis_y.setRange(0, axis_maximum)

        axis_y.setTickCount(6)

        # Use Rs instead of ₹ here.
        axis_y.setLabelFormat("Rs %.0f")

        axis_y.setTitleText("Amount")

        axis_y.setGridLineVisible(True)

        chart.addAxis(axis_y, Qt.AlignLeft)

        series.attachAxis(axis_y)

        # -----------------------------------------------------
        # Chart View
        # -----------------------------------------------------

        chart_view = QChartView(chart)

        chart_view.setRenderHint(QPainter.Antialiasing)

        chart_view.setMinimumHeight(300)

        layout.addWidget(chart_view)

    # =========================================================
    # CATEGORY BAR CHARTS
    # =========================================================

    def show_category_chart(self, chart_frame, data):
        layout = chart_frame.chart_container.layout()

        # Clear old chart
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not data:
            empty_label = QLabel("No data available for this period.")

            empty_label.setAlignment(Qt.AlignCenter)

            empty_label.setObjectName("emptyChartLabel")

            layout.addWidget(empty_label)

            return

        series = QBarSeries()

        categories = []

        colors = [
            QColor("#D4AF37"),
            QColor("#16A34A"),
            QColor("#D97706"),
            QColor("#BFA76A"),
            QColor("#DC2626"),
            QColor("#52525B"),
            QColor("#A16207"),
            QColor("#71717A"),
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

        axis_x.setLabelsAngle(0)

        axis_x.setGridLineVisible(False)

        chart.addAxis(axis_x, Qt.AlignBottom)

        series.attachAxis(axis_x)

        axis_y = QValueAxis()

        axis_y.setRange(0, maximum * 1.2 if maximum else 100)

        axis_y.setTickCount(5)

        axis_y.setLabelFormat("Rs %.0f")

        axis_y.setGridLineVisible(True)

        chart.addAxis(axis_y, Qt.AlignLeft)

        series.attachAxis(axis_y)

        chart_view = QChartView(chart)

        chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chart_view)

    # =========================================================
    # EXPORT PDF
    # =========================================================

    def export_pdf(self):
        month = self.month_combo.currentIndex() + 1

        year = int(self.year_combo.currentText())

        month_name = self.month_combo.currentText()

        default_name = f"Hotel_Report_{month_name}_{year}.pdf"

        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", default_name, "PDF Files (*.pdf)")

        if not file_path:
            return

        if Path(file_path).exists():
            confirm = QMessageBox.question(self, "Overwrite File?", f"The file '{Path(file_path).name}' already exists. Do you want to replace it?", QMessageBox.Yes | QMessageBox.No)

            if confirm != QMessageBox.Yes:
                return

        try:
            income = self.transaction_controller.get_monthly_income(month, year)
            expense = self.transaction_controller.get_monthly_expense(month, year)
            profit = income - expense
            transactions = self.transaction_controller.get_monthly_transaction_count(month, year)
            daily_data = self.transaction_controller.get_daily_income_expense(month, year)
            income_categories = self.transaction_controller.get_income_by_category(month, year)
            expense_categories = self.transaction_controller.get_expense_by_category(month, year)
            hotel_information = self.settings_controller.get_settings()
            create_monthly_report_pdf(
                file_path,
                month,
                year,
                income,
                expense,
                profit,
                transactions,
                daily_data,
                income_categories,
                expense_categories,
                hotel_information,
            )

            QMessageBox.information(self, "Report Saved", "PDF report was saved successfully.")

        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to prepare the report for export. Please check the database connection and try again.",
            )
        except (OSError, PermissionError):
            QMessageBox.critical(
                self,
                "PDF Export Failed",
                "The report could not be exported. Please check the selected location and try again.",
            )
        except Exception:
            logger.exception("Unexpected error while exporting a PDF report.")
            QMessageBox.critical(
                self,
                "PDF Export Failed",
                "The report could not be exported. Please check the selected location and try again.",
            )
