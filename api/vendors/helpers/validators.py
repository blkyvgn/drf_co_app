import re


# At least one letter, number or symbol (@$!%*#?&). Min 8 max 16.
passwd_regex = re.compile(r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*\d)(?=.*?[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$')
# letter, number or symbol (.-_)
email_regex = re.compile(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$')


def email_validation_check(email, error_msg=None):
	if re.fullmatch(email_regex, email) is None:
		# write to log
		return False
	return True

# ----------- for test only -----------
passwd_regex = re.compile(r'^[ 0-9]+$')
# -------------------------------------
def passwd_validation_check(passwd, error_msg=None):
	if re.fullmatch(passwd_regex, passwd) is None:
		# write to log
		return False
	return True

def birthdate_validation_check(date, error_msg=None):
	pass 

def phone_validation_check(phone, error_msg=None):
	pass 