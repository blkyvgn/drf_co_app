from django.db import models
from termcolor import colored
from django.conf import settings
from django.utils.encoding import force_str
from api.vendors.base.model import BaseModel
from django.utils.http import urlsafe_base64_decode
from api.apps.company.tasks.mail import send_email_celery_task
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from api.vendors.helpers.translation import tr
from api.vendors.helpers.mail import (
	get_activate_account_mail_body,
	get_reset_passwd_mail_body,
)
from django.contrib.auth.models import (
	AbstractBaseUser, 
	PermissionsMixin,
)
from api.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
)


class AccountManager(BaseUserManager):

	def create_user(self, username, email, password, **extra_fields):
		if not email:
			raise ValueError(_('The Email must be set'))
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		extra_fields.setdefault('is_verified', True)
		extra_fields.setdefault('type', Account.Type.ADMIN)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		print(colored('Use "su-admin" for access admin panel', 'green')) 
		return self.create_user(username, email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin, BaseModel, TimestampsMixin, SoftdeleteMixin):
	class Type(models.TextChoices):
		ADMIN    = 'ADMIN',    tr('admin')
		EMPLOYEE = 'EMPLOYEE', tr('employee')
		CUSTOMER = 'CUSTOMER', tr('customer')

	_type = models.CharField(db_column='type',
		max_length=15,
		choices=Type.choices,
		default=Type.CUSTOMER,
		verbose_name=(tr('type'))
	)

	username = models.CharField(
		max_length=80,
		unique=True,
	)
	email = models.EmailField(
		unique=True,
	)
	is_staff = models.BooleanField(
		default=False,
	)
	is_active = models.BooleanField(
		default=True,
	)
	is_verified = models.BooleanField(
		default=False,
	)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = AccountManager()

	class Meta:
		verbose_name =  _('Account')
		verbose_name_plural =  _('Accounts')
		ordering = ('-created_at',)
		permissions = [
			('view_dashboard',   'View page: Dashboard'),
			('change_password',  'Change account password'),
			('allow_chat',       'Allow chat'),
		]
		indexes = [
			models.Index(fields=['email',]),
			models.Index(fields=['username',]),
		]

	def __str__(self):
		return self.username
		
	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, val):
		self._type = val

	@classmethod
	def get_by_uid(cls, uidb64):
		try:
			uid = force_str(urlsafe_base64_decode(uidb64)) 
			user = cls.objs.get(pk=uid)
		except(TypeError, ValueError, OverflowError, user.DoesNotExist):
			user = None
		return user

	def create_profile(self, **kwargs):
		from api.apps.account.models.profile import Profile
		Profile.objects.create(account=self, **kwargs)

	def set_permissions(self):
		content_type = ContentType.objects.get_for_model(Account)
		accont_perms = Permission.objects.filter(content_type=content_type)
		for perm in accont_perms:
			self.user_permissions.add(perm)

	def send_registration_email(self, request):
		try:
			send_email_celery_task.delay(
				self.email, 
				get_activate_account_mail_body(request, self)
			)
		except:
			print('----------------------- mail body -------------------------')
			print(get_activate_account_mail_body(request, self))
			print('----------------------- ********* -------------------------')

	def send_reset_passwd_email(self, request):
		try:
			send_email_celery_task.delay(
				self.email, 
				get_reset_passwd_mail_body(request, self)
			)
		except:
			print('----------------------- mail body -------------------------')
			print(get_reset_passwd_mail_body(request, self))
			print('----------------------- ********* -------------------------')

class AdminManager(BaseUserManager):
	def get_queryset(self):
		return super().get_queryset().filter(type=Account.Type.ADMIN)

class Admin(Account):
	admin = AdminManager()

	class Meta:
		proxy = True

	def set_permissions(self):
		super().set_permissions()

	def save(self, *args, **kwargs):
		self.is_staff = True
		self.type = Account.Types.ADMIN
		super().save(*args, **kwargs)


class EmployeeManager(BaseUserManager):
	def get_queryset(self):
		return super().get_queryset().filter(type=Account.Type.EMPLOYEE)

class Employee(Account):
	employee = EmployeeManager()

	class Meta:
		proxy = True

	def set_permissions(self):
		super().set_permissions()

	def save(self, *args, **kwargs):
		self.is_staff = True
		self.type = Account.Type.EMPLOYEE
		super().save(*args, **kwargs)


class CustomerManager(BaseUserManager):
	def get_queryset(self):
		return super().get_queryset().filter(type=Account.Type.CUSTOMER)

class Customer(Account):
	customer = CustomerManager()

	class Meta:
		proxy = True

	def set_permissions(self):
		super().set_permissions()

	def save(self, *args, **kwargs):
		self.is_staff = False
		self.type = Account.Type.CUSTOMER
		super().save(*args, **kwargs)
