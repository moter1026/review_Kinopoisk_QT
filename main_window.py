from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QScrollArea, QFileDialog, QSizePolicy, QMessageBox, QLineEdit
                            

import sys

from iterator import Iterator
import copy_dataset
import copy_dataset_random
import description

class ButtonYellow(QPushButton):
    def __init__(self, str: str):
        super().__init__()
        self.setFixedSize(QSize(100,50))
        self.setStyleSheet("background-color: yellow; border: 1px solid black; border-radius:10px;")
        self.adjustSize()
        # self.move(200, 200)
        
        self.setText(str)

class ButtonBlack(QPushButton):
    def __init__(self, str: str):
        super().__init__()
        self.setFixedSize(QSize(200,50))
        # self.setMaximumWidth(100)
        self.setStyleSheet("background-color: black; border: 1px solid white; border-radius:10px; color: white; width: 100px; white-space: pre-line;")
        self.adjustSize()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))
        # self.move(200, 200)
        
        self.setText(str)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # базовые настройки главного окна
        self.setWindowTitle("Lab3-main window")
        # self.setFixedSize(QSize(1000,600))
        self.setMinimumSize(QSize(1000,600))
        self.setStyleSheet("background-color: #E1E8FF;")

        # Создаю итераторы каждого класса для получения след и пред комментариев
        self.goodReview = Iterator("good")
        self.badReview = Iterator("bad")

        # Создаю кнопки для графического интерфейса
        self.button = ButtonYellow("След.")
        self.button2 = ButtonYellow("Пред.")

        # Создаю Лэйбл для отображения комментариев.
        # .setWordWrap(), чтобы текст автоматически переносился на другую строку
        self.textLabel = QLabel()
        self.textLabel.setWordWrap(True)
        self.textLabel.setText("Нажмите на кнопку 'Следующий комментарий'")
        self.textLabel.adjustSize()
        

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.textLabel)
        self.scrollArea.setFixedSize(QSize(600, 600))

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.button)
        vlayout.addWidget(self.button2)
        

        hlayout = QHBoxLayout()
        hlayout.setSpacing(5)
        hlayout.setContentsMargins(5, 0, 5, 0)
        # hlayout.addWidget(self.button2)
        hlayout.addWidget(self.scrollArea)
        hlayout.addLayout(vlayout)
        # hlayout.addWidget(button)

        self.button.setCheckable(True)
        self.button.clicked.connect(self.nextGoodReview)
        self.button2.clicked.connect(self.prevGoodReview)
        
        

        widget = QWidget()
        widget.setLayout(hlayout)
        self.setCentralWidget(widget)
   
    def nextGoodReview(self):
        try:
            path_of_review = self.goodReview.__next__()
            text_of_review = ""
            try_encodings = ["utf-8", "utf-8-sig", "cp1251", "latin-1"]

            for encoding in try_encodings:
                try:
                    with open(path_of_review, "r", encoding=encoding) as readFile:
                        text_of_review = readFile.read()
                    break  # Прерываем цикл, если декодирование успешно
                except UnicodeDecodeError:
                    continue  # Переходим к следующей кодировке, если декодирование не удалось
                
            self.textLabel.setText("good\n" + text_of_review)
            self.textLabel.adjustSize()
        except FileNotFoundError:
            warning_box = QMessageBox()
            warning_box.setIcon(QMessageBox.Icon.Warning)
            warning_box.setWindowTitle("Предупреждение")
            warning_box.setText("Сначала необходимо сделать копию датасета с рандомными числами")
            warning_box.exec()
    
    def nextBadReview(self):
        try:
            path_of_review = self.badReview.__next__()
            text_of_review = ""
            try_encodings = ["utf-8", "utf-8-sig", "cp1251", "latin-1"]

            for encoding in try_encodings:
                try:
                    with open(path_of_review, "r", encoding=encoding) as readFile:
                        text_of_review = readFile.read()
                    break  # Прерываем цикл, если декодирование успешно
                except UnicodeDecodeError:
                    continue  # Переходим к следующей кодировке, если декодирование не удалось
            self.textLabel.setText("bad\n" + text_of_review)
            self.textLabel.adjustSize()
        except FileNotFoundError:
            warning_box = QMessageBox()
            warning_box.setIcon(QMessageBox.Icon.Warning)
            warning_box.setWindowTitle("Предупреждение")
            warning_box.setText("Сначала необходимо сделать копию датасета с рандомными числами")
            warning_box.exec()


    def prevGoodReview(self):
        if self.goodReview.counter <= 1:
            return
        path_of_review = self.goodReview.elem[-2]
        # print(path_of_review)
        text_of_review = ""
        try_encodings = ["utf-8", "utf-8-sig", "cp1251", "latin-1"]

        for encoding in try_encodings:
            try:
                with open(path_of_review, "r", encoding=encoding) as readFile:
                    text_of_review = readFile.read()
                    self.goodReview.elem.remove(self.goodReview.elem[-1])
                    self.goodReview.counter -= 1
                break  # Прерываем цикл, если декодирование успешно
            except UnicodeDecodeError:
                continue  # Переходим к следующей кодировке, если декодирование не удалось
        self.textLabel.setText("good\n" + text_of_review)
        self.textLabel.adjustSize()
    
    def prevBadReview(self):
        if self.badReview.counter <= 1:
            return
        path_of_review = self.badReview.elem[-2]
        text_of_review = ""
        try_encodings = ["utf-8", "utf-8-sig", "cp1251", "latin-1"]

        for encoding in try_encodings:
            try:
                with open(path_of_review, "r", encoding=encoding) as readFile:
                    text_of_review = readFile.read()
                    self.badReview.elem.remove(self.badReview.elem[-1])
                    self.badReview.counter -= 1
                break  # Прерываем цикл, если декодирование успешно
            except UnicodeDecodeError:
                continue  # Переходим к следующей кодировке, если декодирование не удалось
        self.textLabel.setText("bad\n" + text_of_review)
        self.textLabel.adjustSize()

    
    def makeDescriptionAnyFolders(self):
        try:
            if self.lineEditForAnyDescription.text() == "":
                warning_box = QMessageBox()
                warning_box.setIcon(QMessageBox.Icon.Warning)
                warning_box.setWindowTitle("Предупреждение")
                warning_box.setText("Вы не ввели название для нового файла!")
                warning_box.exec()
                return
            folderpath = QFileDialog.getExistingDirectory(self, 'Выберите папку, для создания описания')
            description.make_description(self.lineEditForAnyDescription.text(), folderpath)
        except Exception as e:
            warning_box = QMessageBox()
            warning_box.setIcon(QMessageBox.Icon.Warning)
            warning_box.setWindowTitle("Предупреждение")
            warning_box.setText("Это предупреждение!")
            warning_box.exec()

    



if __name__ == "__main__":
    app = QApplication(sys.argv) 

    app.setWindowIcon(QIcon("./img/apple.svg"))

    window = MainWindow()
    window.show()

    app.exec()