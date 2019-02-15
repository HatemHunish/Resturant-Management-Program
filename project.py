import datetime
import sqlite3
import sys
import time
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem

from backend import Datebase
datebase = Datebase("book.db")
selected_row = None


class Food_App(QtWidgets.QMainWindow):
    def __init__(self):
        super(Food_App, self).__init__()
        uic.loadUi('interface.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.tableWidget.setColumnCount(2)

        self.pushButton_9.clicked.connect(self.add_command)
        self.pushButton_6.clicked.connect(self.search_command)
        self.pushButton_7.clicked.connect(self.view_command)
        # self.listWidget.itemClicked.connect(self.select)
        self.pushButton_8.clicked.connect(self.delete_command)
        self.pushButton_10.clicked.connect(self.update_command)
        self.tableWidget.clicked.connect(self.select)
        self.pushButton_11.clicked.connect(self.clear)
        self.pushButton_12.clicked.connect(self.printf)
        self.exitbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.minbtn.clicked.connect(lambda: self.showMinimized())

    def clear(self):
        self.Name_I.clear()
        self.Meal_I.clear()
        self.Price_I.clear()
        self.Pay_I.clear()
        self.plainTextEdit.clear()

    def printf(self):
        datebase.printf()

    def select(self):
        global selected_row

        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(),
                  currentQTableWidgetItem.text())
            selected_row = currentQTableWidgetItem.row()
            print("test", currentQTableWidgetItem.text())
        self.ass()

    def add_command(self):
        Name = self.Name_I.text()
        Meal = self.Meal_I.text()
        Price = self.Price_I.text()
        Payment = self.Pay_I.text()
        Date = datetime.datetime.now()
        Note = self.plainTextEdit.toPlainText()
        datebase.insert(Name, Date, Meal,
                        Price, Payment, Note)
        self.view_command()

    def search_command(self):
        self.tableWidget.setRowCount(datebase.count())
        Name = self.Name_I.text()
        Meal = self.Meal_I.text()
        Price = self.Price_I.text()
        Payment = self.Pay_I.text()
        Date = datetime.datetime.now()
        i = -1
        for row in datebase.search(Name, Date,
                                   Meal, Price, Payment):
            i = i+1
            print(row)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(f"{row[1]}"))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(f"{row[2]}"))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(f"{row[3]}"))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(f"{row[4]}"))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(f"{row[5]}"))
            self.tableWidget.item(i, 0).setBackground(
                QtGui.QColor(124, 252, 0))

    def view_command(self):
        i = -1
        self.tableWidget.setRowCount(datebase.count())
        for row in datebase.view():
            i = i+1
            # print(i, row[1])
            self.tableWidget.setItem(i, 0, QTableWidgetItem(f"{row[1]}"))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(f"{row[2]}"))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(f"{row[3]}"))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(f"{row[4]}"))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(f"{row[5]}"))

    def delete_command(self):
        index = self.ass()
        if index is not None:

            datebase.delete(index)
            # print(index)
            self.view_command()

        else:
            QMessageBox.about(self, "Error", "Nohing To Delete")
        index = None

    def update_command(self):
        Name = self.Name_I.text()
        Meal = self.Meal_I.text()
        Price = self.Price_I.text()
        Payment = self.Pay_I.text()
        Date = datetime.datetime.now()
        Note = self.plainTextEdit.toPlainText()
        datebase.update(selected_row+1, Name, Date,
                        Meal, Price, Payment, Note)
        self.view_command()

    def ass(self):

        new = []
        i = -1
        for row in datebase.view():
            i = i+1
            new.insert(i, row)
        print(new)
        if selected_row is not None:

            self.Name_I.setText(str(new[selected_row][1]))
            self.Meal_I.setText(str(new[selected_row][3]))
            self.Price_I.setText(str(new[selected_row][4]))
            self.Pay_I.setText(str(new[selected_row][5]))
            self.plainTextEdit.setPlainText(str(new[selected_row][6]))
            return(str(new[selected_row][0]))

        else:
            QMessageBox.about(self, "Error", "Nohing To Delete")


app = QtWidgets.QApplication([])
win = Food_App()
win.show()
sys.exit(app.exec())
