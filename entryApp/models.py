from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings

class Gender(models.Model):

	code = models.CharField(max_length=1, blank=False)
	description = models.CharField(max_length=15, blank=False)

	def __str__(self):
		return self.description


class MaritalStatus(models.Model):

	code = models.CharField(max_length=1, blank=False)
	description = models.CharField(max_length=15, blank=False)
	
	class Meta:
		verbose_name_plural = 'Marital Status'

	def __str__(self):
		return self.description


class Profile(AbstractUser):
	gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
	marital_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE, null=True)
	date_of_birth = models.DateField(null=True)
	number_of_children = models.IntegerField(null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	class Meta:

		ordering = ["-timestamp"]
		verbose_name_plural = 'Users'

	def __str__(self):
		return self.username

	def get_absolute_url(self):
		return reverse('reg_app.views.admin_function_list_view', 
			args=[str(self.id)])


