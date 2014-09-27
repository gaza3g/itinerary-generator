import sys
import random
from datetime import date, datetime, time, timedelta
from track import Track
from session import Session
from talk import Talk
import csv
from collections import defaultdict

MORNING_SESSION_DURATION = 180
MAX_AFTERNOON_SESSION_DURATION = 240
MIN_AFTERNOON_SESSION_DURATION = 180

TRACK1_MORNING_SESSION = "Track 1: Morning Session"
TRACK1_AFTERNOON_SESSION = "Track 1: Afternoon Session"
TRACK2_MORNING_SESSION = "Track 2: Morning Session"
TRACK2_AFTERNOON_SESSION = "Track 2: Afternoon Session"

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

		sessions = [
						Session(TRACK1_MORNING_SESSION, MORNING_SESSION_DURATION), 
						Session(TRACK1_AFTERNOON_SESSION, MAX_AFTERNOON_SESSION_DURATION), 
						Session(TRACK2_MORNING_SESSION, MORNING_SESSION_DURATION), 
						Session(TRACK2_AFTERNOON_SESSION, MAX_AFTERNOON_SESSION_DURATION)
					]

		t1 = Track("Track One", 
					sessions[0], 
					sessions[1], 
					MORNING_SESSION_DURATION, 
					MAX_AFTERNOON_SESSION_DURATION
			)

		t2 = Track("Track Two", sessions[2], sessions[3], MORNING_SESSION_DURATION, MAX_AFTERNOON_SESSION_DURATION)

		# sessions = [
		# 				Session(TRACK1_MORNING_SESSION, MORNING_SESSION_DURATION), 
		# 				Session(TRACK1_AFTERNOON_SESSION, MAX_AFTERNOON_SESSION_DURATION), 
		# 				Session(TRACK2_MORNING_SESSION, MORNING_SESSION_DURATION), 
		# 				Session(TRACK2_AFTERNOON_SESSION, MAX_AFTERNOON_SESSION_DURATION)
		# 			]


		# first check to ensure that our sessions have been allocated enough
		# time to fit in all the talks in the list
		total_time_for_all_talks = sum(t.duration for t in talks)
		total_time_capacity = sum(s.time_capacity for s in sessions) 

		if total_time_for_all_talks > total_time_capacity:
			print("Please allocate more space to the sessions in order to " + \
					"accomodate all the talks.\n" + \
					"Total talk time: {}\nTotal time allocated in sessions:{}\n\n".format(total_time_for_all_talks, total_time_capacity))
			break

		while len(talks) != 0:

			# Break out of the loop if all sessions still have
			# spaces in them but not big enough to accomodate the
			# current talk
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


		t1 = Track("Track One", sessions[0], sessions[1], MORNING_SESSION_DURATION, MAX_AFTERNOON_SESSION_DURATION)
		t2 = Track("Track Two", sessions[2], sessions[3], MORNING_SESSION_DURATION, MAX_AFTERNOON_SESSION_DURATION)

		if t1.is_schedule_valid() and \
			 t2.is_schedule_valid() and \
			 t1.total_talks() + t2.total_talks() == len(all_talks):			
			print("Valid conference itinerary found at iteration: {}".format(i))
			print(t1)
			print(t2)
			break

		i += 1


if __name__ == "__main__":
    main()