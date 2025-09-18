import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog

class Model:

    @staticmethod
    def resource_path(relative_path):
        """ Retorna o caminho absoluto para o arquivo, compatível com PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)

    @staticmethod
    def open_directory():
        """
            O tkinter é utilizado para exibir janela do explorer a fim de selecionar a pasta contendo o Dataset.
                * root = tk.Tk() - instância do tkinter
                * root.withdraw() -  Oculta a janela principal (para exibir apenas o pop-up)
                * filedialog.askdirectory(title="") - Abre a janela de seleção de pastas e retorna o caminho escolhido
        """
        root = tk.Tk()
        root.withdraw()

        path = filedialog.askdirectory(title="Selecione a pasta desejada")
        # Se o usuário cancelar ou fechar a janela, path será ""
        if not path:
            return None

        return path

    @staticmethod
    def directory_files_list(dir_path):

        files_list = []
        # Cria uma lista contendo o caminho de cada um dos itens presentes no diretório selecionado
        # contanto que os itens estejam no formato de imagem (de acordo com sua extensão)
        for file in os.listdir(dir_path):
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                files_list.append(os.path.join(dir_path, file))

        return files_list

    @staticmethod
    def get_file_basename(file):
        # Retorna apenas o nome do arquivo, ignorando os demais trechos referentes ao caminho
        return os.path.basename(file)

    @staticmethod
    def manage_dirs(folder_name):
        # cria o diretório para armazenar os frames (caso não exista previamente)
        os.makedirs('Reclassificados', exist_ok=True)
        os.makedirs(os.path.join('Reclassificados', folder_name), exist_ok=True)

    @staticmethod
    def move_files(original_path, class_name, img_path):

        destiny = os.path.join('Reclassificados', class_name)
        shutil.move(original_path, os.path.join(destiny, os.path.basename(img_path)))  # Move o arquivo entre diretórios

        return  os.path.join(destiny, os.path.basename(img_path))

    @staticmethod
    def undo_operation(src_path, dest_path, current_index, image_list):

        if os.path.exists(dest_path):
            shutil.move(dest_path, src_path)

            # Ajusta índice e recarrega imagem
            current_index = max(0, current_index - 1)

            # Re-insere o caminho da imagem na lista
            if src_path not in image_list:
                image_list.insert(current_index, src_path)

        return current_index, image_list