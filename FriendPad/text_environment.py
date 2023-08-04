from PySide6.QtWidgets import QWidget, QTextEdit, QHBoxLayout

class TextRegion(QWidget):
    def __init__(self, file_name):
        super().__init__()

        self.file_name = file_name
        self.layout = QHBoxLayout(self)
        value = 5
        self.text_area = QTextEdit()

        format = self.text_area.document().rootFrame().frameFormat()
        format.setBottomMargin(value)
        format.setTopMargin(value)
        format.setLeftMargin(value)
        format.setRightMargin(value)
        
        self.text_area.document().rootFrame().setFrameFormat(format)

        self.layout.addWidget(self.text_area)


