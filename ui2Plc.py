from ui.Ui_test02 import Ui_MainWindow
from module.TestConnect02 import Plc
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
import sys

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.plc = Plc()
        self._init_memory()
        self.setup_ui_signals()
        self.init_timer()

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plc_data)
        self.timer.start(100)

    def _init_memory(self):

        self.bPc2plc = [False] * 16
        self.bPlc2pc = [False] * 16

        self.iPc2plc = [0] * 10
        self.iPlc2pc = [0] * 10


    def set_status_style(self, widget, status):
        if status:
            widget.setStyleSheet("background-color: rgb(0, 170, 0); color: white; border: 1px solid black;")
        else:
            widget.setStyleSheet("background-color: rgb(145, 145, 145); color: black; border: 1px solid gray;")

    def setup_ui_signals(self):

        for i in range(1,15):
            btn_name = f'btnBit_{i}'
            if hasattr(self.ui, btn_name):
                btn = getattr(self.ui, btn_name)
                btn.pressed.connect(lambda idx=i: self.on_button_event(idx, True))
                btn.released.connect(lambda idx=i: self.on_button_event(idx, False))

    def on_button_event(self, index, state):

        self.bPc2plc[index - 1] = state
        btn = getattr(self.ui, f'btnBit_{index}')
        self.set_status_style(btn, state)

    def update_plc_data(self):

        self.plc.UpdateData(self.bPlc2pc, self.iPlc2pc, self.bPc2plc, self.iPc2plc)

        for i in range(15):
            lamp_name = f'lmpbit_{i + 1}'
            if hasattr(self.ui, lamp_name):
                lamp = getattr(self.ui, lamp_name)
                self.set_status_style(lamp, self.bPlc2pc[i])


app = QApplication(sys.argv)

# Tạo đối tượng cửa sổ
window = Main()
window.setWindowTitle("PLC HMI Control System")
window.show() # Hiển thị giao diện lên màn hình

# Bắt đầu vòng lặp sự kiện của Qt
sys.exit(app.exec())   