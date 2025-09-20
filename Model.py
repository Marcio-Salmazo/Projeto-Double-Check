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

    @staticmethod
    def list_subdir(dir_path):
        return [
            name for name in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, name))
        ]

    @staticmethod
    def verify_existence(path, folder):
        full_path = os.path.join(path, folder)
        if os.path.isdir(full_path):
            return True
        else:
            return False

    @staticmethod
    def find_correspondence(file_name, current_class, og_path):

        folders = Model.list_subdir(og_path)
        for folder in folders:

            if folder is not current_class:
                items_list = Model.directory_files_list(os.path.join(og_path, folder))
                # Nova lista contendo apena os nome de arquivos dos itens originais
                name_list = set(os.path.basename(f) for f in items_list)

                if file_name in name_list:
                    return folder



    @staticmethod
    def compare_datsets(original_data_path, reclassified_data_path):

        expected_dirs = ['Indolor', 'Pouca dor', 'Muita dor', 'Incerto']
        divergences = {} # Dicionário, contendo as imagens que não tem correspondências, para serem tratadas depois

        for folder in expected_dirs:
            # Para cada uma das pastas, verificar se elas existem nos diretórios original e reclassificado
            if Model.verify_existence(original_data_path, folder) and Model.verify_existence(reclassified_data_path,
                                                                                             folder):
                # Coleta do itens pertencentes às pasta, para validar se há divergências
                og_itens = Model.directory_files_list(os.path.join(original_data_path, folder))
                rec_itens = Model.directory_files_list(os.path.join(reclassified_data_path, folder))

                # Nova lista contendo apena os nome de arquivos dos itens originais
                og_names_set = set(os.path.basename(f) for f in og_itens)

                # Para cada um do itens da lista coletada do dataset reclassificada, verificar se há
                # correspondência entre os itens da lista coletada do dataset original
                for item in rec_itens:

                    item_base_name = Model.get_file_basename(item)
                    if item_base_name not in og_names_set:
                        # Se não houver correspondência, obter qual outra classe associada ao item e
                        # salvar no dicionário
                        og_class = Model.find_correspondence(item_base_name, folder, original_data_path)
                        divergences[item_base_name] = {"classe_original": og_class,
                                                  "classe_atual": folder}

            else:
                continue

        return divergences
