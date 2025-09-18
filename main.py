import sys
from PyQt5.QtWidgets import QApplication

from Interface import Interface


class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.player = Interface()

    def run(self):
        self.player.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    main = Main()
    main.run()
