TWILIO_ACCOUNT_SID = "enter_your_info_here"
TWILIO_AUTH_TOKEN  = "enter_your_info_here"
TWILIO_PHONE_NUMBER = 'enter_your_info_here'

MESSAGES = (
	{
		'phone_number': 'enter_your_info_here', # phone number to send to
		'interval': 0, # interval in seconds
		'messages': ('enter_your_info_here', 'enter_your_info_here') # tuple of messages to cycle through
	},
)


REST_HOURS = {'start': 24, 'end': 0} # Won't send texts within these hours