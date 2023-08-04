from PySide6.QtWidgets import QApplication
from window_view import WindowView
import sys

app = QApplication(sys.argv)

window = WindowView(app)
window.show()

app.exec()
