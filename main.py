#!/usr/bin/env python
"""Paint App.

This module contains the logic to manipulate the paint app.

Todo:
    Add more feature to the app.
    
Copyright 2021
"""
import os

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.utils import get_color_from_hex
from kivy.graphics import Line, Color
from kivy.lang import Builder
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton


kv_path: str = "./kv/"
for kv in os.listdir(kv_path):
    Builder.load_file(kv_path + kv)


class RadioButton(ToggleButton):
    """A toggle button with the characteristic of a radio button. I mean, one
    button must be down.

    Args:
        ToggleButton (ToggleButton): The parent class for this.
    """

    def _do_press(self):
        """For keeping a button down always."""
        if self.state == "normal":
            ToggleButtonBehavior._do_press(self)


class CanvasWidget(Widget):
    line_width: int = 2

    def on_touch_down(self, touch):
        """First, verifies that the button is not pressed. If it is, return.
        Later, draw a circle with the touch x and y coordinates of the mouse.

        Args:
            touch (MotionEvent): The mouse event.

        Returns:
            None: Calling superclass' method.
        """
        if Widget.on_touch_down(self, touch):
            return
        
        with self.canvas:
            touch.ud["current_line"] = Line(
                points=(touch.x, touch.y,), width=self.line_width
            )
    
    def on_touch_move(self, touch):
        if 'current_line' in touch.ud:
            touch.ud['current_line'].points += (touch.x, touch.y)

    def set_line_width(self, line_width="normal"):
        self.line_width = {"Thin": 1, "Normal": 2, "Thick": 3}[line_width]
        
    def clear_canvas(self):
        """Save the actual children (make a copy of them) later clear widgets
        and canvas, finally draw again the children.
        """
        saved = self.children[:]
        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)

    def set_color(self, new_color):
        """Change the current color to a new color.

        Args:
            new_color (Color): The color to use.
        """
        with self.canvas:
            Color(*new_color)


class PaintApp(App):
    """Paint App. This the app class.

    Args:
        App (App): The app what's beeing executing.
    """

    def build(self):
        self.canvas_widget = CanvasWidget()
        self.canvas_widget.set_color(get_color_from_hex("#2980B9"))
        return self.canvas_widget


if __name__ == "__main__":
    Config.set("graphics", "width", 960)
    Config.set("graphics", "height", 540)
    # Config.set("graphics", "resizable", "0")
    # Config.set('input', 'mouse', 'mouse,disable_multitouch')
    Config.set("kivy", "window_icon", "./img/icon.png")
    from kivy.core.window import Window

    Window.clearcolor = get_color_from_hex("#FFFFFF")
    PaintApp().run()
