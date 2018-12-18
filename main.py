import os
import ctypes


class File:
    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.path = path + '/' + name

    def change_name(self, new_name):
        self.name = new_name
        # отправить автоматизатору

    def change_type(self, new_type):
        self.type = new_type
        # отправить автоматизатору

    def hide(self):  # прячет файл
        ctypes.windll.kernel32.SetFileAttributesW(self.get_path(), 2)

    def unhide(self):  # открывает файл
        ctypes.windll.kernel32.SetFileAttributesW(self.get_path(), 128)
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
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]

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
        self.FILENAME = 0
        self.DIRPATH = 1
        self.DIRNAME = 2

    # nesting_level отвечает за уровень вложенности (если 0 - не входит во вложенные каталоги,
    # если 1 - входит в подкаталоги, если -1 - входит во все подпапки)
    def find_things(self, nesting_level=-1):
        things = []
        level = nesting_level
        for (dirpath, dirnames, names) in os.walk(self.get_path()):
            path = dirpath
            path = path.replace('\\', '/')
            things.append((names, path))
            if level == 0:
                break
            else:
                level -= 1
        for name, path in things:
            if name:
                thing = File(name[0], name[0].split('.')[-1], path)
            else:
                thing = Folder(path)
            self.things.append(thing)

    def get_path(self):
        return self.path

    def get_things(self):
        return self.things


if __name__ == '__main__':
    auto = Automatizator('D:/Python/Automatizator/test')
    auto.find_things()
    for i in auto.get_things():
        print(i.get_name())
        print(i.get_path())
        print()
