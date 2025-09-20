from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

from LoadWindow import LoadingWindow
from Model import Model


class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reclassificador")
        self.setGeometry(200, 200, 900, 600) # Define as dimensões da janela
        self.setFixedSize(self.size()) # Mantém as dimensões da janela fixas
        self.setWindowIcon(QIcon(Model().resource_path("figures/check_fig.png")))

        # Layout principal
        main_layout = QHBoxLayout(self)

        # Área da esquerda, contendo imagem + label
        left_layout = QVBoxLayout() # Criação de um Layout Vertical

        self.image_label = QLabel("Nenhuma imagem carregada")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        self.image_label.setFixedSize(600, 400)

        self.text_label = QLabel("Nome da imagem carregada")
        self.text_label.setAlignment(Qt.AlignCenter)

        left_layout.addWidget(self.image_label)
        left_layout.addWidget(self.text_label)

        # Área da direita, contendo os botões de funcionalidades
        right_layout = QVBoxLayout() # Criação de um Layout Vertical
        right_layout.setAlignment(Qt.AlignTop)  # Controles alinhados ao topo

        # Criação dos botões de funcionalidades e Labels
        self.btn_select_dir = QPushButton("Selecionar diretório de imagens")
        self.btn_ind = QPushButton("Classificar como 'Indolor'")
        self.btn_pd = QPushButton("Classificar como 'Pouca dor'")
        self.btn_md = QPushButton("Classificar como 'Muita dor'")
        self.btn_inc = QPushButton("Classificar como 'Incerto'")
        self.btn_undo = QPushButton("Desfazer última operação")
        self.btn_compare = QPushButton("Comparar datasets (projeto-ratos)")
        self.btn_exit = QPushButton("Sair do programa")
        self.delim1 = QLabel("Seleção de arquivos")
        self.delim2 = QLabel("Classificações")
        self.delim3 = QLabel("Funções adicionais")

        # Adicionando os botões como widgets ao right_layout
        right_layout.addWidget(self.delim1)
        right_layout.addWidget(self.btn_select_dir)
        right_layout.addSpacing(40)  # espaçamento fixo de 40px
        right_layout.addWidget(self.delim2)
        right_layout.addWidget(self.btn_ind)
        right_layout.addWidget(self.btn_pd)
        right_layout.addWidget(self.btn_md)
        right_layout.addWidget(self.btn_inc)
        right_layout.addSpacing(40)  # espaçamento fixo de 40px
        right_layout.addWidget(self.delim3)
        right_layout.addWidget(self.btn_undo)
        right_layout.addWidget(self.btn_compare)
        right_layout.addWidget(self.btn_exit)

        # Conectar sinais
        self.btn_select_dir.clicked.connect(self.load_data)
        self.btn_ind.clicked.connect(lambda: self.classify_image("Indolor"))
        self.btn_pd.clicked.connect(lambda: self.classify_image("Pouca dor"))
        self.btn_md.clicked.connect(lambda: self.classify_image("Muita dor"))
        self.btn_inc.clicked.connect(lambda: self.classify_image("Incerto"))
        self.btn_undo.clicked.connect(self.undo_operation)
        self.btn_compare.clicked.connect(self.compare_datasets)
        self.btn_exit.clicked.connect(self.close)

        # Adiciona layouts ao principal
        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addLayout(right_layout, stretch=1)

        # Inicialização das variáveis globais
        self.dir_path = None
        self.image_list = None
        self.current_index = 0 # Define o índice da imagem processada
        self.history = []  # Armazena a última operação para permitir desfazer, se for necessário

        # Status inicial dos botões de funcionalidades:
        self.btn_ind.setEnabled(False)
        self.btn_pd.setEnabled(False)
        self.btn_md.setEnabled(False)
        self.btn_inc.setEnabled(False)
        self.btn_select_dir.setEnabled(True)
        self.btn_exit.setEnabled(True)
        self.btn_undo.setEnabled(False)

        # Inserção de label para inserir a logo da UFU
        self.logo_label = QLabel()
        pixmap = QPixmap(Model().resource_path("figures/fig_ufu.png"))
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)  # Centraliza a imagem
        self.logo_label.setContentsMargins(0, 30, 0, 0)  # Padding para espaçar a exibição da imagem
        right_layout.addWidget(self.logo_label)

        # Inserção de label para definir a versão do software
        # Seguindo o padrão de Versionamento Semântico
        # MAJOR.MINOR.PATCH-SUFIX
        self.version_label = QLabel("Ver. 1.0.0", self)
        self.version_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.version_label)

        # -------------------------------------------------------------------
        # -------------------------------------------------------------------
        # -------------------------------------------------------------------
        # Funções da classe

    def load_data(self):

        # Recebe o caminho do dretório com as imagens
        self.dir_path = Model.open_directory()

        if self.dir_path:
            # Rece a lista dos arquivos contidos no diretório (contanto que sejam arquivos de imagens)
            self.image_list = Model.directory_files_list(self.dir_path)

        if self.image_list:
            # Carrega a imagem para a interface, caso a lista não seja vazia
            self.load_image()
            self.btn_ind.setEnabled(True)
            self.btn_pd.setEnabled(True)
            self.btn_md.setEnabled(True)
            self.btn_inc.setEnabled(True)
            self.btn_select_dir.setEnabled(True)
            self.btn_exit.setEnabled(True)
        else:
            QMessageBox.warning(self, "Aviso", "Nenhuma imagem encontrada nesse diretório.")


    def load_image(self):

        if self.current_index < len(self.image_list):

            # Exibe a imagem (por meio de um pixmap) referênte ao índice definido em current_index.
            # O processo não é feito em loop para evitar travamentos durante a execução e para
            # evitar complexidade desnecessária
            img_path = self.image_list[self.current_index]
            pixmap = QPixmap(img_path).scaled(600, 400, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.text_label.setText(f"Exibindo a imagem: {Model.get_file_basename(img_path)}")

        else:
            self.image_label.clear()
            self.text_label.setText("Nenhuma imagem carregada no momento.")
            QMessageBox.information(self, "Concluído", "Todas as imagens foram classificadas!")

    def classify_image(self, class_name):

        # Caso a lista de imagens esteja vazia, encerra a função
        if not self.image_list:
            return

        # Cria na pasta raiz do programa a estrutura de diretórios responsáveis por
        # armazenar os arquivos reclassificados.
        Model.manage_dirs(class_name)
        img_path = self.image_list[self.current_index] # Recebe o caminho da imagem por meio da lista criada
        destiny_path = Model.move_files(img_path, class_name, img_path) # Move de fato, o arquivo

        # salva no histórico
        self.history.append((img_path, destiny_path))

        self.text_label.setText(f"{Model.get_file_basename(img_path)} → {class_name}")
        QMessageBox.information(self, "Concluído", "Imagem re-classificada com sucesso!")

        # avança para próxima
        self.current_index += 1
        self.load_image()
        self.btn_undo.setEnabled(True)

    def undo_operation(self):

        # Avalia se existem operações prévias que podem ser desfeitas, durante a execução
        # Em caso negativo, a execução da função é encerrada
        if not self.history:
            QMessageBox.warning(self, "Aviso", "Nenhuma operação para desfazer.")
            return

        # Pega o último registro do histórico
        src_path, dest_path = self.history.pop()
        current_index, image_list =  Model.undo_operation(src_path, dest_path, self.current_index, self.image_list)

        self.current_index = current_index
        self.image_list = image_list

        if image_list:
            QMessageBox.warning(self, "Aviso", f"Operação desfeita: {Model.get_file_basename(src_path)}")
            self.load_image()
        else:
            QMessageBox.warning(self, "Erro", "O arquivo não foi encontrado para desfazer.")

    def compare_datasets(self):

        QMessageBox.warning(self, "Observação", "Atenção: Esta funcionalidade deve ser executada apenas para comparar "
                                                "bases de dados que contenham a mesma estrutura de diretórios,uma vez "
                                                "que a função pressupõe essa organização em AMBOS os diretórios "
                                                "(original e reclassificado) para percorrer os itens.")
        QMessageBox.warning(self, "Atenção", "Selecionar o diretório contendo o dataset original à ser comparado")
        original_data_path = Model.open_directory()
        QMessageBox.warning(self, "Atenção", "Selecionar o diretório contendo o dataset re-classificado")
        reclassified_data_path = Model.open_directory()

        if original_data_path is None or reclassified_data_path is None:
            QMessageBox.warning(self, "Erro", "Diretório nulo ou incompatível. Por favor, re-faça a operação")
            return

        loadScreen = LoadingWindow()
        loadScreen.show()
        # força atualização da interface para mostrar o diálogo
        QApplication.processEvents()

        divergencies = Model.compare_datsets(original_data_path, reclassified_data_path)

        if divergencies:
            loadScreen.close()

        print(divergencies)

