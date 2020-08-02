import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from dotenv import load_dotenv, find_dotenv
from os import getenv
import sys
from PyQt5 import QtWidgets

from Controller import Controller
from view.UIMainWindow import UIMainWindow
from Model import Model

load_dotenv(find_dotenv())

db_config = {
    "host": getenv("DB_HOST"),
    "user": getenv("DB_USER"),
    "passwd": getenv("DB_PASS"),
    "database": getenv("DB_NAME"),
}

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    try:
        my_db = mysql.connector.connect(**db_config)
    except mysql.connector.Error as e:
        sys.exit(UIMainWindow.show_message(title="Error", text=str(e), icon=QMessageBox.Critical))

    MainWindow = QtWidgets.QMainWindow()
    ui = UIMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    model = Model(my_db)

    controller = Controller(view=ui, model=model)

    sys.exit(app.exec_())
