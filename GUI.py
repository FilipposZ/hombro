import json
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from utilitywidgets import FloatInput
import communications

class HomeScreen(BoxLayout):

    preset_btns = ObjectProperty()
    preset_data = {}

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        # For each preset, add to the dictionary preset_params the parameters of the
        # preset and create the corresponding buttons.
        self.preset_data = config['presets']
        print(self.preset_data)
        for pr_name, params in self.preset_data.items():
            btn = ToggleButton(text = pr_name, group = 'presets')
            btn.bind(on_press = self.preset_clicked)
            self.preset_btns.add_widget(btn)


    def power_switch(self, device):
        if device.state == 'normal':
            communications.send(device.name, 'power', 'off')
        elif device.state == 'down':
            communications.send(device.name, 'power', 'on')

    def color_changed(self, device, rgb_val):
        communications.send(device.name, 'color', str(rgb_val))

    def preset_clicked(self, preset):
        name = preset.text
        print(name)

    def add_color_to_preset(self, rgb_val):
        # Find the currently active preset
        for btn in self.preset_btns.children:
            if btn.state == 'down':
                self.preset_data[btn.text].append({'color': rgb_val, 'duration': duration})

                print(self.preset_data[btn.text][-1])


class HombroApp(App):

    def build(self):
        with open('config.json') as config_file:
            config = json.load(config_file)
        return HomeScreen(config)

    def on_stop(self):
        communications.stop_coms()
