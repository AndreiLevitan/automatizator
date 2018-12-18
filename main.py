import os
import ctypes
import shutil

class File:
    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.path = path + '/' + name
        self.hidden = False

    def change_name(self, new_name):
        self.name = new_name
        # отправить автоматизатору

    def change_type(self, new_type):
        self.type = new_type
        # отправить автоматизатору

    def hide(self):  # прячет файл
        ctypes.windll.kernel32.SetFileAttributesW(self.get_path(), 2)
        self.hidden = True

    def unhide(self):  # открывает файл
        ctypes.windll.kernel32.SetFileAttributesW(self.get_path(), 128)
        self.hidden = False

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
        self.hidden = False

    def change_name(self, new_name):
        self.name = new_name
        # отправить автоматизатору

    def hide(self):  # прячет файл
        ctypes.windll.kernel32.SetFileAttributesW(self.get_path(), 2)
        self.hidden = True

    def unhide(self):  # открывает файл
        ctypes.windll.kernel32.SetFileAttributesW(self.get_path(), 128)
        self.hidden = False

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

    # nesting_level отвечает за уровень вложенности (если 0 - не входит во вложенные каталоги,
    # если 1 - входит в подкаталоги, если -1 - входит во все подпапки)
    def find_things(self, nesting_level=-1):
        things = set()
        level = nesting_level
        for (dirpath, dirnames, filenames) in os.walk(self.get_path()):
            path = dirpath
            path = path.replace('\\', '/')
            for filename in filenames:
                type = 'file'
                things.add((filename, path, type))
            for dirname in dirnames:
                type = 'folder'
                things.add((dirname, path + '/' + dirname, type))
            if level == 0:
                break
            else:
                level -= 1
        things = list(things)
        for name, path, type in things:
            if type == 'file':
                thing = File(name, name.split('.')[-1], path)
                self.things.append(thing)
            else:
                cur_path = os.getcwd().replace('\\', '/') + '/' + self.path.split('/')[-1]
                if cur_path != path:
                    thing = Folder(path)
                    self.things.append(thing)

    def delete_certain_things(self, type='', name='', only_files=False):  # если only_files, то не будет трогать папки
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            if thing_type == 'Folder' and not only_files and name in thing.get_name():
                shutil.rmtree(thing.get_path(), ignore_errors=True)
                self.things.remove(thing)
            elif thing_type == 'File' and name in thing.get_name() \
                and thing.get_name().split('.')[-1] == type:
                os.remove(thing.get_path())
                self.things.remove(thing)

                # ПРОВЕРИТЬ!!!




    def get_path(self):
        return self.path

    def get_things(self):
        return self.things


if __name__ == '__main__':
    auto = Automatizator('D:/Python/Automatizator/test')
    auto.find_things(nesting_level=2)
    for i in auto.get_things():
        print(i.get_name())
        print(i.get_path())
        print()
