from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.utils import get_color_from_hex
from kivy.base import EventLoop
from kivy.graphics import Line, Color
from kivy.lang import Builder
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
import os

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
        """For keeping a button down always.
        """
        if self.state == "normal":
            ToggleButtonBehavior._do_press(self)

class CanvasWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            color = tuple(get_color_from_hex("#0080FF80"))
            Color(*color)
            Line(circle=(touch.x, touch.y, 25), width=4)
        return super().on_touch_down(touch)

    def clear_canvas(self):
        """Save the actual children (make a copy of them) later clear widgets
        and canvas, finally draw again the children.
        """
        saved = self.children[:]
        print(saved)
        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)
    
    def set_color(self, new_color):
        """Change the current color to a new color.

        Args:
            new_color (Color): The color to use.
        """
        print(new_color)
        with self.canvas:
            Color(*new_color)


class PaintApp(App):
    """Paint App. This the app class.

    Args:
        App (App): The app what's beeing executing.
    """
    def build(self):
        EventLoop.ensure_window()
        if EventLoop.window.__class__.__name__.endswith("Pygame"):
            try:
                from pygame import mouse
                from pygame.cursors import compile

                a, b = compile()
                mouse.set_cursor((24, 24), (9, 9), a, b)
            except:
                pass
        
        self.canvas_widget = CanvasWidget()
        self.canvas_widget.set_color(get_color_from_hex("#2980B9"))
        return self.canvas_widget


if __name__ == "__main__":
    Config.set("graphics", "width", 960)
    Config.set("graphics", "height", 540)
    Config.set("graphics", "resizable", "0")
    # Config.set('input', 'mouse', 'mouse,disable_multitouch')
    from kivy.core.window import Window

    Window.clearcolor = get_color_from_hex("#FFFFFF")
    PaintApp().run()
