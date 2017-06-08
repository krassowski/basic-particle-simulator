sound_available = False

from threading import Thread
try:
    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
    from gi.repository import GObject
    sound_available = True
except ImportError:
    sound_available = False
    print('No Gst package in repository - the sound will not work.')
    print('Upgrade your GTK+ to have all features.')


class Sound:

    def __init__(self, frequency=587.33, length=250):

        if not sound_available:
            return

        Gst.init_check()
        self.frequency = frequency
        self.length = length
        # play in a separate thread - do not block simulation
        thread = Thread(target=self.play)
        thread.start()

    def play(self):
        if not sound_available:
            return False

        pipeline = Gst.Pipeline(name='note')
        source = Gst.ElementFactory.make('audiotestsrc', 'src')
        sink = Gst.ElementFactory.make('autoaudiosink', 'output')

        source.set_property('freq', self.frequency)
        pipeline.add(source)
        pipeline.add(sink)
        source.link(sink)
        pipeline.set_state(Gst.State.PLAYING)

        GObject.timeout_add(self.length, self.stop, pipeline)

    def stop(self, pipeline):
        if not sound_available:
            return False

        pipeline.set_state(Gst.State.NULL)
        return False


