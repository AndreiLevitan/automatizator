import os
import win32api, win32con
import shutil
import time

class File:
    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.path = path + '/' + name
        self.hidden = win32api.GetFileAttributes(self.get_path())
        if self.hidden == 128:
            self.hidden = False
        else:
            self.hidden = True

    def change_name(self, new_name):
        self.name = new_name
        # отправить автоматизатору

    def change_type(self, new_type):
        self.type = new_type
        # отправить автоматизатору

    def hide(self):  # прячет файл
        win32api.SetFileAttributes(self.get_path(), win32con.FILE_ATTRIBUTE_HIDDEN)
        self.hidden = True

    def unhide(self):  # открывает файл
        win32api.SetFileAttributes(self.get_path(), win32con.FILE_ATTRIBUTE_NORMAL)
        self.hidden = False

    # "геттеры"
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_path(self):
        return self.path

    def is_hidden(self):
        return self.hidden


class Folder:
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]
        self.hidden = win32api.GetFileAttributes(self.get_path())
        if self.hidden in [2, 18]:
            self.hidden = True
        else:
            self.hidden = False

    def change_name(self, new_name):
        self.name = new_name
        # отправить автоматизатору

    def hide(self):  # прячет файл
        win32api.SetFileAttributes(self.get_path(), win32con.FILE_ATTRIBUTE_HIDDEN)
        self.hidden = True

    def unhide(self):  # открывает файл
        win32api.SetFileAttributes(self.get_path(), win32con.FILE_ATTRIBUTE_NORMAL)
        self.hidden = False

    # "геттеры"
    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def is_hidden(self):
        return self.hidden


class Automatizator:
    def __init__(self, path):
        self.path = path
        self.things = []   # здесь и далее things - и файлы, и папки
        self.FILENAME = 0
        self.DIRPATH = 1

        # шаблоны лямда-функций для метода rename_certian_things и GUI
        self.rename_lambdas = {
            # добавляет к названию дату и время
            'дата-время': lambda x: x + time.strftime(' [%Y-%m-%d %H-%M-%S]', time.gmtime())

        }

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

    # удаляет файлы и папки, подходящие по условию
    # если only_files, то не будет трогать папки
    def delete_certain_things(self, type='', name='', only_files=False):
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            only_files1 = only_files
            if type:
                only_files1 = True
            if thing_type == 'Folder' and not only_files1 and name in thing.get_name():
                shutil.rmtree(thing.get_path(), ignore_errors=True)
                self.things.remove(thing)
            elif thing_type == 'File' and name in thing.get_name() and (not type or type == thing.get_type()):
                os.remove(thing.get_path())
                self.things.remove(thing)

    # переименовывает определённые things согласно лямбда-функции
    def rename_certian_things(self, type='', name='', only_files=False, function=lambda x: x + '1'):
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            only_files1 = only_files
            if type:
                only_files1 = True
            if thing_type == 'Folder' and not only_files1 and name in thing.get_name():
                path = '/'.join(thing.get_path().split('/')[:-1])
                old_name = thing.get_path().split('/')[-1]
                new_name = function(old_name)
                old_path = path + '/' + old_name
                new_path = path + '/' + new_name
                os.rename(old_path, new_path)
            elif thing_type == 'File' and name in thing.get_name() and (not type or type == thing.get_type()):
                path = '/'.join(thing.get_path().split('/')[:-1])
                type = thing.get_type()
                old_name = thing.get_path().split('/')[-1]
                old_name = '.'.join(old_name.split('.')[:-1])
                new_name = function(old_name)
                old_path = path + '/' + old_name + '.' + type
                new_path = path + '/' + new_name + '.' + type
                os.rename(old_path, new_path)

    def hide_certain_things(self, type='', name='', only_files=False):  # прячет файлы и папки
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            only_files1 = only_files
            if thing_type == 'Folder' and not only_files1 and name in thing.get_name():
                if not thing.is_hidden():
                    thing.hide()
            elif thing_type == 'File' and name in thing.get_name()and (not type or type == thing.get_type()):
                if not thing.is_hidden():
                    thing.hide()

    def unhide_certain_things(self, type='', name='', only_files=False):  # открывает файлы и папки
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            only_files1 = only_files
            if thing_type == 'Folder' and not only_files1 and name in thing.get_name():
                if thing.is_hidden():
                    thing.unhide()
            elif thing_type == 'File' and name in thing.get_name()and (not type or type == thing.get_type()):
                if thing.is_hidden():
                    thing.unhide()

    def keep_only_certain_files(self, type='', name=''):  # удаляет все файлы, не подходящие по условию
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            if thing_type == 'File' and not (name in thing.get_name() and (not type or type == thing.get_type())):
                os.remove(thing.get_path())
                self.things.remove(thing)

    def get_path(self):
        return self.path

    def get_things(self):
        return self.things

    def get_lambda_rename(self, name):
        return self.rename_lambdas[name]


if __name__ == '__main__':
    auto = Automatizator('D:/Python/Automatizator/test')
    auto.find_things(nesting_level=0)
    for i in auto.get_things():
        print(i.get_name())
        print(i.get_path())
        print()
    auto.keep_only_certain_files(name='32')
