'''
Session object is used to store either
AM or PM session. 
'''
class Session(object):

	def __init__(self, time_capacity):
		self.time_capacity = time_capacity.value
		self.remaining = time_capacity.value
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

	def is_valid(self):
		raise NotImplementedError

	def total_talk_duration(self):
		return self.time_capacity - self.remaining

	def __str__(self):
		return ''.join(str(self.talks))





