import types


class Signals:

    names = (
        'on_load', 'on_start', 'on_pause',
        'on_end', 'on_simulate', 'on_collision'
    )

    def __init__(self):
        self.signals = {}

    def clear_all(self):
        self.signals = {}

    def emit(self, signal):
        if signal in self.signals:
            try:
                self.signals[signal]()
            except Exception as e:
                print(e)

    def connect(self, signal, callback):
        self.signals[signal] = callback

    def unconnect(self, signal):
        if signal in self.signals:
            del self.signals[signal]

    def update(self, signal, callback):
        if callback and isinstance(callback, types.FunctionType):
            self.connect(signal, callback)
        else:
            self.unconnect(signal)

