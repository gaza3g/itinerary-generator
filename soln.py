import sys
import random
from datetime import date, datetime, time, timedelta
from track import Track
from session import Session, AMSession, PMSession
from talk import Talk
from conference import Conference
import csv
from collections import defaultdict
from enum import Enum


SESSION_DURATION = {
	'AM': 180,
	'PM_MIN': 180,
	'PM_MAX': 240
}

def load_talks_from_csv():
	talks = []

	input_file = open('input.csv', 'r', newline='')

	data = csv.reader(input_file)

	for line in data:
		if len(line) == 2:
			[topic, duration] = line
			talks.append(Talk(topic, int(duration)))

	return talks


def main():

	all_talks = load_talks_from_csv()


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

		''' 
		Group available sessions from both tracks so that we can populate
		them later
		'''
		sessions = [t1.morning, t1.afternoon, t2.morning, t2.afternoon]



		'''
		first check to ensure that our sessions have been allocated enough
		time to fit in all the talks in the list
		'''
		total_time_for_all_talks = sum(t.duration for t in talks)
		total_time_capacity = sum(s.time_allocated for s in sessions) 

		if total_time_for_all_talks > total_time_capacity:
			print("Please allocate more space to the sessions in order to " + \
					"accomodate all the talks.\n" + \
					"Total talk time: {}\nTotal time allocated in sessions:{}\n\n".format(total_time_for_all_talks, total_time_capacity))
			break


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

			# Do first-fit bin packing
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
				break


		# if t1.is_schedule_valid() and \
		# 	 t2.is_schedule_valid() and \
		# 	 t1.total_talks() + t2.total_talks() == len(all_talks):			
		# 	print("Valid conference itinerary found at iteration: {}".format(i))
		# 	print(t1)
		# 	print(t2)
		# 	break
		c = Conference([t1,t2])



		if t1.is_valid() and \
			 t2.is_valid(): # and \
			 #t1.total_talks() + t2.total_talks() == len(all_talks):			
			print("Valid conference itinerary found at iteration: {}".format(i))
			print(t1)
			print(t2)
			print("total talks: ", c.talk_count(), "\nall talks: ", len(all_talks))
			break


		# if t1.morning.is_valid() and \
		# 	 t1.afternoon.is_valid() and \
		# 	 t2.morning.is_valid() and \
		# 	 t2.afternoon.is_valid() and \
		# 	 t1.total_talks() + t2.total_talks() == len(all_talks):			
		# 	print("Valid conference itinerary found at iteration: {}".format(i))
		# 	print(t1)
		# 	print(t2)
		# 	break


		i += 1


if __name__ == "__main__":
    main()







