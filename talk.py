class Talk(object):

	def __init__(self, topic, duration):
		self.topic = topic
		self.duration = duration

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "%s | %s" % (self.topic, str(self.duration))


