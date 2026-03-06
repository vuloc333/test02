from ui.Ui_test02 import Ui_MainWindow
from module.TestConnect02 import Plc
from PySide6.QtGui import QPalette, QColor


class Main:
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.plc = Plc()
    
    def set_status_style(self, widget, status):

        widget.setAutoFillBackground(True)

        if status:
            # Chuyển sang màu Alternate Background bạn đã cài
            widget.setBackgroundRole(QPalette.AlternateBase)
        else:
            # Quay lại màu Background mặc định
            widget.setBackgroundRole(QPalette.Window)
    
    def TestConnect(self):

        self.bPlc2pc = 0
        self.iPlc2pc = 0
        self.bPc2plc = 0
        self.iPc2plc = 0

        for i in range(14):
            self.bPlc2pc(i) = getattr(self.ui, f'lmpbit_{i}').isChecked()

        self.plc.UpdateData(self.bPlc2pc, self.iPlc2pc, self.bPc2plc, self.iPc2plc)

        for i in range(14):
            self.set_status_style(self.ui, f'lmpbit_{i}', self.bPlc2pc(i))
            self.set_status_style(self.ui, f'btnBit_{i}', self.bPc2plc(i))

        self.plc.UpdateData()

