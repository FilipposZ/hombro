from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import communications


class HomeScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def power_switch(self, device):
        if device.state == 'normal':
            communications.send(device.name, 'power', 'off')
        elif device.state == 'down':
            communications.send(device.name, 'power', 'on')

    def color_changed(self, device, col_value):
        communications.send(device.name, 'color', str(col_value))

    pass


class HombroApp(App):
    def build(self):
        return HomeScreen()

    def on_stop(self):
        communications.stop_coms()
