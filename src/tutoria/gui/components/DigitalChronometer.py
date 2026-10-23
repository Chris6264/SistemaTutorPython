from PySide6.QtCore import QTimer, QTime
from PySide6.QtWidgets import QLCDNumber

class DigitalChronometer(QLCDNumber):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setDigitCount(5)
        self.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.current_time = QTime(0,0,0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chronometer)

        self.show_time()

    def show_time(self):
         self.display(self.current_time.toString("mm:ss"))

    def update_chronometer(self):
            self.current_time = self.current_time.addSecs(1)
            self.show_time()

    def start_chronometer(self):
         self.timer.start(1000)

    def pause_chronometer(self):
         self.timer.stop()

    def restart_chronometer(self):
         self.timer.stop()
         self.current_time = QTime(0,0,0)
         self.show_time()
    