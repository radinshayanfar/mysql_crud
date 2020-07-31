from PictoMainWindow import PictoMainWindow
from PictoModel import PictoModel


class PictoController:
    def __init__(self, view: PictoMainWindow, model: PictoModel):
        self._view = view
        self._model = model

        tables = self._model.get_tables()
        self._view.sideListWidget.addItems(tables)
        self._view.sideListWidget.currentItemChanged.connect(self.show_new_table)

    def show_new_table(self, new, prev):
        columns, rows = self._model.get_table(new.text())

        self._view.tableGroupBox.buildTable(columns, rows, self.tableClick)

    def tableClick(self, action: str, row_index: int):
        row = [ln.text() for ln in self._view.tableGroupBox.lineEdits[row_index]]
        if action == "update":
            self._model.update_row(row, row_index)
        else:
            # self._model.update_row(row)
            pass
        t = type(5)