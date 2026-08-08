from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy, QScrollArea, QVBoxLayout, QWidget


class ScrollablePage(QWidget):
    """Wrap a page widget in a vertical scroll area."""

    def __init__(self, page_widget: QWidget):
        super().__init__()

        self.page_widget = page_widget

        self.setObjectName("scrollablePage")
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        content = QWidget()
        content.setObjectName("scrollablePageContent")
        content.setLayout(QVBoxLayout())
        content.layout().setContentsMargins(0, 0, 0, 0)
        content.layout().setSpacing(0)
        content.layout().addWidget(self.page_widget)

        self.page_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.scroll_area.setWidget(content)
        self.layout().addWidget(self.scroll_area)

    def widget(self):
        return self.page_widget

    def __getattr__(self, name):
        return getattr(self.page_widget, name)
