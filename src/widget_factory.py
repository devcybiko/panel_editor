from dataclasses import dataclass


class WidgetFactory:
    @staticmethod
    def from_properties(props: dataclass) -> any:
        from draggable_button import DraggableButton
        from draggable_container import DraggableContainer
        from draggable_input import DraggableInput
        from draggable_label import DraggableLabel
        from draggable_textarea import DraggableTextArea
        from draggable_datatable import DraggableDataTable
        from draggable_tree import DraggableTree

        """Create a widget instance based on its properties type"""
        if props.type == "Button":
            return DraggableButton(props)
        elif props.type == "Container":
            return DraggableContainer(props)
        elif props.type == "DataTable":
            return DraggableDataTable(props)
        elif props.type == "Input":
            return DraggableInput(props)
        elif props.type == "Label":
            return DraggableLabel(props)
        elif props.type == "TextArea":
            return DraggableTextArea(props)
        elif props.type == "Tree":
            return DraggableTree(props)
        else:
            raise ValueError(f"Unknown widget type: {props.type}")
    