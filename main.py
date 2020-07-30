import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from dotenv import load_dotenv, find_dotenv
from os import getenv
import sys
from PyQt5 import QtWidgets
from PictoMainWindow import PictoMainWindow

load_dotenv(find_dotenv())

db_config = {
    "host": getenv("DB_HOST"),
    "user": getenv("DB_USER"),
    "passwd": getenv("DB_PASS"),
    "database": getenv("DB_NAME"),
}


def show_message(title, text, icon=None, parent=None):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)

    return msg.exec()


def db_connect():
    my_db = mysql.connector.connect(**db_config)
    my_cursor = my_db.cursor()

    return my_db, my_cursor


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    try:
        my_db, db_cursor = db_connect()
    except mysql.connector.Error as e:
        sys.exit(show_message(title="Error", text=str(e), icon=QMessageBox.Critical))

    MainWindow = QtWidgets.QMainWindow()
    ui = PictoMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
