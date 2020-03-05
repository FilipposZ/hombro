import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import DictProperty, ListProperty,ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
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

    def power_switch(self, btn, name):
        if btn.state == 'normal':
            communications.send(name, 'power', 'off')
        elif btn.state == 'down':
            communications.send(name, 'power', 'on')

    def color_changed(self, instance, name, rgb_val):
        communications.send(name, 'color', str(rgb_val))

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


class SwitchScreen(Screen):

    def __init__(self, dev_data, **kwargs):
        super().__init__(**kwargs)

    def power_switch(self, btn, name):
        if btn.state == 'normal':
            communications.send(name, 'power', 'off')
        elif btn.state == 'down':
            communications.send(name, 'power', 'on')

class SettingsScreen(Screen):
    pass


class ScreenController(ScreenManager):
    devices = ListProperty()
    selected_device = StringProperty()

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.devices = config['devices']
        self.selected_device = self.devices[0]['name']


class HombroApp(App):

    def build(self):
        with open('config.json') as config_file:
            config = json.load(config_file) # Get the configuration file
        self.icon = 'icons/app_icon.png' # Set the logo of the app
        self.manager = ScreenController(config, transition = WipeTransition())
        for device in self.manager.devices:
            # For each device create a screen and add it to the screen controller
            if device['type'] == 'ledstrip':
                self.manager.add_widget(LedstripScreen(device, name = device['name']))
            elif device['type'] == 'switch':
                self.manager.add_widget(SwitchScreen(device, name = device['name']))

        self.manager.current = self.manager.selected_device
        return self.manager

    def on_stop(self):
        communications.stop_coms()
