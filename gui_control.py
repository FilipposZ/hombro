from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import coms_control


class HomeScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def power_switch(self, btn):
        if btn.state == 'normal':
            coms_control.send('ledstrip', 'power', 'off')
        elif btn.state == 'down':
            coms_control.send('ledstrip', 'power', 'on')

    def color_changed(self, col_value):
        coms_control.send('ledstrip', 'color', str(col_value))
        print(col_value)

    pass


class HombroApp(App):
    def build(self):
        return HomeScreen()

    def on_stop(self):
        coms_control.stop_coms()
