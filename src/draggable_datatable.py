from dataclasses import dataclass
import io
import os
from textual.widgets import DataTable
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget
from mixins.filebacked_widget import FilebackedWidget
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
    backing_file: str = ""
    readonly: bool = True

class DraggableDataTable(DraggableWidget, PropertiesWidget, FilebackedWidget, DataTable):    
    def __init__(self, props: DataTableProperties = None, *args, **kwargs):
        if props is None:
            props = DataTableProperties()
        DataTable.__init__(self, classes="draggable-datatable", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        FilebackedWidget.__init__(self)
        self.update()
    
    def update(self, props=None):
        super().update(props)
        self.border_title = self.props.name
        self.backingfile_update()
        if self.last_value == self.props.value:
            return
        if not self.props.value:
            self.clear(columns=True)
            return
        n_cols = 0
        i = 0
        reader = csv.reader(io.StringIO(self.props.value))
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
