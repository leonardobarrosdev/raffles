from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
import os


def get_upload_path(instance, filename):
	'''Split the name of ext, create a new name with fname and return the path'''
	ext = '.' + filename.split('.')[-1]
	filename = str(instance.user.first_name) + ext
	return os.path.join('images', 'user', filename)


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""Create and save a user with the given email and password"""
		if not email:
			raise ValueError("The given email must be set")
		email = self.normalize_email(email)
		user = self.model(username=email, email=email, **extra_fields)
		user.password = make_password(password)
		user.save(using=self._db)
		return user

	def create_customer(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)
		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")
		return self._create_user(email, password, **extra_fields)

	def ban_user(self, request, queryset, **extra_fields):
		if extra_fields.get("is_superuser"):
			queryset.update(is_active = False)


class UserProfile(AbstractUser):
	email = models.EmailField(unique=True)
	cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
	phone = models.CharField("contato", max_length=11, null=True, blank=True)
	date_birth = models.DateField(null=True, blank=True)
	is_staff = models.BooleanField("Rifeiro", default=False)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["first_name"]

	objects = UserManager()

	def __str__(self):
		return self.first_name
