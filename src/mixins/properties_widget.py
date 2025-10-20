from dataclasses import dataclass
from textual.events import MouseDown, MouseUp, MouseMove
from properties_sheet import PropertiesSheet
from widget_factory import WidgetFactory

class PropertiesWidget:
    def __init__(self, props: dataclass, *args, **kwargs):
        self.props = props
        self.type = props.type

    def _update_widget(self, field_name: str, field_value) -> None:
        if field_name in ("row", "col"):
            new_x = self.props.col
            new_y = self.props.row
            self.styles.offset = (new_x, new_y)
            return
        
        if hasattr(self.styles, field_name):
            setattr(self.styles, field_name, field_value)
            return
        
        if field_name in ("name"):
            # These are dataclass-only properties, not widget attributes
            # GLS - should "name" be the "id" of the widget?
            return
            
        if hasattr(self, field_name):
            setattr(self, field_name, field_value)
            return
    
        return
    
    def update(self, props=None):
        if not props:
            props = self.props
        
        # Handle both dictionary and dataclass properties
        if hasattr(props, 'items'):
            # Dictionary-like object
            items = props.items()
        else:
            # Dataclass object - convert to field_name, field_value pairs
            from dataclasses import fields, is_dataclass
            if is_dataclass(props):
                items = [(field.name, getattr(props, field.name)) for field in fields(props)]
            else:
                return  # Can't process this type
        
        # Handle dataclass properties
        for field_name, field_value in items:
            ## skip it if it is from a property sheet that doesnt have our prop
            if not hasattr(self.props, field_name):
                continue
            
            # Update the dataclass property
            setattr(self.props, field_name, field_value)
            
            # Apply changes using convention-based mapping
            self._update_widget(field_name, field_value)

    def show_properties_sheet(self) -> None:
        self.app.push_screen(PropertiesSheet(self, f"{self.type} Properties"), self.update)
    
    def copy_props(self):
        from dataclasses import replace
        return replace(self.props)
    
    def clone(self):
        cloned_props = self.copy_props()
        return WidgetFactory.create_widget(cloned_props)

    def clone_and_mount(self):
        cloned_props = self.copy_props()
        cloned_props.name = "_"
        cloned_props.row += 3
        new_widget = WidgetFactory.from_properties(cloned_props)
        self.parent.mount(new_widget)