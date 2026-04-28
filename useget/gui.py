# Entrypoint for GUI

import sys
import logging
from PyQt5.QtWidgets import QApplication
from gui import UsegetGUI

def main():
    logger = logging.getLogger("GUI")
    app = QApplication(sys.argv)
    gui = UsegetGUI()
    gui.show()
    sys.exit(app.exec_())
