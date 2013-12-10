class Errors(Exception):
	pass

class API_Key_Error(Errors):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message