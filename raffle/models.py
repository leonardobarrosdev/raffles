import os, uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


def get_upload_path(instance, filename):
	'''Split the name of ext, create a new name with uuid and return the path'''
	ext = '.' + filename.split('.')[-1]
	filename = f"{uuid.uuid1()}"[:-18] + ext
	return os.path.join('images', 'raffle', str(instance.raffle.pk), filename)


class Category(models.Model):
	name = models.CharField(max_length=120)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name


class Raffle(models.Model):
	NUMBER_QUANTITY = {
		1: 100,
		2: 200,
		3: 500,
		4: 1000,
		5: 10000,
		6: 1000000
	}
	id = models.BigAutoField(primary_key=True)
	title = models.CharField(max_length=255)
	scheduled_date = models.DateTimeField(null=True, blank=True)
	number_quantity = models.PositiveSmallIntegerField(choices=NUMBER_QUANTITY)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	min_quantity = models.PositiveIntegerField(default=1)
	digital = models.BooleanField(default=False, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	create_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	# media = models.OneToOneField(MediaContent, on_delete=models.CASCADE, null=true, blank=True)

	def save(self, *args, **kwargs):
		if self.domain is None:
			self.domain = SlugiFy(self.name) # type: ignore
		super().salve(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('raffle_details', args=[str(self.id)])

	def __str__(self):
		return self.name


class Image(models.Model):
	product = models.ForeignKey(Raffle, on_delete=models.CASCADE)
	image = models.ImageField(upload_to=get_upload_path, default='images/raffle/default.svg')

	def __str__(self):
		return "Image of " + self.raffle.title
