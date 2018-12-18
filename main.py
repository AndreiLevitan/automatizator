import os
import ctypes


class File:
    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.path = path

    def change_name(self, new_name):
        self.name = new_name
        # отправить автоматизатору

    def change_type(self, new_type):
        self.type = new_type
        # отправить автоматизатору

    def hide_file(self):  # прячет\показывает имя файла
        self.name = '.' + self.name
        # отправить автоматизатору

    # "геттеры"
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_path(self):
        return self.path

    def is_hidden(self):
        pass


class Folder:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def change_name(self, new_name):
        self.name = new_name
        # отправить автоматизатору

    def hide_file(self):  # прячет\показывает имя папки
        self.name = '.' + self.name
        # отправить автоматизатору

    # "геттеры"
    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def is_hidden(self):
        pass


class Automatizator:
    def __init__(self, path):
        self.path = path
        self.things = []   # здесь и далее things - и файлы, и папки

    # nesting_level отвечает за уровень вложенности (если 0 - не входит во вложенные каталоги,
    # если 1 - входит в подкаталоги, если -1 - входит во все подпапки)
    def find_things(self, nesting_level=-1):
        files = []
        level = nesting_level
        for (dirpath, dirnames, filenames) in os.walk(self.get_path()):
            files.extend(filenames)
            if level == 0:
                break
            else:
                level -= 1
        self.things = files
        print(files)

    def get_path(self):
        return self.path


if __name__ == '__main__':
    auto = Automatizator(os.getcwd())
    auto.find_things()


