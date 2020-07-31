from PictoMainWindow import PictoMainWindow
from PictoModel import PictoModel


class PictoController:
    def __init__(self, view: PictoMainWindow, model: PictoModel):
        self._view = view
        self._model = model

        tables = self._model.get_tables()
        self._view.sideListWidget.addItems(tables)
        self._view.sideListWidget.currentItemChanged.connect(self.new_table_clicked)

    def new_table_clicked(self, new, prev):
        self._load_table(new.text())

    def _load_table(self, table_name=None):
        columns, rows = self._model.get_table(table_name)

        self._view.tableGroupBox.buildTable(columns, rows, self.tableClick)

    def tableClick(self, action: str, row_index: int = 0):
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
