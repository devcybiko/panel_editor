# Panel Editor (Textual)

An application generator reminiscent of Visual Basic, but for Textual User Interfaces

- https://textual.textualize.io/

## Installation

- `./install.sh`

## Running the program

- `./run.sh`

## Keyboard Options

- 'Ctrl-p' - the Textual "palette" is displayed
- 'Ctrl-q' - quits the application immediately
- 'Ctrl-s' - saves the current state of the panel

## Creating Widgets

- "Right-click" on the background, a dialog will pop up giving you options to create new widgets
- Widgets can be edited by "Right-clicking" on the widget. A Properties Sheet will pop up
- Widgets can be "dragged" by holding down the right button and dragging the object around
- Widgets can be "resized" by "dragging" the lower right corner of the Widget
- A "Container" can hold a collection of widgets. Just drag-n-drop the widget into the container. Once dropped, it can be dragged within the container.
- An object can be removed from a Container by dragging it outside the Container and dropped on the main "panel"

## Buttons, Values, and Actions

- Buttons have a "command" property. It is a shell-script command that is executed when the button is "clicked."
- All the widgets' values will be exported into the shell's environment variables for use in the "command".
- The name of the Widget becomes the name of the environment variable.
- For Widgets inside of a Container, the name is "container-name_widget-name" (that is, the container and widget names separated by an underscore)
- The output of the Button Command is redirected to the "value" of another widget. The "Target" property of the button indicates which Widget will receive the output from the command.

## "Hidden" Widget Values

- You may not want all the Widget values to become environment variables upon a button-click.
- To facilitate "hidden" widget values, the Python convention of "underscore == private" is used.
- Any Widget whose name begins with an underscore is not exported to the command on a button-click.

## Widgets Properties

- Type: (non-modifiable) The type of the Widget (Button, Lable, Input, etc...)
- Name: the name of the widget. It is used to identify the widget for button-command output and sometimes as the visible label of the widget
- Label: The visible label of the Widget
- Value: Some Widgets have a value that is exported to the button-command shell. Different Widgets interpret the value differently (the DataTable uses CSV, the Tree uses JSON)
- Placeholder: For certain user-input fields (Text Input, TextArea) the placeholder is a "dimmed out" bit of text that is displayed when the input field is empty.
- Row: The row the Widget appears on (aka, 'y' coordinate)
- Col: The column the Widget appears on (aka, 'x' coordinate)
- Width: The horizontal size of the widget
- Height: The vertical size of the widget

### Button

- A Button is a clickable entity that has an 'action' or 'command associated it.
- Command: The shell command to execute when the button is clicked. All the panel's Widget values will be exported as environment variables. (You may add the Widget values using the shell "$" conventions. eg: `cat "$fname"` if fname were a Text Input Widget).
- Target: The on-screen Widget to receive the output from the Button-Command.
    - Note that different Widgets interpret the value in different ways. For example, the TextArea Widget will display the value as simple text. The DataTable will expect a Comma-Separated-Values format. And the Tree expects a JSON format.

### Data Table

- The Data Table is a grid of cells that resembles a spreadsheet.
- Data Table interprets its "value" as a comma-separated-values text string and displays it as a scrollable table with headers.
- Often, you do not want this exported during a Button-Command.
- To prevent exporting it, start the "name" property with an underscore "_" to make it "private."
- The values and structure of the Data Table are read-only to the user.

### Container

- The Container is a region in the screen that has a border and a Label. Other Widgets can be dragged into the Container.
- Containers may not contain other containers.
- Widgets can be dragged into the Container.
- And Widgets can be dragged out of the Container.
- Upon Button-Commands, the Widgets inside the container are exported as "container-name_widget-name". In other words, the container and widget names are separated by an underscore.

### Label

- The Label is a bit of static text - often used for labeling Text Input fields
- Labels are not resizable using the mouse.
- However you can set the Height property in the Property Sheet.

### Text Area

- The Text Area is a text input field that has both width and height allowing multiple rows of text to be input.

### Text Input

-  The Text Input is a single-line of text input.

### Tree

- The Tree Widget is a collapsible tree structure similar to the tree structure used to navigate file systems.
- The Tree Widget interprets its "value" property as JSON
- The values and structure of the Tree Widget are read-only to the user.
- Often, you do not want this exported during a Button-Command.
- To prevent exporting it, start the "name" property with an underscore "_" to make it "private."

## Saving

- "Ctrl-S" will save the panel to a single file 'a.json'
- In this pre-release version there is no facility to save to a user-selected file

## Loading

- The file 'a.json' is loaded when the Panel Editor starts up. 
- In this pre-release version there is no facility to load from a user-selected file

## Undo

- There is no "undo" key in the pre-release version.
- So, save early and save often.
- bump
