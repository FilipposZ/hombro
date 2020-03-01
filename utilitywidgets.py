from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label

import re

class PresetButton(ToggleButton):
    pass


class DeviceButton(ToggleButton):
    pass


class FloatInput(TextInput):
# A widget that allows the user to input as text only float data.
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class Separator(Widget):
    color = ListProperty()


class OverlayView(ModalView):

    device_btns = ObjectProperty()

    def __init__(self, devices, **kwargs):
        super().__init__(**kwargs)
        for device in devices:
            # For each device add an instance to the dropdown list
            btn = DeviceButton(text = device['name'])
            self.device_btns.add_widget(btn)


class NavigationBar(BoxLayout):
    overlay_btn = ObjectProperty()
    devices = ListProperty()
    selected_dev = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_devices(self, instance, value):
        self.overlay = OverlayView(self.devices, attach_to = self.overlay_btn)
