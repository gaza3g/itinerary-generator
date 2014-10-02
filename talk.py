'''
Simple talk class that represents
a particular talk in a conference 
that has a topic and a duration in
minutes
'''
class Talk(object):

	def __init__(self, topic, duration):
		self.topic = topic
		self.duration = duration


