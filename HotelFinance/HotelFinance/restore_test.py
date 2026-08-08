import sys
import os
from PySide6.QtCore import QCoreApplication
from app.workers.restore_worker import RestoreWorker

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)

    backup_file = r'C:\Billing\HotelFinance\HotelFinance\backups\hotel_finance_2026-08-07_23-23-17.backup'
    worker = RestoreWorker(backup_file)

    def on_finished():
        print('restore_finished signal received')
        app.quit()

    def on_error(error):
        print('restore_error signal received:', error)
        app.quit()

    def on_thread_done():
        print('thread finished signal received')
        app.quit()

    worker.restore_finished.connect(on_finished)
    worker.restore_error.connect(on_error)
    worker.finished.connect(on_thread_done)

    print('starting worker')
    worker.start()
    sys.exit(app.exec())
