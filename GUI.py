import json
from functools import partial
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
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


class BasicDevice():
    def power_switch(self, btn, name):
        if btn.state == 'normal':
            communications.send(name, 'power', 'off')
        elif btn.state == 'down':
            communications.send(name, 'power', 'on')


class LedstripScreen(Screen, BasicDevice):

    preset_btns = ObjectProperty()
    active_preset = StringProperty()
    presets = DictProperty()

    def __init__(self, dev_data, **kwargs):
        super().__init__(**kwargs)
        # For each preset, add to the dictionary preset_params the parameters of the
        # preset and create the corresponding buttons.
        self.presets = dev_data['presets']
        self.active_preset = dev_data['default_preset']
        for pr_name, params in self.presets.items():
            btn = PresetButton(text = pr_name, halign = 'center')
            btn.bind(on_press = self.change_active_preset)
            if self.active_preset == pr_name:
                btn.state = 'down'
            self.preset_btns.add_widget(btn)

    def color_changed(self, instance, name, rgb_val):
        communications.send(name, 'color', str(rgb_val))

    def change_active_preset(self, preset_btn):
        if (preset_btn.state == 'down'):
            self.active_preset = preset_btn.text
            communications.send(self.name, 'mode', self.active_preset)

    def add_color_to_preset(self, rgb_val):
        # Adds the currently selected color to the active preset.
        print(f'Adding color = {rgb_val} , with duration = 1')

    def switch_to_preset_edit(self, btn, scrn_manager):
        # If the screen already exists, delete it
        if scrn_manager.has_screen('preset_edit'):
            scrn_manager.remove_widget(scrn_manager.get_screen('preset_edit'))

        # Add the new preset edit screen and change to it
        scrn_manager.add_widget(PresetEditScreen(self.presets, self.active_preset, name = 'preset_edit'))
        scrn_manager.current = 'preset_edit'

class SwitchScreen(Screen, BasicDevice):

    def __init__(self, dev_data, **kwargs):
        super().__init__(**kwargs)


class PresetEditScreen(Screen):
    presets = DictProperty()
    active_preset = StringProperty()

    def __init__(self, presets, active_preset, **kwargs):
        super().__init__(**kwargs)
        self.presets = presets
        self.active_preset = active_preset

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
        config = communications.config
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
