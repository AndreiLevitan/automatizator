from PyQt5 import QtCore, QtGui, QtWidgets


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
        self.current_move_combo_box = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.current_move_combo_box.setEditable(False)
        self.current_move_combo_box.setCurrentText("")
        self.current_move_combo_box.setMaxVisibleItems(9)
        self.current_move_combo_box.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.current_move_combo_box.setObjectName("current_move_combo_box")
        self.gridLayout.addWidget(self.current_move_combo_box, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 520, 601, 23))
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 210, 631, 125))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
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
        self.only_files_box = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.only_files_box.setObjectName("only_files_box")
        self.gridLayout_2.addWidget(self.only_files_box, 0, 0, 1, 1)
        self.name_input = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.name_input.setReadOnly(False)
        self.name_input.setClearButtonEnabled(False)
        self.name_input.setObjectName("name_input")
        self.gridLayout_2.addWidget(self.name_input, 2, 1, 1, 1)
        self.find_level_spin = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.find_level_spin.setMinimum(0)
        self.find_level_spin.setObjectName("find_level_spin")
        self.gridLayout_2.addWidget(self.find_level_spin, 3, 1, 1, 1)
        self.find_level_box = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.find_level_box.setObjectName("find_level_box")
        self.gridLayout_2.addWidget(self.find_level_box, 3, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(360, 460, 271, 21))
        self.pushButton_3.setObjectName("pushButton_3")
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
        self.current_directory_label.setText(_translate("MainWindow", "директория"))
        self.label_2.setText(_translate("MainWindow", "Действие:"))
        self.label.setText(_translate("MainWindow", "Текущая директория:"))
        self.pushButton_2.setText(_translate("MainWindow", "Начать"))
        self.set_name_box.setText(_translate("MainWindow", "Настроить шаблон имени"))
        self.type_input.setText(_translate("MainWindow", "Введите здесь типы файлов (mp3, txt и т.д.)"))
        self.set_type_box.setText(_translate("MainWindow", "Настроить тип файла"))
        self.only_files_box.setText(_translate("MainWindow", "Только файлы"))
        self.name_input.setText(_translate("MainWindow", "Все папки и файлы, которые содержат",
                                           "данное имя, будут изменены"))
        self.find_level_box.setText(_translate("MainWindow", "Уровень поиска"))
        self.pushButton_3.setText(_translate("MainWindow", "Найти"))
        self.label_5.setText(_translate("MainWindow", "Нажмите НАЙТИ для поиска заданных файлов и папок"))

