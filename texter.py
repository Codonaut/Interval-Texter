import random
import time
import os
from datetime import datetime, timedelta

from config import (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, 
	TWILIO_PHONE_NUMBER, MESSAGES, REST_HOURS)
import daemon
from twilio.rest import TwilioRestClient

random.seed(os.urandom(10))

def start_texting():
	twilio_client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
	start_time = datetime.now()
	next_message = None
	while True:
		get_next_send_times(start_time)
		next_message = next_send_message()
		if next_message:
			time.sleep((next_message['next_send'] - datetime.now()).total_seconds())
			now = datetime.now()
			if now < today_at_hour(now, REST_HOURS['start']) and now > today_at_hour(now, REST_HOURS['end']):
				twilio_client.sms.messages.create(body=random.choice(next_message['messages']),
		    		to=next_message['phone_number'],
		    		from_=TWILIO_PHONE_NUMBER)

def today_at_hour(now, hour):
	return datetime(now.year, now.month, now.day, hour)

def next_send_message():
	time_asc = sorted(MESSAGES, key=lambda x: x.get('next_send', datetime(4000, 1, 1)))
	for t in time_asc:
		if t['next_send'] > datetime.now():
			return t
	return None

def get_next_send_times(start_time):
	for message in MESSAGES:
		next_send = message.get('next_send')
		if not next_send:
			message['send_num'] = 0
			message['next_send'] = pick_next_send_time(message, start_time)
		elif next_send < datetime.now():
			message['send_num'] += 1
			message['next_send'] = pick_next_send_time(message, start_time)

def pick_next_send_time(message, start_time):
	''' Randomly picks a send time between start_time+interval*send_number 
		and start_time+interval*(send_number+1) 
	'''
	low = start_time + timedelta(seconds=message['interval']*message['send_num'])
	return low + timedelta(seconds=random.randint(0, message['interval']))


if __name__ == '__main__':
	with daemon.DaemonContext():
		start_texting()
