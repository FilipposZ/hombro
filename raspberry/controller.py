import threading
import time
from itertools import cycle

class ControlThread(threading.Thread):
    def __init__(self, device, colors):
        print('Creating thread')
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.device = device
        self.colors = colors

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def run(self):
        print('Running thread')
        if len(self.colors) == 1:
            self.device.set_color(*self.colors[0]['color'])
        else:
            for col_params in cycle(self.colors):
                if self.stopped():
                    print('Returning from loop thread')
                    return
                color = col_params['color']
                duration = col_params['duration']

                self.device.set_color(*color)
                time.sleep(duration)
