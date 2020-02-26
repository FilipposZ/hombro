import json
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from utilitywidgets import FloatInput, PresetButton
import communications

class HomeScreen(BoxLayout):

    preset_btns = ObjectProperty()
    preset_data = {}

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        # For each preset, add to the dictionary preset_params the parameters of the
        # preset and create the corresponding buttons.
        self.preset_data = config['presets']
        for pr_name, params in self.preset_data.items():
            btn = PresetButton(text = pr_name, halign = 'center')
            if pr_name == self.preset_btns.active_btn:
                btn.state = 'down'
            self.preset_btns.add_widget(btn)

    def power_switch(self, device):
        if device.state == 'normal':
            communications.send(device.name, 'power', 'off')
        elif device.state == 'down':
            communications.send(device.name, 'power', 'on')

    def color_changed(self, device, rgb_val):
        communications.send(device.name, 'color', str(rgb_val))

    def preset_clicked(self, preset_btn):
        name = preset_btn.text
        if (preset_btn.state == 'down'):
            self.preset_btns.active_btn = name
            print(name)

    def add_color_to_preset(self, rgb_val):
        # Adds the currently selected color to the active preset.
        pr_name = self.preset_btns.active_btn
        self.preset_data[pr_name].append({'color': rgb_val, 'duration': 1})

        print(self.preset_data[pr_name][-1])


class HombroApp(App):

    def build(self):
        with open('config.json') as config_file:
            config = json.load(config_file)
        return HomeScreen(config)

    def on_stop(self):
        communications.stop_coms()
