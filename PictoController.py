import mysql.connector
from PyQt5.QtWidgets import QMessageBox

from PictoMainWindow import PictoMainWindow
from PictoModel import PictoModel


class PictoController:
    def __init__(self, view: PictoMainWindow, model: PictoModel):
        self._view = view
        self._model = model

        tables = self._model.get_tables()
        self._view.sideListWidget.addItems(tables)
        self._view.sideListWidget.currentItemChanged.connect(self.new_table_clicked)
        self._view.statusbar.messageChanged.connect(self.statusBarMessageChanged)

    def new_table_clicked(self, new, prev):
        self._load_table(new.text())

    def _load_table(self, table_name=None):
        columns, rows, prev_en, next_en = self._model.get_table(table_name)
        self._view.statusbar.showMessage(self._model.get_status_message(update_count=True))
        self._view.tableGroupBox.buildTable(columns, rows, self.tableClick, self.paginationClicked, prev_en, next_en)

    def tableClick(self, action: str, row_index: int = 0):
        try:
            if action == "insert":
                row = [ln.text() for ln in self._view.tableGroupBox.insertLineEdits]
                self._model.insert_row(row)
                self._load_table()
                return

            row = [ln.text() for ln in self._view.tableGroupBox.tableLineEdits[row_index]]
            if action == "update":
                self._model.update_row(row, row_index)
            else:
                self._model.delete_row(row_index)
                self._load_table()
        except mysql.connector.Error as e:
            PictoMainWindow.show_message(title="Error", text=str(e), icon=QMessageBox.Critical,
                                         parent=self._view.centralwidget)

    def paginationClicked(self, dir: str):
        if dir == "next":
            self._model.next_page()
        else:
            self._model.prev_page()
        self._load_table()

    def statusBarMessageChanged(self, new_msg):
        if new_msg == '':
            self._view.statusbar.showMessage(self._model.get_status_message(update_count=True))
