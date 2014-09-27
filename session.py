class Session(object):

	def __init__(self, label, time_capacity):
		self.label = label
		self.time_capacity = time_capacity
		self.remaining = time_capacity
		self.talks = []

	def append(self, talk):
		if self.remaining >= talk.duration:
			self.talks.append(talk)
			self.remaining = self.remaining - talk.duration
			return True
		else:
			return False

	def is_full(self):
		return self.remaining == 0

	def total_talk_duration(self):
		return self.time_capacity - self.remaining

	def __str__(self):
		return ''.join(str(self.talks))

