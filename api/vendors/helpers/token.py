from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import random 
import string

def get_random_string(length):
    ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class AccountTokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
		)

account_token = AccountTokenGenerator()