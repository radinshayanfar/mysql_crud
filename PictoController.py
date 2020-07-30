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

        self._view.tableGroupBox.buildTable(columns, rows)