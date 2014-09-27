'''
Session object is used to store either
AM or PM session. 
'''
class Session(object):

	'''
	Time capacity refers to the amount of time 
	allocated for this session in minutes.
	for e.g
	If session is from 9AM-12PM then time allocated
	would be 180(3hrs)
	'''
	def __init__(self, time_allocated):
		self.time_allocated = time_allocated
		self.remaining = time_allocated
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

	def talk_count(self):
		return len(self.talks)

	def is_valid(self):
		raise NotImplementedError

	def total_talk_duration(self):
		return self.time_allocated - self.remaining

	def __str__(self):
		return ''.join(str(self.talks))


'''
For this session to be valid, the requirement is that
it has to be fully filled with no gaps. So 'self.remaining' 
has to be 0 in order for an AM session to be valid.
'''
class AMSession(Session):

	def __init__(self, time_allocated):
		self.remaining = time_allocated
		super(AMSession, self).__init__(time_allocated)

	def is_valid(self):
		return self.remaining == 0

'''
For the case of the PM session, we have the choice of
allowing it to end as follows: 
4PM <= end time <= 5PM
which means, 180 <= self.remaining <= 240
'''
class PMSession(Session):

	def __init__(self, time_allocated, minimum_duration):
		self.remaining = time_allocated
		self.minimum_duration = minimum_duration
		super(PMSession, self).__init__(time_allocated)

	def is_valid(self):
		return super(PMSession, self).total_talk_duration() > self.minimum_duration











