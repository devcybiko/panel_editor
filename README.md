# Panel Editor (Textual)

A collection of simple Textual applications demonstrating input fields and user interfaces.

- https://textual.textualize.io/

## Programs

### 1. Simple Input App (`simple_input.py`)
A basic Textual app featuring:
- A text input field with a label
- Real-time feedback as you type
- Clean, centered layout

### 2. Advanced Input App (`advanced_input.py`)
A more sophisticated form with:
- Multiple input fields (first name, last name, email)
- Input validation
- Submit and Clear buttons
- Result display with feedback

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Programs

### Simple Input App
```bash
python simple_input.py
```

### Advanced Input App
```bash
python advanced_input.py
```

## Features Demonstrated

- **Input widgets** with placeholders and validation
- **Label widgets** for text display and user feedback
- **CSS styling** for layout and appearance
- **Event handling** for input changes and button presses
- **Container layouts** (Vertical, Horizontal) for organization
- **Real-time updates** as users interact with the interface

## Key Concepts

- `Input.Changed` event handling for real-time feedback
- CSS styling with Textual's built-in design system
- Widget querying with `query_one()` for accessing specific widgets
- Validation using Textual's validation system
- Responsive layout with containers and proper alignment

# panel_editor
# panel_editor
