from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel


class LoadingWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.setModal(True)  # bloqueia interação com a janela principal
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aguarde, processando..."))
        self.setLayout(layout)
        self.setFixedSize(200, 100)