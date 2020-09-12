from gpiozero import PWMOutputDevice
from controller import ControlThread
import threading

def dev_factory(type, **kwargs):
    if type == 'ledstrip':
        return Ledstrip(**kwargs)
    elif type == 'switch':
        return Switch(**kwargs)


class Device():

    def __init__(self, name, host_name, host_ip, power):
        self.name = name
        self.host_name = host_name
        self.host_ip = host_ip
        self.power = eval(power)

    def set_power(self, state):
        print(f'Changing the power of the {self.name} to {state}')
        if (state == 'off'):
            self.power = False
        elif (state == 'on'):
            self.power = True



class Ledstrip(Device):

    def __init__(self, name, host_name, host_ip, power, pins, presets, **kwargs):
        super().__init__(name, host_name, host_ip, power)

        self.r_pin = PWMOutputDevice(pins['R'], initial_value = 0)
        self.g_pin = PWMOutputDevice(pins['G'], initial_value = 0)
        self.b_pin = PWMOutputDevice(pins['B'], initial_value = 0)
        self.presets = presets
        self.c_thread = ControlThread(self, self.presets['MonoColor'])

    def set_power(self, state):
        super().set_power(state)
        if (state == 'off'):
            self.r_pin.off()
            self.g_pin.off()
            self.b_pin.off()

        elif (state == 'on'):
            self.set_color(0.3, 0, 0.3)

    def set_color(self, r, g, b):
        if (self.power):
            print(f'Changing the color of the {self.name} to [{r}, {g}, {b}]')
            self.r_pin.value = r
            self.g_pin.value = g
            self.b_pin.value = b

    def set_mode(self, mode):
        if self.c_thread.is_alive():
            self.c_thread.stop()
            print('Stopped the thread')
            self.c_thread.join()
            print('Killed the thread')

        self.c_thread = ControlThread(self, self.presets[mode])
        self.c_thread.start()


class Switch(Device):
    def __init__(self, name, host_name, host_ip, power, pins, **kwargs):
        super().__init__(name, host_name, host_ip, power)
        pass
