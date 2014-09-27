import sys
import random
from datetime import date, datetime, time, timedelta
from track import Track
from session import Session, AMSession, PMSession
from talk import Talk
from conference import Conference
import csv
from collections import defaultdict
from datetime import date, datetime, time, timedelta
'''
Define time constants that will
be used for sessions in this particular 
conference:

Morning session is allowed to be from:
9AM-12PM(3hrs) = 180mins 

Afternoon session starts at 1pm and can be as short as 4pm:
1PM-4PM(3hrs) = 180mins

Afternoon session can also last until 5pm:
1PM-5PM(4hrs) = 240mins
'''
SESSION_DURATION = {
	'AM': 180,
	'PM_MIN': 180,
	'PM_MAX': 240
}


'''
Define timings used for each session
'''
SESSION_TIMINGS = {
	
	'MORNING' : datetime.combine(date.today(), time(9, 0)),

	'LUNCH' : datetime.combine(date.today(), time(12, 0)) ,

	'AFTERNOON' : datetime.combine(date.today(), time(13, 0)) 

}

'''
Load a list of talks from CSV file
Filename: input.csv
Format:
<topic>,<duration>
For e.g:
"Ruby on Rails Legacy App Maintenance", 60
"A World Without HackerNews", 30
"User Interface CSS in Rails Apps", 30
'''
def load_talks_from_csv():
	talks = []

	input_file = open('input.csv', 'r', newline='')

	data = csv.reader(input_file)

	for line in data:
		if len(line) == 2:
			[topic, duration] = line
			talks.append(Talk(topic, int(duration)))

	return talks

'''
This is where the actual work will take place
'''
def main():

	all_talks = load_talks_from_csv()

	'''
	Sum up all the minutes for all the talks that we
	loaded from CSV
	'''
	total_time_for_all_talks = sum(t.duration for t in all_talks)



	i = 0

	while True:

		talks = list(all_talks)

		random.shuffle(talks)

		t1 = Track("Track One",
					AMSession(SESSION_DURATION['AM']), 
					PMSession(SESSION_DURATION['PM_MAX'], SESSION_DURATION['PM_MIN'])
		)

		t2 = Track("Track Two",
					AMSession(SESSION_DURATION['AM']), 
					PMSession(SESSION_DURATION['PM_MAX'], SESSION_DURATION['PM_MIN'])
		)


		c = Conference(SESSION_TIMINGS['MORNING'], 
						SESSION_TIMINGS['LUNCH'], 
						SESSION_TIMINGS['AFTERNOON'])
		c.append(t1)
		c.append(t2)

		'''
		Check to ensure that our sessions have been allocated enough
		time to fit in all the talks in the list
		'''
		if total_time_for_all_talks > c.time_allocated():
			print("Please allocate more space to the sessions in order to " + \
					"accomodate all the talks.\n" + \
					"Total talk time: {}\nTotal time allocated in sessions:{}\n\n".format(total_time_for_all_talks, c.time_allocated()))

			sys.exit()

		''' 
		Multi-capacity bin that we will populate with talks
		'''
		sessions = c.get_all_sessions()


		'''
		Loop while there are still talks that have yet to be allocated
		to a session
		'''
		while len(talks) != 0:

			'''
			Use this to break out of the loop if all sessions still have
			space in them but not big enough to accomodate the
			current talk
			for e.g.
			Python for beginners: 60mins
			Track 1, AM session: 30mins unallocated
			Track 1, PM session: 15mins unallocated
			Track 2, AM session: 5mins unallocated
			Track 2, PM session: 30mins unallocated
			'''
			can_fit_in_at_least_one_session = False

			''' 
			Start doing first-fit bin packing
			'''
			for session in sessions:
				if session.is_full():
					continue

				if session.append(talks[0]):
					can_fit_in_at_least_one_session = True
					talks.pop(0)
					break;

			if not can_fit_in_at_least_one_session:
				print("Sessions still have spaces in them " + \
						"but not big enough to accomodate this talk: \n{}\nSkipped this iteration\n\n".format(talks[0]))

				'''
				Skip this loop so we can work another permutation of talks
				'''
				break


		'''
		All talks have now been distributed successfully so now we just need to ensure 
		the conference passes the contraints of our itinerary
		'''
		if c.is_valid() and c.talk_count() == len(all_talks):
			print("Valid conference itinerary found at iteration: {}".format(i))
			print(c.schedule_string())
			break

		i += 1


if __name__ == "__main__":
    main()







