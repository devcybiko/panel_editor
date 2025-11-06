from dataclasses import dataclass
from properties_sheet import PropertiesSheet
from widget_factory import WidgetFactory

class text(str):
    """A type hint for multi-line or long text fields."""
    pass

class code(str):
    """A type hint for multi-line code fields."""
    pass

class PropertiesWidget:
    def __init__(self, props: dataclass, *args, **kwargs):
        self.props = props
        self.type = props.type
        self.props_hash = None

    def _update_widget_member(self, property_name: str, property_value) -> None:
        if property_name in ("row", "col"):
            new_x = self.props.col
            new_y = self.props.row
            self.styles.offset = (new_x, new_y)
            return

        if property_name in ("name", "border"):
            # These are dataclass-only properties, not widget attributes
            # GLS - should "name" be the "id" of the widget?
            return

        if hasattr(self.styles, property_name):
            setattr(self.styles, property_name, property_value)
            return
                    
        if hasattr(self, property_name):
            if property_name in ("language"):
                # Special handling for TextArea code editor properties
                if self.language == self.props.language:
                    return
            if property_name in ("placeholder"):
                # Special handling for TextArea code editor properties
                self.placeholder = self.props.placeholder or self.props.name
                return
            if self.type == "Checkbox" and property_name == "value":
                # Special handling for Checkbox value property
                return
            setattr(self, property_name, property_value)
            return
    
        return
    
    def update(self, props=None):
        from dataclasses import fields, is_dataclass
        if props is None:
            props = self.props
        props_hash = hash(str(props))
        if self.props_hash == props_hash:
            return
        self.props_hash = props_hash
        
        if hasattr(props, 'items'):
            # Dictionary-like object
            items = props.items()
        elif is_dataclass(props):
            # Dataclass object - convert to field_name, field_value pairs
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
            self._update_widget_member(field_name, field_value)
        self.refresh()

    def show_properties_sheet(self) -> None:
        self._debug(f"Showing properties sheet for {self.props.name} ({self.props.type})")
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
