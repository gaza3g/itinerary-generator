class Track(object):

	def __init__(self, label, *sessions):
		self.label = label
		# self.morning = morning
		# self.afternoon = afternoon
		self.sessions = sessions


	def talk_count(self):
		return sum(s.talk_count() for s in self.sessions)

	'''
	Let 'sessions' do their own validation.
	We just need to make sure there aren't
	any invalid session in this track.
	'''
	def is_valid(self):

		'''
		If either session is found to be invalid, 
		then this conference itinerary is not
		gonna work.
		'''
		for session in self.sessions:
			if not session.is_valid():
				return False

		return True
