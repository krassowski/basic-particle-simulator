sound_avaliable = False

try:
	from gi.repository import Gst
	from gi.repository import GObject
	sound_avaliable = True
except:
	sound_avaliable = False
	print "No Gst package in repository - the sound will not work."
	print "Upgrade your GTK+ to have all featrues."

class Sound():

	def __init__(self, frequency=587.33, length=250):

		if not sound_avaliable:
			return None

		Gst.init_check()
		self.frequency = frequency
		self.length = length
		self.play()

	def play(self):
		if not sound_avaliable:
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
		if not sound_avaliable:
			return False

		pipeline.set_state(Gst.State.NULL)
		return False


