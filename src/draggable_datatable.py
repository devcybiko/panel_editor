from dataclasses import dataclass
from textual.widgets import DataTable
from draggable_widget import DraggableWidget
from properties_widget import PropertiesWidget
import csv

@dataclass
class DataTableProperties:
    type: str = "DataTable"
    name: str = "_"
    value: str = ""
    row: int = 0
    col: int = 0
    width: int = 40
    height: int = 3
    placeholder: str = "placeholder"

class DraggableDataTable(DraggableWidget, PropertiesWidget, DataTable):    
    def __init__(self, props: DataTableProperties = None, *args, **kwargs):
        if props is None:
            props = DataTableProperties()
        DataTable.__init__(self, classes="draggable-datatable", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        self.update()
    
    def update(self, props=None):
        super().update(props)
        self.border_title = self.props.name
        if not self.props.value:
            self.clear(columns=True)
            return
        n_cols = 0
        i = 0
        with open("people-100.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                i += 1
                if i == 1:
                    n_cols = len(row)
                    self.clear(columns=True)
                    self.add_columns(*row)
                    continue
                if len(row) != n_cols:
                    self.app.notify(f"DataTable: ERROR: Row {i} has {len(row)} columns, expected {n_cols}. Row skipped.")
                    continue
                self.add_row(*row)
