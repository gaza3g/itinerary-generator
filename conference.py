import itertools

from datetime import timedelta

from session import AMSession, PMSession

'''
Represents the entire conference that
stores all the tracks
'''
class Conference(object):

	def __init__(self, start_datetime, 
						lunch_datetime, 
						afternoon_datetime):

		self.tracks = []
		self.start_datetime = start_datetime
		self.lunch_datetime = lunch_datetime
		self.afternoon_datetime = afternoon_datetime

	def append(self, track):
		self.tracks.append(track)


	'''
	Get a total count of all the talks 
	inside all tracks
	'''
	def talk_count(self):
		return sum(t.talk_count() for t in self.tracks)

	'''
	Get a total duration of all the talks 
	inside all tracks
	'''
	def total_talk_duration(self):
		return sum(t.total_talk_duration() for t in self.tracks)


	'''
	Get a total of all time allocated for this conference
	'''
	def time_allocated(self):
		return sum(t.time_allocated() for t in self.tracks)


	'''
	Retrieve sessions inside all tracks
	'''
	def get_all_sessions(self):

		''' 
		Returns 2d list
		'''
		sessions = [t.sessions for t in self.tracks]

		'''
		Flatten 2d list so instead of:
		[ [Session, Session] , [Session, Session] ]
		we get:
		[ Session, Session , Session, Session ]
		'''
		return list(itertools.chain.from_iterable(sessions))

	def reset_sessions(self):

		for session in self.get_all_sessions():
			session.talks = []
			session.remaining = session.time_allocated



	'''
	Let 'tracks' do their own validation.
	We just need to make sure there aren't
	any invalid tracks.
	'''
	def is_valid(self):

		'''
		If one track is not valid, then
		this conference itinerary is not
		gonna work.
		'''
		for track in self.tracks:
			if not track.is_valid():
				return False

		return True



	'''
	Get data from tracks and sessions and generate
	a string which shows the scheduled events.
	'''
	def schedule_string(self):
		output = ""

		for track in self.tracks:

			current_time = self.start_datetime
			track_output = "%s \n" % track.label

			for session in track.sessions:

				if isinstance(session, AMSession):

					current_time = self.start_datetime

				elif isinstance(session, PMSession):

					'''
					Insert the Lunch event just between the last event 
					of the AM session and the first event for the PM session
					'''
					track_output += "%s\tLunch\n" % self.lunch_datetime.strftime("%I:%M %p")	

					current_time = self.afternoon_datetime


				for talk in session.talks:
					track_output += "%s\t%s %smins\n" % (current_time.strftime("%I:%M %p"), 
													talk.topic, 
													talk.duration)

					current_time = current_time + timedelta(minutes=talk.duration)


			track_output += "%s\tNetworking Event \n\n" % current_time.strftime("%I:%M %p")

			output += track_output

		return "\n\n%s\n\n" % output




