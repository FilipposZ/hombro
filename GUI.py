import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import DictProperty, ListProperty,ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from utilitywidgets import FloatInput, PresetButton
import communications

class LedstripScreen(Screen):

    preset_btns = ObjectProperty()
    preset_data = DictProperty()

    def __init__(self, dev_data, **kwargs):
        super().__init__(**kwargs)
        self.preset_btns.active_preset = dev_data['default_preset']
        # For each preset, add to the dictionary preset_params the parameters of the
        # preset and create the corresponding buttons.
        self.preset_data = dev_data['presets']
        for pr_name, params in self.preset_data.items():
            btn = PresetButton(text = pr_name, halign = 'center')
            btn.bind(on_press = self.preset_clicked)
            if self.preset_btns.active_preset == pr_name:
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
        if (preset_btn.state == 'down'):
            name = preset_btn.text
            self.preset_btns.active_preset = name
            print(name)

    def add_color_to_preset(self, rgb_val):
        # Adds the currently selected color to the active preset.
        pr_name = self.preset_btns.active_preset
        self.preset_data[pr_name].append({'color': rgb_val, 'duration': 1})

        print(self.preset_data[pr_name][-1])

class SettingsScreen(Screen):
    pass


class ScreenController(ScreenManager):
    devices = ListProperty()

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.devices = config['devices']

    pass



class HombroApp(App):

    def build(self):
        with open('config.json') as config_file:
            config = json.load(config_file) # Get the configuration file
        self.icon = 'icons/app_icon.png' # Set the logo of the app
        self.scrn_ctrl = ScreenController(config)
        for device in config['devices']:
            # For each device create a screen and add it to the screen controller
            if device['type'] == 'ledstrip':
                self.scrn_ctrl.add_widget(LedstripScreen(device, name = device['name']))

        return self.scrn_ctrl

    def on_stop(self):
        communications.stop_coms()
