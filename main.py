import os
import win32api
import win32con
import shutil
import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QMainWindow, QApplication, QFileDialog


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
        win32api.SetFileAttributes(self.get_path(),
                                   win32con.FILE_ATTRIBUTE_HIDDEN)
        self.hidden = True

    def unhide(self):  # открывает файл
        win32api.SetFileAttributes(self.get_path(),
                                   win32con.FILE_ATTRIBUTE_NORMAL)
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
        win32api.SetFileAttributes(self.get_path(),
                                   win32con.FILE_ATTRIBUTE_HIDDEN)
        win32api.SetFileAttributes(self.get_path(),
                                   win32con.ICON)
        self.hidden = True

    def unhide(self):  # открывает файл
        win32api.SetFileAttributes(self.get_path(),
                                   win32con.FILE_ATTRIBUTE_NORMAL)
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
        self.things = []  # здесь и далее things - и файлы, и папки
        self.FILENAME = 0
        self.DIRPATH = 1

        # шаблоны лямда-функций для метода rename_certian_things и GUI
        self.rename_lambdas = {
            # добавляет к названию дату и время
            'дата-время': lambda x:
            x + time.strftime(' [%Y-%m-%d %H-%M-%S]', time.gmtime())

        }

        # возможные действия пользователя
        self.actions = [
            'Удалить',
            'Оставить',
            'Переименовать',
            'Скрыть',
            'Показать'
        ]

    # nesting_level отвечает за уровень вложенности
    # (если 0 - не входит во вложенные каталоги,
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
                cur_path = os.getcwd().replace('\\', '/') + '/' \
                           + self.path.split('/')[-1]
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
            if thing_type == 'Folder' and not only_files1 \
                    and name in thing.get_name():
                shutil.rmtree(thing.get_path(), ignore_errors=True)
                self.things.remove(thing)
            elif thing_type == 'File' and name in thing.get_name() \
                    and (not type or type == thing.get_type()):
                os.remove(thing.get_path())
                self.things.remove(thing)

    # переименовывает определённые things согласно лямбда-функции
    def rename_certian_things(self, type='', name='',
                              only_files=False,
                              function=lambda x: x + '1'):
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            only_files1 = only_files
            if type:
                only_files1 = True
            if thing_type == 'Folder' and not only_files1 \
                    and name in thing.get_name():
                path = '/'.join(thing.get_path().split('/')[:-1])
                old_name = thing.get_path().split('/')[-1]
                new_name = function(old_name)
                old_path = path + '/' + old_name
                new_path = path + '/' + new_name
                os.rename(old_path, new_path)
            elif thing_type == 'File' and name in thing.get_name() \
                    and (not type or type == thing.get_type()):
                path = '/'.join(thing.get_path().split('/')[:-1])
                type = thing.get_type()
                old_name = thing.get_path().split('/')[-1]
                old_name = '.'.join(old_name.split('.')[:-1])
                new_name = function(old_name)
                old_path = path + '/' + old_name + '.' + type
                new_path = path + '/' + new_name + '.' + type
                os.rename(old_path, new_path)

    # прячет файлы и папки
    def hide_certain_things(self, type='', name='', only_files=False):
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            only_files1 = only_files
            if thing_type == 'Folder' and not only_files1 \
                    and name in thing.get_name():
                if not thing.is_hidden():
                    thing.hide()
            elif thing_type == 'File' and name in thing.get_name()\
                    and (not type or type == thing.get_type()):
                if not thing.is_hidden():
                    thing.hide()

    # открывает файлы и папки
    def unhide_certain_things(self, type='',
                              name='', only_files=False):
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            only_files1 = only_files
            if thing_type == 'Folder' and not only_files1 \
                    and name in thing.get_name():
                if thing.is_hidden():
                    thing.unhide()
            elif thing_type == 'File' and name in thing.get_name() \
                    and (not type or type == thing.get_type()):
                if thing.is_hidden():
                    thing.unhide()

    # удаляет все файлы, не подходящие по условию
    def keep_only_certain_files(self, type='', name=''):
        for thing in self.things.copy():
            thing_type = thing.__class__.__name__
            if thing_type == 'File' \
                    and not (name in thing.get_name() and
                             (not type or type == thing.get_type())):
                os.remove(thing.get_path())
                self.things.remove(thing)

    def get_path(self):
        return self.path

    def get_things(self):
        return self.things

    def get_lambda_rename(self, name):
        return self.rename_lambdas[name]

    def get_actions(self):
        return self.actions


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(658, 600)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 631, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.change_dir_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.change_dir_btn.setMaximumSize(QtCore.QSize(120, 16777215))
        self.change_dir_btn.setObjectName("change_dir_btn")
        self.gridLayout.addWidget(self.change_dir_btn, 0, 2, 1, 1)
        self.current_directory_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.current_directory_label.setFont(font)
        self.current_directory_label.setObjectName("current_directory_label")
        self.gridLayout.addWidget(self.current_directory_label, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.current_move_combo_box = \
            QtWidgets.QComboBox(self.gridLayoutWidget)
        self.current_move_combo_box.setEditable(False)
        self.current_move_combo_box.setCurrentText("")
        self.current_move_combo_box.setMaxVisibleItems(9)
        self.current_move_combo_box.setInsertPolicy(
            QtWidgets.QComboBox.InsertAtBottom)
        self.current_move_combo_box.setObjectName("current_move_combo_box")
        self.gridLayout.addWidget(self.current_move_combo_box, 1, 1, 1, 1)
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(30, 520, 601, 23))
        self.start_btn.setCheckable(False)
        self.start_btn.setAutoDefault(False)
        self.start_btn.setDefault(False)
        self.start_btn.setFlat(False)
        self.start_btn.setObjectName("start_btn")
        self.gridLayoutWidget_2 = \
            QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 210, 631, 125))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = \
            QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.set_name_box = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.set_name_box.setObjectName("set_name_box")
        self.gridLayout_2.addWidget(self.set_name_box, 2, 0, 1, 1)
        self.type_input = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.type_input.setReadOnly(False)
        self.type_input.setClearButtonEnabled(False)
        self.type_input.setObjectName("type_input")
        self.gridLayout_2.addWidget(self.type_input, 1, 1, 1, 1)
        self.set_type_box = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.set_type_box.setCheckable(True)
        self.set_type_box.setChecked(False)
        self.set_type_box.setObjectName("set_type_box")
        self.gridLayout_2.addWidget(self.set_type_box, 1, 0, 1, 1)
        self.only_files_box = \
            QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.only_files_box.setObjectName("only_files_box")
        self.gridLayout_2.addWidget(self.only_files_box, 0, 0, 1, 1)
        self.name_input = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.name_input.setReadOnly(False)
        self.name_input.setClearButtonEnabled(False)
        self.name_input.setObjectName("name_input")
        self.gridLayout_2.addWidget(self.name_input, 2, 1, 1, 1)
        self.find_level_spin = \
            QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.find_level_spin.setMinimum(0)
        self.find_level_spin.setObjectName("find_level_spin")
        self.gridLayout_2.addWidget(self.find_level_spin, 3, 1, 1, 1)
        self.find_level_box = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.find_level_box.setObjectName("find_level_box")
        self.gridLayout_2.addWidget(self.find_level_box, 3, 0, 1, 1)
        self.find_btn = QtWidgets.QPushButton(self.centralwidget)
        self.find_btn.setGeometry(QtCore.QRect(360, 460, 271, 21))
        self.find_btn.setObjectName("find_btn")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 460, 331, 16))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 658, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.change_dir_btn.setText(_translate("MainWindow", "Изменить..."))
        self.current_directory_label.setText(
            _translate("MainWindow", "директория"))
        self.label_2.setText(_translate("MainWindow", "Действие:"))
        self.label.setText(_translate("MainWindow",
                                      "Текущая директория:"))
        self.start_btn.setText(_translate("MainWindow",
                                          "Начать"))
        self.set_name_box.setText(_translate("MainWindow",
                                             "Настроить шаблон имени"))
        self.type_input.setText(_translate("MainWindow",
                                           "Введите здесь типы файлов" +
                                           " (mp3, txt и т.д.)"))
        self.set_type_box.setText(_translate("MainWindow",
                                             "Настроить тип файла"))
        self.only_files_box.setText(_translate("MainWindow", "Только файлы"))
        self.name_input.setText(_translate("MainWindow",
                                           "Объекты, которые содержат" +
                                           " данное имя, будут изменены"))
        self.find_level_box.setText(_translate("MainWindow", "Уровень поиска"))
        self.find_btn.setText(_translate("MainWindow", "Найти"))
        self.label_5.setText(_translate("MainWindow",
                                        "Нажмите НАЙТИ для поиска" +
                                        " заданных файлов и папок"))


class GUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.set_dir_in_label(auto.get_path())
        self.current_move_combo_box.addItems(auto.get_actions())

        self.name_input.setDisabled(True)
        self.set_name_box.clicked.connect(self.name_box_run)

        self.find_level_spin.setDisabled(True)
        self.find_level_box.clicked.connect(self.find_level_box_run)

        self.type_input.setDisabled(True)
        self.set_type_box.clicked.connect(self.type_box_run)

        self.only_files_box.clicked.connect(self.only_files_box_run)

        self.change_dir_btn.clicked.connect(self.change_dir)

        self.find_btn.clicked.connect(self.find_run)

    def find_run(self):
        only_files = bool(self.only_files_box.isChecked())
        print(only_files)
        # auto.find_things()

    def change_dir(self):
        path = QFileDialog.getExistingDirectory()
        self.set_dir_in_label(path)

    def set_dir_in_label(self, path):
        print(path)
        if len(path) > 50:
            path = path[:50] + '...'
        self.current_directory_label.setText(path)
        self.current_directory_label.adjustSize()

    def only_files_box_run(self):
        if self.only_files_box.isChecked():
            self.set_type_box.setDisabled(True)
            self.type_input.setDisabled(True)
        else:
            self.set_type_box.setDisabled(False)
            self.type_box_run()

    def type_box_run(self):
        if self.set_type_box.isChecked():
            self.type_input.setDisabled(False)
        else:
            self.type_input.setDisabled(True)

    def name_box_run(self):
        if self.set_name_box.isChecked():
            self.name_input.setDisabled(False)
        else:
            self.name_input.setDisabled(True)

    def find_level_box_run(self):
        if self.find_level_box.isChecked():
            self.find_level_spin.setDisabled(False)
        else:
            self.find_level_spin.setDisabled(True)


if __name__ == '__main__':
    auto = Automatizator('C:/Users/User/PycharmProjects/' +
                         'SecondHalf/Automatizator/test')
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
