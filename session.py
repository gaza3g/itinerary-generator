'''
Session object is used to store either
AM or PM session. 
'''
class Session(object):

	def __init__(self, time_allocated):
		self.time_allocated = time_allocated
		self.remaining = time_allocated
		self.talks = []

	'''
	Append 'talk' to current list of talks and 
	update our remaining minutes. Return False
	if the duration of the talk is too long to
	fit in this session 
	'''
	def append(self, talk):
		if self.remaining >= talk.duration:
			self.talks.append(talk)
			self.remaining = self.remaining - talk.duration
			return True
		else:
			return False

	'''
	Session is full. Not accepting anymore talks
	'''
	def is_full(self):
		return self.remaining == 0


	'''
	Returns a count of the talks in this session
	'''
	def talk_count(self):
		return len(self.talks)


	'''
	To be implemented by subclass based on their
	own constraints
	'''
	def is_valid(self):
		raise NotImplementedError


	'''
	Number of minutes used by the talks already
	added to this session
	'''
	def total_talk_duration(self):
		return self.time_allocated - self.remaining


'''
For this session to be valid, the requirement is that
it has to be fully filled with no gaps. So 'self.remaining' 
has to be 0 in order for an AM session to be valid.
'''
class AMSession(Session):

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
		self.minimum_duration = minimum_duration
		super(PMSession, self).__init__(time_allocated)

	def is_valid(self):
		return self.total_talk_duration() > self.minimum_duration











