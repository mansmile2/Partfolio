import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtGui
from PIL import Image
class Registr(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('registr.ui', self)
        self.setWindowTitle('All+: Регистрация')
        self.lineEdit_login.setPlaceholderText('Введите логин')
        self.lineEdit_password1.setPlaceholderText('Введите пароль')
        self.lineEdit_password2.setPlaceholderText('Введите пароль ещё один раз')
        self.pushButton_registr.clicked.connect(self.regisrt)
        self.pushButton_login.clicked.connect(self.log)
    def regisrt(self):
        con = sqlite3.connect('catalog.db')
        cur = con.cursor()
        if self.lineEdit_login.text() != '' and self.lineEdit_password1.text() != '':
            if self.lineEdit_password1.text() == self.lineEdit_password2.text():
                result = cur.execute("SELECT user FROM registr WHERE user = ?", (self.lineEdit_login.text(),)).fetchone()
                if result:
                    mess = QMessageBox()
                    mess.setWindowTitle("Ошибка")
                    mess.setText("Данный логин уже занят")
                    mess.setStandardButtons(QMessageBox.StandardButton.Ok)
                    mess.setIcon(QMessageBox.Icon.Warning)
                    mess.exec()
                else:
                    cur.execute("INSERT INTO registr (user, password)  VALUES (?, ?)", (self.lineEdit_login.text(),self.lineEdit_password1.text()))
                    con.commit()
                    self.window_login = Login()
                    self.window_login.show()
                    self.close()
            else:
                mess = QMessageBox()
                mess.setWindowTitle("Ошибка")
                mess.setText("Пароли не совпадают")
                mess.setStandardButtons(QMessageBox.StandardButton.Ok)
                mess.setIcon(QMessageBox.Icon.Warning)
                mess.exec()
        else:
            mess = QMessageBox()
            mess.setWindowTitle("Ошибка")
            mess.setText("Поля пусты")
            mess.setStandardButtons(QMessageBox.StandardButton.Ok)
            mess.setIcon(QMessageBox.Icon.Critical)
            mess.exec()
        con.close()
    def log(self):
        self.window_login = Login()
        self.window_login.show()
        self.close()
class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.setWindowTitle('All+: Авторизация')
        self.lineEdit_login.setPlaceholderText('Введите логин')
        self.lineEdit_password.setPlaceholderText('Введите пароль')
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_registr.clicked.connect(self.reg)
    def login(self):
        con = sqlite3.connect('catalog.db')
        cur = con.cursor()
        if self.lineEdit_login.text() != '' and self.lineEdit_password.text() != '':
            result = cur.execute("SELECT user, password FROM registr WHERE user = ? AND password = ?", (self.lineEdit_login.text(), self.lineEdit_password.text())).fetchone()
            if result:
                self.window_main = Main()
                self.window_main.show()
                self.close()
            else:
                mess = QMessageBox()
                mess.setWindowTitle("Ошибка")
                mess.setText("Неправильный логин или пароль")
                mess.setStandardButtons(QMessageBox.StandardButton.Ok)
                mess.setIcon(QMessageBox.Icon.Warning)
                mess.exec()
        else:
            mess = QMessageBox()
            mess.setWindowTitle("Ошибка")
            mess.setText("Поля пусты")
            mess.setStandardButtons(QMessageBox.StandardButton.Ok)
            mess.setIcon(QMessageBox.Icon.Critical)
            mess.exec()
        con.close()
    def reg(self):
        self.window_registr = Registr()
        self.window_registr.show()
        self.close()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('glavstr.ui',self)
        self.setWindowTitle('All+: Главная страница')
        self.pushButton_catalog.clicked.connect(self.catalog)
        self.pushButton_dobavitrez.clicked.connect(self.plus)
        self.pushButton_out.clicked.connect(self.reg)
    def catalog(self):
        self.window_catalog = Catalog()
        self.window_catalog.show()
        self.close()
    def reg(self):
        self.window_registr = Registr()
        self.window_registr.show()
        self.close()
    def plus(self):
        self.window_plus = Plus()
        self.window_plus.show()
        self.close()
class Catalog(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('catalog.ui',self)
        self.setWindowTitle('All+: Каталог рецептов')
        base = sqlite3.connect('catalog.db').cursor()
        bases = base.execute('SELECT id, nazvanie, ingridient, rezept FROM catalogrez').fetchall()
        base_img = base.execute('SELECT images FROM catalogrez').fetchall()
        self.pushButton_back.clicked.connect(self.back)
        g_x=10
        g_y=60
        g_shir=250
        g_vis=250
        data=[]
        for row in bases:
            id_data, naz_data, opi_data, rez_data = row
            data.append(row)
        pix_list = []
        for i in base_img:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(i[0])
            pix_list.append(pixmap)
        for a in range(0, row[0], 3):
            self.groupbox = QGroupBox(self.frame)
            self.groupbox.setObjectName(f"group_+{a+1}")
            self.groupbox.setGeometry(QRect(g_x ,g_y + a * 90, g_shir ,g_vis))
            self.groupbox.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.layout = QVBoxLayout(self.groupbox)
            self.layout.setObjectName(f"layout_+{a+1}")
            self.label = QLabel(self.groupbox)
            self.label.setObjectName(f"label_+{a+1}")
            self.label.setScaledContents(True)
            self.label.setPixmap(pix_list[a])
            self.label.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.layout.addWidget(self.label)
            self.button = QPushButton(self.groupbox)
            self.button.setObjectName(f"button_+{a+1}")
            self.button.setText(data[a][1])
            self.button.setStyleSheet("background-color: rgb(255, 255, 255); border: 0px solid;")
            self.layout.addWidget(self.button)
            self.button.clicked.connect(self.resept)
        for b in range(1, row[0], 3):
            self.groupbox = QGroupBox(self.frame)
            self.groupbox.setObjectName(f"group_+{b}")
            self.groupbox.setGeometry(QRect(g_x + 270 ,g_y + b * 90 - 90, g_shir ,g_vis))
            self.groupbox.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.layout = QVBoxLayout(self.groupbox)
            self.layout.setObjectName(f"layout_+{b+1}")
            self.label = QLabel(self.groupbox)
            self.label.setObjectName(f"label_+{b+1}")
            self.label.setScaledContents(True)
            self.label.setPixmap(pix_list[b])
            self.label.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.layout.addWidget(self.label)
            self.button = QPushButton(self.groupbox)
            self.button.setObjectName(f"button_+{b+1}")
            self.button.setText(data[b][1])
            self.button.setStyleSheet("background-color: rgb(255, 255, 255); border: 0px solid;")
            self.layout.addWidget(self.button)
            self.button.clicked.connect(self.resept)
        for c in range(2, row[0], 3):
            self.groupbox = QGroupBox(self.frame)
            self.groupbox.setObjectName(f"group_+{c+1}")
            self.groupbox.setGeometry(QRect(g_x + 540 ,g_y + c * 90 - 180, g_shir, g_vis))
            self.groupbox.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.layout = QVBoxLayout(self.groupbox)
            self.layout.setObjectName(f"layout_+{c+1}")
            self.label = QLabel(self.groupbox)
            self.label.setObjectName(f"label_+{c+1}")
            self.label.setScaledContents(True)
            self.label.setPixmap(pix_list[c])
            self.label.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.layout.addWidget(self.label)
            self.button = QPushButton(self.groupbox)
            self.button.setObjectName(f"button_+{c+1}")
            self.button.setText(data[c][1])
            self.button.setStyleSheet("background-color: rgb(255, 255, 255); border: 0px solid;")
            self.layout.addWidget(self.button)
            self.button.clicked.connect(self.resept)
        self.frame.setMinimumSize(QSize(0, g_x * row[0]*10))
    def resept(self):
        self.window_resept = Resept()
        self.window_resept.show()
        self.close()
    def back(self):
        self.window_back = Main()
        self.window_back.show()
        self.close()
class Resept(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('resept.ui',self)
        self.setWindowTitle('All+: Рецепт')
        self.img_data = None
        base = sqlite3.connect('catalog.db').cursor()
        bases = base.execute('SELECT id, nazvanie, ingridient, rezept FROM catalogrez').fetchall()
        base_img = base.execute('SELECT images FROM catalogrez').fetchall()
        elem = base.execute('SELECT id, nazvanie FROM catalogrez').fetchall()
        self.pushButton.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.izmen)
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        data=[]
        for row in bases:
            id_data, naz_data, opi_data, rez_data = row
            data.append(row)
        pix_list = []
        for i in base_img:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(i[0])
            pix_list.append(pixmap)
        for el in elem:
            if self.sender().text() == el[1]:
                self.label_nazvanie.setText(data[el[0]-1][1])
                self.label_pix.setPixmap(pix_list[el[0]-1])
                self.plainTextEdit.insertPlainText(data[el[0]-1][3])
                self.plainTextEdit_2.insertPlainText(data[el[0]-1][2])
    def izmen(self):
        self.pushButton_2.setText('Сохранить')
        self.plainTextEdit.setReadOnly(False)
        self.plainTextEdit_2.setReadOnly(False)
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_3.show()
        self.pushButton_4.show()
        self.pushButton_3.clicked.connect(self.saveimag)
        self.pushButton_4.clicked.connect(self.delete)
        
    def saveimag(self):
        filename = QFileDialog.getOpenFileName(self, 'Выберите изображение', '.', 'Images (*.png);;All Files (*)')
        filename = filename[0]
        with Image.open(filename) as img:
            img.load()

        pixmap = QtGui.QPixmap(filename)
        self.label_pix.setPixmap(pixmap)

        with open(filename, 'rb') as f:
            self.img_data = f.read()


    def save(self):
        con = sqlite3.connect('catalog.db')
        cur = con.cursor()
        self.pushButton_2.setText('Изменить')
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit_2.setReadOnly(True)
        self.pushButton_2.clicked.connect(self.save)
        ingrid = f"{self.plainTextEdit_2.toPlainText()}"
        rezep = f"{self.plainTextEdit.toPlainText()}"
        nazvan = self.label_nazvanie.text()
        if self.pushButton_3.sender():
            cur.execute("UPDATE catalogrez SET ingridient = ?, rezept = ?, images = ? WHERE nazvanie = ?", (ingrid, rezep, self.img_data, nazvan))
            con.commit()
        else:
            cur.execute("UPDATE catalogrez SET ingridient = ?, rezept = ? WHERE nazvanie = ?", (ingrid, rezep, nazvan))
            con.commit()
        con.close()
        self.pushButton_2.clicked.connect(self.izmen)

    def delete(self):
        con = sqlite3.connect('catalog.db')
        cur = con.cursor()
        nazvan = self.label_nazvanie.text()
        cur.execute("DELETE FROM catalogrez WHERE nazvanie = ?",(nazvan,))
        con.commit()
        self.back()
    def back(self):
        self.window_back = Catalog()
        self.window_back.show()
        self.close()
class Plus(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('plusrez.ui',self)
        self.setWindowTitle('All+: Добавление рецепта')
        self.img_data = None
        self.pushButton.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.save_rez)
        self.pushButton_3.clicked.connect(self.saveimag)
    def saveimag(self):
        filename = QFileDialog.getOpenFileName(self, 'Выберите изображение', '.', 'Images (*.png);;All Files (*)')
        filename = filename[0]
        with Image.open(filename) as img:
            img.load()
        pixmap = QtGui.QPixmap(filename)
        self.label_2.setPixmap(pixmap)
        with open(filename, 'rb') as f:
            self.img_data = f.read()
    def save_rez(self):
        con = sqlite3.connect('catalog.db')
        cur = con.cursor()
        allel = con.execute('SELECT id FROM catalogrez').fetchall()
        for i in allel:
            index, = i
        rezep = f"{self.plainTextEdit.toPlainText()}"
        ingrid = f"{self.plainTextEdit_2.toPlainText()}"
        nazvan = f"{self.plainTextEdit_3.toPlainText()}"
        result = cur.execute("SELECT id, rezept, ingridient, images, nazvanie FROM catalogrez WHERE id = ? AND rezept = ? AND ingridient = ? AND images = ? AND nazvanie = ?", (index, rezep, ingrid, self.img_data, nazvan,)).fetchone()
        if not index or not rezep or not ingrid or not nazvan or self.img_data == None:
            mess = QMessageBox() 
            mess.setWindowTitle("Ошибка") 
            mess.setText("Заполните все поля") 
            mess.setStandardButtons(QMessageBox.StandardButton.Ok) 
            mess.setIcon(QMessageBox.Icon.Critical) 
            mess.exec()
        elif result:
            mess = QMessageBox()
            mess.setWindowTitle("Ошибка")
            mess.setText("Данный рецепт уже существует")
            mess.setStandardButtons(QMessageBox.StandardButton.Ok)
            mess.setIcon(QMessageBox.Icon.Warning)
            mess.exec()
        else:
            cur.execute("INSERT INTO catalogrez (id, rezept, ingridient, images, nazvanie)  VALUES (?, ?, ?, ?, ?)", (index+1, rezep, ingrid, self.img_data, nazvan,))
            con.commit()
            mess = QMessageBox()
            mess.setWindowTitle("Успех")
            mess.setText("Рецепт создан")
            mess.setStandardButtons(QMessageBox.StandardButton.Ok)
            mess.setIcon(QMessageBox.Icon.Information)
            mess.exec()
    def back(self):
        self.window_main = Main()
        self.window_main.show()
        self.close()
app = QApplication(sys.argv)
ex = Registr()
ex.show()
sys.exit(app.exec())
