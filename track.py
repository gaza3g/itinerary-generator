from datetime import date, datetime, time, timedelta

class Track(object):

	def __init__(self, label, morning, afternoon, morning_duration, afternoon_duration):
		self.label = label
		self.morning = morning
		self.afternoon = afternoon

	def is_morning_schedule_valid(self):
		return self.morning.total_talk_duration() == 180

	def is_afternoon_schedule_valid(self):
		return self.afternoon.total_talk_duration() >= 180 and \
				self.afternoon.total_talk_duration() <= 240

	def total_talks(self):
		return len(self.morning.talks) + len(self.afternoon.talks)

	def networking_event_start_time(self):
		total_track_duration = self.morning.total_talk_duration() + \
								self.afternoon.total_talk_duration()

		# start at 10 to account for the 1hr Lunch 
		return datetime.combine(date.today(), time(10, 0)) + \
				timedelta(minutes=total_track_duration)


	def is_schedule_valid(self):
		return self.is_morning_schedule_valid() and self.is_afternoon_schedule_valid()

	def schedule_string(self):
		current_time = current_time = datetime.combine(date.today(), time(9, 0)) 
		output = "%s \n" % self.label

		for talk in self.morning.talks:
			output += "%s\t%s %smins\n" % (current_time.strftime("%I:%M %p"), 
											talk.topic, 
											talk.duration)

			current_time = current_time + timedelta(minutes=talk.duration)

		current_time = current_time = datetime.combine(date.today(), time(12, 0)) 
		output += "%s\tLunch\n" % current_time.strftime("%I:%M %p")

		current_time = current_time = datetime.combine(date.today(), time(13, 0)) 

		for talk in self.afternoon.talks:
			output += "%s\t%s %smins\n" % (current_time.strftime("%I:%M %p"), 
											talk.topic, 
											talk.duration)

			current_time = current_time + timedelta(minutes=talk.duration)

		output += "%s\tNetworking Event \n" % current_time.strftime("%I:%M %p")

		return output

	def __str__(self):
		return self.schedule_string()



