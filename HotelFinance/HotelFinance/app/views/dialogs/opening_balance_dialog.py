from PySide6.QtWidgets import (QDialogButtonBox,QDoubleSpinBox,QFormLayout)

from app.views.dialogs.base_dialog import BaseDialog


class OpeningBalanceDialog(BaseDialog):
    """Dialog for setting opening balances."""

    def __init__(self,cash_opening=0,online_opening=0,):
        super().__init__("Set Opening Balance")

        self.build_ui()

        self.cash_spin.setValue(float(cash_opening))
        self.online_spin.setValue(float(online_opening))

    def build_ui(self):

        form = QFormLayout()
        form.setSpacing(15)

        self.cash_spin = QDoubleSpinBox()
        self.cash_spin.setPrefix("₹ ")
        self.cash_spin.setDecimals(2)
        self.cash_spin.setMaximum(999999999)

        self.online_spin = QDoubleSpinBox()
        self.online_spin.setPrefix("₹ ")
        self.online_spin.setDecimals(2)
        self.online_spin.setMaximum(999999999)

        form.addRow(
            "Cash Opening",
            self.cash_spin,
        )

        form.addRow(
            "Online Opening",
            self.online_spin,
        )

        self.layout.addLayout(form)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Save |
            QDialogButtonBox.Cancel
        )

        
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)



    def get_cash_opening(self):
        return self.cash_spin.value()
    
    def get_online_opening(self):
        return self.online_spin.value()