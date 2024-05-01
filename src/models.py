from django.db import models
import os, uuid


def get_upload_path(instance, filename):
	'''Split the name of ext, create a new name with uuid and return the path'''
	ext = '.' + filename.split('.')[1]
	filename = f"{uuid.uuid1()}"[:-18] + ext
	return os.path.join('images', 'raffle', str(instance.raffle.pk), filename)


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
	name = models.CharField(max_length=255)
	domain = models.SlugField(max_length=255, null=True, blank=True)
	scheduled_date = models.DateTimeField()
	number_quantity = models.IntegerField(choices=NUMBER_QUANTITY)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	min_quantity = models.PositiveIntegerField(default=1)
	google_tag_manage_id = models.CharField(max_length=255, null=True, blank=True)
	pixel_facebook = models.CharField(max_length=255, null=True, blank=True)
	youtube_video_link = models.CharField(max_length=255, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	create_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "Raffles"

	def salve(self, *args, **kwargs):
		if self.domain is None:
			self.domain = SlugiFy(self.name)
		super().salve(*arg, **kwargs)

	def __str__(self):
		return self.name


class AutomaticBuy(models.Model):
	quantity = models.PositiveIntegerField(default=0)
	more_popular = models.BooleanField(null=True)
	raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Automatic Buys'


class Category(models.Model):
	name = models.CharField(max_length=120, default='outros')
	raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name


class Image(models.Model):
	image = models.ImageField(upload_to=get_upload_path)
	raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)

	def __str__(self):
		return "Image of " + self.raffle.name


class Promotion(models.Model):
	number_quantity = models.PositiveIntegerField(default=0)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
	raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)


class AwardedQuota(models.Model):
	number = models.PositiveIntegerField(default=0)
	raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
