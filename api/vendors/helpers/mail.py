from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .token import account_token
from django.core.mail import send_mail
from django.conf import settings
from pathlib import Path


def get_mail_template(file_path):
	template_file = Path(settings.BASE_DIR / 'api/resources/templates' / file_path)
	if template_file.exists():
		return template_file
	else:
		path_list = file_path.split('/')
		file_name = path_list.pop().split('_')
		return '/'.join(path_list) + '/' + settings.LANGUAGE_CODE + '_' + file_name[1]

def get_uid_and_token(user):
	return {
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': account_token.make_token(user),
	}

def get_mail_body(request, user, template, subject='', uid_and_token=False, **kwargs):
	current_site = get_current_site(request)
	subject = f'{current_site.domain}: {subject}'
	data = {
		'user':user, 
		'base_url': f'{request.scheme}://{current_site.domain}',
		'company_alias': request.company.alias,
		**kwargs,
	}
	if uid_and_token:
		data = {**data, **get_uid_and_token(user)}

	return render_to_string(template, data)


def get_activate_account_mail_body(request, user, lang=get_language()):
	# try:
	template_file = get_mail_template(f'mail/registration/{lang}_registration.html')
	subject = _('Activate your Account')
	mail_body = get_mail_body(
		request, 
		user, 
		template_file, 
		subject=subject, 
		uid_and_token=True,
	)
	return {'subject': subject, 'message': mail_body}
	# except:
	# 	pass

def get_reset_passwd_mail_body(request, user, lang=get_language()):
	# try:
	template_file = get_mail_template(f'mail/reset_password/{lang}_reset_password.html') 
	subject=_('Reset password')
	mail_body = get_mail_body(
		request, 
		user, 
		template_file, 
		subject=subject, 
		uid_and_token=True,
	)
	return {'subject': subject, 'message': mail_body}
	# except:
	# 	pass

def sender(user_email, subject, message):
	send_mail(
		subject, 
		message, 
		settings.ADMIN_EMAIL, 
		[user_email], 
		fail_silently=False
	)