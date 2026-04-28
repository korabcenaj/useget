# Entrypoint for GUI
import sys
from PyQt5.QtWidgets import QApplication
from gui import UsegetGUI

def main():
    app = QApplication(sys.argv)
    gui = UsegetGUI()
    gui.show()
    sys.exit(app.exec_())
